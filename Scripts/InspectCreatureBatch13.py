"""Inspect saved kobold drafts, independent family proportions and protected exports."""
import bpy,bmesh,json,math,hashlib
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
out=Path(__file__).resolve().parents[1]/'Art/CreatureInterpretations'
bpy.ops.wm.open_mainfile(filepath=str(out/'CreatureBatch13.blend'))
for c in bpy.data.collections:c.hide_viewport=False
bpy.context.view_layer.update();result={}
for key in ['kobold','large_kobold','kobold_leader']:
    parts=[o for o in bpy.data.objects if o.type=='MESH' and o.get('creature')==key];assert parts
    for o in parts:
        paint=o.data.color_attributes.get('Paint');assert paint and paint.domain=='CORNER' and paint.data_type=='FLOAT_COLOR',o.name
        assert all(math.isfinite(c) for v in o.data.vertices for c in v.co)
        assert all(p.area>1e-12 for p in o.data.polygons),o.name
    points=[o.matrix_world@v.co for o in parts for v in o.data.vertices]
    low=[min(v[i] for v in points) for i in range(3)];high=[max(v[i] for v in points) for i in range(3)]
    assert low[2]>=-.003,(key,low)
    body=bpy.data.objects[key+'_continuous_anatomy']
    eyes=sorted([o for o in parts if o.get('eye_side')],key=lambda o:o['eye_side']);assert len(eyes)==2
    a,b=[o.location for o in eyes];assert abs(a.x+b.x)<1e-6 and abs(a.y-b.y)<1e-6 and abs(a.z-b.z)<1e-6
    tree=BVHTree.FromObject(body,bpy.context.evaluated_depsgraph_get())
    gaps=[tree.find_nearest(body.matrix_world.inverted()@o.location)[3] for o in eyes]
    assert max(gaps)<.012,(key,gaps)
    ears=[o for o in parts if o.get('ear_tip_height')];assert len(ears)==2
    assert all(any(sum(p.color[:3])>1.5 for p in o.data.color_attributes['Paint'].data) for o in ears)
    modules=[o for o in parts if o.get('rank_module')];assert bool(modules)==(key=='kobold_leader')
    assert not any('weapon' in o.name or 'shadow' in o.name or 'tail' in o.name for o in parts)
    result[key]=dict(parts=len(parts),triangles=sum(sum(len(p.vertices)-2 for p in o.data.polygons) for o in parts),bounds_m=[low,high],paint_valid=True,paired_eyes=True,eye_center_surface_distances_m=gaps,painted_ear_tips=2,rank_modules=len(modules),height_parameter=body['height_parameter'],chest_parameter=body['chest_parameter'],head_parameter=body['head_parameter'])
assert result['large_kobold']['height_parameter']>result['kobold']['height_parameter']
assert result['large_kobold']['chest_parameter']/result['kobold']['chest_parameter']>result['large_kobold']['height_parameter']/result['kobold']['height_parameter']
protected=json.loads((out/'batch13-protected-assets.json').read_text());assert len(protected)==38
assert all(hashlib.sha256((out/n).read_bytes()).hexdigest()==h for n,h in protected.items())
result['previous_38_exports_unchanged']=True
(out/'batch13-mesh-inspection.json').write_text(json.dumps(result,indent=2))
print('CREATURE_BATCH13_NATIVE_CHECK PASS '+json.dumps(result),flush=True)
