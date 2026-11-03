"""Named artifact design: short haft, forged iron, silver edges and gold interlace."""
import sys,math,hashlib,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from CreatureGeometry import *
import CreatureGeometry as g
OUT=ROOT/'Art/ObjectInterpretations';OUT.mkdir(parents=True,exist_ok=True)
manifest=OUT/'mjollnir-protected-assets.json'
if not manifest.exists():
    files=[p for folder in ['CreatureInterpretations','ObjectInterpretations','EnvironmentInterpretations','TileFallback'] for p in (ROOT/'Art'/folder).glob('*.fbx')]
    manifest.write_text(json.dumps({p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in files},indent=2))
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for key,color,rough,metal in [('object_iron',(.24,.29,.32),.22,1.0),('object_silver',(.65,.72,.76),.18,1.0),('object_gold',(.70,.36,.055),.32,.75),('hammer_leather',(.085,.028,.014),.76,0),('hammer_wood',(.17,.065,.020),.72,0),('hammer_seam',(.016,.022,.026),.65,.3)]:
    COLORS[key]=color;mat=bpy.data.materials.new(key);mat.use_nodes=True;mat.diffuse_color=(*color,1)
    sh=mat.node_tree.nodes['Principled BSDF'];sh.inputs['Roughness'].default_value=rough;sh.inputs['Metallic'].default_value=metal;MATS[key]=mat
g.GROUP='mjollnir'
# Grounded upright examination pose. Head has flaring, chamfered striking ends.
profile=[(-.28,.435),(-.30,.46),(-.30,.60),(-.27,.625),(-.16,.605),(-.09,.58),(.09,.58),(.16,.605),(.27,.625),(.30,.60),(.30,.46),(.28,.435),(.15,.452),(.08,.478),(-.08,.478),(-.15,.452)]
verts=[(x,y,z) for y in [-.095,.095] for x,z in profile];n=len(profile)
faces=[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
mesh=bpy.data.meshes.new('Forged flared head');mesh.from_pydata(verts,[],faces);mesh.update()
o=bpy.data.objects.new('head',mesh);bpy.context.collection.objects.link(o);g.finish(o,'forged_head','object_iron')
mod=o.modifiers.new('Forged edge chamfers','BEVEL');mod.width=.009;mod.segments=3
for x in [-.278,.278]:
    box('silver_striking_face',(x,0,.529),(.045,.202,.163),'object_silver',.009)
    for side in [-1,1]:
        for z in [.465,.591]:box('gold_face_border',(x,side*.104,z),(.035,.006,.008),'object_gold',.002)
box('haft',(0,0,.255),(.051,.056,.475),'hammer_wood',.012)
for z in [.067,.371,.439]:box('silver_collar',(0,0,z),(.070,.072,.024),'object_silver',.006)
grip=box('wooden_grip',(0,0,.218),(.064,.066,.275),'hammer_wood',.010)
# Dense surface sampling for longitudinal, slightly wandering painted wood grain.
for obj in list(bpy.data.objects):
    if obj.type=='MESH' and obj.get('pigment')=='hammer_wood':
        mod=obj.modifiers.new('Grain sampling','SUBSURF');mod.subdivision_type='SIMPLE';mod.levels=5
box('pommel',(0,0,.035),(.080,.078,.060),'object_iron',.012)
box('pommel_inlay',(0,-.040,.036),(.031,.005,.025),'object_gold',.001)
# Mirrored interlaced loops, shallow raised wire seated against both head faces.
# These are ornamental geometry, not claimed readable ancient inscriptions.
for side in [-1,1]:
    box('central_silver_boss',(0,side*.097,.532),(.075,.009,.072),'object_silver',.003)
    for sign in [-1,1]:
        pts=[]
        for i in range(161):
            t=i/160*math.tau
            pts.append((sign*(.128+.088*math.cos(t)),side*(.100+.003*math.sin(t*3)),.530+.038*math.sin(t*2)))
        limb('gold_interlace',pts,[.0028]*len(pts),'object_gold')
    # Diamond centre and dotted rivets make the middle readable at tile scale.
    pts=[(0,side*.105,.564),(.025,side*.105,.532),(0,side*.105,.500),(-.025,side*.105,.532),(0,side*.105,.564)]
    limb('central_diamond',pts,[.0025]*len(pts),'object_gold')
    for x in [-.227,.227]:orb('silver_rivet',(x,side*.100,.530),(.009,.005,.009),'object_silver')
def pigment(obj,p,color,colors):
    if obj['pigment']=='hammer_wood':
        grain=.5+.5*math.sin(p.x*1850+p.y*1370+math.sin(p.z*23)*1.7)
        return tuple(a*(1-grain*.55)+b*grain*.55 for a,b in zip((.40,.20,.065),(.13,.047,.010)))
    if obj['pigment']=='object_iron':
        shade=.91+.06*math.sin(p.x*143+p.z*177)*math.sin(p.y*151-p.z*89)
        return tuple(c*shade for c in color)
    return color
GROUPS=['mjollnir'];BLEND_NAME='Mjollnir.blend';REPORT_NAME='projection-report-mjollnir.json'
SOURCE_TILE_NAMES={'mjollnir':'war hammer'};PIGMENT_FUNCTION=pigment;SPATIAL_MASK_KEYS=GROUPS
pipeline=Path(__file__).with_name('CreatureBatch2Pipeline.py').read_text(encoding='utf-8').replace('win/share/monsters.txt','win/share/objects.txt')
exec(compile(pipeline,'MjollnirPipeline','exec'))


