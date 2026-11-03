"""Painted garter snake, snake and water moccasin static drafts."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from CreatureGeometry import *
from CreatureBatch26Config import *
from SnakeFamily import snake,pigment
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for key,color in {'snake_orange':(.58,.15,.006),'snake_rust':(.48,.115,.006),'snake_brown':(.23,.068,.003),'snake_ochre':(.65,.33,.060),'snake_black':(.012,.016,.015),'snake_charcoal':(.038,.046,.041),'snake_eye':(.74,.76,.69),'snake_pupil':(.003,.004,.003),'snake_red':(.85,.004,.002),'snake_green':(.012,.57,.005)}.items():
    COLORS[key]=color;mat=bpy.data.materials.new(key);mat.use_nodes=True;mat.diffuse_color=(*color,1)
    mat.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.82;MATS[key]=mat
for key in GROUPS:snake(key)
PIGMENT_FUNCTION=pigment
exec(compile(Path(__file__).with_name('CreatureBatch2Pipeline.py').read_text(encoding='utf-8'),'CreatureBatch26Pipeline','exec'))
