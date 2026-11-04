"""Render extra front/underside views from the saved editable scene."""
import bpy,math
from pathlib import Path
from mathutils import Vector
root=Path(__file__).resolve().parents[1];out=root/'Art/Sokoban'
bpy.ops.wm.open_mainfile(filepath=str(out/'Sokoban.blend'))
for c in bpy.data.collections:c.hide_viewport=False
scene=bpy.context.scene;camera=scene.camera
scene.render.resolution_x=400;scene.render.resolution_y=400;scene.cycles.samples=16
for key in ['soko_wall','soko_floor','soko_boulder','soko_pit','soko_hole','soko_frame','soko_trim','soko_lamp']:
    parts=[]
    for o in scene.objects:
        if o.type=='MESH':
            o.hide_render=o.get('creature')!=key
            if not o.hide_render:parts.append(o)
    bpy.context.view_layer.update()
    pts=[o.matrix_world@v.co for o in parts for v in o.data.vertices]
    low=Vector(tuple(min(p[i] for p in pts) for i in range(3)));high=Vector(tuple(max(p[i] for p in pts) for i in range(3)));center=(low+high)*.5
    for view,yaw,elev in [('front',-90,15),('underside',-125,-35)]:
        a=math.radians(yaw);e=math.radians(elev)
        camera.location=center+Vector((math.cos(a)*math.cos(e),math.sin(a)*math.cos(e),math.sin(e)))*5
        camera.rotation_euler=(center-camera.location).to_track_quat('-Z','Y').to_euler()
        camera.data.ortho_scale=max((high-low).length*1.1,.35);camera.data.shift_x=camera.data.shift_y=0
        scene.render.filepath=str(out/(key+'-'+view+'.png'));bpy.ops.render.render(write_still=True)
print('SOKOBAN_DETAILS_READY',flush=True)
