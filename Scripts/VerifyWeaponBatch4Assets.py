"""Read saved batch assets; verify slots and colour buffers after reloading."""
import unreal,json
from pathlib import Path
root=Path(unreal.Paths.project_dir()).resolve();dest='/Game/WeaponBatch4';report={}
expected={'w4_steel':'M_ObjectSteel','w4_edge':'M_ObjectEdge','w4_silver':'M_ObjectSilver','w4_brass':'M_ObjectBrass','w4_dark':'M_ObjectDark','w4_leather':'M_ObjectLeather','w4_blue_wrap':'M_ObjectBlueWrap'}
for family,rough,metal in [('Steel',.26,1),('Edge',.19,1),('Silver',.22,1),('Brass',.29,.85),('Dark',.34,1),('Leather',.72,0),('BlueWrap',.73,0)]:
    for memory in [False,True]:
        mat=unreal.load_asset(dest+'/M_Object'+family+('Memory' if memory else ''));assert mat
        for prop,value in [(unreal.MaterialProperty.MP_ROUGHNESS,rough),(unreal.MaterialProperty.MP_METALLIC,metal)]:
            node=unreal.MaterialEditingLibrary.get_material_property_input_node(mat,prop)
            assert node and abs(node.get_editor_property('r')-value)<1e-5,(family,memory,value)
for key in ['silver_saber','broadsword','two_handed_sword']:
    path=dest+'/Meshes/SM_'+key;mesh=unreal.load_asset(path);assert mesh
    assert unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem).has_vertex_colors(mesh)
    slots=[]
    for slot in mesh.static_materials:
        name=str(slot.get_editor_property('imported_material_slot_name'));mat=slot.get_editor_property('material_interface');assert mat
        assert mat.get_name()==expected[name],(name,mat.get_name())
        memory=unreal.load_asset(dest+'/'+mat.get_name()+'Memory');assert memory
        slots.append(dict(source=name,normal=mat.get_path_name(),memory=memory.get_path_name()))
    assert slots;assert (root/'Content/WeaponBatch4/Meshes'/('SM_'+key+'.uasset')).exists()
    report[key]=dict(asset=path,vertex_colors=True,slots=slots)
(root/'Art/ObjectInterpretations/weapon-batch4-unreal-assets.json').write_text(json.dumps(report,indent=2))
unreal.log('WEAPON_BATCH4_SAVED_ASSETS_PASS '+json.dumps(report))
