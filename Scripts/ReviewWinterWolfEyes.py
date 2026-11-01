"""Matched front, quarter and profile close views of saved winter-wolf heads."""
import bpy,math
from pathlib import Path
from mathutils import Vector
out=Path(__file__).resolve().parents[1]/'Art/CreatureInterpretations'
bpy.ops.wm.open_mainfile(filepath=str(out/'CreatureBatch5.blend'))
for col in bpy.data.collections:col.hide_viewport=False
bpy.context.view_layer.update()
scene=bpy.context.scene;camera=scene.camera;scene.cycles.samples=24
scene.render.resolution_x=600;scene.render.resolution_y=600
for key,hx,hz,head in [('winter_wolf_cub',-.213,.39944,.112),('winter_wolf',-.294,.66164,.137)]:
    # Cub skull centre is leg + depth + .87*depth = .39944.
    for obj in bpy.data.objects:
        if obj.type=='MESH':obj.hide_render=obj.get('creature')!=key
    target=Vector((hx-head*.37,0,hz+.025))
    for label,yaw,elevation in [('front',180,0),('quarter',-140,10),('profile',-90,0)]:
        a=math.radians(yaw);e=math.radians(elevation)
        camera.location=target+Vector((math.cos(a)*math.cos(e),math.sin(a)*math.cos(e),math.sin(e)))*3
        camera.rotation_euler=(target-camera.location).to_track_quat('-Z','Y').to_euler()
        camera.data.ortho_scale=head*3.15;camera.data.shift_x=0;camera.data.shift_y=0
        scene.render.filepath=str(out/(key+'-head-'+label+'.png'));bpy.ops.render.render(write_still=True)
print('WINTER_WOLF_EYE_REVIEW_READY',flush=True)
