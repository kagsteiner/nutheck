"""Refine only saved wing membranes, preserving all other bat geometry and paint."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from CreatureGeometry import *
import CreatureGeometry as geo
from BatFamily import wing_surface
bpy.ops.wm.open_mainfile(filepath=str(OUT/'CreatureBatch8.blend'))
for col in bpy.data.collections:col.hide_viewport=False
for obj in list(bpy.data.objects):
    obj.hide_viewport=False
    if obj.type in {'LIGHT','CAMERA'} or (obj.get('wing_membrane') and not obj.get('tail_membrane')):
        bpy.data.objects.remove(obj,do_unlink=True)
    elif obj.type=='MESH':obj['preserve_paint']=True
for key in ['bat','giant_bat','vampire_bat']:
    col=bpy.data.collections.get(key)
    if col:
        for obj in list(col.objects):
            col.objects.unlink(obj);bpy.context.scene.collection.objects.link(obj)
        bpy.data.collections.remove(col)
bpy.context.view_layer.update()
for key,length,width,span,chord,skin,color in [
    ('bat',.125,.052,.350,.235,'bat_skin',(.17,.067,.022)),
    ('giant_bat',.165,.065,.470,.295,'giant_skin',(.22,.075,.022)),
    ('vampire_bat',.157,.071,.445,.320,'vampire_skin',(.014,.019,.025))]:
    geo.GROUP=key;z=.26+length*.30;COLORS[skin]=color;MATS[skin]=bpy.data.materials[skin]
    for side in [-1,1]:
        shoulder=(-length*.40,side*width*.75,z+.010);elbow=(length*.02,side*span*.28,z+.055)
        wrist=(-length*.58,side*span*.53,z+.080)
        tips=[(-chord*.34,side*span*.94,z+.055),(-chord*.01,side*span,z-.005),
              (chord*.56,side*span*.77,z-.038),(chord*.83,side*span*.43,z-.067)]
        obj=wing_surface(wrist,tips,(length*.83,side*width*.98,z-.108),
            (length*.21,side*width*.83,z-.025),shoulder,elbow,skin,.003 if key=='bat' else .004)
        obj['wing_side']=side
GROUPS=['bat','giant_bat','vampire_bat'];BLEND_NAME='CreatureBatch8.blend';REPORT_NAME='projection-report-batch8.json'
exec(compile(Path(__file__).with_name('CreatureBatch2Pipeline.py').read_text(encoding='utf-8'),'CreatureBatch2Pipeline.py','exec'))
