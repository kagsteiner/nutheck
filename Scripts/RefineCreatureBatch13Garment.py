"""One-time replacement of leader's intersecting cloth/belt; preserve all anatomy."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from CreatureGeometry import *
import CreatureGeometry as g
from KoboldFamily import rank_garment
bpy.ops.wm.open_mainfile(filepath=str(OUT/'CreatureBatch13.blend'))
for c in bpy.data.collections:c.hide_viewport=False
bpy.context.view_layer.update()
for o in list(bpy.data.objects):
    if o.type=='MESH':
        if o.name in ['kobold_leader_detachable_rank_tunic','kobold_leader_detachable_rank_belt']:bpy.data.objects.remove(o,do_unlink=True)
        else:o['preserve_paint']=True
for key,color in {'kobold_orange':(.95,.22,.012),'kobold_cool':(.11,.25,.38)}.items():
    COLORS[key]=color;MATS[key]=bpy.data.materials[key]
g.GROUP='kobold_leader';rank_garment(.134,.99/.88)
for o in list(bpy.context.scene.objects):
    if o.type=='MESH' and o.get('creature')=='kobold_leader' and not o.get('preserve_paint'):
        for c in list(o.users_collection):c.objects.unlink(o)
        bpy.data.collections['kobold_leader'].objects.link(o)
pipeline=Path(__file__).with_name('CreatureBatch2Pipeline.py').read_text()
exec(compile(pipeline[:pipeline.index('if globals().get(\'POST_PAINT\')')],'paint_replacement_cloth','exec'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
    if o.type=='MESH' and o.get('creature')=='kobold_leader':o.select_set(True)
bpy.ops.export_scene.fbx(filepath=str(OUT/'kobold_leader.fbx'),use_selection=True,object_types={'MESH'},apply_unit_scale=True,axis_forward='-Y',axis_up='Z',add_leaf_bones=False,bake_anim=False,mesh_smooth_type='FACE')
for key in ['kobold','large_kobold','kobold_leader']:
    bpy.data.collections[key].hide_viewport=key!='kobold'
    for o in bpy.data.collections[key].objects:o.hide_render=key!='kobold'
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'CreatureBatch13.blend'))
print('CREATURE_BATCH13_GARMENT_REFIT_READY',flush=True)
