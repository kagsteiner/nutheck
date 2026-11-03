"""Shared icon shopkeeper and complete static carved altars; source facts in docs."""
import math,bpy
import CreatureGeometry as g
from CreatureGeometry import orb,limb,box
from HumanPlayerFamily import human_player,garment

def shopkeeper():
    key='shopkeeper';g.GROUP=key
    body=human_player(key,False)
    # Reuse compatible human construction, retaining complete hands and seated eyes.
    for o in list(bpy.context.scene.objects):
        if o.type!='MESH' or o.get('creature')!=key:continue
        if any(t in o.name for t in ['hair_cap','short_waist_garment','_belt','_toe']):bpy.data.objects.remove(o,do_unlink=True);continue
        for field in ['human_player','player_form','sex']:
            if field in o:del o[field]
        o['shared_shopkeeper_sexes']=True
        if o.get('pigment') in ['human_green','human_gold','human_brow']:o['pigment']='shop_brown';o.data.materials.clear();o.data.materials.append(g.MATS['shop_brown'])
    body['anatomy_source']='HumanPlayerFamily human construction; no earlier asset changed'
    shopkeeper_outfit()

def shopkeeper_outfit():
    g.GROUP='shopkeeper'
    # Fitted blue/cyan jacket, green trousers, black hat and brown shoes follow tile.
    pieces=[orb('jacket_chest',(0,0,1.15),(.239,.159,.220),'shop_cyan'),orb('jacket_waist',(0,0,1.00),(.185,.142,.19),'shop_cyan')]
    for side in [-1,1]:
        pieces.append(orb('jacket_shoulder',(side*.217,0,1.267),(.098,.092,.100),'shop_cyan'))
        pieces.append(limb('jacket_arm',[(side*.217,0,1.255),(side*.280,-.008,1.06),(side*.295,-.035,.89)],[.091,.076,.049],'shop_cyan'))
        limb('cuff_'+str(side),[(side*.295,-.035,.905),(side*.295,-.035,.878)],[.048,.047],'shop_dark')
        limb('trouser_'+str(side),[(side*.102,0,.81),(side*.119,-.005,.46),(side*.122,.007,.29),(side*.122,0,.07)],[.112,.082,.077,.067],'shop_green')
        orb('shoe_'+str(side),(side*.122,-.048,.045),(.065,.115,.044),'shop_brown')
    garment('trouser_waist',[(.70,.183,.137),(.81,.187,.138),(.91,.177,.139)],'shop_green')
    garment('collar',[(1.28,.078,.075),(1.36,.064,.065)],'shop_dark')
    # Broad hat brim is genuine dark upper anatomy; right/lower black tile is shadow.
    brim=orb('hat_brim',(0,-.005,1.675),(.177,.145,.022),'shop_dark');brim['hat_module']=True
    crown=orb('hat_crown',(0,.005,1.71),(.121,.106,.084),'shop_dark');crown['hat_module']=True
    # Thin sculpted seams stay on the clothing, not a guessed bag/shield/weapon.
    g.sculpt_union(pieces,'jacket','shop_cyan',.006)

def altar(kind):
    g.GROUP='altar_'+kind
    box('stepped_foot',(0,0,.035),(.86,.62,.070),'altar_'+kind,.015)
    box('lower_step',(0,0,.095),(.75,.54,.055),'altar_'+kind,.012)
    box('stone_pedestal',(0,0,.285),(.56,.40,.33),'altar_'+kind,.022)
    box('upper_cornice',(0,0,.455),(.70,.51,.065),'altar_'+kind,.014)
    top=box('offering_slab',(0,0,.525),(.88,.64,.09),'altar_'+kind,.020);top['altar_top']=True
    sub=top.modifiers.new('Mineral paint sampling grid','SUBSURF');sub.subdivision_type='SIMPLE';sub.levels=4
    # Recessed border is fitted stone detail, independent of shrine/ownership state.
    for side in [-1,1]:
        box('rim_long_'+str(side),(0,side*.276,.575),(.80,.026,.014),'altar_'+kind,.004)
        box('rim_short_'+str(side),(side*.382,0,.575),(.026,.53,.014),'altar_'+kind,.004)
    if kind=='other':
        # Static white ray inlay interprets the displayed sanctum tile's white rays.
        for i in range(12):
            a=math.tau*i/12
            ray=limb('white_ray_inlay_'+str(i),[(.12*math.cos(a),.12*math.sin(a),.571),(.235*math.cos(a),.235*math.sin(a),.571)],[.004,.003],'altar_white');ray['static_ray_inlay']=True

def pigment(obj,p,base,colors):
    if obj.name=='shopkeeper_human_anatomy' and p.z<1.39:
        if p.z>.90:return colors['shop_blue' if abs(p.x)>.225 else 'shop_cyan']
        if abs(p.x)<.23:return colors['shop_green'] if p.z>.09 else colors['shop_brown']
    if obj.name=='shopkeeper_jacket':
        if p.z<.91 and abs(p.x)<.23:return colors['shop_green']
        if abs(p.x)>.225:return colors['shop_blue']
        if abs(p.x)<.007 and p.y<-.10 and .90<p.z<1.27:return colors['shop_blue']
    if obj['creature'].startswith('altar_'):
        if obj.get('static_ray_inlay'):return base
        grain=.95+.025*math.sin(p.x*197+p.y*133+p.z*151)+.02*math.sin(p.x*319-p.y*241)
        if obj.get('altar_top') and p.z>.55 and abs(p.x)<.36 and abs(p.y)<.25:
            kind=obj['creature'][6:]
            noise=math.sin(p.x*34+p.y*17)*math.sin(p.y*41-p.x*9)
            threshold={'unaligned':-.25,'chaotic':-.05,'neutral':.20,'lawful':.54,'other':2}[kind]
            if noise>threshold:
                t=min(.82,(noise-threshold)*1.6)
                base=tuple(a*(1-t)+b*t for a,b in zip(base,colors['altar_red']))
        return tuple(v*grain for v in base)
    return base
