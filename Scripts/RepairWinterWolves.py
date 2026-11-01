"""Revise only saved winter wolves: remove tile-shadow paint and rebuild eyes."""
import sys,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from CreatureGeometry import *
import CreatureGeometry as geo
from WinterWolfEyes import winter_wolf_eyes

bpy.ops.wm.open_mainfile(filepath=str(OUT/'CreatureBatch5.blend'))
for col in bpy.data.collections:col.hide_viewport=False
for obj in bpy.data.objects:obj.hide_viewport=False
bpy.context.view_layer.update()
COLORS.update(winter_white=(.83,.88,.83),wolf_red=(.70,.008,.016),winter_inner=(.39,.34,.32))
# Reuse the saved pigment materials, retaining their vertex-colour shader.
for key in ['winter_white','wolf_red','black','glint']:
    mat=bpy.data.materials.get(key)
    if not mat:
        mat=bpy.data.materials.new(key);mat.use_nodes=True
        mat.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.82
    MATS[key]=mat
mat=bpy.data.materials.new('winter_inner');mat.use_nodes=True
mat.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.82
MATS['winter_inner']=mat
def paint(obj,pigment):
    mesh=obj.data
    color=COLORS[pigment];obj['pigment']=pigment
    attr=mesh.color_attributes.get('Paint') or mesh.color_attributes.new(name='Paint',type='FLOAT_COLOR',domain='CORNER')
    mesh.color_attributes.active_color=attr
    lo=min(v.co.z for v in mesh.vertices);hi=max(v.co.z for v in mesh.vertices)
    for loop in mesh.loops:
        v=mesh.vertices[loop.vertex_index];p=obj.matrix_world@v.co
        shade=.79+.19*(v.co.z-lo)/max(.01,hi-lo)+.018*math.sin(p.x*28+p.y*21+p.z*13)
        attr.data[loop.index].color=(*(max(0,min(1,c*shade)) for c in color),1)
    for material in mesh.materials:
        shader=material.node_tree.nodes.get('Principled BSDF')
        node=material.node_tree.nodes.get('Pigment')
        if not node:node=material.node_tree.nodes.new('ShaderNodeVertexColor');node.name='Pigment';node.layer_name='Paint'
        # Preserve the approved fur texture graph on existing coat surfaces.
        if not material.name.startswith('Fur_'):material.node_tree.links.new(node.outputs['Color'],shader.inputs['Base Color'])

unchanged=hashlib.sha256((OUT/'wolf.fbx').read_bytes()).hexdigest()
for key,length,head,leg,depth in [('winter_wolf_cub',.205,.112,.19,.112),('winter_wolf',.34,.137,.34,.172)]:
    parts=[o for o in bpy.data.objects if o.type=='MESH' and o.get('creature')==key]
    for obj in parts:
        suffix=obj.name[len(key)+1:]
        if suffix.startswith(('eye','cyan_muzzle_corner','orbital_rim','round_pupil','upper_eyelid','lower_eyelid')):
            bpy.data.objects.remove(obj,do_unlink=True)
        elif suffix.startswith('ear_lining'):
            obj.data.materials.clear();obj.data.materials.append(MATS['winter_inner']);paint(obj,'winter_inner')
        elif obj.get('coat_marking')=='winter_points':
            del obj['coat_marking'];paint(obj,'winter_white')
    body=bpy.data.objects[key+'_continuous_anatomy']
    before=set(bpy.data.objects)
    hx=-length*.60-.09;hz=leg+depth+depth*.87
    winter_wolf_eyes(key,hx,hz,head,body)
    for obj in set(bpy.data.objects)-before:
        bpy.context.view_layer.objects.active=obj
        for modifier in list(obj.modifiers):bpy.ops.object.modifier_apply(modifier=modifier.name)
        bm=bmesh.new();bm.from_mesh(obj.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(obj.data);bm.free()
        paint(obj,obj['pigment'])
        for parent in list(obj.users_collection):parent.objects.unlink(obj)
        bpy.data.collections[key].objects.link(obj)
    bpy.ops.object.select_all(action='DESELECT')
    parts=[o for o in bpy.data.objects if o.type=='MESH' and o.get('creature')==key]
    for obj in parts:obj.hide_render=False;obj.select_set(True)
    bpy.context.view_layer.objects.active=body
    bpy.ops.export_scene.fbx(filepath=str(OUT/(key+'.fbx')),use_selection=True,object_types={'MESH'},apply_unit_scale=True,
        axis_forward='-Y',axis_up='Z',add_leaf_bones=False,bake_anim=False,mesh_smooth_type='FACE')
for key in ['wolf','winter_wolf_cub','winter_wolf']:
    bpy.data.collections[key].hide_viewport=key!='wolf'
    for obj in bpy.data.objects:
        if obj.get('creature')==key:obj.hide_render=key!='wolf'
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'CreatureBatch5.blend'))
assert hashlib.sha256((OUT/'wolf.fbx').read_bytes()).hexdigest()==unchanged
print('WINTER_WOLF_REPAIR_READY count=2 ordinary_wolf_unchanged=True',flush=True)
