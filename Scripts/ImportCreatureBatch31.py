"""Targeted primate import; reuse all shared creature materials."""
import unreal,json
from pathlib import Path
r=Path(unreal.Paths.project_dir()).resolve();dest='/Game/CreatureInterpretations';tools=unreal.AssetToolsHelpers.get_asset_tools()
fur=unreal.load_asset('/Game/FurStudy/M_PaintedFur');assert fur
materials={k:unreal.load_asset(dest+'/M_'+k) for k in ['Paint','Eye']};assert all(materials.values())
gel=unreal.load_asset(dest+'/M_Gel');assert gel
for key in ['blue_jelly','spotted_jelly','ochre_jelly']:
 task=unreal.AssetImportTask()
 for n,v in dict(filename=str(r/'Art/CreatureInterpretations'/(key+'.fbx')),destination_path=dest+'/Meshes',destination_name='SM_'+key,automated=True,replace_existing=True,replace_existing_settings=True,save=True).items():task.set_editor_property(n,v)
 opt=unreal.FbxImportUI()
 for n,v in dict(import_mesh=True,import_as_skeletal=False,import_materials=False,import_textures=False,automated_import_should_detect_type=False,mesh_type_to_import=unreal.FBXImportType.FBXIT_STATIC_MESH).items():opt.set_editor_property(n,v)
 for n,v in dict(combine_meshes=True,auto_generate_collision=False,transform_vertex_to_absolute=True,normal_import_method=unreal.FBXNormalImportMethod.FBXNIM_IMPORT_NORMALS,vertex_color_import_option=unreal.VertexColorImportOption.REPLACE).items():opt.static_mesh_import_data.set_editor_property(n,v)
 task.set_editor_property('options',opt);tools.import_asset_tasks([task]);mesh=unreal.load_asset(dest+'/Meshes/SM_'+key);assert mesh
 for i,slot in enumerate(mesh.static_materials):
  mesh.set_material(i,gel)
 assert unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem).has_vertex_colors(mesh)
 unreal.EditorAssetLibrary.save_loaded_asset(mesh);unreal.log('SCULPTED_CREATURE_IMPORTED '+key)

unreal.log('SCULPTED_CREATURES_READY count=3')
exec(compile((r/'Scripts/VerifyCreatureBatch31Assets.py').read_text(),'VerifyCreatureBatch31Assets','exec'))
