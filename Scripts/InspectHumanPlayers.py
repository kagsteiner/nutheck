"""Saved fixed icon characters: one mesh each, preserved anatomy/eyes and integral colours."""
import bpy,json,math,hashlib
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
out=Path(__file__).resolve().parents[1]/'Art/CreatureInterpretations'
bpy.ops.wm.open_mainfile(filepath=str(out/'HumanPlayers.blend'))
for c in bpy.data.collections:c.hide_viewport=False
bpy.context.view_layer.update();result={}
for key in ['valkyrie_female_human','barbarian_male_human']:
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
    legwear=[0,0];leg_levels=[set(),set()];brown_low=100
    for face in mesh.polygons:
        mat=mesh.materials[face.material_index]
        if mat.name.startswith('player_'):
            for i in face.vertices:
                p=points[i];brown_low=min(brown_low,p.z)
                if .14<p.z<.70:legwear[0 if p.x<0 else 1]+=1
                if .08<p.z<.81:leg_levels[0 if p.x<0 else 1].add(round(p.z,2))
    if key=='valkyrie_female_human':
        assert min(legwear)>0
        assert all(min(levels)<.13 and max(levels)>.75 and any(.25<z<.34 for z in levels) and any(.42<z<.50 for z in levels) for levels in leg_levels),leg_levels
    else:assert brown_low>.74,brown_low
    result[key]=dict(mesh_objects=1,fixed_icon_costume=True,paint_valid=True,body_connected_components=components,
        triangles=sum(len(p.vertices)-2 for p in mesh.polygons),eye_centers=[list(a),list(b)],fitted_eyes=True,
        integral_legwear_corners=legwear,costume_low_z=brown_low,ancestry=obj['ancestry'],sex=obj['sex'])
protected=json.loads((out/'human-players-protected-assets.json').read_text());assert len(protected)==36
assert all(hashlib.sha256((out/n).read_bytes()).hexdigest()==h for n,h in protected.items())
result['prior_36_exports_unchanged']=True
(out/'human-players-inspection.json').write_text(json.dumps(result,indent=2))
print('HUMAN_PLAYERS_NATIVE_CHECK PASS '+json.dumps(result),flush=True)
