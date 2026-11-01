"""First three official object interpretations; separate from creature inventory."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from CreatureGeometry import *
from ObjectFamily import container,coins,object_pigment
OUT=ROOT/'Art/ObjectInterpretations';OUT.mkdir(parents=True,exist_ok=True)
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for key,color in {'wood':(.40,.105,.018),'wood_edge':(.64,.21,.032),'wood_dark':(.075,.026,.008),'object_brass':(.69,.45,.045),'object_gold':(.80,.43,.040)}.items():
    COLORS[key]=color;mat=bpy.data.materials.new(key);mat.use_nodes=True;mat.diffuse_color=(*color,1)
    sh=mat.node_tree.nodes['Principled BSDF'];sh.inputs['Roughness'].default_value=.52 if key.startswith('object_') else .82
    sh.inputs['Metallic'].default_value=.55 if key.startswith('object_') else 0;MATS[key]=mat
container('large_box');container('chest',True);coins()
GROUPS=['large_box','chest','gold_piece'];BLEND_NAME='ObjectBatch1.blend';REPORT_NAME='projection-report-object1.json'
SOURCE_TILE_NAMES={key:key.replace('_',' ') for key in GROUPS};PIGMENT_FUNCTION=object_pigment
SPATIAL_MASK_KEYS=GROUPS
pipeline=Path(__file__).with_name('CreatureBatch2Pipeline.py').read_text(encoding='utf-8')
pipeline=pipeline.replace('win/share/monsters.txt','win/share/objects.txt')
exec(compile(pipeline,'ObjectBatchPipeline','exec'))
print('OBJECT_BATCH1_READY count=3',flush=True)
