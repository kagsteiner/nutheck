"""Import three object drafts with painted wood/metal and dim memory variants."""
import unreal
from pathlib import Path
root=Path(unreal.Paths.project_dir()).resolve();source=root/'Art/ObjectInterpretations'
tools=unreal.AssetToolsHelpers.get_asset_tools();dest='/Game/AppearanceBatch1';materials={}
for family,rough,metal in [('Oak',.53,0),('Iron',.24,1.0),('DarkIron',.34,1.0),('Gold',.23,1.0),('Ruby',.12,0)]:
    for memory in [False,True]:
        name='M_Object'+family+('Memory' if memory else '');path=dest+'/'+name
        mat=unreal.load_asset(path) or tools.create_asset(name,dest,unreal.Material,unreal.MaterialFactoryNew())
        lib=unreal.MaterialEditingLibrary;lib.delete_all_material_expressions(mat)
        color=lib.create_material_expression(mat,unreal.MaterialExpressionVertexColor,-500,0)
        scalar=lib.create_material_expression(mat,unreal.MaterialExpressionConstant,-500,150);scalar.set_editor_property('r',.20 if memory else 1.)
        multiply=lib.create_material_expression(mat,unreal.MaterialExpressionMultiply,-250,0)
        assert lib.connect_material_expressions(color,'',multiply,'A')
        assert lib.connect_material_expressions(scalar,'',multiply,'B')
        assert lib.connect_material_property(multiply,'',unreal.MaterialProperty.MP_BASE_COLOR)
        for value,prop,y in [(rough,unreal.MaterialProperty.MP_ROUGHNESS,240),(metal,unreal.MaterialProperty.MP_METALLIC,360)]:
            node=lib.create_material_expression(mat,unreal.MaterialExpressionConstant,-250,y);node.set_editor_property('r',value)
            assert lib.connect_material_property(node,'',prop)
        mat.set_editor_property('used_with_instanced_static_meshes',True);lib.recompile_material(mat)
        unreal.EditorAssetLibrary.save_loaded_asset(mat);materials[name]=mat
for key in ['ruby_ring','spherical_amulet','oak_wand']:
    task=unreal.AssetImportTask()
    for name,value in dict(filename=str(source/(key+'.fbx')),destination_path=dest+'/Meshes',destination_name='SM_'+key,automated=True,replace_existing=True,replace_existing_settings=True,save=True).items():task.set_editor_property(name,value)
    options=unreal.FbxImportUI()
    for name,value in dict(import_mesh=True,import_as_skeletal=False,import_materials=False,import_textures=False,automated_import_should_detect_type=False,mesh_type_to_import=unreal.FBXImportType.FBXIT_STATIC_MESH).items():options.set_editor_property(name,value)
    for name,value in dict(combine_meshes=True,auto_generate_collision=False,transform_vertex_to_absolute=True,normal_import_method=unreal.FBXNormalImportMethod.FBXNIM_IMPORT_NORMALS,vertex_color_import_option=unreal.VertexColorImportOption.REPLACE).items():options.static_mesh_import_data.set_editor_property(name,value)
    task.set_editor_property('options',options);tools.import_asset_tasks([task]);mesh=unreal.load_asset(dest+'/Meshes/SM_'+key);assert mesh
    for i,slot in enumerate(mesh.static_materials):
        name=str(slot.get_editor_property('imported_material_slot_name'));mesh.set_material(i,materials[{'app1_iron':'M_ObjectIron','app1_dark_iron':'M_ObjectDarkIron','app1_gold':'M_ObjectGold','app1_oak':'M_ObjectOak','app1_ruby':'M_ObjectRuby'}[name]])
    assert unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem).has_vertex_colors(mesh)
    unreal.EditorAssetLibrary.save_loaded_asset(mesh);unreal.log('OBJECT_IMPORTED '+key)
unreal.log('APPEARANCE_BATCH1_IMPORT_READY count=3')





