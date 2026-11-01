"""Saved feline paint, fur UVs, paired eyes and distinct anatomy checks."""
import bpy,json,math
from pathlib import Path
from mathutils import Vector
out=Path(__file__).resolve().parents[1]/'Art/CreatureInterpretations'
bpy.ops.wm.open_mainfile(filepath=str(out/'CreatureBatch9.blend'))
for col in bpy.data.collections:col.hide_viewport=False
for obj in bpy.data.objects:obj.hide_viewport=False
bpy.context.view_layer.update()
result={}
for key in ['jaguar','lynx','panther']:
    parts=[o for o in bpy.data.objects if o.type=='MESH' and o.get('creature')==key]
    assert parts,key
    for obj in parts:
        paint=obj.data.color_attributes.get('Paint')
        assert paint and paint.domain=='CORNER' and paint.data_type=='FLOAT_COLOR',obj.name
        assert all(all(math.isfinite(c) for c in v.co) for v in obj.data.vertices)
        if obj.get('fur_surface'):
            assert obj.data.uv_layers.get('FurFlow')
            assert all(m.name.startswith('Fur_') for m in obj.data.materials)
    body=bpy.data.objects[key+'_continuous_anatomy']
    points=[o.matrix_world@Vector(c) for o in parts for c in o.bound_box]
    low=[min(p[i] for p in points) for i in range(3)];high=[max(p[i] for p in points) for i in range(3)]
    assert low[2]>=-.003,(key,low)
    eyes=sorted([o for o in parts if o.get('eye_center') is not None],key=lambda o:o['eye_side'])
    assert len(eyes)==2
    a,b=[Vector(o['eye_center']) for o in eyes]
    assert abs(a.x-b.x)<.001 and abs(a.z-b.z)<.001 and abs(a.y+b.y)<.001,(key,a,b)
    tail=next(o for o in parts if o.get('tail_form'))
    result[key]=dict(parts=len(parts),triangles=sum(sum(len(p.vertices)-2 for p in o.data.polygons) for o in parts),
        bounds_m=[low,high],paint_valid=True,fur_uv_valid=True,eye_symmetry_valid=True,
        eye_centers_m=[list(a),list(b)],body_length=body['body_length'],body_width=body['body_width'],
        head_to_body_length=body['head_to_body_length'],paw_ratio=body['paw_length']/body['body_length'],tail_form=tail['tail_form'])
    paint=body.data.color_attributes['Paint'].data
    if key=='jaguar':
        dark=sum(c.color[0]<.13 for c in paint);gold=sum(c.color[0]>.35 for c in paint)
        assert dark>100 and gold>100
        assert not any('rosette' in o.name or 'spot' in o.name for o in parts)
        result[key].update(dark_paint_corners=dark,gold_paint_corners=gold,rosettes_paint_only=True)
    if key=='lynx':
        tufts=[o for o in parts if o.name.startswith('lynx_ear_tuft')]
        ears=[o for o in parts if o.name.startswith('lynx_pointed_ear')]
        assert len(tufts)==len(ears)==2
        assert not any('cheek_ruff' in o.name for o in parts)
        for tuft in tufts:
            side=1 if sum((tuft.matrix_world@v.co).y for v in tuft.data.vertices)>0 else -1
            ear=next(o for o in ears if (1 if o.location.y+sum(v.co.y for v in o.data.vertices)/len(o.data.vertices)>0 else -1)==side)
            assert min((tuft.matrix_world@v.co).z for v in tuft.data.vertices)<max((ear.matrix_world@v.co).z for v in ear.data.vertices)
        assert any(c.color[0]<.04 for c in tail.data.color_attributes['Paint'].data)
        result[key].update(cheeks_paint_only=True,tuft_bounds_overlap_ears=True)
    if key=='panther':
        assert max(c.color[2] for c in paint)<.06
        result[key]['no_bright_blue_coat']=True
assert result['jaguar']['body_width']>result['panther']['body_width']
assert result['panther']['body_length']>result['jaguar']['body_length']
assert result['lynx']['paw_ratio']>result['jaguar']['paw_ratio']
assert result['lynx']['tail_form']=='bobbed' and result['panther']['tail_form']=='raised_long'
(out/'batch9-mesh-inspection.json').write_text(json.dumps(result,indent=2))
print('CREATURE_BATCH9_NATIVE_CHECK PASS '+json.dumps(result),flush=True)
