"""Inspect saved ancestry, painted state modules, closure and old exports."""
import bpy,bmesh,json,math,hashlib,struct,re
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
root=Path(__file__).resolve().parents[1];out=root/'Art/CreatureInterpretations'
bpy.ops.wm.open_mainfile(filepath=str(out/'CreatureBatch20.blend'))
for c in bpy.data.collections:c.hide_viewport=False
bpy.context.view_layer.update();result={};bodies=[]
def signature(o):return hashlib.sha256(b''.join(struct.pack('<3f',*v.co) for v in o.data.vertices)).hexdigest()
for key in ['uruk_hai','orc_shaman','orc_captain']:
    parts=[o for o in bpy.data.objects if o.type=='MESH' and o.get('creature')==key];assert parts
    for o in parts:
        paint=o.data.color_attributes.get('Paint');assert paint and paint.domain=='CORNER' and paint.data_type=='FLOAT_COLOR',o.name
        assert all(math.isfinite(c) for v in o.data.vertices for c in v.co)
        assert all(p.area>1e-12 for p in o.data.polygons),o.name
    points=[o.matrix_world@v.co for o in parts for v in o.data.vertices]
    low=[min(v[i] for v in points) for i in range(3)];high=[max(v[i] for v in points) for i in range(3)];assert low[2]>=-.003
    body=bpy.data.objects[key+'_body'];digest=signature(body);bodies.append(digest)
    eyes=sorted([o for o in parts if o.get('eye_side')],key=lambda o:o['eye_side']);assert len(eyes)==2
    a,b=[o.location for o in eyes];assert abs(a.x+b.x)<1e-6 and abs(a.y-b.y)<1e-6 and abs(a.z-b.z)<1e-6
    tree=BVHTree.FromObject(body,bpy.context.evaluated_depsgraph_get());gaps=[tree.find_nearest(body.matrix_world.inverted()@o.location)[3] for o in eyes];assert max(gaps)<.012
    closed=[o for o in parts if any(o.name==key+'_'+n for n in ['tunic','belt','helmet','detachable_shield','detachable_helmet_rim'])]
    for o in closed:
        bm=bmesh.new();bm.from_mesh(o.data);assert all(e.is_manifold for e in bm.edges),o.name;bm.free()
    shield=[o for o in parts if o.get('shield_module')];assert len(shield)==(1 if key=='uruk_hai' else 0)
    if shield:
        paint=shield[0].data.color_attributes['Paint'].data
        assert any(p.color[0]>.4 and p.color[1]<.02 for p in paint)
        assert any(p.color[2]>.3 and p.color[0]>.2 for p in paint)
        shield_tree=BVHTree.FromObject(shield[0],bpy.context.evaluated_depsgraph_get())
        assert shield_tree.find_nearest(Vector((.232,-.140,.548)))[3]<.015
        assert bpy.data.objects.get(key+'_shield_back_grip')
    assert sum(bool(o.get('rank_module')) for o in parts)==(1 if key=='orc_captain' else 0)
    assert bool(bpy.data.objects.get(key+'_held_pale_blade'))==(key=='orc_captain')
    assert not any('shadow' in o.name or 'crown' in o.name or 'magic_effect' in o.name for o in parts)
    result[key]=dict(parts=len(parts),triangles=sum(sum(len(p.vertices)-2 for p in o.data.polygons) for o in parts),bounds_m=[low,high],paint_valid=True,paired_eyes_surface_gaps_m=gaps,body_vertex_hash=digest,closed_state_modules=True,shield_count=len(shield))
with bpy.data.libraries.load(str(out/'CreatureBatch18.blend'),link=False) as (src,dst):dst.objects=['mordor_orc_body']
assert all(h==signature(dst.objects[0]) for h in bodies)
text=(root/'upstream/NetHack/win/share/monsters.txt').read_text(encoding='utf-8')
tiles={name:rows for _,name,rows in re.findall(r'^# tile (\d+) \(([^\n]+)\)\s*\{([^}]+)\}',text,re.M)}
assert all(tiles[n+',male']==tiles[n+',female'] for n in ['Uruk-hai','orc shaman','orc-captain'])
protected=json.loads((out/'batch20-protected-assets.json').read_text(encoding='utf-8'));assert len(protected)==64
assert all(hashlib.sha256((root/n).read_bytes()).hexdigest()==h for n,h in protected.items())
result.update(previous_64_exports_unchanged=True,source_sex_tiles_identical=True,saved_orc_ancestry_exact=True)
(out/'batch20-mesh-inspection.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print('CREATURE_BATCH20_NATIVE_CHECK PASS '+json.dumps(result),flush=True)
