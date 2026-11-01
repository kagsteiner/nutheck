"""Saved geometry/paint/UV/eye checks, independent age proportions and prior-asset protection."""
import bpy,json,math,hashlib
from pathlib import Path
from mathutils import Vector
out=Path(__file__).resolve().parents[1]/'Art/CreatureInterpretations'
bpy.ops.wm.open_mainfile(filepath=str(out/'CreatureBatch10.blend'))
for col in bpy.data.collections:col.hide_viewport=False
for obj in bpy.data.objects:obj.hide_viewport=False
bpy.context.view_layer.update()
result={}
for key in ['tiger','hell_hound_pup','hell_hound']:
    parts=[o for o in bpy.data.objects if o.type=='MESH' and o.get('creature')==key]
    assert parts,key
    for obj in parts:
        paint=obj.data.color_attributes.get('Paint')
        assert paint and paint.domain=='CORNER' and paint.data_type=='FLOAT_COLOR',obj.name
        assert all(all(math.isfinite(c) for c in v.co) for v in obj.data.vertices)
        if obj.get('fur_surface'):
            assert obj.data.uv_layers.get('FurFlow'),obj.name
            assert all(m.name.startswith('Fur_') for m in obj.data.materials)
    body=bpy.data.objects[key+'_continuous_anatomy']
    points=[o.matrix_world@Vector(c) for o in parts for c in o.bound_box]
    low=[min(p[i] for p in points) for i in range(3)];high=[max(p[i] for p in points) for i in range(3)]
    assert low[2]>=-.003,(key,low)
    eyes=sorted([o for o in parts if o.get('eye_center') is not None],key=lambda o:o['eye_side'])
    assert len(eyes)==2
    a,b=[Vector(o['eye_center']) for o in eyes]
    assert abs(a.x-b.x)<.001 and abs(a.z-b.z)<.001 and abs(a.y+b.y)<.001,(key,a,b)
    assert all(o.get('eye_surface_conforming') for o in eyes)
    result[key]=dict(parts=len(parts),triangles=sum(sum(len(p.vertices)-2 for p in o.data.polygons) for o in parts),
        bounds_m=[low,high],paint_valid=True,fur_uv_valid=True,eye_symmetry_valid=True,eye_surface_conforming=True,
        eye_centers_m=[list(a),list(b)],body_length=body['body_length'],body_width=body['body_width'],
        head_to_body_length=body['head_to_body_length'],head_length=body['head_length'],leg_height=body['leg_height'])
    if key=='tiger':
        regions={name:[0,0] for name in ['spine','left_flank','right_flank']}
        colors=body.data.color_attributes['Paint'].data
        for loop in body.data.loops:
            p=body.matrix_world@body.data.vertices[loop.vertex_index].co
            if -.24<p.x<.25 and p.z>body['body_center_z']-.05:
                name='spine' if p.z>body['body_center_z']+.12 else 'left_flank' if p.y<0 else 'right_flank'
                regions[name][0]+=1;regions[name][1]+=max(colors[loop.index].color[:3])<.06
        assert all(total>100 and dark>100 and .08<dark/total<.7 for total,dark in regions.values()),regions
        assert not any('stripe' in o.name or 'spot' in o.name for o in parts)
        result[key].update(stripe_region_corners=regions,stripes_paint_only=True)
    else:
        assert len([o for o in parts if o.name.startswith(key+'_upper_canine')])==4
        assert body.get('breath_effect_hook')
        result[key].update(muzzle_length=body['muzzle_length'],breath_effect_hook=list(body['breath_effect_hook']))
pup=result['hell_hound_pup'];adult=result['hell_hound']
assert pup['head_to_body_length']>adult['head_to_body_length']*1.15
assert pup['muzzle_length']/pup['head_length']<adult['muzzle_length']/adult['head_length']*.85
assert pup['leg_height']/pup['body_length']<adult['leg_height']/adult['body_length']*.95
assert adult['body_length']>pup['body_length'] and adult['body_width']>pup['body_width']
protected=json.loads((out/'batch10-protected-assets.json').read_text())
assert len(protected)==27,len(protected)
assert all(hashlib.sha256((out/name).read_bytes()).hexdigest()==digest for name,digest in protected.items())
result['previous_27_exports_unchanged']=True
(out/'batch10-mesh-inspection.json').write_text(json.dumps(result,indent=2))
print('CREATURE_BATCH10_NATIVE_CHECK PASS '+json.dumps(result),flush=True)
