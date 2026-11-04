"""Read saved batch assets; verify slots and colour buffers after reloading."""
import unreal,json
from pathlib import Path
root=Path(unreal.Paths.project_dir()).resolve();dest='/Game/ToolBatch1';report={}
expected={'tool1_edge':'M_ObjectSilver','tool1_iron':'M_ObjectIron','tool1_brass':'M_ObjectGold','tool1_leather':'M_ObjectPaint','tool1_wood':'M_ObjectPaint','tool1_tube':'M_ObjectPaint'}
for key in ['pick_axe','grappling_hook','stethoscope']:
    path=dest+'/Meshes/SM_'+key;mesh=unreal.load_asset(path);assert mesh
    assert unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem).has_vertex_colors(mesh)
    slots=[]
    for slot in mesh.static_materials:
        name=str(slot.get_editor_property('imported_material_slot_name'));mat=slot.get_editor_property('material_interface');assert mat
        assert mat.get_name()==expected[name],(name,mat.get_name())
        memory=unreal.load_asset(dest+'/'+mat.get_name()+'Memory');assert memory
        slots.append(dict(source=name,normal=mat.get_path_name(),memory=memory.get_path_name()))
    assert slots;assert (root/'Content/ToolBatch1/Meshes'/('SM_'+key+'.uasset')).exists()
    report[key]=dict(asset=path,vertex_colors=True,slots=slots)
(root/'Art/ObjectInterpretations/tool-batch1-unreal-assets.json').write_text(json.dumps(report,indent=2))
unreal.log('TOOL_BATCH1_SAVED_ASSETS_PASS '+json.dumps(report))
