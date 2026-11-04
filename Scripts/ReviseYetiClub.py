import sys,bpy,bmesh,math,json,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from CreatureGeometry import *
from YetiClub import add_club
bpy.ops.wm.open_mainfile(filepath=str(OUT/'CreatureBatch29.blend'))
for c in bpy.data.collections:c.hide_viewport=False
bpy.context.view_layer.update()
assert not any(o.get('held_club') for o in bpy.data.objects),'Revision already applied; use saved render scripts'
protected={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'Art').rglob('*.fbx') if p.stem!='yeti'}
(OUT/'yeti-club-protected.json').write_text(json.dumps(protected,indent=2))
club=add_club();mesh=club.data
bm=bmesh.new();bm.from_mesh(mesh);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));assert all(e.is_manifold for e in bm.edges);bm.to_mesh(mesh);bm.free()
paint=mesh.color_attributes.new(name='Paint',type='FLOAT_COLOR',domain='CORNER');mesh.color_attributes.active_color=paint
for loop in mesh.loops:
 p=mesh.vertices[loop.vertex_index].co;grain=.82+.13*math.sin(p.x*92+p.y*77)+.035*math.sin(p.z*157)
 paint.data[loop.index].color=(.40*grain,.12*grain,.018*grain,1)
mat=mesh.materials[0];attr=mat.node_tree.nodes.new('ShaderNodeVertexColor');attr.layer_name='Paint';mat.node_tree.links.new(attr.outputs['Color'],mat.node_tree.nodes['Principled BSDF'].inputs['Base Color'])
for c in list(club.users_collection):c.objects.unlink(club)
bpy.data.collections['yeti'].objects.link(club)
bpy.ops.object.select_all(action='DESELECT')
parts=[o for o in bpy.data.objects if o.type=='MESH' and o.get('creature')=='yeti']
for o in parts:o.select_set(True)
bpy.context.view_layer.objects.active=club
bpy.ops.export_scene.fbx(filepath=str(OUT/'yeti.fbx'),use_selection=True,object_types={'MESH'},apply_unit_scale=True,axis_forward='-Y',axis_up='Z',add_leaf_bones=False,bake_anim=False,mesh_smooth_type='FACE')
assert min(v.co.z for v in mesh.vertices)>0
assert all(hashlib.sha256((ROOT/n).read_bytes()).hexdigest()==h for n,h in protected.items())
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'CreatureBatch29.blend'))
print('YETI_CLUB_REVISION_PASS protected='+str(len(protected)))
