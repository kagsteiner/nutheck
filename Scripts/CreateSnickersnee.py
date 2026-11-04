"""Snickersnee: an exceptional static katana, named appearance rather than hidden power."""
import sys,math,json,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from CreatureGeometry import *
import CreatureGeometry as g
OUT=ROOT/'Art/ObjectInterpretations';GROUPS=['snickersnee'];g.GROUP='snickersnee'
manifest=OUT/'snickersnee-protected.json'
if not manifest.exists():manifest.write_text(json.dumps({p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'Art').rglob('*.fbx') if p.stem!='snickersnee'},indent=2))
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for k,c,rough,metal in [('sn_steel',(.32,.43,.53),.21,1),('sn_edge',(.72,.79,.84),.16,1),('sn_gold',(.60,.35,.075),.24,1),('sn_black',(.018,.027,.040),.30,1),('sn_indigo',(.009,.020,.062),.72,0),('sn_ray',(.73,.67,.48),.76,0)]:
    COLORS[k]=c;m=bpy.data.materials.new(k);m.use_nodes=True;m.diffuse_color=(*c,1)
    s=m.node_tree.nodes['Principled BSDF'];s.inputs['Roughness'].default_value=rough;s.inputs['Metallic'].default_value=metal;MATS[k]=m

def ring(name,at,r,minor,color,scale=(1,1,1)):
    bpy.ops.mesh.primitive_torus_add(major_radius=r,minor_radius=minor,major_segments=64,minor_segments=12,location=at)
    o=bpy.context.object;o.scale=scale;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    for p in o.data.polygons:p.use_smooth=True
    return g.finish(o,name,color)

def disk(name,at,r,depth,color,scale=(1,1,1)):
    bpy.ops.mesh.primitive_cylinder_add(vertices=64,radius=r,depth=depth,location=at);o=bpy.context.object;o.scale=scale;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    g.finish(o,name,color);b=o.modifiers.new('Precise fitting bevel','BEVEL');b.width=min(.001,depth*.2);b.segments=3;return o

# Closed blade with a high longitudinal ridge, spine, bevel land and cutting edge.
stations=[i*.94/94 for i in range(95)]+[.96,.975,.985,.994,1.]
fractions=[-1,-.60,-.15,0,.20,.35,.45,.55,.70,.85,1]
def shape(t):return .095*t*t,.423+.902*t,.029*(1-.32*t)*max(.012,min(1,(1-t)/.065))
def thickness(a):return .65+(.35*(a+1)/.85) if a<-.15 else 1.-.94*(a+.15)/1.15
cross=[(a,-thickness(a)) for a in fractions]+[(a,thickness(a)) for a in reversed(fractions)]
verts=[];faces=[]
for t in stations:
    x,z,w=shape(t)
    for a,b in cross:verts.append((x+a*w,b*max(.00025,.0052*min(1,(1-t)/.05)),z))
n=len(cross)
for j in range(len(stations)-1):
    for i in range(n):a=j*n+i;b=j*n+(i+1)%n;faces.append((a,b,b+n,a+n))
faces += [tuple(reversed(range(n))),tuple((len(stations)-1)*n+i for i in range(n))]
m=bpy.data.meshes.new('Tempered blade sections');m.from_pydata(verts,[],faces);m.update();o=bpy.data.objects.new('Snickersnee blade',m);bpy.context.collection.objects.link(o)
g.finish(o,'curved_tempered_blade','sn_steel');o['crafted_blade']=True;o['section_count']=len(stations)

# The guard is genuinely pierced: outer ring, central mount and four wave spokes.
ring('pierced_black_tsuba',(0,0,.394),.064,.0065,'sn_black',(1,.82,1))['pierced_guard']=True
for z in [.389,.399]:ring('gold_guard_edge',(0,0,z),.064,.00125,'sn_gold',(1,.82,1))
disk('tsuba_centre',(0,0,.394),.026,.011,'sn_black',(1,.80,1))
for j in range(4):
    a=j*math.pi/2;pts=[]
    for i in range(25):
        t=i/24;r=.022+.043*t;ang=a+.25*math.sin(t*math.pi)
        pts.append((r*math.cos(ang),r*.82*math.sin(ang),.394))
    limb('wave_guard_bridge',pts,[.0042]*len(pts),'sn_black')
    for side in [-1,1]:limb('gold_wave_guard_inlay',[(x,y,z+side*.0042) for x,y,z in pts],[.00065]*len(pts),'sn_gold')
for z in [.383,.405]:disk('gold_seppa',(0,0,z),.031,.004,'sn_gold',(1,.73,1))
box('gold_habaki',(0,0,.425),(.062,.026,.034),'sn_gold',.0025)
for side in [-1,1]:
    for k in range(3):
        limb('habaki_fine_chasing',[(-.023,side*.014,.414+k*.007),(0,side*.014,.415+k*.007),(.022,side*.014,.414+k*.007)],[.0005]*3,'sn_black')

# Pale pebbled underlay and real overlapping indigo wrap bands on both faces.
box('rayskin_underlay',(0,0,.213),(.047,.033,.316),'sn_ray',.007)['wrapped_grip']=True
for side in [-1,1]:
    for j in range(13):
        z=.069+j*.023
        for direction in [-1,1]:
            b=box('indigo_diamond_wrap',(0,side*.0175,z),(.057,.0055,.010),'sn_indigo',.001)
            b.rotation_euler.y=direction*math.radians(34)
            bpy.context.view_layer.objects.active=b;bpy.ops.object.transform_apply(location=False,rotation=True,scale=False)
    for z in [.155,.270]:
        # Small sculpted wave ornaments under the binding, no readable magic rune.
        for j in range(3):
            limb('gold_menuki_wave',[(-.011+j*.007,side*.021,z-.005),(-.007+j*.007,side*.022,z+.001),(-.001+j*.007,side*.021,z-.002)],[.0013,.0019,.0008],'sn_gold')
for z in [.043,.371]:
    box('black_hilt_fitting',(0,0,z),(.056,.040,.024),'sn_black',.004)
    for dz in [-.009,.009]:
        # Complete oval rims around the fittings, not just front-face strips.
        ring('gold_fitting_rim',(0,0,z+dz),.026,.001,'sn_gold',(1,.72,1))
    for side in [-1,1]:
        for j in range(3):
            pts=[(-.020+i*.002,side*.0205,z+.003*math.sin(i*.55+j)) for i in range(21)]
            limb('gold_fitting_wave',pts,[.00055]*len(pts),'sn_gold')
for side in [-1,1]:
    # Restrained paired blade-root waves echo the guard/fittings without a glow.
    for j in range(2):
        pts=[]
        for i in range(25):
            t=i/24;z=.465+t*.115;x=.095*((z-.423)/.902)**2-.011+j*.009+.003*math.sin(t*math.tau)
            pts.append((x,side*.0052,z))
        limb('blade_root_gold_wave',pts,[.00055]*len(pts),'sn_gold')

parts=[o for o in bpy.data.objects if o.type=='MESH'];low=min((o.matrix_world@v.co).z for o in parts for v in o.data.vertices)
for o in parts:o.location.z-=low;o['floor_shift']=low
def pigment(o,p,c,colors):
    if o.get('crafted_blade'):
        z=p.z+o['floor_shift'];t=max(0,min(1,(z-.423)/.902));x,_,w=shape(t);a=(p.x-x)/max(.0002,w)
        if a>.42+.085*math.sin(t*math.tau*13):return colors['sn_edge']
    if o['pigment']=='sn_ray':
        f=.85+.12*math.sin(p.x*2900)*math.sin(p.z*2700);return tuple(v*f for v in c)
    return c
BLEND_NAME='Snickersnee.blend';REPORT_NAME='projection-report-snickersnee.json';PIGMENT_FUNCTION=pigment
SOURCE_TILE_NAMES={'snickersnee':'samurai sword / katana'}
pipeline=Path(__file__).with_name('CreatureBatch2Pipeline.py').read_text(encoding='utf-8').replace('win/share/monsters.txt','win/share/objects.txt')
pipeline=pipeline.replace('target_width=max(x for x,y in target)-min(x for x,y in target)+1','target_width=13').replace('target_height=max(y for x,y in target)-min(y for x,y in target)+1','target_height=13')
lights="""
for at,power in [((-1,-3,1.),450),((2,2,1.5),300)]:
    data=bpy.data.lights.new('Blade reflection strip','AREA');data.energy=power;data.shape='RECTANGLE';data.size=2.;data.size_y=3.
    obj=bpy.data.objects.new('Blade reflection strip',data);bpy.context.collection.objects.link(obj);obj.location=at;obj.rotation_euler=(Vector((0,0,.65))-obj.location).to_track_quat('-Z','Y').to_euler()
"""
pipeline=pipeline.replace('scene.render.film_transparent=True;',lights+'\nscene.render.film_transparent=True;')
exec(compile(pipeline,'SnickersneePipeline','exec'))
