"""Render existing special assets front/profile; never regenerate geometry."""
import bpy,math
from pathlib import Path
from mathutils import Vector
out=Path(__file__).resolve().parents[1]/'Art/SpecialBatch1'
bpy.ops.wm.open_mainfile(filepath=str(out/'SpecialBatch1.blend'))
for c in bpy.data.collections:c.hide_viewport=False
bpy.context.view_layer.update();scene=bpy.context.scene;camera=scene.camera
scene.render.resolution_x=500;scene.render.resolution_y=500;scene.cycles.samples=16
for key in ['grid_bug','corpse','fountain']:
    for o in bpy.data.objects:
        if o.type=='MESH':o.hide_render=o.get('creature')!=key
    s=1.0
    target=Vector((-.10,0,.14)) if key=='grid_bug' else Vector((0,0,.08)) if key=='corpse' else Vector((0,0,.57))
    for label,yaw in [('front',-90),('profile',0)]:
        a=math.radians(yaw);camera.location=target+Vector((math.cos(a),math.sin(a),0))*3
        camera.rotation_euler=(target-camera.location).to_track_quat('-Z','Y').to_euler();camera.data.ortho_scale=.55 if key!='fountain' else 1.10;camera.data.shift_x=0;camera.data.shift_y=0
        scene.render.filepath=str(out/(key+'-head-'+label+'.png'));bpy.ops.render.render(write_still=True)
print('SPECIAL_BATCH1_DETAIL_READY',flush=True)
