import unreal,json
from pathlib import Path
r=Path(unreal.Paths.project_dir()).resolve();report={}
for key in ['samurai_male_human','samurai_female_human']:
 mesh=unreal.load_asset('/Game/CreatureInterpretations/Meshes/SM_'+key);assert mesh
 assert unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem).has_vertex_colors(mesh)
 slots=[]
 for slot in mesh.static_materials:
  name=str(slot.get_editor_property('imported_material_slot_name'));m=slot.get_editor_property('material_interface');assert m
  expected='M_Eye' if name in ['human_dark','human_sclera','human_blue','human_green','glint'] else 'M_Paint'
  assert m.get_name()==expected,(key,name,m.get_name())
  slots.append(dict(source=name,material=m.get_path_name()))

 report[key]=dict(asset=mesh.get_path_name(),vertex_colors=True,slots=slots)
(r/'Art/CreatureInterpretations/samurai-unreal-assets.json').write_text(json.dumps(dict(status='PASS',meshes=report),indent=2))
unreal.log('SAMURAI_SAVED_ASSETS_PASS')
