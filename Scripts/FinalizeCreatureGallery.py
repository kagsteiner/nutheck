"""Blender: organise editable drafts into separately visible collections."""
import bpy
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]; path=ROOT/'Art/CreatureInterpretations/CreatureInterpretations.blend'
bpy.ops.wm.open_mainfile(filepath=str(path))
for key in ['giant_ant','little_dog','goblin']:
    collection=bpy.data.collections.get(key) or bpy.data.collections.new(key)
    if collection.name not in bpy.context.scene.collection.children: bpy.context.scene.collection.children.link(collection)
    for obj in list(bpy.context.scene.objects):
        if obj.get('creature')==key:
            for parent in list(obj.users_collection): parent.objects.unlink(obj)
            collection.objects.link(obj); obj.hide_render=key!='giant_ant'
    collection.hide_viewport=key!='giant_ant'
camera=bpy.context.scene.camera; camera.location=(1.4,-2.8,1.6)
camera.rotation_euler=(Vector((0,0,.25))-camera.location).to_track_quat('-Z','Y').to_euler()
camera.data.ortho_scale=1.55; camera.data.shift_x=0; camera.data.shift_y=0
bpy.context.scene.render.resolution_x=800; bpy.context.scene.render.resolution_y=800
bpy.ops.wm.save_as_mainfile(filepath=str(path))
print('CREATURE_COLLECTIONS_READY',flush=True)
