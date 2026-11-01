"""Kobold shaman, mummy and zombie from saved reviewed ancestry geometry."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from CreatureGeometry import *
from KoboldStates import append_kobold,mummy_wraps,state_pigment
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for key,color in {'kobold_blue':(.008,.43,.78),'kobold_cool':(.11,.25,.38),'kobold_pale':(.86,.88,.82),'kobold_orange':(.95,.22,.012),
                  'shaman_yellow':(.82,.65,.015),'mummy_linen':(.74,.71,.60),'mummy_skin':(.46,.27,.16),
                  'zombie_blue':(.012,.31,.53),'zombie_green':(.025,.35,.035)}.items():
    COLORS[key]=color;mat=bpy.data.materials.get(key) or bpy.data.materials.new(key);mat.use_nodes=True
    mat.diffuse_color=(*color,1);mat.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.82;MATS[key]=mat
shaman,body=append_kobold('kobold_shaman','kobold_leader')
# Recolour the existing detachable garment; no new staff/crown or false inventory.
for o in shaman.objects:
    if o.get('rank_module'):o['caster_module']=True;o['rank_module']=False
mummy,body=append_kobold('kobold_mummy','large_kobold');mummy_wraps(body,'kobold_mummy')
zombie,body=append_kobold('kobold_zombie','large_kobold')
GROUPS=['kobold_shaman','kobold_mummy','kobold_zombie'];BLEND_NAME='CreatureBatch14.blend';REPORT_NAME='projection-report-batch14.json';PIGMENT_FUNCTION=state_pigment
# Appended collections already exist; move meshes to the scene until pipeline grouping.
for key in GROUPS:
    col=bpy.data.collections[key]
    for obj in list(col.objects):col.objects.unlink(obj);bpy.context.scene.collection.objects.link(obj)
    bpy.data.collections.remove(col)
exec(compile(Path(__file__).with_name('CreatureBatch2Pipeline.py').read_text(encoding='utf-8'),'CreatureBatch2Pipeline.py','exec'))
