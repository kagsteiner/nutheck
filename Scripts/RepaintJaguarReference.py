"""Repaint only the saved jaguar from user reference; preserve other meshes exactly."""
import sys,hashlib,json
from pathlib import Path
from array import array
sys.path.insert(0,str(Path(__file__).resolve().parent))
from CreatureGeometry import *
from JaguarCoat import jaguar_pigment
bpy.ops.wm.open_mainfile(filepath=str(OUT/'CreatureBatch9.blend'))
for col in bpy.data.collections:col.hide_viewport=False
for obj in bpy.data.objects:obj.hide_viewport=False
bpy.context.view_layer.update()
def signature(key):
    digest=hashlib.sha256()
    for obj in sorted([o for o in bpy.data.objects if o.type=='MESH' and o.get('creature')==key],key=lambda o:o.name):
        digest.update(obj.name.encode());digest.update(str(list(obj.matrix_world)).encode())
        for collection,prop,n in [(obj.data.vertices,'co',3),(obj.data.color_attributes['Paint'].data,'color',4)]:
            values=array('f',[0])*(len(collection)*n);collection.foreach_get(prop,values);digest.update(values.tobytes())
    return digest.hexdigest()
protected={key:dict(mesh_paint=signature(key),fbx=hashlib.sha256((OUT/(key+'.fbx')).read_bytes()).hexdigest()) for key in ['lynx','panther']}
geometry_before={o.name:tuple(tuple(v.co) for v in o.data.vertices) for o in bpy.data.objects if o.type=='MESH' and o.get('creature')=='jaguar'}
stats={}
for obj in bpy.data.objects:
    if obj.type!='MESH' or obj.get('creature')!='jaguar':continue
    if not (obj.get('coat_marking') in {'jaguar_rosettes','jaguar_tail'} or obj.get('pigment') in {'jaguar_gold','jaguar_muzzle'}):continue
    mesh=obj.data;paint=mesh.color_attributes['Paint']
    lo=min(v.co.z for v in mesh.vertices);hi=max(v.co.z for v in mesh.vertices)
    for loop in mesh.loops:
        v=mesh.vertices[loop.vertex_index];p=obj.matrix_world@v.co
        color=jaguar_pigment(obj,p)
        shade=.88+.10*(v.co.z-lo)/max(.01,hi-lo)
        paint.data[loop.index].color=(*(c*shade for c in color),1)
    stats[obj.name]=dict(corners=len(paint.data),dark_corners=sum(max(c.color[:3])<.10 for c in paint.data))
for name,coords in geometry_before.items():assert coords==tuple(tuple(v.co) for v in bpy.data.objects[name].data.vertices),name
bpy.ops.object.select_all(action='DESELECT')
parts=[o for o in bpy.data.objects if o.type=='MESH' and o.get('creature')=='jaguar']
for obj in parts:obj.hide_render=False;obj.select_set(True)
bpy.context.view_layer.objects.active=parts[0]
bpy.ops.export_scene.fbx(filepath=str(OUT/'jaguar.fbx'),use_selection=True,object_types={'MESH'},apply_unit_scale=True,
    axis_forward='-Y',axis_up='Z',add_leaf_bones=False,bake_anim=False,mesh_smooth_type='FACE')
for key,values in protected.items():
    assert signature(key)==values['mesh_paint'],key
    assert hashlib.sha256((OUT/(key+'.fbx')).read_bytes()).hexdigest()==values['fbx'],key
for key in ['jaguar','lynx','panther']:
    bpy.data.collections[key].hide_viewport=key!='jaguar'
    for obj in bpy.data.objects:
        if obj.get('creature')==key:obj.hide_render=key!='jaguar'
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'CreatureBatch9.blend'))
(OUT/'jaguar-reference-repaint.json').write_text(json.dumps(dict(geometry_unchanged=True,protected=protected,paint=stats),indent=2))
print('JAGUAR_REFERENCE_REPAINT PASS geometry_unchanged=True lynx_panther_unchanged=True '+json.dumps(stats),flush=True)
