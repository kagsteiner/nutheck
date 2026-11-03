"""Actual saved front/profile head and altar top detail views."""
import sys,bpy,math
from pathlib import Path
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from SpecialBatch2Config import *
bpy.ops.wm.open_mainfile(filepath=str(OUT/BLEND_NAME))
for c in bpy.data.collections:c.hide_viewport=False
bpy.context.view_layer.update();scene=bpy.context.scene;cam=scene.camera
scene.render.resolution_x=500;scene.render.resolution_y=500;scene.cycles.samples=16
for key in GROUPS:
    for o in bpy.data.objects:
        if o.type=='MESH':o.hide_render=o.get('creature')!=key
    target=Vector((0,0,1.54 if key=='shopkeeper' else .44))
    for label,yaw in [('front',-90),('profile',0)]:
        a=math.radians(yaw);cam.location=target+Vector((math.cos(a),math.sin(a),.10 if key=='shopkeeper' else .85))*3
        cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=.65 if key=='shopkeeper' else 1.05;cam.data.shift_x=0;cam.data.shift_y=0
        scene.render.filepath=str(OUT/(key+'-head-'+label+'.png'));bpy.ops.render.render(write_still=True)
print('SPECIAL_BATCH2_DETAIL_READY')
