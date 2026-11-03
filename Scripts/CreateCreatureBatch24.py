"""Shared spider family and independently constructed scorpion; static creatures."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from CreatureGeometry import *
from CreatureBatch24Config import *
from ArachnidFamily import spider,scorpion,pigment
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for key,color in {'spider_cool':(.24,.36,.49),'spider_blue':(.025,.44,.65),'spider_brown':(.28,.10,.018),'spider_warm':(.48,.17,.030),
                  'scorpion_shell':(.29,.105,.018),'scorpion_light':(.47,.18,.035),'spider_fang':(.65,.012,.008),
                  'arachnid_green':(.12,.67,.008),'arachnid_dark':(.009,.012,.010)}.items():
    COLORS[key]=color;mat=bpy.data.materials.new(key);mat.use_nodes=True;mat.diffuse_color=(*color,1)
    mat.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.82;MATS[key]=mat
spider('cave_spider');spider('giant_spider',True);scorpion();PIGMENT_FUNCTION=pigment
exec(compile(Path(__file__).with_name('CreatureBatch2Pipeline.py').read_text(encoding='utf-8'),'CreatureBatch24Pipeline','exec'))
