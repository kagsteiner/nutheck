"""Pony, horse and warhorse: complete independently proportioned equine family."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from CreatureGeometry import *
from EquineFamily import equine
from CreatureFur import apply_fur
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for key,color in {
    'pony_chestnut':(.48,.145,.022),'horse_chestnut':(.53,.155,.020),'warhorse_chestnut':(.57,.165,.021),
    'equine_mane':(.18,.065,.012),'warhorse_mane':(.21,.072,.011),'equine_horn':(.76,.51,.33),
    'equine_dark':(.027,.019,.012),'equine_inner':(.27,.105,.062),'equine_blue':(.015,.065,.56),
}.items():
    COLORS[key]=color;mat=bpy.data.materials.new(key);mat.use_nodes=True;mat.diffuse_color=(*color,1)
    mat.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.82;MATS[key]=mat
equine('pony',.286,.119,.145,.340,.282,.132,.167,.128,.032,'pony_chestnut','equine_mane')
equine('horse',.356,.127,.164,.477,.350,.137,.218,.143,.036,'horse_chestnut','equine_mane')
equine('warhorse',.389,.163,.190,.505,.378,.159,.240,.147,.043,'warhorse_chestnut','warhorse_mane')
GROUPS=['pony','horse','warhorse'];BLEND_NAME='CreatureBatch11.blend';REPORT_NAME='projection-report-batch11.json'
POST_PAINT=lambda:apply_fur([o for o in bpy.context.scene.objects if o.type=='MESH'])
exec(compile(Path(__file__).with_name('CreatureBatch2Pipeline.py').read_text(encoding='utf-8'),'CreatureBatch2Pipeline.py','exec'))
