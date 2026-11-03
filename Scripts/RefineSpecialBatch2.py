"""Saved review correction: full jacket/leg coverage and sampled stone-top pigments."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from CreatureGeometry import *
from SpecialBatch2Config import *
from ShopkeeperAltarGeometry import shopkeeper_outfit,pigment
bpy.ops.wm.open_mainfile(filepath=str(OUT/BLEND_NAME))
for c in bpy.data.collections:c.hide_viewport=False
for o in list(bpy.data.objects):
    if o.type!='MESH':continue
    if o.get('creature')=='shopkeeper' and any(o.name.startswith('shopkeeper_'+n) for n in ['jacket','sleeve_','cuff_','trouser','shoe_','collar','hat_']):
        bpy.data.objects.remove(o,do_unlink=True);continue
    if o.get('altar_top') and len(o.data.vertices)<500:
        sub=o.modifiers.new('Mineral paint sampling grid','SUBSURF');sub.subdivision_type='SIMPLE';sub.levels=4
        old=o.data.color_attributes.get('Paint')
        if old:o.data.color_attributes.remove(old)
        if 'preserve_paint' in o:del o['preserve_paint']
    else:o['preserve_paint']=True
for key in ['shop_cyan','shop_blue','shop_green','shop_dark','shop_brown']:
    MATS[key]=bpy.data.materials[key];COLORS[key]=tuple(MATS[key].diffuse_color[:3])
for kind in ALTARS:COLORS['altar_'+kind]=tuple(bpy.data.materials['altar_'+kind].diffuse_color[:3])
COLORS['altar_red']=(.62,.005,.006)
shopkeeper_outfit()
for o in list(bpy.data.objects):
    if o.type=='MESH' and o.get('creature')=='shopkeeper' and o not in bpy.data.collections['shopkeeper'].objects[:]:
        for c in list(o.users_collection):c.objects.unlink(o)
        bpy.data.collections['shopkeeper'].objects.link(o)
PIGMENT_FUNCTION=pigment
pipeline=Path(__file__).with_name('CreatureBatch2Pipeline.py').read_text()
exec(compile(pipeline[:pipeline.index('# Studio renders')],'repair_paint_export','exec'))
for key in GROUPS:
    bpy.data.collections[key].hide_viewport=key!=INITIAL_GROUP
    for o in bpy.data.collections[key].objects:o.hide_render=key!=INITIAL_GROUP
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/BLEND_NAME))
print('SPECIAL_BATCH2_SAVED_REFINEMENT_READY')
