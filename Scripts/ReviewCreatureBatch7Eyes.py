"""Actual frontal/profile head views for eye and mouth-state review."""
import bpy,math
from pathlib import Path
from mathutils import Vector
out=Path(__file__).resolve().parents[1]/'Art/CreatureInterpretations'
bpy.ops.wm.open_mainfile(filepath=str(out/'CreatureBatch7.blend'))
for col in bpy.data.collections:col.hide_viewport=False
bpy.context.view_layer.update()
scene=bpy.context.scene;camera=scene.camera;scene.cycles.samples=16
scene.render.resolution_x=500;scene.render.resolution_y=500
for key,length,leg,depth,head in [('coyote',.265,.266,.114,.107),('warg',.345,.310,.182,.159),('rabid_rat',0,0,0,0)]:
    for obj in bpy.data.objects:
        if obj.type=='MESH':obj.hide_render=obj.get('creature')!=key or bool(obj.get('tail_form')) or 'bare_tail' in obj.name
    target=Vector((-.225,0,.105)) if key=='rabid_rat' else Vector((-length*.6-.085-head*.37,0,leg+depth+depth*.91+.015))
    for label,yaw in [('front',180),('profile',-90)]:
        a=math.radians(yaw);camera.location=target+Vector((math.cos(a),math.sin(a),0))*3
        camera.rotation_euler=(target-camera.location).to_track_quat('-Z','Y').to_euler()
        camera.data.ortho_scale=.34 if key=='rabid_rat' else head*3.15
        camera.data.shift_x=0;camera.data.shift_y=0
        scene.render.filepath=str(out/(key+'-head-'+label+'.png'));bpy.ops.render.render(write_still=True)
print('CREATURE_BATCH7_EYE_REVIEW_READY',flush=True)
