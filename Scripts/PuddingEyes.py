"""Official-tile eyes, following explicit user interpretation despite native NOEYES."""
import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree
import CreatureGeometry as g
def add_eyes(key,body):
 g.GROUP=key;bpy.context.view_layer.update();tree=BVHTree.FromObject(body,bpy.context.evaluated_depsgraph_get());inv=body.matrix_world.inverted();out=[]
 colors={'pudding_eye_pale':(.88,.84,.70),'pudding_eye_dark':(.004,.003,.002),'pudding_eye_hot':(.98,.17,.002)}
 for name,c in colors.items():
  g.COLORS[name]=c;mat=bpy.data.materials.get(name) or bpy.data.materials.new(name);mat.use_nodes=True;mat.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.32;g.MATS[name]=mat
 for side in [-1,1]:
  brown=key=='brown_pudding';y=side*(.082 if brown else .047);z=.34 if brown else .78
  for name,w,h,color,lift in ([('eye',.048,.048,'pudding_eye_pale',.004),('pupil',.021,.026,'pudding_eye_dark',.013)] if brown else [('eye',.029,.040,'pudding_eye_hot',.004)]):
   o=g.orb(name,(0,0,0),(.009,w,h),color)
   for v in o.data.vertices:
    hit,normal,_,_=tree.ray_cast(inv@Vector((-1,y+v.co.y,z+v.co.z)),Vector((1,0,0)),2)
    assert hit is not None,(key,side,name)
    v.co=body.matrix_world@hit+Vector((v.co.x-lift,0,0))
   o['tile_eye']=True;o['eye_side']=side;o['primary_eye']=name=='eye';out.append(o)
 return out
