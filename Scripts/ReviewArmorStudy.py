import bpy,math
from pathlib import Path
from mathutils import Vector
r=Path(__file__).resolve().parents[1];out=r/'Art/ObjectInterpretations'
bpy.ops.wm.open_mainfile(filepath=str(out/globals().get('ARMOR_BLEND','ArmorStudy.blend')))
for c in bpy.data.collections:c.hide_viewport=False
bpy.context.view_layer.update();scene=bpy.context.scene;cam=scene.camera
scene.render.resolution_x=600;scene.render.resolution_y=600;scene.cycles.samples=12
for key in globals().get('ARMOR_KEYS',['leather_armor','studded_leather_armor','chain_mail','banded_mail','elven_mithril_coat','dwarvish_mithril_coat']):
    for o in bpy.data.objects:
        if o.type=='MESH':o.hide_render=o.get('creature')!=key
    for label,yaw,elev in [('front',-90,5),('underside',-110,-45)]:
        target=Vector((0,0,.43));a=math.radians(yaw);e=math.radians(elev);cam.location=target+Vector((math.cos(a)*math.cos(e),math.sin(a)*math.cos(e),math.sin(e)))*3
        cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=1.0;cam.data.shift_x=cam.data.shift_y=0
        scene.render.filepath=str(out/(key+'-'+label+'.png'));bpy.ops.render.render(write_still=True)
print('ARMOR_STUDY_DETAIL_REVIEW_READY')

