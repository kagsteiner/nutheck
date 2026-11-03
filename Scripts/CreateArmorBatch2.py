"""Three plate armors and ten active dragon-scale mails; static design drafts."""
import sys,math,json,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from CreatureGeometry import *
import CreatureGeometry as g
OUT=ROOT/'Art/ObjectInterpretations'
DRAGONS={'gray':(.25,.29,.33),'gold':(.64,.36,.055),'silver':(.57,.68,.75),'red':(.44,.018,.009),'white':(.70,.76,.77),'orange':(.70,.16,.010),'black':(.012,.019,.025),'blue':(.015,.085,.48),'green':(.018,.30,.065),'yellow':(.66,.49,.015)}
GROUPS=['plate_mail','crystal_plate_mail','bronze_plate_mail']+[c+'_dragon_scale_mail' for c in DRAGONS]
manifest=OUT/'armor-batch2-protected.json'
if not manifest.exists():
    files=[p for f in ['CreatureInterpretations','ObjectInterpretations','EnvironmentInterpretations','TileFallback'] for p in (ROOT/'Art'/f).glob('*.fbx')]
    manifest.write_text(json.dumps({p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in files},indent=2))
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
PALETTES={'plate_steel':((.32,.39,.43),.23,1),'plate_bronze':((.48,.23,.065),.29,.9),'plate_crystal':((.67,.83,.90),.055,.75),'armor_dark':((.019,.025,.028),.85,0),'regal_silver':((.65,.76,.81),.17,1),'regal_gold':((.62,.36,.075),.25,.85),'dragon_horn':((.21,.19,.15),.5,0)}
PALETTES.update({'dragon_'+c:(rgb,.24 if c in ['gray','silver','gold'] else .32,.6 if c in ['gray','silver','gold'] else .14) for c,rgb in DRAGONS.items()})
for key,(col,rough,metal) in PALETTES.items():
    COLORS[key]=col;m=bpy.data.materials.new(key);m.use_nodes=True;m.diffuse_color=(*col,1);s=m.node_tree.nodes['Principled BSDF'];s.inputs['Roughness'].default_value=rough;s.inputs['Metallic'].default_value=metal
    if key=='plate_crystal':s.inputs['Coat Weight'].default_value=1;s.inputs['Coat Roughness'].default_value=.025
    MATS[key]=m
# Reuse construction functions, not prior meshes or any previous output files.
old=Path(__file__).with_name('CreateArmorStudy.py').read_text()
exec(compile(old[old.index('def point('):old.index('\nfor key in GROUPS:')],'ArmorShellHelpers','exec'))
def setpigment(o,key):o['pigment']=key;o.data.materials.clear();o.data.materials.append(MATS[key])
def crest(name,center,u,v,normal,w,h,pigment):
    outline=[(-w,0),(-w*.72,h*.55),(0,h*.78),(w*.72,h*.55),(w,0),(0,-h*.78)]
    vv=[center+u*x+v*y+normal*.002 for x,y in outline];vv+=[center+u*x+v*y-normal*.006 for x,y in outline];vv.append(center+normal*.017)
    ff=[(12,i,(i+1)%6) for i in range(6)]+[tuple(reversed(range(6,12)))]+[(i,i+6,(i+1)%6+6,(i+1)%6) for i in range(6)]
    mm=bpy.data.meshes.new(name);mm.from_pydata(vv,[],ff);mm.update();o=bpy.data.objects.new(name,mm);bpy.context.collection.objects.link(o);g.finish(o,name,pigment);return o
from DragonMailFamily import build as build_dragon_mail
for key in GROUPS:
    if '_dragon_' in key:
        build_dragon_mail(key)
        continue
    g.GROUP=key;core=shell(key)
    pigment={'plate_mail':'plate_steel','bronze_plate_mail':'plate_bronze','crystal_plate_mail':'plate_crystal'}[key]
    trim='regal_silver' if key=='crystal_plate_mail' else 'plate_steel'
    setpigment(core,pigment)
    # Broad angular chest/back plates and overlapping lower lames.
    for face in [-1,1]:
        normal=Vector((0,face,0));u=Vector((1,0,0));v=Vector((0,0,1))
        crest('ridged_cuirass',Vector((0,face*.147,.487)),u,v,normal,.213,.175,pigment)
        for x in [-.13,0,.13]:crest('articulated_tasset',Vector((x,face*.127,.195)),u,v,normal,.072,.100,pigment)
        for x in [-.155,.155]:orb('plate_rivet',(x,face*.16,.47),(.007,.005,.007),trim)
    for z in [.30,.335]:limb('waist_lame',[point(math.tau*i/96,z,key,.015) for i in range(97)],[.012]*97,pigment)
    for z in [.095,.675]:limb('crafted_edge_binding',[point(math.tau*i/96,z,key,.016) for i in range(97)],[.006]*97,trim)

def paint(o,p,c,colors):
    if o['pigment'].startswith('dragon_'):
        f=.87+.12*math.sin(p.x*83+p.z*67)*math.sin(p.y*71-p.z*45);return tuple(v*f for v in c)
    return c
BLEND_NAME='ArmorBatch2.blend';REPORT_NAME='projection-report-armor-batch2.json';PIGMENT_FUNCTION=paint
SOURCE_TILE_NAMES={k:k.replace('_',' ') for k in GROUPS};SPATIAL_MASK_KEYS=GROUPS
pipeline=Path(__file__).with_name('CreatureBatch2Pipeline.py').read_text(encoding='utf-8').replace('win/share/monsters.txt','win/share/objects.txt')
exec(compile(pipeline,'ArmorBatch2Pipeline','exec'))
