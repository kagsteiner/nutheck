"""Saved equine anatomy, hooves, fitted eyes/ears, independent proportions and export protection."""
import bpy,json,math,hashlib
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
out=Path(__file__).resolve().parents[1]/'Art/CreatureInterpretations'
bpy.ops.wm.open_mainfile(filepath=str(out/'CreatureBatch11.blend'))
for col in bpy.data.collections:col.hide_viewport=False
for obj in bpy.data.objects:obj.hide_viewport=False
bpy.context.view_layer.update();result={}
for key in ['pony','horse','warhorse']:
    parts=[o for o in bpy.data.objects if o.type=='MESH' and o.get('creature')==key]
    assert parts
    for obj in parts:
        paint=obj.data.color_attributes.get('Paint')
        assert paint and paint.domain=='CORNER' and paint.data_type=='FLOAT_COLOR',obj.name
        assert all(all(math.isfinite(c) for c in v.co) for v in obj.data.vertices)
        if obj.get('fur_surface'):
            assert obj.data.uv_layers.get('FurFlow'),obj.name
            assert all(m.name.startswith('Fur_') for m in obj.data.materials)
    body=bpy.data.objects[key+'_continuous_anatomy'];points=[o.matrix_world@Vector(c) for o in parts for c in o.bound_box]
    low=[min(p[i] for p in points) for i in range(3)];high=[max(p[i] for p in points) for i in range(3)]
    assert low[2]>=-.003,(key,low)
    hooves=[o for o in parts if o.get('single_hoof')];assert len(hooves)==4
    centers=[sum((o.matrix_world@v.co for v in o.data.vertices),Vector())/len(o.data.vertices) for o in hooves]
    assert sum(p.x<0 for p in centers)==sum(p.x>0 for p in centers)==2
    assert sum(p.y<0 for p in centers)==sum(p.y>0 for p in centers)==2
    eyes=sorted([o for o in parts if o.get('eye_center') is not None],key=lambda o:o['eye_side']);assert len(eyes)==2
    a,b=[Vector(o['eye_center']) for o in eyes]
    assert abs(a.x-b.x)<.001 and abs(a.z-b.z)<.001 and abs(a.y+b.y)<.001,(key,a,b)
    assert all(o.get('eye_surface_conforming') and abs(o['gaze_normal'][1])>.90 for o in eyes)
    pupils=[o for o in parts if o.name.startswith(key+'_horizontal_pupil')];assert len(pupils)==2
    ears=[o for o in parts if o.get('ear_base') is not None];linings=[o for o in parts if o.get('ear_surface_conforming')];assert len(ears)==len(linings)==2
    ear_gaps=[]
    for lining in linings:
        side=1 if sum(v.co.y for v in lining.data.vertices)>0 else -1
        outer=next(o for o in ears if o['ear_side']==side)
        tree=BVHTree.FromObject(outer,bpy.context.evaluated_depsgraph_get())
        gap=max(tree.find_nearest(lining.matrix_world@v.co)[3] for v in lining.data.vertices)
        assert gap<.002,(lining.name,gap);ear_gaps.append(gap)
    mane=next(o for o in parts if o.get('mane_mass'));assert mane.get('mane_fitted_to_neck')
    tail=next(o for o in parts if o.get('tail_form'));assert tail.get('long_hair_mass')
    assert not any(any(word in o.name for word in ['saddle','bridle','armour','paw','toe_crease']) for o in parts)
    result[key]=dict(parts=len(parts),triangles=sum(sum(len(p.vertices)-2 for p in o.data.polygons) for o in parts),
        bounds_m=[low,high],paint_valid=True,fur_uv_valid=True,eye_symmetry_valid=True,lateral_eyes=True,horizontal_pupils=2,
        eye_centers_m=[list(a),list(b)],single_hooves=4,hoof_centers_m=[list(p) for p in centers],fitted_ear_max_gaps_m=ear_gaps,
        fitted_mane=True,tail_form=tail['tail_form'],body_length=body['body_length'],body_width=body['body_width'],
        head_length=body['head_length'],muzzle_length=body['muzzle_length'],leg_height=body['leg_height'],neck_height=body['neck_height'])
pony=result['pony'];horse=result['horse'];war=result['warhorse']
assert pony['leg_height']/pony['body_length']<horse['leg_height']/horse['body_length']*.93
assert pony['body_width']/pony['body_length']>horse['body_width']/horse['body_length']*1.10
assert pony['muzzle_length']/pony['head_length']<horse['muzzle_length']/horse['head_length']*.85
assert war['body_width']>horse['body_width']*1.2 and war['head_length']>horse['head_length']*1.1
assert war['neck_height']>horse['neck_height']>pony['neck_height']
protected=json.loads((out/'batch11-protected-assets.json').read_text());assert len(protected)==30
assert all(hashlib.sha256((out/n).read_bytes()).hexdigest()==h for n,h in protected.items())
result['previous_30_exports_unchanged']=True
(out/'batch11-mesh-inspection.json').write_text(json.dumps(result,indent=2))
print('CREATURE_BATCH11_NATIVE_CHECK PASS '+json.dumps(result),flush=True)
