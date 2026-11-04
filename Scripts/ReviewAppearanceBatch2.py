import bpy,bmesh,math,json,hashlib
from pathlib import Path
from mathutils import Vector
r=Path(__file__).resolve().parents[1];out=r/'Art/ObjectInterpretations';keys=['sapphire_ring','triangular_amulet','silver_wand']
bpy.ops.wm.open_mainfile(filepath=str(out/'AppearanceBatch2.blend'))
for c in bpy.data.collections:c.hide_viewport=False
bpy.context.view_layer.update();result={}
for key in keys:
    parts=[o for o in bpy.data.objects if o.type=='MESH' and o.get('creature')==key]
    for o in parts:
        a=o.data.color_attributes.get('Paint');assert a and a.domain=='CORNER' and a.data_type=='FLOAT_COLOR'
        assert not o.modifiers and not o.animation_data
        assert all(abs(v-1)<1e-6 for v in o.scale)
        assert all(math.isfinite(v) and 0<=v<=1 for c in a.data for v in c.color)
        assert all(math.isfinite(c) for v in o.data.vertices for c in v.co)
        assert all(p.area>1e-12 for p in o.data.polygons),o.name
        bm=bmesh.new();bm.from_mesh(o.data);assert all(e.is_manifold for e in bm.edges),o.name;bm.free()
    if key=='sapphire_ring':
        gem=next(o for o in parts if o.get('cut_gem'));top=[gem.matrix_world@gem.data.vertices[i].co for i in range(12)]
        assert max(v.z for v in top)-min(v.z for v in top)<1e-7
        assert all(v.z>=max((gem.matrix_world@v.co).z for v in gem.data.vertices)-1e-7 for v in top)
        assert list(gem['crown_axis'])==[0,0,1]
    assert any(o.get({'sapphire_ring':'open_band','triangular_amulet':'triangular_body','silver_wand':'metal_shaft'}[key]) for o in parts)
    pts=[o.matrix_world@v.co for o in parts for v in o.data.vertices];assert abs(min(p.z for p in pts))<1e-6
    result[key]=dict(parts=len(parts),triangles=sum(len(p.vertices)-2 for o in parts for p in o.data.polygons),closed_geometry=True,paint_valid=True,bounds_m=[[min(p[i] for p in pts) for i in range(3)],[max(p[i] for p in pts) for i in range(3)]])
protected=json.loads((out/'appearance-batch2-protected.json').read_text())
assert all(hashlib.sha256((r/n).read_bytes()).hexdigest()==h for n,h in protected.items());result['protected_exports']=len(protected);result['previous_exports_unchanged']=True
(out/'appearance-batch2-inspection.json').write_text(json.dumps(result,indent=2));print('APPEARANCE_BATCH2_MESH_CHECK PASS '+json.dumps(result))
import sys
if '--checks-only' in sys.argv: sys.exit(0)
scene=bpy.context.scene;cam=scene.camera;scene.cycles.samples=12;scene.render.resolution_x=700;scene.render.resolution_y=700
for key in keys:
    for o in bpy.data.objects:
        if o.type=='MESH':o.hide_render=o.get('creature')!=key
    for label,yaw,elev in [('front',-90,2),('underside',-110,-35),('hilt',-100,15)]:
        height=max(p.z for o in bpy.data.objects if o.type=='MESH' and o.get('creature')==key for p in [o.matrix_world@v.co for v in o.data.vertices]);target=Vector((0,0,height*.5 if label!='hilt' else {'sapphire_ring':.034,'triangular_amulet':.025,'silver_wand':.10}[key]));a=math.radians(yaw);e=math.radians(elev);cam.location=target+Vector((math.cos(a)*math.cos(e),math.sin(a)*math.cos(e),math.sin(e)))*3
        cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=height*1.12 if label!='hilt' else {'sapphire_ring':.033,'triangular_amulet':.055,'silver_wand':.12}[key];cam.data.shift_x=cam.data.shift_y=0
        scene.render.filepath=str(out/(key+'-'+label+'.png'));bpy.ops.render.render(write_still=True)
print('APPEARANCE_BATCH2_DETAIL_REVIEW_READY')
