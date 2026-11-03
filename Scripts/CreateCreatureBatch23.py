"""Killer bee, queen bee and separately reviewed xan; static painted flight forms."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from CreatureGeometry import *
from CreatureBatch23Config import *
from WingedInsects import bee,xan,pigment
from CreatureFur import apply_fur
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for key,color in {'bee_brown':(.32,.11,.015),'bee_gold':(.92,.70,.005),'bee_dark':(.018,.012,.005),'bee_eye':(.012,.40,.68),'bee_glint':(.18,.69,.86),
                  'bee_wing':(.28,.43,.58),'bee_wing_root':(.83,.51,.33),'bee_vein':(.10,.30,.45),
                  'xan_green':(.16,.75,.006),'xan_pale':(.60,.83,.35),'xan_white':(.88,.89,.80),'xan_gold':(.89,.73,.007),'xan_wing':(.68,.71,.12),'xan_vein':(.41,.46,.03)}.items():
    COLORS[key]=color;mat=bpy.data.materials.new(key);mat.use_nodes=True;mat.diffuse_color=(*color,1)
    mat.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.82;MATS[key]=mat
bee('killer_bee');bee('queen_bee',True);xan();PIGMENT_FUNCTION=pigment
POST_PAINT=lambda:apply_fur([o for o in bpy.context.scene.objects if o.type=='MESH'])
exec(compile(Path(__file__).with_name('CreatureBatch2Pipeline.py').read_text(encoding='utf-8'),'CreatureBatch23Pipeline','exec'))
