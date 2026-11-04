"""Reload centaur paint/materials and inventory statue-compatible mesh coverage."""
import unreal,json,re
from pathlib import Path
r=Path(unreal.Paths.project_dir()).resolve();report={}
for key in ['plains_centaur','forest_centaur','mountain_centaur']:
 path='/Game/CreatureInterpretations/Meshes/SM_'+key;mesh=unreal.load_asset(path);assert mesh
 assert unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem).has_vertex_colors(mesh)
 slots=[]
 for slot in mesh.static_materials:
  name=str(slot.get_editor_property('imported_material_slot_name'));m=slot.get_editor_property('material_interface');assert m
  assert m.get_name()==('M_Eye' if name in ['human_dark','human_sclera','human_blue','glint'] else 'M_Paint'),(key,name,m.get_name())
  slots.append(dict(source=name,material=m.get_path_name()))
 report[key]=dict(asset=path,vertex_colors=True,slots=slots)
for name in ['M_WhiteMarble','M_WhiteMarbleMemory']:
 m=unreal.load_asset('/Game/Statues/'+name);assert m
 lib=unreal.MaterialEditingLibrary
 color=lib.get_material_property_input_node(m,unreal.MaterialProperty.MP_BASE_COLOR);assert isinstance(color,unreal.MaterialExpressionConstant3Vector),(name,color)
 value=color.get_editor_property('constant');expected=.20 if name.endswith('Memory') else 1.
 assert all(abs(c-expected)<1e-6 for c in [value.r,value.g,value.b]),(name,value)
 for prop,expected_scalar in [(unreal.MaterialProperty.MP_ROUGHNESS,.28),(unreal.MaterialProperty.MP_METALLIC,0.),(unreal.MaterialProperty.MP_SPECULAR,.5)]:
  node=lib.get_material_property_input_node(m,prop);assert isinstance(node,unreal.MaterialExpressionConstant),(name,prop,node)
  assert abs(node.get_editor_property('r')-expected_scalar)<1e-6,(name,prop)
 assert b'MaterialExpressionVertexColor' not in (r/'Content/Statues'/(name+'.uasset')).read_bytes()
 report[name]=dict(asset=m.get_path_name(),expressions=lib.get_num_material_expressions(m),verified_constant_rgb=[value.r,value.g,value.b],roughness=.28,metallic=0.,no_vertex_color_input=True)
supported=[];missing=[]
for row in json.loads((r/'Art/CreatureCatalogue/creatures.json').read_text(encoding='utf-8'))['creatures']:
 for female in [False,True]:
  key=re.sub(r'[^a-z0-9]+','_',row['name'].lower()).strip('_')
  if female and unreal.EditorAssetLibrary.does_asset_exist('/Game/CreatureInterpretations/Meshes/SM_'+key+'_female'):key+='_female'
  candidates=[('/Game/CreatureInterpretations/Meshes/SM_'+key,'sculpted'),('/Game/CreatureInterpretations/Meshes/SM_'+key+('_female_human' if female else '_male_human'),'human player'),('/Game/DefaultTiles/Meshes/SM_'+key+('_female' if female else '_male'),'legacy volume')]
  found=next(((p,t) for p,t in candidates if unreal.EditorAssetLibrary.does_asset_exist(p)),None)
  if found:supported.append(dict(id=row['id'],name=row['name'],female=female,mesh=found[0],kind=found[1]))
  else:missing.append(dict(id=row['id'],name=row['name'],female=female,fallback='native official statue tile'))
report.update(status='PASS',supported_statue_display_forms=len(supported),supported_creature_ids=len({c['id'] for c in supported}),missing_model_display_forms=len(missing))
(r/'Art/CreatureInterpretations/centaurs-unreal-assets.json').write_text(json.dumps(report,indent=2))
(r/'Art/CreatureInterpretations/statue-model-coverage.json').write_text(json.dumps(dict(supported=supported,native_tile_fallback=missing),indent=2))
unreal.log('CENTAUR_SAVED_ASSETS_PASS '+json.dumps(report))
