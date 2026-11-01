"""Saved-mesh review refinements: expose mouth froth and open the warg jaw."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from CreatureGeometry import *
import CreatureGeometry as geo
from CreatureSaliva import rat_saliva
bpy.ops.wm.open_mainfile(filepath=str(OUT/'CreatureBatch7.blend'))
for col in bpy.data.collections:col.hide_viewport=False
for obj in bpy.data.objects:obj.hide_viewport=False
bpy.context.view_layer.update()
for obj in list(bpy.data.objects):
    if obj.get('creature')=='rabid_rat' and obj.get('state_module')=='saliva':bpy.data.objects.remove(obj,do_unlink=True)
geo.GROUP='rabid_rat';COLORS['saliva']=(.78,.79,.72);MATS['saliva']=bpy.data.materials['saliva']
before=set(bpy.data.objects);rat_saliva()
for obj in set(bpy.data.objects)-before:
    mesh=obj.data;bm=bmesh.new();bm.from_mesh(mesh);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(mesh);bm.free()
    attr=mesh.color_attributes.new(name='Paint',type='FLOAT_COLOR',domain='CORNER');mesh.color_attributes.active_color=attr
    lo=min(v.co.z for v in mesh.vertices);hi=max(v.co.z for v in mesh.vertices)
    for loop in mesh.loops:
        v=mesh.vertices[loop.vertex_index];p=obj.matrix_world@v.co
        shade=.79+.19*(v.co.z-lo)/max(.01,hi-lo)+.018*math.sin(p.x*28+p.y*21+p.z*13)
        attr.data[loop.index].color=(*(c*shade for c in COLORS['saliva']),1)
    for parent in list(obj.users_collection):parent.objects.unlink(obj)
    bpy.data.collections['rabid_rat'].objects.link(obj)
bpy.data.objects['warg_lower_jaw'].location.z-=.012
bpy.data.objects['warg_tongue'].location.z-=.004
for key in ['warg','rabid_rat']:
    bpy.ops.object.select_all(action='DESELECT')
    parts=[o for o in bpy.data.objects if o.type=='MESH' and o.get('creature')==key]
    for obj in parts:obj.hide_render=False;obj.select_set(True)
    bpy.context.view_layer.objects.active=parts[0]
    bpy.ops.export_scene.fbx(filepath=str(OUT/(key+'.fbx')),use_selection=True,object_types={'MESH'},apply_unit_scale=True,
        axis_forward='-Y',axis_up='Z',add_leaf_bones=False,bake_anim=False,mesh_smooth_type='FACE')
for key in ['coyote','warg','rabid_rat']:
    bpy.data.collections[key].hide_viewport=key!='coyote'
    for obj in bpy.data.objects:
        if obj.get('creature')==key:obj.hide_render=key!='coyote'
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'CreatureBatch7.blend'))
print('CREATURE_BATCH7_STATE_REFINEMENT_READY',flush=True)
