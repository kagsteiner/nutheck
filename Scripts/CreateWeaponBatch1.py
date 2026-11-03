"""Three ordinary swords with distinct section geometry and complete fittings."""
import sys,math,json,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from CreatureGeometry import *
import CreatureGeometry as g
OUT=ROOT/'Art/ObjectInterpretations';GROUPS=['long_sword','scimitar','katana']
manifest=OUT/'weapon-batch1-protected.json'
if not manifest.exists():
    files=[p for f in ['CreatureInterpretations','ObjectInterpretations','EnvironmentInterpretations','TileFallback'] for p in (ROOT/'Art'/f).glob('*.fbx')]
    manifest.write_text(json.dumps({p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in files},indent=2))
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for key,c,rough,metal in [('sword_steel',(.38,.45,.49),.23,1),('sword_edge',(.66,.72,.76),.17,1),('sword_brass',(.48,.28,.07),.30,.85),('sword_leather',(.12,.025,.015),.72,0),('sword_wood',(.10,.045,.016),.56,0),('katana_wrap',(.012,.025,.036),.76,0),('katana_underlay',(.56,.51,.36),.85,0)]:
    COLORS[key]=c;m=bpy.data.materials.new(key);m.use_nodes=True;m.diffuse_color=(*c,1);s=m.node_tree.nodes['Principled BSDF'];s.inputs['Roughness'].default_value=rough;s.inputs['Metallic'].default_value=metal;MATS[key]=m
def section(key,t):
    if key=='long_sword':return 0,.335+.895*t,.032*(1-.30*t)
    if key=='scimitar':return .145*t*t,.315+.790*t,.029+.009*math.sin(math.pi*t)
    return .058*t*t,.405+.850*t,.024-.005*t
def blade(key):
    stations=[i*.90/28 for i in range(29)]+[.94,.97,.99,1.0];verts=[];faces=[]
    for t in stations:
        x,z,w=section(key,t);tip=max(.016,min(1,(1-t)/(.10 if key=='long_sword' else .055)))
        w*=tip;thick=max(.0004,.0052*tip)
        if key=='long_sword':
            # Recessed central fuller, broad lands and two sharpened edges.
            cross=[(-1,-.10),(-.72,-1),(-.26,-.84),(0,-.42),(.26,-.84),(.72,-1),(1,-.10),(1,.10),(.72,1),(.26,.84),(0,.42),(-.26,.84),(-.72,1),(-1,.10)]
        else:
            # Flat spine on -X, raised shinogi/land and thin cutting edge on +X.
            cross=[(-1,-.72),(.10,-1),(1,-.09),(1,.09),(.10,1),(-1,.72)]
        for a,b in cross:verts.append((x+a*w,b*thick,z))
    N=len(cross)
    for j in range(len(stations)-1):
        for i in range(N):a=j*N+i;b=j*N+(i+1)%N;faces.append((a,b,b+N,a+N))
    faces.extend([tuple(reversed(range(N))),tuple((len(stations)-1)*N+i for i in range(N))])
    mm=bpy.data.meshes.new(key+'_blade_sections');mm.from_pydata(verts,[],faces);mm.update();o=bpy.data.objects.new('blade',mm);bpy.context.collection.objects.link(o);g.finish(o,'forged_blade','sword_steel');o['blade_section_count']=len(stations);o['double_edged']=key=='long_sword'
def cylinder(name,at,radius,depth,color,scale=(1,1,1)):
    bpy.ops.mesh.primitive_cylinder_add(vertices=64,radius=radius,depth=depth,location=at);o=bpy.context.object;o.scale=scale;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);g.finish(o,name,color)
    mod=o.modifiers.new('Soft fitting edge','BEVEL');mod.width=min(.0015,depth*.20);mod.segments=3
    return o
for key in GROUPS:
    g.GROUP=key;blade(key)
    if key=='long_sword':
        limb('leather_grip',[(0,0,.09),(0,0,.16),(0,0,.323)],[.018,.020,.017],'sword_leather')
        limb('steel_crossguard',[(-.13,0,.305),(-.09,0,.325),(0,0,.328),(.09,0,.325),(.13,0,.305)],[.008,.010,.012,.010,.008],'sword_steel')
        box('ricasso_collar',(0,0,.338),(.066,.023,.032),'sword_steel',.004)
        pommel=cylinder('wheel_pommel',(0,0,.052),.032,.025,'sword_steel');pommel.rotation_euler.x=math.pi/2
        for side in [-1,1]:orb('pommel_inlay',(0,side*.013,.052),(.012,.0025,.012),'sword_brass')
        for j in range(15):
            z=.102+j*.0115;cylinder('grip_binding',(0,0,z),.020,.0022,'sword_leather')
    elif key=='scimitar':
        limb('curved_wood_grip',[(-.026,0,.052),(-.022,0,.12),(0,0,.205),(0,0,.294)],[.026,.022,.019,.020],'sword_wood')
        limb('hooked_pommel',[(-.026,0,.055),(-.055,0,.044),(-.067,0,.062)],[.026,.023,.012],'sword_brass')
        limb('brass_quillons',[(-.115,0,.290),(-.065,0,.302),(0,0,.300),(.068,0,.292),(.112,0,.270)],[.007,.009,.012,.009,.007],'sword_brass')
        for face in [-1,1]:
            limb('guard_langet',[(0,face*.018,.255),(0,face*.019,.300),(0,face*.018,.347)],[.003,.012,.002],'sword_brass')
            for z in [.115,.205]:orb('grip_pin',(-.015 if z<.15 else 0,face*.022,z),(.004,.003,.004),'sword_brass')
        for z in [.084,.267]:cylinder('grip_collar',(-.021 if z<.1 else 0,0,z),.025,.014,'sword_brass')
    else:
        box('textured_grip_underlay',(0,0,.221),(.043,.030,.270),'katana_underlay',.008)
        for face in [-1,1]:
            for j in range(10):
                z=.097+j*.025
                for direction in [-1,1]:limb('crossed_textile_wrap',[(-.020,face*.017,z),(.020,face*.017,z+direction*.022)],[.0035,.0035],'katana_wrap')
            for z in [.145,.270]:orb('small_menuki',(0,face*.018,z),(.006,.0025,.005),'sword_brass')
        for z in [.079,.361]:box('matching_hilt_cap',(0,0,z),(.050,.037,.018),'sword_brass',.004)
        cylinder('oval_tsuba',(0,0,.382),.066,.009,'sword_steel',(1,.75,1))
        for z in [.374,.390]:cylinder('seppa',(0,0,z),.030,.003,'sword_brass',(1,.70,1))
        box('habaki',(0,0,.410),(.055,.023,.035),'sword_brass',.003)
        # Restrained four-point brass tsuba accents, not an effect/rarity emblem.
        for i in range(4):
            a=math.tau*i/4;orb('tsuba_pin',(.049*math.cos(a),.034*math.sin(a),.388),(.003,.003,.0018),'sword_brass')
def pigment(o,p,c,colors):
    if o.get('blade_section_count'):
        key=o['creature'];base=.335 if key=='long_sword' else .315 if key=='scimitar' else .405;length=.895 if key=='long_sword' else .790 if key=='scimitar' else .850
        t=max(0,min(1,(p.z-base)/length));x,z,w=section(key,t);a=(p.x-x)/max(.001,w)
        if key=='long_sword' and abs(a)<.27:return (.20,.26,.29)
        if (abs(a)>.71 if key=='long_sword' else a>.20):return colors['sword_edge']
        return c
    if o['pigment']=='sword_wood':
        f=.78+.19*math.sin(p.x*630+p.y*590+math.sin(p.z*14));return tuple(v*f for v in c)
    return c
BLEND_NAME='WeaponBatch1.blend';REPORT_NAME='projection-report-weapon-batch1.json';PIGMENT_FUNCTION=pigment
SOURCE_TILE_NAMES={'long_sword':'long sword','scimitar':'curved sword / scimitar','katana':'samurai sword / katana'};SPATIAL_MASK_KEYS=GROUPS
pipeline=Path(__file__).with_name('CreatureBatch2Pipeline.py').read_text().replace('win/share/monsters.txt','win/share/objects.txt')
strip_lights='''
# Tall neutral softboxes reveal polished blade lands and cutting bevels.
for at,power in [((-1,-3,1.7),650),((2,2,1.5),450)]:
    data=bpy.data.lights.new('Blade reflection strip','AREA');data.energy=power;data.shape='RECTANGLE';data.size=2.0;data.size_y=3.0
    o=bpy.data.objects.new('Blade reflection strip',data);bpy.context.collection.objects.link(o);o.location=at;o.rotation_euler=(Vector((0,0,.65))-o.location).to_track_quat('-Z','Y').to_euler()
'''
pipeline=pipeline.replace("scene.render.film_transparent=True;",strip_lights+"\nscene.render.film_transparent=True;")
exec(compile(pipeline,'WeaponBatch1Pipeline','exec'))
