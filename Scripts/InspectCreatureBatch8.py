"""Saved bat geometry: closed wings, digits/thumbs, paired eyes and proportion checks."""
import bpy,bmesh,json,math
from pathlib import Path
from mathutils import Vector
out=Path(__file__).resolve().parents[1]/'Art/CreatureInterpretations'
bpy.ops.wm.open_mainfile(filepath=str(out/'CreatureBatch8.blend'))
for col in bpy.data.collections:col.hide_viewport=False
for obj in bpy.data.objects:obj.hide_viewport=False
bpy.context.view_layer.update()
result={}
for key in ['bat','giant_bat','vampire_bat']:
    parts=[o for o in bpy.data.objects if o.type=='MESH' and o.get('creature')==key]
    assert parts,key
    for obj in parts:
        paint=obj.data.color_attributes.get('Paint')
        assert paint and paint.domain=='CORNER' and paint.data_type=='FLOAT_COLOR',obj.name
        assert all(all(math.isfinite(c) for c in v.co) for v in obj.data.vertices)
        if obj.get('fur_surface'):
            assert obj.data.uv_layers.get('FurFlow')
            assert all(m.name.startswith('Fur_') for m in obj.data.materials)
        if obj.get('wing_membrane'):
            bm=bmesh.new();bm.from_mesh(obj.data)
            assert all(e.is_manifold for e in bm.edges),obj.name
            assert all(f.calc_area()>1e-11 for f in bm.faces),obj.name
            bm.free()
            assert not obj.get('fur_surface'),obj.name
    wings=[o for o in parts if o.get('wing_membrane') and not o.get('tail_membrane')]
    assert len(wings)==2 and {o['wing_side'] for o in wings}=={-1,1}
    assert len([o for o in parts if o.get('tail_membrane')])==1
    assert len([o for o in parts if o.name.startswith(key+'_free_thumb')])==2
    assert len([o for o in parts if o.name.startswith(key+'_thumb_claw')])==2
    for side in [-1,1]:
        assert sorted(o['wing_digit'] for o in parts if o.get('wing_side')==side and o.get('wing_digit'))==[2,3,4,5]
    body=bpy.data.objects[key+'_continuous_anatomy']
    eyes=sorted([o for o in parts if o.get('eye_center') is not None],key=lambda o:o['eye_side'])
    assert len(eyes)==2
    a,b=[Vector(o['eye_center']) for o in eyes]
    assert abs(a.x-b.x)<.001 and abs(a.z-b.z)<.001 and abs(a.y+b.y)<.001,(key,a,b)
    points=[o.matrix_world@Vector(c) for o in parts for c in o.bound_box]
    low=[min(p[i] for p in points) for i in range(3)];high=[max(p[i] for p in points) for i in range(3)]
    assert low[2]>=0,(key,low)
    result[key]=dict(parts=len(parts),triangles=sum(sum(len(p.vertices)-2 for p in o.data.polygons) for o in parts),
        bounds_m=[low,high],paint_valid=True,fur_uv_valid=True,closed_membranes=True,wing_fingers_per_side=4,
        free_thumbs=2,eye_symmetry_valid=True,eye_centers_m=[list(a),list(b)],half_span=body['half_span'],
        wing_chord=body['wing_chord'],head_to_body_length=body['head_to_body_length'])
assert result['giant_bat']['half_span']>result['bat']['half_span']
assert result['giant_bat']['head_to_body_length']<result['bat']['head_to_body_length']
assert result['vampire_bat']['wing_chord']>result['giant_bat']['wing_chord']
(out/'batch8-mesh-inspection.json').write_text(json.dumps(result,indent=2))
print('CREATURE_BATCH8_NATIVE_CHECK PASS '+json.dumps(result),flush=True)
