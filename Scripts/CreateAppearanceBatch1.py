"""Physical ruby ring, spherical iron amulet and oak wand; no effect-specific design."""
import sys,math,json,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from CreatureGeometry import *
import CreatureGeometry as g
OUT=ROOT/'Art/ObjectInterpretations';GROUPS=['ruby_ring','spherical_amulet','oak_wand']
manifest=OUT/'appearance-batch1-protected.json'
if not manifest.exists():manifest.write_text(json.dumps({p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'Art').rglob('*.fbx') if p.stem not in GROUPS},indent=2))
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for k,c,rough,metal in [('app1_gold',(.65,.38,.09),.23,1),('app1_iron',(.39,.45,.49),.24,1),('app1_dark_iron',(.16,.19,.21),.34,1),('app1_ruby',(.43,.008,.028),.12,0),('app1_oak',(.28,.125,.039),.53,0)]:
 COLORS[k]=c;m=bpy.data.materials.new(k);m.use_nodes=True;m.diffuse_color=(*c,1);s=m.node_tree.nodes['Principled BSDF'];s.inputs['Roughness'].default_value=rough;s.inputs['Metallic'].default_value=metal
 if k=='app1_ruby':s.inputs['Coat Weight'].default_value=.35;s.inputs['IOR'].default_value=1.77
 MATS[k]=m
def torus(name,at,major,minor,color,normal=Vector((0,1,0)),segments=64):
 bpy.ops.mesh.primitive_torus_add(major_segments=segments,minor_segments=12,location=at,major_radius=major,minor_radius=minor)
 o=bpy.context.object;o.rotation_euler=Vector(normal).to_track_quat('Z','Y').to_euler();bpy.ops.object.transform_apply(location=False,rotation=True,scale=True)
 for p in o.data.polygons:p.use_smooth=True
 return g.finish(o,name,color)
def lathe(name,profile,color,n=64):
 verts=[];faces=[]
 for z,r in profile:
  for j in range(n):a=math.tau*j/n;verts.append((r*math.cos(a),r*math.sin(a),z))
 for i in range(len(profile)-1):
  for j in range(n):a=i*n+j;b=i*n+(j+1)%n;faces.append((a,b,b+n,a+n))
 faces += [tuple(reversed(range(n))),tuple((len(profile)-1)*n+i for i in range(n))]
 mesh=bpy.data.meshes.new(name);mesh.from_pydata(verts,[],faces);mesh.update();o=bpy.data.objects.new(name,mesh);bpy.context.collection.objects.link(o);g.finish(o,name,color)
 for p in mesh.polygons:p.use_smooth=True
 return o
g.GROUP='ruby_ring'
band=torus('carved_ruby_shank',(0,0,.014),.011,.0022,'app1_ruby');band['open_band']=True
for y in [-.0015,.0015]:torus('fine_gold_shank_edge',(0,y,.014),.0111,.00045,'app1_gold')
# A genuine cut stone: table, crown, girdle and converging pavilion, not a painted jewel.
verts=[];faces=[];n=8
# The crown faces radially outward from the shank: +Z, perpendicular to
# the finger-hole axis (+/-Y). Its table lies in XY, never parallel to the band.
for z,rx,ry in [(.036,.0048,.0060),(.0325,.0078,.0092),(.0315,.0078,.0092),(.0255,.0007,.0008)]:
 for j in range(n):a=math.tau*(j+.5)/n;verts.append((rx*math.cos(a),ry*math.sin(a),z))
for i in range(3):
 for j in range(n):a=i*n+j;b=i*n+(j+1)%n;faces.append((a,b,b+n,a+n))
faces += [tuple(reversed(range(n))),tuple(3*n+i for i in range(n))]
mesh=bpy.data.meshes.new('Octagonal cut ruby');mesh.from_pydata(verts,[],faces);mesh.update();o=bpy.data.objects.new('ruby_crown',mesh);bpy.context.collection.objects.link(o);g.finish(o,'faceted_ruby','app1_ruby');o['cut_gem']=True
o['crown_axis']=[0,0,1]
for side in [-1,1]:
 limb('pierced_gallery_arch',[(side*.003,0,.023),(side*.007,0,.0275),(side*.007,0,.0315)],[.0009,.0008,.0007],'app1_gold')
 for j in range(4):orb('shoulder_bead',(side*(.004+j*.0016),-.001,.022+j*.0005),(.0007,.0007,.0007),'app1_gold')
# A continuous gallery rail connects every claw to the supporting arches.
rail=torus('gallery_rail',(0,0,.0305),.0078,.00055,'app1_gold',Vector((0,0,1)))
rail.scale.y=.0092/.0078;bpy.context.view_layer.objects.active=rail;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
for j in range(6):
 a=math.tau*j/6;c=math.cos(a);t=math.sin(a)
 limb('claw_prong',[(.0078*c,.0092*t,.0295),(.0084*c,.0098*t,.0325),(.0046*c,.0057*t,.0362)],[.00065,.00065,.00045],'app1_gold')

g.GROUP='spherical_amulet'
orb('closed_iron_globe',(0,0,.023),(.015,.015,.015),'app1_dark_iron')['spherical_body']=True
for z in [-.009,0,.009]:torus('polished_latitude_rib',(0,0,.023+z),math.sqrt(.015**2-z*z)+.00015,.00055,'app1_iron',Vector((0,0,1)))
for j in range(6):
 a=math.tau*j/6;torus('meridian_rib',(0,0,.023),.0152,.00045,'app1_iron',Vector((math.cos(a),math.sin(a),0)))
lathe('globe_neck',[(.036,.0025),(.039,.0034),(.041,.0025)],'app1_iron')
torus('pendant_bail',(0,0,.0445),.0032,.0007,'app1_iron')
for j in range(36):
 a=math.tau*j/36;at=Vector((.027*math.sin(a),0,.090-.045*math.cos(a)))
 normal=Vector((0,1,0)) if j%2==0 else Vector((math.sin(a),0,-math.cos(a)))
 torus('interlocking_chain_link',at,.0030,.00060,'app1_iron',normal,32)
g.GROUP='oak_wand'
profile=[(.002,.008),(.006,.011),(.017,.011)]
for j in range(8):profile += [(.020+j*.009,.0105),(.022+j*.009,.0095),(.025+j*.009,.0105)]
profile += [(.089,.0105),(.095,.013),(.103,.013),(.110,.010),(.15,.0088),(.23,.0075),(.31,.0058),(.36,.0045),(.368,.002)]
lathe('turned_oak_rod',profile,'app1_oak')['turned_shaft']=True
lathe('heel_ferrule',[(0,.008),(.001,.0095),(.006,.0095),(.008,.009)],'app1_gold')
lathe('thin_collar',[(.096,.0132),(.098,.0138),(.101,.0138),(.103,.0132)],'app1_gold')
for j in range(12):
 a=math.tau*j/12;orb('collar_stud',(.0135*math.cos(a),.0135*math.sin(a),.0995),(.0007,.0007,.0007),'app1_gold')
for key in GROUPS:
 parts=[o for o in bpy.data.objects if o.type=='MESH' and o.get('creature')==key];low=min((o.matrix_world@v.co).z for o in parts for v in o.data.vertices)
 for o in parts:o.location.z-=low
def pigment(o,p,c,colors):
 if o['pigment']=='app1_oak':
  f=.82+.13*math.sin(900*p.x+650*p.y+2*math.sin(p.z*41));return tuple(v*f for v in c)
 return c
BLEND_NAME='AppearanceBatch1.blend';REPORT_NAME='projection-report-appearance-batch1.json';PIGMENT_FUNCTION=pigment
records=json.loads((ROOT/'Art/ObjectCatalogue/objects.json').read_text(encoding='utf-8'))['objects'];ids=['RIN_CONFLICT','AMULET_OF_LIFE_SAVING','WAN_NOTHING']
SOURCE_TILE_NAMES={k:next(r['official_tile']['label'] for r in records if r['id']==i) for k,i in zip(GROUPS,ids)}
pipeline=Path(__file__).with_name('CreatureBatch2Pipeline.py').read_text(encoding='utf-8').replace('win/share/monsters.txt','win/share/objects.txt')
pipeline=pipeline.replace('target_width=max(x for x,y in target)-min(x for x,y in target)+1','target_width=13').replace('target_height=max(y for x,y in target)-min(y for x,y in target)+1','target_height=13').replace('max((high-low).length*1.1,1.1)','max((high-low).length*1.1,.025)')
exec(compile(pipeline,'AppearanceBatch1Pipeline','exec'))
