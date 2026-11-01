"""Refresh the saved fur-study renders after texture edits, without new geometry."""
import bpy
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'Art/FurStudy'
bpy.ops.wm.open_mainfile(filepath=str(OUT/'FurStudy.blend'))
for collection in bpy.data.collections:collection.hide_viewport=False
for obj in bpy.data.objects:obj.hide_viewport=False
bpy.context.view_layer.update()
for image in bpy.data.images:
    if image.source=='FILE':image.reload()
scene=bpy.context.scene;camera=scene.camera
groups={key:[o for o in scene.objects if o.get('study_key')==key] for key in
    ['little_dog_smooth','little_dog_painted','little_dog_tufted','housecat_smooth','housecat_painted','housecat_tufted']}
for key,parts in groups.items():
    for group,objects in groups.items():
        for obj in objects:obj.hide_render=group!=key
    camera.location=(-2.8,-3.7,2.25);target=Vector((0,0,.36))
    camera.rotation_euler=(target-camera.location).to_track_quat('-Z','Y').to_euler();camera.data.ortho_scale=1.15
    for view,pixels in [('close',700),('gameplay',64),('level',16)]:
        scene.render.resolution_x=pixels;scene.render.resolution_y=pixels
        scene.render.filepath=str(OUT/(key+'-'+view+'.png'));bpy.ops.render.render(write_still=True)
for key,parts in groups.items():
    for obj in parts:obj.hide_render=key!='little_dog_painted'
    bpy.data.collections[key].hide_viewport=key!='little_dog_painted'
scene.render.resolution_x=700;scene.render.resolution_y=700
for image in bpy.data.images:
    if image.source=='FILE':image.filepath=bpy.path.relpath(image.filepath)
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'FurStudy.blend'))
print('FUR_STUDY_RENDERS_READY',flush=True)
