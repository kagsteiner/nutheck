"""Nearest-filtered official atlas on a masked, unlit, two-sided instanced quad."""
import unreal,json
from pathlib import Path
root=Path(unreal.Paths.project_dir()).resolve();source=root/'Art/TileFallback';data=json.loads((source/'atlas.json').read_text())
tools=unreal.AssetToolsHelpers.get_asset_tools();dest='/Game/TileFallback';lib=unreal.MaterialEditingLibrary
task=unreal.AssetImportTask()
for k,v in dict(filename=str(source/'OfficialTiles.png'),destination_path=dest,destination_name='T_OfficialTiles',automated=True,replace_existing=True,save=True).items():task.set_editor_property(k,v)
tools.import_asset_tasks([task]);texture=unreal.load_asset(dest+'/T_OfficialTiles');assert texture
texture.set_editor_property('filter',unreal.TextureFilter.TF_NEAREST)
texture.set_editor_property('mip_gen_settings',unreal.TextureMipGenSettings.TMGS_NO_MIPMAPS)
texture.set_editor_property('compression_settings',unreal.TextureCompressionSettings.TC_EDITOR_ICON)
texture.set_editor_property('srgb',True);texture.set_editor_property('never_stream',True)
unreal.EditorAssetLibrary.save_loaded_asset(texture)
mat=unreal.load_asset(dest+'/M_OfficialTile') or tools.create_asset('M_OfficialTile',dest,unreal.Material,unreal.MaterialFactoryNew())
lib.delete_all_material_expressions(mat)
mat.set_editor_property('blend_mode',unreal.BlendMode.BLEND_MASKED)
mat.set_editor_property('shading_model',unreal.MaterialShadingModel.MSM_UNLIT)
mat.set_editor_property('two_sided',True);mat.set_editor_property('used_with_instanced_static_meshes',True)
mat.set_editor_property('opacity_mask_clip_value',.5)
def node(cls):return lib.create_material_expression(mat,cls)
def constant(v):
    n=node(unreal.MaterialExpressionConstant);n.set_editor_property('r',v);return n
def connect(a,b,pin):
    if lib.connect_material_expressions(a,'',b,pin):return
    names=lib.get_material_expression_input_names(b)
    if len(names)==1:
        assert lib.connect_material_expressions(a,'',b,str(names[0])),(b,names)
    else:raise RuntimeError(str(type(b))+' input '+pin+' available '+str(names))
def op(cls,a,b):
    n=node(cls);connect(a,n,'A');connect(b,n,'B');return n
def instance(index,default):
    n=node(unreal.MaterialExpressionPerInstanceCustomData);n.set_editor_property('data_index',index);n.set_editor_property('const_default_value',default)
    inter=node(unreal.MaterialExpressionVertexInterpolator);connect(n,inter,'Input');return inter
tile=instance(0,0);brightness=instance(1,1)
row_div=op(unreal.MaterialExpressionDivide,tile,constant(data['columns']))
row=node(unreal.MaterialExpressionFloor);connect(row_div,row,'Input')
col=op(unreal.MaterialExpressionSubtract,tile,op(unreal.MaterialExpressionMultiply,row,constant(data['columns'])))
cell=op(unreal.MaterialExpressionAppendVector,col,row)
uv=node(unreal.MaterialExpressionTextureCoordinate)
offset=op(unreal.MaterialExpressionAdd,op(unreal.MaterialExpressionMultiply,cell,constant(data['stride'])),constant(data['padding']))
pixel=op(unreal.MaterialExpressionMultiply,uv,constant(data['pixels']))
coord=op(unreal.MaterialExpressionDivide,op(unreal.MaterialExpressionAdd,offset,pixel),constant(data['width']))
sample=node(unreal.MaterialExpressionTextureSample);sample.set_editor_property('texture',texture);sample.set_editor_property('sampler_type',unreal.MaterialSamplerType.SAMPLERTYPE_COLOR);connect(coord,sample,'UVs')
color=node(unreal.MaterialExpressionMultiply)
assert lib.connect_material_expressions(sample,'RGB',color,'A');connect(brightness,color,'B')
assert lib.connect_material_property(color,'',unreal.MaterialProperty.MP_EMISSIVE_COLOR)
assert lib.connect_material_property(sample,'A',unreal.MaterialProperty.MP_OPACITY_MASK)
lib.layout_material_expressions(mat);lib.recompile_material(mat);unreal.EditorAssetLibrary.save_loaded_asset(mat)
task=unreal.AssetImportTask()
for k,v in dict(filename=str(source/'TileStandee.fbx'),destination_path=dest,destination_name='SM_TileStandee',automated=True,replace_existing=True,replace_existing_settings=True,save=True).items():task.set_editor_property(k,v)
options=unreal.FbxImportUI()
for k,v in dict(import_mesh=True,import_as_skeletal=False,import_materials=False,import_textures=False,automated_import_should_detect_type=False,mesh_type_to_import=unreal.FBXImportType.FBXIT_STATIC_MESH).items():options.set_editor_property(k,v)
for k,v in dict(combine_meshes=True,auto_generate_collision=False,transform_vertex_to_absolute=True).items():options.static_mesh_import_data.set_editor_property(k,v)
task.set_editor_property('options',options);tools.import_asset_tasks([task]);mesh=unreal.load_asset(dest+'/SM_TileStandee');assert mesh;mesh.set_material(0,mat)
unreal.EditorAssetLibrary.save_loaded_asset(mesh)
unreal.log('TILE_FALLBACK_IMPORT_READY count='+str(data['tile_count']))
