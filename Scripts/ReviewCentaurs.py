"""Inspect saved centaur geometry and render real close views and marble overrides."""
import bpy,bmesh,math,json,hashlib,re
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[1];O=R/'Art/CreatureInterpretations';keys=['plains_centaur','forest_centaur','mountain_centaur']
bpy.ops.wm.open_mainfile(filepath=str(O/'Centaurs.blend'))
for c in bpy.data.collections:c.hide_viewport=False
bpy.context.view_layer.update();result={}
white=bpy.data.materials.new('Uniform pure white marble review');white.use_nodes=True;white.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=(1,1,1,1);white.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.28
scene=bpy.context.scene;cam=scene.camera;scene.render.resolution_x=700;scene.render.resolution_y=700;scene.cycles.samples=16
for key in keys:
 parts=[o for o in bpy.data.objects if o.type=='MESH' and o.get('creature')==key]
 for o in parts:
  assert not o.modifiers and not o.animation_data,o.name
  assert all(math.isfinite(c) for v in o.data.vertices for c in v.co),o.name
  assert all(p.area>1e-12 for p in o.data.polygons),o.name
  a=o.data.color_attributes.get('Paint');assert a and a.domain=='CORNER' and len(a.data)==len(o.data.loops),o.name
  bm=bmesh.new();bm.from_mesh(o.data)
  if o.get('eye_surface_conforming'):assert all(e.is_manifold or e.is_boundary for e in bm.edges)
  else:assert all(e.is_manifold for e in bm.edges),o.name
  if o.get('centaur_human') or o.get('centaur_equine'):
   todo=[next(iter(bm.verts))];seen=set()
   while todo:
    v=todo.pop()
    if v in seen:continue
    seen.add(v);todo.extend(e.other_vert(v) for e in v.link_edges)
   assert len(seen)==len(bm.verts),('disconnected',o.name,len(seen),len(bm.verts))
  bm.free()
 assert sum(bool(o.get('single_hoof')) for o in parts)==4
 assert sum('finger' in o.name for o in parts)==8 and sum('thumb' in o.name for o in parts)==2
 assert sum('eye_center' in o for o in parts)==2
 points=[o.matrix_world@v.co for o in parts for v in o.data.vertices];low=Vector(tuple(min(v[i] for v in points) for i in range(3)));high=Vector(tuple(max(v[i] for v in points) for i in range(3)));assert abs(low.z)<1e-6
 result[key]=dict(parts=len(parts),triangles=sum(len(p.vertices)-2 for o in parts for p in o.data.polygons),bounds_m=[list(low),list(high)],four_hooves=True,complete_hands=True,fitted_eyes=2,paint_valid=True,closed_solids_except_fitted_eye_patches=True,connected_human_and_equine_bodies=True)
 for o in bpy.data.objects:
  if o.type=='MESH':o.hide_render=o not in parts
 center=(low+high)*.5;body=next(o for o in parts if o.get('centaur_human'));head=Vector((body.matrix_world.translation.x,0,body['head_z']+body.location.z))
 # body location includes its original waist origin; absolute head height is stored pre-transform.
 head.z=body['head_z']+low.z
 for label,yaw,elev,target,scale in [('front',180,5,center,(high-low).length*1.15),('profile',-90,5,center,(high-low).length*1.15),('underside',-125,-35,center,(high-low).length*1.15),('face',180,5,head,.36),('marble',-125,30,center,(high-low).length*1.15)]:
  a=math.radians(yaw);e=math.radians(elev);cam.location=target+Vector((math.cos(a)*math.cos(e),math.sin(a)*math.cos(e),math.sin(e)))*4
  cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=scale;cam.data.shift_x=0;cam.data.shift_y=0;scene.view_layers[0].material_override=white if label=='marble' else None
  scene.render.filepath=str(O/(key+'-'+label+'.png'));bpy.ops.render.render(write_still=True)
 scene.view_layers[0].material_override=None
protected=json.loads((O/'centaurs-protected.json').read_text());assert all(hashlib.sha256((R/n).read_bytes()).hexdigest()==h for n,h in protected.items())
raw=(R/'upstream/NetHack/win/share/monsters.txt').read_text();tiles={n:rows.strip().splitlines() for _,n,rows in re.findall(r'^# tile (\d+) \(([^\n]+)\)\s*\{([^}]+)\}',raw,re.M)}
assert all(tiles[k.replace('_',' ')+',male']==tiles[k.replace('_',' ')+',female'] for k in keys)
result.update(status='PASS',protected_exports_unchanged=len(protected),source_sex_tiles_identical=True)
(O/'centaurs-mesh-inspection.json').write_text(json.dumps(result,indent=2));print('CENTAURS_MESH_REVIEW_PASS '+json.dumps(result),flush=True)
