"""Gecko, iguana and lizard, painted static miniature interpretations."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from CreatureGeometry import *
from CreatureBatch25Config import *
from ReptileFamily import reptile,pigment
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for key,color in {'gecko_pale':(.68,.68,.64),'gecko_peach':(.93,.42,.20),'iguana_green':(.015,.40,.005),'iguana_lime':(.22,.88,.005),'lizard_green':(.008,.36,.003),'lizard_brown':(.30,.13,.004),'reptile_belly':(.36,.43,.24),'claw':(.21,.17,.095),'eye_red':(.80,.008,.003),'eye_gold':(.65,.48,.005),'reptile_dark':(.006,.008,.005)}.items():
    COLORS[key]=color;mat=bpy.data.materials.new(key);mat.use_nodes=True;mat.diffuse_color=(*color,1)
    mat.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.82;MATS[key]=mat
COLORS['tongue_red']=(.80,.008,.003);MATS['tongue_red']=MATS['eye_red']
for key in GROUPS:reptile(key)
PIGMENT_FUNCTION=pigment
exec(compile(Path(__file__).with_name('CreatureBatch2Pipeline.py').read_text(encoding='utf-8'),'CreatureBatch25Pipeline','exec'))
