"""One-time saved-scene review fix: expose fitted manes and attach inner ear leaves."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from CreatureGeometry import *
import CreatureGeometry as geo
from EquineFamily import fitted_mane,fit_ear_lining
bpy.ops.wm.open_mainfile(filepath=str(OUT/'CreatureBatch11.blend'))
for col in bpy.data.collections:col.hide_viewport=False
for obj in bpy.data.objects:obj.hide_viewport=False
for name in ['equine_mane','warhorse_mane','equine_inner']:
    MATS[name]=bpy.data.materials[name];COLORS[name]=tuple(MATS[name].diffuse_color[:3])
for obj in list(bpy.data.objects):
    if obj.type!='MESH':continue
    if obj.get('mane_mass') or obj.name.startswith(tuple(k+'_ear_lining' for k in ['pony','horse','warhorse'])):
        bpy.data.objects.remove(obj,do_unlink=True)
    else:obj['preserve_paint']=True
bpy.context.view_layer.update()
new=[]
for key in ['pony','horse','warhorse']:
    geo.GROUP=key;body=bpy.data.objects[key+'_continuous_anatomy']
    new.append(fitted_mane(key,body,'warhorse_mane' if key=='warhorse' else 'equine_mane'))
    for side in [-1,1]:
        ear_obj=next(o for o in bpy.data.objects if o.get('creature')==key and o.name.startswith(key+'_ear') and not 'lining' in o.name and (1 if o.data.vertices[0].co.y>0 else -1)==side)
        base=(body['head_x']+.017,side*body['head_length']*.36,body['head_z']+body['head_length']*.53)
        height={'pony':.128,'horse':.143,'warhorse':.147}[key]
        ear_obj['ear_base']=list(base);ear_obj['ear_height']=height;ear_obj['ear_side']=side
        new.append(fit_ear_lining(ear_obj,base,height,side))
pipeline=Path(__file__).with_name('CreatureBatch2Pipeline.py').read_text(encoding='utf-8')
exec(compile(pipeline[:pipeline.index("GROUPS=globals().get")],'paint_fitted_parts','exec'))
for obj in new:
    collection=bpy.data.collections[obj['creature']]
    for parent in list(obj.users_collection):parent.objects.unlink(obj)
    collection.objects.link(obj)
for key in ['pony','horse','warhorse']:
    bpy.ops.object.select_all(action='DESELECT');parts=[o for o in bpy.data.objects if o.type=='MESH' and o.get('creature')==key]
    for obj in parts:obj.select_set(True)
    bpy.context.view_layer.objects.active=parts[0]
    bpy.ops.export_scene.fbx(filepath=str(OUT/(key+'.fbx')),use_selection=True,object_types={'MESH'},apply_unit_scale=True,axis_forward='-Y',axis_up='Z',add_leaf_bones=False,bake_anim=False,mesh_smooth_type='FACE')
for key in ['pony','horse','warhorse']:
    bpy.data.collections[key].hide_viewport=key!='pony'
    for obj in bpy.data.collections[key].objects:obj.hide_render=key!='pony'
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'CreatureBatch11.blend'))
print('CREATURE_BATCH11_REFINE_READY fitted_manes=3 fitted_ear_linings=6',flush=True)
