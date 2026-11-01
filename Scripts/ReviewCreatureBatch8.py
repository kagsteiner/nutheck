"""Saved bat front, underside and face detail; real closed membranes in every view."""
import bpy,math
from pathlib import Path
from mathutils import Vector
out=Path(__file__).resolve().parents[1]/'Art/CreatureInterpretations'
bpy.ops.wm.open_mainfile(filepath=str(out/'CreatureBatch8.blend'))
for col in bpy.data.collections:col.hide_viewport=False
bpy.context.view_layer.update()
scene=bpy.context.scene;camera=scene.camera;scene.cycles.samples=16
scene.render.resolution_x=500;scene.render.resolution_y=500
data=bpy.data.lights.new('Underside inspection fill','AREA');data.energy=140;data.size=3
fill=bpy.data.objects.new('Underside inspection fill',data);scene.collection.objects.link(fill)
fill.location=(-2,0,-3);fill.rotation_euler=(Vector((0,0,.3))-fill.location).to_track_quat('-Z','Y').to_euler()
for key in ['bat','giant_bat','vampire_bat']:
    for obj in bpy.data.objects:
        if obj.type=='MESH':obj.hide_render=obj.get('creature')!=key
    body=bpy.data.objects[key+'_continuous_anatomy']
    for label,yaw,elevation in [('front',180,20),('underside',180,-35),('face',180,0)]:
        if label=='face':
            target=Vector((body['head_x']-body['head_length']*.25,0,body['head_z']+.035));scale=body['head_length']*3.8
        else:target=Vector((.015,0,.31));scale=body['half_span']*2.28
        a=math.radians(yaw);e=math.radians(elevation)
        camera.location=target+Vector((math.cos(a)*math.cos(e),math.sin(a)*math.cos(e),math.sin(e)))*3
        camera.rotation_euler=(target-camera.location).to_track_quat('-Z','Y').to_euler()
        camera.data.ortho_scale=scale;camera.data.shift_x=0;camera.data.shift_y=0
        scene.render.filepath=str(out/(key+'-review-'+label+'.png'));bpy.ops.render.render(write_still=True)
print('CREATURE_BATCH8_WING_FACE_REVIEW_READY',flush=True)
