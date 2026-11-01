"""Add only the two tile-supported beardless forms to the saved batch."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from CreatureGeometry import *
from GnomeStates import append_gnome,fitted_belt,gnome_state_pigment
bpy.ops.wm.open_mainfile(filepath=str(OUT/'CreatureBatch15.blend'))
MATS['leather']=bpy.data.materials['leather']
for col in bpy.data.collections:col.hide_viewport=False
for obj in bpy.data.objects:
    if obj.type=='MESH':obj['preserve_paint']=True
for key,color in {'lime':(.13,.77,.012),'forest':(.008,.29,.008),'red':(.78,.012,.008),'peach':(.78,.40,.23),'beard':(.64,.67,.60),
                  'wizard_green':(.045,.48,.018),'mummy_linen':(.74,.71,.60),'gnome_dry_skin':(.51,.39,.28),'undead_red':(.65,.008,.012),
                  'gnome_rot_green':(.018,.28,.032),'gnome_rot_light':(.12,.54,.025),'gnome_ash_beard':(.20,.32,.30),'zombie_cloth':(.028,.37,.025)}.items():
    COLORS[key]=color;MATS[key]=bpy.data.materials.get(key)
NEW=['gnomish_wizard_female','gnome_zombie_female']
for key in NEW:
    col,body=append_gnome(key);fitted_belt(key)
    for obj in list(bpy.context.scene.objects):
        if obj.type=='MESH' and obj.get('creature')==key:
            for parent in list(obj.users_collection):parent.objects.unlink(obj)
            col.objects.link(obj)
PIGMENT_FUNCTION=gnome_state_pigment
pipeline=Path(__file__).with_name('CreatureBatch2Pipeline.py').read_text(encoding='utf-8')
exec(compile(pipeline[:pipeline.index("if globals().get('POST_PAINT')")],'paint_new_female_forms','exec'))
for key in NEW:
    bpy.ops.object.select_all(action='DESELECT')
    for obj in bpy.data.objects:
        if obj.type=='MESH' and obj.get('creature')==key:obj.select_set(True)
    bpy.ops.export_scene.fbx(filepath=str(OUT/(key+'.fbx')),use_selection=True,object_types={'MESH'},apply_unit_scale=True,axis_forward='-Y',axis_up='Z',add_leaf_bones=False,bake_anim=False,mesh_smooth_type='FACE')
for col in bpy.data.collections:
    if col.name in NEW+['gnomish_wizard','gnome_mummy','gnome_zombie']:
        col.hide_viewport=col.name!='gnomish_wizard'
        for obj in col.objects:obj.hide_render=col.name!='gnomish_wizard'
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'CreatureBatch15.blend'))
print('CREATURE_BATCH15_FEMALE_FORMS_READY count=2',flush=True)
