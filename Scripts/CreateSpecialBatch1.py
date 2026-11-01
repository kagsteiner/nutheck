"""Requested grid bug, generic corpse and carved fountain; mixed source batch."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from CreatureGeometry import *
from SpecialBatchConfig import *
from SpecialAssetGeometry import grid_bug,corpse,fountain,special_pigment
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for key,color in {'bug_white':(.84,.87,.78),'bug_blue':(.012,.025,.74),'bug_red':(.80,.008,.014),'bug_yellow':(.88,.74,.006),'bug_orange':(.96,.25,.007),
                  'corpse_red':(.33,.025,.020),'corpse_orange':(.58,.15,.035),'corpse_bone':(.77,.75,.64),
                  'fountain_stone':(.58,.56,.48),'fountain_light':(.76,.73,.63),'fountain_water':(.008,.25,.67),'fountain_foam':(.23,.68,.78)}.items():
    COLORS[key]=color;mat=bpy.data.materials.new(key);mat.use_nodes=True;mat.diffuse_color=(*color,1)
    sh=mat.node_tree.nodes['Principled BSDF'];sh.inputs['Roughness'].default_value=.16 if key in ['fountain_water','fountain_foam'] else .82;MATS[key]=mat
grid_bug();corpse();fountain();PIGMENT_FUNCTION=special_pigment
exec(compile(Path(__file__).with_name('CreatureBatch2Pipeline.py').read_text(encoding='utf-8'),'MixedSpecialPipeline','exec'))
