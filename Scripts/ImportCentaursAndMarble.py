"""Targeted centaur import and uniform white marble; never rewrite creature materials."""
import unreal,json
from pathlib import Path
r=Path(unreal.Paths.project_dir()).resolve();dest='/Game/CreatureInterpretations';tools=unreal.AssetToolsHelpers.get_asset_tools()
materials={k:unreal.load_asset(dest+'/M_'+k) for k in ['Paint','Eye']};assert all(materials.values())
for key in ['plains_centaur','forest_centaur','mountain_centaur']:
 task=unreal.AssetImportTask()
 for n,v in dict(filename=str(r/'Art/CreatureInterpretations'/(key+'.fbx')),destination_path=dest+'/Meshes',destination_name='SM_'+key,automated=True,replace_existing=True,replace_existing_settings=True,save=True).items():task.set_editor_property(n,v)
 opt=unreal.FbxImportUI()
 for n,v in dict(import_mesh=True,import_as_skeletal=False,import_materials=False,import_textures=False,automated_import_should_detect_type=False,mesh_type_to_import=unreal.FBXImportType.FBXIT_STATIC_MESH).items():opt.set_editor_property(n,v)
 for n,v in dict(combine_meshes=True,auto_generate_collision=False,transform_vertex_to_absolute=True,normal_import_method=unreal.FBXNormalImportMethod.FBXNIM_IMPORT_NORMALS,vertex_color_import_option=unreal.VertexColorImportOption.REPLACE).items():opt.static_mesh_import_data.set_editor_property(n,v)
 task.set_editor_property('options',opt);tools.import_asset_tasks([task]);mesh=unreal.load_asset(dest+'/Meshes/SM_'+key);assert mesh
 for i,slot in enumerate(mesh.static_materials):
  name=str(slot.get_editor_property('imported_material_slot_name'));mesh.set_material(i,materials['Eye' if name in ['human_dark','human_sclera','human_blue','glint'] else 'Paint'])
 assert unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem).has_vertex_colors(mesh)
 unreal.EditorAssetLibrary.save_loaded_asset(mesh);unreal.log('CENTAUR_IMPORTED '+key)
for memory in [False,True]:
 name='M_WhiteMarble'+('Memory' if memory else '');path='/Game/Statues/'+name
 mat=unreal.load_asset(path) or tools.create_asset(name,'/Game/Statues',unreal.Material,unreal.MaterialFactoryNew())
 lib=unreal.MaterialEditingLibrary;lib.delete_all_material_expressions(mat)
 color=lib.create_material_expression(mat,unreal.MaterialExpressionConstant3Vector,-300,0);v=.20 if memory else 1.
 color.set_editor_property('constant',unreal.LinearColor(v,v,v,1));assert lib.connect_material_property(color,'',unreal.MaterialProperty.MP_BASE_COLOR)
 for value,prop,y in [(.28,unreal.MaterialProperty.MP_ROUGHNESS,150),(0.,unreal.MaterialProperty.MP_METALLIC,250),(.5,unreal.MaterialProperty.MP_SPECULAR,350)]:
  n=lib.create_material_expression(mat,unreal.MaterialExpressionConstant,-300,y);n.set_editor_property('r',value);assert lib.connect_material_property(n,'',prop)
 mat.set_editor_property('used_with_instanced_static_meshes',True);lib.recompile_material(mat);unreal.EditorAssetLibrary.save_loaded_asset(mat)
unreal.log('CENTAURS_AND_WHITE_MARBLE_READY')
