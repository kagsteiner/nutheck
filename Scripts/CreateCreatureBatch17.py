"""Dwarf mummy/zombie, appending reviewed ancestry without regeneration."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from CreatureGeometry import *
from DwarfStates import append_dwarf,dwarf_linen,dwarf_state_pigment
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for key,color in {'dwarf_skin':(.78,.40,.23),'dwarf_skin_shade':(.38,.17,.09),'dwarf_beard':(.66,.70,.67),
                  'dwarf_blue':(.012,.023,.78),'dwarf_cyan':(.008,.54,.80),'mummy_linen':(.78,.77,.70),
                  'dry_skin':(.69,.40,.25),'undead_red':(.76,.006,.008),'linen_red':(.76,.006,.008),
                  'rot_green':(.006,.27,.008),'rot_light':(.012,.51,.008),'ash_beard':(.21,.34,.42)}.items():
    COLORS[key]=color;mat=bpy.data.materials.get(key) or bpy.data.materials.new(key);mat.use_nodes=True;mat.diffuse_color=(*color,1)
    mat.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.82;MATS[key]=mat
GROUPS=['dwarf_mummy','dwarf_zombie']
for key in GROUPS:
    col,body=append_dwarf(key)
    if key=='dwarf_mummy':dwarf_linen(body,key)
    for obj in list(col.objects):col.objects.unlink(obj);bpy.context.scene.collection.objects.link(obj)
    bpy.data.collections.remove(col)
BLEND_NAME='CreatureBatch17.blend';REPORT_NAME='projection-report-batch17.json';PIGMENT_FUNCTION=dwarf_state_pigment;SPATIAL_MASK_KEYS=GROUPS
exec(compile(Path(__file__).with_name('CreatureBatch2Pipeline.py').read_text(encoding='utf-8'),'CreatureBatch2Pipeline.py','exec'))
