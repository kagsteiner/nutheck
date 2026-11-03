import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from CreatureGeometry import *
from CreatureBatch27Config import *
from AdvancedSnakeFamily import build,pigment
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for key,c in {'python_brown':(.36,.12,.005),'python_orange':(.61,.19,.006),'python_eye':(.18,.80,.004),'viper_black':(.010,.015,.012),'cobra_black':(.009,.013,.012),'pale_eye':(.72,.75,.69),'cobra_eye':(.18,.30,.40),'snake_dark':(.002,.003,.002),'snake_red':(.82,.005,.002)}.items():
    COLORS[key]=c;m=bpy.data.materials.new(key);m.use_nodes=True;m.diffuse_color=(*c,1);m.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.82;MATS[key]=m
for key in GROUPS:build(key)
PIGMENT_FUNCTION=pigment
exec(compile(Path(__file__).with_name('CreatureBatch2Pipeline.py').read_text(),'CreatureBatch27Pipeline','exec'))
