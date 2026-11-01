"""Dog, large dog and dingo: independent canid dimensions, paint and coat maps."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from CreatureGeometry import *
from CanidFamily import canid
from CreatureFur import apply_fur

bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for key,color in {
    'dog_ginger':(.58,.19,.035),'dog_cream':(.77,.63,.37),
    'dingo_ginger':(.88,.245,.012),'dingo_pale':(.91,.52,.29),
    'canid_inner':(.38,.17,.105),'canid_amber':(.22,.095,.018),
}.items():
    COLORS[key]=color
    mat=bpy.data.materials.new(key);mat.use_nodes=True;mat.diffuse_color=(*color,1)
    mat.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.82
    MATS[key]=mat

canid('dog',.305,.130,.155,.285,.139,.112,.190,.060)
canid('large_dog',.355,.150,.182,.335,.152,.128,.205,.069)
canid('dingo',.325,.108,.139,.320,.122,.135,.190,.051,domestic=False)
GROUPS=['dog','large_dog','dingo']
BLEND_NAME='CreatureBatch6.blend';REPORT_NAME='projection-report-batch6.json'
POST_PAINT=lambda:apply_fur([o for o in bpy.context.scene.objects if o.type=='MESH'])
exec(compile(Path(__file__).with_name('CreatureBatch2Pipeline.py').read_text(encoding='utf-8'),'CreatureBatch2Pipeline.py','exec'))
