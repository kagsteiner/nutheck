"""Replace only dragon armor in the saved study; retain exact plate meshes/paint."""
import sys,ast
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from CreatureGeometry import *
import CreatureGeometry as g
from ArmorBatch2Config import GROUPS as ALL_GROUPS
from DragonMailFamily import build
OUT=ROOT/'Art/ObjectInterpretations';GROUPS=ALL_GROUPS[3:]
bpy.ops.wm.open_mainfile(filepath=str(OUT/'ArmorBatch2.blend'))
for c in bpy.data.collections:c.hide_viewport=False
for o in list(bpy.data.objects):
    if o.type=='MESH' and o.get('creature') in GROUPS:bpy.data.objects.remove(o,do_unlink=True)
    elif o.type=='MESH':o['preserve_paint']=True
    elif o.type in {'LIGHT','CAMERA'}:bpy.data.objects.remove(o,do_unlink=True)
for key in GROUPS:
    old=bpy.data.collections.get(key)
    if old:bpy.data.collections.remove(old)
# Rebind palette/material references after opening the saved file.
source=Path(__file__).with_name('CreateArmorBatch2.py').read_text()
tree=ast.parse(source);dragons=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='DRAGONS' for t in n.targets))
palettes=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='PALETTES' for t in n.targets))
palettes.update({'dragon_'+c:(rgb,.24 if c in ['gray','silver','gold'] else .32,.6 if c in ['gray','silver','gold'] else .14) for c,rgb in dragons.items()})
for k,(color,rough,metal) in palettes.items():COLORS[k]=color;MATS[k]=bpy.data.materials[k]
for key in GROUPS:build(key)
def paint(o,p,c,colors):
    if o['pigment'].startswith('dragon_'):
        f=.92+.07*math.sin(p.x*83+p.z*67)*math.sin(p.y*71-p.z*45);return tuple(v*f for v in c)
    return c
BLEND_NAME='ArmorBatch2.blend';REPORT_NAME='projection-report-dragon-revision.json';PIGMENT_FUNCTION=paint
SOURCE_TILE_NAMES={k:k.replace('_',' ') for k in GROUPS};SPATIAL_MASK_KEYS=GROUPS
pipeline=Path(__file__).with_name('CreatureBatch2Pipeline.py').read_text().replace('win/share/monsters.txt','win/share/objects.txt')
exec(compile(pipeline,'ReworkDragonMailPipeline','exec'))
# The shared study still contains all thirteen collections, with exact old plates.
prior=json.loads((OUT/'projection-report-armor-batch2.json').read_text());revised=json.loads((OUT/REPORT_NAME).read_text())
(OUT/'projection-report-armor-batch2.json').write_text(json.dumps([r for r in prior if r['key'] not in GROUPS]+revised,indent=2))
print('DRAGON_MAIL_REVISION_READY forms=10')
