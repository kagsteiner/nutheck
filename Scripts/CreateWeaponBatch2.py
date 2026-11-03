"""Batch-specific editable dagger, short sword and socketed spear."""
import sys,math,json,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from CreatureGeometry import *
import CreatureGeometry as g
OUT=ROOT/'Art/ObjectInterpretations';GROUPS=['dagger','short_sword','spear']
manifest=OUT/'weapon-batch2-protected.json'
if not manifest.exists():
    files=sorted(p for p in (ROOT/'Art').rglob('*.fbx') if p.stem not in GROUPS)
    manifest.write_text(json.dumps({p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in files},indent=2))
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for key,c,rough,metal in [('weapon2_iron',(.34,.40,.44),.25,1),('weapon2_edge',(.67,.72,.75),.18,1),('weapon2_brass',(.43,.26,.075),.30,.8),('weapon2_leather',(.075,.027,.018),.78,0),('weapon2_wood',(.22,.105,.037),.59,0)]:
    COLORS[key]=c;m=bpy.data.materials.new(key);m.use_nodes=True;m.diffuse_color=(*c,1);s=m.node_tree.nodes['Principled BSDF'];s.inputs['Roughness'].default_value=rough;s.inputs['Metallic'].default_value=metal;MATS[key]=m

def ring(name,z,r,depth,color='weapon2_iron'):
    bpy.ops.mesh.primitive_cylinder_add(vertices=48,radius=r,depth=depth,location=(0,0,z));o=bpy.context.object;g.finish(o,name,color)
    mod=o.modifiers.new('Turned fitting bevel','BEVEL');mod.width=min(.0015,depth*.18);mod.segments=3
    return o

def blade(key,stations):
    verts=[];faces=[]
    # A raised central ridge, broad blade lands and genuinely thin edges, both faces.
    cross=[(-1,0),(-.72,-.48),(0,-1),(.72,-.48),(1,0),(.72,.48),(0,1),(-.72,.48)]
    for z,w,d in stations:
        for x,y in cross:verts.append((x*w,y*d,z))
    for j in range(len(stations)-1):
        for i in range(8):a=j*8+i;b=j*8+(i+1)%8;faces.append((a,b,b+8,a+8))
    faces.extend([tuple(reversed(range(8))),tuple((len(stations)-1)*8+i for i in range(8))])
    mm=bpy.data.meshes.new(key+'_forged_section');mm.from_pydata(verts,[],faces);mm.update();o=bpy.data.objects.new('blade',mm);bpy.context.collection.objects.link(o);g.finish(o,'forged_blade','weapon2_iron');o['blade_section_count']=len(stations);o['double_edged']=True

for key in GROUPS:
    g.GROUP=key
    if key=='dagger':
        blade(key,[(.172,.023,.0045),(.195,.028,.005),(.32,.022,.0044),(.405,.012,.003),(.47,.0005,.0004)])
        limb('waisted_leather_grip',[(0,0,.038),(0,0,.075),(0,0,.12),(0,0,.157)],[.016,.014,.013,.016],'weapon2_leather')
        limb('swept_guard',[(-.066,0,.156),(-.048,0,.17),(0,0,.172),(.048,0,.17),(.066,0,.156)],[.005,.007,.009,.007,.005],'weapon2_iron')
        orb('faceted_scent_stop_pommel',(0,0,.022),(.023,.016,.022),'weapon2_iron')
        for z in [.043,.15]:ring('grip_ferrule',z,.017,.009,'weapon2_brass')
        for j in range(9):ring('raised_leather_binding',.054+j*.010,.015,.002,'weapon2_leather')
        for side in [-1,1]:orb('peened_tang',(0,side*.015,.022),(.004,.002,.004),'weapon2_brass')
    elif key=='short_sword':
        blade(key,[(.204,.033,.0055),(.245,.039,.006),(.39,.029,.0055),(.55,.038,.005),(.65,.027,.004),(.77,.0005,.0004)])
        # Broad waisted blade, compact boat guard, carved wooden grip: distinct from long sword.
        limb('carved_wood_grip',[(0,0,.058),(0,0,.086),(0,0,.14),(0,0,.182)],[.023,.020,.017,.022],'weapon2_wood')
        box('boat_guard',(0,0,.197),(.142,.045,.023),'weapon2_brass',.009)
        orb('oval_pommel',(0,0,.032),(.038,.024,.032),'weapon2_brass')
        for z in [.059,.18]:ring('grip_collar',z,.024,.011,'weapon2_iron')
        for side in [-1,1]:
            for z in [.085,.142]:orb('grip_rivet',(0,side*.019,z),(.004,.002,.004),'weapon2_brass')
            limb('blade_root_inlay',[(-.016,side*.0045,.235),(0,side*.0062,.253),(.016,side*.0045,.235)],[.001,.001,.001],'weapon2_brass')
    else:
        blade(key,[(1.72,.012,.006),(1.77,.031,.0065),(1.85,.048,.007),(1.96,.037,.006),(2.08,.015,.0035),(2.16,.0005,.0004)])
        limb('tapered_ash_shaft',[(0,0,.08),(0,0,.65),(0,0,1.3),(0,0,1.77)],[.017,.018,.016,.013],'weapon2_wood')
        limb('forged_socket',[(0,0,1.57),(0,0,1.68),(0,0,1.76)],[.020,.018,.012],'weapon2_iron')
        limb('butt_ferrule',[(0,0,.004),(0,0,.055),(0,0,.12)],[.006,.020,.018],'weapon2_iron')
        for z in [1.59,1.68]:ring('socket_bands',z,.0205,.008,'weapon2_brass')
        for side in [-1,1]:orb('socket_rivet',(0,side*.020,1.62),(.004,.002,.004),'weapon2_brass')
        for j in range(19):ring('hand_binding',.90+j*.012,.019,.004,'weapon2_leather')

def pigment(o,p,c,colors):
    if o.get('blade_section_count'):
        # Highlight actual edge lands according to geometric distance to central ridge.
        if abs(p.y)<.003:return colors['weapon2_edge']
    if o['pigment']=='weapon2_wood':
        f=.78+.20*math.sin(p.x*770+p.y*650+math.sin(p.z*19));return tuple(v*f for v in c)
    return c
BLEND_NAME='WeaponBatch2.blend';REPORT_NAME='projection-report-weapon-batch2.json';PIGMENT_FUNCTION=pigment
SOURCE_TILE_NAMES={k:k.replace('_',' ') for k in GROUPS};SPATIAL_MASK_KEYS=GROUPS
pipeline=Path(__file__).with_name('CreatureBatch2Pipeline.py').read_text().replace('win/share/monsters.txt','win/share/objects.txt')
# Tiny projections fill their frame independently of generic tile proportions.
pipeline=pipeline.replace('target_width=max(x for x,y in target)-min(x for x,y in target)+1','target_width=13').replace('target_height=max(y for x,y in target)-min(y for x,y in target)+1','target_height=13')
pipeline=pipeline.replace('max((high-low).length*1.1,1.1)','max((high-low).length*1.1,.1)')
strip_lights="""
for at,power in [((-1,-3,1.7),650),((2,2,1.5),450)]:
    data=bpy.data.lights.new('Blade reflection strip','AREA');data.energy=power;data.shape='RECTANGLE';data.size=2.0;data.size_y=3.0
    o=bpy.data.objects.new('Blade reflection strip',data);bpy.context.collection.objects.link(o);o.location=at;o.rotation_euler=(Vector((0,0,.65))-o.location).to_track_quat('-Z','Y').to_euler()
"""
pipeline=pipeline.replace('scene.render.film_transparent=True;',strip_lights+'\nscene.render.film_transparent=True;')
exec(compile(pipeline,'WeaponBatch2Pipeline','exec'))
