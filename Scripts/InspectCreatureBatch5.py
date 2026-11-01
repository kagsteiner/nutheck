"""Validate saved wolf geometry, independent age dimensions, UVs and paint."""
import bpy,json,math
from pathlib import Path
from mathutils import Vector
out=Path(__file__).resolve().parents[1]/'Art/CreatureInterpretations'
bpy.ops.wm.open_mainfile(filepath=str(out/'CreatureBatch5.blend'))
for collection in bpy.data.collections:collection.hide_viewport=False
for obj in bpy.data.objects:obj.hide_viewport=False
bpy.context.view_layer.update()
result={}
for key in ['wolf','winter_wolf_cub','winter_wolf']:
    parts=[o for o in bpy.data.objects if o.type=='MESH' and o.get('creature')==key]
    assert parts,key
    for obj in parts:
        paint=obj.data.color_attributes.get('Paint')
        assert paint and paint.domain=='CORNER' and paint.data_type=='FLOAT_COLOR',obj.name
        assert all(all(math.isfinite(c) for c in v.co) for v in obj.data.vertices)
        if obj.get('fur_surface'):
            assert obj.data.uv_layers.get('FurFlow'),obj.name
            assert all(m.name.startswith('Fur_') for m in obj.data.materials),obj.name
    body=bpy.data.objects[key+'_continuous_anatomy']
    points=[o.matrix_world@Vector(c) for o in parts for c in o.bound_box]
    low=[min(p[i] for p in points) for i in range(3)];high=[max(p[i] for p in points) for i in range(3)]
    assert low[2]>=-.003,(key,low)
    if key!='wolf':
        assert bpy.data.objects.get(key+'_cold_breath_socket')
        assert all('cyan' not in o.name and o.get('pigment')!='winter_cyan' for o in parts)
        assert all(c.color[2]<c.color[0]*1.12 for c in body.data.color_attributes['Paint'].data)
        eyes=[o for o in parts if o.get('eye_center') is not None]
        assert len(eyes)==2,(key,len(eyes))
        eyes.sort(key=lambda o:o['eye_side'])
        a,b=[Vector(o['eye_center']) for o in eyes]
        assert abs(a.x-b.x)<.001 and abs(a.z-b.z)<.001 and abs(a.y+b.y)<.001,(key,a,b)
        assert all(o['gaze_normal'][0]<-.6 for o in eyes)
    result[key]=dict(parts=len(parts),triangles=sum(sum(len(p.vertices)-2 for p in o.data.polygons) for o in parts),
        paint_valid=True,fur_uv_valid=True,bounds_m=[low,high],head_to_torso_length=body['head_to_torso_length'],age_variant=body['age_variant'])
    if key!='wolf':result[key].update(shadow_paint_removed=True,eye_centers_m=[list(a),list(b)],eye_symmetry_valid=True)
assert result['winter_wolf_cub']['head_to_torso_length']>result['winter_wolf']['head_to_torso_length']
assert result['winter_wolf']['bounds_m'][1][2]>result['wolf']['bounds_m'][1][2]>result['winter_wolf_cub']['bounds_m'][1][2]
(out/'batch5-mesh-inspection.json').write_text(json.dumps(result,indent=2))
print('CREATURE_BATCH5_NATIVE_CHECK PASS '+json.dumps(result),flush=True)
