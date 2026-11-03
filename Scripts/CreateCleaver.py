"""Oversized barbarian divine-gift double battle-axe; complete static geometry."""
import sys,math,hashlib,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from CreatureGeometry import *
import CreatureGeometry as g
OUT=ROOT/'Art/ObjectInterpretations';manifest=OUT/'cleaver-protected-assets.json'
if not manifest.exists():
    files=[p for folder in ['CreatureInterpretations','ObjectInterpretations','EnvironmentInterpretations','TileFallback'] for p in (ROOT/'Art'/folder).glob('*.fbx')]
    manifest.write_text(json.dumps({p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in files},indent=2))
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for key,col,rough,metal in [('cleaver_iron',(.13,.17,.19),.29,1),('cleaver_edge',(.57,.65,.69),.19,1),('cleaver_bronze',(.38,.19,.055),.35,.85),('cleaver_wood',(.16,.065,.020),.65,0),('cleaver_hide',(.065,.022,.012),.78,0),('cleaver_bone',(.57,.45,.27),.60,0)]:
    COLORS[key]=col;m=bpy.data.materials.new(key);m.use_nodes=True;m.diffuse_color=(*col,1);s=m.node_tree.nodes['Principled BSDF'];s.inputs['Roughness'].default_value=rough;s.inputs['Metallic'].default_value=metal;MATS[key]=m
g.GROUP='cleaver'
def prism(name,profile,depth,color,bevel=0):
    n=len(profile);vv=[(x,y,z) for y in [-depth/2,depth/2] for x,z in profile];ff=[tuple(reversed(range(n))),tuple(range(n,n*2))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
    mm=bpy.data.meshes.new(name);mm.from_pydata(vv,[],ff);mm.update();o=bpy.data.objects.new(name,mm);bpy.context.collection.objects.link(o);g.finish(o,name,color)
    if bevel:mod=o.modifiers.new('Forged edge breaks','BEVEL');mod.width=bevel;mod.segments=3
    return o
# Massive twin crescent blades, low beard points, full-thickness forged cheeks.
edge=[(.39,.86),(.49,.97),(.555,1.10),(.57,1.25),(.545,1.39),(.47,1.49)]
for sign in [-1,1]:
    inner=[(.105,1.325),(.105,1.06),(.255,.98)]
    profile=[(sign*x,z) for x,z in edge+inner]
    prism('forged_crescent',profile,.080,'cleaver_iron',.006)
    # Closed sharpened ribbon: thick inner shoulder fades to a narrow edge.
    vv=[];ff=[]
    for x,z in edge:
        vv.extend([(sign*(x-.052),-.044,z),(sign*x,-.002,z),(sign*x,.002,z),(sign*(x-.052),.044,z)])
    for i in range(len(edge)-1):
        for k in range(4):ff.append((i*4+k,i*4+(k+1)%4,(i+1)*4+(k+1)%4,(i+1)*4+k))
    ff.extend([(3,2,1,0),tuple((len(edge)-1)*4+k for k in range(4))])
    mm=bpy.data.meshes.new('Sharpened cutting bevel');mm.from_pydata(vv,[],ff);mm.update();o=bpy.data.objects.new('cutting_edge',mm);bpy.context.collection.objects.link(o);g.finish(o,'bright_cutting_bevel','cleaver_edge')
    for face in [-1,1]:
        # Angular broken chevrons are applied metal, not invented readable runes.
        pts=[(sign*.16,face*.045,1.28),(sign*.30,face*.045,1.35),(sign*.39,face*.045,1.30),(sign*.34,face*.045,1.16),(sign*.25,face*.045,1.10)]
        limb('blade_chevron',pts,[.007]*len(pts),'cleaver_bronze')
        for x,z in [(.15,1.31),(.15,1.10),(.32,1.28)]:orb('peened_rivet',(sign*x,face*.048,z),(.012,.007,.012),'cleaver_edge')
# Continuous long hardwood haft, reinforced where the head is socketed.
limb('hardwood_haft',[(0,0,.075),(0,0,.51),(.008,0,.92),(0,0,1.41)],[.036,.031,.034,.040],'cleaver_wood')
box('head_socket',(0,0,1.23),(.13,.13,.34),'cleaver_iron',.015)
for z in [1.08,1.36]:box('socket_band',(0,0,z),(.15,.145,.041),'cleaver_bronze',.008)
for base,length,turns in [(.13,.29,9),(.60,.23,7)]:
    limb('hide_grip_core',[(0,0,base),(0,0,base+length)],[.037,.036],'cleaver_hide')
    pts=[]
    for i in range(turns*24+1):
        t=i/(turns*24);a=t*math.tau*turns;pts.append((.039*math.cos(a),.039*math.sin(a),base+t*length))
    limb('heavy_hide_lashing',pts,[.007]*len(pts),'cleaver_hide')
    for z in [base-.014,base+length+.014]:limb('grip_ferrule',[(0,0,z-.009),(0,0,z+.009)],[.046,.046],'cleaver_bronze')
# Spiked iron pommel and a compact crown spike, rather than magical VFX.
prism('pommel_spike',[(-.045,.085),(0,.006),(.045,.085),(.035,.12),(-.035,.12)],.065,'cleaver_iron',.004)
prism('crown_spike',[(-.035,1.39),(0,1.555),(.035,1.39)],.060,'cleaver_edge',.003)
for side in [-1,1]:
    # Paired ivory fangs frame the socket as a trophy-like craft motif.
    for face in [-1,1]:
        limb('ivory_fang',[(side*.046,face*.073,1.27),(side*.074,face*.081,1.22),(side*.060,face*.079,1.165)],[.014,.012,.0015],'cleaver_bone')
def pigment(o,p,c,colors):
    if o['pigment']=='cleaver_iron':
        f=.88+.10*math.sin(p.x*123+p.z*141)*math.sin(p.z*175-p.y*113);return tuple(v*f for v in c)
    if o['pigment']=='cleaver_wood':
        f=.75+.23*math.sin(p.z*8+p.x*690+p.y*507);return tuple(v*f for v in c)
    return c
GROUPS=['cleaver'];BLEND_NAME='Cleaver.blend';REPORT_NAME='projection-report-cleaver.json';PIGMENT_FUNCTION=pigment
SOURCE_TILE_NAMES={'cleaver':'double-headed axe / battle-axe'};SPATIAL_MASK_KEYS=GROUPS
pipeline=Path(__file__).with_name('CreatureBatch2Pipeline.py').read_text(encoding='utf-8').replace('win/share/monsters.txt','win/share/objects.txt')
exec(compile(pipeline,'CleaverPipeline','exec'))
