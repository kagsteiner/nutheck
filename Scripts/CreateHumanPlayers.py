"""Requested human female Valkyrie and human male Barbarian static player forms."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from CreatureGeometry import *
from HumanPlayerFamily import human_player,human_pigment,fixed_characters
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for key,color in {
    'human_skin':(.69,.37,.23),'human_dark':(.012,.009,.008),'human_sclera':(.77,.77,.66),
    'human_blue':(.015,.075,.66),'human_green':(.065,.51,.014),'human_lip':(.25,.072,.050),
    'human_gold':(.86,.59,.017),'human_brow':(.28,.135,.012),
    'player_leather':(.28,.085,.015),'player_trim':(.53,.18,.018),'player_boot':(.21,.065,.014),'player_belt':(.12,.037,.009),
}.items():
    COLORS[key]=color;mat=bpy.data.materials.new(key);mat.use_nodes=True;mat.diffuse_color=(*color,1)
    mat.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.82;MATS[key]=mat
human_player('valkyrie_female_human',True)
human_player('barbarian_male_human',False)
GROUPS=['valkyrie_female_human','barbarian_male_human'];BLEND_NAME='HumanPlayers.blend';REPORT_NAME='projection-report-human-players.json'
PIGMENT_FUNCTION=human_pigment
POST_PAINT=fixed_characters
SOURCE_TILE_NAMES={'valkyrie_female_human':'valkyrie,female','barbarian_male_human':'barbarian,male'}
exec(compile(Path(__file__).with_name('CreatureBatch2Pipeline.py').read_text(encoding='utf-8'),'CreatureBatch2Pipeline.py','exec'))
