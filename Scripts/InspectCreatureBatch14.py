"""Verify saved ancestry reuse, fitted solid linen, paint and unchanged prior exports."""
import bpy,bmesh,json,math,hashlib,struct
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
root=Path(__file__).resolve().parents[1];out=root/'Art/CreatureInterpretations'
bpy.ops.wm.open_mainfile(filepath=str(out/'CreatureBatch14.blend'))
for c in bpy.data.collections:c.hide_viewport=False
bpy.context.view_layer.update()
def signature(o):return hashlib.sha256(b''.join(struct.pack('<3f',*v.co) for v in o.data.vertices)).hexdigest()
result={};saved={}
for key in ['kobold_shaman','kobold_mummy','kobold_zombie']:
    parts=[o for o in bpy.data.objects if o.type=='MESH' and o.get('creature')==key];assert parts
    for o in parts:
        paint=o.data.color_attributes.get('Paint');assert paint and paint.domain=='CORNER' and paint.data_type=='FLOAT_COLOR'
        assert all(math.isfinite(c) for v in o.data.vertices for c in v.co)
        assert all(p.area>1e-12 for p in o.data.polygons),o.name
    body=bpy.data.objects[key+'_continuous_anatomy'];saved[key]=signature(body)
    points=[o.matrix_world@v.co for o in parts for v in o.data.vertices]
    low=[min(p[i] for p in points) for i in range(3)];high=[max(p[i] for p in points) for i in range(3)];assert low[2]>=-.003,(key,low)
    eyes=sorted([o for o in parts if o.get('eye_side')],key=lambda o:o['eye_side']);assert len(eyes)==2
    a,b=[o.location for o in eyes];assert abs(a.x+b.x)<1e-6 and abs(a.y-b.y)<1e-6 and abs(a.z-b.z)<1e-6
    tree=BVHTree.FromObject(body,bpy.context.evaluated_depsgraph_get());gaps=[tree.find_nearest(body.matrix_world.inverted()@o.location)[3] for o in eyes];assert max(gaps)<.012
    wraps=[o for o in parts if o.get('wrap_module')];wrap_gaps={}
    assert bool(wraps)==(key=='kobold_mummy')
    for o in wraps:
        bm=bmesh.new();bm.from_mesh(o.data);assert all(e.is_manifold for e in bm.edges),o.name;bm.free()
        dist=max(tree.find_nearest(body.matrix_world.inverted()@(o.matrix_world@v.co))[3] for v in o.data.vertices)
        assert dist<.006,(o.name,dist);wrap_gaps[o.name]=dist
    assert (sum(bool(o.get('caster_module')) for o in parts)>0)==(key=='kobold_shaman')
    assert not any('weapon' in o.name or 'staff' in o.name or 'shadow' in o.name for o in parts)
    result[key]=dict(parts=len(parts),triangles=sum(sum(len(p.vertices)-2 for p in o.data.polygons) for o in parts),bounds_m=[low,high],paint_valid=True,paired_eyes=True,eye_surface_distances_m=gaps,wrap_count=len(wraps),wrap_max_surface_gaps_m=wrap_gaps,body_vertex_hash=saved[key])
# Load reference objects as data only to compare exact ancestry geometry.
with bpy.data.libraries.load(str(out/'CreatureBatch13.blend'),link=False) as (src,dst):
    dst.objects=['kobold_leader_continuous_anatomy','large_kobold_continuous_anatomy']
leader,large=dst.objects
assert saved['kobold_shaman']==signature(leader)
assert saved['kobold_mummy']==saved['kobold_zombie']==signature(large)
protected=json.loads((out/'batch14-protected-assets.json').read_text());assert len(protected)==45
assert all(hashlib.sha256((root/n).read_bytes()).hexdigest()==h for n,h in protected.items())
result['previous_45_exports_unchanged']=True;result['exact_ancestry_shape_reuse']=True
(out/'batch14-mesh-inspection.json').write_text(json.dumps(result,indent=2))
print('CREATURE_BATCH14_NATIVE_CHECK PASS '+json.dumps(result),flush=True)
