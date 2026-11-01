"""Verify wrapping coverage and unchanged approved cats after the reference repaint."""
import bpy,json,hashlib
from pathlib import Path
from array import array
out=Path(__file__).resolve().parents[1]/'Art/CreatureInterpretations'
bpy.ops.wm.open_mainfile(filepath=str(out/'CreatureBatch9.blend'))
for col in bpy.data.collections:col.hide_viewport=False
for obj in bpy.data.objects:obj.hide_viewport=False
bpy.context.view_layer.update()
report=json.loads((out/'jaguar-reference-repaint.json').read_text())
def signature(key):
    digest=hashlib.sha256()
    for obj in sorted([o for o in bpy.data.objects if o.type=='MESH' and o.get('creature')==key],key=lambda o:o.name):
        digest.update(obj.name.encode());digest.update(str(list(obj.matrix_world)).encode())
        for collection,prop,n in [(obj.data.vertices,'co',3),(obj.data.color_attributes['Paint'].data,'color',4)]:
            values=array('f',[0])*(len(collection)*n);collection.foreach_get(prop,values);digest.update(values.tobytes())
    return digest.hexdigest()
for key,item in report['protected'].items():
    assert signature(key)==item['mesh_paint'],key
    assert hashlib.sha256((out/(key+'.fbx')).read_bytes()).hexdigest()==item['fbx'],key
body=bpy.data.objects['jaguar_continuous_anatomy'];paint=body.data.color_attributes['Paint']
regions={key:dict(corners=0,dark=0) for key in ['spine','left_flank','right_flank','head','legs']}
for loop in body.data.loops:
    p=body.matrix_world@body.data.vertices[loop.vertex_index].co
    names=[]
    if abs(p.y)<.055 and p.z>.52 and -.15<p.x<.23:names.append('spine')
    if p.y<-.09 and p.z>.33 and -.20<p.x<.23:names.append('left_flank')
    if p.y>.09 and p.z>.33 and -.20<p.x<.23:names.append('right_flank')
    if p.x<-.22 and p.z>.40:names.append('head')
    if p.z<.22:names.append('legs')
    for key in names:
        regions[key]['corners']+=1
        regions[key]['dark']+=int(max(paint.data[loop.index].color[:3])<.14)
assert all(v['dark']>30 for v in regions.values()),regions
assert report['geometry_unchanged']
(out/'jaguar-reference-inspection.json').write_text(json.dumps(dict(regions=regions,approved_cats_unchanged=True,geometry_unchanged=True),indent=2))
print('JAGUAR_REFERENCE_CHECK PASS '+json.dumps(regions),flush=True)
