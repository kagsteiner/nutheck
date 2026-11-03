"""Saved eight-legged topology, body plans, eyes, pincers, tail and prior export audit."""
import sys,bpy,bmesh,json,math,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from CreatureBatch24Config import *
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
    pts=[o.matrix_world@v.co for o in parts for v in o.data.vertices]
    low=[min(v[i] for v in pts) for i in range(3)];high=[max(v[i] for v in pts) for i in range(3)];assert low[2]>=0
    legs=[o for o in parts if o.get('cephalothorax_root')];assert len(legs)==8
    assert {(o['leg_index'],o['leg_side']) for o in legs}=={(i,s) for i in range(4) for s in [-1,1]}
    primary=[o for o in parts if o.get('eye_side') and not o.get('secondary_eye')];assert len(primary)==2
    assert abs(primary[0].location.x-primary[1].location.x)<1e-6 and abs(primary[0].location.y+primary[1].location.y)<1e-6
    assert not any('wing' in o.name or 'web' in o.name or 'aura' in o.name for o in parts)
    if key!='scorpion':
        assert sum(bool(o.get('secondary_eye')) for o in parts)==6
        assert len([o for o in parts if o.get('fang_side')])==2
        assert len([o for o in parts if o.get('pedipalp_side')])==2
        assert len([o for o in parts if o.get('anatomy_role')=='abdomen'])==1
    else:
        segments=[o for o in parts if 'tail_segment' in o];assert len(segments)==5
        assert {o['tail_segment'] for o in segments}==set(range(5))
        assert sum(bool(o.get('telson')) for o in parts)==1
        assert sum(o.get('source_attack')=='AT_STNG/AD_DRST' for o in parts)==1
        fingers=[o for o in parts if o.get('pincer_finger')];assert len(fingers)==4
        assert {(o['pincer_side'],o['pincer_finger']) for o in fingers}=={(s,f) for s in [-1,1] for f in [-1,1]}
        assert len([o for o in parts if 'dorsal_segment' in o])==6
        assert high[2]>.57
    result[key]=dict(parts=len(parts),triangles=sum(sum(len(p.vertices)-2 for p in o.data.polygons) for o in parts),bounds_m=[low,high],closed_geometry=True,paint_valid=True,walking_legs=8,primary_eyes=2,source_sex_shared=True)
assert bpy.data.objects['giant_spider_abdomen'].dimensions.x>bpy.data.objects['cave_spider_abdomen'].dimensions.x*1.7
assert bpy.data.objects['giant_spider_cephalothorax'].dimensions.y>bpy.data.objects['cave_spider_cephalothorax'].dimensions.y*1.6
assert result['giant_spider']['bounds_m'][1][1]>result['cave_spider']['bounds_m'][1][1]*1.5
assert all(tiles[n+',male']==tiles[n+',female'] for n in ['cave spider','giant spider','scorpion'])
protected=json.loads((OUT/'batch24-protected-assets.json').read_text());assert len(protected)==86
assert all(hashlib.sha256((ROOT/n).read_bytes()).hexdigest()==h for n,h in protected.items())
result.update(previous_86_exports_unchanged=True,source_sex_tiles_identical=True,independent_spider_proportions=True,separate_scorpion_body=True)
(OUT/'batch24-mesh-inspection.json').write_text(json.dumps(result,indent=2))
print('CREATURE_BATCH24_NATIVE_CHECK PASS '+json.dumps(result),flush=True)
