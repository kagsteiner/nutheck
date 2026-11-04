"""Full Unreal editor startup script for the 100 creature identities (104 forms) and four human player candidates."""
from pathlib import Path
import unreal

root=Path(unreal.Paths.project_dir()).resolve(); source=root/'Art/CreatureInterpretations'
tools=unreal.AssetToolsHelpers.get_asset_tools(); destination='/Game/CreatureInterpretations'
materials={}
for key,roughness,metallic in [('Paint',.82,0),('Chitin',.48,0),('Metal',.48,.55),('Eye',.35,0)]:
    path=destination+'/M_'+key; mat=unreal.load_asset(path)
    if not mat: mat=tools.create_asset('M_'+key,destination,unreal.Material,unreal.MaterialFactoryNew())
    unreal.MaterialEditingLibrary.delete_all_material_expressions(mat)
    color=unreal.MaterialEditingLibrary.create_material_expression(mat,unreal.MaterialExpressionVertexColor,-300,0)
    if not unreal.MaterialEditingLibrary.connect_material_property(color,'',unreal.MaterialProperty.MP_BASE_COLOR): raise RuntimeError('Missing vertex-colour connection')
    for value,prop,y in [(roughness,unreal.MaterialProperty.MP_ROUGHNESS,160),(metallic,unreal.MaterialProperty.MP_METALLIC,300)]:
        node=unreal.MaterialEditingLibrary.create_material_expression(mat,unreal.MaterialExpressionConstant,-300,y)
        node.set_editor_property('r',value)
        if not unreal.MaterialEditingLibrary.connect_material_property(node,'',prop): raise RuntimeError('Missing material connection')
    mat.set_editor_property('used_with_instanced_static_meshes',True)
    unreal.MaterialEditingLibrary.recompile_material(mat); unreal.EditorAssetLibrary.save_loaded_asset(mat); materials[key]=mat
# Reuse the approved texture-only study material; canonical old slots stay unchanged.
fur=unreal.load_asset('/Game/FurStudy/M_PaintedFur')
if not fur:raise RuntimeError('Missing approved painted fur material')
keys=globals().get('CREATURE_IMPORT_KEYS',['samurai_male_human','samurai_female_human','gray_ooze','brown_pudding','black_pudding','blue_jelly','spotted_jelly','ochre_jelly','acid_blob','quivering_blob','gelatinous_cube','yeti','sasquatch','owlbear','monkey','ape','carnivorous_ape','plains_centaur','forest_centaur','mountain_centaur','oracle','giant_ant','little_dog','goblin','jackal','fox','gnome','sewer_rat','giant_rat','gnome_ruler','kitten','housecat','large_cat','wolf','winter_wolf_cub','winter_wolf','dog','large_dog','dingo','coyote','warg','rabid_rat','bat','giant_bat','vampire_bat','jaguar','lynx','panther','tiger','hell_hound_pup','hell_hound','pony','horse','warhorse','white_unicorn','gray_unicorn','black_unicorn','kobold','large_kobold','kobold_leader','kobold_shaman','kobold_mummy','kobold_zombie','gnomish_wizard','gnome_mummy','gnome_zombie','gnomish_wizard_female','gnome_zombie_female','dwarf','dwarf_leader','dwarf_ruler','dwarf_mummy','dwarf_zombie','hobgoblin','hill_orc','mordor_orc','floating_eye','newt','lichen','uruk_hai','orc_shaman','orc_captain','grid_bug','orc_mummy','orc_zombie','soldier_ant','soldier_ant_female','fire_ant','fire_ant_female','giant_beetle','shopkeeper','killer_bee','queen_bee','xan','cave_spider','giant_spider','scorpion','gecko','iguana','lizard','garter_snake','snake','water_moccasin','python','pit_viper','cobra','valkyrie_female_human','barbarian_male_human'])
for key in keys:
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
    task.set_editor_property('options',options); tools.import_asset_tasks([task])
    mesh=unreal.load_asset(destination+'/Meshes/SM_'+key)
    if not mesh: raise RuntimeError('Creature import failed: '+key)
    for i,slot in enumerate(mesh.static_materials):
        name=str(slot.get_editor_property('imported_material_slot_name'))
        family='Metal' if name in ['steel','brass'] else 'Chitin' if name in ['shell','shell_light','joint','fire_shell','fire_light','fire_joint','beetle_red','beetle_orange','beetle_dark','beetle_highlight'] else 'Eye' if name in ['black','cyan','green','glint','fire_eye'] else 'Paint'
        if key in ['samurai_male_human','samurai_female_human','oracle','plains_centaur','forest_centaur','mountain_centaur'] and name in ['human_dark','human_sclera','human_blue','human_green','glint']:family='Eye'
        mesh.set_material(i,fur if name.startswith('Fur_') else materials[family])
    if key in ['wolf','winter_wolf_cub','winter_wolf','dog','large_dog','dingo','coyote','warg','rabid_rat','bat','giant_bat','vampire_bat','jaguar','lynx','panther','tiger','hell_hound_pup','hell_hound','pony','horse','warhorse','white_unicorn','gray_unicorn','black_unicorn']:
        assert any(str(slot.get_editor_property('imported_material_slot_name')).startswith('Fur_') for slot in mesh.static_materials),key
        unreal.log('CREATURE_FUR_MATERIAL_VALID '+key)
    unreal.EditorAssetLibrary.save_loaded_asset(mesh)
    if not unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem).has_vertex_colors(mesh): raise RuntimeError('Missing paint: '+key)
    unreal.log('SCULPTED_CREATURE_IMPORTED '+key)
unreal.log('SCULPTED_CREATURES_READY count='+str(len(keys)))
