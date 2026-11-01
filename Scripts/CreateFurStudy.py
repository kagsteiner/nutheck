"""Reuse dog/cat meshes; compare smooth, brush texture and a few coat clumps."""
import bpy,bmesh,math,json
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'Art/FurStudy';OUT.mkdir(parents=True,exist_ok=True)
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)

brush=bpy.data.images.load(str(OUT/'Textures/FurBrush.png'));brush.colorspace_settings.name='Non-Color'
normal=bpy.data.images.load(str(OUT/'Textures/FurBrushNormal.png'));normal.colorspace_settings.name='Non-Color'
coat_dog={'ginger','ginger_light','cream'}
coat_cat={'cat_orange','cat_peach','cat_cream'}
stats=[];groups={}

def fur_material(source):
    mat=source.copy();mat.name='Fur_'+source.name
    nodes=mat.node_tree.nodes;links=mat.node_tree.links
    shader=nodes.get('Principled BSDF');shader.inputs['Roughness'].default_value=.82
    pigment=nodes.get('Pigment')
    if not pigment: pigment=nodes.new('ShaderNodeVertexColor');pigment.layer_name='Paint'
    tex=nodes.new('ShaderNodeTexImage');tex.image=brush;tex.interpolation='Linear';tex.extension='REPEAT'
    amount=nodes.new('ShaderNodeMath');amount.operation='MULTIPLY';amount.inputs[1].default_value=2
    links.new(tex.outputs['Color'],amount.inputs[0])
    mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1
    links.new(pigment.outputs['Color'],mix.inputs[1]);links.new(amount.outputs[0],mix.inputs[2]);links.new(mix.outputs[0],shader.inputs['Base Color'])
    norm=nodes.new('ShaderNodeTexImage');norm.image=normal;norm.interpolation='Linear';norm.extension='REPEAT'
    bump=nodes.new('ShaderNodeNormalMap');bump.inputs['Strength'].default_value=1
    links.new(norm.outputs['Color'],bump.inputs['Color']);links.new(bump.outputs['Normal'],shader.inputs['Normal'])
    return mat

def coat_uv(obj):
    mesh=obj.data
    for layer in list(mesh.uv_layers):mesh.uv_layers.remove(layer)
    uv=mesh.uv_layers.new(name='FurFlow')
    for face in mesh.polygons:
        n=(obj.matrix_world.to_3x3()@face.normal).normalized()
        for index in face.loop_indices:
            p=obj.matrix_world@mesh.vertices[mesh.loops[index].vertex_index].co
            # Four repeats/metre gives short broad strokes, rather than single hairs.
            if 'tail' in obj.name or p.z<(.20 if 'little_dog' in obj.name else .18):
                a,b=p.z,(p.x if abs(n.y)>.5 else p.y)
            elif abs(n.z)>.5:a,b=p.x,p.y
            elif abs(n.y)>.5:a,b=p.x,p.z
            else:a,b=p.z,p.y
            uv.data[index].uv=(a*4,b*4)

def tuft(name,base,tip,width,thickness,color,material):
    base=Vector(base);tip=Vector(tip);axis=(tip-base).normalized()
    right=axis.cross(Vector((0,0,1)))
    if right.length<.01:right=axis.cross(Vector((0,1,0)))
    right.normalize();up=axis.cross(right).normalized()
    verts=[base+right*width,base-right*width,base+up*thickness,base-up*thickness,
           tip+right*width*.18,tip-right*width*.18]
    faces=[(0,2,4),(2,1,5,4),(1,3,5),(3,0,4,5),(0,3,1,2)]
    mesh=bpy.data.meshes.new(name);mesh.from_pydata(verts,[],faces);mesh.update()
    obj=bpy.data.objects.new(name,mesh);bpy.context.scene.collection.objects.link(obj)
    obj.data.materials.append(material)
    for face in mesh.polygons:face.use_smooth=True
    topology=bmesh.new();topology.from_mesh(mesh);bmesh.ops.recalc_face_normals(topology,faces=list(topology.faces));topology.to_mesh(mesh);topology.free()
    paint=mesh.color_attributes.new(name='Paint',type='FLOAT_COLOR',domain='CORNER');mesh.color_attributes.active_color=paint
    for item in paint.data:item.color=(*color,1)
    coat_uv(obj);return obj

for species,blend in [('little_dog','CreatureInterpretations.blend'),('housecat','CreatureBatch4.blend')]:
    with bpy.data.libraries.load(str(ROOT/'Art/CreatureInterpretations'/blend),link=False) as (source,loaded):
        loaded.objects=[n for n in source.objects if n.startswith(species+'_')]
    originals=list(loaded.objects)
    for obj in originals:bpy.context.scene.collection.objects.link(obj);obj.hide_render=False;obj.hide_viewport=False
    bpy.context.view_layer.update()
    for variant in ['smooth','painted','tufted']:
        key=species+'_'+variant;parts=[];coats=[]
        for original in originals:
            obj=original.copy();obj.data=original.data.copy();obj.name=key+'_'+original.name
            bpy.context.scene.collection.objects.link(obj);obj.hide_render=False;obj.hide_viewport=False;parts.append(obj)
            obj['study_key']=key
            pigment=original.get('pigment','')
            # Leave eyes, nose, ear linings, mouth, toe creases and whiskers alone.
            is_coat=pigment in (coat_dog if species=='little_dog' else coat_cat) and not any(s in original.name for s in ['eye','glint','whisker'])
            if is_coat:
                coats.append(obj)
                if variant!='smooth':
                    coat_uv(obj)
                    for i,mat in enumerate(list(obj.data.materials)):obj.data.materials[i]=fur_material(mat)
                    obj['fur_surface']=True
        if variant=='tufted':
            mat=coats[0].data.materials[0]
            # Broad, low-sided clumps at coat breaks; no strands, shells or cards.
            positions=[]
            if species=='little_dog':
                for side in [-1,1]:
                    for j in range(3):positions.append(((-.205,side*.108,.43-j*.027),(-.145,side*.15,.385-j*.027),.025,.009,(.56,.18,.035)))
                    positions.extend([((-.295,side*.087,.57),(-.24,side*.14,.535),.022,.009,(.57,.19,.035)),
                                      ((.29,side*.025,.48),(.33,side*.07,.535),.022,.009,(.72,.29,.065))])
            else:
                for side in [-1,1]:
                    positions.extend([((-.20,side*.070,.372),(-.16,side*.093,.355),.014,.005,(.85,.22,.015)),
                                      ((.16,side*.075,.31),(.20,side*.095,.29),.014,.005,(.84,.37,.12))])
            for i,(a,b,w,t,c) in enumerate(positions):
                obj=tuft(key+'_clump_'+str(i),a,b,w,t,c,mat);obj['study_key']=key;obj['fur_surface']=True;parts.append(obj)
        bpy.context.view_layer.update()
        for obj in parts:obj.select_set(False)
        groups[key]=parts
        triangles=sum(sum(len(p.vertices)-2 for p in o.data.polygons) for o in parts)
        stats.append(dict(key=key,species=species,variant=variant,parts=len(parts),triangles=triangles,fur_parts=sum(bool(o.get('fur_surface')) for o in parts)))
    for obj in originals:bpy.data.objects.remove(obj,do_unlink=True)

for key,parts in groups.items():
    bpy.ops.object.select_all(action='DESELECT')
    for obj in parts:obj.hide_render=False;obj.hide_viewport=False;obj.select_set(True)
    bpy.context.view_layer.objects.active=parts[0]
    bpy.ops.export_scene.fbx(filepath=str(OUT/(key+'.fbx')),use_selection=True,object_types={'MESH'},apply_unit_scale=True,
        axis_forward='-Y',axis_up='Z',add_leaf_bones=False,bake_anim=False,mesh_smooth_type='FACE')

scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=24;scene.render.film_transparent=True
scene.render.image_settings.color_mode='RGBA'
world=bpy.data.worlds.new('Fur neutral studio');scene.world=world;world.use_nodes=True
world.node_tree.nodes['Background'].inputs[0].default_value=(.12,.14,.17,1);world.node_tree.nodes['Background'].inputs[1].default_value=.45
for at,power,size in [((-2,-3,5),450,4),((3,2,4),300,3)]:
    light=bpy.data.lights.new('Softbox','AREA');light.energy=power;light.size=size
    obj=bpy.data.objects.new('Softbox',light);scene.collection.objects.link(obj);obj.location=at
    obj.rotation_euler=(Vector((0,0,.4))-obj.location).to_track_quat('-Z','Y').to_euler()
data=bpy.data.cameras.new('Fur camera');camera=bpy.data.objects.new('Fur camera',data);scene.collection.objects.link(camera);scene.camera=camera;data.type='ORTHO'
for key,parts in groups.items():
    for group,objects in groups.items():
        for obj in objects:obj.hide_render=group!=key
    camera.location=(-2.8,-3.7,2.25);target=Vector((0,0,.36))
    camera.rotation_euler=(target-camera.location).to_track_quat('-Z','Y').to_euler();data.ortho_scale=1.15
    for view,pixels in [('close',700),('gameplay',64),('level',16)]:
        scene.render.resolution_x=pixels;scene.render.resolution_y=pixels;scene.render.resolution_percentage=100
        scene.render.filepath=str(OUT/(key+'-'+view+'.png'));bpy.ops.render.render(write_still=True)
for key,parts in groups.items():
    collection=bpy.data.collections.new(key);scene.collection.children.link(collection)
    for obj in parts:
        for parent in list(obj.users_collection):parent.objects.unlink(obj)
        collection.objects.link(obj);obj.hide_render=key!='little_dog_painted'
    collection.hide_viewport=key!='little_dog_painted'
for row in stats:
    base=next(s['triangles'] for s in stats if s['species']==row['species'] and s['variant']=='smooth')
    row['added_triangles']=row['triangles']-base
    assert row['added_triangles']<=160
    if row['variant']=='painted':assert row['added_triangles']==0
(OUT/'study-manifest.json').write_text(json.dumps(stats,indent=2))
scene.render.resolution_x=700;scene.render.resolution_y=700
brush.filepath='//Textures/FurBrush.png';normal.filepath='//Textures/FurBrushNormal.png'
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'FurStudy.blend'))
print('FUR_STUDY_READY variants=6 texture_maps=2',flush=True)
