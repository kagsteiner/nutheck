"""Read saved batch assets; verify slots and colour buffers after reloading."""
import unreal,json
from pathlib import Path
root=Path(unreal.Paths.project_dir()).resolve();dest='/Game/AppearanceBatch1';report={}
expected={'app1_iron':'M_ObjectIron','app1_dark_iron':'M_ObjectDarkIron','app1_gold':'M_ObjectGold','app1_oak':'M_ObjectOak','app1_ruby':'M_ObjectRuby'}
for key in ['ruby_ring','spherical_amulet','oak_wand']:
    path=dest+'/Meshes/SM_'+key;mesh=unreal.load_asset(path);assert mesh
    assert unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem).has_vertex_colors(mesh)
    slots=[]
    for slot in mesh.static_materials:
        name=str(slot.get_editor_property('imported_material_slot_name'));mat=slot.get_editor_property('material_interface');assert mat
        assert mat.get_name()==expected[name],(name,mat.get_name())
        memory=unreal.load_asset(dest+'/'+mat.get_name()+'Memory');assert memory
        slots.append(dict(source=name,normal=mat.get_path_name(),memory=memory.get_path_name()))
    assert slots;assert (root/'Content/AppearanceBatch1/Meshes'/('SM_'+key+'.uasset')).exists()
    report[key]=dict(asset=path,vertex_colors=True,slots=slots)
(root/'Art/ObjectInterpretations/appearance-batch1-unreal-assets.json').write_text(json.dumps(report,indent=2))
unreal.log('APPEARANCE_BATCH1_SAVED_ASSETS_PASS '+json.dumps(report))
