"""Requested shopkeeper and native displayed altar variants."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from CreatureGeometry import *
from SpecialBatch2Config import *
from ShopkeeperAltarGeometry import shopkeeper,altar,pigment
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
PALETTE={'human_skin':(.69,.37,.23),'human_dark':(.012,.009,.008),'human_sclera':(.77,.77,.66),'human_blue':(.015,.075,.66),'human_green':(.065,.51,.014),'human_lip':(.25,.072,.050),'human_gold':(.86,.59,.017),'human_brow':(.28,.135,.012),'player_leather':(.28,.085,.015),'player_belt':(.12,.037,.009),
         'shop_cyan':(.012,.46,.69),'shop_blue':(.012,.025,.65),'shop_green':(.018,.40,.006),'shop_dark':(.008,.009,.011),'shop_brown':(.27,.10,.014),
         'altar_unaligned':(.025,.026,.027),'altar_chaotic':(.12,.12,.13),'altar_neutral':(.23,.36,.49),'altar_lawful':(.79,.78,.72),'altar_other':(.56,.008,.36),'altar_red':(.62,.005,.006),'altar_white':(.89,.87,.79)}
for key,color in PALETTE.items():
    COLORS[key]=color;mat=bpy.data.materials.new(key);mat.use_nodes=True;mat.diffuse_color=(*color,1)
    mat.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.82;MATS[key]=mat
shopkeeper()
for kind in ALTARS:altar(kind)
PIGMENT_FUNCTION=pigment
exec(compile(Path(__file__).with_name('CreatureBatch2Pipeline.py').read_text(encoding='utf-8'),'SpecialBatch2Pipeline','exec'))
