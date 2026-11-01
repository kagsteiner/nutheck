"""Saved object geometry, complete solid lids, paint and prior-export validation."""
import bpy,bmesh,json,math,hashlib
from pathlib import Path
from mathutils import Vector
root=Path(__file__).resolve().parents[1];out=root/'Art/ObjectInterpretations'
bpy.ops.wm.open_mainfile(filepath=str(out/'ObjectBatch1.blend'))
for c in bpy.data.collections:c.hide_viewport=False
bpy.context.view_layer.update();result={}
for key in ['large_box','chest','gold_piece']:
    parts=[o for o in bpy.data.objects if o.type=='MESH' and o.get('creature')==key];assert parts
    for o in parts:
        paint=o.data.color_attributes.get('Paint');assert paint and paint.domain=='CORNER' and paint.data_type=='FLOAT_COLOR'
        assert all(math.isfinite(c) for v in o.data.vertices for c in v.co)
        assert all(p.area>1e-12 for p in o.data.polygons),o.name
        bm=bmesh.new();bm.from_mesh(o.data);assert all(e.is_manifold for e in bm.edges),o.name;bm.free()
    points=[o.matrix_world@v.co for o in parts for v in o.data.vertices]
    low=[min(p[i] for p in points) for i in range(3)];high=[max(p[i] for p in points) for i in range(3)]
    assert -.002<low[2]<.003 and high[0]-low[0]<1 and high[1]-low[1]<1
    if key=='gold_piece':assert sum(bool(o.get('coin_disc')) for o in parts)==9
    else:assert any(o.get('lid_part') for o in parts)
    result[key]=dict(parts=len(parts),triangles=sum(sum(len(p.vertices)-2 for p in o.data.polygons) for o in parts),bounds_m=[low,high],paint_valid=True,closed_meshes=True)
assert result['chest']['bounds_m'][1][2]>result['large_box']['bounds_m'][1][2]+.08
protected=json.loads((out/'protected-creature-player-assets.json').read_text());assert len(protected)==41
assert all(hashlib.sha256((root/'Art/CreatureInterpretations'/n).read_bytes()).hexdigest()==h for n,h in protected.items())
result['previous_41_creature_player_exports_unchanged']=True
(out/'object-batch1-inspection.json').write_text(json.dumps(result,indent=2))
print('OBJECT_BATCH1_NATIVE_CHECK PASS '+json.dumps(result),flush=True)
