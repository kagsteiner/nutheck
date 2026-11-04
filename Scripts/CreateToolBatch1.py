"""Editable utility objects: pick-axe, four-tined hook and binaural stethoscope."""
import sys,math,json,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from CreatureGeometry import *
import CreatureGeometry as g
OUT=ROOT/'Art/ObjectInterpretations';GROUPS=['pick_axe','grappling_hook','stethoscope']
manifest=OUT/'tool-batch1-protected.json'
if not manifest.exists():
    files=sorted(p for p in (ROOT/'Art').rglob('*.fbx') if p.stem not in GROUPS)
    manifest.write_text(json.dumps({p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in files},indent=2))
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for key,c,rough,metal in [('tool1_iron',(.28,.34,.37),.30,1),('tool1_edge',(.65,.70,.73),.18,1),('tool1_brass',(.39,.24,.068),.32,.8),('tool1_leather',(.063,.026,.014),.78,0),('tool1_wood',(.23,.11,.037),.60,0),('tool1_tube',(.05,.065,.07),.65,0)]:
    COLORS[key]=c;m=bpy.data.materials.new(key);m.use_nodes=True;m.diffuse_color=(*c,1);s=m.node_tree.nodes['Principled BSDF'];s.inputs['Roughness'].default_value=rough;s.inputs['Metallic'].default_value=metal;MATS[key]=m

def ring(name,at,r,depth,color='tool1_iron',face=False):
    bpy.ops.mesh.primitive_cylinder_add(vertices=40,radius=r,depth=depth,location=at);o=bpy.context.object
    if face:o.rotation_euler.x=math.pi/2;bpy.ops.object.transform_apply(location=False,rotation=True,scale=True)
    g.finish(o,name,color);m=o.modifiers.new('Machined bevel','BEVEL');m.width=min(.0015,depth*.15);m.segments=3
    return o

def torus(name,at,major,minor,color,rotation=(math.pi/2,0,0)):
    bpy.ops.mesh.primitive_torus_add(major_segments=64,minor_segments=12,location=at,major_radius=major,minor_radius=minor,rotation=rotation)
    o=bpy.context.object;bpy.ops.object.transform_apply(location=False,rotation=True,scale=True)
    for p in o.data.polygons:p.use_smooth=True
    return g.finish(o,name,color)

def eye(o,z):
    bpy.ops.mesh.primitive_cylinder_add(vertices=48,radius=.023,depth=.3,location=(0,0,z));cut=bpy.context.object;bpy.context.view_layer.objects.active=o
    for m in list(o.modifiers):bpy.ops.object.modifier_apply(modifier=m.name)
    m=o.modifiers.new('Actual haft opening','BOOLEAN');m.operation='DIFFERENCE';m.object=cut;bpy.ops.object.modifier_apply(modifier=m.name);bpy.data.objects.remove(cut,do_unlink=True)
    o.data.materials.clear();o.data.materials.append(MATS[o['pigment']])
    for p in o.data.polygons:p.material_index=0
    o['haft_eye']=True

def bezier(points,n=25):
    a,b,c,d=map(Vector,points)
    return [tuple((1-t)**3*a+3*(1-t)**2*t*b+3*(1-t)*t*t*c+t**3*d) for t in [i/(n-1) for i in range(n)]]

g.GROUP='pick_axe'
limb('shaped_wood_haft',[(0,0,.025),(.012,0,.20),(.010,0,.48),(0,0,.82)],[.026,.024,.021,.022],'tool1_wood')
ring('heel_ferrule',(0,0,.025),.027,.035)
for j in range(13):ring('leather_hand_binding',(.006+j*.0003,0,.075+j*.011),.025,.003,'tool1_leather')
head=box('forged_eye_block',(0,0,.77),(.12,.085,.09),'tool1_iron',.009);eye(head,.77);head['crafted_tool']=True
# Curved square-section taper; a pick point and a broader transverse chisel are distinct ends.
verts=[];faces=[]
stations=[(-.045,.780,.043,.035),(-.115,.788,.039,.031),(-.21,.775,.026,.021),(-.30,.731,.014,.013),(-.36,.674,.0012,.0012)]
for x,z,h,d in stations:
    for yy,zz in [(-.7,-1),(-1,-.7),(-1,.7),(-.7,1),(.7,1),(1,.7),(1,-.7),(.7,-1)]:verts.append((x,yy*d,z+zz*h))
for j in range(len(stations)-1):
    for i in range(8):a=j*8+i;b=j*8+(i+1)%8;faces.append((a,b,b+8,a+8))
faces += [tuple(reversed(range(8))),tuple((len(stations)-1)*8+i for i in range(8))]
mm=bpy.data.meshes.new('pick_taper');mm.from_pydata(verts,[],faces);mm.update();o=bpy.data.objects.new('tapered_pick',mm);bpy.context.collection.objects.link(o);g.finish(o,'tapered_pick','tool1_iron')
for p in mm.polygons:p.use_smooth=True
limb('adze_arm',[(.04,0,.77),(.12,0,.78),(.22,0,.75)],[.036,.030,.023],'tool1_iron')
box('broad_chisel_bit',(.24,0,.739),(.058,.098,.018),'tool1_edge',.003)
box('haft_wedge',(0,0,.825),(.030,.009,.009),'tool1_iron',.001)
for side in [-1,1]:
    box('reinforcing_strap',(0,side*.024,.625),(.025,.007,.20),'tool1_iron',.002)
    for z in [.56,.68]:orb('strap_rivet',(0,side*.029,z),(.004,.002,.004),'tool1_brass')

g.GROUP='grappling_hook'
limb('forged_spine',[(0,0,.16),(0,0,.30),(0,0,.425)],[.027,.020,.019],'tool1_iron')
torus('open_rope_eye',(0,0,.466),.035,.008,'tool1_iron')
ring('eye_neck',(0,0,.419),.024,.021,'tool1_brass')
for j in range(4):
    a=math.tau*j/4
    profile=bezier([(0,0,.20),(.15,0,-.025),(.255,0,.15),(.125,0,.285)],33)
    pts=[(x*math.cos(a),x*math.sin(a),z) for x,y,z in profile]
    radii=[.019*(1-i/32)+.0010*(i/32) for i in range(33)]
    o=limb('curved_tine_%d'%j,pts,radii,'tool1_iron');o['crafted_tool']=True
    # Small tapered terminal at each claw, same forged material rather than a rarity marker.
    orb('tine_root_rivet_%d'%j,(.020*math.cos(a),.020*math.sin(a),.20),(.006,.006,.006),'tool1_brass')
ring('forged_hub',(0,0,.186),.034,.030)

g.GROUP='stethoscope'
for side in [-1,1]:
    pts=bezier([(0,0,.275),(side*.055,0,.32),(side*.16,0,.47),(side*.095,0,.565)],33)
    o=limb('steel_ear_arm',pts,[.0075]*33,'tool1_edge');o['crafted_tool']=True
    ear=limb('soft_ear_tip',[(side*.095,0,.565),(side*.077,0,.572)],[.011,.010],'tool1_tube')
ring('junction_collar',(0,0,.283),.011,.021,'tool1_brass')
# Relaxed hanging tube with a chest piece: no loose detachable components or state cues.
p1=bezier([(0,0,.275),(-.14,0,.16),(-.16,0,.018),(-.02,0,.016)],33)
p2=bezier([(-.02,0,.016),(.11,0,.008),(.16,0,.08),(.115,0,.132)],33)
limb('flexible_sound_tube',p1+p2[1:],[.0095]*(len(p1)+len(p2)-1),'tool1_tube')
limb('chest_piece_stem',[(.115,0,.132),(.10,0,.156)],[.007,.007],'tool1_iron')
ring('chest_piece_body',(.10,0,.179),.028,.016,'tool1_iron',True)
torus('chest_piece_rim',(.10,-.010,.179),.026,.003,'tool1_edge')
ring('recessed_diaphragm',(.10,-.008,.179),.023,.002,'tool1_edge',True)
torus('rear_bell_rim',(.10,.011,.179),.019,.003,'tool1_brass')
# Put the editable object's lowest point at the common floor origin.
bpy.context.view_layer.update()
for key in GROUPS:
    parts=[o for o in bpy.data.objects if o.type=='MESH' and o.get('creature')==key]
    low=min((o.matrix_world@v.co).z for o in parts for v in o.data.vertices)
    for o in parts:o.location.z-=low

def pigment(o,p,c,colors):
    if o['pigment']=='tool1_wood':
        f=.82+.15*math.sin(p.x*700+p.y*650+math.sin(p.z*15));return tuple(v*f for v in c)
    if o['creature']=='pick_axe' and 'tapered_pick' in o.name and p.x<-.30:return colors['tool1_edge']
    return c
BLEND_NAME='ToolBatch1.blend';REPORT_NAME='projection-report-tool-batch1.json';PIGMENT_FUNCTION=pigment
SOURCE_TILE_NAMES={'pick_axe':'pick-axe','grappling_hook':'grappling hook','stethoscope':'stethoscope'};SPATIAL_MASK_KEYS=GROUPS
pipeline=Path(__file__).with_name('CreatureBatch2Pipeline.py').read_text().replace('win/share/monsters.txt','win/share/objects.txt')
pipeline=pipeline.replace('target_width=max(x for x,y in target)-min(x for x,y in target)+1','target_width=13').replace('target_height=max(y for x,y in target)-min(y for x,y in target)+1','target_height=13').replace('max((high-low).length*1.1,1.1)','max((high-low).length*1.1,.1)')
strip_lights="""
for at,power in [((-1,-3,1.7),650),((2,2,1.5),450)]:
    data=bpy.data.lights.new('Tool reflection strip','AREA');data.energy=power;data.shape='RECTANGLE';data.size=2.;data.size_y=3.
    o=bpy.data.objects.new('Tool reflection strip',data);bpy.context.collection.objects.link(o);o.location=at;o.rotation_euler=(Vector((0,0,.4))-o.location).to_track_quat('-Z','Y').to_euler()
"""
pipeline=pipeline.replace('scene.render.film_transparent=True;',strip_lights+'\nscene.render.film_transparent=True;')
exec(compile(pipeline,'ToolBatch1Pipeline','exec'))
