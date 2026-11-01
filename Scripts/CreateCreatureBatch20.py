"""Uruk-hai, orc shaman and orc-captain using the reviewed saved orc body."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from CreatureGeometry import *
from OrcRanks import append_orc,uruk_shield,captain_brim,rank_pigment
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for key,color in {'orc_skin':(.71,.30,.12),'orc_cloth':(.018,.48,.004),'orc_boot':(.35,.085,.008),'orc_belt':(.37,.22,.015),
                  'orc_metal':(.60,.68,.71),'orc_rod':(.28,.095,.012),'rank_skin':(.22,.35,.43),'rank_cheek':(.84,.46,.28),
                  'rank_metal':(.39,.55,.66),'rank_red':(.82,.006,.008),'rank_cyan':(.008,.51,.76),'rank_white':(.82,.85,.81),
                  'rank_lime':(.11,.72,.004),'rank_brown':(.28,.085,.008),'shaman_orange':(.94,.22,.005),'rank_magenta':(.73,.005,.45)}.items():
    COLORS[key]=color;mat=bpy.data.materials.get(key) or bpy.data.materials.new(key);mat.use_nodes=True;mat.diffuse_color=(*color,1)
    mat.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.82;MATS[key]=mat
GROUPS=['uruk_hai','orc_shaman','orc_captain']
for key in GROUPS:
    append_orc(key)
    if key=='uruk_hai':uruk_shield()
    if key=='orc_captain':captain_brim()
BLEND_NAME='CreatureBatch20.blend';REPORT_NAME='projection-report-batch20.json'
SOURCE_TILE_NAMES={'uruk_hai':'Uruk-hai,male','orc_captain':'orc-captain,male'};PIGMENT_FUNCTION=rank_pigment;SPATIAL_MASK_KEYS=GROUPS
exec(compile(Path(__file__).with_name('CreatureBatch2Pipeline.py').read_text(encoding='utf-8'),'CreatureBatch2Pipeline.py','exec'))
