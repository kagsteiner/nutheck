import sys,bpy,bmesh,json,math,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from CreatureBatch27Config import *
from AdvancedSnakeFamily import path
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
        assert not o.modifiers and not o.animation_data
    body=next(o for o in parts if o.get('anatomy'));assert body['path_samples']==(169 if key=='python' else 121)
    bm=bmesh.new();bm.from_mesh(body.data);bm.verts.ensure_lookup_table();todo=[bm.verts[0]];seen=set()
    while todo:
        v=todo.pop()
        if v in seen:continue
        seen.add(v);todo.extend(e.other_vert(v) for e in v.link_edges)
    assert len(seen)==len(bm.verts),key;bm.free()
    tree=BVHTree.FromObject(body,bpy.context.evaluated_depsgraph_get());hit,n,i,d=tree.find_nearest(body.matrix_world.inverted()@path(key)[-1]);assert d<.012
    assert sum(bool(o.get('eye_side')) for o in parts)==2
    assert sum(bool(o.get('pupil_side')) for o in parts)==2
    assert sum(bool(o.get('facial_pit_side')) for o in parts)==(2 if key=='pit_viper' else 0)
    assert sum('tongue_fork' in o.name for o in parts)==(0 if key=='python' else 2)
    assert not any('wing' in o.name or 'leg' in o.name for o in parts)
    if key=='cobra':
        assert body['hood_width']>.27
        # Saved hood is genuinely spread on both sides of the upright neck.
        band=[body.matrix_world@v.co for v in body.data.vertices if .35<(body.matrix_world@v.co).z<.46]
        assert max(v.y for v in band)-min(v.y for v in band)>.24
    pts=[o.matrix_world@v.co for o in parts for v in o.data.vertices];low=[min(v[i] for v in pts) for i in range(3)];high=[max(v[i] for v in pts) for i in range(3)];assert low[2]>=0,(key,low)
    result[key]=dict(parts=len(parts),triangles=sum(len(p.vertices)-2 for o in parts for p in o.data.polygons),bounds_m=[low,high],closed_geometry=True,paint_valid=True,connected_body=True,source_sex_shared=True,head_width=body['head_width'],body_radius=body['body_radius'])
assert result['python']['body_radius']>result['pit_viper']['body_radius']>result['cobra']['body_radius']
assert result['pit_viper']['head_width']>result['python']['head_width']>result['cobra']['head_width']
assert all(tiles[n.replace('_',' ')+',male']==tiles[n.replace('_',' ')+',female'] for n in GROUPS)
protected=json.loads((OUT/'batch27-protected-assets.json').read_text());assert len(protected)==117
assert all(hashlib.sha256((ROOT/n).read_bytes()).hexdigest()==h for n,h in protected.items())
result.update(previous_117_exports_unchanged=True,black_anatomy_retained=True,source_sex_tiles_identical=True)
(OUT/'batch27-mesh-inspection.json').write_text(json.dumps(result,indent=2));print('CREATURE_BATCH27_NATIVE_CHECK PASS '+json.dumps(result))
