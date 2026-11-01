"""Run once through Unreal Editor's Python plugin to create the starter map/material."""
import unreal

tools = unreal.AssetToolsHelpers.get_asset_tools()
material_path = "/Game/Materials/M_Prototype"
material = unreal.load_asset(material_path)
if not material:
    material = tools.create_asset("M_Prototype", "/Game/Materials", unreal.Material, unreal.MaterialFactoryNew())
    tint = unreal.MaterialEditingLibrary.create_material_expression(material, unreal.MaterialExpressionVectorParameter, -300, 0)
    tint.set_editor_property("parameter_name", "Tint")
    tint.set_editor_property("default_value", unreal.LinearColor(.3, .4, .4, 1))
    unreal.MaterialEditingLibrary.connect_material_property(tint, "", unreal.MaterialProperty.MP_BASE_COLOR)
    roughness = unreal.MaterialEditingLibrary.create_material_expression(material, unreal.MaterialExpressionConstant, -300, 150)
    roughness.set_editor_property("r", .85)
    unreal.MaterialEditingLibrary.connect_material_property(roughness, "", unreal.MaterialProperty.MP_ROUGHNESS)

# Set usage explicitly so the first game launch uses the intended material.
material.set_editor_property("used_with_instanced_static_meshes", True)
unreal.MaterialEditingLibrary.recompile_material(material)
unreal.EditorAssetLibrary.save_loaded_asset(material)

level_path = "/Game/Maps/DungeonPrototype"
if not unreal.EditorAssetLibrary.does_asset_exist(level_path):
    subsystem = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    if not subsystem.new_level(level_path):
        raise RuntimeError("Could not create prototype map")
    if not subsystem.save_current_level():
        raise RuntimeError("Could not save prototype map")
unreal.log("PROTOTYPE_ASSETS_READY")
unreal.SystemLibrary.quit_editor()
