"""Render saved globe/iris, newt head and lichen surface; never regenerate geometry."""
import bpy,math
from pathlib import Path
from mathutils import Vector
out=Path(__file__).resolve().parents[1]/'Art/CreatureInterpretations'
bpy.ops.wm.open_mainfile(filepath=str(out/'CreatureBatch19.blend'))
for c in bpy.data.collections:c.hide_viewport=False
bpy.context.view_layer.update();scene=bpy.context.scene;camera=scene.camera
scene.render.resolution_x=500;scene.render.resolution_y=500;scene.cycles.samples=16
for key in ['floating_eye','newt','lichen']:
    for o in bpy.data.objects:
        if o.type=='MESH':o.hide_render=o.get('creature')!=key
    s=1.0
    target=Vector((0,0,.64)) if key=='floating_eye' else Vector((-.22,0,.11)) if key=='newt' else Vector((0,0,.10))
    for label,yaw in ([('front',-180),('profile',-90)] if key=='newt' else [('front',-90),('profile',0)]):
        a=math.radians(yaw);camera.location=target+Vector((math.cos(a),math.sin(a),1.2 if key=='lichen' else 0))*3
        camera.rotation_euler=(target-camera.location).to_track_quat('-Z','Y').to_euler();camera.data.ortho_scale=.58 if key=='floating_eye' else .35 if key=='newt' else .65;camera.data.shift_x=0;camera.data.shift_y=0
        scene.render.filepath=str(out/(key+'-head-'+label+'.png'));bpy.ops.render.render(write_still=True)
print('CREATURE_BATCH19_HEAD_REVIEW_READY',flush=True)
