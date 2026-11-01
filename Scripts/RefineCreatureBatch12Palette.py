"""Saved-scene paint-only review correction: tails follow coats, not contrasting manes."""
import sys,hashlib,struct
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from CreatureGeometry import *
bpy.ops.wm.open_mainfile(filepath=str(OUT/'CreatureBatch12.blend'))
for col in bpy.data.collections:col.hide_viewport=False
for obj in bpy.data.objects:obj.hide_viewport=False
bpy.context.view_layer.update()
def positions():
    return hashlib.sha256(b''.join(struct.pack('<3f',*v.co) for o in sorted(bpy.data.objects,key=lambda o:o.name) if o.type=='MESH' for v in o.data.vertices)).hexdigest()
before=positions()
for key,color in [('white_unicorn',(.72,.76,.75)),('gray_unicorn',(.25,.36,.46)),('black_unicorn',(.024,.025,.025))]:
    tail=next(o for o in bpy.data.objects if o.get('creature')==key and o.get('tail_form'))
    pigment='unicorn_'+key.split('_')[0]+'_tail';tail['pigment']=pigment
    mat=tail.data.materials[0].copy();mat.name=pigment;mat.diffuse_color=(*color,1);tail.data.materials.clear();tail.data.materials.append(mat)
    mesh=tail.data;paint=mesh.color_attributes['Paint'];zmin=min(v.co.z for v in mesh.vertices);zmax=max(v.co.z for v in mesh.vertices)
    for loop in mesh.loops:
        v=mesh.vertices[loop.vertex_index];p=tail.matrix_world@v.co
        shade=.79+.19*(v.co.z-zmin)/max(.01,zmax-zmin)+.018*math.sin(p.x*28+p.y*21+p.z*13)
        paint.data[loop.index].color=(*(c*shade for c in color),1)
    bpy.ops.object.select_all(action='DESELECT');parts=[o for o in bpy.data.objects if o.type=='MESH' and o.get('creature')==key]
    for obj in parts:obj.select_set(True)
    bpy.context.view_layer.objects.active=parts[0]
    bpy.ops.export_scene.fbx(filepath=str(OUT/(key+'.fbx')),use_selection=True,object_types={'MESH'},apply_unit_scale=True,axis_forward='-Y',axis_up='Z',add_leaf_bones=False,bake_anim=False,mesh_smooth_type='FACE')
assert positions()==before
for key in ['white_unicorn','gray_unicorn','black_unicorn']:
    bpy.data.collections[key].hide_viewport=key!='white_unicorn'
    for obj in bpy.data.collections[key].objects:obj.hide_render=key!='white_unicorn'
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'CreatureBatch12.blend'))
print('CREATURE_BATCH12_PALETTE_REVIEW_READY geometry_unchanged=True coat_tails=3',flush=True)
