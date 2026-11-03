"""Six requested native torso armors, hollow construction and physical mail."""
import sys,math,json,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from CreatureGeometry import *
import CreatureGeometry as g
OUT=ROOT/'Art/ObjectInterpretations';OUT.mkdir(exist_ok=True)
GROUPS=['leather_armor','studded_leather_armor','chain_mail','banded_mail','elven_mithril_coat','dwarvish_mithril_coat']
manifest=OUT/'armor-study-protected.json'
if not manifest.exists():
    files=[p for folder in ['CreatureInterpretations','ObjectInterpretations','EnvironmentInterpretations','TileFallback'] for p in (ROOT/'Art'/folder).glob('*.fbx')]
    manifest.write_text(json.dumps({p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in files},indent=2))
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for key,col,rough,metal in [('armor_hide',(.23,.075,.023),.67,0),('armor_dark',(.065,.022,.012),.76,0),('armor_iron',(.24,.29,.32),.27,1),('armor_mithril',(.63,.74,.79),.21,1),('armor_gold',(.58,.32,.065),.30,.85),('armor_green',(.025,.105,.065),.78,0),('armor_blue',(.025,.055,.105),.78,0)]:
    COLORS[key]=col;m=bpy.data.materials.new(key);m.use_nodes=True;m.diffuse_color=(*col,1);sh=m.node_tree.nodes['Principled BSDF'];sh.inputs['Roughness'].default_value=rough;sh.inputs['Metallic'].default_value=metal;MATS[key]=m

def point(a,z,key,extra=0):
    broad=1.12 if key=='dwarvish_mithril_coat' else .94 if key=='elven_mithril_coat' else 1
    radius=.208+.035*math.exp(-((z-.51)/.13)**2)-.023*math.exp(-((z-.27)/.11)**2)
    if z>.59:radius=radius*(1-(z-.59)/.10)+.105*((z-.59)/.10)
    return Vector(((radius+extra)*math.cos(a)*broad,(radius+extra)*math.sin(a)*.59,z))
def hole(a,z):return .425<z<.610 and abs(math.cos(a))>.88
def shell(key):
    verts=[point(math.tau*i/64,.09+j*.60/30,key) for j in range(31) for i in range(64)];faces=[]
    for j in range(30):
        for i in range(64):
            if hole(math.tau*(i+.5)/64,.09+(j+.5)*.02):continue
            a=j*64+i;b=j*64+(i+1)%64;faces.append((a,b,b+64,a+64))
    used=sorted({i for f in faces for i in f});remap={v:i for i,v in enumerate(used)}
    mesh=bpy.data.meshes.new(key+'_shell');mesh.from_pydata([verts[i] for i in used],[],[tuple(remap[i] for i in f) for f in faces]);mesh.update()
    o=bpy.data.objects.new('garment',mesh);bpy.context.collection.objects.link(o)
    color='armor_hide' if 'leather' in key else 'armor_green' if 'elven' in key else 'armor_blue' if 'dwarvish' in key else 'armor_dark'
    g.finish(o,'hollow_garment',color);mod=o.modifiers.new('Material thickness','SOLIDIFY');mod.thickness=.008
    for p in mesh.polygons:p.use_smooth=True
    return o
def ringmesh(key):
    verts=[];faces=[];mithril='mithril' in key;step=.019 if mithril else .025
    rows=int(.57/step)
    for row in range(rows):
        z=.105+row*step;n=60 if mithril else 46
        for i in range(n):
            a=math.tau*(i+.5*(row%2))/n
            if hole(a,z):continue
            c=point(a,z,key,.009);normal=Vector((math.cos(a),math.sin(a)/.59,0)).normalized();u=Vector((-normal.y,normal.x,0));v=Vector((0,0,1));rad=step*.54;tube=step*.12;start=len(verts)
            for j in range(12):
                t=math.tau*j/12;d=u*math.cos(t)+v*math.sin(t)
                for k in range(6):
                    b=math.tau*k/6;verts.append(c+d*(rad+tube*math.cos(b))+normal*tube*math.sin(b))
            for j in range(12):
                for k in range(6):faces.append(tuple(start+x for x in [j*6+k,((j+1)%12)*6+k,((j+1)%12)*6+(k+1)%6,j*6+(k+1)%6]))
    mesh=bpy.data.meshes.new('linked_rings');mesh.from_pydata(verts,[],faces);mesh.update();o=bpy.data.objects.new('mail',mesh);bpy.context.collection.objects.link(o);g.finish(o,'individual_mail_rings','armor_mithril' if mithril else 'armor_iron')
    for p in mesh.polygons:p.use_smooth=True
for key in GROUPS:
    g.GROUP=key;shell(key)
    if key in ['chain_mail','elven_mithril_coat','dwarvish_mithril_coat']:ringmesh(key)
    for z in [.105,.385,.675]:
        pts=[point(math.tau*i/128,z,key,.012) for i in range(129)];limb('bound_edge',pts,[.006]*129,'armor_gold' if 'mithril' in key else 'armor_dark')
    if key=='studded_leather_armor':
        for z in [.16,.23,.30,.47,.54]:
            for i in range(24):
                a=math.tau*i/24
                if hole(a,z):continue
                p=point(a,z,key,.006);orb('steel_stud',p,(.007,.007,.007),'armor_iron')
    if key=='banded_mail':
        for z in [.14+i*.047 for i in range(10)]:
            for half in [-1,1]:
                angles=[math.pi*(i/48)+(0 if half==1 else math.pi) for i in range(49)]
                if z>.425:angles=angles[9:-9]
                vv=[];ff=[]
                for a in angles:
                    vv.extend([point(a,z-.022,key,.010),point(a,z+.022,key,.010),point(a,z+.022,key,.021),point(a,z-.022,key,.021)])
                for j in range(len(angles)-1):
                    for k in range(4):ff.append((j*4+k,j*4+(k+1)%4,(j+1)*4+(k+1)%4,(j+1)*4+k))
                ff.extend([(3,2,1,0),tuple((len(angles)-1)*4+k for k in range(4))])
                mm=bpy.data.meshes.new('formed_band');mm.from_pydata(vv,[],ff);mm.update();oo=bpy.data.objects.new('band',mm);bpy.context.collection.objects.link(oo);g.finish(oo,'overlapping_steel_band','armor_iron')
    for z in [.24,.32,.40]:
        box('front_fastener',(0,-point(-math.pi/2,z,key).length*.0-abs(point(-math.pi/2,z,key).y)-.008,z),(.035,.012,.023),'armor_gold' if 'mithril' in key else 'armor_iron',.003)
    if 'elven' in key:
        for side in [-1,1]:
            pts=[(-.12+side*.035*math.sin(i/30*math.pi),-.151,.43+i*.006) for i in range(31)];limb('leaf_scroll',pts,[.003]*31,'armor_gold')
    if 'dwarvish' in key:
        for x in [-.11,.11]:box('geometric_chest_plate',(x,-.153,.50),(.12,.017,.095),'armor_mithril',.009)
BLEND_NAME='ArmorStudy.blend';REPORT_NAME='projection-report-armor-study.json'
SOURCE_TILE_NAMES={key:key.replace('_',' ').replace('mithril coat','mithril-coat') for key in GROUPS};SPATIAL_MASK_KEYS=GROUPS
pipeline=Path(__file__).with_name('CreatureBatch2Pipeline.py').read_text(encoding='utf-8').replace('win/share/monsters.txt','win/share/objects.txt')
exec(compile(pipeline,'ArmorStudyPipeline','exec'))
