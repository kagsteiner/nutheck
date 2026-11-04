"""Fresh-editor reload of every saved Sokoban mesh and material assignment."""
import unreal,json
from pathlib import Path
root=Path(unreal.Paths.project_dir()).resolve();dest='/Game/Sokoban';report={}
expected={'soko_sandstone':'Masonry','soko_floor':'Floor','soko_basalt':'Basalt','soko_bronze':'Bronze','soko_rock':'Boulder','soko_pit_earth':'Earth','soko_dark':'Dark','soko_lamp':'Lamp'}
properties={'Masonry':(.86,0),'Floor':(.89,0),'Basalt':(.83,0),'Bronze':(.32,.82),'Boulder':(.94,0),'Earth':(.95,0),'Dark':(1.,0),'Lamp':(.4,0)}
lib=unreal.MaterialEditingLibrary
for family,(rough,metal) in properties.items():
    for memory in [False,True]:
        name='M_Object'+family+('Memory' if memory else '');mat=unreal.load_asset(dest+'/'+name);assert mat,name
        for prop,value in [(unreal.MaterialProperty.MP_ROUGHNESS,rough),(unreal.MaterialProperty.MP_METALLIC,metal)]:
            node=lib.get_material_property_input_node(mat,prop);assert node and abs(node.get_editor_property('r')-value)<1e-5,name
        base=lib.get_material_property_input_node(mat,unreal.MaterialProperty.MP_BASE_COLOR);assert isinstance(base,unreal.MaterialExpressionMultiply),name
for key in ['soko_wall','soko_floor','soko_boulder','soko_pit','soko_hole','soko_frame','soko_trim','soko_lamp']:
    path=dest+'/Meshes/SM_'+key;mesh=unreal.load_asset(path);assert mesh,path
    assert unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem).has_vertex_colors(mesh),key
    slots=[]
    for slot in mesh.static_materials:
        name=str(slot.get_editor_property('imported_material_slot_name'));mat=slot.get_editor_property('material_interface');assert mat
        assert mat.get_name()=='M_Object'+expected[name],(key,name,mat.get_name())
        memory=unreal.load_asset(dest+'/'+mat.get_name()+'Memory');assert memory
        slots.append(dict(source=name,normal=mat.get_path_name(),memory=memory.get_path_name()))
    assert slots and (root/'Content/Sokoban/Meshes'/('SM_'+key+'.uasset')).exists()
    report[key]=dict(asset=path,vertex_colors=True,slots=slots)
(root/'Art/Sokoban/unreal-assets.json').write_text(json.dumps(dict(status='PASS',meshes=report,material_families=properties),indent=2))
unreal.log('SOKOBAN_SAVED_ASSETS_PASS count='+str(len(report)))
