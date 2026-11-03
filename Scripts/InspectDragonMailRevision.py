import sys,bpy,bmesh,json,hashlib,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from ArmorBatch2Config import *
bpy.ops.wm.open_mainfile(filepath=str(OUT/'ArmorBatch2.blend'))
for c in bpy.data.collections:c.hide_viewport=False
bpy.context.view_layer.update();report={}
for key in GROUPS[3:]:
    parts=[o for o in bpy.data.objects if o.type=='MESH' and o.get('creature')==key];assert parts
    for o in parts:
        a=o.data.color_attributes.get('Paint');assert a and a.domain=='CORNER' and a.data_type=='FLOAT_COLOR',o.name
        assert not o.modifiers and not o.animation_data
        assert all(math.isfinite(c) for v in o.data.vertices for c in v.co)
        assert all(p.area>1e-12 for p in o.data.polygons),o.name
        bm=bmesh.new();bm.from_mesh(o.data);assert all(e.is_manifold for e in bm.edges),o.name;bm.free()
    body=next(o for o in parts if 'fine_overlapping_leaf_scales' in o.name)
    assert body['leaf_scale_count']>850
    assert len([o for o in parts if 'curved_pauldron_lame' in o.name])==6
    assert not any(any(s in o.name for s in ['great_chest_scute','gray_pectoral','gray_crown_scute','layered_dragon_pauldron','shoulder_horn']) for o in parts)
    pts=[o.matrix_world@v.co for o in parts for v in o.data.vertices];assert min(p.z for p in pts)>0
    report[key]=dict(parts=len(parts),triangles=sum(len(p.vertices)-2 for o in parts for p in o.data.polygons),body_leaf_scales=body['leaf_scale_count'],total_leaf_scales=sum(o.get('leaf_scale_count',0) for o in parts),curved_shoulder_lames=6,closed_geometry=True,paint_valid=True,large_slabs_removed=True)
protected=json.loads((OUT/'dragon-mail-revision-protected.json').read_text());assert len(protected)==107
assert all(hashlib.sha256((ROOT/n).read_bytes()).hexdigest()==h for n,h in protected.items())
# Exact previous plate geometry and corner paint, not just unchanged FBX files.
def plate_signature():
    result={}
    for o in bpy.data.objects:
        if o.type!='MESH' or o.get('creature') not in GROUPS[:3]:continue
        result[o.name]=dict(vertices=[tuple(v.co) for v in o.data.vertices],faces=[tuple(p.vertices) for p in o.data.polygons],paint=[tuple(c.color) for c in o.data.color_attributes['Paint'].data])
    return hashlib.sha256(json.dumps(result,sort_keys=True).encode()).hexdigest()
current=plate_signature();bpy.ops.wm.open_mainfile(filepath=str(OUT/'DragonMail-v1/ArmorBatch2.blend'));assert plate_signature()==current
report.update(previous_107_exports_unchanged=True,plate_geometry_and_paint_unchanged=True)
(OUT/'dragon-mail-revision-inspection.json').write_text(json.dumps(report,indent=2));print('DRAGON_MAIL_REVISION_NATIVE_CHECK PASS '+json.dumps(report))
