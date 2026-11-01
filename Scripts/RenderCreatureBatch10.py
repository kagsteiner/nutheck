"""Refresh saved batch10 renders and packed textures without regenerating meshes."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from CreatureGeometry import *
bpy.ops.wm.open_mainfile(filepath=str(OUT/'CreatureBatch10.blend'))
for collection in bpy.data.collections:collection.hide_viewport=False
for obj in list(bpy.data.objects):
    obj.hide_viewport=False
    if obj.type in {'LIGHT','CAMERA'}:bpy.data.objects.remove(obj,do_unlink=True)
for image in bpy.data.images:
    if image.name.startswith('FurBrush'):
        image.filepath=str(ROOT/'Art/FurStudy/Textures'/Path(image.filepath).name)
        image.reload();image.pack()
bpy.context.view_layer.update()
GROUPS=['tiger','hell_hound_pup','hell_hound'];INITIAL_GROUP='jaguar'
BLEND_NAME='CreatureBatch10.blend';REPORT_NAME='projection-report-batch10.json'
objects={key:[o for o in bpy.data.objects if o.type=='MESH' and o.get('creature')==key] for key in GROUPS}
pipeline=Path(__file__).with_name('CreatureBatch2Pipeline.py').read_text()
render=pipeline[pipeline.index('# Studio renders'):pipeline.index('for parts in objects.values():')]
exec(compile(render,'saved_batch10_renders','exec'))
for key,parts in objects.items():
    for obj in parts:obj.hide_render=key!=INITIAL_GROUP
    bpy.data.collections[key].hide_viewport=key!=INITIAL_GROUP
scene.render.resolution_x=800;scene.render.resolution_y=800
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/BLEND_NAME))
(OUT/REPORT_NAME).write_text(json.dumps(report,indent=2))
print('CREATURE_BATCH10_RENDER_READY count=3',flush=True)
