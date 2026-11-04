"""Tile-derived primate family; independent proportions, complete digits, static poses."""
import math,bpy
from mathutils import Vector,Matrix
from mathutils.bvhtree import BVHTree
import CreatureGeometry as g
from CreatureGeometry import orb,limb,sculpt_union

def limb(name,points,radii,color):
 # Interpolate anatomical joints before meshing, avoiding wedge-like knees/elbows.
 pts=[Vector(p) for p in points];dense=[];rr=[]
 for i in range(len(pts)-1):
  a=pts[max(0,i-1)];b=pts[i];c=pts[i+1];d=pts[min(len(pts)-1,i+2)]
  for j in range(6):
   t=j/6;dense.append(.5*(2*b+(-a+c)*t+(2*a-5*b+4*c-d)*t*t+(-a+3*b-3*c+d)*t*t*t));rr.append(radii[i]*(1-t)+radii[i+1]*t)
 dense.append(pts[-1]);rr.append(radii[-1])
 # Transport the frame continuously. Switching reference axes at a bent knee
 # twists neighbouring rings and can leave false gaps after voxel remeshing.
 verts=[];faces=[];n=16;right=None
 for i,p in enumerate(dense):
  direction=(dense[min(i+1,len(dense)-1)]-dense[max(0,i-1)]).normalized()
  if right is None:
   helper=Vector((1,0,0)) if abs(direction.x)<.8 else Vector((0,1,0));right=direction.cross(helper).normalized()
  else:right=(right-direction*right.dot(direction)).normalized()
  up=direction.cross(right).normalized()
  for j in range(n):
   a=math.tau*j/n;verts.append(p+rr[i]*(right*math.cos(a)+up*math.sin(a)))
 for i in range(len(dense)-1):
  for j in range(n):a=i*n+j;b=i*n+(j+1)%n;faces.append((a,b,b+n,a+n))
 faces += [tuple(reversed(range(n))),tuple((len(dense)-1)*n+j for j in range(n))]
 mesh=bpy.data.meshes.new(name);mesh.from_pydata(verts,[],faces);mesh.update();o=bpy.data.objects.new(name,mesh);bpy.context.collection.objects.link(o);g.finish(o,name,color)
 for face in mesh.polygons:face.use_smooth=True
 return o
SPECS={
 'monkey':dict(h=.72,head=.082,shoulder=.100,hip=.072,arm=.035,face=.047,pose=0),
 'ape':dict(h=1.17,head=.135,shoulder=.220,hip=.130,arm=.079,face=.075,pose=1),
 'carnivorous_ape':dict(h=1.30,head=.150,shoulder=.270,hip=.145,arm=.098,face=.085,pose=2)}

def build(key):
 g.GROUP=key;s=SPECS[key];h=s['h'];r=s['head'];w=s['shoulder'];pose=s['pose'];coat='primate_coat';skin='primate_skin';before=set(bpy.data.objects)
 hz=h-r*1.05;hipz=h*.40;chestz=h*.65
 parts=[orb('pelvis',(0,.025,hipz),(s['hip'],r*.83,h*.135),coat),orb('abdomen',(0,.018,h*.51),(w*.63,r*.88,h*.18),coat),orb('chest',(0,0,chestz),(w,r*1.15,h*.17),coat),orb('neck',(0,-.012,hz-r*.85),(r*.70,r*.75,r*.85),coat),orb('skull',(0,-.024,hz),(r,r*.88,r*1.06),coat),orb('muzzle',(0,-r*.86,hz-r*.39),(r*.72,s['face'],r*.49),coat)]
 for side in [-1,1]:
  shoulder=(side*w*.89,0,chestz+.025);elbow=(side*w*1.21,-r*.20,h*.43);wrist=(side*w*1.23,-r*.70,h*.20)
  if pose==0 and side==-1:elbow=(side*w*1.45,-r*.38,h*.52);wrist=(side*w*1.36,-r*1.15,h*.60)
  if pose==2:elbow=(side*w*1.30,-r*.72,h*.49);wrist=(side*w*.98,-r*2.1,h*.53)
  parts += [orb('deltoid',shoulder,(s['arm']*1.19,s['arm'],s['arm']*1.35),coat),limb('arm',[shoulder,elbow,wrist],[s['arm'],s['arm']*.76,s['arm']*.45],coat)]
  knee=(side*s['hip']*.92,-r*.66,h*.23);ankle=(side*s['hip']*1.05,-r*.10,h*.062)
  parts.append(limb('leg',[(side*s['hip']*.67,.025,hipz),knee,ankle],[r*.66,r*.48,r*.28],coat))
  # Rounded external ears belong to the head, not shadow-derived side shapes.
  parts.append(orb('outer_ear',(side*r*.97,-.012,hz-r*.10),(r*.28,r*.21,r*.34),coat))
 # Broad low supraorbital ridge and cheek roots distinguish the ape face.
 if pose:
  for side in [-1,1]:parts.append(orb('brow_ridge',(side*r*.43,-r*.76,hz+r*.32),(r*.48,r*.23,r*.17),coat))
 body=sculpt_union(parts,'continuous_anatomy',coat,.004 if pose==0 else .006)
 mod=body.modifiers.new('Relax anatomical joints','SMOOTH');mod.factor=.65;mod.iterations=8;bpy.context.view_layer.objects.active=body;bpy.ops.object.modifier_apply(modifier=mod.name)
 body['anatomy']=True;body['fur_surface']=True;body['fur_leg_height']=h*.23;body['head_z']=hz;body['shoulder_width']=w*2;body['has_tail']=pose==0
 # Separate palms/digits permit readable opposed thumbs, not mitten hands.
 for side in [-1,1]:
  wrist=Vector((side*w*1.23,-r*.70,h*.20))
  if pose==0 and side==-1:wrist=Vector((side*w*1.36,-r*1.15,h*.60))
  if pose==2:wrist=Vector((side*w*.98,-r*2.1,h*.53))
  palm=wrist+Vector((0,-r*.10,-r*.25));pr=r*.37
  handparts=[orb('palm',palm,(pr,pr*.65,pr*1.2),skin)]
  for j in range(4):
   x=palm.x+(j-1.5)*pr*.46;z=palm.z-pr*.50
   handparts.append(limb('finger',[(x,palm.y,z),(x,palm.y-pr*.22,z-pr*(1.05+.12*(j in [1,2]))),(x,palm.y-pr*.65,z-pr*1.12)],[pr*.19,pr*.16,pr*.11],skin))
  handparts.append(limb('opposed_thumb',[palm+Vector((-side*pr*.66,0,.006)),palm+Vector((-side*pr*1.30,-pr*.30,-pr*.36)),palm+Vector((-side*pr*.95,-pr*.85,-pr*.75))],[pr*.27,pr*.22,pr*.15],skin))
  hand=sculpt_union(handparts,'hand',skin,.0018 if pose==0 else .0027);hand['hand_side']=side;hand['digits']=5
  footparts=[orb('foot',(side*s['hip']*1.05,-r*.42,h*.055),(r*.40,r*.75,h*.045),skin)]
  for j in range(4):
   x=side*s['hip']*1.05+(j-1.5)*r*.15
   footparts.append(limb('toe',[(x,-r*.60,h*.055),(x,-r*1.15,h*.042),(x,-r*1.28,h*.046)],[r*.105,r*.085,r*.055],skin))
  footparts.append(limb('opposed_big_toe',[(side*(s['hip']*1.05-r*.22),-r*.43,h*.058),(side*(s['hip']*1.05-r*.52),-r*.82,h*.045),(side*(s['hip']*1.05-r*.47),-r*1.05,h*.045)],[r*.16,r*.125,r*.075],skin))
  foot=sculpt_union(footparts,'foot',skin,.0018 if pose==0 else .0027);foot['foot_side']=side;foot['digits']=5
  orb('ear_inner',(side*r*1.03,-r*.15,hz-r*.10),(r*.17,r*.075,r*.23),skin)
 if pose==0:
  pts=[]
  for i in range(45):
   t=i/44;a=-math.pi*.55+t*math.pi*1.48
   pts.append((.05+.15*(1-.32*t)*math.cos(a),.12+.10*math.sin(a),hipz-.04+.21*t))
  pts=[(0,.06,hipz),(.03,.12,hipz-.04)]+pts
  tail=limb('curled_tail',pts,[.018*(1-i/(len(pts)-1))+.003 for i in range(len(pts))],coat);tail['tail']=True;tail['fur_surface']=True
 # Paint the muzzle/eye mask on the continuous skull. Eye patches ray-fit to it.
 tree=BVHTree.FromObject(body,bpy.context.evaluated_depsgraph_get());inv=body.matrix_world.inverted()
 for side in [-1,1]:
  def surface(u,v,lift):
   hit,normal,_,_=tree.ray_cast(inv@Vector((side*r*.43+u,-r*3,hz+r*.15+v)),Vector((0,1,0)),r*6)
   assert hit is not None,(key,side,u,v)
   return body.matrix_world@hit+Vector((0,-lift,0))
  for name,rx,rz,color,lift in [('orbital_rim',.215,.124,'black',.0007),('eye',.173,.089,'primate_blue' if pose else 'primate_dark',.0013),('pupil',.055,.066,'black',.0019)]:
   verts=[surface(0,0,lift)]
   for i in range(40):
    a=math.tau*i/40;verts.append(surface(r*rx*math.cos(a),r*rz*math.sin(a),lift))
   mesh=bpy.data.meshes.new(name);mesh.from_pydata(verts,[],[(0,i+1,(i+1)%40+1) for i in range(40)]);mesh.update();o=bpy.data.objects.new(name,mesh);bpy.context.collection.objects.link(o);g.finish(o,name,color);o['eye_patch']=True;o['eye_side']=side;o['eye_lift']=lift
  orb('nostril',(side*r*.24,-r*.86-s['face']*.92,hz-r*.34),(r*.085,r*.045,r*.055),'primate_dark')
 mouthz=hz-r*.65
 orb('mouth',(0,-r*.86-s['face']*.83,mouthz),(r*.43,r*.08,r*(.19 if pose==2 else .045)),'primate_red' if pose==2 else 'primate_dark')
 if pose==2:
  # Native red mouth accent; teeth are an inferred anatomical completion.
  for side in [-1,1]:orb('canine',(side*r*.25,-r*.86-s['face']*.89,mouthz+r*.06),(r*.05,r*.07,r*.09),'primate_ivory')
 # Rotate the complete figure to the established animal -X front.
 turn=Matrix.Rotation(-math.pi/2,4,'Z')
 for o in set(bpy.data.objects)-before:o.matrix_world=turn@o.matrix_world
 bpy.context.view_layer.update();meshes=[o for o in bpy.data.objects if o.type=='MESH' and o.get('creature')==key];low=min((o.matrix_world@v.co).z for o in meshes for v in o.data.vertices)
 for o in meshes:o.location.z-=low

def pigment(o,p,c,colors):
 if not o.get('anatomy'):return c
 key=o['creature'];s=SPECS[key];r=s['head'];hz=o['head_z']
 # Local -Y front becomes world -X; face, chest and ears are continuous paint.
 face=max(0,min(1,(-p.x-r*.43)/(r*.40)))*max(0,1-abs(p.z-(hz-r*.23))/(r*.93))
 chest=max(0,min(1,(-p.x-r*.65)/(r*.40)))*max(0,1-abs(p.z-s['h']*.57)/(s['h']*.16))*.52
 w=max(face,chest);return tuple(a*(1-w)+b*w for a,b in zip(c,colors['primate_skin']))
