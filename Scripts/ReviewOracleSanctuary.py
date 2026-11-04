import bpy,bmesh,json,math,hashlib
from pathlib import Path
r=Path(__file__).resolve().parents[1];out=r/'Art/OracleSanctuary';bpy.ops.wm.open_mainfile(filepath=str(out/'OracleSanctuary.blend'));parts=[o for o in bpy.data.objects if o.type=='MESH']
for o in parts:
 assert not o.modifiers and not o.animation_data
 assert all(math.isfinite(c) for v in o.data.vertices for c in v.co)
 assert all(p.area>1e-12 for p in o.data.polygons)
 a=o.data.color_attributes.get('Paint');assert a and a.domain=='CORNER' and a.data_type=='FLOAT_COLOR'
 bm=bmesh.new();bm.from_mesh(o.data);assert all(e.is_manifold for e in bm.edges);bm.free()
pts=[o.matrix_world@v.co for o in parts for v in o.data.vertices];assert all(-.5<=p.x<=.5 and -.5<=p.y<=.5 and 0<=p.z<=1.21 for p in pts)
protected=json.loads((out/'protected.json').read_text());assert all(hashlib.sha256((r/n).read_bytes()).hexdigest()==h for n,h in protected.items())
report=dict(parts=len(parts),triangles=sum(len(p.vertices)-2 for o in parts for p in o.data.polygons),prior_fbx_unchanged=len(protected),wall_footprint_m=[[min(p[i] for p in pts) for i in range(3)],[max(p[i] for p in pts) for i in range(3)]])
(out/'inspection.json').write_text(json.dumps(report,indent=2));print('ORACLE_GEOMETRY_PASS '+json.dumps(report))
