"""Refresh only revised jaguar imagery; preserve the approved other two records."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from CreatureGeometry import *
bpy.ops.wm.open_mainfile(filepath=str(OUT/'CreatureBatch9.blend'))
for col in bpy.data.collections:col.hide_viewport=False
for obj in list(bpy.data.objects):
    obj.hide_viewport=False
    if obj.type in {'LIGHT','CAMERA'}:bpy.data.objects.remove(obj,do_unlink=True)
bpy.context.view_layer.update()
old=json.loads((OUT/'projection-report-batch9.json').read_text())
GROUPS=['jaguar'];INITIAL_GROUP='jaguar'
objects={key:[o for o in bpy.data.objects if o.type=='MESH' and o.get('creature')==key] for key in ['jaguar','lynx','panther']}
pipeline=Path(__file__).with_name('CreatureBatch2Pipeline.py').read_text(encoding='utf-8')
exec(compile(pipeline[pipeline.index('# Studio renders'):pipeline.index('for parts in objects.values():')],
    'saved_jaguar_reference_render','exec'))
entry=report[0]
(OUT/'projection-report-batch9.json').write_text(json.dumps([entry]+[r for r in old if r['key']!='jaguar'],indent=2))
scene.cycles.samples=24;scene.render.resolution_x=1000;scene.render.resolution_y=800
# Additional broad flank/back inspection views show the wrap rather than a flat decal.
for label,yaw,elevation in [('side',-90,8),('back',-110,65)]:
    aim(yaw,elevation,1.06);scene.render.filepath=str(OUT/('jaguar-reference-'+label+'.png'));bpy.ops.render.render(write_still=True)
for key,parts in objects.items():
    for obj in parts:obj.hide_render=key!='jaguar'
    bpy.data.collections[key].hide_viewport=key!='jaguar'
scene.render.resolution_x=800;scene.render.resolution_y=800
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'CreatureBatch9.blend'))
print('JAGUAR_REFERENCE_RENDER_READY',flush=True)
