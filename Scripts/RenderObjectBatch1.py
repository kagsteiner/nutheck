"""Refresh saved object renders without regenerating meshes."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from CreatureGeometry import *
OUT=ROOT/'Art/ObjectInterpretations'
bpy.ops.wm.open_mainfile(filepath=str(OUT/'ObjectBatch1.blend'))
for collection in bpy.data.collections:collection.hide_viewport=False
for obj in list(bpy.data.objects):
    obj.hide_viewport=False
    if obj.type in {'LIGHT','CAMERA'}:bpy.data.objects.remove(obj,do_unlink=True)
bpy.context.view_layer.update()
GROUPS=['large_box','chest','gold_piece'];INITIAL_GROUP='large_box'
BLEND_NAME='ObjectBatch1.blend';REPORT_NAME='projection-report-object1.json'
objects={key:[o for o in bpy.data.objects if o.type=='MESH' and o.get('creature')==key] for key in GROUPS}
SOURCE_TILE_NAMES={key:key.replace('_',' ') for key in GROUPS}
SPATIAL_MASK_KEYS=GROUPS
pipeline=Path(__file__).with_name('CreatureBatch2Pipeline.py').read_text(encoding='utf-8').replace('win/share/monsters.txt','win/share/objects.txt')
render=pipeline[pipeline.index('# Studio renders'):pipeline.index('for parts in objects.values():')]
exec(compile(render,'saved_object1_renders','exec'))
for key,parts in objects.items():
    for obj in parts:obj.hide_render=key!=INITIAL_GROUP
    bpy.data.collections[key].hide_viewport=key!=INITIAL_GROUP
scene.render.resolution_x=800;scene.render.resolution_y=800
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/BLEND_NAME))
(OUT/REPORT_NAME).write_text(json.dumps(report,indent=2))
print('OBJECT_BATCH1_RENDER_READY count=3',flush=True)
