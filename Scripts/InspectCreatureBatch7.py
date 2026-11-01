"""Native paint/UV/eye checks and exact approved rat-body/paint reuse evidence."""
import bpy,json,math,hashlib
from array import array
from pathlib import Path
from mathutils import Vector
out=Path(__file__).resolve().parents[1]/'Art/CreatureInterpretations'
bpy.ops.wm.open_mainfile(filepath=str(out/'CreatureBatch7.blend'))
for col in bpy.data.collections:col.hide_viewport=False
for obj in bpy.data.objects:obj.hide_viewport=False
bpy.context.view_layer.update()
result={}
for key in ['coyote','warg','rabid_rat']:
    parts=[o for o in bpy.data.objects if o.type=='MESH' and o.get('creature')==key]
    assert parts,key
    for obj in parts:
        paint=obj.data.color_attributes.get('Paint')
        assert paint and paint.domain=='CORNER' and paint.data_type=='FLOAT_COLOR',obj.name
        assert all(all(math.isfinite(c) for c in v.co) for v in obj.data.vertices)
        if obj.get('fur_surface'):
            assert obj.data.uv_layers.get('FurFlow'),obj.name
            assert all(m.name.startswith('Fur_') for m in obj.data.materials),obj.name
    body=bpy.data.objects[key+'_continuous_anatomy']
    points=[o.matrix_world@Vector(c) for o in parts for c in o.bound_box]
    low=[min(p[i] for p in points) for i in range(3)];high=[max(p[i] for p in points) for i in range(3)]
    assert low[2]>=-.003,(key,low)
    result[key]=dict(parts=len(parts),triangles=sum(sum(len(p.vertices)-2 for p in o.data.polygons) for o in parts),
        bounds_m=[low,high],paint_valid=True,fur_uv_valid=True)
    if key!='rabid_rat':
        eyes=sorted([o for o in parts if o.get('eye_center') is not None],key=lambda o:o['eye_side'])
        assert len(eyes)==2,key
        a,b=[Vector(o['eye_center']) for o in eyes]
        assert abs(a.x-b.x)<.001 and abs(a.z-b.z)<.001 and abs(a.y+b.y)<.001,(key,a,b)
        assert all(o['gaze_normal'][0]<-.6 for o in eyes)
        tail=next(o for o in parts if o.get('tail_form'))
        result[key].update(eye_symmetry_valid=True,eye_centers_m=[list(a),list(b)],body_width=body['body_width'],
            body_length=body['body_length'],head_to_torso_length=body['head_to_torso_length'],tail_form=tail['tail_form'])
    else:
        assert sum(o.get('state_module')=='saliva' for o in parts)==7
        assert not any(o.get('fur_surface') and any(t in o.name for t in ['bare_tail','whisker','toe','ear_cup']) for o in parts)

assert result['warg']['body_width']>result['coyote']['body_width']*1.5
assert result['warg']['head_to_torso_length']>result['coyote']['head_to_torso_length']
assert len([o for o in bpy.data.objects if o.name.startswith('warg_upper_fang')])==4
def digest(mesh,attribute):
    if attribute=='co':
        data=array('f',[0.0])*(len(mesh.vertices)*3);mesh.vertices.foreach_get('co',data)
    else:
        paint=mesh.color_attributes['Paint'];data=array('f',[0.0])*(len(paint.data)*4);paint.data.foreach_get('color',data)
    return hashlib.sha256(data.tobytes()).hexdigest()
with bpy.data.libraries.load(str(out/'CreatureBatch3.blend'),link=False) as (available,loaded):
    loaded.objects=['sewer_rat_continuous_anatomy']
base=loaded.objects[0];reused=bpy.data.objects['rabid_rat_continuous_anatomy']
for attr in ['co','color']:assert digest(base.data,attr)==digest(reused.data,attr),attr
result['rabid_rat'].update(exact_lean_body_reuse=True,original_paint_preserved=True,state_parts=7,
    reused_body_sha256=digest(reused.data,'co'))
(out/'batch7-mesh-inspection.json').write_text(json.dumps(result,indent=2))
print('CREATURE_BATCH7_NATIVE_CHECK PASS '+json.dumps(result),flush=True)
