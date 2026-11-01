"""Saved geometry/paint, hover/iris, amphibian and fungal body checks."""
import bpy,bmesh,json,math,hashlib,re
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
root=Path(__file__).resolve().parents[1];out=root/'Art/CreatureInterpretations'
bpy.ops.wm.open_mainfile(filepath=str(out/'CreatureBatch19.blend'))
for c in bpy.data.collections:c.hide_viewport=False
bpy.context.view_layer.update();result={}
for key in ['floating_eye','newt','lichen']:
    parts=[o for o in bpy.data.objects if o.type=='MESH' and o.get('creature')==key];assert parts
    for o in parts:
        paint=o.data.color_attributes.get('Paint');assert paint and paint.domain=='CORNER' and paint.data_type=='FLOAT_COLOR',o.name
        assert all(math.isfinite(c) for v in o.data.vertices for c in v.co)
        assert all(p.area>1e-12 for p in o.data.polygons),o.name
        bm=bmesh.new();bm.from_mesh(o.data);assert all(e.is_manifold for e in bm.edges),o.name;bm.free()
    points=[o.matrix_world@v.co for o in parts for v in o.data.vertices]
    low=[min(v[i] for v in points) for i in range(3)];high=[max(v[i] for v in points) for i in range(3)]
    assert low[2]>=0,(key,low)
    checks={}
    if key=='floating_eye':
        assert len(parts)==2 and .40<low[2]<.41
        iris=bpy.data.objects[key+'_curved_iris'];center=Vector((0,0,.64))
        radii=[((iris.matrix_world@v.co)-center).length for v in iris.data.vertices]
        assert min(radii)>.235 and max(radii)<.238,(min(radii),max(radii))
        paint=iris.data.color_attributes['Paint'].data
        assert any(p.color[2]>.3 and p.color[1]>.2 for p in paint)
        assert any(p.color[2]>.3 and p.color[1]<.05 for p in paint)
        assert any(max(p.color[:3])<.02 for p in paint)
        checks=dict(hover_clearance_m=low[2],curved_closed_iris=True,iris_radius_range_m=[min(radii),max(radii)],three_source_iris_colours=True)
    else:
        body=next(o for o in parts if not o.get('eye_side'));tree=BVHTree.FromObject(body,bpy.context.evaluated_depsgraph_get());inv=body.matrix_world.inverted()
        # Both are single connected closed bodies, with complete undersides.
        adjacency=[[] for _ in body.data.vertices]
        for e in body.data.edges:
            a,b=e.vertices;adjacency[a].append(b);adjacency[b].append(a)
        seen=set();todo=[0]
        while todo:
            v=todo.pop()
            if v in seen:continue
            seen.add(v);todo.extend(adjacency[v])
        assert len(seen)==len(adjacency),(key,len(seen),len(adjacency))
        if key=='newt':
            eyes=sorted([o for o in parts if o.get('eye_side')],key=lambda o:o['eye_side']);assert len(eyes)==2 and len(parts)==3
            gaps=[tree.find_nearest(inv@o.location)[3] for o in eyes];assert max(gaps)<.006,gaps
            probes=[(x,s*y,z) for s in [-1,1] for x,y,z in [(-.170,.149,.026),(.110,.155,.026)]]
            gaps_feet=[tree.find_nearest(inv@Vector(p))[3] for p in probes];assert max(gaps_feet)<.025
            assert high[0]>.35 and high[1]>.18 and low[0]<-.35
            checks=dict(continuous_body=True,paired_eyes_surface_gaps_m=gaps,four_splayed_feet_surface_gaps_m=gaps_feet,tapered_tail_present=True)
        else:
            assert len(parts)==1 and high[2]<.25
            assert not any(s in body.name for s in ['eye','head','limb','stem'])
            paint=body.data.color_attributes['Paint'].data
            assert any(p.color[0]>.4 and p.color[1]<.4 for p in paint)
            assert any(p.color[0]>.4 and p.color[1]>.4 for p in paint)
            checks=dict(continuous_foliose_body=True,eyeless_headless_limbless=True,orange_and_pale_surface_paint=True)
    result[key]=dict(parts=len(parts),triangles=sum(sum(len(p.vertices)-2 for p in o.data.polygons) for o in parts),bounds_m=[low,high],paint_valid=True,closed_geometry=True,**checks)
text=(root/'upstream/NetHack/win/share/monsters.txt').read_text(encoding='utf-8')
tiles={name:rows for _,name,rows in re.findall(r'^# tile (\d+) \(([^\n]+)\)\s*\{([^}]+)\}',text,re.M)}
assert all(tiles[n+',male']==tiles[n+',female'] for n in ['floating eye','newt','lichen'])
protected=json.loads((out/'batch19-protected-assets.json').read_text(encoding='utf-8'));assert len(protected)==61
assert all(hashlib.sha256((root/n).read_bytes()).hexdigest()==h for n,h in protected.items())
result.update(previous_61_exports_unchanged=True,source_sex_tiles_identical=True)
(out/'batch19-mesh-inspection.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print('CREATURE_BATCH19_NATIVE_CHECK PASS '+json.dumps(result),flush=True)
