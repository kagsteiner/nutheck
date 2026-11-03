import bpy,bmesh,math,json,hashlib
from pathlib import Path
from mathutils import Vector
r=Path(__file__).resolve().parents[1];out=r/'Art/ObjectInterpretations';keys=['long_sword','scimitar','katana']
bpy.ops.wm.open_mainfile(filepath=str(out/'WeaponBatch1.blend'))
for c in bpy.data.collections:c.hide_viewport=False
bpy.context.view_layer.update();result={}
for key in keys:
    parts=[o for o in bpy.data.objects if o.type=='MESH' and o.get('creature')==key]
    for o in parts:
        a=o.data.color_attributes.get('Paint');assert a and a.domain=='CORNER' and a.data_type=='FLOAT_COLOR'
        assert not o.modifiers and not o.animation_data
        assert all(math.isfinite(c) for v in o.data.vertices for c in v.co)
        assert all(p.area>1e-12 for p in o.data.polygons),o.name
        bm=bmesh.new();bm.from_mesh(o.data);assert all(e.is_manifold for e in bm.edges),o.name;bm.free()
    blade=next(o for o in parts if o.get('blade_section_count'));assert blade['blade_section_count']==33
    assert bool(blade['double_edged'])==(key=='long_sword')
    pts=[o.matrix_world@v.co for o in parts for v in o.data.vertices];assert min(p.z for p in pts)>=0
    result[key]=dict(parts=len(parts),triangles=sum(len(p.vertices)-2 for o in parts for p in o.data.polygons),closed_geometry=True,paint_valid=True)
protected=json.loads((out/'weapon-batch1-protected.json').read_text());assert len(protected)==120
assert all(hashlib.sha256((r/n).read_bytes()).hexdigest()==h for n,h in protected.items());result['previous_120_exports_unchanged']=True
(out/'weapon-batch1-inspection.json').write_text(json.dumps(result,indent=2));print('WEAPON_BATCH1_NATIVE_CHECK PASS '+json.dumps(result))
scene=bpy.context.scene;cam=scene.camera;scene.cycles.samples=12;scene.render.resolution_x=700;scene.render.resolution_y=700
for key in keys:
    for o in bpy.data.objects:
        if o.type=='MESH':o.hide_render=o.get('creature')!=key
    for label,yaw,elev in [('front',-90,2),('underside',-110,-35),('hilt',-100,15)]:
        target=Vector((.025,0,.64 if label!='hilt' else .24));a=math.radians(yaw);e=math.radians(elev);cam.location=target+Vector((math.cos(a)*math.cos(e),math.sin(a)*math.cos(e),math.sin(e)))*3
        cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=1.40 if label!='hilt' else .47;cam.data.shift_x=cam.data.shift_y=0
        scene.render.filepath=str(out/(key+'-'+label+'.png'));bpy.ops.render.render(write_still=True)
print('WEAPON_BATCH1_DETAIL_REVIEW_READY')
