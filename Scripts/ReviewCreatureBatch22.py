"""Front/profile close renders from saved insects; never regenerate geometry."""
import bpy,math
from pathlib import Path
from mathutils import Vector
out=Path(__file__).resolve().parents[1]/'Art/CreatureInterpretations'
bpy.ops.wm.open_mainfile(filepath=str(out/'CreatureBatch22.blend'))
for c in bpy.data.collections:c.hide_viewport=False
bpy.context.view_layer.update();scene=bpy.context.scene;cam=scene.camera
scene.render.resolution_x=500;scene.render.resolution_y=500;scene.cycles.samples=16
for key in ['soldier_ant','soldier_ant_female','fire_ant','fire_ant_female','giant_beetle']:
    for o in bpy.data.objects:
        if o.type=='MESH':o.hide_render=o.get('creature')!=key
    target=Vector((-.40,0,.27))
    for label,yaw in [('front',180),('profile',-90)]:
        a=math.radians(yaw);cam.location=target+Vector((math.cos(a)*3,math.sin(a)*3,1))
        cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=.73;cam.data.shift_x=0;cam.data.shift_y=0
        scene.render.filepath=str(out/(key+'-head-'+label+'.png'));bpy.ops.render.render(write_still=True)
print('CREATURE_BATCH22_DETAIL_REVIEW_READY')
