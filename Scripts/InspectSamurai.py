"""Saved fixed icon characters: one mesh each, preserved anatomy/eyes and integral colours."""
import bpy,json,math,hashlib
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
out=Path(__file__).resolve().parents[1]/'Art/CreatureInterpretations'
bpy.ops.wm.open_mainfile(filepath=str(out/'Samurai.blend'))
for c in bpy.data.collections:c.hide_viewport=False
bpy.context.view_layer.update();result={}
for key in ['samurai_male_human','samurai_female_human']:
    parts=[o for o in bpy.data.objects if o.type=='MESH' and o.get('creature')==key]
    assert len(parts)==1,(key,len(parts))
    obj=parts[0];assert obj.get('fixed_icon_costume') and not obj.get('role_module')
    mesh=obj.data;paint=mesh.color_attributes.get('Paint');assert paint and paint.domain=='CORNER' and paint.data_type=='FLOAT_COLOR'
    assert all(all(math.isfinite(c) for c in v.co) for v in mesh.vertices)
    index=obj.vertex_groups['anatomy'].index
    indices={v.index for v in mesh.vertices if any(g.group==index and g.weight>.5 for g in v.groups)}
    adjacent={i:set() for i in indices}
    for edge in mesh.edges:
        a,b=edge.vertices
        if a in indices and b in indices:adjacent[a].add(b);adjacent[b].add(a)
    unseen=set(indices);components=0
    while unseen:
        components+=1;todo=[unseen.pop()]
        while todo:
            v=todo.pop()
            for n in adjacent[v]:
                if n in unseen:unseen.remove(n);todo.append(n)
    assert components==1,(key,components)
    points=[obj.matrix_world@v.co for v in mesh.vertices];assert min(p.z for p in points)>=-.003
    eye=list(obj['fitted_eye_centers']);assert len(eye)==6
    a,b=Vector(eye[:3]),Vector(eye[3:]);assert abs(a.x+b.x)<.001 and abs(a.y-b.y)<.001 and abs(a.z-b.z)<.001
    faces=[list(p.vertices) for p in mesh.polygons if all(i in indices for i in p.vertices)]
    tree=BVHTree.FromPolygons(points,faces)
    assert all(tree.find_nearest(p)[3]<.005 for p in [a,b])
    result[key]=dict(mesh_objects=1,fixed_icon_costume=True,paint_valid=True,body_connected_components=components,
        triangles=sum(len(p.vertices)-2 for p in mesh.polygons),eye_centers=[list(a),list(b)],fitted_eyes=True,
        ancestry=obj['ancestry'],sex=obj['sex'])
protected=json.loads((out/'samurai-protected.json').read_text());root=out.parents[1]
assert all(hashlib.sha256((root/n).read_bytes()).hexdigest()==h for n,h in protected.items())
assert result['samurai_female_human']['triangles']!=result['samurai_male_human']['triangles']
result['prior_exports_unchanged']=len(protected)
(out/'samurai-inspection.json').write_text(json.dumps(result,indent=2))
print('SAMURAI_NATIVE_CHECK PASS '+json.dumps(result),flush=True)
