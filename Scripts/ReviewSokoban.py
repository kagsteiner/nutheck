"""Inspect saved modules and render a real assembled construction study."""
import bpy,bmesh,json,math,hashlib
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[1];O=R/'Art/Sokoban';keys=['soko_wall','soko_floor','soko_boulder','soko_pit','soko_hole','soko_frame','soko_trim','soko_lamp']
bpy.ops.wm.open_mainfile(filepath=str(O/'Sokoban.blend'))
for c in bpy.data.collections:c.hide_viewport=False
bpy.context.view_layer.update();result={}
for key in keys:
 parts=[o for o in bpy.data.objects if o.type=='MESH' and o.get('creature')==key];assert parts
 for o in parts:
  assert not o.modifiers and not o.animation_data,o.name
  assert all(math.isfinite(v) for p in o.data.vertices for v in p.co)
  assert all(p.area>1e-12 for p in o.data.polygons),o.name
  a=o.data.color_attributes.get('Paint');assert a and a.domain=='CORNER' and len(a.data)==len(o.data.loops)
  bm=bmesh.new();bm.from_mesh(o.data);assert all(e.is_manifold for e in bm.edges),o.name;bm.free()
 pts=[o.matrix_world@v.co for o in parts for v in o.data.vertices];low=[min(p[i] for p in pts) for i in range(3)];high=[max(p[i] for p in pts) for i in range(3)]
 assert high[0]-low[0]<=1.001 and high[1]-low[1]<=1.001,(key,low,high)
 if key=='soko_wall':assert abs(high[2]-1.20)<1e-5 and low[2]>=-1e-5
 if key=='soko_boulder':assert abs(low[2])<1e-6 and high[0]-low[0]<.80 and high[1]-low[1]<.80
 if key in ['soko_pit','soko_hole']:assert low[2]<-.1 and abs(high[2]-.08)<1e-5
 result[key]=dict(parts=len(parts),triangles=sum(len(p.vertices)-2 for o in parts for p in o.data.polygons),bounds_m=[low,high],closed_geometry=True,paint_valid=True)
protected=json.loads((O/'protected.json').read_text());assert all(hashlib.sha256((R/p).read_bytes()).hexdigest()==h for p,h in protected.items())
result.update(status='PASS',protected_exports=len(protected),previous_exports_unchanged=True)
(O/'inspection.json').write_text(json.dumps(result,indent=2));print('SOKOBAN_GEOMETRY_PASS '+json.dumps(result),flush=True)
scene=bpy.context.scene;cam=scene.camera;scene.render.resolution_x=900;scene.render.resolution_y=700;scene.cycles.samples=20
for o in bpy.data.objects:
 if o.type=='MESH':o.hide_render=True
# This is an explicitly labelled construction study, not a native puzzle layout.
for key,at in [('soko_wall',(-1,1,0)),('soko_wall',(0,1,0)),('soko_wall',(1,1,0)),('soko_floor',(-1,0,0)),('soko_floor',(-1,-1,0)),('soko_floor',(0,-1,0)),('soko_floor',(1,-1,0)),('soko_pit',(0,0,0)),('soko_hole',(1,0,0)),('soko_boulder',(-1,-1,.08))]:
 for src in [o for o in list(bpy.data.objects) if o.type=='MESH' and o.get('creature')==key and not o.get('study_copy')]:
  o=src.copy();o.data=src.data.copy();scene.collection.objects.link(o);o.location+=Vector(at);o.hide_render=False;o['study_copy']=True
target=Vector((0,0,.3));cam.location=target+Vector((-3.8,-5.7,5.6));cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=4.5;cam.data.shift_x=cam.data.shift_y=0
scene.render.filepath=str(O/'Sokoban-ConstructionStudy.png');bpy.ops.render.render(write_still=True)
print('SOKOBAN_CONSTRUCTION_STUDY_READY')
