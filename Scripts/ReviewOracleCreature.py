"""Inspect and render the saved Oracle, without regenerating any geometry."""
import bpy,bmesh,math,json,hashlib
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[1];O=R/'Art/CreatureInterpretations'
bpy.ops.wm.open_mainfile(filepath=str(O/'OracleCreature.blend'))
bpy.context.view_layer.update()
parts=[o for o in bpy.data.objects if o.type=='MESH' and o.get('creature')=='oracle']
body=next(o for o in parts if o.get('native_id')=='PM_ORACLE')
for o in parts:
 assert not o.modifiers and not o.animation_data,o.name
 assert all(math.isfinite(c) for v in o.data.vertices for c in v.co),o.name
 assert all(p.area>1e-12 for p in o.data.polygons),o.name
 a=o.data.color_attributes.get('Paint');assert a and a.domain=='CORNER' and len(a.data)==len(o.data.loops),o.name
 bm=bmesh.new();bm.from_mesh(o.data)
 if o.get('eye_surface_conforming'):assert all(e.is_manifold or e.is_boundary for e in bm.edges)
 else:assert all(e.is_manifold for e in bm.edges),o.name
 bm.free()
bm=bmesh.new();bm.from_mesh(body.data);todo=[next(iter(bm.verts))];seen=set()
while todo:
 v=todo.pop()
 if v in seen:continue
 seen.add(v);todo.extend(e.other_vert(v) for e in v.link_edges)
assert len(seen)==len(bm.verts),('Disconnected anatomy',len(seen),len(bm.verts));bm.free()
assert sum('raised_finger' in o.name for o in parts)==8
assert sum('thumb' in o.name for o in parts)==2
assert sum('toe' in o.name for o in parts)==10
assert sum('eye_center' in o for o in parts)==2
points=[o.matrix_world@v.co for o in parts for v in o.data.vertices]
low=[min(v[i] for v in points) for i in range(3)];high=[max(v[i] for v in points) for i in range(3)]
assert abs(low[2])<1e-6,low
protected=json.loads((O/'oracle-protected.json').read_text())
assert all(hashlib.sha256((R/n).read_bytes()).hexdigest()==h for n,h in protected.items())
report=dict(status='PASS',parts=len(parts),triangles=sum(len(p.vertices)-2 for o in parts for p in o.data.polygons),bounds_m=[low,high],connected_anatomy=True,closed_geometry_except_fitted_eye_surfaces=True,paint_valid=True,static=True,protected_exports_unchanged=len(protected),fingers=8,thumbs=2,toes=10,eyes=2)
(O/'oracle-mesh-inspection.json').write_text(json.dumps(report,indent=2))
print('ORACLE_MESH_CHECK PASS '+json.dumps(report),flush=True)
scene=bpy.context.scene;cam=scene.camera;scene.render.resolution_x=800;scene.render.resolution_y=800;scene.cycles.samples=24
center=(Vector(low)+Vector(high))*.5
for label,yaw,elev,target,scale in [('front',-90,5,center,1.5),('profile',0,5,center,1.5),('underside',-115,-35,center,1.5),('face',-95,5,Vector((0,-.015,body['head_z']+body.location.z-.33)),.34),('hand',-90,10,Vector((.415,-.013,1.12+body.location.z-.33)),.18)]:
 a=math.radians(yaw);e=math.radians(elev);cam.location=target+Vector((math.cos(a)*math.cos(e),math.sin(a)*math.cos(e),math.sin(e)))*3
 cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=scale;cam.data.shift_x=0;cam.data.shift_y=0
 scene.render.filepath=str(O/('oracle-'+label+'.png'));bpy.ops.render.render(write_still=True)
print('ORACLE_DETAIL_REVIEW_READY')
