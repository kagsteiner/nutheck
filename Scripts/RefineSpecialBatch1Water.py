"""One-time saved thin-water bevel repair. Fresh generator has the correction."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from CreatureGeometry import *
import CreatureGeometry as g
from SpecialBatchConfig import *
from SpecialAssetGeometry import cylinder,special_pigment
bpy.ops.wm.open_mainfile(filepath=str(OUT/BLEND_NAME))
for c in bpy.data.collections:c.hide_viewport=False
for o in list(bpy.context.scene.objects):
    o.hide_viewport=False
    if o.type in {'LIGHT','CAMERA'}:bpy.data.objects.remove(o,do_unlink=True)
    elif o.type=='MESH':o['preserve_paint']=True
bpy.data.objects.remove(bpy.data.objects['fountain_still_basin_water'],do_unlink=True)
g.GROUP='fountain';COLORS['fountain_water']=(.008,.25,.67);MATS['fountain_water']=bpy.data.materials['fountain_water']
cylinder('still_basin_water',.366,.008,.297,'fountain_water')
for key in GROUPS:
    c=bpy.data.collections[key]
    for o in list(c.objects):c.objects.unlink(o);bpy.context.scene.collection.objects.link(o)
    bpy.data.collections.remove(c)
PIGMENT_FUNCTION=special_pigment
exec(compile(Path(__file__).with_name('CreatureBatch2Pipeline.py').read_text(encoding='utf-8'),'SavedSpecialWaterRepair','exec'))
