"""One-time saved review fix: joined dome with narrow medial shell seam."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from CreatureGeometry import *
import CreatureGeometry as G
from AntBeetleFamily import elytron,insect_pigment
bpy.ops.wm.open_mainfile(filepath=str(OUT/'CreatureBatch22.blend'))
for c in bpy.data.collections:c.hide_viewport=False
abdomen=bpy.data.objects['giant_beetle_abdomen'];abdomen.location=(.18,0,.30);abdomen.dimensions=(.62,.46,.39)
bpy.context.view_layer.update()
for o in list(bpy.data.objects):
    if o.type=='MESH':
        if o.get('closed_elytron'):bpy.data.objects.remove(o,do_unlink=True)
        else:o['preserve_paint']=True
G.GROUP='giant_beetle';COLORS['beetle_red']=(.76,.012,.003);COLORS['beetle_highlight']=(.95,.48,.23);MATS['beetle_red']=bpy.data.materials['beetle_red']
for side in [-1,1]:
    o=elytron(side)
    for c in list(o.users_collection):c.objects.unlink(o)
    bpy.data.collections['giant_beetle'].objects.link(o)
PIGMENT_FUNCTION=insect_pigment
pipeline=Path(__file__).with_name('CreatureBatch2Pipeline.py').read_text()
exec(compile(pipeline[:pipeline.index('GROUPS=globals()')],'paint_repaired_elytra','exec'))
parts=[o for o in bpy.data.objects if o.type=='MESH' and o.get('creature')=='giant_beetle']
bpy.ops.object.select_all(action='DESELECT')
for o in parts:o.select_set(True)
bpy.context.view_layer.objects.active=parts[0]
bpy.ops.export_scene.fbx(filepath=str(OUT/'giant_beetle.fbx'),use_selection=True,object_types={'MESH'},apply_unit_scale=True,axis_forward='-Y',axis_up='Z',add_leaf_bones=False,bake_anim=False,mesh_smooth_type='FACE')
for key in ['soldier_ant','soldier_ant_female','fire_ant','fire_ant_female','giant_beetle']:
    bpy.data.collections[key].hide_viewport=key!='soldier_ant'
    for o in bpy.data.collections[key].objects:o.hide_render=key!='soldier_ant'
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'CreatureBatch22.blend'))
print('CREATURE_BATCH22_ELYTRA_REFINED')
