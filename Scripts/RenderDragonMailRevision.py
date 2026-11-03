"""Refresh the saved revision without regenerating plates or scale geometry."""
import sys,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from CreatureGeometry import *
import CreatureGeometry as g
from ArmorBatch2Config import GROUPS as ALL_GROUPS
OUT=ROOT/'Art/ObjectInterpretations';bpy.ops.wm.open_mainfile(filepath=str(OUT/'ArmorBatch2.blend'))
for c in bpy.data.collections:c.hide_viewport=False
for o in list(bpy.data.objects):
    o.hide_viewport=False
    if o.type in {'LIGHT','CAMERA'}:bpy.data.objects.remove(o,do_unlink=True)
# Close the tiny crown openings in the saved first-pass curved shoulder lames.
# Future generations close these in DragonMailFamily.py directly.
for key in ALL_GROUPS[3:]:
    g.GROUP=key;pigment='dragon_'+key.split('_')[0];mat=bpy.data.materials[pigment];MATS[pigment]=mat
    if not any(o.get('creature')==key and o.get('shoulder_crown_cap') for o in bpy.data.objects):
        for side in [-1,1]:
            for tier in range(3):
                o=orb('small_closed_shoulder_crown',(side*(.217+tier*.024),0,.595-tier*.043+.059),(.012,.014,.003),pigment);o['shoulder_crown_cap']=True
                a=o.data.color_attributes.new(name='Paint',type='FLOAT_COLOR',domain='CORNER');o.data.color_attributes.active_color=a
                color=mat.diffuse_color[:3]
                for c in a.data:c.color=(*[v*.94 for v in color],1)
        # Export only the revised ten models; all plate exports remain untouched.
    parts=[o for o in bpy.data.objects if o.type=='MESH' and o.get('creature')==key]
    bpy.ops.object.select_all(action='DESELECT')
    for o in parts:o.select_set(True)
    bpy.context.view_layer.objects.active=parts[0]
    bpy.ops.export_scene.fbx(filepath=str(OUT/(key+'.fbx')),use_selection=True,object_types={'MESH'},apply_unit_scale=True,axis_forward='-Y',axis_up='Z',add_leaf_bones=False,bake_anim=False,mesh_smooth_type='FACE')
GROUPS=ALL_GROUPS[3:];INITIAL_GROUP=GROUPS[0];BLEND_NAME='ArmorBatch2.blend';REPORT_NAME='projection-report-armor-batch2.json'
objects={k:[o for o in bpy.data.objects if o.type=='MESH' and o.get('creature')==k] for k in GROUPS}
previous=json.loads((OUT/REPORT_NAME).read_text());SOURCE_TILE_NAMES={k:k.replace('_',' ') for k in GROUPS};SPATIAL_MASK_KEYS=GROUPS
pipeline=Path(__file__).with_name('CreatureBatch2Pipeline.py').read_text().replace('win/share/monsters.txt','win/share/objects.txt')
render=pipeline[pipeline.index('# Studio renders'):pipeline.index('for parts in objects.values():')]
exec(compile(render,'SavedDragonRevisionRender','exec'))
for o in bpy.data.objects:
    if o.type=='MESH':o.hide_render=o.get('creature')!=INITIAL_GROUP
for c in bpy.data.collections:
    if c.name in ALL_GROUPS:c.hide_viewport=c.name!=INITIAL_GROUP
scene.render.resolution_x=scene.render.resolution_y=800;bpy.ops.wm.save_as_mainfile(filepath=str(OUT/BLEND_NAME))
(OUT/REPORT_NAME).write_text(json.dumps([r for r in previous if r['key'] not in GROUPS]+report,indent=2))
print('DRAGON_MAIL_REVISION_RENDER_READY forms=10')
