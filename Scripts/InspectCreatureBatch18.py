"""Inspect saved orc paint/geometry, shared ancestry and protected exports."""
import bpy,bmesh,json,math,hashlib,struct,re
from pathlib import Path
from mathutils.bvhtree import BVHTree
root=Path(__file__).resolve().parents[1];out=root/'Art/CreatureInterpretations'
bpy.ops.wm.open_mainfile(filepath=str(out/'CreatureBatch18.blend'))
for c in bpy.data.collections:c.hide_viewport=False
bpy.context.view_layer.update();result={};bodies=[];reused={}
def signature(o):return hashlib.sha256(b''.join(struct.pack('<3f',*v.co) for v in o.data.vertices)).hexdigest()
for key in ['hobgoblin','hill_orc','mordor_orc']:
    parts=[o for o in bpy.data.objects if o.type=='MESH' and o.get('creature')==key];assert parts
    for o in parts:
        paint=o.data.color_attributes.get('Paint');assert paint and paint.domain=='CORNER' and paint.data_type=='FLOAT_COLOR',o.name
        assert all(math.isfinite(c) for v in o.data.vertices for c in v.co)
        assert all(p.area>1e-12 for p in o.data.polygons),o.name
    points=[o.matrix_world@v.co for o in parts for v in o.data.vertices]
    low=[min(v[i] for v in points) for i in range(3)];high=[max(v[i] for v in points) for i in range(3)]
    assert low[2]>=-.003,(key,low)
    if key=='hobgoblin':
        reused={o['source_family_object']:signature(o) for o in parts};assert len(reused)==len(parts)
        irises=[o for o in parts if 'green_iris' in o.name];assert len(irises)==2
        assert all(sum(p.color[0] for p in o.data.color_attributes['Paint'].data)>sum(p.color[2] for p in o.data.color_attributes['Paint'].data)*10 for o in irises)
        assert all(abs(o.scale.z-1.10)<1e-5 for o in parts)
        eye_gaps=[];digest=signature(bpy.data.objects[key+'_sculpted_head'])
    else:
        body=bpy.data.objects[key+'_body'];digest=signature(body);bodies.append(digest)
        eyes=sorted([o for o in parts if o.get('eye_side')],key=lambda o:o['eye_side']);assert len(eyes)==2
        a,b=[o.location for o in eyes];assert abs(a.x+b.x)<1e-6 and abs(a.y-b.y)<1e-6 and abs(a.z-b.z)<1e-6
        tree=BVHTree.FromObject(body,bpy.context.evaluated_depsgraph_get());eye_gaps=[tree.find_nearest(body.matrix_world.inverted()@o.location)[3] for o in eyes];assert max(eye_gaps)<.012,(key,eye_gaps)
        for suffix in ['tunic','belt','helmet']:
            bm=bmesh.new();bm.from_mesh(bpy.data.objects[key+'_'+suffix].data);assert all(e.is_manifold for e in bm.edges),(key,suffix);bm.free()
        assert sum(bool(o.get('equipment_module')) for o in parts)==3
    assert not any('shadow' in o.name or 'crown' in o.name for o in parts)
    result[key]=dict(parts=len(parts),triangles=sum(sum(len(p.vertices)-2 for p in o.data.polygons) for o in parts),bounds_m=[low,high],paint_valid=True,eye_surface_distances_m=eye_gaps,body_vertex_hash=digest)
assert len(set(bodies))==1
requested=list(reused)
with bpy.data.libraries.load(str(out/'CreatureInterpretations.blend'),link=False) as (src,dst):dst.objects=list(requested)
assert all(signature(o)==reused[name] for name,o in zip(requested,dst.objects))
text=(root/'upstream/NetHack/win/share/monsters.txt').read_text(encoding='utf-8')
tiles={name:rows for _,name,rows in re.findall(r'^# tile (\d+) \(([^\n]+)\)\s*\{([^}]+)\}',text,re.M)}
assert all(tiles[n+',male']==tiles[n+',female'] for n in ['hobgoblin','hill orc','Mordor orc'])
protected=json.loads((out/'batch18-protected-assets.json').read_text(encoding='utf-8'));assert len(protected)==58
assert all(hashlib.sha256((root/n).read_bytes()).hexdigest()==h for n,h in protected.items())
result.update(previous_58_exports_unchanged=True,source_sex_tiles_identical=True,upright_orc_ancestry_exact=True,hobgoblin_saved_local_geometry_exact=True)
(out/'batch18-mesh-inspection.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print('CREATURE_BATCH18_NATIVE_CHECK PASS '+json.dumps(result),flush=True)
