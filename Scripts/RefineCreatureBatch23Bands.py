"""Saved paint review: denser colour sampling and full dark abdomen bands only."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from CreatureGeometry import *
from CreatureBatch23Config import *
from WingedInsects import pigment
bpy.ops.wm.open_mainfile(filepath=str(OUT/BLEND_NAME))
for c in bpy.data.collections:c.hide_viewport=False
for o in bpy.data.objects:
    if o.type!='MESH':continue
    if o.get('striped_abdomen'):
        o.data.color_attributes.remove(o.data.color_attributes['Paint'])
        if 'preserve_paint' in o:del o['preserve_paint']
        sub=o.modifiers.new('Band pigment sampling','SUBSURF');sub.subdivision_type='SIMPLE';sub.levels=2
    else:o['preserve_paint']=True
COLORS.update(bee_gold=(.92,.70,.005),bee_dark=(.018,.012,.005))
PIGMENT_FUNCTION=pigment
pipeline=Path(__file__).with_name('CreatureBatch2Pipeline.py').read_text()
exec(compile(pipeline[:pipeline.index('# Studio renders')],'saved_band_paint_export','exec'))
for key in GROUPS:
    bpy.data.collections[key].hide_viewport=key!=INITIAL_GROUP
    for o in bpy.data.collections[key].objects:o.hide_render=key!=INITIAL_GROUP
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/BLEND_NAME))
print('CREATURE_BATCH23_BANDS_REFINED')
