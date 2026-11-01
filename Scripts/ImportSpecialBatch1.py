"""Three canonical asset namespaces; vertex paint, static water and memory materials."""
import unreal
from pathlib import Path
root=Path(unreal.Paths.project_dir()).resolve();scripts=root/'Scripts'
CREATURE_IMPORT_KEYS=['grid_bug']
exec(compile((scripts/'ImportCreatureInterpretations.py').read_text(encoding='utf-8'),'ImportCreatureInterpretations.py','exec'))
tools=unreal.AssetToolsHelpers.get_asset_tools();lib=unreal.MaterialEditingLibrary;dest='/Game/EnvironmentInterpretations';mats={}
for family,rough,spec in [('Stone',.78,.28),('Water',.13,.65)]:
    for memory in [False,True]:
        name='M_Fountain'+family+('Memory' if memory else '')
        mat=unreal.load_asset(dest+'/'+name) or tools.create_asset(name,dest,unreal.Material,unreal.MaterialFactoryNew());lib.delete_all_material_expressions(mat)
        color=lib.create_material_expression(mat,unreal.MaterialExpressionVertexColor,-500,0)
        scalar=lib.create_material_expression(mat,unreal.MaterialExpressionConstant,-500,150);scalar.set_editor_property('r',.2 if memory else 1.)
        mul=lib.create_material_expression(mat,unreal.MaterialExpressionMultiply,-250,0)
        assert lib.connect_material_expressions(color,'',mul,'A') and lib.connect_material_expressions(scalar,'',mul,'B')
        assert lib.connect_material_property(mul,'',unreal.MaterialProperty.MP_BASE_COLOR)
        for value,prop,y in [(rough,unreal.MaterialProperty.MP_ROUGHNESS,220),(spec,unreal.MaterialProperty.MP_SPECULAR,340)]:
            c=lib.create_material_expression(mat,unreal.MaterialExpressionConstant,-250,y);c.set_editor_property('r',value);assert lib.connect_material_property(c,'',prop)
        mat.set_editor_property('used_with_instanced_static_meshes',True);lib.recompile_material(mat);unreal.EditorAssetLibrary.save_loaded_asset(mat);mats[name]=mat
for key,folder,pkg in [('corpse','ObjectInterpretations','/Game/ObjectInterpretations'),('fountain','EnvironmentInterpretations',dest)]:
    task=unreal.AssetImportTask()
    for name,value in dict(filename=str(root/'Art'/folder/(key+'.fbx')),destination_path=pkg+'/Meshes',destination_name='SM_'+key,automated=True,replace_existing=True,replace_existing_settings=True,save=True).items():task.set_editor_property(name,value)
    options=unreal.FbxImportUI()
    for name,value in dict(import_mesh=True,import_as_skeletal=False,import_materials=False,import_textures=False,automated_import_should_detect_type=False,mesh_type_to_import=unreal.FBXImportType.FBXIT_STATIC_MESH).items():options.set_editor_property(name,value)
    for name,value in dict(combine_meshes=True,auto_generate_collision=False,transform_vertex_to_absolute=True,normal_import_method=unreal.FBXNormalImportMethod.FBXNIM_IMPORT_NORMALS,vertex_color_import_option=unreal.VertexColorImportOption.REPLACE).items():options.static_mesh_import_data.set_editor_property(name,value)
    task.set_editor_property('options',options);tools.import_asset_tasks([task]);mesh=unreal.load_asset(pkg+'/Meshes/SM_'+key);assert mesh
    for i,slot in enumerate(mesh.static_materials):
        name=str(slot.get_editor_property('imported_material_slot_name'))
        mat=unreal.load_asset('/Game/ObjectInterpretations/M_ObjectPaint') if key=='corpse' else mats['M_FountainWater' if name in ['fountain_water','fountain_foam'] else 'M_FountainStone']
        assert mat;mesh.set_material(i,mat)
    assert unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem).has_vertex_colors(mesh)
    unreal.EditorAssetLibrary.save_loaded_asset(mesh);unreal.log('SPECIAL_ASSET_IMPORTED '+key)
assert unreal.load_asset('/Game/ObjectInterpretations/M_ObjectPaintMemory')
unreal.log('SPECIAL_BATCH1_IMPORT_READY count=3')
