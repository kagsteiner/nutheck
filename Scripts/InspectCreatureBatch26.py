"""Saved snake topology, paint, continuous body and source/protected-asset audit."""
import sys,bpy,bmesh,json,math,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from CreatureBatch26Config import *
from SnakeFamily import path,SPECS
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
    body=next(o for o in parts if o.get('anatomy'));assert body['path_samples']==121
    # The remeshed body must be a single connected surface with a real tail.
    bm=bmesh.new();bm.from_mesh(body.data);bm.verts.ensure_lookup_table();seen=set();todo=[bm.verts[0]]
    while todo:
        v=todo.pop()
        if v in seen:continue
        seen.add(v);todo.extend(e.other_vert(v) for e in v.link_edges)
    assert len(seen)==len(bm.verts);bm.free()
    tree=BVHTree.FromObject(body,bpy.context.evaluated_depsgraph_get())
    tip=path(key)[-1];hit,normal,index,distance=tree.find_nearest(body.matrix_world.inverted()@tip);assert distance<.012
    eyes=[o for o in parts if o.get('eye_side')];assert len(eyes)==2
    assert len([o for o in parts if o.get('pupil_side')])==2
    assert not any(any(n in o.name for n in ['leg','wing','hood','fin']) for o in parts)
    assert sum('fork' in o.name for o in parts)==(0 if key=='garter_snake' else 2)
    pts=[o.matrix_world@v.co for o in parts for v in o.data.vertices]
    low=[min(v[i] for v in pts) for i in range(3)];high=[max(v[i] for v in pts) for i in range(3)];assert low[2]>=0,(key,low)
    result[key]=dict(parts=len(parts),triangles=sum(sum(len(p.vertices)-2 for p in o.data.polygons) for o in parts),bounds_m=[low,high],closed_geometry=True,paint_valid=True,continuous_body=True,eyes=2,source_sex_shared=True,head_width=body['head_width'],body_radius=body['body_radius'])
assert result['water_moccasin']['head_width']>result['snake']['head_width']>result['garter_snake']['head_width']
assert all(tiles[n.replace('_',' ')+',male']==tiles[n.replace('_',' ')+',female'] for n in GROUPS)
protected=json.loads((OUT/'batch26-protected-assets.json').read_text());assert len(protected)==92
assert all(hashlib.sha256((ROOT/n).read_bytes()).hexdigest()==h for n,h in protected.items())
report=json.loads((OUT/REPORT_NAME).read_text());water=next(e for e in report if e['key']=='water_moccasin')
assert water['mask_method']=='explicit_reviewed_spatial_mask_dark_anatomy_retained'
garter=next(e for e in report if e['key']=='garter_snake')
assert garter['mask_method']=='explicit_reviewed_spatial_mask_dark_anatomy_retained'
assert all((x,y) not in SOURCE_FIGURE_MASKS['garter_snake'] for y,row in enumerate(tiles['garter snake,male']) for x,ch in enumerate(row) if ch=='P')
result.update(previous_92_exports_unchanged=True,source_sex_tiles_identical=True,black_moccasin_anatomy_retained=True)
(OUT/'batch26-mesh-inspection.json').write_text(json.dumps(result,indent=2))
print('CREATURE_BATCH26_NATIVE_CHECK PASS '+json.dumps(result),flush=True)
