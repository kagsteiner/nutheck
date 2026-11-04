"""Three tile-derived centaur miniatures; shared anatomy, independent proportions/poses."""
import sys,math,json,hashlib,re
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from CreatureGeometry import *
import CreatureGeometry as g
from HumanPlayerFamily import face_eyes,hair_cap,garment
from EquineFamily import hoof
OUT=ROOT/'Art/CreatureInterpretations';GROUPS=['plains_centaur','forest_centaur','mountain_centaur']
manifest=OUT/'centaurs-protected.json'
if not manifest.exists():manifest.write_text(json.dumps({p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'Art').rglob('*.fbx') if p.stem not in GROUPS},indent=2))
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
palette={'human_skin':(.76,.43,.29),'human_dark':(.018,.012,.014),'human_sclera':(.82,.79,.70),'human_blue':(.11,.17,.19),'human_brow':(.27,.08,.018),'centaur_hair':(.28,.075,.009),'centaur_coat':(.40,.13,.020),'centaur_deep':(.25,.075,.012),'centaur_horn':(.55,.24,.05),'centaur_jerkin':(.25,.11,.035)}
for key,c in palette.items():
 COLORS[key]=c;m=bpy.data.materials.new(key);m.use_nodes=True;m.diffuse_color=(*c,1);m.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.82;MATS[key]=m

def tube(name,points,radii,color):
 # Stable front/back frame for the sagittal curves, avoiding orientation jumps.
 pts=[Vector(p) for p in points];dense=[];rr=[]
 for i in range(len(pts)-1):
  p0=pts[max(0,i-1)];p1=pts[i];p2=pts[i+1];p3=pts[min(len(pts)-1,i+2)]
  for j in range(10):
   t=j/10;dense.append(.5*(2*p1+(-p0+p2)*t+(2*p0-5*p1+4*p2-p3)*t*t+(-p0+3*p1-3*p2+p3)*t*t*t));rr.append(radii[i]*(1-t)+radii[i+1]*t)
 dense.append(pts[-1]);rr.append(radii[-1]);verts=[];faces=[];n=24
 for i,p in enumerate(dense):
  d=(dense[min(i+1,len(dense)-1)]-dense[max(0,i-1)]).normalized();helper=Vector((0,1,0)) if abs(d.y)<.9 else Vector((0,0,1));right=d.cross(helper).normalized();up=d.cross(right).normalized()
  for j in range(n):
   a=math.tau*j/n;verts.append(p+rr[i]*(right*math.cos(a)+up*math.sin(a)))
 for i in range(len(dense)-1):
  for j in range(n):a=i*n+j;b=i*n+(j+1)%n;faces.append((a,b,b+n,a+n))
 faces += [tuple(reversed(range(n))),tuple((len(dense)-1)*n+i for i in range(n))]
 mesh=bpy.data.meshes.new(name);mesh.from_pydata(verts,[],faces);mesh.update();o=bpy.data.objects.new(name,mesh);bpy.context.collection.objects.link(o);g.finish(o,name,color)
 for f in mesh.polygons:f.use_smooth=True
 return o

for key,length,width,leg,bulk,arm in [('plains_centaur',.45,.19,.55,1.,0),('forest_centaur',.42,.165,.59,.89,1),('mountain_centaur',.48,.225,.56,1.16,2)]:
 g.GROUP=key;before=set(bpy.data.objects);hz=1.76 if arm!=2 else 1.84
 # Human upper body has the established -Y front until rotated onto the equine forequarters.
 parts=[orb('waist',(0,0,1.08),(.12*bulk,.105,.18),'human_skin'),orb('ribs',(0,0,1.32),(.18*bulk,.12,.23),'human_skin'),orb('trapezius',(0,0,1.49),(.15*bulk,.09,.08),'human_skin'),tube('neck',[(0,0,1.48),(0,0,hz-.10)],[.065,.055],'human_skin'),orb('skull',(0,-.005,hz),(.105,.09,.132),'human_skin'),orb('jaw',(0,-.025,hz-.07),(.085,.075,.068),'human_skin'),orb('nose_bridge',(0,-.085,hz-.005),(.015,.025,.038),'human_skin'),orb('nose_tip',(0,-.115,hz-.035),(.021,.024,.017),'human_skin')]
 for side in [-1,1]:
  shoulder=(side*.175*bulk,0,1.45);elbow=(side*.25*bulk,-.025,1.24);wrist=(side*.22*bulk,-.10,1.08)
  if arm==1 and side==-1:elbow=(side*.25,-.03,1.53);wrist=(side*.24,-.12,1.73)
  if arm==0 and side==-1:elbow=(side*.30,-.06,1.35);wrist=(side*.29,-.16,1.52)
  if arm==2:wrist=(side*.26,-.15,1.17)
  parts.append(orb('deltoid',shoulder,(.075*bulk,.070,.090),'human_skin'))
  parts.append(tube('arm',[shoulder,elbow,wrist],[.059*bulk,.042*bulk,.027*bulk],'human_skin'))
  palm=Vector(wrist)+Vector((0,-.015,-.025 if arm==2 else .025));parts.append(orb('palm',palm,(.036,.026,.045),'human_skin'))
  for j in range(4):
   x=palm.x+(j-1.5)*.014;up=-1 if arm==2 else 1
   tube('finger',[(x,palm.y,palm.z),(x,palm.y-.012,palm.z+up*.052),(x,palm.y-.028,palm.z+up*.057)],[.0075,.0065,.0045],'human_skin')
  tube('thumb',[(palm.x-side*.024,palm.y,palm.z),(palm.x-side*.048,palm.y-.025,palm.z+.018)],[.011,.007],'human_skin')
  parts.append(orb('ear',(side*.105,0,hz),(.018,.018,.035),'human_skin'))
 human=sculpt_union(parts,'human_anatomy','human_skin',.0055);human['centaur_human']=True;human['head_z']=hz
 mod=human.modifiers.new('Skin relaxation','SMOOTH');mod.factor=.7;mod.iterations=10;bpy.context.view_layer.objects.active=human;bpy.ops.object.modifier_apply(modifier=mod.name)
 bpy.context.view_layer.update();face_eyes(key,human,hz,'human_skin','human_blue');hair_cap(hz,'centaur_hair')
 tube('mouth',[(-.028,-.094,hz-.08),(0,-.103,hz-.082),(.028,-.094,hz-.08)],[.0015,.002,.0015],'human_dark')
 for side in [-1,1]:
  tube('temple_hair',[(side*.093,-.015,hz+.065),(side*.108,-.006,hz-.025),(side*.093,.004,hz-.065)],[.026,.026,.012],'centaur_hair')
 # A short chestnut beard echoes the dark/orange lower-face source marks.
 beard=orb('beard',(0,-.055,hz-.115),(.071,.070,.062 if arm!=2 else .09),'centaur_hair')
 if arm==2:garment('brown_jerkin',[(1.03,.163,.135),(1.22,.225,.150),(1.42,.245,.155),(1.49,.20,.125)],'centaur_jerkin')
 human_objects=set(bpy.data.objects)-before
 from mathutils import Matrix
 turn=Matrix.Rotation(-math.pi/2,4,'Z');shift=Matrix.Translation(Vector((-length*.65,0,0)))
 for o in human_objects:o.matrix_world=shift@turn@o.matrix_world
 z=leg+.20;shoulder=-length*.63;hip=length*.66
 parts=[orb('barrel',(0,0,z),(length,width,.22),'centaur_coat'),orb('haunch',(hip,0,z),(.24,width*1.03,.23),'centaur_coat'),orb('equine_shoulder',(shoulder,0,z+.025),(.22,width,.25),'centaur_coat'),orb('torso_transition',(shoulder,0,z+.18),(.17,width*.78,.22),'centaur_coat')]
 for back,x in [(False,shoulder),(True,hip)]:
  for side in [-1,1]:
   y=side*width*.70;offset=(.025 if side==1 else -.025)
   path=[(x,y,z),((x-.065 if back else x+.01),y,leg*.82),(x+.085 if back else x-.01,y,leg*.43),(x+offset,y,.08)]
   parts.append(tube('hind_leg' if back else 'fore_leg',path,[width*.45,width*.32,width*.20,.033],'centaur_coat'))
   parts.append(orb('fetlock',(x+offset,y,.10),(.047,.041,.045),'centaur_coat'));hoof('hoof',x+offset-.012,y,.043 if arm!=2 else .049,'centaur_horn')
 horse=sculpt_union(parts,'equine_anatomy','centaur_coat',.0065);horse['centaur_equine']=True;horse['four_legs']=True
 mod=horse.modifiers.new('Equine sculpt relaxation','SMOOTH');mod.factor=.8;mod.iterations=12;bpy.context.view_layer.objects.active=horse;bpy.ops.object.modifier_apply(modifier=mod.name)
 tube('flowing_tail',[(hip+.13,0,z+.10),(hip+.26,.005,z+.02),(hip+.34,.015,z-.22),(hip+.33,.02,.16)],[.035,.045,.045,.008],'centaur_hair')
 # Floor origin, with all four hooves complete and the torso joined at the withers.
 bpy.context.view_layer.update();meshes=[o for o in bpy.data.objects if o.type=='MESH' and o.get('creature')==key];low=min((o.matrix_world@v.co).z for o in meshes for v in o.data.vertices)
 for o in meshes:o.location.z-=low

def pigment(o,p,c,colors):
 if o.get('centaur_equine'):
  w=.22*max(0,min(1,(.83-p.z)/.22));return tuple(v*(1-w) for v in c)
 return c
PIGMENT_FUNCTION=pigment;BLEND_NAME='Centaurs.blend';REPORT_NAME='projection-report-centaurs.json'
source=(ROOT/'upstream/NetHack/win/share/monsters.txt').read_text();tiles={n:rows.strip().splitlines() for _,n,rows in re.findall(r'^# tile (\d+) \(([^\n]+)\)\s*\{([^}]+)\}',source,re.M)}
# Reviewed spatial masks: keep small upper facial/neck dark marks; offset
# right/down black mass is cast shadow, not another limb or tail.
SOURCE_FIGURE_MASKS={key:[(x,y) for y,row in enumerate(tiles[key.replace('_',' ')+',male']) for x,ch in enumerate(row.strip()) if ch not in {'.','A'} or (ch=='A' and x in {3,4} and y in {4,5,6,7})] for key in GROUPS}
exec(compile(Path(__file__).with_name('CreatureBatch2Pipeline.py').read_text(encoding='utf-8'),'CentaurPipeline','exec'))
