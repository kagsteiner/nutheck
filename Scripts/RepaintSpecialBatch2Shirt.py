"""Saved paint-only undergarment coverage at neck/shoulder; geometry unchanged."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from CreatureGeometry import *
from SpecialBatch2Config import *
from ShopkeeperAltarGeometry import pigment
bpy.ops.wm.open_mainfile(filepath=str(OUT/BLEND_NAME))
for c in bpy.data.collections:c.hide_viewport=False
for o in bpy.data.objects:
    if o.type!='MESH':continue
    if o.name in ['shopkeeper_human_anatomy','shopkeeper_jacket']:
        if 'preserve_paint' in o:del o['preserve_paint']
        o.data.color_attributes.remove(o.data.color_attributes['Paint'])
    else:o['preserve_paint']=True
for m in bpy.data.materials:
    if m.use_nodes:COLORS[m.name]=tuple(m.diffuse_color[:3])
COLORS.update(shop_blue=(.012,.025,.65),shop_cyan=(.012,.46,.69),shop_green=(.018,.40,.006),shop_brown=(.27,.10,.014))
PIGMENT_FUNCTION=pigment
pipeline=Path(__file__).with_name('CreatureBatch2Pipeline.py').read_text()
GROUPS=['shopkeeper']
exec(compile(pipeline[:pipeline.index('# Studio renders')],'shirt_paint_export','exec'))
for key in ALL_GROUPS if 'ALL_GROUPS' in globals() else ['shopkeeper']+['altar_'+k for k in ALTARS]:
    bpy.data.collections[key].hide_viewport=key!=INITIAL_GROUP
    for o in bpy.data.collections[key].objects:o.hide_render=key!=INITIAL_GROUP
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/BLEND_NAME))
print('SPECIAL_BATCH2_SHIRT_PAINT_READY')
