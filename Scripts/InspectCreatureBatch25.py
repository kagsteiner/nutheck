"""Audit saved reptile topology, paint, inferred anatomy and preceding exports."""
import sys,bpy,bmesh,json,math,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from CreatureBatch25Config import *
from ReptileFamily import SPECS
from mathutils import Vector
from mathutils.bvhtree import BVHTree
bpy.ops.wm.open_mainfile(filepath=str(OUT/BLEND_NAME))
for c in bpy.data.collections:c.hide_viewport=False
bpy.context.view_layer.update();result={}
for key in GROUPS:
    parts=[o for o in bpy.data.objects if o.type=='MESH' and o.get('creature')==key];assert parts
    for o in parts:
        a=o.data.color_attributes.get('Paint');assert a and a.domain=='CORNER' and a.data_type=='FLOAT_COLOR',o.name
        assert all(math.isfinite(c) for v in o.data.vertices for c in v.co)
        assert all(p.area>1e-12 for p in o.data.polygons),o.name
        bm=bmesh.new();bm.from_mesh(o.data);assert all(e.is_manifold for e in bm.edges),o.name;bm.free()
        assert not o.modifiers and not o.animation_data,o.name
    body=next(o for o in parts if o.get('anatomy'));assert body['digit_count']==20
    assert bool(body['toe_pads'])==(key=='gecko')
    eyes=[o for o in parts if o.get('eye_side')];assert len(eyes)==2
    assert abs(eyes[0].location.y+eyes[1].location.y)<.0035 # one remesh voxel surface tolerance
    assert len([o for o in parts if o.get('pupil_side')])==2
    # Limbs/digits/claws are fused into the continuous body. Check the actual
    # saved surface at all twenty inferred toe tips rather than object names.
    spec=SPECS[key];tree=BVHTree.FromObject(body,bpy.context.evaluated_depsgraph_get())
    for side in [-1,1]:
        for front in [True,False]:
            x=-spec['length']*.65 if front else spec['length']*.60
            foot=Vector((x+(.005 if front else -.045),side*(spec['width']+.12),.025))
            for k in range(5):
                a=(k-2)*.43;d=(.045 if key=='gecko' else .063)*(1-.12*abs(k-2))
                tip=foot+Vector((math.sin(a)*d,side*math.cos(a)*d,-.012))
                hit,normal,index,distance=tree.find_nearest(body.matrix_world.inverted()@tip)
                assert distance<.012,(key,side,front,k,distance)
    assert sum('dorsal_spine' in o for o in parts)==(13 if key=='iguana' else 0)
    assert sum(bool(o.get('dewlap')) for o in parts)==(1 if key=='iguana' else 0)
    pts=[o.matrix_world@v.co for o in parts for v in o.data.vertices]
    low=[min(v[i] for v in pts) for i in range(3)];high=[max(v[i] for v in pts) for i in range(3)];assert low[2]>=0
    result[key]=dict(parts=len(parts),triangles=sum(sum(len(p.vertices)-2 for p in o.data.polygons) for o in parts),bounds_m=[low,high],closed_geometry=True,paint_valid=True,digits=20,eyes=2,source_sex_shared=True)
assert all(tiles[n+',male']==tiles[n+',female'] for n in GROUPS)
protected=json.loads((OUT/'batch25-protected-assets.json').read_text());assert len(protected)==89
assert all(hashlib.sha256((ROOT/n).read_bytes()).hexdigest()==h for n,h in protected.items())
result.update(previous_89_exports_unchanged=True,source_sex_tiles_identical=True)
(OUT/'batch25-mesh-inspection.json').write_text(json.dumps(result,indent=2))
print('CREATURE_BATCH25_NATIVE_CHECK PASS '+json.dumps(result),flush=True)

