import unreal,json
from pathlib import Path
r=Path(unreal.Paths.project_dir()).resolve();report={}
for key in ['blue_jelly','spotted_jelly','ochre_jelly']:
 mesh=unreal.load_asset('/Game/CreatureInterpretations/Meshes/SM_'+key);assert mesh
 assert unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem).has_vertex_colors(mesh)
 slots=[]
 for slot in mesh.static_materials:
  name=str(slot.get_editor_property('imported_material_slot_name'));m=slot.get_editor_property('material_interface');assert m
  expected='M_Gel'
  assert m.get_name()==expected,(key,name,m.get_name())
  slots.append(dict(source=name,material=m.get_path_name()))

 report[key]=dict(asset=mesh.get_path_name(),vertex_colors=True,slots=slots)
(r/'Art/CreatureInterpretations/batch31-unreal-assets.json').write_text(json.dumps(dict(status='PASS',meshes=report),indent=2))
unreal.log('CREATURE_BATCH31_SAVED_ASSETS_PASS')
