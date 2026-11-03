"""Orc mummy and zombie: exact saved anatomy, separate linen and undead paint."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from CreatureGeometry import *
from OrcUndead import append_orc_undead,orc_linen,zombie_pupils,orc_undead_pigment
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for key,color in {'orc_skin':(.71,.30,.12),'orc_cloth':(.018,.48,.004),'orc_boot':(.35,.085,.008),'orc_belt':(.37,.22,.015),
                  'orc_metal':(.60,.68,.71),'orc_linen':(.75,.75,.69),'dry_orc_skin':(.60,.60,.54),
                  'undead_red':(.78,.006,.008),'undead_orange':(.93,.21,.005),'undead_gray':(.25,.38,.47),'undead_metal':(.58,.65,.68),
                  'zombie_lime':(.11,.77,.005),'zombie_green':(.015,.34,.008),'zombie_cyan':(.008,.51,.76),'zombie_brown':(.33,.12,.012)}.items():
    COLORS[key]=color;mat=bpy.data.materials.get(key) or bpy.data.materials.new(key);mat.use_nodes=True;mat.diffuse_color=(*color,1)
    mat.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.82;MATS[key]=mat
GROUPS=['orc_mummy','orc_zombie']
for key in GROUPS:
    body=append_orc_undead(key)
    if key=='orc_mummy':orc_linen(body,key)
    else:zombie_pupils()
BLEND_NAME='CreatureBatch21.blend';REPORT_NAME='projection-report-batch21.json';PIGMENT_FUNCTION=orc_undead_pigment;SPATIAL_MASK_KEYS=GROUPS
exec(compile(Path(__file__).with_name('CreatureBatch2Pipeline.py').read_text(encoding='utf-8'),'CreatureBatch2Pipeline.py','exec'))
