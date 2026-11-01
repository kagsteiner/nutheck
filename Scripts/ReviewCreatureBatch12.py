"""Frontal/profile saved equine head views for lateral eyes and fitted inner ears."""
import bpy,math
from pathlib import Path
from mathutils import Vector
out=Path(__file__).resolve().parents[1]/'Art/CreatureInterpretations'
bpy.ops.wm.open_mainfile(filepath=str(out/'CreatureBatch12.blend'))
for col in bpy.data.collections:col.hide_viewport=False
bpy.context.view_layer.update()
scene=bpy.context.scene;camera=scene.camera;scene.cycles.samples=16
scene.render.resolution_x=500;scene.render.resolution_y=500
for key in ['white_unicorn','gray_unicorn','black_unicorn']:
    for obj in bpy.data.objects:
        if obj.type=='MESH':obj.hide_render=obj.get('creature')!=key or bool(obj.get('tail_form'))
    body=bpy.data.objects[key+'_continuous_anatomy'];head=body['head_length']
    target=Vector((body['head_x']-body['muzzle_length']*.40,0,body['head_z']+.030))
    for label,yaw in [('front',180),('profile',-90)]:
        a=math.radians(yaw);camera.location=target+Vector((math.cos(a),math.sin(a),0))*3
        camera.rotation_euler=(target-camera.location).to_track_quat('-Z','Y').to_euler()
        camera.data.ortho_scale=head*4.9;camera.data.shift_x=0;camera.data.shift_y=0
        scene.render.filepath=str(out/(key+'-head-'+label+'.png'));bpy.ops.render.render(write_still=True)
print('CREATURE_BATCH12_HEAD_REVIEW_READY',flush=True)

# Leave the saved gallery in its intended opening state after isolated head views.
for key in ['white_unicorn','gray_unicorn','black_unicorn']:
    bpy.data.collections[key].hide_viewport=key!='white_unicorn'
    for obj in bpy.data.collections[key].objects:obj.hide_render=key!='white_unicorn'
scene.render.resolution_x=800;scene.render.resolution_y=800
bpy.ops.wm.save_as_mainfile(filepath=str(out/'CreatureBatch12.blend'))
