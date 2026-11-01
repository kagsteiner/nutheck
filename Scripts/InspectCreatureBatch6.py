"""Saved native anatomy/paint/UV/eye checks; no mesh regeneration."""
import bpy,json,math
from pathlib import Path
from mathutils import Vector
out=Path(__file__).resolve().parents[1]/'Art/CreatureInterpretations'
bpy.ops.wm.open_mainfile(filepath=str(out/'CreatureBatch6.blend'))
for col in bpy.data.collections:col.hide_viewport=False
for obj in bpy.data.objects:obj.hide_viewport=False
bpy.context.view_layer.update()
result={}
for key in ['dog','large_dog','dingo']:
    parts=[o for o in bpy.data.objects if o.type=='MESH' and o.get('creature')==key]
    assert parts,key
    for obj in parts:
        paint=obj.data.color_attributes.get('Paint')
        assert paint and paint.domain=='CORNER' and paint.data_type=='FLOAT_COLOR',obj.name
        assert all(all(math.isfinite(c) for c in v.co) for v in obj.data.vertices)
        if obj.get('fur_surface'):
            assert obj.data.uv_layers.get('FurFlow')
            assert all(m.name.startswith('Fur_') for m in obj.data.materials)
    body=bpy.data.objects[key+'_continuous_anatomy']
    points=[o.matrix_world@Vector(c) for o in parts for c in o.bound_box]
    low=[min(p[i] for p in points) for i in range(3)];high=[max(p[i] for p in points) for i in range(3)]
    assert low[2]>=-.003,(key,low)
    eyes=sorted([o for o in parts if o.get('eye_center') is not None],key=lambda o:o['eye_side'])
    assert len(eyes)==2,key
    a,b=[Vector(o['eye_center']) for o in eyes]
    assert abs(a.x-b.x)<.001 and abs(a.z-b.z)<.001 and abs(a.y+b.y)<.001,(key,a,b)
    assert all(o['gaze_normal'][0]<-.6 for o in eyes)
    tail=next(o for o in parts if o.get('tail_form'))
    result[key]=dict(parts=len(parts),triangles=sum(sum(len(p.vertices)-2 for p in o.data.polygons) for o in parts),
        bounds_m=[low,high],paint_valid=True,fur_uv_valid=True,eye_symmetry_valid=True,
        eye_centers_m=[list(a),list(b)],head_to_torso_length=body['head_to_torso_length'],
        body_width=body['body_width'],body_length=body['body_length'],muzzle_length=body['muzzle_length'],tail_form=tail['tail_form'])
assert result['large_dog']['bounds_m'][1][2]>result['dog']['bounds_m'][1][2]
assert result['large_dog']['head_to_torso_length']<result['dog']['head_to_torso_length']
assert result['dingo']['body_width']<result['dog']['body_width']
assert result['dingo']['muzzle_length']>result['dog']['muzzle_length']
assert result['dog']['tail_form']==result['large_dog']['tail_form']=='curled'
assert result['dingo']['tail_form']=='swept_down'
(out/'batch6-mesh-inspection.json').write_text(json.dumps(result,indent=2))
print('CREATURE_BATCH6_NATIVE_CHECK PASS '+json.dumps(result),flush=True)
