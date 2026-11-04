import sys,bpy
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from CreatureGeometry import *
bpy.ops.wm.open_mainfile(filepath=str(OUT/'Samurai.blend'))
for c in bpy.data.collections:c.hide_viewport=False
bpy.context.view_layer.update()
for key in ['samurai_male_human','samurai_female_human']:
 o=next(o for o in bpy.data.objects if o.type=='MESH' and o.get('creature')==key);assert not o.get('calf_fit_revised')
 indices={i for p in o.data.polygons if o.data.materials[p.material_index].name.startswith('samurai_red') for i in p.vertices}
 inverse=o.matrix_world.inverted()
 for i in indices:
  v=o.data.vertices[i];p=o.matrix_world@v.co
  if .10<p.z<.70:p.y*=1.4;v.co=inverse@p
 o['calf_fit_revised']=True
 bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
 bpy.ops.export_scene.fbx(filepath=str(OUT/(key+'.fbx')),use_selection=True,object_types={'MESH'},apply_unit_scale=True,axis_forward='-Y',axis_up='Z',add_leaf_bones=False,bake_anim=False,mesh_smooth_type='FACE')
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'Samurai.blend'))
