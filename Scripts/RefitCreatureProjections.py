"""Blender: repeat the reverse-projection check without rebuilding sculptures."""
import bpy
import json
import math
import re
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'Art/CreatureInterpretations'
bpy.ops.wm.open_mainfile(filepath=str(OUT/'CreatureInterpretations.blend'))
scene=bpy.context.scene; camera=scene.camera; scene.cycles.samples=8
scene.render.resolution_x=16; scene.render.resolution_y=16
text=(ROOT/'upstream/NetHack/win/share/monsters.txt').read_text()
tiles={name:[r.strip() for r in rows.strip().splitlines()] for number,name,rows in re.findall(r'^# tile (\d+) \(([^\n]+)\)\s*\{([^}]+)\}',text,re.M)}
objects={key:[o for o in scene.objects if o.get('creature')==key] for key in ['giant_ant','little_dog','goblin']}
report=[]
for key,parts in objects.items():
    for other,models in objects.items():
        for obj in models: obj.hide_render=other!=key
    bpy.context.view_layer.update()
    points=[o.matrix_world@Vector(corner) for o in parts for corner in o.bound_box]
    low=Vector(tuple(min(p[i] for p in points) for i in range(3))); high=Vector(tuple(max(p[i] for p in points) for i in range(3)))
    center=(low+high)*.5
    target={(x,15-y) for y,row in enumerate(tiles[key.replace('_',' ')+',male']) for x,ch in enumerate(row) if ch not in ['.','A']}
    tx0=min(x for x,y in target); tx1=max(x for x,y in target); ty0=min(y for x,y in target); ty1=max(y for x,y in target)
    candidates=[]
    for yaw in [-115,-90,-65]:
        for elevation in [25,45]:
            a=math.radians(yaw); e=math.radians(elevation)
            camera.location=center+Vector((math.cos(a)*math.cos(e),math.sin(a)*math.cos(e),math.sin(e)))*5
            camera.rotation_euler=(center-camera.location).to_track_quat('-Z','Y').to_euler()
            inverse=camera.rotation_euler.to_matrix().transposed(); projected=[inverse@(p-center) for p in points]
            xmin=min(p.x for p in projected); xmax=max(p.x for p in projected); ymin=min(p.y for p in projected); ymax=max(p.y for p in projected)
            scale=max((xmax-xmin)*16/(tx1-tx0+2),(ymax-ymin)*16/(ty1-ty0+2))
            camera.data.ortho_scale=scale
            camera.data.shift_x=(xmin+xmax)*.5/scale-((tx0+tx1+1)/32-.5)
            camera.data.shift_y=(ymin+ymax)*.5/scale-((ty0+ty1+1)/32-.5)
            path=OUT/(key+f'-pixel-{yaw}-{elevation}.png'); scene.render.filepath=str(path)
            bpy.ops.render.render(write_still=True)
            image=bpy.data.images.load(str(path),check_existing=False); rgba=list(image.pixels)
            silhouette={(i%16,i//16) for i in range(256) if rgba[i*4+3]>.5}
            iou=len(silhouette&target)/max(1,len(silhouette|target)); bpy.data.images.remove(image)
            candidates.append(dict(yaw=yaw,elevation=elevation,silhouette_iou=round(iou,4),file=path.name))
    report.append(dict(key=key,bounds_m=[list(low),list(high)],best_projection=max(candidates,key=lambda c:c['silhouette_iou']),candidates=candidates))
for parts in objects.values():
    for obj in parts: obj.hide_render=False
(OUT/'projection-report.json').write_text(json.dumps(report,indent=2))
print('CREATURE_PROJECTIONS_REFIT_READY',flush=True)
