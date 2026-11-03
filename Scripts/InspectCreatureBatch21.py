"""Saved ancestry/wrap/paint checks and protection of earlier canonical exports."""
import bpy,bmesh,json,math,hashlib,struct,re
from pathlib import Path
from mathutils.bvhtree import BVHTree
root=Path(__file__).resolve().parents[1];out=root/'Art/CreatureInterpretations'
bpy.ops.wm.open_mainfile(filepath=str(out/'CreatureBatch21.blend'))
for c in bpy.data.collections:c.hide_viewport=False
bpy.context.view_layer.update();result={};bodies=[]
def signature(o):return hashlib.sha256(b''.join(struct.pack('<3f',*v.co) for v in o.data.vertices)).hexdigest()
for key in ['orc_mummy','orc_zombie']:
    parts=[o for o in bpy.data.objects if o.type=='MESH' and o.get('creature')==key];assert parts
    for o in parts:
        paint=o.data.color_attributes.get('Paint');assert paint and paint.domain=='CORNER' and paint.data_type=='FLOAT_COLOR',o.name
        assert all(math.isfinite(c) for v in o.data.vertices for c in v.co)
        assert all(p.area>1e-12 for p in o.data.polygons),o.name
    points=[o.matrix_world@v.co for o in parts for v in o.data.vertices]
    low=[min(v[i] for v in points) for i in range(3)];high=[max(v[i] for v in points) for i in range(3)];assert low[2]>=-.003
    body=bpy.data.objects[key+'_body'];digest=signature(body);bodies.append(digest)
    tree=BVHTree.FromObject(body,bpy.context.evaluated_depsgraph_get());inv=body.matrix_world.inverted()
    eyes=sorted([o for o in parts if o.get('eye_side')],key=lambda o:o['eye_side']);assert len(eyes)==2
    a,b=[o.location for o in eyes];assert abs(a.x+b.x)<1e-6 and abs(a.y-b.y)<1e-6 and abs(a.z-b.z)<1e-6
    gaps=[tree.find_nearest(inv@o.location)[3] for o in eyes];assert max(gaps)<.012
    wraps=[o for o in parts if o.get('wrap_module')];assert len(wraps)==(12 if key=='orc_mummy' else 0)
    wrap_gaps={}
    for o in wraps:
        bm=bmesh.new();bm.from_mesh(o.data);assert all(e.is_manifold for e in bm.edges),o.name;bm.free()
        gap=max(tree.find_nearest(inv@(o.matrix_world@v.co))[3] for v in o.data.vertices)
        assert gap<(.009 if 'orange_linen' in o.name else .006),(o.name,gap);wrap_gaps[o.name]=gap
    assert not any('held_' in o.name or 'shield' in o.name or 'crown' in o.name for o in parts)
    assert bpy.data.objects.get(key+'_helmet')
    if key=='orc_mummy':
        assert not any(any(s in o.name for s in ['tunic','trouser','fitted_sleeve','belt']) for o in parts)
        assert all(sum(p.color[0] for p in o.data.color_attributes['Paint'].data)>sum(p.color[1] for p in o.data.color_attributes['Paint'].data)*10 for o in eyes)
    else:
        assert sum(bool(o.get('pupil_module')) for o in parts)==2
        assert all(sum(p.color[1] for p in o.data.color_attributes['Paint'].data)>sum(p.color[0] for p in o.data.color_attributes['Paint'].data)*4 for o in eyes)
    result[key]=dict(parts=len(parts),triangles=sum(sum(len(p.vertices)-2 for p in o.data.polygons) for o in parts),bounds_m=[low,high],paint_valid=True,paired_eyes_surface_gaps_m=gaps,body_vertex_hash=digest,wrap_count=len(wraps),wrap_max_surface_gaps_m=wrap_gaps)
with bpy.data.libraries.load(str(out/'CreatureBatch18.blend'),link=False) as (src,dst):dst.objects=['mordor_orc_body']
assert all(h==signature(dst.objects[0]) for h in bodies)
text=(root/'upstream/NetHack/win/share/monsters.txt').read_text(encoding='utf-8')
tiles={name:rows for _,name,rows in re.findall(r'^# tile (\d+) \(([^\n]+)\)\s*\{([^}]+)\}',text,re.M)}
assert all(tiles[n+',male']==tiles[n+',female'] for n in ['orc mummy','orc zombie'])
protected=json.loads((out/'batch21-protected-assets.json').read_text(encoding='utf-8'));assert len(protected)==70
assert all(hashlib.sha256((root/n).read_bytes()).hexdigest()==h for n,h in protected.items())
result.update(previous_70_exports_unchanged=True,source_sex_tiles_identical=True,saved_orc_ancestry_exact=True)
(out/'batch21-mesh-inspection.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print('CREATURE_BATCH21_NATIVE_CHECK PASS '+json.dumps(result),flush=True)
