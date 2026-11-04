"""Valkyrie quest: opaque readable ice, volcanic rock, sanctuary stone and lava."""
import unreal
lib=unreal.MaterialEditingLibrary;tools=unreal.AssetToolsHelpers.get_asset_tools()
for key,low,high,rough,metal in [
 ('Ice',(.10,.28,.40),(.63,.83,.90),.38,0),('Snow',(.65,.75,.82),(.91,.95,1),.91,0),
 ('Sanctuary',(.23,.29,.34),(.55,.62,.67),.8,0),('SanctuaryFloor',(.14,.20,.24),(.35,.43,.48),.84,0),
 ('ColdRock',(.10,.14,.17),(.24,.30,.33),.92,0),('Basalt',(.025,.026,.03),(.13,.115,.105),.94,0),
 ('BasaltFloor',(.035,.03,.027),(.16,.12,.09),.93,0),('Lava',(.025,.009,.003),(1,.21,.015),.8,0),
 ('Water',(.025,.09,.13),(.11,.30,.36),.19,0),('Bronze',(.20,.11,.035),(.53,.34,.11),.32,.8)]:
 dest='/Game/ValkyrieQuest';name='M_'+key
 m=unreal.load_asset(dest+'/'+name) or tools.create_asset(name,dest,unreal.Material,unreal.MaterialFactoryNew())
 lib.delete_all_material_expressions(m);m.set_editor_property('used_with_instanced_static_meshes',True)
 def node(cls):return lib.create_material_expression(m,cls)
 def link(a,b,pin):assert lib.connect_material_expressions(a,'',b,pin)
 pos=node(unreal.MaterialExpressionWorldPosition);time=node(unreal.MaterialExpressionTime)
 c=node(unreal.MaterialExpressionCustom);entries=[]
 for n in ['P','T']:
  e=unreal.CustomInput();e.set_editor_property('input_name',n);entries.append(e)
 c.set_editor_property('inputs',entries);link(pos,c,'P');link(time,c,'T')
 c.set_editor_property('output_type',unreal.CustomMaterialOutputType.CMOT_FLOAT3)
 lo='float3'+str(tuple(low));hi='float3'+str(tuple(high))
 # A deterministic world-space cellular fracture field, independent of tile seams.
 code='float2 q=P.xy*.035;'
 if key=='Lava':code+='q+=float2(sin(T*.18+q.y*.2),cos(T*.13+q.x*.2))*.12;'
 code+='float2 b=floor(q);float f1=10,f2=10; for(int x=-1;x<=1;x++)for(int y=-1;y<=1;y++){float2 a=b+float2(x,y);float2 h=frac(sin(float2(dot(a,float2(127.1,311.7)),dot(a,float2(269.5,183.3))))*43758.5453);float d=length(a+h-q);if(d<f1){f2=f1;f1=d;}else f2=min(f2,d);}float seam=1-smoothstep(.015,.07,f2-f1);float grain=.5+.5*sin(P.x*.16+sin(P.y*.23))*sin(P.z*.31+P.y*.17);'
 if key=='Lava':code+=f'return lerp({lo},{hi},seam)*(.85+.15*sin(T*.8+P.x*.02));'
 elif key=='Ice':code+=f'return lerp({lo},{hi},saturate(.24+grain*.22+seam*.7));'
 else:code+=f'return lerp({lo},{hi},grain*.6)*(1-seam*.15);'
 c.set_editor_property('code',code)
 memory=node(unreal.MaterialExpressionScalarParameter);memory.set_editor_property('parameter_name','Memory');memory.set_editor_property('default_value',1.)
 mul=node(unreal.MaterialExpressionMultiply);link(c,mul,'A');link(memory,mul,'B');lib.connect_material_property(mul,'',unreal.MaterialProperty.MP_BASE_COLOR)
 if key=='Lava':
  # Emission cannot cast light into undiscovered areas; memory emission is disabled.
  power=node(unreal.MaterialExpressionCustom);e=unreal.CustomInput();e.set_editor_property('input_name','M');power.set_editor_property('inputs',[e]);link(memory,power,'M');power.set_editor_property('code','return M>.9 ? 1.8 : 0;');power.set_editor_property('output_type',unreal.CustomMaterialOutputType.CMOT_FLOAT1)
  glow=node(unreal.MaterialExpressionMultiply);link(c,glow,'A');link(power,glow,'B');lib.connect_material_property(glow,'',unreal.MaterialProperty.MP_EMISSIVE_COLOR)
 for prop,value in [(unreal.MaterialProperty.MP_ROUGHNESS,rough),(unreal.MaterialProperty.MP_METALLIC,metal),(unreal.MaterialProperty.MP_SPECULAR,.18)]:
  v=node(unreal.MaterialExpressionConstant);v.set_editor_property('r',value);lib.connect_material_property(v,'',prop)
 lib.recompile_material(m);unreal.EditorAssetLibrary.save_loaded_asset(m)
 unreal.log('VALKYRIE_MATERIAL_READY '+key)
