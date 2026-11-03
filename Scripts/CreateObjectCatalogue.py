"""Source-only object/appearance/artifact inventory. Never changes manual backlogs or assets."""
import ast,csv,json,re
from collections import Counter,defaultdict
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'Art/ObjectCatalogue'
REVISION='16ff59115315917b93185d026aeefea06db9b0f4'

def clean(text):
    return re.sub(r'/\*.*?\*/',lambda m:''.join('\n' if c=='\n' else ' ' for c in m[0]),text,flags=re.S)

def split_args(text):
    result=[];start=depth=0;quoted=escape=False
    for i,c in enumerate(text):
        if quoted:
            if escape:escape=False
            elif c=='\\':escape=True
            elif c=='"':quoted=False
        elif c=='"':quoted=True
        elif c=='(':depth+=1
        elif c==')':depth-=1
        elif c==',' and depth==0:result.append(text[start:i].strip());start=i+1
    result.append(text[start:].strip());return result

def call(text):
    match=re.match(r'\s*(\w+)\s*\(',text);assert match,text[:100]
    start=match.end();depth=1;quoted=escape=False
    for i in range(start,len(text)):
        c=text[i]
        if quoted:
            if escape:escape=False
            elif c=='\\':escape=True
            elif c=='"':quoted=False
        elif c=='"':quoted=True
        elif c=='(':depth+=1
        elif c==')':
            depth-=1
            if not depth:return match[1],split_args(text[start:i]),i+1
    raise ValueError('Unclosed macro: '+text[:80])

def tokens(text,replacements):
    return re.sub(r'"(?:\\.|[^"\\])*"|\b[A-Za-z_]\w*\b',lambda m:m[0] if m[0].startswith('"') else replacements.get(m[0],m[0]),text)

def cstring(text):
    parts=re.findall(r'"(?:\\.|[^"\\])*"',text)
    return ''.join(ast.literal_eval(s) for s in parts) if parts else None

def source_objects():
    lines=clean((ROOT/'upstream/NetHack/include/objects.h').read_text()).splitlines()
    macros={};aliases={};conditions=[];records=[];i=0
    def expand(name,args):
        if name=='OBJECT':return [tokens(a,aliases) for a in args]
        params,body=macros[name];assert len(params)==len(args),(name,len(params),len(args))
        expanded=tokens(tokens(body,dict(zip(params,args))),aliases)
        inner,values,_=call(expanded);return expand(inner,values)
    while i<len(lines):
        line=i+1;chunk=lines[i].strip();i+=1
        while chunk.endswith('\\'):
            chunk=chunk[:-1]+' '+lines[i].strip();i+=1
        if chunk.startswith('#'):
            directive=re.match(r'#\s*(\w+)\s*(.*)',chunk);kind,body=directive.groups()
            if kind in ['if','ifdef','ifndef']:conditions.append((line,kind+' '+body))
            elif kind=='endif':conditions.pop()
            elif kind in ['else','elif'] and conditions:conditions[-1]=(conditions[-1][0],kind+' '+body)
            elif kind=='define':
                m=re.match(r'(\w+)\(([^)]*)\)\s*(.*)',body)
                if m:
                    if m[1] not in ['OBJ','OBJECT','BITS','MARKER','HARDGEM']:macros[m[1]]=(split_args(m[2]),m[3])
                else:
                    m=re.match(r'(\w+)\s+(.*)',body)
                    if m:aliases[m[1]]=m[2]
            elif kind=='undef':macros.pop(body.strip(),None);aliases.pop(body.strip(),None)
            continue
        if not chunk or not re.match(r'\w+\s*\(',chunk):continue
        # Top-level invocations can span physical lines; preserve the starting source line.
        while True:
            try:name,args,end=call(chunk);break
            except ValueError:chunk+=' '+lines[i].strip();i+=1
        if name=='MARKER':continue
        values=expand(name,args)
        if len(values)==14:continue # Array terminator has no stable enum ID.
        assert len(values)==15,(line,name,values)
        _,obj,_=call(values[0]);_,bits,_=call(values[1]);assert len(obj)==2 and len(bits)==13
        ident=values[14].strip()
        if ident=='0' and all(cstring(v) is None for v in obj):continue
        assert re.fullmatch(r'[A-Z][A-Z0-9_]*',ident),ident
        cond=[c for n,c in conditions if 70<n<1645]
        record=dict(id=ident,name=cstring(obj[0]),default_description=cstring(obj[1]),source_class=values[3],
                    source=dict(path='upstream/NetHack/include/objects.h',line=line,macro=name,conditions=cond),
                    fields=dict(zip(['name_known','mergeable','uses_known','container','magical','charged','unique','nowish','big','tough','direction','subtype','material'],bits)),
                    property=values[2],probability=values[4],delay=values[5],weight=values[6],cost=values[7],small_damage=values[8],large_damage=values[9],oc1=values[10],oc2=values[11],nutrition=values[12],ascii_colour=values[13])
        record['scope']='deferred' if any(c.startswith('if 0') for c in cond) else 'conditional' if cond else 'normal'
        record['record_kind']='generic_display' if ident.startswith('GENERIC_') else 'dummy' if ident=='STRANGE_OBJECT' else 'appearance_only' if record['name'] is None else 'object_type'
        records.append(record)
    assert len({r['id'] for r in records})==len(records)
    return records

CLASSES={'WEAPON':'Weapons','ARMOR':'Armor','RING':'Rings','AMULET':'Amulets','TOOL':'Tools','FOOD':'Food','POTION':'Potions','SCROLL':'Scrolls','SPBOOK':'Spellbooks','WAND':'Wands','COIN':'Coins','GEM':'Gems and stones','ROCK':'Large rocks and statues','BALL':'Punishment gear','CHAIN':'Punishment gear','VENOM':'Venom','ILLOBJ':'Display auxiliaries'}
def family(r):
    cls=r['source_class'].removesuffix('_CLASS');sub=r['fields']['subtype'];name=r['name'] or r['default_description'] or ''
    if cls=='WEAPON' or r['source']['macro']=='WEPTOOL':
        if any(x in name for x in ['sword','katana','tsurugi','scimitar','saber']):return 'Swords and long blades'
        if any(x in name for x in ['dagger','knife','athame','scalpel','stiletto','tooth']):return 'Daggers and short blades'
        if sub in ['P_BOW','P_SLING','P_CROSSBOW']:return 'Launchers'
        if sub.startswith('-') or r['source']['macro']=='PROJECTILE':return 'Ammunition and thrown weapons'
        if sub in ['P_POLEARMS','P_LANCE','P_SPEAR','P_TRIDENT']:return 'Polearms and thrusting weapons'
        if sub in ['P_AXE','P_PICK_AXE']:return 'Axes and picks'
        if sub in ['P_WHIP','P_FLAIL']:return 'Flexible weapons'
        return 'Clubs, hammers and staves'
    if cls=='ARMOR':return {'ARM_SUIT':'Body armor','ARM_HELM':'Headwear','ARM_SHIELD':'Shields','ARM_GLOVES':'Gloves and gauntlets','ARM_BOOTS':'Footwear','ARM_CLOAK':'Cloaks','ARM_SHIRT':'Shirts'}.get(sub,'Armor review')
    if cls=='TOOL':
        if r['fields']['container']=='1':return 'Containers'
        if r['source']['macro']=='EYEWEAR':return 'Eyewear'
        if any(x in name for x in ['lamp','lantern','candle','candelabrum']):return 'Lights'
        if any(x in name for x in ['flute','harp','horn','bugle','drum','bell']):return 'Instruments and sound tools'
        if any(x in name for x in ['key','pick','card','tinning','leash','saddle','blindfold','towel','mirror','stethoscope','whistle']):return 'Hand tools and equipment'
        return 'Special tools and devices'
    return {'RING':'Bands and settings','AMULET':'Pendants','POTION':'Bottles and visible contents','SCROLL':'Rolled sheets and labels','SPBOOK':'Bindings and covers','WAND':'Rods and handles','GEM':'Faceted gems and rough stones','FOOD':'Food and organic objects','COIN':'Coins','ROCK':'Large stone forms','BALL':'Balls','CHAIN':'Chains','VENOM':'Splashes'}.get(cls,'Display symbols')

def shuffle_groups(records):
    active=[r for r in records if r['scope']!='deferred'];byid={r['id']:i for i,r in enumerate(active)}
    groups={}
    for cls in ['AMULET','POTION','RING','SCROLL','SPBOOK','WAND','VENOM']:
        candidates=[r for r in active if r['source_class']==cls+'_CLASS' and r['record_kind'] not in ['generic_display','dummy']]
        if cls=='POTION':candidates=candidates[:next(i for i,r in enumerate(candidates) if r['id']=='POT_WATER')]
        elif cls in ['AMULET','SCROLL','SPBOOK']:
            candidates=candidates[:next((i for i,r in enumerate(candidates) if r['fields']['unique']=='1' or r['fields']['magical']=='0'),len(candidates))]
        groups[cls.lower()+'_appearances']=[r['id'] for r in candidates if r['fields']['name_known']!='1']
    for start,end in [('HELMET','HELM_OF_TELEPATHY'),('LEATHER_GLOVES','GAUNTLETS_OF_DEXTERITY'),('CLOAK_OF_PROTECTION','CLOAK_OF_DISPLACEMENT'),('SPEED_BOOTS','LEVITATION_BOOTS')]:
        groups[start.lower()+'_appearances']=[r['id'] for r in active[byid[start]:byid[end]+1] if r['fields']['name_known']!='1']
    return groups

def artifacts():
    raw=clean((ROOT/'upstream/NetHack/include/artilist.h').read_text());result=[]
    for m in re.finditer(r'^\s*A\(',raw,re.M):
        name,args,_=call(raw[m.start():]);assert len(args)==17
        label=cstring(args[0])
        if not label:continue
        line=raw.count('\n',0,m.start())+1
        # Preserve the explicitly obsolete artifact separately from current ones.
        preceding=raw[:m.start()];scope='obsolete' if preceding.rfind('#if 0')>preceding.rfind('#endif') else 'normal'
        result.append(dict(id='ART_'+args[16],name=label,base_object_id=args[1],scope=scope,source=dict(path='upstream/NetHack/include/artilist.h',line=line),native_flags=args[2:5],attacks=args[5:8],invoked_property=args[8],alignment=args[9],role=args[10],ancestry=args[11],native_cost=args[14],glow_colour=args[15],asset_status='MVP live placement and native visible name verified; extended verification pending' if args[16] in {'MJOLLNIR','CLEAVER'} else 'not modelled',design_policy='Distinctive named treatment only when native displayed knowledge permits; otherwise retain the legal base appearance.'))
    assert len({a['id'] for a in result})==len(result);return result

def write_csv(path,rows,fields):
    with path.open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
        for r in rows:w.writerow({k:' / '.join(r[k]) if isinstance(r.get(k),list) else r.get(k,'') for k in fields})

def main():
    OUT.mkdir(parents=True,exist_ok=True);records=source_objects();groups=shuffle_groups(records)
    registry=json.loads((ROOT/'Art/ObjectInterpretations/object-assets.json').read_text())
    completed={r['id']:r for r in registry['objects'] if r['asset_status']=='generated and verified static draft'}
    tiletext=(ROOT/'upstream/NetHack/win/share/objects.txt').read_text()
    tiles=[dict(index=int(i),label=label) for i,label in re.findall(r'^# tile (\d+) \(([^\n]+)\)',tiletext,re.M)]
    active=[r for r in records if r['scope']!='deferred']
    atlas=json.loads((ROOT/'Art/TileFallback/atlas.json').read_text())
    atlas_indices={t['source_index']:t['tile_index'] for t in atlas['tiles'] if t['source']=='objects' and not t['statue']}
    appearances=[]
    used={};last_index=-1
    for r in records:
        name,desc=r['name'],r['default_description']
        exact=(desc+' / '+name) if name and desc else name or desc
        candidates=[t for t in tiles if t['label']==exact]
        if not candidates:candidates=[t for t in tiles if name and name in t['label'].split(' / ') and (not desc or desc in t['label'].split(' / '))]
        candidates=[t for t in candidates if t['index']>last_index]
        # Identical labels can recur in different classes (silver/polymorph book and wand).
        # Resolve by source order only after exact label matching, never a guessed glyph offset.
        if len(candidates)>1:candidates=[min(candidates,key=lambda t:t['index'])]
        if not candidates and r['scope']=='deferred':continue
        assert len(candidates)==1,(r['id'],name,desc,candidates)
        t=candidates[0];i=t['index'];assert i not in used,(r['id'],used.get(i));used[i]=r['id'];last_index=i
        r['official_tile']=dict(path='upstream/NetHack/win/share/objects.txt',file_local_index=i,combined_atlas_index=atlas_indices[i],label=t['label'])
    assert len(used)==len(tiles),(len(used),len(tiles),[t for t in tiles if t['index'] not in used])
    for r in records:
        cls=r['source_class'].removesuffix('_CLASS');r['category']=CLASSES[cls];r['visual_family']=family(r)
        r['shuffle_group']=next((k for k,v in groups.items() if r['id'] in v),None)
        r['asset_status']='generated and verified static draft' if r['id'] in completed else 'not modelled'
        r['evidence']=completed.get(r['id'],{}).get('evidence')
        if r['id'] in {'LEATHER_ARMOR','STUDDED_LEATHER_ARMOR','CHAIN_MAIL','BANDED_MAIL','ELVEN_MITHRIL_COAT','DWARVISH_MITHRIL_COAT','DWARVISH_CLOAK'}:
            r['asset_status']='MVP live placement verified; finishing and extended verification pending'
            r['evidence']='Docs/ArmorStudy.md'
        if r['id'] in {'PLATE_MAIL','CRYSTAL_PLATE_MAIL','BRONZE_PLATE_MAIL'} or r['id'] in {c+'_DRAGON_SCALE_MAIL' for c in ['GRAY','GOLD','SILVER','RED','WHITE','ORANGE','BLACK','BLUE','GREEN','YELLOW']}:
            r['asset_status']='MVP live placement verified; finishing and extended verification pending'
            r['evidence']='Docs/ArmorBatch2.md'
        if r['id'] in {'LONG_SWORD','SCIMITAR','KATANA'}:
            r['asset_status']='MVP live placement verified; finishing and extended verification pending'
            r['evidence']='Docs/WeaponBatch1.md'
        if r['id'] in {'DAGGER','SHORT_SWORD','SPEAR'}:
            r['asset_status']='MVP live placement verified; finishing and extended verification pending'
            r['evidence']='Docs/WeaponBatch2.md'
        if r['id'] in completed:r['draft_scope']=completed[r['id']].get('scope','Selected fixed object presentation; see evidence.')
        r['design_tags']=[r['fields']['material'],r['fields']['subtype']]
        r['style_tags']=[tag for tag in ['elven','orcish','dwarvish'] if (r['name'] or '').startswith(tag+' ')]
        if r['record_kind'] in ['object_type','appearance_only'] and r['scope']!='deferred':
            appearances.append(dict(id='APPEARANCE_'+r['id'],source_slot_id=r['id'],category=r['category'],visual_family=r['visual_family'],label=r['default_description'] or r['name'],shuffle_group=r['shuffle_group'],official_tile=r['official_tile'],asset_status=r['asset_status'],evidence=r['evidence'],policy='Source slot, not a live identity-to-look binding. Resolve the native displayed appearance/tile at runtime; default source effect pairing is not fixed.'))
    art=artifacts();ids={r['id'] for r in records}
    assert all(a['base_object_id'] in ids for a in art)
    named=[r for r in records if r['record_kind']=='object_type' and r['scope']!='deferred']
    summary=dict(named_object_types=len(named),unconditional_named_types=sum(r['scope']=='normal' for r in named),conditional_named_types=sum(r['scope']=='conditional' for r in named),verified_object_drafts=len(completed),remaining_named_types=len(named)-len(completed),source_appearance_slots=len(appearances),extra_appearance_only_slots=sum(r['record_kind']=='appearance_only' and r['scope']!='deferred' for r in records),display_auxiliaries=sum(r['record_kind'] in ['generic_display','dummy'] for r in records),deferred_types=sum(r['scope']=='deferred' for r in records),official_object_tiles=len(tiles),deferred_source_tiles=sum(r['scope']=='deferred' and 'official_tile' in r for r in records),artifacts=sum(a['scope']=='normal' for a in art),obsolete_artifacts=sum(a['scope']=='obsolete' for a in art),by_category=dict(Counter(r['category'] for r in named)))
    base=dict(schema_version=1,source_revision=REVISION,scope='Source inventory including MAIL_STRUCTURES and separately marked deferred/auxiliary slots; numeric enum values are not runtime identity keys.',summary=summary,appearance_policy='Identity and appearance are separate. Default descriptions/materials/tiles may be shuffled; use native displayed knowledge, never hidden object type.',shuffle_source='upstream/NetHack/src/o_init.c::obj_shuffle_range / shuffle_all / shuffle',shuffle_groups=groups)
    for filename,data in [('objects.json',{**base,'objects':records}),('appearances.json',{**base,'appearances':appearances}),('artifacts.json',dict(source_revision=REVISION,artifacts=art)),('summary.json',summary)]:
        (OUT/filename).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    flat=[dict(id=r['id'],name=r['name'],default_description=r['default_description'],category=r['category'],visual_family=r['visual_family'],material=r['fields']['material'],subtype=r['fields']['subtype'],scope=r['scope'],record_kind=r['record_kind'],shuffle_group=r['shuffle_group'],tile_index=r.get('official_tile',{}).get('file_local_index'),source_line=r['source']['line'],asset_status=r['asset_status'],evidence=r['evidence']) for r in records]
    write_csv(OUT/'objects.csv',flat,list(flat[0]))
    write_csv(OUT/'appearances.csv',appearances,['id','source_slot_id','category','visual_family','label','shuffle_group','asset_status','evidence'])
    write_csv(OUT/'artifacts.csv',art,['id','name','base_object_id','scope','alignment','role','ancestry','asset_status'])
    md=['# Object source inventory','',f"{len(named)} named types ({summary['conditional_named_types']} conditional), {len(appearances)} source appearance slots, {summary['artifacts']} current artifact overlays.",'','Generated by `Scripts/CreateObjectCatalogue.py`; progress lives in [object-backlog.md](../../object-backlog.md). This file is regenerated; the manual backlog is not.','', 'Hierarchy: native category â†’ useful visual family. Materials, culture and finish are facets, not a mandatory inheritance tree. Default appearance/effect pairings are not live bindings.','', '| Category | Named source types | Verified drafts |','| --- | ---: | ---: |']
    for cat,count in summary['by_category'].items():md.append(f"| {cat} | {count} | {sum(r['id'] in completed for r in named if r['category']==cat)} |")
    for kind,heading in [('object_type','Named object types'),('appearance_only','Extra shuffled appearance slots'),('generic_display','Generic display auxiliaries'),('dummy','Dummy source entry')]:
        md+=['',f'## {heading}','']
        for r in records:
            if r['record_kind']!=kind:continue
            md.append(f"- `{r['id']}` â€” {r['name'] or r['default_description']} | {r['category']} / {r['visual_family']} | {r['scope']} | {r['asset_status']}")
    md+=['','## Artifact overlays','']+[f"- `{a['id']}` â€” {a['name']} â†’ `{a['base_object_id']}` ({a['scope']}); appearance gated by native knowledge." for a in art]
    (OUT/'Inventory.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
    print('OBJECT_CATALOGUE_READY '+json.dumps(summary),flush=True)

if __name__=='__main__':main()

