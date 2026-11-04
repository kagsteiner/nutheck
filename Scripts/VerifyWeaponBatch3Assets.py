"""Read saved batch assets; verify slots and colour buffers after reloading."""
import unreal,json
from pathlib import Path
root=Path(unreal.Paths.project_dir()).resolve();dest='/Game/WeaponBatch3';report={}
expected={'weapon3_edge':'M_ObjectSilver','weapon3_iron':'M_ObjectIron','weapon3_brass':'M_ObjectGold','weapon3_leather':'M_ObjectPaint','weapon3_wood':'M_ObjectPaint'}
for key in ['axe','mace','war_hammer']:
    path=dest+'/Meshes/SM_'+key;mesh=unreal.load_asset(path);assert mesh
    assert unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem).has_vertex_colors(mesh)
    slots=[]
    for slot in mesh.static_materials:
        name=str(slot.get_editor_property('imported_material_slot_name'));mat=slot.get_editor_property('material_interface');assert mat
        assert mat.get_name()==expected[name],(name,mat.get_name())
        memory=unreal.load_asset(dest+'/'+mat.get_name()+'Memory');assert memory
        slots.append(dict(source=name,normal=mat.get_path_name(),memory=memory.get_path_name()))
    assert slots;assert (root/'Content/WeaponBatch3/Meshes'/('SM_'+key+'.uasset')).exists()
    report[key]=dict(asset=path,vertex_colors=True,slots=slots)
(root/'Art/ObjectInterpretations/weapon-batch3-unreal-assets.json').write_text(json.dumps(report,indent=2))
unreal.log('WEAPON_BATCH3_SAVED_ASSETS_PASS '+json.dumps(report))
