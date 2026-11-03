"""Five physical forms for soldier ant, fire ant and giant beetle."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from CreatureGeometry import *
from AntBeetleFamily import ant,beetle,insect_pigment
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for key,color in {'fire_shell':(.65,.008,.004),'fire_light':(.95,.15,.003),'fire_joint':(.19,.014,.003),'fire_eye':(.12,.85,.003),
                  'beetle_red':(.76,.012,.003),'beetle_orange':(.71,.14,.014),'beetle_dark':(.16,.032,.008),'beetle_highlight':(.95,.48,.23)}.items():
    COLORS[key]=color;mat=bpy.data.materials.new(key);mat.use_nodes=True;mat.diffuse_color=(*color,1)
    mat.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.48;MATS[key]=mat
GROUPS=['soldier_ant','soldier_ant_female','fire_ant','fire_ant_female','giant_beetle']
for key in GROUPS:
    if key=='giant_beetle':beetle()
    else:ant(key,key.endswith('_female'))
SOURCE_TILE_NAMES={key:key.removesuffix('_female').replace('_',' ')+(',female' if key.endswith('_female') else ',male') for key in GROUPS}
SPATIAL_MASK_KEYS=GROUPS;PIGMENT_FUNCTION=insect_pigment
BLEND_NAME='CreatureBatch22.blend';REPORT_NAME='projection-report-batch22.json'
exec(compile(Path(__file__).with_name('CreatureBatch2Pipeline.py').read_text(encoding='utf-8'),'CreatureBatch2Pipeline.py','exec'))
