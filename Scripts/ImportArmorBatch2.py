"""Independent material/import validation for plate and dragon mail designs."""
import unreal,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from ArmorBatch2Config import GROUPS
root=Path(unreal.Paths.project_dir()).resolve();source=root/'Art/ObjectInterpretations'
tools=unreal.AssetToolsHelpers.get_asset_tools();dest='/Game/ArmorBatch2';materials={}
IMPORT_KEYS=globals().get('ARMOR_IMPORT_KEYS',GROUPS)
palettes={'plate_steel':(.23,1),'plate_bronze':(.29,.9),'plate_crystal':(.055,.75),'armor_dark':(.85,0),'regal_silver':(.17,1),'regal_gold':(.25,.85),'dragon_horn':(.5,0)}
for c in ['gray','gold','silver','red','white','orange','black','blue','green','yellow']:palettes['dragon_'+c]=(.24,.6) if c in ['gray','silver','gold'] else (.32,.14)
for pigment,(rough,metal) in palettes.items():
    if all('_dragon_' in k for k in IMPORT_KEYS) and pigment.startswith('plate_'):continue
    for memory in [False,True]:
        name='M_'+pigment+('Memory' if memory else '');mat=unreal.load_asset(dest+'/'+name) or tools.create_asset(name,dest,unreal.Material,unreal.MaterialFactoryNew());lib=unreal.MaterialEditingLibrary;lib.delete_all_material_expressions(mat)
        color=lib.create_material_expression(mat,unreal.MaterialExpressionVertexColor,-500,0);scale=lib.create_material_expression(mat,unreal.MaterialExpressionConstant,-500,150);scale.set_editor_property('r',.2 if memory else 1)
        mul=lib.create_material_expression(mat,unreal.MaterialExpressionMultiply,-250,0);assert lib.connect_material_expressions(color,'',mul,'A');assert lib.connect_material_expressions(scale,'',mul,'B');assert lib.connect_material_property(mul,'',unreal.MaterialProperty.MP_BASE_COLOR)
        values=[(rough,unreal.MaterialProperty.MP_ROUGHNESS),(metal,unreal.MaterialProperty.MP_METALLIC)]
        if pigment=='plate_crystal':
            mat.set_editor_property('shading_model',unreal.MaterialShadingModel.MSM_CLEAR_COAT)
            # Python's property enum omits the two custom clearcoat inputs.
            # Named MakeMaterialAttributes pins expose them without hidden enums.
            attributes=lib.create_material_expression(mat,unreal.MaterialExpressionMakeMaterialAttributes,0,0)
            pins=lib.get_material_expression_input_names(attributes)
            def pin(wanted):
                return next(str(p) for p in pins if str(p).replace(' ','').lower()==wanted.lower())
            assert lib.connect_material_expressions(mul,'',attributes,pin('BaseColor'))
            mat.set_editor_property('use_material_attributes',True)
            assert lib.connect_material_property(attributes,'',unreal.MaterialProperty.MP_MATERIAL_ATTRIBUTES)
            values=[(rough,'Roughness'),(metal,'Metallic'),(1,'ClearCoat'),(.025,'ClearCoatRoughness')]
        for i,(value,prop) in enumerate(values):
            node=lib.create_material_expression(mat,unreal.MaterialExpressionConstant,-250,200+i*100);node.set_editor_property('r',value)
            assert lib.connect_material_expressions(node,'',attributes,pin(prop)) if isinstance(prop,str) else lib.connect_material_property(node,'',prop)
        mat.set_editor_property('used_with_instanced_static_meshes',True);lib.recompile_material(mat);unreal.EditorAssetLibrary.save_loaded_asset(mat);materials[name]=mat
for key in IMPORT_KEYS:
    task=unreal.AssetImportTask()
    for name,value in dict(filename=str(source/(key+'.fbx')),destination_path=dest+'/Meshes',destination_name='SM_'+key,automated=True,replace_existing=True,replace_existing_settings=True,save=True).items():task.set_editor_property(name,value)
    options=unreal.FbxImportUI()
    for name,value in dict(import_mesh=True,import_as_skeletal=False,import_materials=False,import_textures=False,automated_import_should_detect_type=False,mesh_type_to_import=unreal.FBXImportType.FBXIT_STATIC_MESH).items():options.set_editor_property(name,value)
    for name,value in dict(combine_meshes=True,auto_generate_collision=False,transform_vertex_to_absolute=True,normal_import_method=unreal.FBXNormalImportMethod.FBXNIM_IMPORT_NORMALS,vertex_color_import_option=unreal.VertexColorImportOption.REPLACE).items():options.static_mesh_import_data.set_editor_property(name,value)
    task.set_editor_property('options',options);tools.import_asset_tasks([task]);mesh=unreal.load_asset(dest+'/Meshes/SM_'+key);assert mesh
    for i,slot in enumerate(mesh.static_materials):
        name=str(slot.get_editor_property('imported_material_slot_name'));assert 'M_'+name in materials,name;mesh.set_material(i,materials['M_'+name])
    assert unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem).has_vertex_colors(mesh)
    unreal.EditorAssetLibrary.save_loaded_asset(mesh);unreal.log('ARMOR_BATCH2_IMPORTED '+key)
unreal.log('ARMOR_BATCH2_IMPORT_READY count='+str(len(IMPORT_KEYS))+' crystal_clearcoat='+('True' if 'crystal_plate_mail' in IMPORT_KEYS else 'untouched'))
