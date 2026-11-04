"""Read saved batch assets; verify slots and colour buffers after reloading."""
import unreal,json
from pathlib import Path
root=Path(unreal.Paths.project_dir()).resolve();dest='/Game/AppearanceBatch2';report={}
expected={'app2_iron':'M_ObjectIron','app2_dark_iron':'M_ObjectDarkIron','app2_silver':'M_ObjectSilver','app2_dark_silver':'M_ObjectDarkSilver','app2_sapphire':'M_ObjectSapphire'}
for family,rough,metal in [('Sapphire',.13,0),('Silver',.26,1),('DarkSilver',.35,1),('Iron',.28,1),('DarkIron',.38,1)]:
    for memory in [False,True]:
        mat=unreal.load_asset(dest+'/M_Object'+family+('Memory' if memory else ''));assert mat
        for prop,value in [(unreal.MaterialProperty.MP_ROUGHNESS,rough),(unreal.MaterialProperty.MP_METALLIC,metal)]:
            node=unreal.MaterialEditingLibrary.get_material_property_input_node(mat,prop)
            assert node and abs(node.get_editor_property('r')-value)<1e-5,(family,memory,value)
for key in ['sapphire_ring','triangular_amulet','silver_wand']:
    path=dest+'/Meshes/SM_'+key;mesh=unreal.load_asset(path);assert mesh
    assert unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem).has_vertex_colors(mesh)
    slots=[]
    for slot in mesh.static_materials:
        name=str(slot.get_editor_property('imported_material_slot_name'));mat=slot.get_editor_property('material_interface');assert mat
        assert mat.get_name()==expected[name],(name,mat.get_name())
        memory=unreal.load_asset(dest+'/'+mat.get_name()+'Memory');assert memory
        slots.append(dict(source=name,normal=mat.get_path_name(),memory=memory.get_path_name()))
    assert slots;assert (root/'Content/AppearanceBatch2/Meshes'/('SM_'+key+'.uasset')).exists()
    report[key]=dict(asset=path,vertex_colors=True,slots=slots)
(root/'Art/ObjectInterpretations/appearance-batch2-unreal-assets.json').write_text(json.dumps(report,indent=2))
unreal.log('APPEARANCE_BATCH2_SAVED_ASSETS_PASS '+json.dumps(report))
