"""Saved closed flight anatomy, wing/leg counts, hover, source and export protection."""
import bpy,bmesh,json,math,hashlib,sys,re
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from CreatureBatch23Config import *
bpy.ops.wm.open_mainfile(filepath=str(OUT/BLEND_NAME))
for c in bpy.data.collections:c.hide_viewport=False
bpy.context.view_layer.update();result={}
for key in GROUPS:
    parts=[o for o in bpy.data.objects if o.type=='MESH' and o.get('creature')==key];assert parts
    for o in parts:
        attr=o.data.color_attributes.get('Paint');assert attr and attr.domain=='CORNER' and attr.data_type=='FLOAT_COLOR',o.name
        assert all(math.isfinite(c) for v in o.data.vertices for c in v.co)
        assert all(p.area>1e-12 for p in o.data.polygons),o.name
        bm=bmesh.new();bm.from_mesh(o.data);assert all(e.is_manifold for e in bm.edges),o.name;bm.free()
        assert not o.animation_data and not o.modifiers,o.name
    pts=[o.matrix_world@v.co for o in parts for v in o.data.vertices]
    low=[min(p[i] for p in pts) for i in range(3)];high=[max(p[i] for p in pts) for i in range(3)];assert low[2]>.12
    legs=[o for o in parts if o.get('thoracic_root')];assert {(o['leg_index'],o['leg_side']) for o in legs}=={(i,s) for i in range(3) for s in [-1,1]}
    eyes=[o for o in parts if o.get('eye_side')];assert len(eyes)==2
    wings=[o for o in parts if o.get('insect_wing')];assert len(wings)==(2 if key=='xan' else 4)
    assert all(o['closed_thickness_m']>=.003 for o in wings)
    for pair in range(1 if key=='xan' else 2):
        a,b=sorted([o for o in wings if o['wing_pair']==pair],key=lambda o:o['wing_side'])
        for field in ['wing_root','wing_tip']:
            va,vb=a[field],b[field];assert abs(va[0]-vb[0])<1e-6 and abs(va[1]+vb[1])<1e-6 and abs(va[2]-vb[2])<1e-6
    if key!='xan':
        thorax=next(o for o in parts if o.get('fur_surface'));assert thorax.data.uv_layers.get('FurFlow')
        assert all(m.name.startswith('Fur_') for m in thorax.data.materials)
        abdomen=next(o for o in parts if o.get('striped_abdomen'));colors=abdomen.data.color_attributes['Paint'].data
        assert max(v.color[0] for v in colors)>.6 and min(v.color[0] for v in colors)<.08
        assert len([o for o in parts if o.get('source_attack')=='AT_STNG/AD_DRST'])==1
    else:
        assert len([o for o in parts if o.get('mosquito_abdomen')])==1
        assert len([o for o in parts if o.get('source_attack')=='AT_STNG/AD_LEGS'])==1
        assert not any(o.get('striped_abdomen') or o.get('fur_surface') for o in parts)
    result[key]=dict(parts=len(parts),triangles=sum(sum(len(p.vertices)-2 for p in o.data.polygons) for o in parts),bounds_m=[low,high],closed_surfaces=True,paint_valid=True,thoracic_legs=6,paired_eyes=True,wing_count=len(wings),hover_clearance_m=low[2])
assert bpy.data.objects['queen_bee_abdomen'].dimensions.x>bpy.data.objects['killer_bee_abdomen'].dimensions.x*1.25
assert bpy.data.objects['queen_bee_thorax'].dimensions.x>bpy.data.objects['killer_bee_thorax'].dimensions.x*1.1
assert all(tiles[n+',male']==tiles[n+',female'] for n in ['killer bee','queen bee','xan'])
protected=json.loads((OUT/'batch23-protected-assets.json').read_text());assert len(protected)==83
assert all(hashlib.sha256((ROOT/n).read_bytes()).hexdigest()==h for n,h in protected.items())
result.update(previous_83_exports_unchanged=True,source_sex_tiles_identical=True,independent_queen_proportions=True,separate_xan_body=True)
(OUT/'batch23-mesh-inspection.json').write_text(json.dumps(result,indent=2))
print('CREATURE_BATCH23_NATIVE_CHECK PASS '+json.dumps(result),flush=True)
