import bpy,bmesh,math,json,hashlib
from pathlib import Path
r=Path(__file__).resolve().parents[1];out=r/'Art/ObjectInterpretations'
bpy.ops.wm.open_mainfile(filepath=str(out/globals().get('ARMOR_BLEND','ArmorStudy.blend')))
for c in bpy.data.collections:c.hide_viewport=False
bpy.context.view_layer.update();report={}
for key in globals().get('ARMOR_KEYS',['leather_armor','studded_leather_armor','chain_mail','banded_mail','elven_mithril_coat','dwarvish_mithril_coat']):
    parts=[o for o in bpy.data.objects if o.type=='MESH' and o.get('creature')==key];assert parts
    for o in parts:
        a=o.data.color_attributes.get('Paint');assert a and a.domain=='CORNER' and a.data_type=='FLOAT_COLOR'
        assert not o.modifiers and not o.animation_data
        assert all(math.isfinite(c) for v in o.data.vertices for c in v.co)
        assert all(p.area>1e-12 for p in o.data.polygons),o.name
        bm=bmesh.new();bm.from_mesh(o.data);assert all(e.is_manifold for e in bm.edges),o.name;bm.free()
    report[key]=dict(parts=len(parts),triangles=sum(len(p.vertices)-2 for o in parts for p in o.data.polygons),closed_geometry=True,paint_valid=True)
protected=json.loads((out/'armor-study-protected.json').read_text());assert len(protected)==96
assert all(hashlib.sha256((r/n).read_bytes()).hexdigest()==h for n,h in protected.items())
report['previous_96_exports_unchanged']=True
(out/globals().get('ARMOR_REPORT','armor-study-inspection.json')).write_text(json.dumps(report,indent=2));print('ARMOR_STUDY_NATIVE_CHECK PASS '+json.dumps(report))

