"""Oracle: tile-derived seated, raised-arm human Pythia; static miniature."""
import sys,math,json,hashlib,re
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from CreatureGeometry import *
import CreatureGeometry as g
from HumanPlayerFamily import face_eyes,hair_cap
OUT=ROOT/'Art/CreatureInterpretations';GROUPS=['oracle'];g.GROUP='oracle'
manifest=OUT/'oracle-protected.json'
if not manifest.exists():manifest.write_text(json.dumps({p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'Art').rglob('*.fbx') if p.stem!='oracle'},indent=2))
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
palette={'human_skin':(.76,.43,.29),'human_dark':(.018,.012,.014),'human_sclera':(.82,.79,.70),'human_blue':(.10,.18,.24),'human_brow':(.65,.65,.59),'oracle_lip':(.32,.12,.10),'oracle_white':(.87,.86,.76),'oracle_blue':(.018,.055,.68),'oracle_cyan':(.015,.43,.67),'oracle_fold':(.015,.16,.43),'oracle_leaf':(.17,.53,.012),'oracle_leaf_dark':(.08,.27,.012)}
for key,c in palette.items():
 COLORS[key]=c;m=bpy.data.materials.new(key);m.use_nodes=True;m.diffuse_color=(*c,1);m.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.82;MATS[key]=m
# Round the tubular construction before union so limbs have sculpted contours.
_base_limb=limb
def limb(name,points,radii,color):
 # Dense curved centerline preserves full joint volume while smoothing contour.
 pts=[Vector(p) for p in points];dense=[];rr=[]
 for i in range(len(pts)-1):
  p0=pts[max(0,i-1)];p1=pts[i];p2=pts[i+1];p3=pts[min(len(pts)-1,i+2)]
  for j in range(12):
   t=j/12;dense.append(.5*((2*p1)+(-p0+p2)*t+(2*p0-5*p1+4*p2-p3)*t*t+(-p0+3*p1-3*p2+p3)*t*t*t));rr.append(radii[i]*(1-t)+radii[i+1]*t)
 dense.append(pts[-1]);rr.append(radii[-1]);verts=[];faces=[];n=24
 for i,p in enumerate(dense):
  d=(dense[min(i+1,len(dense)-1)]-dense[max(0,i-1)]).normalized();right=d.cross(Vector((0,1,0))).normalized();up=d.cross(right).normalized()
  for j in range(n):
   a=math.tau*j/n;verts.append(p+rr[i]*(right*math.cos(a)+up*math.sin(a)))
 for i in range(len(dense)-1):
  for j in range(n):a=i*n+j;b=i*n+(j+1)%n;faces.append((a,b,b+n,a+n))
 faces += [tuple(reversed(range(n))),tuple((len(dense)-1)*n+i for i in range(n))]
 mesh=bpy.data.meshes.new(name);mesh.from_pydata(verts,[],faces);mesh.update();o=bpy.data.objects.new(name,mesh);bpy.context.collection.objects.link(o);g.finish(o,name,color)
 for f in mesh.polygons:f.use_smooth=True
 return o

hz=.94
parts=[orb('pelvis',(0,0,.33),(.16,.11,.13),'human_skin'),orb('abdomen',(0,0,.49),(.115,.09,.17),'human_skin'),orb('ribcage',(0,0,.65),(.16,.105,.16),'human_skin'),limb('neck',[(0,0,.72),(0,0,.85)],[.062,.050],'human_skin'),orb('skull',(0,-.005,hz),(.101,.088,.132),'human_skin'),orb('jaw',(0,-.025,hz-.07),(.077,.073,.068),'human_skin'),orb('nose_bridge',(0,-.085,hz-.006),(.014,.022,.035),'human_skin'),orb('nose_tip',(0,-.113,hz-.034),(.019,.023,.016),'human_skin')]
for side in [-1,1]:
 parts.append(orb('ear',(side*.10,-.003,hz),(.018,.017,.033),'human_skin'))
 parts.append(limb('raised_arm',[(side*.145,0,.70),(side*.245,-.012,.73),(side*.35,-.015,.97),(side*.405,-.014,1.08)],[.049,.040,.030,.025],'human_skin'))
 parts.append(orb('palm',(side*.415,-.013,1.105),(.040,.024,.038),'human_skin'))
 # Actual bent thigh, knee, shin and ankle: crossing occurs below the tunic.
 z=.095 if side==-1 else .14
 parts.append(limb('folded_leg',[(side*.09,0,.34),(side*.30,-.03,.20),(-side*.09,-.22,z)],[.082,.068,.040],'human_skin'))
 parts.append(orb('knee',(side*.295,-.035,.20),(.075,.067,.065),'human_skin'))
 parts.append(orb('foot',(-side*.16,-.235,z-.012),(.095,.050,.035),'human_skin'))
body=sculpt_union(parts,'oracle_anatomy','human_skin',.0045);body['native_id']='PM_ORACLE';body['seated']=True;body['head_z']=hz
bpy.context.view_layer.update();face_eyes('oracle',body,hz,'human_skin','human_blue')
# Chanting mouth is the source black facial aperture, not an oversized eye.
orb('open_mouth',(0,-.100,hz-.082),(.019,.003,.008),'human_dark')
limb('lower_lip',[(-.018,-.100,hz-.087),(0,-.104,hz-.09),(.018,-.100,hz-.087)],[.0018]*3,'oracle_lip')
for side in [-1,1]:
 for j in range(4):
  x=side*(.398+j*.014)
  limb('raised_finger',[(x,-.015,1.115),(x+side*.010,-.014,1.157),(x+side*.019,-.012,1.160-j*.004)],[.007,.006,.0048],'human_skin')
 limb('thumb',[(side*.391,-.020,1.10),(side*.370,-.043,1.124)],[.011,.007],'human_skin')
 # Five toes make the bare feet complete without a shadow-derived limb.
 for j in range(5):orb('toe',(-side*(.19+j*.010),-.264,.078 if side==-1 else .123),(.012,.015,.011),'human_skin')
hair_cap(hz,'oracle_white')
for j in range(9):
 a=math.pi*j/8
 x=.094*math.cos(a);y=.028+.070*math.sin(a)
 limb('flowing_rear_hair',[(x,y,1.00),(x*1.10,y+.012,.92),(x*1.12,y+.024,.79),(x*.95,y+.023,.71)],[.025,.029,.026,.013],'oracle_white')
for side in [-1,1]:
 limb('temple_lock',[(side*.093,-.047,1.005),(side*.112,-.051,.94),(side*.115,-.056,.84),(side*.10,-.042,.76)],[.018,.019,.018,.009],'oracle_white')
 for j in range(5):
  x=side*(.020+j*.017);y=-.079+.022*j/4;z=1.04-.008*j
  leaf=orb('laurel_leaf',(x,y,z),(.018,.006,.008),'oracle_leaf' if j%2 else 'oracle_leaf_dark');leaf.rotation_euler.y=side*(-.30+j*.12)
# Closed elliptical folded shells; no flat tile extrusion, rear and underside complete.
def robe(name,stations,color):
 n=96;verts=[];faces=[]
 stations=[tuple(a*(1-t/6)+b*t/6 for a,b in zip(stations[j],stations[j+1])) for j in range(len(stations)-1) for t in range(6)]+[stations[-1]]
 for z,rx,ry,fold in stations:
  for i in range(n):
   a=math.tau*i/n;ripple=fold*math.cos(12*a+1.2*math.sin(z*8))+ .003*math.sin(20*z+4*a);verts.append(((rx+ripple)*math.cos(a),(ry+ripple*.7)*math.sin(a),z))
 for j in range(len(stations)-1):
  for i in range(n):a=j*n+i;b=j*n+(i+1)%n;faces.append((a,b,b+n,a+n))
 faces += [tuple(reversed(range(n))),tuple((len(stations)-1)*n+i for i in range(n))]
 mm=bpy.data.meshes.new(name);mm.from_pydata(verts,[],faces);mm.update();o=bpy.data.objects.new(name,mm);bpy.context.collection.objects.link(o);g.finish(o,name,color)
 for p in mm.polygons:p.use_smooth=True
 o['robe']=True
 return o
robe('blue_chiton',[(.26,.310,.160,.006),(.32,.290,.155,.01),(.44,.165,.120,.007),(.52,.130,.112,.006),(.63,.169,.119,.005),(.71,.156,.105,.004),(.75,.078,.076,.001)],'oracle_cyan')
# Floor origin for this seated pose.
bpy.context.view_layer.update();objs=[o for o in bpy.data.objects if o.type=='MESH'];low=min((o.matrix_world@v.co).z for o in objs for v in o.data.vertices)
for o in objs:o.location.z-=low

def pigment(o,p,c,colors):
 if o.get('robe'):
  if p.x>.025:return colors['oracle_blue']
  return tuple(v*(.94+.045*math.sin(p.z*61+p.x*23)) for v in c)
 if o.name=='oracle_oracle_anatomy' and p.z>.85:
  # Restrained warm cheek paint directly on skin.
  w=.12*max(0,1-abs(abs(p.x)-.06)/.03)*max(0,1-abs(p.z-.90)/.035)
  return tuple(a*(1-w)+b*w for a,b in zip(c,colors['oracle_lip']))
 return c
PIGMENT_FUNCTION=pigment;BLEND_NAME='OracleCreature.blend';REPORT_NAME='projection-report-oracle.json';SOURCE_TILE_NAMES={'oracle':'Oracle,female'}
raw=(ROOT/'upstream/NetHack/win/share/monsters.txt').read_text();rows=next(c for _,b,c in re.findall(r'^# tile (\d+) \(([^\n]+)\)\s*\{([^}]+)\}',raw,re.M) if b=='Oracle,female').strip().splitlines()
# Explicit source anatomy mask retains the central dark mouth, excludes right/lower cast shadow.
SOURCE_FIGURE_MASKS={'oracle':[(x,y) for y,row in enumerate(rows) for x,ch in enumerate(row.strip()) if ch not in {'.','A'} or (ch=='A' and y==5 and x in [7,8]) ]}
exec(compile(Path(__file__).with_name('CreatureBatch2Pipeline.py').read_text(encoding='utf-8'),'OracleCreaturePipeline','exec'))
