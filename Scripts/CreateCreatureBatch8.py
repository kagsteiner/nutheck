"""Bat, giant bat and vampire bat with closed, finger-supported wing membranes."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from CreatureGeometry import *
from BatFamily import bat
from CreatureFur import apply_fur
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for key,color in {
    'bat_coat':(.30,.12,.027),'bat_skin':(.17,.067,.022),'bat_rib':(.43,.17,.033),
    'giant_coat':(.43,.15,.025),'giant_skin':(.22,.075,.022),'giant_rib':(.58,.22,.035),
    'vampire_coat':(.025,.030,.036),'vampire_skin':(.014,.019,.025),'vampire_rib':(.06,.068,.077),
    'bat_eye':(.75,.58,.012),'vampire_eye':(.72,.009,.014),
    'claw':(.24,.19,.12),'tooth':(.76,.72,.59),
}.items():
    COLORS[key]=color
    mat=bpy.data.materials.new(key);mat.use_nodes=True;mat.diffuse_color=(*color,1)
    mat.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.82
    MATS[key]=mat

bat('bat',.125,.052,.060,.350,.235,.100,'bat_coat','bat_skin','bat_rib','bat_eye')
bat('giant_bat',.165,.065,.071,.470,.295,.118,'giant_coat','giant_skin','giant_rib','bat_eye')
bat('vampire_bat',.157,.071,.075,.445,.320,.101,'vampire_coat','vampire_skin','vampire_rib','vampire_eye',True)
GROUPS=['bat','giant_bat','vampire_bat'];BLEND_NAME='CreatureBatch8.blend';REPORT_NAME='projection-report-batch8.json'
POST_PAINT=lambda:apply_fur([o for o in bpy.context.scene.objects if o.type=='MESH'])
exec(compile(Path(__file__).with_name('CreatureBatch2Pipeline.py').read_text(encoding='utf-8'),'CreatureBatch2Pipeline.py','exec'))
