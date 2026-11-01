"""Saved unicorn paint/eyes/hooves/horn attachment and protected prior exports."""
import bpy,bmesh,json,math,hashlib,struct
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
out=Path(__file__).resolve().parents[1]/'Art/CreatureInterpretations'
bpy.ops.wm.open_mainfile(filepath=str(out/'CreatureBatch12.blend'))
for col in bpy.data.collections:col.hide_viewport=False
for obj in bpy.data.objects:obj.hide_viewport=False
bpy.context.view_layer.update();result={};body_hashes=[];body_brightness=[]
for key in ['white_unicorn','gray_unicorn','black_unicorn']:
    parts=[o for o in bpy.data.objects if o.type=='MESH' and o.get('creature')==key];assert parts
    for obj in parts:
        paint=obj.data.color_attributes.get('Paint')
        assert paint and paint.domain=='CORNER' and paint.data_type=='FLOAT_COLOR',obj.name
        assert all(all(math.isfinite(c) for c in v.co) for v in obj.data.vertices)
        if obj.get('fur_surface'):
            assert obj.data.uv_layers.get('FurFlow'),obj.name
            assert all(m.name.startswith('Fur_') for m in obj.data.materials)
    body=bpy.data.objects[key+'_continuous_anatomy'];points=[o.matrix_world@Vector(c) for o in parts for c in o.bound_box]
    low=[min(p[i] for p in points) for i in range(3)];high=[max(p[i] for p in points) for i in range(3)];assert low[2]>=-.003
    hooves=[o for o in parts if o.get('single_hoof')];assert len(hooves)==4
    centers=[sum((o.matrix_world@v.co for v in o.data.vertices),Vector())/len(o.data.vertices) for o in hooves]
    assert sum(p.x<0 for p in centers)==sum(p.x>0 for p in centers)==2
    assert sum(p.y<0 for p in centers)==sum(p.y>0 for p in centers)==2
    eyes=sorted([o for o in parts if o.get('eye_center') is not None],key=lambda o:o['eye_side']);assert len(eyes)==2
    a,b=[Vector(o['eye_center']) for o in eyes]
    assert abs(a.x-b.x)<.001 and abs(a.z-b.z)<.001 and abs(a.y+b.y)<.001
    assert all(o.get('eye_surface_conforming') and abs(o['gaze_normal'][1])>.90 for o in eyes)
    assert len([o for o in parts if o.name.startswith(key+'_horizontal_pupil')])==2
    expected={'white_unicorn':'equine_blue','gray_unicorn':'unicorn_green','black_unicorn':'unicorn_red'}[key]
    assert all(o['pigment']==expected for o in eyes)
    ears=[o for o in parts if o.get('ear_base') is not None];linings=[o for o in parts if o.get('ear_surface_conforming')];assert len(ears)==len(linings)==2
    gaps=[]
    for lining in linings:
        side=1 if sum(v.co.y for v in lining.data.vertices)>0 else -1;outer=next(o for o in ears if o['ear_side']==side)
        tree=BVHTree.FromObject(outer,bpy.context.evaluated_depsgraph_get())
        gap=max(tree.find_nearest(lining.matrix_world@v.co)[3] for v in lining.data.vertices);assert gap<.002;gaps.append(gap)
    assert next(o for o in parts if o.get('mane_mass')).get('mane_fitted_to_neck')
    tail=next(o for o in parts if o.get('tail_form'))
    assert tail['pigment']=='unicorn_'+key.split('_')[0]+'_tail'
    horns=[o for o in parts if o.get('unicorn_horn')];assert len(horns)==1
    horn=horns[0];topology=bmesh.new();topology.from_mesh(horn.data)
    assert all(e.is_manifold for e in topology.edges) and all(f.calc_area()>1e-12 for f in topology.faces);topology.free()
    root=Vector(horn['horn_root']);axis=Vector(horn['horn_axis']);assert abs(root.y)<.0001 and axis.x<-.4 and axis.z>.8
    tree=BVHTree.FromObject(body,bpy.context.evaluated_depsgraph_get());inv=body.matrix_world.inverted()
    hit,normal,face,distance=tree.ray_cast(inv@(root+axis*.04),-axis,.10);assert hit is not None
    depth=(body.matrix_world@hit-root).dot(axis);assert .003<depth<.012,(key,depth)
    assert root.x<body['head_x'] and root.z>body['head_z']
    assert not any(any(w in o.name for w in ['saddle','bridle','armour','wings']) for o in parts)
    digest=hashlib.sha256(b''.join(struct.pack('<3f',*(round(c,6) for c in v.co)) for v in body.data.vertices)).hexdigest();body_hashes.append(digest)
    paint=body.data.color_attributes['Paint'].data;brightness=sum(sum(c.color[:3])/3 for c in paint)/len(paint);body_brightness.append(brightness)
    if key=='black_unicorn':assert max(max(c.color[:3]) for c in paint)<.04 # no blue shadow socks/patches
    result[key]=dict(parts=len(parts),triangles=sum(sum(len(p.vertices)-2 for p in o.data.polygons) for o in parts),bounds_m=[low,high],
        paint_valid=True,fur_uv_valid=True,single_hooves=4,eye_symmetry_valid=True,lateral_eyes=True,iris=expected,eye_centers_m=[list(a),list(b)],
        fitted_ear_max_gaps_m=gaps,horn_manifold=True,horn_root_depth_m=depth,horn_length_m=horn['horn_length'],horn_axis=list(axis),
        source_alignment=body['source_alignment'],body_vertex_hash=digest,body_mean_brightness=brightness)
assert len(set(body_hashes))==1,'compatible source forms should share the same anatomy'
assert body_brightness[0]>body_brightness[1]*1.7 and body_brightness[1]>body_brightness[2]*5
protected=json.loads((out/'batch12-protected-assets.json').read_text());assert len(protected)==33
assert all(hashlib.sha256((out/n).read_bytes()).hexdigest()==h for n,h in protected.items())
result['previous_33_exports_unchanged']=True;result['shared_compatible_anatomy_verified']=True
(out/'batch12-mesh-inspection.json').write_text(json.dumps(result,indent=2))
print('CREATURE_BATCH12_NATIVE_CHECK PASS '+json.dumps(result),flush=True)
