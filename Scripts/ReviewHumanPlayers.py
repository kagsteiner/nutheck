"""Actual saved human player face views, without rebuilding geometry."""
import bpy,math
from pathlib import Path
from mathutils import Vector
out=Path(__file__).resolve().parents[1]/'Art/CreatureInterpretations'
bpy.ops.wm.open_mainfile(filepath=str(out/'HumanPlayers.blend'))
for c in bpy.data.collections:c.hide_viewport=False
bpy.context.view_layer.update();scene=bpy.context.scene;camera=scene.camera
scene.render.resolution_x=600;scene.render.resolution_y=600;scene.cycles.samples=24
for key in ['valkyrie_female_human','barbarian_male_human']:
    for o in bpy.data.objects:
        if o.type=='MESH':o.hide_render=o.get('creature')!=key
    body=next(o for o in bpy.data.objects if o.get('creature')==key and o.get('human_player'))
    target=Vector((0,-.010,body['head_z']))
    for label,yaw in [('front',-90),('profile',0)]:
        a=math.radians(yaw);camera.location=target+Vector((math.cos(a),math.sin(a),0))*3
        camera.rotation_euler=(target-camera.location).to_track_quat('-Z','Y').to_euler();camera.data.ortho_scale=.42;camera.data.shift_x=0;camera.data.shift_y=0
        scene.render.filepath=str(out/(key+'-head-'+label+'.png'));bpy.ops.render.render(write_still=True)
print('HUMAN_PLAYERS_HEAD_REVIEW_READY',flush=True)
