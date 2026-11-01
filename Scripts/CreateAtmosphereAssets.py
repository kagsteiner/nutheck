"""Create candle flame and animated, softly lit floor-mist materials."""
import unreal

path = '/Game/Materials/M_CandleFlame'
material = unreal.load_asset(path)
if not material:
    material = unreal.AssetToolsHelpers.get_asset_tools().create_asset(
        'M_CandleFlame', '/Game/Materials', unreal.Material, unreal.MaterialFactoryNew())
    material.set_editor_property('shading_model', unreal.MaterialShadingModel.MSM_UNLIT)
    color = unreal.MaterialEditingLibrary.create_material_expression(
        material, unreal.MaterialExpressionConstant3Vector)
    color.set_editor_property('constant', unreal.LinearColor(5, 1.6, .25))
    unreal.MaterialEditingLibrary.connect_material_property(color, '', unreal.MaterialProperty.MP_EMISSIVE_COLOR)
    material.set_editor_property('used_with_instanced_static_meshes', True)
    unreal.MaterialEditingLibrary.recompile_material(material)
    unreal.EditorAssetLibrary.save_loaded_asset(material)

path = '/Game/Materials/M_DriftingMist'
mist = unreal.load_asset(path)
if not mist:
    mist = unreal.AssetToolsHelpers.get_asset_tools().create_asset(
        'M_DriftingMist', '/Game/Materials', unreal.Material, unreal.MaterialFactoryNew())
lib = unreal.MaterialEditingLibrary
lib.delete_all_material_expressions(mist)
mist.set_editor_property('blend_mode', unreal.BlendMode.BLEND_TRANSLUCENT)
mist.set_editor_property('two_sided', True)
mist.set_editor_property('translucency_lighting_mode', unreal.TranslucencyLightingMode.TLM_SURFACE_PER_PIXEL_LIGHTING)
mist.set_editor_property('used_with_instanced_static_meshes', True)

def node(cls, **properties):
    expression = lib.create_material_expression(mist, cls)
    for key, value in properties.items():
        expression.set_editor_property(key, value)
    return expression

inputs = []
for name in ('Position', 'Edges', 'Clock', 'Amount', 'SoftIntersection'):
    entry = unreal.CustomInput()
    entry.set_editor_property('input_name', name)
    inputs.append(entry)
opacity = node(unreal.MaterialExpressionCustom,
    output_type=unreal.CustomMaterialOutputType.CMOT_FLOAT1,
    inputs=inputs,
    code='''
struct MistNoise {
    float Hash(float2 p) {
        p = frac(p * float2(123.34, 456.21));
        p += dot(p, p + 45.32);
        return frac(p.x * p.y);
    }
    float Sample(float2 p) {
        float2 i = floor(p), f = frac(p);
        float2 u = f*f*(3.0-2.0*f);
        return lerp(lerp(Hash(i), Hash(i+float2(1,0)), u.x),
                    lerp(Hash(i+float2(0,1)), Hash(i+1), u.x), u.y);
    }
};
MistNoise noise;
float2 p = Position.xy / 150.0;
float2 drift = Clock * float2(0.035, 0.016);
float n = 0.65*noise.Sample(p-drift+Position.z*0.013)
        + 0.35*noise.Sample(p*2.3+drift*0.6+Position.z*0.041);
float wisps = smoothstep(0.28, 0.75, n);
// Fade only at the border of visible floor, never between adjacent visible
// cells. The animated world pattern therefore has no internal tile seams.
float2 uv = frac(Position.xy/100.0+0.5);
int edges = (int)Edges;
float edge = 1.0;
if (edges & 1) edge *= smoothstep(0.0,0.12,uv.x);
if (edges & 2) edge *= smoothstep(0.0,0.12,1-uv.x);
if (edges & 4) edge *= smoothstep(0.0,0.12,uv.y);
if (edges & 8) edge *= smoothstep(0.0,0.12,1-uv.y);
float height = saturate(1.0 - Position.z/75.0);
return 0.55 * wisps * edge * height * Amount * SoftIntersection;
''')
sources = {
    'Position': node(unreal.MaterialExpressionWorldPosition),
    'Clock': node(unreal.MaterialExpressionTime),
    'Amount': node(unreal.MaterialExpressionScalarParameter, parameter_name='MistAmount', default_value=1.0),
    'SoftIntersection': node(unreal.MaterialExpressionDepthFade, fade_distance_default=12.0),
}
edge_data = node(unreal.MaterialExpressionPerInstanceCustomData, data_index=0, const_default_value=15.0)
edge_pixel = node(unreal.MaterialExpressionVertexInterpolator)
lib.connect_material_expressions(edge_data, '', edge_pixel, 'VS')
sources['Edges'] = edge_pixel
for name, source in sources.items():
    if not lib.connect_material_expressions(source, '', opacity, name):
        raise RuntimeError('Could not connect mist input ' + name)
lib.connect_material_property(opacity, '', unreal.MaterialProperty.MP_OPACITY)
color = node(unreal.MaterialExpressionConstant3Vector, constant=unreal.LinearColor(.72, .76, .78))
lib.connect_material_property(color, '', unreal.MaterialProperty.MP_BASE_COLOR)
emission = node(unreal.MaterialExpressionConstant3Vector, constant=unreal.LinearColor(.10, .12, .14))
lib.connect_material_property(emission, '', unreal.MaterialProperty.MP_EMISSIVE_COLOR)
for value, prop in [(1.0, unreal.MaterialProperty.MP_ROUGHNESS), (0.0, unreal.MaterialProperty.MP_SPECULAR)]:
    lib.connect_material_property(node(unreal.MaterialExpressionConstant, r=value), '', prop)
lib.recompile_material(mist)
unreal.EditorAssetLibrary.save_loaded_asset(mist)
unreal.log('ATMOSPHERE_ASSETS_READY')
unreal.SystemLibrary.quit_editor()
