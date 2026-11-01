"""Unreal editor Python: import the Blender study and assign shared palette materials."""
import json
import time
from pathlib import Path
import unreal

ROOT=Path(unreal.Paths.project_dir()).resolve()
SOURCE=ROOT/'Art/Studies/01-MiniatureDungeon'
TOOLS=unreal.AssetToolsHelpers.get_asset_tools()
DEST='/Game/ArtStudy'
palette=json.loads((SOURCE/'palette.json').read_text())
base_path=DEST+'/M_Miniature'
base=unreal.load_asset(base_path)
if not base:
    base=TOOLS.create_asset('M_Miniature',DEST,unreal.Material,unreal.MaterialFactoryNew())
    for name,prop,kind,x,y in [
        ('Tint',unreal.MaterialProperty.MP_BASE_COLOR,unreal.MaterialExpressionVectorParameter,-300,0),
        ('Roughness',unreal.MaterialProperty.MP_ROUGHNESS,unreal.MaterialExpressionScalarParameter,-300,180),
        ('Metallic',unreal.MaterialProperty.MP_METALLIC,unreal.MaterialExpressionScalarParameter,-300,340)]:
        node=unreal.MaterialEditingLibrary.create_material_expression(base,kind,x,y)
        node.set_editor_property('parameter_name',name)
        unreal.MaterialEditingLibrary.connect_material_property(node,'',prop)
base.set_editor_property('used_with_instanced_static_meshes',True)
unreal.MaterialEditingLibrary.recompile_material(base)
unreal.EditorAssetLibrary.save_loaded_asset(base)
materials={}
for name,(rgb,roughness,metallic) in palette.items():
    asset_name='MI_'+name
    mat=unreal.load_asset(DEST+'/Materials/'+asset_name)
    if not mat:
        mat=TOOLS.create_asset(asset_name,DEST+'/Materials',unreal.MaterialInstanceConstant,unreal.MaterialInstanceConstantFactoryNew())
    unreal.MaterialEditingLibrary.set_material_instance_parent(mat,base)
    unreal.MaterialEditingLibrary.set_material_instance_vector_parameter_value(mat,'Tint',unreal.LinearColor(*rgb,1))
    unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(mat,'Roughness',roughness)
    unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(mat,'Metallic',metallic)
    unreal.EditorAssetLibrary.save_loaded_asset(mat)
    materials[name]=mat

for group in ['Room','Hero','Dog','Ant','Goblin','Jelly']:
    task=unreal.AssetImportTask()
    task.set_editor_property('filename',str(SOURCE/(group+'.fbx')))
    task.set_editor_property('destination_path',DEST+'/Meshes')
    task.set_editor_property('destination_name','SM_'+group)
    task.set_editor_property('automated',True)
    task.set_editor_property('replace_existing',True)
    task.set_editor_property('save',True)
    options=unreal.FbxImportUI()
    options.set_editor_property('import_mesh',True)
    options.set_editor_property('import_as_skeletal',False)
    options.set_editor_property('import_materials',False)
    options.set_editor_property('import_textures',False)
    options.set_editor_property('automated_import_should_detect_type',False)
    options.set_editor_property('mesh_type_to_import',unreal.FBXImportType.FBXIT_STATIC_MESH)
    data=options.get_editor_property('static_mesh_import_data')
    data.set_editor_property('combine_meshes',True)
    data.set_editor_property('auto_generate_collision',False)
    data.set_editor_property('transform_vertex_to_absolute',True)
    data.set_editor_property('normal_import_method',unreal.FBXNormalImportMethod.FBXNIM_IMPORT_NORMALS)
    task.set_editor_property('options',options)
    TOOLS.import_asset_tasks([task])
    mesh=unreal.load_asset(DEST+'/Meshes/SM_'+group)
    if not mesh: raise RuntimeError(f'Import failed for {group}: {task.imported_object_paths}')
    for i,slot in enumerate(mesh.get_editor_property('static_materials')):
        name=str(slot.get_editor_property('imported_material_slot_name'))
        if name not in materials: raise RuntimeError(f'Unknown material slot {group}: {name}')
        mesh.set_material(i,materials[name])
    unreal.EditorAssetLibrary.save_loaded_asset(mesh)
    unreal.log(f'ART_STUDY_IMPORTED {group} slots={len(mesh.static_materials)}')
unreal.log('ART_STUDY_IMPORT_READY')
# Let editor startup and Interchange's UI callbacks complete before shutdown.
# Immediate quit in the startup Python callback can create editor UI during GC.
_quit_after=time.monotonic()+4.0
def _finish_import(delta_seconds):
    if time.monotonic()>=_quit_after:
        unreal.unregister_slate_post_tick_callback(_quit_handle)
        unreal.log('ART_STUDY_IMPORT_SHUTDOWN_READY')
        unreal.SystemLibrary.quit_editor()
_quit_handle=unreal.register_slate_post_tick_callback(_finish_import)
