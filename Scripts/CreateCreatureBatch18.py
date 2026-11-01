"""Hobgoblin, hill orc and Mordor orc: saved ancestry plus new upright family."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from CreatureGeometry import *
from OrcFamily import hobgoblin,upright_orc,orc_pigment
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for key,color in {'hob_yellow':(.82,.73,.006),'orc_skin':(.71,.30,.12),'orc_cloth':(.018,.48,.004),'hill_lime':(.26,.86,.006),
                  'orc_boot':(.35,.085,.008),'orc_belt':(.37,.22,.015),'orc_metal':(.60,.68,.71),'orc_rod':(.28,.095,.012),
                  'mordor_skin':(.22,.35,.43),'mordor_cloth':(.70,.005,.42),'mordor_boot':(.19,.30,.38),'mordor_red':(.75,.006,.008),
                  'mordor_cyan':(.008,.50,.72)}.items():
    COLORS[key]=color;mat=bpy.data.materials.new(key);mat.use_nodes=True;mat.diffuse_color=(*color,1)
    mat.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.82;MATS[key]=mat
hobgoblin();upright_orc()
GROUPS=['hobgoblin','hill_orc','mordor_orc'];BLEND_NAME='CreatureBatch18.blend';REPORT_NAME='projection-report-batch18.json'
SOURCE_TILE_NAMES={'mordor_orc':'Mordor orc,male'};PIGMENT_FUNCTION=orc_pigment;SPATIAL_MASK_KEYS=GROUPS
exec(compile(Path(__file__).with_name('CreatureBatch2Pipeline.py').read_text(encoding='utf-8'),'CreatureBatch2Pipeline.py','exec'))
