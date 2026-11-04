import sys,bpy,bmesh,math,json,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from CreatureGeometry import *
from PuddingEyes import add_eyes
bpy.ops.wm.open_mainfile(filepath=str(OUT/'CreatureBatch32.blend'))
for c in bpy.data.collections:c.hide_viewport=False
bpy.context.view_layer.update()
protected={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'Art').rglob('*.fbx') if p.stem not in ['brown_pudding','black_pudding']}
(OUT/'batch32-eye-protected.json').write_text(json.dumps(protected,indent=2))
for key in ['brown_pudding','black_pudding']:
 assert not any(o.get('tile_eye') and o.get('creature')==key for o in bpy.data.objects)
 body=next(o for o in bpy.data.objects if o.get('creature')==key and o.get('anatomy'))
 # Remove earlier inclusion interpretations from the two faces.
 attr=body.data.color_attributes['Paint']
 if key=='black_pudding':
  for item in attr.data:item.color=(.010,.013,.017,1)
 else:
  for loop in body.data.loops:
   p=body.matrix_world@body.data.vertices[loop.vertex_index].co;wave=math.sin(p.x*20+p.z*14)*math.cos(p.y*23-p.x*9);t=max(0,wave)**7*.65
   attr.data[loop.index].color=(*[a*(1-t)+b*t for a,b in zip((.29,.077,.004),(.82,.23,.014))],1)
 eyes=add_eyes(key,body)
 for o in eyes:
  mesh=o.data;bm=bmesh.new();bm.from_mesh(mesh);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));assert all(e.is_manifold for e in bm.edges);bm.to_mesh(mesh);bm.free()
  a=mesh.color_attributes.new(name='Paint',type='FLOAT_COLOR',domain='CORNER');mesh.color_attributes.active_color=a;c=COLORS[o['pigment']]
  for loop in mesh.loops:
   p=mesh.vertices[loop.vertex_index].co;t=1 if key!='black_pudding' else max(0,min(1,(p.z-.76)/.04))
   rgb=c if key!='black_pudding' else (.98,.008+.23*t,.002)
   a.data[loop.index].color=(*rgb,1)
  mat=mesh.materials[0];node=mat.node_tree.nodes.new('ShaderNodeVertexColor');node.layer_name='Paint';mat.node_tree.links.new(node.outputs['Color'],mat.node_tree.nodes['Principled BSDF'].inputs['Base Color'])
  for col in list(o.users_collection):col.objects.unlink(o)
  bpy.data.collections[key].objects.link(o)
 bpy.ops.object.select_all(action='DESELECT')
 for o in bpy.data.objects:
  if o.type=='MESH' and o.get('creature')==key:o.select_set(True)
 bpy.context.view_layer.objects.active=body
 bpy.ops.export_scene.fbx(filepath=str(OUT/(key+'.fbx')),use_selection=True,object_types={'MESH'},apply_unit_scale=True,axis_forward='-Y',axis_up='Z',add_leaf_bones=False,bake_anim=False,mesh_smooth_type='FACE')
assert all(hashlib.sha256((ROOT/n).read_bytes()).hexdigest()==h for n,h in protected.items())
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'CreatureBatch32.blend'))
print('PUDDING_EYES_REVISION_PASS')
