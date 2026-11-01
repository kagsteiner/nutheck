"""White, gray and black unicorns: compatible anatomy, distinct official palettes."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from CreatureGeometry import *
from UnicornFamily import unicorn,unicorn_pigment
from CreatureFur import apply_fur
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for key,color in {
    'unicorn_white':(.80,.82,.80),'unicorn_gray':(.25,.36,.46),'unicorn_black':(.024,.025,.025),
    'unicorn_blue_mane':(.018,.36,.52),'unicorn_white_mane':(.77,.82,.82),'unicorn_brown_mane':(.22,.075,.012),
    'unicorn_white_tail':(.72,.76,.75),'unicorn_gray_tail':(.25,.36,.46),'unicorn_black_tail':(.024,.025,.025),
    'equine_horn':(.76,.51,.33),'equine_dark':(.018,.015,.013),'equine_inner':(.26,.14,.12),
    'equine_blue':(.015,.065,.56),'unicorn_green':(.10,.65,.012),'unicorn_red':(.82,.006,.008),
    'unicorn_gold':(.76,.61,.19),'unicorn_groove':(.22,.29,.30),
}.items():
    COLORS[key]=color;mat=bpy.data.materials.new(key);mat.use_nodes=True;mat.diffuse_color=(*color,1)
    mat.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.82;MATS[key]=mat
unicorn('white_unicorn','unicorn_white','unicorn_blue_mane','equine_blue',7,'unicorn_white_tail')
unicorn('gray_unicorn','unicorn_gray','unicorn_white_mane','unicorn_green',0,'unicorn_gray_tail')
unicorn('black_unicorn','unicorn_black','unicorn_brown_mane','unicorn_red',-7,'unicorn_black_tail')
GROUPS=['white_unicorn','gray_unicorn','black_unicorn'];BLEND_NAME='CreatureBatch12.blend';REPORT_NAME='projection-report-batch12.json'
PIGMENT_FUNCTION=unicorn_pigment
POST_PAINT=lambda:apply_fur([o for o in bpy.context.scene.objects if o.type=='MESH'])
exec(compile(Path(__file__).with_name('CreatureBatch2Pipeline.py').read_text(encoding='utf-8'),'CreatureBatch2Pipeline.py','exec'))
