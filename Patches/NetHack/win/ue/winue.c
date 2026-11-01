/* nUthEck window port, created 2026-10-30.
 * NetHack may be freely redistributed. See dat/license for details.
 * NDJSON display events over stdout; sequenced input replies over stdin.
 * Only window glyphs and the hero's own status cross this boundary. */
#include "hack.h"
extern struct window_procs tty_procs;
#include "func_tab.h"
#include "dlb.h"
#include <io.h>
#include <fcntl.h>

#ifdef UEBRIDGE
typedef struct { anything id; char accelerator, group; char *text; unsigned int flags; } UEEntry;
typedef struct { int type, count; UEEntry *entries; char prompt[BUFSZ]; } UEWindow;
static UEWindow ue_windows[64];
static int sequence;
static char reply[16384];
struct window_procs ue_procs = { "ue", wp_shim };

static void quote(const char *s)
{
    const unsigned char *p = (const unsigned char *) (s ? s : "");
    putchar('"');
    for (; *p; ++p) {
        if (*p == '"' || *p == '\\') { putchar('\\'); putchar(*p); }
        else if (*p < 32) printf("\\u%04x", *p);
        else putchar(*p);
    }
    putchar('"');
}

static void message(const char *s)
{
    printf("{\"event\":\"message\",\"text\":"); quote(s); puts("}");
}

static void state(void)
{
    int x,y;
    if (u.ux < 1 || u.ux >= COLNO) return;
    printf("{\"event\":\"state\",\"x\":%d,\"y\":%d,\"moves\":%ld,\"hp\":%d,\"maxhp\":%d,\"ac\":%d,\"level\":%d,\"depth\":%d,\"dungeon\":%d,\"vision\":\"",
        u.ux-1,u.uy,svm.moves,Upolyd ? u.mh : u.uhp,Upolyd ? u.mhmax : u.uhpmax,u.uac,u.ulevel,depth(&u.uz),u.uz.dnum);
    for(y=0;y<ROWNO;++y) for(x=1;x<COLNO;++x) putchar(cansee(x,y)?'1':'0');
    /* Illumination is disclosed only on currently visible squares. */
    printf("\",\"lighting\":\"");
    for(y=0;y<ROWNO;++y) for(x=1;x<COLNO;++x)
        putchar('0' + (cansee(x,y) ? ((levl[x][y].lit ? 1 : 0)
                                  | (templit(x,y) ? 2 : 0)) : 0));
    printf("\",\"hero_race\":"); quote(gu.urace.noun ? gu.urace.noun : "");
    printf(",\"hero_polymorphed\":%s}\n",Upolyd ? "true" : "false");
}

static const char *request(const char *type, const char *text)
{
    int seq = ++sequence;
    state();
    printf("{\"event\":\"input\",\"seq\":%d,\"type\":",seq); quote(type);
    printf(",\"text\":"); quote(text); puts("}"); fflush(stdout);
    while (fgets(reply,sizeof reply,stdin)) {
        char *p;
        long got = strtol(reply,&p,10);
        if (got != seq || *p != '\t') continue;
        ++p; p[strcspn(p,"\r\n")] = 0;
        return p;
    }
    /* EOF follows the core's hangup path, saving and removing session locks. */
#ifdef HANGUPHANDLING
    end_of_input();
#endif
    exit(EXIT_SUCCESS);
}

static int keyrequest(const char *type, const char *text)
{
    return atoi(request(type,text));
}

static void freewindow(winid w)
{
    int i;
    if(w<1 || w>=64) return;
    for(i=0;i<ue_windows[w].count;++i) free(ue_windows[w].entries[i].text);
    free(ue_windows[w].entries); ue_windows[w].entries=0; ue_windows[w].count=0; ue_windows[w].prompt[0]=0;
}
static winid ue_create(int type)
{
    int w; for(w=1;w<64;++w) if(!ue_windows[w].type) { ue_windows[w].type=type; return w; }
    panic("UE window limit"); return WIN_ERR;
}
static void ue_clear(winid w)
{
    if(w<1 || w>=64) return;
    freewindow(w);
    if(ue_windows[w].type==NHW_MAP) puts("{\"event\":\"clear\"}");
}
static void ue_destroy(winid w) { freewindow(w); if(w>0 && w<64) ue_windows[w].type=0; }
static void ue_add(winid w,const glyph_info *gi,const ANY_P *id,char ch,char group,int attr,int clr,const char *text,unsigned int flags)
{
    UEEntry *e;
    if(w<1 || w>=64) return;
    ue_windows[w].entries=(UEEntry*)realloc(ue_windows[w].entries,(ue_windows[w].count+1)*sizeof(UEEntry));
    e=&ue_windows[w].entries[ue_windows[w].count++]; memset(e,0,sizeof *e);
    if(id) e->id=*id;
    e->accelerator=ch; e->group=group; e->text=_strdup(text?text:""); e->flags=flags;
}
static void ue_put(winid w,int attr,const char *text)
{
    if(w>0 && w<64 && (ue_windows[w].type==NHW_TEXT || ue_windows[w].type==NHW_MENU))
        ue_add(w,0,0,0,0,attr,0,text,0);
    else if(w<1 || w>=64 || ue_windows[w].type!=NHW_STATUS) message(text);
}
static void sendmenu(winid w,int how)
{
    int i,automatic=0;
    printf("{\"event\":\"menu\",\"how\":%d,\"title\":",how); quote(ue_windows[w].prompt);
    printf(",\"items\":[");
    for(i=0;i<ue_windows[w].count;++i) {
        UEEntry *e=&ue_windows[w].entries[i];
        char ch=e->accelerator;
        if(e->id.a_void && !ch) { ch=automatic<26?'a'+automatic:'A'+automatic-26; ++automatic; }
        if(i) putchar(',');
        printf("{\"index\":%d,\"key\":%d,\"group\":%d,\"selectable\":%s,\"selected\":%s,\"text\":",i,(unsigned char)ch,(unsigned char)e->group,e->id.a_void?"true":"false",(e->flags & MENU_ITEMFLAGS_SELECTED)?"true":"false");
        quote(e->text); putchar('}');
    }
    puts("]}");
}
static int ue_select(winid w,int how,MENU_ITEM_P **out)
{
    const char *p; int count=0;
    *out=0; sendmenu(w,how);
    p=request("menu",ue_windows[w].prompt);
    if(!strcmp(p,"-1")) return -1;
    *out=(MENU_ITEM_P*)alloc((ue_windows[w].count+1)*sizeof(MENU_ITEM_P));
    while(*p) {
        char *end; long index=strtol(p,&end,10), amount=-1;
        if(end==p) break;
        p=end;
        if(*p==':') { amount=strtol(p+1,&end,10); p=end; }
        if(index>=0 && index<ue_windows[w].count && ue_windows[w].entries[index].id.a_void) {
            (*out)[count].item=ue_windows[w].entries[index].id;
            (*out)[count].count=amount; ++count;
        }
        if(*p==',') ++p; else break;
        if(how==PICK_ONE) break;
    }
    if(!count) { free(*out); *out=0; }
    return count;
}
static void ue_display(winid w,boolean blocking)
{
    if(w>0 && w<64 && (ue_windows[w].type==NHW_TEXT || ue_windows[w].type==NHW_MENU)) {
        sendmenu(w,PICK_NONE); (void)request("menu",ue_windows[w].prompt);
    } else if(blocking && w==WIN_MESSAGE) (void)keyrequest("continue","Press Space or Enter to continue");
}
static void ue_start(winid w,unsigned long behavior) { freewindow(w); }
static void ue_end(winid w,const char *prompt) { if(w>0 && w<64) Strcpy(ue_windows[w].prompt,prompt?prompt:""); }
static void ue_file(const char *name,boolean complain)
{
    dlb *f=dlb_fopen(name,"r"); char line[BUFSZ]; winid w;
    if(!f) { if(complain) message("Unable to open requested text file."); return; }
    w=ue_create(NHW_TEXT);
    while(dlb_fgets(line,sizeof line,f)) { line[strcspn(line,"\r\n")]=0; ue_put(w,0,line); }
    dlb_fclose(f); ue_end(w,name); ue_display(w,TRUE); ue_destroy(w);
}
static const char *terrain(int glyph)
{
    int s;
    if(!glyph_is_cmap(glyph)) return "none";
    s=glyph_to_cmap(glyph);
    if(s>=S_vwall && s<=S_trwall) return "wall";
    if(s==S_stone) return "stone";
    if(s==S_vcdoor || s==S_hcdoor) return "closed";
    if(s==S_vodoor || s==S_hodoor) return "open";
    if(s==S_pool || s==S_water) return "water";
    if(s==S_lava || s==S_lavawall) return "lava";
    if(s==S_tree || s==S_bars) return "wall";
    if(s==S_upstair || s==S_upladder || s==S_brupstair || s==S_brupladder) return "up";
    if(s==S_dnstair || s==S_dnladder || s==S_brdnstair || s==S_brdnladder) return "down";
    if(s==S_fountain) return "fountain";
    if(s==S_sink) return "sink";
    if(s>=S_arrow_trap && s<=S_polymorph_trap) return "trap";
    return "floor";
}
static void ue_glyph(winid w,coordxy x,coordxy y,const glyph_info *fg,const glyph_info *bg)
{
    int g=fg->glyph; const char *kind="terrain",*t=terrain(g);
    if(x<1 || x>=COLNO || y<0 || y>=ROWNO) return;
    if(g==GLYPH_UNEXPLORED || g==GLYPH_NOTHING) kind="unknown";
    else if(glyph_is_pet(g)) kind="pet";
    else if(glyph_is_monster(g) || glyph_is_invisible(g)) kind="monster";
    else if(glyph_is_object(g)) kind="item";
    else if(!glyph_is_cmap(g)) kind="effect";
    if(x==u.ux && y==u.uy && !strcmp(kind,"monster")) kind="hero";
    if(!strcmp(t,"none") && bg) t=terrain(bg->glyph);
    printf("{\"event\":\"tile\",\"x\":%d,\"y\":%d,\"glyph\":%d,\"kind\":",x-1,y,g); quote(kind);
    printf(",\"terrain\":"); quote(t);
    /* nUthEck 2026-10-31: resolved by NetHack's native tile map, which also
       shuffles unidentified object appearances. No object/monster world lookup. */
    if (g >= 0 && g < MAX_GLYPH)
        printf(",\"tile_index\":%d", (int) fg->gm.tileidx);
    /* Resolve only the displayed glyph, never the hidden monster at (x,y). */
    if (glyph_is_monster(g)) {
        int m = glyph_to_mon(g);
        boolean female = glyph_is_normal_female_monster(g)
            || glyph_is_female_pet(g) || glyph_is_detected_female_monster(g)
            || glyph_is_ridden_female_monster(g);
        if (m >= LOW_PM && m < NUMMONS) {
            printf(",\"display_monster\":"); quote(mons[m].pmnames[NEUTRAL]);
            printf(",\"female\":%s",female?"true":"false");
        }
    }
    /* Whitelist non-randomised appearances from the displayed glyph only.
       Never inspect floor objects, contents, quantity, traps or lock state. */
    if (glyph_is_object(g)) {
        int o = glyph_to_obj(g);
        const char *appearance = o == LARGE_BOX ? "large box"
            : o == CHEST ? "chest" : o == GOLD_PIECE ? "gold piece"
            : o == CORPSE ? "corpse" : 0;
        if (appearance) {
            printf(",\"display_object\":"); quote(appearance);
        }
    }
    {
        int tg=glyph_is_cmap(g)?g:(bg?bg->glyph:g);
        int s=glyph_is_cmap(tg)?glyph_to_cmap(tg):-1;
        printf(",\"symbol\":%d,\"horizontal\":%s}\n",fg->ttychar,(s==S_hcdoor || s==S_hodoor)?"true":"false");
    }
}
static void ue_init(int *argc,char **argv) { iflags.window_inited=TRUE; puts("{\"event\":\"hello\",\"protocol\":1,\"cols\":79,\"rows\":21}"); }
static void ue_player(void) { (void)genl_player_setup(80); }
static void ue_name(void) { const char *s=request("line","What is your name?"); copynchars(svp.plname,*s?s:"Adventurer",PL_NSIZ-1); }
static void ue_exit(const char *s) { if(s && *s) message(s); puts("{\"event\":\"end\"}"); }
static void ue_void(void) {}
static void ue_suspend(const char *s) {}
static void ue_curs(winid w,int x,int y) { if(w==WIN_MAP) printf("{\"event\":\"cursor\",\"x\":%d,\"y\":%d}\n",x-1,y); }
static void ue_int(int n) {}
static void ue_xy(int x,int y) {}
static void ue_str(const char *s) {}
static int ue_prev(void) { return 0; }
static int ue_getch(void) { return keyrequest("key","Choose a key or direction"); }
static int ue_poskey(coordxy *x,coordxy *y,int *mod)
{
    const char *type=program_state.input_state==commandInp?"command":program_state.input_state==getposInp?"position":"key";
    *x=*y=0; *mod=0;
    return keyrequest(type,program_state.input_state==getposInp?"Move the cursor; . selects, Esc cancels":"");
}
static char ue_yn(const char *query,const char *choices,char def)
{
    char full[BUFSZ*2]; int ch;
    Snprintf(full,sizeof full,"%s %s%s%s",query,choices?"[":"",choices?choices:"",choices?"]":"");
    do { ch=keyrequest(program_state.input_state==getdirInp?"direction":"yn",full); if(ch=='\r' || ch=='\n' || ch==' ') ch=def?def:'\033'; }
    while(ch!='\033' && choices && !strchr(choices,ch));
    if(ch=='\033' && choices) ch=strchr(choices,'q')?'q':strchr(choices,'n')?'n':def?def:choices[0];
    if(ch=='#') { const char *n=request("line","How many?"); yn_number=atol(n); }
    return (char)ch;
}
static char ue_message_menu(char let,int how,const char *s) { message(s); return (char)keyrequest("key","Press a key"); }
static void ue_line(const char *query,char *out) { const char *s=request("line",query); copynchars(out,s,BUFSZ-1); }
static int ue_ext(void)
{
    int i; const char *s=request("line","Extended command (#):");
    for(i=0;extcmdlist[i].ef_txt;++i) if(!strcmpi(s,extcmdlist[i].ef_txt)) return i;
    return -1;
}
static char *ue_history(boolean init) { return 0; }
static void ue_puthistory(const char *s,boolean restoring) {}
static void ue_status(int field,genericptr_t ptr,int chg,int percent,int color,unsigned long *masks) { if(field==BL_FLUSH) state(); }
static void ue_inventory(int flags) {}
static win_request_info *ue_ctrl(winid w,int request,win_request_info *info) { return info; }
static void ue_position(char *s) {}
static void ue_color(int color,long rgb,int reverse) {}
static char *ue_colors(void) { return 0; }

void ue_win_init(int direction)
{
    if(direction!=WININIT) return;
    windowprocs=tty_procs;
    windowprocs.name="ue"; windowprocs.wp_id=wp_shim;
    windowprocs.wincap=WC_ASCII_MAP|WC_COLOR;
    windowprocs.wincap2=WC2_FLUSH_STATUS|WC2_RESET_STATUS;
    windowprocs.win_init_nhwindows=ue_init; windowprocs.win_player_selection=ue_player;
    windowprocs.win_askname=ue_name; windowprocs.win_get_nh_event=ue_void;
    windowprocs.win_exit_nhwindows=ue_exit; windowprocs.win_suspend_nhwindows=ue_suspend; windowprocs.win_resume_nhwindows=ue_void;
    windowprocs.win_create_nhwindow=ue_create; windowprocs.win_clear_nhwindow=ue_clear;
    windowprocs.win_display_nhwindow=ue_display; windowprocs.win_destroy_nhwindow=ue_destroy;
    windowprocs.win_curs=ue_curs; windowprocs.win_putstr=ue_put; windowprocs.win_putmixed=genl_putmixed;
    windowprocs.win_display_file=ue_file; windowprocs.win_start_menu=ue_start; windowprocs.win_add_menu=ue_add;
    windowprocs.win_end_menu=ue_end; windowprocs.win_select_menu=ue_select; windowprocs.win_message_menu=ue_message_menu;
    windowprocs.win_mark_synch=ue_void; windowprocs.win_wait_synch=ue_void;
#ifdef CLIPPING
    windowprocs.win_cliparound=ue_xy;
#endif
#ifdef POSITIONBAR
    windowprocs.win_update_positionbar=ue_position;
#endif
    windowprocs.win_print_glyph=ue_glyph; windowprocs.win_raw_print=message; windowprocs.win_raw_print_bold=message;
    windowprocs.win_nhgetch=ue_getch; windowprocs.win_nh_poskey=ue_poskey;
    windowprocs.win_nhbell=ue_void; windowprocs.win_doprev_message=ue_prev;
    windowprocs.win_yn_function=ue_yn; windowprocs.win_getlin=ue_line; windowprocs.win_get_ext_cmd=ue_ext;
    windowprocs.win_number_pad=ue_int; windowprocs.win_delay_output=ue_void;
#ifdef CHANGE_COLOR
    windowprocs.win_change_color=ue_color; windowprocs.win_get_color_string=ue_colors;
#endif
    windowprocs.win_outrip=genl_outrip; windowprocs.win_preference_update=ue_str;
    windowprocs.win_getmsghistory=ue_history; windowprocs.win_putmsghistory=ue_puthistory;
    windowprocs.win_status_init=genl_status_init; windowprocs.win_status_finish=genl_status_finish;
    windowprocs.win_status_enablefield=genl_status_enablefield; windowprocs.win_status_update=ue_status;
    windowprocs.win_can_suspend=genl_can_suspend_no; windowprocs.win_update_inventory=ue_inventory; windowprocs.win_ctrl_nhwindow=ue_ctrl;
}

boolean ue_bridge_bootstrap(int *argc,char **argv)
{
    int i,j; const char *root=0; char path[4096]; FILE *config;
    for(i=1;i<*argc;++i) if(!strncmp(argv[i],"--ue-root=",10)) {
        root=argv[i]+10;
        _putenv_s("NUTHECK_SESSION",root);
        for(j=i;j<*argc;++j) argv[j]=argv[j+1]; --*argc; break;
    }
    if(!root) return FALSE;
    Snprintf(path,sizeof path,"%s/.nethackrc",root);
    config=fopen(path,"wx");
    if(config) {
        fputs("# nUthEck session defaults (2026-10-30)\nOPTIONS=number_pad:0,!tutorial,!legacy,!news,time,lit_corridor\n",config);
        fclose(config);
    }
    _setmode(_fileno(stdin),_O_BINARY); _setmode(_fileno(stdout),_O_BINARY);
    setvbuf(stdout,0,_IONBF,0);
    return TRUE;
}
#endif
