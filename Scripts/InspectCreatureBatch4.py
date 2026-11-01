"""Inspect saved geometry and paint without rerunning the generator."""
import bpy,json
from pathlib import Path
from mathutils import Vector
out=Path(__file__).resolve().parents[1]/'Art/CreatureInterpretations'
bpy.ops.wm.open_mainfile(filepath=str(out/'CreatureBatch4.blend'))
# Hidden gallery collections do not evaluate object transforms on file load.
for collection in bpy.data.collections: collection.hide_viewport=False
for obj in bpy.data.objects: obj.hide_viewport=False
bpy.context.view_layer.update()
result={}
for key in ['kitten','housecat','large_cat']:
    parts=[o for o in bpy.data.objects if o.type=='MESH' and o.get('creature')==key]
    assert parts,key
    for obj in parts:
        paint=obj.data.color_attributes.get('Paint')
        assert paint and paint.domain=='CORNER' and paint.data_type=='FLOAT_COLOR',obj.name
        assert all(v.co.x==v.co.x and v.co.y==v.co.y and v.co.z==v.co.z for v in obj.data.vertices)
    body=bpy.data.objects[key+'_continuous_anatomy']
    points=[o.matrix_world@Vector(c) for o in parts for c in o.bound_box]
    low=[min(p[i] for p in points) for i in range(3)];high=[max(p[i] for p in points) for i in range(3)]
    assert low[2]>=-.003,key
    result[key]=dict(parts=len(parts),vertices=sum(len(o.data.vertices) for o in parts),
        paint_valid=True,bounds_m=[low,high],head_to_torso_length=body['head_to_torso_length'],age_variant=body['age_variant'])
assert result['kitten']['head_to_torso_length']>result['housecat']['head_to_torso_length']
assert result['housecat']['bounds_m'][1][2]>result['kitten']['bounds_m'][1][2]
assert result['large_cat']['bounds_m'][1][2]>result['housecat']['bounds_m'][1][2]
(out/'batch4-mesh-inspection.json').write_text(json.dumps(result,indent=2))
print('CREATURE_BATCH4_NATIVE_CHECK PASS '+json.dumps(result),flush=True)
