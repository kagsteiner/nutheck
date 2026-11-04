"""Three independent ordinary sword constructions, with complete hilts and sections."""
import sys,math,json,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from CreatureGeometry import *
import CreatureGeometry as g
OUT=ROOT/'Art/ObjectInterpretations';GROUPS=['silver_saber','broadsword','two_handed_sword']
manifest=OUT/'weapon-batch4-protected.json'
if not manifest.exists():manifest.write_text(json.dumps({p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'Art').rglob('*.fbx') if p.stem not in GROUPS},indent=2))
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for k,c,rough,metal in [('w4_steel',(.38,.46,.52),.26,1),('w4_edge',(.71,.77,.82),.19,1),('w4_silver',(.74,.79,.83),.22,1),('w4_brass',(.48,.29,.085),.29,.85),('w4_dark',(.09,.13,.16),.34,1),('w4_leather',(.09,.025,.013),.72,0),('w4_blue_wrap',(.012,.035,.062),.73,0)]:
    COLORS[k]=c;m=bpy.data.materials.new(k);m.use_nodes=True;m.diffuse_color=(*c,1)
    s=m.node_tree.nodes['Principled BSDF'];s.inputs['Roughness'].default_value=rough;s.inputs['Metallic'].default_value=metal;MATS[k]=m

def cylinder(name,at,r,depth,color,normal=None,scale=(1,1,1)):
    bpy.ops.mesh.primitive_cylinder_add(vertices=48,radius=r,depth=depth,location=at);o=bpy.context.object;o.scale=scale
    if normal:o.rotation_euler=Vector(normal).to_track_quat('Z','Y').to_euler()
    bpy.ops.object.transform_apply(location=False,rotation=True,scale=True)
    g.finish(o,name,color);b=o.modifiers.new('Worked fitting bevel','BEVEL');b.width=min(.002,depth*.18);b.segments=3;return o

def ring(name,at,r,minor,color):
    bpy.ops.mesh.primitive_torus_add(major_radius=r,minor_radius=minor,major_segments=48,minor_segments=10,location=at,rotation=(math.pi/2,0,0))
    o=bpy.context.object;bpy.ops.object.transform_apply(location=False,rotation=True,scale=True)
    for p in o.data.polygons:p.use_smooth=True
    return g.finish(o,name,color)

def section(key,t):
    if key=='silver_saber':return .13*t*t,.265+.855*t,.024*(1-.40*t)
    if key=='broadsword':return 0,.300+.805*t,.043*(1-.22*t)
    return 0,.640+1.020*t,.033*(1-.33*t)

def blade(key):
    stations=[j*.84/28 for j in range(29)]+[.89,.93,.96,.98,.995,1.]
    if key=='silver_saber':cross=[(-1,-.72),(-.45,-1),(.12,-.86),(1,-.05),(1,.05),(.12,.86),(-.45,1),(-1,.72)]
    elif key=='broadsword':
        # Two genuine recessed channels separated by a raised central rib.
        face=[(-1,-.06),(-.76,-1),(-.57,-.93),(-.44,-.40),(-.27,-.40),(-.17,-.93),(0,-1.04),(.17,-.93),(.27,-.40),(.44,-.40),(.57,-.93),(.76,-1),(1,-.06)]
        cross=face+[(x,-y) for x,y in reversed(face)]
    else:cross=[(-1,-.06),(-.70,-.92),(0,-1.18),(.70,-.92),(1,-.06),(1,.06),(.70,.92),(0,1.18),(-.70,.92),(-1,.06)]
    verts=[];faces=[]
    for t in stations:
        x,z,w=section(key,t);tip=max(.012,min(1,(1-t)/(.13 if key=='silver_saber' else .18)))
        for a,b in cross:verts.append((x+a*w*tip,b*max(.0003,.005*tip),z))
    n=len(cross)
    for j in range(len(stations)-1):
        for i in range(n):a=j*n+i;b=j*n+(i+1)%n;faces.append((a,b,b+n,a+n))
    faces += [tuple(reversed(range(n))),tuple((len(stations)-1)*n+i for i in range(n))]
    m=bpy.data.meshes.new('Forged sections');m.from_pydata(verts,[],faces);m.update();o=bpy.data.objects.new('blade',m);bpy.context.collection.objects.link(o)
    g.finish(o,'curved_single_edge' if key=='silver_saber' else 'double_fuller_blade' if key=='broadsword' else 'diamond_section_blade','w4_silver' if key=='silver_saber' else 'w4_steel')
    o['crafted_blade']=True;o['section_count']=len(stations)

for key in GROUPS:
    g.GROUP=key;blade(key)
    if key=='silver_saber':
        limb('shaped_blue_grip',[(-.017,0,.041),(-.012,0,.105),(0,0,.185),(0,0,.250)],[.024,.021,.018,.018],'w4_blue_wrap')
        for j in range(11):cylinder('fine_grip_binding',(-.014+.014*j/10,0,.064+j*.015),.021,.0025,'w4_blue_wrap',scale=(1,.80,1))
        cylinder('oval_guard',(0,0,.255),.062,.009,'w4_silver',scale=(1.4,.60,1))
        limb('swept_knuckle_bow',[(.070,0,.255),(.096,0,.208),(.095,0,.110),(.068,0,.050),(-.015,0,.027)],[.006,.0065,.007,.007,.010],'w4_silver')
        limb('rear_quillon',[(-.045,0,.256),(-.095,0,.261),(-.119,0,.280)],[.008,.006,.005],'w4_silver')
        cylinder('heel_cap',(-.017,0,.033),.028,.025,'w4_silver',scale=(1,.85,1))
        for side in [-1,1]:
            limb('guard_langet',[(0,side*.016,.226),(0,side*.016,.256),(0,side*.012,.290)],[.004,.010,.003],'w4_silver')
            for z in [.085,.19]:orb('grip_pin',(-.012 if z<.1 else 0,side*.019,z),(.003,.002,.003),'w4_silver')
    elif key=='broadsword':
        limb('short_oval_leather_grip',[(0,0,.087),(0,0,.15),(0,0,.275)],[.022,.024,.020],'w4_leather')
        for j in range(12):cylinder('raised_leather_wrap',(0,0,.099+j*.014),.023,.003,'w4_leather',scale=(1,.78,1))
        limb('downturned_crossguard',[(-.145,0,.264),(-.110,0,.284),(0,0,.290),(.110,0,.284),(.145,0,.264)],[.007,.010,.014,.010,.007],'w4_steel')
        cylinder('coin_pommel',(0,0,.045),.038,.024,'w4_steel',(0,1,0))
        for side in [-1,1]:
            cylinder('pommel_border',(0,side*.013,.045),.030,.003,'w4_brass',(0,1,0))
            cylinder('pommel_recess',(0,side*.015,.045),.022,.003,'w4_dark',(0,1,0))
            orb('peened_tang',(0,side*.017,.045),(.006,.003,.006),'w4_steel')
        box('fitted_blade_collar',(0,0,.302),(.088,.023,.030),'w4_steel',.003)
    else:
        limb('long_two_hand_grip',[(0,0,.090),(0,0,.23),(0,0,.414)],[.026,.024,.021],'w4_leather')
        for j in range(20):cylinder('two_hand_binding',(0,0,.105+j*.015),.025,.003,'w4_leather',scale=(1,.82,1))
        orb('scent_stopper_pommel',(0,0,.052),(.033,.025,.048),'w4_steel')
        for z in [.10,.409]:cylinder('grip_ferrule',(0,0,z),.027,.012,'w4_dark',scale=(1,.85,1))
        limb('long_curved_quillons',[(-.225,0,.467),(-.18,0,.435),(0,0,.430),(.18,0,.435),(.225,0,.467)],[.009,.010,.016,.010,.009],'w4_steel')
        for side in [-1,1]:ring('parry_ring',(side*.075,0,.467),.038,.004,'w4_steel')
        box('unsharpened_ricasso',(0,0,.548),(.052,.014,.210),'w4_dark',.002)
        for side in [-1,1]:limb('ricasso_hook',[(side*.020,0,.663),(side*.068,0,.685),(side*.078,0,.716)],[.012,.009,.004],'w4_steel')
    parts=[o for o in bpy.data.objects if o.type=='MESH' and o.get('creature')==key]
    low=min((o.matrix_world@v.co).z for o in parts for v in o.data.vertices)
    for o in parts:o.location.z-=low

def pigment(o,p,c,colors):
    if o.get('crafted_blade'):
        x,z,w=section(o['creature'],max(0,min(1,(p.z-(.265 if o['creature']=='silver_saber' else .300 if o['creature']=='broadsword' else .640))/(.855 if o['creature']=='silver_saber' else .805 if o['creature']=='broadsword' else 1.020))))
        a=(p.x-x)/max(.001,w)
        if o['creature']=='broadsword' and .27<abs(a)<.55:return (.20,.28,.33)
        if abs(a)>.72:return colors['w4_silver'] if o['creature']=='silver_saber' else colors['w4_edge']
    return c
BLEND_NAME='WeaponBatch4.blend';REPORT_NAME='projection-report-weapon-batch4.json';PIGMENT_FUNCTION=pigment
SOURCE_TILE_NAMES={'silver_saber':'silver saber','broadsword':'broadsword','two_handed_sword':'two-handed sword'}
pipeline=Path(__file__).with_name('CreatureBatch2Pipeline.py').read_text(encoding='utf-8').replace('win/share/monsters.txt','win/share/objects.txt')
pipeline=pipeline.replace('target_width=max(x for x,y in target)-min(x for x,y in target)+1','target_width=13').replace('target_height=max(y for x,y in target)-min(y for x,y in target)+1','target_height=13')
lights="""
for at,power in [((-1,-3,1.0),500),((2,2,1.5),350)]:
    data=bpy.data.lights.new('Blade reflection strip','AREA');data.energy=power;data.shape='RECTANGLE';data.size=2.;data.size_y=3.
    o=bpy.data.objects.new('Blade reflection strip',data);bpy.context.collection.objects.link(o);o.location=at;o.rotation_euler=(Vector((0,0,.65))-o.location).to_track_quat('-Z','Y').to_euler()
"""
pipeline=pipeline.replace('scene.render.film_transparent=True;',lights+'\nscene.render.film_transparent=True;')
exec(compile(pipeline,'WeaponBatch4Pipeline','exec'))
