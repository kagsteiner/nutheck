"""Orb of Fate: deep blue crystal in three interwoven silver fate rings."""
import bpy,math
from pathlib import Path
from mathutils import Vector
root=Path(__file__).resolve().parents[1];out=root/'Art/ObjectInterpretations'
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
colors={'of_crystal':(.055,.20,.34),'of_silver':(.58,.72,.79),'of_gold':(.60,.34,.075),'of_star':(.58,.90,1.)}
materials={}
for key,c in colors.items():
 m=bpy.data.materials.new(key);m.diffuse_color=(*c,1);m.use_nodes=True;n=m.node_tree.nodes['Principled BSDF'];n.inputs['Base Color'].default_value=(*c,1);n.inputs['Metallic'].default_value=.85 if key in ('of_gold','of_silver') else .15;n.inputs['Roughness'].default_value=.20;materials[key]=m

def finish(o,key):
 o.data.materials.append(materials[key]);a=o.data.color_attributes.new(name='Color',type='BYTE_COLOR',domain='CORNER')
 for d in a.data:d.color=(*colors[key],1)
 for f in o.data.polygons:f.use_smooth=True
 return o
bpy.ops.mesh.primitive_uv_sphere_add(segments=64,ring_count=32,radius=.205,location=(0,0,.29));finish(bpy.context.object,'of_crystal')
for axis in range(3):
 bpy.ops.mesh.primitive_torus_add(major_segments=96,minor_segments=12,major_radius=.24,minor_radius=.012,location=(0,0,.29))
 o=bpy.context.object;o.rotation_euler=(math.radians(65 if axis<2 else 0),math.radians(25 if axis==1 else 0),axis*math.tau/3);finish(o,'of_silver')
 # Gold hour beads at regular intervals along each fate ring.
 for i in range(12):
  a=i*math.tau/12;v=o.rotation_euler.to_matrix()@Vector((.24*math.cos(a),.24*math.sin(a),0))
  bpy.ops.mesh.primitive_uv_sphere_add(segments=12,ring_count=8,radius=.018 if i%3==0 else .008,location=Vector((0,0,.29))+v);finish(bpy.context.object,'of_gold')
# A constellation set into the upper hemisphere: readable pale nodes and fine silver threads.
pts=[(-.10,-.06,.458),(-.045,-.10,.463),(.01,-.04,.49),(.08,-.06,.466),(.10,.035,.463)]
for p in pts:
 bpy.ops.mesh.primitive_uv_sphere_add(segments=16,ring_count=8,radius=.009,location=p);finish(bpy.context.object,'of_star')
for a,b in zip(pts,pts[1:]):
 v=Vector(b)-Vector(a);bpy.ops.mesh.primitive_cylinder_add(vertices=10,radius=.002,depth=v.length,location=(Vector(a)+Vector(b))/2);o=bpy.context.object;o.rotation_euler=v.to_track_quat('Z','Y').to_euler();finish(o,'of_silver')
bpy.ops.wm.save_as_mainfile(filepath=str(out/'OrbOfFate.blend'))
bpy.ops.object.select_all(action='SELECT')
bpy.ops.export_scene.fbx(filepath=str(out/'orb_of_fate.fbx'),use_selection=True,object_types={'MESH'},apply_unit_scale=True,apply_scale_options='FBX_SCALE_ALL',axis_forward='-Y',axis_up='Z',bake_anim=False,mesh_smooth_type='FACE',colors_type='SRGB')

# A shareable model preview, separate from the native gameplay view.
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=48
scene.world.color=(.16,.16,.16)
bpy.ops.object.camera_add(location=(.95,-1.45,1.1));camera=bpy.context.object
camera.rotation_euler=(Vector((0,0,.29))-camera.location).to_track_quat('-Z','Y').to_euler();camera.data.type='ORTHO';camera.data.ortho_scale=.8;scene.camera=camera
for at,power,size in [((1,-2,2),180,2),((-1,-.3,1),100,1),((0,2,1),200,1)]:
 bpy.ops.object.light_add(type='AREA',location=at);o=bpy.context.object;o.data.energy=power;o.data.shape='DISK';o.data.size=size;o.rotation_euler=(Vector((0,0,.29))-o.location).to_track_quat('-Z','Y').to_euler()
scene.render.resolution_x=900;scene.render.resolution_y=900;scene.render.resolution_percentage=100
scene.render.filepath=str(out/'OrbOfFate.png');bpy.ops.render.render(write_still=True)
