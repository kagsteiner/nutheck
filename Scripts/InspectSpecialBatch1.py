"""Saved closed geometry, source-supported anatomy, static water and preservation."""
import bpy,bmesh,math,json,hashlib,sys,re
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from SpecialBatchConfig import *
bpy.ops.wm.open_mainfile(filepath=str(OUT/BLEND_NAME))
for c in bpy.data.collections:c.hide_viewport=False
bpy.context.view_layer.update();report={}
for key in GROUPS:
    parts=[o for o in bpy.data.objects if o.type=='MESH' and o.get('creature')==key];assert parts
    for o in parts:
        paint=o.data.color_attributes.get('Paint');assert paint and paint.domain=='CORNER' and paint.data_type=='FLOAT_COLOR',o.name
        assert all(math.isfinite(c) for v in o.data.vertices for c in v.co)
        assert all(p.area>1e-12 for p in o.data.polygons),o.name
        bm=bmesh.new();bm.from_mesh(o.data);assert all(e.is_manifold for e in bm.edges),o.name;bm.free()
        assert not o.animation_data and not o.modifiers,o.name
    points=[o.matrix_world@v.co for o in parts for v in o.data.vertices]
    low=[min(p[i] for p in points) for i in range(3)];high=[max(p[i] for p in points) for i in range(3)];assert low[2]>=-.002,(key,low)
    if key=='grid_bug':
        assert sum(bool(o.get('leg_tip')) for o in parts)==6
        assert sum(bool(o.get('eye_side')) for o in parts)==2
        assert not any('wing' in o.name for o in parts)
    if key=='corpse':assert sum('bone_shaft' in o.name for o in parts)==4
    if key=='fountain':
        assert sum(bool(o.get('static_water')) for o in parts)==6
        assert sum(bool(o.get('basin')) for o in parts)==1
        assert all(abs(p[i])<.46 for p in points for i in [0,1]);assert .8<high[2]<1.1
    report[key]=dict(parts=len(parts),triangles=sum(sum(len(p.vertices)-2 for p in o.data.polygons) for o in parts),bounds_m=[low,high],closed_geometry=True,paint_valid=True,static=True,fbx=str(EXPORT_PATHS[key].relative_to(ROOT)))
protected=json.loads((OUT/'protected-assets.json').read_text(encoding='utf-8'));assert len(protected)==67
assert all(hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h for p,h in protected.items())
text=(ROOT/'upstream/NetHack/win/share/monsters.txt').read_text(encoding='utf-8')
tiles={name:rows for _,name,rows in re.findall(r'^# tile (\d+) \(([^\n]+)\)\s*\{([^}]+)\}',text,re.M)}
assert tiles['grid bug,male']==tiles['grid bug,female']
records=json.loads((ROOT/'Art/CreatureCatalogue/creatures.json').read_text(encoding='utf-8'))['creatures']
record=next(r for r in records if r['id']=='PM_GRID_BUG');assert not any('M1_FLY' in f for f in record['flags'])
report['grid_bug_source_sex_tiles_identical']=True
report['grid_bug_has_no_native_flight_flag']=True
report['previous_67_exports_unchanged']=True
(OUT/'mesh-inspection.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('SPECIAL_BATCH1_NATIVE_CHECK PASS '+json.dumps(report),flush=True)
