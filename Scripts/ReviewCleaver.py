import bpy,bmesh,sys,math,json,hashlib
from pathlib import Path
from mathutils import Vector
r=Path(__file__).resolve().parents[1];out=r/'Art/ObjectInterpretations'
bpy.ops.wm.open_mainfile(filepath=str(out/'Cleaver.blend'))
for c in bpy.data.collections:c.hide_viewport=False
bpy.context.view_layer.update();parts=[o for o in bpy.data.objects if o.type=='MESH'];triangles=0
for o in parts:
    a=o.data.color_attributes.get('Paint');assert a and a.domain=='CORNER' and a.data_type=='FLOAT_COLOR'
    assert not o.modifiers and not o.animation_data
    assert all(math.isfinite(c) for v in o.data.vertices for c in v.co)
    assert all(p.area>1e-12 for p in o.data.polygons),o.name
    bm=bmesh.new();bm.from_mesh(o.data);assert all(e.is_manifold for e in bm.edges),o.name;bm.free()
    triangles+=sum(len(p.vertices)-2 for p in o.data.polygons)
protected=json.loads((out/'cleaver-protected-assets.json').read_text());assert len(protected)==103
assert all(hashlib.sha256((r/n).read_bytes()).hexdigest()==h for n,h in protected.items())
(out/'cleaver-inspection.json').write_text(json.dumps(dict(status='PASS',parts=len(parts),triangles=triangles,closed_geometry=True,paint_valid=True,previous_103_exports_unchanged=True),indent=2))
scene=bpy.context.scene;cam=scene.camera;scene.cycles.samples=24;scene.render.resolution_x=900;scene.render.resolution_y=900
for label,yaw,elev in [('front',-90,8),('rear',90,20),('underside',-125,-40),('detail',-75,15)]:
    target=Vector((0,0,.78 if label!='detail' else 1.22));a=math.radians(yaw);e=math.radians(elev)
    cam.location=target+Vector((math.cos(a)*math.cos(e),math.sin(a)*math.cos(e),math.sin(e)))*3
    cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=1.90 if label!='detail' else 1.35;cam.data.shift_x=cam.data.shift_y=0
    scene.render.filepath=str(out/('cleaver-'+label+'.png'));bpy.ops.render.render(write_still=True)
print('CLEAVER_NATIVE_CHECK PASS triangles='+str(triangles))

