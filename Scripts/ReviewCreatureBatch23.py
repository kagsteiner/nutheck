"""Front/profile/underside views of the saved static flight forms."""
import bpy,sys,math
from pathlib import Path
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from CreatureBatch23Config import *
bpy.ops.wm.open_mainfile(filepath=str(OUT/BLEND_NAME))
for c in bpy.data.collections:c.hide_viewport=False
bpy.context.view_layer.update();scene=bpy.context.scene;cam=scene.camera
scene.render.resolution_x=600;scene.render.resolution_y=600;scene.cycles.samples=16
for key in GROUPS:
    for o in bpy.data.objects:
        if o.type=='MESH':o.hide_render=o.get('creature')!=key
    for label,yaw,elev in [('front',180,5),('profile',-90,0),('underside',-125,-35)]:
        target=Vector((-.29,0,.48)) if label!='underside' else Vector((0,0,.43))
        a=math.radians(yaw);e=math.radians(elev);cam.location=target+Vector((math.cos(a)*math.cos(e),math.sin(a)*math.cos(e),math.sin(e)))*3
        cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=.66 if label!='underside' else 1.3;cam.data.shift_x=0;cam.data.shift_y=0
        scene.render.filepath=str(OUT/(key+'-head-'+label+'.png'));bpy.ops.render.render(write_still=True)
print('CREATURE_BATCH23_DETAIL_REVIEW_READY')
