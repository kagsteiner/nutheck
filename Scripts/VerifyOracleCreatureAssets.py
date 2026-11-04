"""Reload the saved Oracle asset and verify material slots and vertex colours."""
import unreal,json
from pathlib import Path
root=Path(unreal.Paths.project_dir()).resolve();path='/Game/CreatureInterpretations/Meshes/SM_oracle'
mesh=unreal.load_asset(path);assert mesh
assert unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem).has_vertex_colors(mesh)
slots=[]
for slot in mesh.static_materials:
 name=str(slot.get_editor_property('imported_material_slot_name'));mat=slot.get_editor_property('material_interface');assert mat
 expected='M_Eye' if name in ['human_dark','human_sclera','human_blue','glint'] else 'M_Paint'
 assert mat.get_name()==expected,(name,mat.get_name())
 slots.append(dict(source=name,material=mat.get_path_name()))
assert slots
report=dict(asset=path,vertex_colors=True,slots=slots,status='PASS')
(root/'Art/CreatureInterpretations/oracle-unreal-assets.json').write_text(json.dumps(report,indent=2))
unreal.log('ORACLE_CREATURE_SAVED_ASSETS_PASS '+json.dumps(report))
