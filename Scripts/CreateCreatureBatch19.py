"""Requested early-level floating eye, newt and lichen; separate complete forms."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from CreatureGeometry import *
from EarlyDungeonCreatures import floating_eye,newt,lichen,early_pigment
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for key,color in {'eye_white':(.88,.89,.86),'iris_cyan':(.005,.51,.83),'iris_blue':(.008,.025,.78),'eye_pupil':(.003,.004,.009),
                  'newt_orange':(.86,.18,.008),'newt_peach':(.90,.48,.28),'newt_eye':(.045,.017,.005),
                  'lichen_green':(.010,.40,.004),'lichen_orange':(.95,.24,.008),'lichen_pale':(.75,.77,.66)}.items():
    COLORS[key]=color;mat=bpy.data.materials.new(key);mat.use_nodes=True;mat.diffuse_color=(*color,1)
    mat.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.82;MATS[key]=mat
floating_eye();newt();lichen()
GROUPS=['floating_eye','newt','lichen'];BLEND_NAME='CreatureBatch19.blend';REPORT_NAME='projection-report-batch19.json'
PIGMENT_FUNCTION=early_pigment;SPATIAL_MASK_KEYS=GROUPS
exec(compile(Path(__file__).with_name('CreatureBatch2Pipeline.py').read_text(encoding='utf-8'),'CreatureBatch2Pipeline.py','exec'))
