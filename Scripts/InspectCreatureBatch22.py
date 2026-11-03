"""Saved insect topology, source sex variants, segmentation, paint and export audit."""
import bpy,bmesh,json,math,hashlib,re
from pathlib import Path
root=Path(__file__).resolve().parents[1];out=root/'Art/CreatureInterpretations'
bpy.ops.wm.open_mainfile(filepath=str(out/'CreatureBatch22.blend'))
for c in bpy.data.collections:c.hide_viewport=False
bpy.context.view_layer.update();result={}
for key in ['soldier_ant','soldier_ant_female','fire_ant','fire_ant_female','giant_beetle']:
    parts=[o for o in bpy.data.objects if o.type=='MESH' and o.get('creature')==key];assert parts
    for o in parts:
        attr=o.data.color_attributes.get('Paint');assert attr and attr.domain=='CORNER' and attr.data_type=='FLOAT_COLOR',o.name
        assert all(math.isfinite(c) for v in o.data.vertices for c in v.co)
        assert all(p.area>1e-12 for p in o.data.polygons),o.name
        bm=bmesh.new();bm.from_mesh(o.data);assert all(e.is_manifold for e in bm.edges),o.name;bm.free()
    points=[o.matrix_world@v.co for o in parts for v in o.data.vertices]
    low=[min(p[i] for p in points) for i in range(3)];high=[max(p[i] for p in points) for i in range(3)];assert low[2]>=0
    legs=[o for o in parts if o.get('root_thorax')];assert len(legs)==6
    assert {(o['leg_index'],o['leg_side']) for o in legs}=={(i,s) for i in range(3) for s in [-1,1]}
    assert len([o for o in parts if o.get('eye_side')])==2
    assert len([o for o in parts if o.get('mandible_side')])==2
    assert len([o for o in parts if 'antenna_' in o.name])==2
    elytra=[o for o in parts if o.get('closed_elytron')];assert len(elytra)==(2 if key=='giant_beetle' else 0)
    assert not any('wing' in o.name or 'flame' in o.name for o in parts)
    result[key]=dict(parts=len(parts),triangles=sum(sum(len(p.vertices)-2 for p in o.data.polygons) for o in parts),bounds_m=[low,high],closed_surfaces=True,paint_valid=True,thoracic_legs=6,paired_eyes=True,elytra=len(elytra))
for key in ['soldier_ant','fire_ant']:
    a=bpy.data.objects[key+'_thorax'];b=bpy.data.objects[key+'_female_thorax']
    assert b.dimensions.y>a.dimensions.y*1.09 and b.dimensions.x>a.dimensions.x*1.05
    assert result[key+'_female']['bounds_m'][1][1]>result[key]['bounds_m'][1][1]
assert bpy.data.objects['soldier_ant_head'].dimensions.y>bpy.data.objects['fire_ant_head'].dimensions.y*1.2
text=(root/'upstream/NetHack/win/share/monsters.txt').read_text()
tiles={name:rows for _,name,rows in re.findall(r'^# tile (\d+) \(([^\n]+)\)\s*\{([^}]+)\}',text,re.M)}
assert all(tiles[n+',male']!=tiles[n+',female'] for n in ['soldier ant','fire ant'])
assert tiles['giant beetle,male']==tiles['giant beetle,female']
protected=json.loads((out/'batch22-protected-assets.json').read_text());assert len(protected)==72
assert all(hashlib.sha256((root/n).read_bytes()).hexdigest()==h for n,h in protected.items())
result.update(previous_72_exports_unchanged=True,source_sexes_reviewed=True,independent_ant_female_proportions=True,separate_beetle_body=True)
(out/'batch22-mesh-inspection.json').write_text(json.dumps(result,indent=2))
print('CREATURE_BATCH22_NATIVE_CHECK PASS '+json.dumps(result),flush=True)
