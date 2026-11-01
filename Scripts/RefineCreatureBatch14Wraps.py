"""One-time saved wrap replacement; all ancestry vertices remain untouched."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from CreatureGeometry import *
from KoboldStates import mummy_wraps,state_pigment
bpy.ops.wm.open_mainfile(filepath=str(OUT/'CreatureBatch14.blend'))
for c in bpy.data.collections:c.hide_viewport=False
bpy.context.view_layer.update()
for obj in list(bpy.data.objects):
    if obj.type=='MESH':
        if obj.get('wrap_module'):bpy.data.objects.remove(obj,do_unlink=True)
        else:obj['preserve_paint']=True
COLORS['mummy_linen']=(.74,.71,.60);MATS['mummy_linen']=bpy.data.materials['mummy_linen']
body=bpy.data.objects['kobold_mummy_continuous_anatomy'];mummy_wraps(body,'kobold_mummy')
for obj in list(bpy.data.objects):
    if obj.type=='MESH' and obj.get('wrap_module'):
        for col in list(obj.users_collection):col.objects.unlink(obj)
        bpy.data.collections['kobold_mummy'].objects.link(obj)
PIGMENT_FUNCTION=state_pigment
pipeline=Path(__file__).with_name('CreatureBatch2Pipeline.py').read_text(encoding='utf-8')
exec(compile(pipeline[:pipeline.index("if globals().get('POST_PAINT')")],'paint_saved_wraps','exec'))
bpy.ops.object.select_all(action='DESELECT')
for obj in bpy.data.objects:
    if obj.type=='MESH' and obj.get('creature')=='kobold_mummy':obj.select_set(True)
bpy.ops.export_scene.fbx(filepath=str(OUT/'kobold_mummy.fbx'),use_selection=True,object_types={'MESH'},apply_unit_scale=True,axis_forward='-Y',axis_up='Z',add_leaf_bones=False,bake_anim=False,mesh_smooth_type='FACE')
for key in ['kobold_shaman','kobold_mummy','kobold_zombie']:
    bpy.data.collections[key].hide_viewport=key!='kobold_shaman'
    for obj in bpy.data.collections[key].objects:obj.hide_render=key!='kobold_shaman'
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'CreatureBatch14.blend'))
print('CREATURE_BATCH14_WRAP_REFIT_READY',flush=True)
