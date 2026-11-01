"""Import generated limestone albedos and build UV-independent matte materials.

Run with UnrealEditor -ExecutePythonScript=.../ImportWeatheredStone.py.
"""
from pathlib import Path
import unreal

root = Path(unreal.Paths.project_dir()).resolve()
source = root / 'Art/WeatheredStone'
destination = '/Game/WeatheredStone'
tools = unreal.AssetToolsHelpers.get_asset_tools()
lib = unreal.MaterialEditingLibrary

for surface in ('Wall', 'Floor'):
    task = unreal.AssetImportTask()
    for key, value in dict(filename=str(source / f'Limestone{surface}_BaseColor.png'),
                           destination_path=destination, destination_name=f'T_Limestone{surface}',
                           automated=True, replace_existing=True, save=True).items():
        task.set_editor_property(key, value)
    tools.import_asset_tasks([task])
    texture = unreal.load_asset(f'{destination}/T_Limestone{surface}')
    assert texture, surface
    texture.set_editor_property('srgb', True)
    texture.set_editor_property('address_x', unreal.TextureAddress.TA_WRAP)
    texture.set_editor_property('address_y', unreal.TextureAddress.TA_WRAP)
    unreal.EditorAssetLibrary.save_loaded_asset(texture)
    name = f'M_Stone{surface}'
    material = unreal.load_asset(f'{destination}/{name}') or tools.create_asset(
        name, destination, unreal.Material, unreal.MaterialFactoryNew())
    lib.delete_all_material_expressions(material)
    material.set_editor_property('used_with_instanced_static_meshes', True)

    def node(cls):
        return lib.create_material_expression(material, cls)

    def wire(a, b, pin, output=''):
        if lib.connect_material_expressions(a, output, b, pin):
            return
        names = lib.get_material_expression_input_names(b)
        assert len(names) == 1 and lib.connect_material_expressions(a, output, b, str(names[0])), (type(b), pin, names)

    def constant(value):
        result = node(unreal.MaterialExpressionConstant)
        result.set_editor_property('r', value)
        return result

    def op(cls, a, b):
        result = node(cls)
        wire(a, result, 'A')
        wire(b, result, 'B')
        return result

    def mask(a, channels):
        result = node(unreal.MaterialExpressionComponentMask)
        for channel in ('r', 'g', 'b', 'a'):
            result.set_editor_property(channel, channel in channels)
        wire(a, result, 'Input')
        return result

    position = node(unreal.MaterialExpressionWorldPosition)
    coords = op(unreal.MaterialExpressionDivide, position, constant(160.0))
    normal = node(unreal.MaterialExpressionPixelNormalWS)
    absolute = node(unreal.MaterialExpressionAbs)
    wire(normal, absolute, 'Input')
    sharpen = node(unreal.MaterialExpressionPower)
    wire(absolute, sharpen, 'Base')
    wire(constant(4), sharpen, 'Exp')
    weights = [mask(sharpen, channel) for channel in ('r', 'g', 'b')]
    total = op(unreal.MaterialExpressionAdd,
               op(unreal.MaterialExpressionAdd, weights[0], weights[1]), weights[2])
    samples = []
    for axes, weight in zip(('gb', 'rb', 'rg'), weights):
        sample = node(unreal.MaterialExpressionTextureSample)
        sample.set_editor_property('texture', texture)
        sample.set_editor_property('sampler_type', unreal.MaterialSamplerType.SAMPLERTYPE_COLOR)
        wire(mask(coords, axes), sample, 'UVs')
        samples.append(op(unreal.MaterialExpressionMultiply, sample,
                          op(unreal.MaterialExpressionDivide, weight, total)))
    color = op(unreal.MaterialExpressionAdd,
               op(unreal.MaterialExpressionAdd, samples[0], samples[1]), samples[2])
    random = node(unreal.MaterialExpressionPerInstanceRandom)
    variation = op(unreal.MaterialExpressionAdd, constant(.90),
                   op(unreal.MaterialExpressionMultiply, random, constant(.20)))
    tint = node(unreal.MaterialExpressionVectorParameter)
    tint.set_editor_property('parameter_name', 'Tint')
    tint.set_editor_property('default_value', unreal.LinearColor(1, 1, 1, 1))
    color = op(unreal.MaterialExpressionMultiply, color,
               op(unreal.MaterialExpressionMultiply, tint, variation))
    assert lib.connect_material_property(color, '', unreal.MaterialProperty.MP_BASE_COLOR)
    for value, prop in ((.94, unreal.MaterialProperty.MP_ROUGHNESS),
                        (.18, unreal.MaterialProperty.MP_SPECULAR),
                        (0, unreal.MaterialProperty.MP_METALLIC)):
        assert lib.connect_material_property(constant(value), '', prop)
    lib.layout_material_expressions(material)
    lib.recompile_material(material)
    unreal.EditorAssetLibrary.save_loaded_asset(material)
    unreal.log(f'WEATHERED_STONE_IMPORTED {surface}')

unreal.log('WEATHERED_STONE_IMPORT_READY')
