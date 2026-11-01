"""Import isolated fur study meshes and two shared textures; retain live assets."""
import unreal
from pathlib import Path
root=Path(unreal.Paths.project_dir()).resolve();source=root/'Art/FurStudy';dest='/Game/FurStudy'
tools=unreal.AssetToolsHelpers.get_asset_tools()

def task(filename,path,name,options=None):
    job=unreal.AssetImportTask()
    for key,value in dict(filename=str(filename),destination_path=path,destination_name=name,
        automated=True,replace_existing=True,replace_existing_settings=True,save=True).items():job.set_editor_property(key,value)
    if options:job.set_editor_property('options',options)
    tools.import_asset_tasks([job]);asset=unreal.load_asset(path+'/'+name)
    if not asset:raise RuntimeError('Import failed: '+name)
    return asset

textures={}
for key in ['FurBrush','FurBrushNormal']:
    tex=task(source/'Textures'/(key+'.png'),dest+'/Textures','T_'+key)
    tex.set_editor_property('srgb',False)
    if key.endswith('Normal'):
        tex.set_editor_property('compression_settings',unreal.TextureCompressionSettings.TC_NORMALMAP)
        tex.set_editor_property('flip_green_channel',True)
    tex.post_edit_change() if hasattr(tex,'post_edit_change') else None
    unreal.EditorAssetLibrary.save_loaded_asset(tex);textures[key]=tex

mat=unreal.load_asset(dest+'/M_PaintedFur') or tools.create_asset('M_PaintedFur',dest,unreal.Material,unreal.MaterialFactoryNew())
library=unreal.MaterialEditingLibrary;library.delete_all_material_expressions(mat)
vertex=library.create_material_expression(mat,unreal.MaterialExpressionVertexColor,-600,0)
brush=library.create_material_expression(mat,unreal.MaterialExpressionTextureSample,-600,180)
brush.set_editor_property('texture',textures['FurBrush']);brush.set_editor_property('sampler_type',unreal.MaterialSamplerType.SAMPLERTYPE_LINEAR_COLOR)
two=library.create_material_expression(mat,unreal.MaterialExpressionConstant,-600,400);two.set_editor_property('r',2)
modulate=library.create_material_expression(mat,unreal.MaterialExpressionMultiply,-350,160)
base=library.create_material_expression(mat,unreal.MaterialExpressionMultiply,-100,0)
for a,out,b,pin in [(brush,'RGB',modulate,'A'),(two,'',modulate,'B'),(vertex,'',base,'A'),(modulate,'',base,'B')]:
    assert library.connect_material_expressions(a,out,b,pin)
assert library.connect_material_property(base,'',unreal.MaterialProperty.MP_BASE_COLOR)
normal=library.create_material_expression(mat,unreal.MaterialExpressionTextureSample,-350,400)
normal.set_editor_property('texture',textures['FurBrushNormal']);normal.set_editor_property('sampler_type',unreal.MaterialSamplerType.SAMPLERTYPE_NORMAL)
assert library.connect_material_property(normal,'RGB',unreal.MaterialProperty.MP_NORMAL)
rough=library.create_material_expression(mat,unreal.MaterialExpressionConstant,-100,600);rough.set_editor_property('r',.82)
assert library.connect_material_property(rough,'',unreal.MaterialProperty.MP_ROUGHNESS)
mat.set_editor_property('used_with_instanced_static_meshes',True)
library.recompile_material(mat);unreal.EditorAssetLibrary.save_loaded_asset(mat)

for species in ['little_dog','housecat']:
    for variant in ['smooth','painted','tufted']:
        key=species+'_'+variant;options=unreal.FbxImportUI()
        for name,value in dict(import_mesh=True,import_as_skeletal=False,import_materials=False,import_textures=False,
            automated_import_should_detect_type=False,mesh_type_to_import=unreal.FBXImportType.FBXIT_STATIC_MESH).items():options.set_editor_property(name,value)
        data=options.static_mesh_import_data
        for name,value in dict(combine_meshes=True,auto_generate_collision=False,transform_vertex_to_absolute=True,
            normal_import_method=unreal.FBXNormalImportMethod.FBXNIM_IMPORT_NORMALS,
            vertex_color_import_option=unreal.VertexColorImportOption.REPLACE).items():data.set_editor_property(name,value)
        mesh=task(source/(key+'.fbx'),dest+'/Meshes','SM_'+key,options)
        fur_slots=0
        for i,slot in enumerate(mesh.static_materials):
            name=str(slot.get_editor_property('imported_material_slot_name'))
            if name.startswith('Fur_'):material=mat;fur_slots+=1
            else:
                family='Eye' if name in ['black','cyan','green','glint'] else 'Paint'
                material=unreal.load_asset('/Game/CreatureInterpretations/M_'+family)
            if not material:raise RuntimeError('Missing material '+name)
            mesh.set_material(i,material)
        assert unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem).has_vertex_colors(mesh)
        assert (fur_slots==0) if variant=='smooth' else (fur_slots>0)
        unreal.EditorAssetLibrary.save_loaded_asset(mesh)
        unreal.log('FUR_STUDY_IMPORTED '+key+' fur_slots='+str(fur_slots))
unreal.log('FUR_STUDY_IMPORT_READY variants=6 textures=2')
