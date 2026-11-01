"""Generate dwarf/leader/ruler with shared complete ancestry, then export/render."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from CreatureGeometry import *
from DwarfFamily import dwarf,variants,dwarf_pigment
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for key,color in {'dwarf_skin':(.78,.40,.23),'dwarf_skin_shade':(.38,.17,.09),'dwarf_beard':(.66,.70,.67),
                  'dwarf_blue':(.012,.023,.78),'dwarf_cyan':(.008,.54,.80),'dwarf_gold':(.94,.74,.008),'dwarf_orange':(.92,.22,.008)}.items():
    COLORS[key]=color;mat=bpy.data.materials.new(key);mat.use_nodes=True;mat.diffuse_color=(*color,1)
    shader=mat.node_tree.nodes['Principled BSDF'];shader.inputs['Roughness'].default_value=.55 if key=='dwarf_gold' else .82
    MATS[key]=mat
dwarf();variants()
GROUPS=['dwarf','dwarf_leader','dwarf_ruler'];BLEND_NAME='CreatureBatch16.blend';REPORT_NAME='projection-report-batch16.json'
PIGMENT_FUNCTION=dwarf_pigment;SPATIAL_MASK_KEYS=GROUPS
exec(compile(Path(__file__).with_name('CreatureBatch2Pipeline.py').read_text(encoding='utf-8'),'CreatureBatch2Pipeline.py','exec'))
