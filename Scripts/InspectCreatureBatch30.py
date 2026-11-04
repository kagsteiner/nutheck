import sys,bpy,bmesh,json,math,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from CreatureBatch30Config import *
from mathutils.bvhtree import BVHTree
bpy.ops.wm.open_mainfile(filepath=str(OUT/BLEND_NAME))
for c in bpy.data.collections:c.hide_viewport=False
bpy.context.view_layer.update();result={}
for key in GROUPS:
 parts=[o for o in bpy.data.objects if o.type=='MESH' and o.get('creature')==key];assert parts
 body=next(o for o in parts if o.get('anatomy'));tree=BVHTree.FromObject(body,bpy.context.evaluated_depsgraph_get())
 for o in parts:
  a=o.data.color_attributes.get('Paint');assert a and a.domain=='CORNER' and a.data_type=='FLOAT_COLOR',o.name
  assert all(math.isfinite(c) for v in o.data.vertices for c in v.co)
  assert all(p.area>1e-13 for p in o.data.polygons),o.name
  bm=bmesh.new();bm.from_mesh(o.data)
  if not o.get('eye_patch'):assert all(e.is_manifold for e in bm.edges),o.name
  bm.free();assert not o.modifiers and not o.animation_data
  if o.get('fur_surface'):assert o.data.uv_layers.get('FurFlow') and any(m.name.startswith('Fur_') for m in o.data.materials)
 bm=bmesh.new();bm.from_mesh(body.data);bm.verts.ensure_lookup_table();todo=[bm.verts[0]];seen=set()
 while todo:
  v=todo.pop()
  if v in seen:continue
  seen.add(v);todo.extend(e.other_vert(v) for e in v.link_edges)
 assert len(seen)==len(bm.verts),key;bm.free()
 pts=[o.matrix_world@v.co for o in parts for v in o.data.vertices];low=[min(v[i] for v in pts) for i in range(3)];high=[max(v[i] for v in pts) for i in range(3)];assert low[2]>=-1e-6
 assert tiles[key.replace('_',' ')+',male']==tiles[key.replace('_',' ')+',female']
 result[key]=dict(parts=len(parts),triangles=sum(len(p.vertices)-2 for o in parts for p in o.data.polygons),bounds_m=[low,high],closed_solids=True,paint_valid=True,connected_body=True,source_sex_shared=True,texture_only_fur=False)
protected=json.loads((OUT/'batch30-protected-assets.json').read_text());assert all(hashlib.sha256((ROOT/n).read_bytes()).hexdigest()==h for n,h in protected.items())
result['protected_exports_unchanged']=len(protected)
(OUT/'batch30-mesh-inspection.json').write_text(json.dumps(result,indent=2));print('CREATURE_BATCH30_NATIVE_CHECK PASS '+json.dumps(result))
