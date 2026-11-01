import bpy,json
from pathlib import Path
root=Path(__file__).resolve().parents[1]; out=root/'Art/CreatureInterpretations'
bpy.ops.wm.open_mainfile(filepath=str(out/'CreatureBatch3.blend'))
result={}
for key in ['sewer_rat','giant_rat','gnome_ruler']:
 parts=[o for o in bpy.data.objects if o.type=='MESH' and o.get('creature')==key]
 assert parts,key
 for obj in parts:
  attr=obj.data.color_attributes.get('Paint'); assert attr and attr.domain=='CORNER' and attr.data_type=='FLOAT_COLOR',obj.name
 result[key]={'parts':len(parts),'vertices':sum(len(o.data.vertices) for o in parts),'paint_valid':True}
body=bpy.data.objects['gnome_ruler_body']
with bpy.data.libraries.load(str(out/'CreatureBatch2.blend'),link=False) as (source,target):
 target.objects=['gnome_body']
original=target.objects[0]
assert len(body.data.vertices)==len(original.data.vertices)
assert all((a.co-b.co).length<1e-7 for a,b in zip(body.data.vertices,original.data.vertices))
assert bpy.data.objects.get('gnome_ruler_detachable_crown')
assert not any(o.name.startswith('gnome_ruler_pointed_cap') for o in bpy.data.objects)
result['gnome_ruler']['original_body_reused_exactly']=True
(out/'batch3-mesh-inspection.json').write_text(json.dumps(result,indent=2))
print('CREATURE_BATCH3_NATIVE_CHECK PASS '+json.dumps(result),flush=True)
