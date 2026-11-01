"""Build only kobold, large kobold and kobold leader, then export/render."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from CreatureGeometry import *
from KoboldFamily import kobold
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for key,color in {'kobold_blue':(.008,.43,.78),'kobold_cool':(.11,.25,.38),'kobold_pale':(.86,.88,.82),'kobold_orange':(.95,.22,.012)}.items():
    COLORS[key]=color;mat=bpy.data.materials.new(key);mat.use_nodes=True;mat.diffuse_color=(*color,1)
    mat.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.82;MATS[key]=mat
kobold('kobold',.88,.105,.100,.175)
kobold('large_kobold',.99,.127,.108,.185)
kobold('kobold_leader',.99,.134,.112,.192,True)
GROUPS=['kobold','large_kobold','kobold_leader'];BLEND_NAME='CreatureBatch13.blend';REPORT_NAME='projection-report-batch13.json'
def kobold_pigment(obj,p,pigment,colors):
    if obj.get('ear_tip_height') and p.z>obj['ear_tip_height']:return colors['kobold_pale']
    return pigment
PIGMENT_FUNCTION=kobold_pigment
exec(compile(Path(__file__).with_name('CreatureBatch2Pipeline.py').read_text(encoding='utf-8'),'CreatureBatch2Pipeline.py','exec'))
