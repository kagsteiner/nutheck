"""New world-space procedural rock materials; never edit dungeon assets."""
import unreal
tools=unreal.AssetToolsHelpers.get_asset_tools();lib=unreal.MaterialEditingLibrary
noise='''struct Rock {
float hash(float3 p){return frac(sin(dot(p,float3(127.1,311.7,74.7)))*43758.5453);}
float n(float3 p){float3 i=floor(p),f=frac(p);f=f*f*(3-2*f);
return lerp(lerp(lerp(hash(i),hash(i+float3(1,0,0)),f.x),lerp(hash(i+float3(0,1,0)),hash(i+float3(1,1,0)),f.x),f.y),lerp(lerp(hash(i+float3(0,0,1)),hash(i+float3(1,0,1)),f.x),lerp(hash(i+float3(0,1,1)),hash(i+float3(1,1,1)),f.x),f.y),f.z);}
float f(float3 p){return .57*n(p)+.28*n(p*2.13)+.15*n(p*5.47);}
}; Rock r;
'''
for surface in ['Rock','Floor']:
    name='M_Mines'+surface;dest='/Game/Mines'
    m=unreal.load_asset(dest+'/'+name) or tools.create_asset(name,dest,unreal.Material,unreal.MaterialFactoryNew())
    lib.delete_all_material_expressions(m)
    m.set_editor_property('used_with_instanced_static_meshes',True)
    m.set_editor_property('tangent_space_normal',False)
    def node(cls):return lib.create_material_expression(m,cls)
    def link(a,b,pin):assert lib.connect_material_expressions(a,'',b,pin)
    def custom(inputs,code,kind):
        n=node(unreal.MaterialExpressionCustom)
        entries=[]
        for k in inputs:
            entry=unreal.CustomInput();entry.set_editor_property('input_name',k);entries.append(entry)
        n.set_editor_property('inputs',entries)
        n.set_editor_property('code',code);n.set_editor_property('output_type',kind)
        for k,v in inputs.items():link(v,n,k)
        return n
    pos=node(unreal.MaterialExpressionWorldPosition)
    normal=node(unreal.MaterialExpressionVertexNormalWS)
    rock=surface=='Rock'
    low='float3(.12,.047,.025)' if rock else 'float3(.11,.105,.09)'
    high='float3(.39,.18,.078)' if rock else 'float3(.20,.19,.16)'
    col=custom({'P':pos},noise+f'''float a=r.f(P*.022),b=r.f(P*.19);
float crack=1-smoothstep(.015,.075,abs(r.f(P*.042)*2-1));
float seam=pow(saturate(r.f(P*.009)),9);
return lerp({low},{high},saturate(a*.85+b*.25))*(1-crack*{.28 if rock else .16})+seam*float3(.08,.065,.045);''',unreal.CustomMaterialOutputType.CMOT_FLOAT3)
    tint=node(unreal.MaterialExpressionVectorParameter);tint.set_editor_property('parameter_name','Tint');tint.set_editor_property('default_value',unreal.LinearColor(1,1,1,1))
    mul=node(unreal.MaterialExpressionMultiply);link(col,mul,'A');link(tint,mul,'B')
    assert lib.connect_material_property(mul,'',unreal.MaterialProperty.MP_BASE_COLOR)
    height=custom({'P':pos},noise+'return r.f(P*.055)*2.2+r.f(P*.32)*.35;',unreal.CustomMaterialOutputType.CMOT_FLOAT1)
    bump=custom({'P':pos,'N':normal,'H':height},'''float3 a=ddx(P),b=ddy(P);float3 r1=cross(b,N),r2=cross(N,a);float d=dot(a,r1);return normalize(abs(d)*N-sign(d)*(ddx(H)*r1+ddy(H)*r2));''',unreal.CustomMaterialOutputType.CMOT_FLOAT3)
    assert lib.connect_material_property(bump,'',unreal.MaterialProperty.MP_NORMAL)
    displacement='return saturate((P.z-8)/32)*float3(2.8*sin(P.y*.045+P.z*.055),2.8*sin(P.x*.051-P.z*.038),3.8*sin(P.x*.031)*cos(P.y*.039));' if rock else 'return float3(0,0,1.2*sin(P.x*.025)*cos(P.y*.021));'
    offset=custom({'P':pos},displacement,unreal.CustomMaterialOutputType.CMOT_FLOAT3)
    assert lib.connect_material_property(offset,'',unreal.MaterialProperty.MP_WORLD_POSITION_OFFSET)
    for prop,value in [(unreal.MaterialProperty.MP_ROUGHNESS,.97),(unreal.MaterialProperty.MP_SPECULAR,.12)]:
        c=node(unreal.MaterialExpressionConstant);c.set_editor_property('r',value);assert lib.connect_material_property(c,'',prop)
    lib.layout_material_expressions(m);lib.recompile_material(m);unreal.EditorAssetLibrary.save_loaded_asset(m)
    unreal.log('MINES_MATERIAL_READY '+surface)
unreal.SystemLibrary.quit_editor()
