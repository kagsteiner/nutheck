"""Refresh saved batch28 renders and packed textures without regenerating meshes."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from CreatureGeometry import *
bpy.ops.wm.open_mainfile(filepath=str(OUT/'CreatureBatch28.blend'))
for collection in bpy.data.collections:collection.hide_viewport=False
for obj in list(bpy.data.objects):
    obj.hide_viewport=False
    if obj.type in {'LIGHT','CAMERA'}:bpy.data.objects.remove(obj,do_unlink=True)
for image in bpy.data.images:
    if image.name.startswith('FurBrush'):
        image.filepath=str(ROOT/'Art/FurStudy/Textures'/Path(image.filepath).name)
        image.reload();image.pack()
bpy.context.view_layer.update()
from CreatureBatch28Config import *
objects={key:[o for o in bpy.data.objects if o.type=='MESH' and o.get('creature')==key] for key in GROUPS}
ALL_GROUPS=list(GROUPS)
previous_report=json.loads((OUT/REPORT_NAME).read_text())
if '--' in sys.argv:
    GROUPS=sys.argv[sys.argv.index('--')+1:]
    assert GROUPS and set(GROUPS)<=set(ALL_GROUPS)
pipeline=Path(__file__).with_name('CreatureBatch2Pipeline.py').read_text()
render=pipeline[pipeline.index('# Studio renders'):pipeline.index('for parts in objects.values():')]
exec(compile(render,'saved_batch28_renders','exec'))
for key,parts in objects.items():
    for obj in parts:obj.hide_render=key!=INITIAL_GROUP
    bpy.data.collections[key].hide_viewport=key!=INITIAL_GROUP
scene.render.resolution_x=800;scene.render.resolution_y=800
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/BLEND_NAME))
(OUT/REPORT_NAME).write_text(json.dumps([next((r for r in report if r['key']==key),next(r for r in previous_report if r['key']==key)) for key in ALL_GROUPS],indent=2))
print('CREATURE_BATCH28_RENDER_READY count='+str(len(GROUPS)),flush=True)


