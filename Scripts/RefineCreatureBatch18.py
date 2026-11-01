"""One-time saved garment/degenerate-face repair; fresh generator has final values."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from CreatureGeometry import *
import CreatureGeometry as g
from OrcFamily import orc_pigment,remove_degenerate_faces
from DwarfFamily import shell
bpy.ops.wm.open_mainfile(filepath=str(OUT/'CreatureBatch18.blend'))
for c in bpy.data.collections:c.hide_viewport=False
for o in list(bpy.context.scene.objects):
    o.hide_viewport=False
    if o.type in {'LIGHT','CAMERA'}:bpy.data.objects.remove(o,do_unlink=True);continue
    if o.type!='MESH':continue
    o['preserve_paint']=True
    if o.get('creature')=='hobgoblin':
        remove_degenerate_faces(o)
        if not o.data.color_attributes.get('Paint'):del o['preserve_paint']
COLORS.update(orc_cloth=(.018,.48,.004),hill_lime=(.26,.86,.006),mordor_cloth=(.70,.005,.42))
MATS['orc_cloth']=bpy.data.materials['orc_cloth']
for key in ['hill_orc','mordor_orc']:
    for o in list(bpy.context.scene.objects):
        if o.get('creature')==key and (o.name.startswith(key+'_sleeve') or o.name==key+'_tunic'):bpy.data.objects.remove(o,do_unlink=True)
    g.GROUP=key
    for side in [-1,1]:
        sleeve=limb('sleeve',[(side*.160,0,.799),(side*.213,-.010,.698)],[.070,.057],'orc_cloth')
        shoulder=orb('cloth_shoulder',(side*.158,0,.802),(.074,.072,.080),'orc_cloth')
        sleeve=sculpt_union([sleeve,shoulder],'fitted_sleeve','orc_cloth',.0045);sleeve['costume_module']=True
    tunic=shell('tunic',[(.335,.153,.114,0,0),(.48,.163,.120,0,0),(.61,.176,.121,0,0),(.73,.172,.120,0,0),(.81,.177,.112,0,0),(.852,.082,.071,0,0)],'orc_cloth');tunic['costume_module']=True
GROUPS=['hobgoblin','hill_orc','mordor_orc'];BLEND_NAME='CreatureBatch18.blend';REPORT_NAME='projection-report-batch18.json'
SOURCE_TILE_NAMES={'mordor_orc':'Mordor orc,male'};PIGMENT_FUNCTION=orc_pigment;SPATIAL_MASK_KEYS=GROUPS
# Existing named collections are retained; the pipeline will repopulate them.
for key in GROUPS:
    col=bpy.data.collections.get(key)
    for o in list(col.objects):col.objects.unlink(o);bpy.context.scene.collection.objects.link(o)
    bpy.data.collections.remove(col)
exec(compile(Path(__file__).with_name('CreatureBatch2Pipeline.py').read_text(encoding='utf-8'),'CreatureBatch2Pipeline.py','exec'))
