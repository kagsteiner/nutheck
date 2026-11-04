import sys,bpy,bmesh,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from CreatureGeometry import *
bpy.ops.wm.open_mainfile(filepath=str(OUT/'CreatureBatch30.blend'))
for c in bpy.data.collections:c.hide_viewport=False
bpy.context.view_layer.update();o=next(o for o in bpy.data.objects if o.get('creature')=='gelatinous_cube' and o.type=='MESH');bpy.context.view_layer.objects.active=o
bpy.ops.object.select_all(action='DESELECT');o.select_set(True);o.data.remesh_voxel_size=.012;bpy.ops.object.voxel_remesh()
for f in o.data.polygons:f.use_smooth=True
src=Path(__file__).with_name('CreateCreatureBatch30.py').read_text();exec(src[src.index('def pigment('):src.index('PIGMENT_FUNCTION=')])
mesh=o.data
for a in list(mesh.color_attributes):mesh.color_attributes.remove(a)
a=mesh.color_attributes.new(name='Paint',type='FLOAT_COLOR',domain='CORNER');mesh.color_attributes.active_color=a
for loop in mesh.loops:
 p=o.matrix_world@mesh.vertices[loop.vertex_index].co;c=pigment(o,p,(.88,.16,.012),{});a.data[loop.index].color=(*c,1)
low=min((o.matrix_world@v.co).z for v in mesh.vertices);o.location.z-=low
bpy.ops.export_scene.fbx(filepath=str(OUT/'gelatinous_cube.fbx'),use_selection=True,object_types={'MESH'},apply_unit_scale=True,axis_forward='-Y',axis_up='Z',add_leaf_bones=False,bake_anim=False,mesh_smooth_type='FACE')
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'CreatureBatch30.blend'))
print('CUBE_PAINT_SAMPLING_REFINED')
