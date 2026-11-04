"""Procedural night sky: a large cratered moon and fixed stars, with no external textures."""
import unreal
lib=unreal.MaterialEditingLibrary;tools=unreal.AssetToolsHelpers.get_asset_tools()
dest='/Game/ValkyrieQuest';name='M_NightSky'
m=unreal.load_asset(dest+'/'+name) or tools.create_asset(name,dest,unreal.Material,unreal.MaterialFactoryNew())
lib.delete_all_material_expressions(m)
m.set_editor_property('shading_model',unreal.MaterialShadingModel.MSM_UNLIT)
m.set_editor_property('two_sided',True);m.set_editor_property('is_sky',True)
p=lib.create_material_expression(m,unreal.MaterialExpressionWorldPosition)
c=lib.create_material_expression(m,unreal.MaterialExpressionCameraPositionWS)
n=lib.create_material_expression(m,unreal.MaterialExpressionCustom)
entries=[]
for key in ['P','C']:
 e=unreal.CustomInput();e.set_editor_property('input_name',key);entries.append(e)
n.set_editor_property('inputs',entries)
lib.connect_material_expressions(p,'',n,'P');lib.connect_material_expressions(c,'',n,'C')
n.set_editor_property('output_type',unreal.CustomMaterialOutputType.CMOT_FLOAT3)
n.set_editor_property('code',r'''
float3 d=normalize(P-C),moon=float3(0,-.9396926,.3420201);
float horizon=pow(1-abs(d.z),4);
float3 color=lerp(float3(.0015,.003,.009),float3(.009,.015,.033),horizon);
float2 uv=float2(atan2(d.y,d.x)*95,asin(clamp(d.z,-1,1))*95);
float2 cell=floor(uv),local=frac(uv)-.5;
float h=frac(sin(dot(cell,float2(127.1,311.7)))*43758.5453);
float h2=frac(sin(dot(cell,float2(269.5,183.3)))*43758.5453);
float dist=length(local-float2(h-.5,h2-.5)*.65);
float aa=max(length(fwidth(uv))*.5,.012);
float star=(1-smoothstep(.018,.018+aa,dist))*step(.78,h);
color+=star*lerp(float3(.19,.27,.40),float3(.48,.44,.35),h2);
float a=dot(d,moon),disc=smoothstep(cos(.065),cos(.063),a);
float2 q=float2(d.x,dot(d,float3(0,.3420201,.9396926)))/.065;
float maria=.16*exp(-dot(q-float2(-.32,.25),q-float2(-.32,.25))*8)
 +.13*exp(-dot(q-float2(.23,-.16),q-float2(.23,-.16))*14)
 +.10*exp(-dot(q-float2(.37,.42),q-float2(.37,.42))*25);
float relief=.88-maria;
for(int i=0;i<28;i++) {
 float2 h=frac(sin(float2(i*127.1+19.3,i*311.7+47.8))*43758.5453);
 float2 center=(h-.5)*1.75;
 float radius=.035+.11*frac(sin(i*74.7+2.3)*27831.7);
 float r=length(q-center)/radius;
 relief-=.07*(1-smoothstep(.55,.9,r));
 relief+=.06*exp(-pow((r-1)*9,2));
}
float grit=frac(sin(dot(floor(q*180),float2(127.1,311.7)))*43758.5453);
relief=saturate(relief+.018*(grit-.5));
float limb=sqrt(saturate(1-dot(q,q)));
float3 lunar=float3(.55,.60,.65)*relief*(.65+.35*limb);
float halo=pow(saturate(a),340)*.016;
return lerp(color,lunar,disc)+float3(.50,.60,.85)*halo;
''')
lib.connect_material_property(n,'',unreal.MaterialProperty.MP_EMISSIVE_COLOR)
lib.recompile_material(m);unreal.EditorAssetLibrary.save_loaded_asset(m)
unreal.log('VALKYRIE_NIGHT_SKY_READY')
unreal.SystemLibrary.quit_editor()
