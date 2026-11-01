"""Gnomish wizard, gnome mummy and gnome zombie; reuse saved gnome anatomy."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from CreatureGeometry import *
from GnomeStates import append_gnome,fitted_belt,gnome_linen,gnome_state_pigment
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for key,color in {'lime':(.13,.77,.012),'forest':(.008,.29,.008),'red':(.78,.012,.008),'peach':(.78,.40,.23),'beard':(.64,.67,.60),
                  'wizard_green':(.045,.48,.018),'mummy_linen':(.74,.71,.60),'gnome_dry_skin':(.51,.39,.28),'undead_red':(.65,.008,.012),
                  'gnome_rot_green':(.018,.28,.032),'gnome_rot_light':(.12,.54,.025),'gnome_ash_beard':(.20,.32,.30),'zombie_cloth':(.028,.37,.025)}.items():
    COLORS[key]=color;mat=bpy.data.materials.get(key) or bpy.data.materials.new(key);mat.use_nodes=True;mat.diffuse_color=(*color,1)
    mat.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.82;MATS[key]=mat
GROUPS=['gnomish_wizard','gnome_mummy','gnome_zombie','gnomish_wizard_female','gnome_zombie_female']
for key in GROUPS:
    col,body=append_gnome(key)
    if key=='gnome_mummy':gnome_linen(body,key)
    else:fitted_belt(key)
    for obj in list(col.objects):col.objects.unlink(obj);bpy.context.scene.collection.objects.link(obj)
    bpy.data.collections.remove(col)
SOURCE_TILE_NAMES={key:(key.removesuffix('_female').replace('_',' ')+',female') for key in GROUPS if key.endswith('_female')}
BLEND_NAME='CreatureBatch15.blend';REPORT_NAME='projection-report-batch15.json';PIGMENT_FUNCTION=gnome_state_pigment;SPATIAL_MASK_KEYS=GROUPS
exec(compile(Path(__file__).with_name('CreatureBatch2Pipeline.py').read_text(encoding='utf-8'),'CreatureBatch2Pipeline.py','exec'))
