"""Sapphire ring, triangular iron pendant and worked silver wand: physical appearances."""
import sys,math,json,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from CreatureGeometry import *
import CreatureGeometry as g
OUT=ROOT/'Art/ObjectInterpretations';GROUPS=['sapphire_ring','triangular_amulet','silver_wand']
manifest=OUT/'appearance-batch2-protected.json'
if not manifest.exists():
    manifest.write_text(json.dumps({p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'Art').rglob('*.fbx') if p.stem not in GROUPS},indent=2))
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for key,c,rough,metal in [('app2_sapphire',(.012,.075,.48),.13,0),('app2_silver',(.64,.70,.75),.26,1),('app2_dark_silver',(.40,.46,.51),.35,1),('app2_iron',(.35,.41,.45),.28,1),('app2_dark_iron',(.10,.14,.17),.38,1)]:
    COLORS[key]=c;m=bpy.data.materials.new(key);m.use_nodes=True;m.diffuse_color=(*c,1)
    s=m.node_tree.nodes['Principled BSDF'];s.inputs['Roughness'].default_value=rough;s.inputs['Metallic'].default_value=metal
    if key=='app2_sapphire':s.inputs['Coat Weight'].default_value=.35;s.inputs['IOR'].default_value=1.77
    MATS[key]=m

def torus(name,at,major,minor,color,normal=Vector((0,1,0)),segments=64):
    bpy.ops.mesh.primitive_torus_add(major_segments=segments,minor_segments=10,location=at,major_radius=major,minor_radius=minor)
    o=bpy.context.object;o.rotation_euler=Vector(normal).to_track_quat('Z','Y').to_euler();bpy.ops.object.transform_apply(location=False,rotation=True,scale=True)
    for p in o.data.polygons:p.use_smooth=True
    return g.finish(o,name,color)

def meshpart(name,verts,faces,color):
    m=bpy.data.meshes.new(name);m.from_pydata(verts,[],faces);m.update();o=bpy.data.objects.new(name,m);bpy.context.collection.objects.link(o)
    return g.finish(o,name,color)

def lathe(name,profile,color,n=48,flute=0,twist=0):
    verts=[];faces=[]
    for z,r in profile:
        for j in range(n):
            a=math.tau*j/n;radius=r+flute*math.cos(a*8)
            verts.append((radius*math.cos(a+twist*z),radius*math.sin(a+twist*z),z))
    for i in range(len(profile)-1):
        for j in range(n):a=i*n+j;b=i*n+(j+1)%n;faces.append((a,b,b+n,a+n))
    faces += [tuple(reversed(range(n))),tuple((len(profile)-1)*n+i for i in range(n))]
    o=meshpart(name,verts,faces,color)
    for p in o.data.polygons:p.use_smooth=flute==0 and n>20
    return o

g.GROUP='sapphire_ring'
torus('carved_sapphire_band',(0,0,.0134),.011,.0024,'app2_sapphire')['open_band']=True
for y in [-.0018,.0018]:torus('silver_band_lip',(0,y,.0134),.011,.00042,'app2_silver')
# Round brilliant-inspired twelve-sided crown. Table is the upper XY plane.
verts=[];faces=[];n=12
for z,r in [(.035,.0053),(.0317,.0083),(.0307,.0083),(.0253,.0006)]:
    for j in range(n):a=math.tau*(j+.5)/n;verts.append((r*math.cos(a),r*math.sin(a),z))
for i in range(3):
    for j in range(n):a=i*n+j;b=i*n+(j+1)%n;faces.append((a,b,b+n,a+n))
faces += [tuple(reversed(range(n))),tuple(3*n+j for j in range(n))]
gem=meshpart('twelve_facet_sapphire_crown',verts,faces,'app2_sapphire');gem['cut_gem']=True;gem['crown_axis']=[0,0,1];gem['table_vertices']=n
torus('open_gallery_rail',(0,0,.030),.0081,.00065,'app2_silver',Vector((0,0,1)))
for side in [-1,1]:
    limb('split_shoulder',[(side*.008,0,.020),(side*.006,0,.025),(side*.004,0,.0298)],[.0013,.001,.0007],'app2_silver')
    for y in [-.003,.003]:
        limb('shoulder_fan',[(side*.008,0,.020),(side*.007,y,.025),(side*.006,y,.030)],[.0007,.00065,.0006],'app2_silver')
for j in range(6):
    a=math.tau*j/6;c=math.cos(a);s=math.sin(a)
    limb('crown_claw',[(.0079*c,.0079*s,.0288),(.0089*c,.0089*s,.0318),(.0050*c,.0050*s,.0351)],[.00065,.0006,.0004],'app2_silver')

g.GROUP='triangular_amulet'
triangle=[(-.021,.012),(.021,.012),(0,.048)];center=Vector((0,.024))
def triangular_frame(name,scale,inner,depth,color):
    verts=[];faces=[]
    for y in [-depth/2,depth/2]:
        for factor in [scale,inner]:
            for x,z in triangle:
                p=center+(Vector((x,z))-center)*factor;verts.append((p.x,y,p.y))
    for j in range(3):
        k=(j+1)%3;faces.extend([(j,k,k+3,j+3),(j+6,j+9,k+9,k+6),(j,j+6,k+6,k),(j+3,k+3,k+9,j+9)])
    o=meshpart(name,verts,faces,color);b=o.modifiers.new('Soft forged bevel','BEVEL');b.width=.00065;b.segments=3;return o
triangular_frame('forged_open_triangle',1,.58,.0052,'app2_dark_iron')['triangular_body']=True
triangular_frame('bright_front_back_bevel',.94,.82,.0057,'app2_iron')
for x,z in triangle:
    p=center+(Vector((x,z))-center)*.82
    for side in [-1,1]:orb('peened_corner_pin',(p.x,side*.003,p.y),(.0012,.00065,.0012),'app2_iron')
torus('forged_pendant_bail',(0,0,.0505),.003,.0008,'app2_iron')
for j in range(48):
    a=math.tau*j/48;at=Vector((.028*math.sin(a),0,.096-.043*math.cos(a)))
    normal=Vector((0,1,0)) if j%2 else Vector((.043*math.sin(a),0,-.028*math.cos(a)))
    torus('interlocking_iron_chain',at,.0029,.00055,'app2_iron',normal,24)

g.GROUP='silver_wand'
# Eight real shallow flutes twist through the broad grip, with polished ferrules.
lathe('twisted_fluted_grip',[(.006+i*.085/24,.0104) for i in range(25)],'app2_dark_silver',64,.001,7)['worked_grip']=True
lathe('polished_tapered_rod',[(.087,.009),(.11,.008),(.16,.0075),(.24,.0065),(.32,.0056),(.365,.0047),(.377,.0035)],'app2_silver',48)['metal_shaft']=True
for z,r in [(0,.0105),(.092,.0112),(.107,.0094),(.367,.0058)]:
    lathe('turned_silver_ferrule',[(z+.001,r*.86),(z+.002,r),(z+.006,r),(z+.008,r*.86)],'app2_silver')
    for dz in [.0028,.0053]:torus('fine_ferrule_bead',(0,0,z+dz),r+.00012,.00030,'app2_silver',Vector((0,0,1)),48)
orb('rounded_silver_heel',(0,0,.0025),(.0097,.0097,.0025),'app2_silver')
orb('closed_silver_tip',(0,0,.377),(.0035,.0035,.0045),'app2_silver')
for key in GROUPS:
    parts=[o for o in bpy.data.objects if o.type=='MESH' and o.get('creature')==key]
    low=min((o.matrix_world@v.co).z for o in parts for v in o.data.vertices)
    for o in parts:o.location.z-=low
BLEND_NAME='AppearanceBatch2.blend';REPORT_NAME='projection-report-appearance-batch2.json'
records=json.loads((ROOT/'Art/ObjectCatalogue/objects.json').read_text(encoding='utf-8'))['objects'];ids=['RIN_AGGRAVATE_MONSTER','AMULET_OF_RESTFUL_SLEEP','WAN_POLYMORPH']
SOURCE_TILE_NAMES={k:next(r['official_tile']['label'] for r in records if r['id']==i) for k,i in zip(GROUPS,ids)}
pipeline=Path(__file__).with_name('CreatureBatch2Pipeline.py').read_text(encoding='utf-8').replace('win/share/monsters.txt','win/share/objects.txt')
pipeline=pipeline.replace('target_width=max(x for x,y in target)-min(x for x,y in target)+1','target_width=13').replace('target_height=max(y for x,y in target)-min(y for x,y in target)+1','target_height=13').replace('max((high-low).length*1.1,1.1)','max((high-low).length*1.1,.025)')
exec(compile(pipeline,'AppearanceBatch2Pipeline','exec'))
