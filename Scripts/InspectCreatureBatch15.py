"""Saved gnome ancestry hashes, linen fit, paint/eyes and prior-export protection."""
import bpy,bmesh,json,math,hashlib,struct
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
root=Path(__file__).resolve().parents[1];out=root/'Art/CreatureInterpretations'
bpy.ops.wm.open_mainfile(filepath=str(out/'CreatureBatch15.blend'))
for c in bpy.data.collections:c.hide_viewport=False
bpy.context.view_layer.update()
def signature(o):return hashlib.sha256(b''.join(struct.pack('<3f',*v.co) for v in o.data.vertices)).hexdigest()
result={};saved={}
for key in ['gnomish_wizard','gnome_mummy','gnome_zombie','gnomish_wizard_female','gnome_zombie_female']:
    parts=[o for o in bpy.data.objects if o.type=='MESH' and o.get('creature')==key];assert parts
    for o in parts:
        paint=o.data.color_attributes.get('Paint');assert paint and paint.domain=='CORNER' and paint.data_type=='FLOAT_COLOR'
        assert all(math.isfinite(c) for v in o.data.vertices for c in v.co)
        assert all(p.area>1e-12 for p in o.data.polygons),o.name
    body=bpy.data.objects[key+'_body'];saved[key]=signature(body)
    points=[o.matrix_world@v.co for o in parts for v in o.data.vertices]
    low=[min(p[i] for p in points) for i in range(3)];high=[max(p[i] for p in points) for i in range(3)];assert low[2]>=-.003,(key,low)
    eyes=sorted([o for o in parts if o.get('eye_side')],key=lambda o:o['eye_side']);assert len(eyes)==2
    a,b=[o.location for o in eyes];assert abs(a.x+b.x)<1e-6 and abs(a.y-b.y)<1e-6 and abs(a.z-b.z)<1e-6
    tree=BVHTree.FromObject(body,bpy.context.evaluated_depsgraph_get());gaps=[tree.find_nearest(body.matrix_world.inverted()@o.location)[3] for o in eyes];assert max(gaps)<.015
    if key.startswith('gnome_'):
        assert all(sum(p.color[0] for p in o.data.color_attributes['Paint'].data)>sum(p.color[1] for p in o.data.color_attributes['Paint'].data)*5 for o in eyes)
    wraps=[o for o in parts if o.get('wrap_module')];wrap_gaps={};assert bool(wraps)==(key=='gnome_mummy')
    for o in wraps:
        bm=bmesh.new();bm.from_mesh(o.data);assert all(e.is_manifold for e in bm.edges),o.name;bm.free()
        gap=max(tree.find_nearest(body.matrix_world.inverted()@(o.matrix_world@v.co))[3] for v in o.data.vertices)
        assert gap<.006,(o.name,gap);wrap_gaps[o.name]=gap
    assert any('pointed_cap' in o.name for o in parts)
    if key.endswith('_female'):assert not any('beard_chin' in o.name or 'beard_lock' in o.name for o in parts)
    else:assert any('beard_chin' in o.name for o in parts)
    assert sum('boot' in o.name for o in parts)==2
    assert not any(any(s in o.name for s in ['axe','staff','red_cap_tip','shadow','crown']) for o in parts)
    belts=[o for o in parts if 'fitted_costume_belt' in o.name];assert bool(belts)==(key!='gnome_mummy')
    if key=='gnome_mummy':assert not any('tunic' in o.name or 'mantle' in o.name or 'buckle' in o.name for o in parts)
    result[key]=dict(parts=len(parts),triangles=sum(sum(len(p.vertices)-2 for p in o.data.polygons) for o in parts),bounds_m=[low,high],paint_valid=True,paired_eyes=True,eye_surface_distances_m=gaps,wrap_count=len(wraps),wrap_max_surface_gaps_m=wrap_gaps,body_vertex_hash=saved[key],pointed_hat_retained=True,beard_present=not key.endswith('_female'))
with bpy.data.libraries.load(str(out/'CreatureBatch2.blend'),link=False) as (src,dst):dst.objects=['gnome_body']
assert all(h==signature(dst.objects[0]) for h in saved.values())
protected=json.loads((out/'batch15-protected-assets.json').read_text());assert len(protected)==48
assert all(hashlib.sha256((root/n).read_bytes()).hexdigest()==h for n,h in protected.items())
result['previous_48_exports_unchanged']=True;result['exact_ancestry_shape_reuse']=True
(out/'batch15-mesh-inspection.json').write_text(json.dumps(result,indent=2))
print('CREATURE_BATCH15_NATIVE_CHECK PASS '+json.dumps(result),flush=True)
