"""Saved feline corrections: joined lynx tufts, painted cheeks and softer rosettes."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from CreatureGeometry import *
import CreatureGeometry as geo
from WildCatPaint import wild_cat_pigment
bpy.ops.wm.open_mainfile(filepath=str(OUT/'CreatureBatch9.blend'))
for col in bpy.data.collections:col.hide_viewport=False
for obj in bpy.data.objects:obj.hide_viewport=False
bpy.context.view_layer.update()
COLORS.update(jaguar_gold=(.80,.28,.024),jaguar_muzzle=(.80,.61,.34),jaguar_spot=(.055,.022,.008),
    lynx_coat=(.68,.235,.030),lynx_pale=(.83,.48,.25),wild_cat_dark=(.014,.017,.015))
for obj in list(bpy.data.objects):
    if obj.name.startswith(('lynx_cheek_ruff','lynx_ear_tuft')):bpy.data.objects.remove(obj,do_unlink=True)
    elif obj.get('creature') in {'jaguar','lynx','panther'} and any(obj.name.startswith(obj['creature']+'_'+s) for s in ['triangular_nose','philtrum','mouth']):
        obj.location.x-=.006
geo.GROUP='lynx';MATS['wild_cat_dark']=bpy.data.materials['wild_cat_dark']
before=set(bpy.data.objects)
length=.260;head=.127;width=.109;hx=-length*.61-.075;hz=.275+.130+.105
for side in [-1,1]:
    tip=(hx+.020,side*width*.71,hz+head*.60+.104)
    limb('ear_tuft',[(tip[0]-.004,tip[1]-side*.004,tip[2]-.035),
        (tip[0]+.004,tip[1]+side*.006,tip[2]+.030)],[.006,.0008],'wild_cat_dark')
new=list(set(bpy.data.objects)-before)
for obj in new:
    for parent in list(obj.users_collection):parent.objects.unlink(obj)
    bpy.data.collections['lynx'].objects.link(obj)
repaint=[o for o in bpy.data.objects if o.type=='MESH' and
    (o.get('coat_marking') in {'jaguar_rosettes','jaguar_tail','lynx_flank','lynx_tail_tip'} or o in new)]
for obj in repaint:
    mesh=obj.data;base=COLORS[obj['pigment']]
    attr=mesh.color_attributes.get('Paint') or mesh.color_attributes.new(name='Paint',type='FLOAT_COLOR',domain='CORNER')
    mesh.color_attributes.active_color=attr
    lo=min(v.co.z for v in mesh.vertices);hi=max(v.co.z for v in mesh.vertices)
    for loop in mesh.loops:
        v=mesh.vertices[loop.vertex_index];p=obj.matrix_world@v.co
        color=wild_cat_pigment(obj,p,base,COLORS)
        shade=.79+.19*(v.co.z-lo)/max(.01,hi-lo)+.018*math.sin(p.x*28+p.y*21+p.z*13)
        attr.data[loop.index].color=(*(c*shade for c in color),1)
    if obj in new:
        bm=bmesh.new();bm.from_mesh(mesh);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(mesh);bm.free()
    print('FELINE_REPAINT '+obj.name+' min_red='+str(min(c.color[0] for c in attr.data)),flush=True)
for key in ['jaguar','lynx','panther']:
    bpy.ops.object.select_all(action='DESELECT')
    parts=[o for o in bpy.data.objects if o.type=='MESH' and o.get('creature')==key]
    for obj in parts:obj.hide_render=False;obj.select_set(True)
    bpy.context.view_layer.objects.active=parts[0]
    bpy.ops.export_scene.fbx(filepath=str(OUT/(key+'.fbx')),use_selection=True,object_types={'MESH'},apply_unit_scale=True,
        axis_forward='-Y',axis_up='Z',add_leaf_bones=False,bake_anim=False,mesh_smooth_type='FACE')
for key in ['jaguar','lynx','panther']:
    bpy.data.collections[key].hide_viewport=key!='jaguar'
    for obj in bpy.data.objects:
        if obj.get('creature')==key:obj.hide_render=key!='jaguar'
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'CreatureBatch9.blend'))
print('CREATURE_BATCH9_REFINEMENT_READY',flush=True)
