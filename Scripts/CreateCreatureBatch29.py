import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from CreatureGeometry import *
from CreatureBatch29Config import *
from Batch29Family import build,pigment
from CreatureFur import apply_fur
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for key,c in {'primate_coat':(.49,.135,.012),'primate_skin':(.86,.45,.24),'primate_blue':(.025,.055,.88),'primate_dark':(.019,.008,.004),'primate_red':(.88,.007,.002),'primate_ivory':(.84,.76,.52)}.items():
 COLORS[key]=c;m=bpy.data.materials.new(key);m.use_nodes=True;m.diffuse_color=(*c,1);m.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.82;MATS[key]=m
for key,c in {'yeti_white':(.88,.88,.82),'sasquatch_brown':(.49,.135,.012),'sasquatch_eye':(.20,.85,.006),'owl_coat':(.45,.12,.008),'owl_disc':(.68,.66,.59),'owl_eye':(.92,.55,.015),'owl_claw':(.22,.32,.40),'owl_beak':(.90,.41,.005)}.items():
 COLORS[key]=c;m=bpy.data.materials.new(key);m.use_nodes=True;m.diffuse_color=(*c,1);m.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.82;MATS[key]=m
for key in GROUPS:build(key)
PIGMENT_FUNCTION=pigment
def post():apply_fur(list(bpy.context.scene.objects))
POST_PAINT=post
exec(compile(Path(__file__).with_name('CreatureBatch2Pipeline.py').read_text(),'CreatureBatch29Pipeline','exec'))
