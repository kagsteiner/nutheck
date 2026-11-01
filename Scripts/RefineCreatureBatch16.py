"""Replace only the saved ruler's crown points and seat its orange inlays."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from CreatureGeometry import *
import CreatureGeometry as g
from DwarfFamily import crown_details,dwarf_pigment
bpy.ops.wm.open_mainfile(filepath=str(OUT/'CreatureBatch16.blend'))
for col in bpy.data.collections:col.hide_viewport=False
for obj in list(bpy.data.objects):
    obj.hide_viewport=False
    if obj.type in {'LIGHT','CAMERA'}:bpy.data.objects.remove(obj,do_unlink=True)
    elif obj.type=='MESH' and obj.get('creature')=='dwarf_ruler' and ('crown_point' in obj.name or 'orange_inlay' in obj.name):bpy.data.objects.remove(obj,do_unlink=True)
for key in ['dwarf_gold','dwarf_orange']:
    MATS[key]=bpy.data.materials[key];COLORS[key]=tuple(MATS[key].diffuse_color[:3])
g.GROUP='dwarf_ruler';crown_details()
for obj in list(bpy.data.objects):
    if obj.type=='MESH' and obj.data.color_attributes.get('Paint'):obj['preserve_paint']=True
for col in list(bpy.data.collections):
    if col.name in ['dwarf','dwarf_leader','dwarf_ruler']:
        for obj in list(col.objects):col.objects.unlink(obj);bpy.context.scene.collection.objects.link(obj)
        bpy.data.collections.remove(col)
GROUPS=['dwarf','dwarf_leader','dwarf_ruler'];BLEND_NAME='CreatureBatch16.blend';REPORT_NAME='projection-report-batch16.json';SPATIAL_MASK_KEYS=GROUPS
PIGMENT_FUNCTION=dwarf_pigment
exec(compile(Path(__file__).with_name('CreatureBatch2Pipeline.py').read_text(),'CreatureBatch2Pipeline.py','exec'))
