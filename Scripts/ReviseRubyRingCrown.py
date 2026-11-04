"""Replace only the ruby ring in the saved batch; preserve other geometry/paint/exports."""
import bpy,json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1];O=R/'Art/ObjectInterpretations'
def signature(o):
 h=hashlib.sha256();h.update(str([list(row) for row in o.matrix_world]).encode())
 for v in o.data.vertices:h.update(str(tuple(v.co)).encode())
 for p in o.data.polygons:h.update(str(tuple(p.vertices)).encode())
 for c in o.data.color_attributes['Paint'].data:h.update(str(tuple(c.color)).encode())
 return h.hexdigest()
bpy.ops.wm.open_mainfile(filepath=str(O/'AppearanceBatch1.blend'))
baseline={o.name:signature(o) for o in bpy.data.objects if o.type=='MESH' and o.get('creature')!='ruby_ring'}
source=(R/'Scripts/CreateAppearanceBatch1.py').read_text(encoding='utf-8')
source=source.replace("GROUPS=['ruby_ring','spherical_amulet','oak_wand']","GROUPS=['ruby_ring']")
source=source.replace("bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)","""for obj in list(bpy.data.objects):
 if obj.type!='MESH' or obj.get('creature')=='ruby_ring':bpy.data.objects.remove(obj,do_unlink=True)
 else:obj['preserve_paint']=True
old=bpy.data.collections.get('ruby_ring')
if old and not old.objects:bpy.data.collections.remove(old)
""")
source=source.replace('m=bpy.data.materials.new(k)','m=bpy.data.materials.get(k) or bpy.data.materials.new(k)')
start=source.index("g.GROUP='spherical_amulet'");end=source.index('for key in GROUPS:',start);source=source[:start]+source[end:]
# Keep the full batch's original projection report for unrelated models.
old_report=json.loads((O/'projection-report-appearance-batch1.json').read_text())
exec(compile(source,str(R/'Scripts/CreateAppearanceBatch1.py'),'exec'))
current={o.name:signature(o) for o in bpy.data.objects if o.type=='MESH' and o.get('creature')!='ruby_ring'}
assert baseline==current,'Unrelated saved geometry/paint changed'
new_report=json.loads((O/'projection-report-appearance-batch1.json').read_text())
(O/'projection-report-appearance-batch1.json').write_text(json.dumps(new_report+[r for r in old_report if r['key']!='ruby_ring'],indent=2))
protected=json.loads((O/'ring-crown-protected.json').read_text())
assert all(hashlib.sha256((R/p).read_bytes()).hexdigest()==h for p,h in protected.items())
(O/'ring-crown-preservation.json').write_text(json.dumps(dict(status='PASS',protected_exports=len(protected),other_saved_parts=len(baseline),unrelated_geometry_and_paint_unchanged=True),indent=2))
print('RUBY_CROWN_REVISION_PASS',flush=True)
