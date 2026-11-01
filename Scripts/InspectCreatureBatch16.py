"""Inspect saved dwarf geometry/paint, identical ancestry and preceding exports."""
import bpy,bmesh,json,math,hashlib,struct,re
from pathlib import Path
from mathutils.bvhtree import BVHTree
out=Path(__file__).resolve().parents[1]/'Art/CreatureInterpretations'
bpy.ops.wm.open_mainfile(filepath=str(out/'CreatureBatch16.blend'))
for c in bpy.data.collections:c.hide_viewport=False
bpy.context.view_layer.update();result={};bodies=[]
for key in ['dwarf','dwarf_leader','dwarf_ruler']:
    parts=[o for o in bpy.data.objects if o.type=='MESH' and o.get('creature')==key];assert parts
    for o in parts:
        paint=o.data.color_attributes.get('Paint');assert paint and paint.domain=='CORNER' and paint.data_type=='FLOAT_COLOR',o.name
        assert all(math.isfinite(c) for v in o.data.vertices for c in v.co)
        assert all(p.area>1e-12 for p in o.data.polygons),o.name
    points=[o.matrix_world@v.co for o in parts for v in o.data.vertices]
    low=[min(v[i] for v in points) for i in range(3)];high=[max(v[i] for v in points) for i in range(3)]
    assert low[2]>=-.003,(key,low)
    body=bpy.data.objects[key+'_body'];digest=hashlib.sha256(b''.join(struct.pack('<3f',*v.co) for v in body.data.vertices)).hexdigest();bodies.append(digest)
    eyes=sorted([o for o in parts if o.get('eye_side')],key=lambda o:o['eye_side']);assert len(eyes)==2
    a,b=[o.location for o in eyes];assert abs(a.x+b.x)<1e-6 and abs(a.y-b.y)<1e-6 and abs(a.z-b.z)<1e-6
    tree=BVHTree.FromObject(body,bpy.context.evaluated_depsgraph_get());gaps=[tree.find_nearest(body.matrix_world.inverted()@o.location)[3] for o in eyes]
    assert max(gaps)<.012,(key,gaps)
    modules=[o for o in parts if o.get('rank_module')];assert bool(modules)==(key!='dwarf')
    if key=='dwarf_ruler':
        band=bpy.data.objects[key+'_detachable_gold_band'];band_tree=BVHTree.FromObject(band,bpy.context.evaluated_depsgraph_get())
        inlays=[o for o in parts if 'orange_inlay' in o.name];assert len(inlays)==2
        assert all(band_tree.find_nearest(band.matrix_world.inverted()@o.location)[3]<.010 for o in inlays)
    assert sum(bool(o.get('pointed_cap')) for o in parts)==(0 if key=='dwarf_ruler' else 1)
    assert len([o for o in parts if o.get('beard_module')])==1
    assert not any('weapon' in o.name or 'axe' in o.name or 'shadow' in o.name for o in parts)
    shirt=bpy.data.objects[key+'_blue_tunic'];topo=bmesh.new();topo.from_mesh(shirt.data);assert all(e.is_manifold for e in topo.edges);topo.free()
    result[key]=dict(parts=len(parts),triangles=sum(sum(len(p.vertices)-2 for p in o.data.polygons) for o in parts),bounds_m=[low,high],paint_valid=True,eye_center_surface_distances_m=gaps,rank_modules=len(modules),body_vertex_hash=digest,closed_tunic=True)
assert len(set(bodies))==1
text=(out.parents[1]/'upstream/NetHack/win/share/monsters.txt').read_text()
tiles={name:rows for _,name,rows in re.findall(r'^# tile (\d+) \(([^\n]+)\)\s*\{([^}]+)\}',text,re.M)}
assert all(tiles[n+',male']==tiles[n+',female'] for n in ['dwarf','dwarf leader','dwarf ruler'])
protected=json.loads((out/'batch16-protected-assets.json').read_text());assert len(protected)==49
assert all(hashlib.sha256((out/n).read_bytes()).hexdigest()==h for n,h in protected.items())
result['previous_49_exports_unchanged']=True;result['source_sex_tiles_identical']=True;result['shared_ancestry_exact']=True
(out/'batch16-mesh-inspection.json').write_text(json.dumps(result,indent=2))
print('CREATURE_BATCH16_NATIVE_CHECK PASS '+json.dumps(result),flush=True)
