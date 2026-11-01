"""One UV-mapped upright quad; sprites are instanced, not per-pixel geometry."""
import bpy
from pathlib import Path
root=Path(__file__).resolve().parents[1];out=root/'Art/TileFallback';out.mkdir(parents=True,exist_ok=True)
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
bpy.context.scene.unit_settings.system='METRIC';bpy.context.scene.unit_settings.scale_length=1
mesh=bpy.data.meshes.new('TileStandee');mesh.from_pydata([(-.5,0,0),(.5,0,0),(.5,0,1),(-.5,0,1)],[],[(0,1,2,3)]);mesh.update()
uv=mesh.uv_layers.new(name='UVMap')
for loop,coord in zip(mesh.loops,[(0,0),(1,0),(1,1),(0,1)]):uv.data[loop.index].uv=coord
obj=bpy.data.objects.new('TileStandee',mesh);bpy.context.collection.objects.link(obj);obj.select_set(True);bpy.context.view_layer.objects.active=obj
bpy.ops.export_scene.fbx(filepath=str(out/'TileStandee.fbx'),use_selection=True,object_types={'MESH'},apply_unit_scale=True,axis_forward='-Y',axis_up='Z',bake_anim=False,mesh_smooth_type='FACE')
bpy.ops.wm.save_as_mainfile(filepath=str(out/'TileStandee.blend'))
print('TILE_STANDEE_READY triangles=2')
