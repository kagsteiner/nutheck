"""Blender: three complete anatomical interpretations, plus reverse projections.
Actual geometry/render results are kept separate from AI concept artwork.
"""
import bpy
import bmesh
import json
import math
import re
from pathlib import Path
from mathutils import Vector

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'Art/CreatureInterpretations'; OUT.mkdir(parents=True,exist_ok=True)
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
bpy.context.scene.unit_settings.system='METRIC'; bpy.context.scene.unit_settings.scale_length=1
COLORS={
 'shell':(.23,.075,.022),'shell_light':(.43,.17,.045),'joint':(.055,.025,.015),
 'cyan':(.025,.49,.70),'black':(.008,.012,.014),'glint':(.72,.77,.72),
 'ginger':(.58,.19,.035),'ginger_light':(.78,.32,.07),'cream':(.77,.63,.37),
 'tongue':(.55,.025,.035),'skin':(.37,.16,.065),'skin_dark':(.19,.065,.025),
 'magenta':(.58,.012,.37),'cloth_dark':(.22,.006,.095),'leather':(.085,.032,.012),
 'cap':(.23,.085,.025),'green':(.02,.65,.035),'steel':(.31,.37,.36),'brass':(.42,.22,.04),
}
MATS={}
for key,color in COLORS.items():
    mat=bpy.data.materials.new(key); mat.use_nodes=True; mat.diffuse_color=(*color,1)
    shader=mat.node_tree.nodes.get('Principled BSDF')
    shader.inputs['Base Color'].default_value=(*color,1)
    shader.inputs['Roughness'].default_value=.48 if key in ['shell','shell_light','black','steel','brass'] else .82
    shader.inputs['Metallic'].default_value=.55 if key in ['steel','brass'] else 0
    MATS[key]=mat
GROUP='giant_ant'

def finish(obj,name,color):
    obj.name=GROUP+'_'+name; obj['creature']=GROUP; obj['pigment']=color
    obj.data.materials.append(MATS[color]); return obj

def orb(name,at,size,color):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32,ring_count=20,radius=1,location=at)
    obj=bpy.context.object; obj.scale=size
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    for polygon in obj.data.polygons: polygon.use_smooth=True
    return finish(obj,name,color)

def box(name,at,size,color,bevel=.018):
    bpy.ops.mesh.primitive_cube_add(size=1,location=at); obj=bpy.context.object; obj.dimensions=size
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    mod=obj.modifiers.new('Rounded crafted edge','BEVEL'); mod.width=bevel; mod.segments=3
    return finish(obj,name,color)

def limb(name,points,radii,color):
    # Smooth, joined tube with variable section radii; supports bent anatomy.
    vertices=[]; faces=[]; sides=12
    for i,point in enumerate(points):
        direction=Vector(points[min(i+1,len(points)-1)])-Vector(points[max(0,i-1)])
        direction.normalize(); helper=Vector((0,0,1)) if abs(direction.z)<.9 else Vector((0,1,0))
        right=direction.cross(helper).normalized(); up=direction.cross(right).normalized()
        for j in range(sides):
            theta=math.tau*j/sides
            vertices.append(Vector(point)+radii[i]*(right*math.cos(theta)+up*math.sin(theta)))
    for i in range(len(points)-1):
        for j in range(sides):
            a=i*sides+j; b=i*sides+(j+1)%sides
            faces.append((a,b,b+sides,a+sides))
    faces+=[tuple(reversed(range(sides))),tuple((len(points)-1)*sides+j for j in range(sides))]
    mesh=bpy.data.meshes.new(name); mesh.from_pydata(vertices,[],faces); mesh.update()
    obj=bpy.data.objects.new(name,mesh); bpy.context.collection.objects.link(obj)
    for polygon in mesh.polygons: polygon.use_smooth=True
    return finish(obj,name,color)

def sculpt_union(objects,name,color,voxel=.012):
    bpy.ops.object.select_all(action='DESELECT')
    for obj in objects: obj.select_set(True)
    bpy.context.view_layer.objects.active=objects[0]; bpy.ops.object.join(); obj=bpy.context.object
    obj.data.remesh_voxel_size=voxel; bpy.ops.object.voxel_remesh()
    mod=obj.modifiers.new('Sculpt surface relaxation','SMOOTH'); mod.factor=.65; mod.iterations=4
    bpy.ops.object.modifier_apply(modifier=mod.name)
    obj.name=GROUP+'_'+name; obj['creature']=GROUP; obj['pigment']=color
    obj.data.materials.clear(); obj.data.materials.append(MATS[color])
    for polygon in obj.data.polygons: polygon.use_smooth=True
    return obj

def ear(name,base,tip,width,depth,color):
    x,y,z=base; tx,ty,tz=tip
    verts=[(x-width,y,z),(x+width,y,z),(tx,ty,tz),(x,y+depth,z+.04)]
    mesh=bpy.data.meshes.new(name); mesh.from_pydata(verts,[],[(0,1,2),(0,3,1),(1,3,2),(2,3,0)]); mesh.update()
    obj=bpy.data.objects.new(name,mesh); bpy.context.collection.objects.link(obj)
    mod=obj.modifiers.new('Soft ear edge','BEVEL'); mod.width=.012; mod.segments=3
    return finish(obj,name,color)

def cloth(name,bottom,top,lower,upper,color,cape=False):
    verts=[]; faces=[]; n=48
    for ring in range(12):
        t=ring/11; radius=lower*(1-t)+upper*t
        for i in range(n+1):
            theta=i/n*(math.pi if cape else math.tau)
            fold=.023*math.cos(theta*10)*(1-.8*t)
            verts.append(((radius+fold)*math.cos(theta),.055+(radius+fold)*math.sin(theta)*.65,
                bottom+(top-bottom)*t+.015*math.cos(theta*7)*(1-t)))
    for ring in range(11):
        for i in range(n):
            a=ring*(n+1)+i; faces.append((a,a+1,a+n+2,a+n+1))
    mesh=bpy.data.meshes.new(name); mesh.from_pydata(verts,[],faces); mesh.update()
    obj=bpy.data.objects.new(name,mesh); bpy.context.collection.objects.link(obj)
    for polygon in mesh.polygons: polygon.use_smooth=True
    mod=obj.modifiers.new('Fabric thickness','SOLIDIFY'); mod.thickness=.012
    return finish(obj,name,color)

# GIANT ANT: all six legs originate on the thorax, behind the broad biting head.
orb('gaster',(.25,0,.26),(.24,.15,.17),'shell')
orb('thorax',(-.055,0,.27),(.15,.105,.12),'shell_light')
orb('petiole',(.105,0,.25),(.07,.065,.06),'joint')
head=orb('head',(-.285,0,.255),(.16,.145,.115),'shell_light')
for dx in [.19,.29,.38]:
    orb('gaster_ridge',(dx,0,.275),(.022,.147,.145),'shell_light')
for i,dx in enumerate([-.13,-.045,.04]):
    for side in [-1,1]:
        splay=[-.16,0,.16][i]
        points=[(dx,side*.075,.27),(dx+splay,side*.24,.30),(dx+splay+.035,side*.39,.12),(dx+splay-.02,side*.43,.027)]
        limb('leg_%d_%d'%(i,side),points,[.027,.024,.016,.007],'joint')
        orb('leg_joint',(dx+splay,side*.24,.30),(.03,.028,.027),'shell')
for side in [-1,1]:
    orb('compound_eye',(-.31,side*.125,.30),(.055,.025,.046),'black')
    orb('cool_eye_glint',(-.335,side*.144,.307),(.018,.006,.012),'cyan')
    limb('antenna',[(-.34,side*.075,.34),(-.44,side*.18,.43),(-.56,side*.20,.40)],[.012,.009,.006],'shell')
    limb('mandible',[(-.39,side*.085,.23),(-.49,side*.10,.22),(-.54,side*.025,.23)],[.041,.032,.005],'shell_light')

# LITTLE DOG: continuous torso/neck/hip anatomy, separate coat markings.
GROUP='little_dog'
body=[orb('torso',(0,0,.31),(.27,.13,.155),'ginger'),orb('hip',(.18,0,.30),(.14,.125,.15),'ginger'),
    orb('shoulder',(-.17,0,.34),(.15,.14,.17),'ginger'),orb('neck',(-.23,0,.45),(.105,.11,.16),'ginger'),
    orb('skull',(-.28,-.015,.59),(.14,.115,.13),'ginger')]
for dx in [-.17,.18]:
    for side in [-1,1]:
        # Hocks on rear legs differ from the straighter front wrists.
        points=[(dx,side*.087,.31),(dx+(.055 if dx>0 else 0),side*.10,.18),(dx+.005,side*.11,.055)]
        body.append(limb('leg',points,[.055,.038,.026],'ginger'))
        body.append(orb('paw',(dx-.025,side*.11,.043),(.063,.041,.035),'ginger'))
sculpt_union(body,'continuous_body','ginger',.009)
orb('chest_bib',(-.292,-.005,.37),(.064,.112,.13),'cream')
orb('muzzle',(-.395,-.015,.55),(.095,.077,.052),'cream')
orb('nose',(-.475,-.015,.574),(.030,.042,.025),'black')
limb('mouth',[(-.445,-.07,.54),(-.405,-.078,.531),(-.365,-.075,.535)],[.006,.007,.005],'black')
orb('tongue',(-.423,-.047,.516),(.031,.022,.018),'tongue')
for side in [-1,1]:
    ear('pointed_ear',(-.255,side*.075,.65),(-.22,side*.12,.82),.065,.035,'ginger_light')
    ear('inner_ear',(-.26,side*.067,.667),(-.226,side*.108,.79),.039,.012,'skin')
    orb('eye_white',(-.35,side*.087,.621),(.038,.019,.032),'cream')
    orb('eye',(-.366,side*.10,.622),(.018,.012,.022),'black')
    orb('eye_glint',(-.372,side*.109,.633),(.006,.004,.007),'glint')
    orb('eyebrow',(-.342,side*.085,.659),(.043,.021,.014),'ginger_light')
tail=limb('curved_tail',[(.22,0,.38),(.35,0,.46),(.40,.01,.60),(.34,.015,.69),(.25,.015,.67)],[.065,.06,.05,.033,.008],'ginger_light')
smooth_tail=tail.modifiers.new('Tail curve smoothing','SUBSURF'); smooth_tail.levels=2
for side in [-1,1]:
    for i in range(3):
        limb('ruff_tuft',[(-.20,side*.10,.45-i*.025),(-.13,side*.15,.41-i*.025)],[.035,.003],'ginger_light')

# GOBLIN: interpret the unusual original palette instead of defaulting to green skin.
GROUP='goblin'
for side in [-1,1]:
    limb('leg',[(side*.10,0,.44),(side*.13,-.025,.26),(side*.14,-.035,.10)],[.075,.058,.042],'skin')
    box('boot',(side*.14,-.075,.075),(.17,.24,.15),'leather',.035)
cloth('magenta_tunic',.30,.73,.245,.17,'magenta')
cloth('short_cape',.32,.75,.27,.20,'cloth_dark',True)
orb('shoulders',(0,.015,.72),(.21,.13,.10),'magenta')
headparts=[orb('skull',(0,0,.91),(.19,.145,.185),'skin'),orb('jaw',(0,-.055,.80),(.16,.13,.095),'skin'),
    orb('neck',(0,.015,.75),(.085,.08,.1),'skin'),orb('nose_bridge',(0,-.14,.92),(.055,.065,.11),'skin'),
    orb('hooked_nose',(0,-.205,.86),(.07,.095,.055),'skin')]
for side in [-1,1]: headparts.append(orb('cheek',(side*.12,-.095,.87),(.085,.065,.065),'skin'))
sculpt_union(headparts,'sculpted_head','skin',.007)
for side in [-1,1]:
    ear('large_ear',(side*.21,.015,.92),(side*.41,.025,1.045),.075,.045,'skin')
    ear('inner_ear',(side*.23,-.017,.94),(side*.37,-.013,1.022),.04,.014,'skin_dark')
    brow=orb('brow',(side*.09,-.135,.99),(.10,.041,.034),'skin_dark'); brow.rotation_euler.y=side*.15
    orb('eye_white',(side*.092,-.139,.948),(.047,.025,.031),'cream')
    orb('green_iris',(side*.092,-.162,.946),(.027,.009,.023),'green')
    orb('pupil',(side*.092,-.171,.946),(.009,.004,.018),'black')
    orb('nostril',(side*.038,-.277,.857),(.017,.009,.01),'skin_dark')
    limb('arm',[(side*.18,0,.70),(side*.255,-.025,.56),(side*.30,-.08,.46)],[.058,.049,.038],'skin')
    orb('hand',(side*.30,-.08,.445),(.055,.043,.066),'skin')
    for finger in [-1,0,1]:
        limb('finger',[(side*.32,-.10+finger*.02,.46),(side*.33,-.10+finger*.02,.417)],[.013,.01],'skin')
    limb('fang',[(side*.09,-.17,.812),(side*.088,-.18,.86)],[.023,.003],'cream')
limb('mouth',[(-.12,-.17,.818),(0,-.189,.804),(.12,-.17,.828)],[.009,.012,.006],'skin_dark')
cap=orb('leather_cap',(0,.025,1.055),(.205,.16,.095),'cap'); cap.rotation_euler.y=-.18
limb('cap_tip',[(-.04,.025,1.10),(-.13,.04,1.17),(-.24,.05,1.14)],[.105,.068,.012],'cap')
box('belt',(0,0,.51),(.40,.29,.05),'leather',.013)
box('buckle',(0,-.16,.51),(.066,.027,.055),'brass',.008)
box('dagger_grip',(.30,-.08,.43),(.039,.035,.13),'leather',.009)
box('dagger_guard',(.30,-.08,.365),(.14,.045,.025),'steel',.006)
limb('dagger_blade',[(.30,-.08,.36),(.30,-.08,.17)],[.029,.001],'steel')

# Apply sculpt modifiers and encode the palette/soft painted shading per corner.
bpy.context.view_layer.update()
for obj in list(bpy.context.scene.objects):
    if obj.type!='MESH': continue
    bpy.context.view_layer.objects.active=obj
    for modifier in list(obj.modifiers): bpy.ops.object.modifier_apply(modifier=modifier.name)
    mesh=obj.data; pigment=COLORS[obj['pigment']]
    topology=bmesh.new(); topology.from_mesh(mesh)
    bmesh.ops.recalc_face_normals(topology,faces=list(topology.faces))
    topology.to_mesh(mesh); topology.free()
    paint=mesh.color_attributes.new(name='Paint',type='FLOAT_COLOR',domain='CORNER'); mesh.color_attributes.active_color=paint
    zmin=min(v.co.z for v in mesh.vertices); zmax=max(v.co.z for v in mesh.vertices)
    for loop in mesh.loops:
        v=mesh.vertices[loop.vertex_index]; p=obj.matrix_world@v.co
        shade=.79+.19*(v.co.z-zmin)/max(.01,zmax-zmin)+.018*math.sin(p.x*28+p.y*21+p.z*13)
        paint.data[loop.index].color=(*(max(0,min(1,c*shade)) for c in pigment),1)
    # Blender and UE both use the painted vertex colour as the actual surface.
    for material in mesh.materials:
        shader=material.node_tree.nodes.get('Principled BSDF')
        attr=material.node_tree.nodes.get('Pigment')
        if not attr: attr=material.node_tree.nodes.new('ShaderNodeVertexColor'); attr.name='Pigment'; attr.layer_name='Paint'
        material.node_tree.links.new(attr.outputs['Color'],shader.inputs['Base Color'])

GROUPS=['giant_ant','little_dog','goblin']
objects={key:[o for o in bpy.context.scene.objects if o.get('creature')==key] for key in GROUPS}
for key,parts in objects.items():
    bpy.ops.object.select_all(action='DESELECT')
    for obj in parts: obj.select_set(True)
    bpy.context.view_layer.objects.active=parts[0]
    bpy.ops.export_scene.fbx(filepath=str(OUT/(key+'.fbx')),use_selection=True,object_types={'MESH'},apply_unit_scale=True,
        axis_forward='-Y',axis_up='Z',add_leaf_bones=False,bake_anim=False,mesh_smooth_type='FACE')

# Studio renders and camera-pose search for actual 16x16 reverse projections.
world=bpy.data.worlds.new('Neutral studio'); bpy.context.scene.world=world; world.use_nodes=True
world.node_tree.nodes['Background'].inputs[0].default_value=(.12,.14,.17,1)
world.node_tree.nodes['Background'].inputs[1].default_value=.45
for location,power,size in [((-2,-3,5),450,4),((3,2,4),300,3)]:
    data=bpy.data.lights.new('Softbox','AREA'); data.energy=power; data.size=size
    obj=bpy.data.objects.new('Softbox',data); bpy.context.collection.objects.link(obj); obj.location=location
    obj.rotation_euler=(Vector((0,0,.4))-obj.location).to_track_quat('-Z','Y').to_euler()
camera_data=bpy.data.cameras.new('Interpretation camera'); camera=bpy.data.objects.new('Interpretation camera',camera_data)
bpy.context.collection.objects.link(camera); camera_data.type='ORTHO'
scene=bpy.context.scene; scene.camera=camera; scene.render.engine='CYCLES'; scene.cycles.samples=20
scene.render.film_transparent=True; scene.render.image_settings.color_mode='RGBA'
source=(ROOT/'upstream/NetHack/win/share/monsters.txt').read_text()
tile_entries={name:rows.strip().splitlines() for number,name,rows in re.findall(r'^# tile (\d+) \(([^\n]+)\)\s*\{([^}]+)\}',source,re.M)}
report=[]
for key in GROUPS:
    for group,parts in objects.items():
        for obj in parts: obj.hide_render=group!=key
    bpy.context.view_layer.update()
    points=[o.matrix_world@Vector(corner) for o in objects[key] for corner in o.bound_box]
    center=sum(points,Vector())/len(points)
    low=Vector(tuple(min(p[i] for p in points) for i in range(3)))
    high=Vector(tuple(max(p[i] for p in points) for i in range(3)))
    center=(low+high)*.5
    def aim(yaw,elevation,scale):
        a=math.radians(yaw); e=math.radians(elevation)
        camera.location=center+Vector((math.cos(a)*math.cos(e),math.sin(a)*math.cos(e),math.sin(e)))*5
        camera.rotation_euler=(center-camera.location).to_track_quat('-Z','Y').to_euler()
        camera_data.ortho_scale=scale
        camera_data.shift_x=0; camera_data.shift_y=0
    scene.render.resolution_x=800; scene.render.resolution_y=800; scene.render.resolution_percentage=100
    for view,yaw,elevation in [('three-quarter',-65,30),('rear',115,25)]:
        aim(yaw,elevation,max((high-low).length*1.1,1.1))
        scene.render.filepath=str(OUT/(key+'-'+view+'.png')); bpy.ops.render.render(write_still=True)
    rows=[r.strip() for r in tile_entries[key.replace('_',' ')+',male']]
    target={(x,15-y) for y,row in enumerate(rows) for x,ch in enumerate(row) if ch not in ['.','A']}
    target_width=max(x for x,y in target)-min(x for x,y in target)+1
    target_height=max(y for x,y in target)-min(y for x,y in target)+1
    candidates=[]; scene.render.resolution_x=16; scene.render.resolution_y=16; scene.cycles.samples=8
    for yaw in [-115,-90,-65]:
        for elevation in [25,45]:
            aim(yaw,elevation,1)
            inverse=camera.rotation_euler.to_matrix().transposed()
            projected=[inverse@(p-center) for p in points]
            width=max(p.x for p in projected)-min(p.x for p in projected)
            height=max(p.y for p in projected)-min(p.y for p in projected)
            camera_data.ortho_scale=max(width*16/(target_width+1),height*16/(target_height+1))
            target_x=(min(x for x,y in target)+max(x for x,y in target)+1)/32-.5
            target_y=(min(y for x,y in target)+max(y for x,y in target)+1)/32-.5
            camera_data.shift_x=(min(p.x for p in projected)+max(p.x for p in projected))*.5/camera_data.ortho_scale-target_x
            camera_data.shift_y=(min(p.y for p in projected)+max(p.y for p in projected))*.5/camera_data.ortho_scale-target_y
            path=OUT/(key+f'-pixel-{yaw}-{elevation}.png'); scene.render.filepath=str(path)
            bpy.ops.render.render(write_still=True)
            image=bpy.data.images.load(str(path),check_existing=False)
            rgba=list(image.pixels); silhouette={(i%16,i//16) for i in range(256) if rgba[i*4+3]>.5}
            iou=len(silhouette&target)/max(1,len(silhouette|target))
            candidates.append(dict(yaw=yaw,elevation=elevation,silhouette_iou=round(iou,4),file=path.name))
            bpy.data.images.remove(image)
    report.append(dict(key=key,bounds_m=[list(low),list(high)],best_projection=max(candidates,key=lambda c:c['silhouette_iou']),candidates=candidates))
    scene.cycles.samples=20
for parts in objects.values():
    for obj in parts: obj.hide_render=False
scene.render.resolution_x=800; scene.render.resolution_y=800
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'CreatureInterpretations.blend'))
(OUT/'projection-report.json').write_text(json.dumps(report,indent=2))
print('CREATURE_INTERPRETATIONS_READY count=3',flush=True)
