"""Run in the full hidden Unreal editor, via -ExecutePythonScript."""
import json
from pathlib import Path
import unreal

root=Path(unreal.Paths.project_dir()).resolve()
source=root/'Art/DefaultTiles'
entries=json.loads((source/'manifest.json').read_text())
tools=unreal.AssetToolsHelpers.get_asset_tools()
destination='/Game/DefaultTiles'
material=unreal.load_asset(destination+'/M_DefaultTilePixels')
if not material: material=tools.create_asset('M_DefaultTilePixels',destination,unreal.Material,unreal.MaterialFactoryNew())
unreal.MaterialEditingLibrary.delete_all_material_expressions(material)
color=unreal.MaterialEditingLibrary.create_material_expression(material,unreal.MaterialExpressionVertexColor,-300,0)
rough=unreal.MaterialEditingLibrary.create_material_expression(material,unreal.MaterialExpressionConstant,-300,200)
rough.set_editor_property('r',.85)
if not unreal.MaterialEditingLibrary.connect_material_property(color,'',unreal.MaterialProperty.MP_BASE_COLOR):
    raise RuntimeError('Could not connect the unnamed vertex RGB output')
if not unreal.MaterialEditingLibrary.connect_material_property(rough,'',unreal.MaterialProperty.MP_ROUGHNESS):
    raise RuntimeError('Could not connect roughness')
material.set_editor_property('used_with_instanced_static_meshes',True)
unreal.MaterialEditingLibrary.recompile_material(material)
unreal.EditorAssetLibrary.save_loaded_asset(material)
material_only='-DefaultTileMaterialOnly' in unreal.SystemLibrary.get_command_line()
for key in ([] if material_only else [e['key'] for e in entries]+['GreyFloor','GreyWall']):
    task=unreal.AssetImportTask()
    for name,value in dict(filename=str(source/(key+'.fbx')),destination_path=destination+'/Meshes',destination_name='SM_'+key,
        automated=True,replace_existing=True,replace_existing_settings=True,save=True).items(): task.set_editor_property(name,value)
    options=unreal.FbxImportUI()
    for name,value in dict(import_mesh=True,import_as_skeletal=False,import_materials=False,import_textures=False,
        automated_import_should_detect_type=False,mesh_type_to_import=unreal.FBXImportType.FBXIT_STATIC_MESH).items(): options.set_editor_property(name,value)
    data=options.static_mesh_import_data
    for name,value in dict(combine_meshes=True,auto_generate_collision=False,transform_vertex_to_absolute=True,
        normal_import_method=unreal.FBXNormalImportMethod.FBXNIM_IMPORT_NORMALS,
        vertex_color_import_option=unreal.VertexColorImportOption.REPLACE).items(): data.set_editor_property(name,value)
    task.set_editor_property('options',options)
    tools.import_asset_tasks([task])
    mesh=unreal.load_asset(destination+'/Meshes/SM_'+key)
    if not mesh: raise RuntimeError('Mesh import failed: '+key)
    if key not in ['GreyFloor','GreyWall']:
        mesh.set_material(0,material)
        unreal.EditorAssetLibrary.save_loaded_asset(mesh)
        if not unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem).has_vertex_colors(mesh): raise RuntimeError('Lost tile colours: '+key)
    unreal.log('DEFAULT_TILE_IMPORTED '+key)
unreal.log(f'DEFAULT_TILES_IMPORT_READY figures={len(entries)} terrain=2')
