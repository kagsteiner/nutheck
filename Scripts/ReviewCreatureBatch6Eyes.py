"""Frontal and profile checks of the actual saved canid heads."""
import bpy,math
from pathlib import Path
from mathutils import Vector
out=Path(__file__).resolve().parents[1]/'Art/CreatureInterpretations'
bpy.ops.wm.open_mainfile(filepath=str(out/'CreatureBatch6.blend'))
for col in bpy.data.collections:col.hide_viewport=False
bpy.context.view_layer.update()
scene=bpy.context.scene;camera=scene.camera;scene.cycles.samples=16
scene.render.resolution_x=500;scene.render.resolution_y=500
for key,length,leg,depth,head in [('dog',.305,.285,.155,.139),('large_dog',.355,.335,.182,.152),('dingo',.325,.320,.139,.122)]:
    for obj in bpy.data.objects:
        if obj.type=='MESH':obj.hide_render=obj.get('creature')!=key or bool(obj.get('tail_form'))
    target=Vector((-length*.6-.085-head*.37,0,leg+depth+depth*.91+.015))
    for label,yaw in [('front',180),('profile',-90)]:
        a=math.radians(yaw);camera.location=target+Vector((math.cos(a),math.sin(a),0))*3
        camera.rotation_euler=(target-camera.location).to_track_quat('-Z','Y').to_euler()
        camera.data.ortho_scale=head*3.15;camera.data.shift_x=0;camera.data.shift_y=0
        scene.render.filepath=str(out/(key+'-head-'+label+'.png'));bpy.ops.render.render(write_still=True)
print('CREATURE_BATCH6_EYE_REVIEW_READY',flush=True)
