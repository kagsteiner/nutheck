"""Blender 5.x: reproducible miniature study, metre units, shared material family.

Run: blender --background --python Scripts/CreateArtStudy.py
The .blend is the editable source; FBX files are inputs to ImportArtStudy.py.
"""
import bpy
import json
import math
import random
import sys
from pathlib import Path
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "Art/Studies/01-MiniatureDungeon"
OUT.mkdir(parents=True, exist_ok=True)
random.seed(107)
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.scale_length = 1.0

# Linear colours, also consumed by Unreal: broad, matte shapes rather than noise.
PALETTE = {
    "Slate": ([.105, .145, .17], .88, 0),
    "Limestone": ([.235, .175, .115], .92, 0),
    "StoneLight": ([.34, .265, .185], .9, 0),
    "StoneDark": ([.135, .105, .075], .96, 0),
    "Mortar": ([.040, .030, .022], 1, 0),
    "Wood": ([.19, .085, .035], .87, 0),
    "WoodLight": ([.27, .135, .055], .84, 0),
    "Bronze": ([.43, .225, .060], .57, .45),
    "Iron": ([.09, .12, .135], .52, .7),
    "Blade": ([.43, .52, .52], .4, .75),
    "Oxblood": ([.32, .026, .037], .91, 0),
    "ClothShade": ([.125, .012, .019], .96, 0),
    "ClothLight": ([.48, .065, .065], .9, 0),
    "Leather": ([.075, .045, .026], .87, 0),
    "Skin": ([.51, .315, .19], .82, 0),
    "Goblin": ([.22, .29, .095], .84, 0),
    "GoblinShade": ([.10, .15, .037], .9, 0),
    "Chitin": ([.17, .047, .020], .55, .06),
    "ChitinLight": ([.30, .095, .032], .51, .06),
    "Fur": ([.34, .23, .13], .95, 0),
    "FurLight": ([.65, .52, .32], .95, 0),
    "Jelly": ([.08, .37, .24], .33, 0),
    "JellyCore": ([.035, .16, .10], .55, 0),
    "Teal": ([.065, .24, .235], .72, 0),
    "Parchment": ([.65, .55, .34], .95, 0),
    "Black": ([.009, .014, .014], .65, 0),
    "Ivory": ([.67, .54, .34], .82, 0),
    "Moss": ([.085, .115, .043], .98, 0),
    "Ember": ([1.0, .29, .025], .72, 0),
}
MATS = {}
for name, (color, roughness, metallic) in PALETTE.items():
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = (*color, 1)
    mat.use_nodes = True
    shader = mat.node_tree.nodes.get('Principled BSDF')
    shader.inputs['Base Color'].default_value = (*color, 1)
    shader.inputs['Roughness'].default_value = roughness
    shader.inputs['Metallic'].default_value = metallic
    paint=mat.node_tree.nodes.new('ShaderNodeVertexColor')
    paint.layer_name='Paint'
    mix=mat.node_tree.nodes.new('ShaderNodeMixRGB')
    mix.blend_type='MULTIPLY'; mix.inputs[0].default_value=1
    mix.inputs[1].default_value=(*color,1)
    mat.node_tree.links.new(paint.outputs['Color'],mix.inputs[2])
    mat.node_tree.links.new(mix.outputs[0],shader.inputs['Base Color'])
    MATS[name] = mat
(OUT / 'palette.json').write_text(json.dumps(PALETTE, indent=2))

GROUP = 'Room'


def finish(obj, name, material):
    obj.name = GROUP + '_' + name
    obj.data.materials.append(MATS[material])
    obj['asset_group'] = GROUP
    return obj


def box(name, at, size, mat, bevel=.025, rot=0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=at)
    obj = bpy.context.object
    obj.dimensions = size
    obj.rotation_euler.z = rot
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if name in ['floor','masonry','cap','corner','corner_cap','stair','stair_lip']:
        for v in obj.data.vertices:
            v.co+=Vector((random.uniform(-.014,.014),random.uniform(-.014,.014),random.uniform(-.009,.009)))
    if bevel:
        mod = obj.modifiers.new('Shared soft edge', 'BEVEL')
        mod.width = bevel
        mod.segments = 3
        mod = obj.modifiers.new('Weighted corner normals', 'WEIGHTED_NORMAL')
        mod.keep_sharp = True
    return finish(obj, name, mat)


def ellipsoid(name, at, size, mat, subdiv=2):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=12, radius=1, location=at)
    obj = bpy.context.object
    obj.scale = size
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    for face in obj.data.polygons: face.use_smooth=True
    return finish(obj, name, mat)


def rod(name, a, b, radius, mat, end_radius=None, vertices=16):
    direction = Vector(b) - Vector(a)
    bpy.ops.mesh.primitive_cone_add(vertices=vertices, radius1=radius,
        radius2=radius if end_radius is None else end_radius,
        depth=direction.length, location=(Vector(a)+Vector(b))*.5)
    obj = bpy.context.object
    obj.rotation_euler = direction.to_track_quat('Z', 'Y').to_euler()
    for face in obj.data.polygons:
        face.use_smooth=len(face.vertices)==4
    return finish(obj, name, mat)


def cloth(name, x, y, bottom, top, lower_radius, upper_radius, cape=False):
    verts=[]; faces=[]; slices=32; rings=8
    for ring in range(rings):
        t=ring/(rings-1)
        radius=lower_radius*(1-t)+upper_radius*t
        for i in range(slices+1):
            theta=(math.pi if cape else math.tau)*i/slices
            fold=(.026*math.cos(theta*12)+.012*math.sin(theta*7))*(1-.75*t)
            r=radius+fold
            verts.append((x+r*math.cos(theta),y+r*math.sin(theta)*(.92 if cape else .64),
                bottom+(top-bottom)*t+.018*math.sin(theta*5)*(1-t)))
    for ring in range(rings-1):
        for i in range(slices):
            a=ring*(slices+1)+i; b=a+slices+1
            faces.append((a,a+1,b+1,b))
    mesh=bpy.data.meshes.new(name); mesh.from_pydata(verts,[],faces); mesh.update()
    obj=bpy.data.objects.new(name,mesh); bpy.context.collection.objects.link(obj)
    for face in mesh.polygons: face.use_smooth=True
    mod=obj.modifiers.new('Cloth thickness','SOLIDIFY'); mod.thickness=.012
    return finish(obj,name,'Oxblood')


# Irregular flagstone rows retain the underlying metre grid without a bathroom-tile pattern.
box('foundation', (0, 0, -.26), (10.25, 8.25, .35), 'Mortar', .10)
y=-4
while y<3.99:
    height=min(random.choice([.44,.52,.61,.68]),4-y)
    x=-5
    while x<4.99:
        width=min(random.choice([.43,.58,.75,.91]),5-x)
        if width>.04:
            mat=random.choice(['Limestone']*7+['StoneDark']*2+['StoneLight']*2)
            box('floor',(x+width*.5,y+height*.5,-.035+random.uniform(-.012,.012)),
                (max(.025,width-.035),max(.025,height-.035),.14),mat,random.uniform(.025,.045),random.uniform(-.012,.012))
        x+=width
    y+=height

# 1.2 m walls, three staggered masonry courses and a slightly projecting cap.
def wall_block(x, y, along_x, length=1):
    for course in range(3):
        pieces = [(0,.96)] if course != 1 else [(-.25,.46),(.25,.46)]
        for offset, width in pieces:
            at=(x+offset if along_x else x, y if along_x else y+offset, .2+course*.36)
            size=(width,.42,.345) if along_x else (.42,width,.345)
            at=(at[0]+random.uniform(-.009,.009),at[1]+random.uniform(-.009,.009),at[2]+random.uniform(-.012,.012))
            box('masonry',at,size,random.choice(['Limestone']*5+['StoneDark','StoneLight']),random.uniform(.04,.065))
    box('cap',(x,y,1.15),(.98,.51,.16) if along_x else (.51,.98,.16),'StoneLight',.045)

for x in range(-5,5):
    wall_block(x+.5,4,True)
    if x not in [-1,0]: wall_block(x+.5,-4,True)
for y in range(-4,4):
    wall_block(-5,y+.5,False)
    if y != 1: wall_block(5,y+.5,False)
for x in [-5,5]:
    for y in [-4,4]:
        for course in range(3): box('corner',(x,y,.2+course*.36),(.48,.48,.345),'Limestone',.035)
        box('corner_cap',(x,y,1.15),(.54,.54,.16),'StoneLight',.035)

# Door at the far side: timber posts, lintel, iron straps and individual planks.
for y in [.98,2.02]: box('door_post',(5,y,.61),(.54,.19,1.24),'Wood',.04)
box('door_lintel',(5,1.5,1.25),(.56,1.23,.22),'WoodLight',.04)
for i in range(5): box('door_plank',(5.4+i*.16,2.08,.54),(.155,.095,1.04),'WoodLight' if i%2 else 'Wood',.018)
for z in [.23,.86]: box('door_strap',(5.72,2.02,z),(.77,.055,.085),'Iron',.01)
ellipsoid('door_handle',(5.98,1.97,.57),(.045,.04,.045),'Bronze')

# Stairs and props; still one metre per gameplay tile, all roots on the floor.
for i in range(5):
    box('stair',(-3.25,-1.6+i*.22,.04+i*.12),(.88,.25,.16+i*.24),'StoneDark',.022)
box('stair_lip',(-3.83,-1.16,.27),(.16,1.25,.54),'Limestone',.025)
box('stair_lip',(-2.67,-1.16,.27),(.16,1.25,.54),'Limestone',.025)
for x in [-3.9,3.7]:
    box('crate',(x,2.8,.32),(.65,.60,.64),'Wood',.035)
    for z in [.07,.54]: box('crate_band',(x,2.8,z),(.69,.64,.07),'Iron',.01)
    for dx in [-.20,0,.20]: box('crate_plank',(x+dx,2.485,.32),(.16,.035,.48),'WoodLight',.009)
rod('potion_bottle',(2.9,-1.6,.04),(2.9,-1.6,.28),.105,'Teal',vertices=10)
rod('potion_neck',(2.9,-1.6,.28),(2.9,-1.6,.38),.045,'Teal')
rod('potion_cork',(2.9,-1.6,.38),(2.9,-1.6,.43),.047,'WoodLight')
box('scroll',(3.18,-1.4,.06),(.3,.25,.06),'Parchment',.02,rot=.25)
for x in [3.03,3.33]: rod('scroll_roll',(x,-1.54,.10),(x,-1.27,.10),.045,'Parchment')
for i in range(6):
    x,y=3.7+random.uniform(-.15,.15),-.8+random.uniform(-.15,.15)
    rod('coin',(x,y,.035),(x,y,.065),.05,'Bronze',vertices=10)

# Small accents share the same palette; avoid filling the room with unrelated props.
for x,y in [(-4.68,2.2),(4.68,-2.0)]:
    box('torch_bracket',(x,y,.72),(.12,.18,.21),'Iron',.02)
    rod('torch_handle',(x,y,.69),(x,y,1.02),.045,'Wood')
    rod('torch_cup',(x,y,.96),(x,y,1.08),.10,'Iron',.13)
    ellipsoid('torch_fire',(x,y,1.14),(.065,.065,.14),'Ember')
for i in range(36):
    x=random.uniform(-4.8,4.8)
    y=random.choice([-3.72,3.72])+random.uniform(-.08,.08)
    s=random.uniform(.025,.075)
    ellipsoid('stone_debris',(x,y,.025),(s,s*.7,s*.55),random.choice(['StoneDark','StoneLight']))
for x,y in [(-4.75,3.4),(4.75,3.4),(-4.75,-2.8)]:
    for i in range(5):
        ellipsoid('moss',(x+random.uniform(-.1,.1),y+random.uniform(-.25,.25),.035),(.09,.06,.015),'Moss')


def adventurer(origin):
    x,y=origin
    def p(a,b,c): return (x+a,y+b,c)
    for dx in [-.17,.17]:
        box('boot',p(dx,-.05,.13),(.22,.36,.25),'Leather',.045)
        rod('leg',p(dx,0,.25),p(dx,0,.60),.095,'Slate')
    cloth('tunic',x,y,.40,.98,.32,.23)
    box('belt',p(0,0,.69),(.55,.34,.09),'Leather',.02)
    box('buckle',p(0,-.19,.69),(.10,.045,.10),'Bronze',.012)
    ellipsoid('head',p(0,-.02,1.13),(.19,.17,.22),'Skin')
    ellipsoid('helmet',p(0,.01,1.26),(.22,.20,.17),'Bronze')
    box('helmet_nose',p(0,-.20,1.15),(.045,.035,.22),'Bronze',.01)
    for side in [-1,1]:
        ellipsoid('eye',p(side*.073,-.172,1.16),(.028,.018,.016),'Black')
        ellipsoid('cheek',p(side*.11,-.14,1.09),(.057,.037,.05),'Skin')
    rod('helmet_ridge',p(0,-.13,1.38),p(0,.14,1.38),.023,'Bronze')
    cloth('cloak',x,y+.08,.32,1.03,.40,.24,cape=True)
    rod('cloak_clasp',p(-.18,-.12,1.00),p(.18,-.12,1.00),.018,'Bronze')
    for dx in [-.31,.31]:
        ellipsoid('pauldron',p(dx,0,.96),(.16,.18,.14),'Iron')
        rod('arm',p(dx,0,.90),p(dx*1.3,-.04,.66),.09,'Oxblood')
        ellipsoid('glove',p(dx*1.3,-.04,.63),(.09,.09,.10),'Leather')
    box('sword',p(.43,-.1,.91),(.065,.045,.66),'Blade',.006,rot=-.15)
    box('guard',p(.43,-.1,.59),(.23,.075,.05),'Bronze',.01)
    rod('grip',p(.43,-.1,.47),p(.43,-.1,.59),.04,'Leather')
    ellipsoid('shield',p(-.43,-.12,.72),(.055,.27,.31),'Wood')
    ellipsoid('shield_boss',p(-.49,-.12,.72),(.06,.075,.075),'Bronze')


GROUP='Hero'
adventurer((0,-1.5))
GROUP='Dog'
x,y=1.25,-.9
ellipsoid('body',(x,y,.38),(.39,.19,.23),'Fur')
ellipsoid('chest',(x-.22,y,.43),(.20,.22,.25),'FurLight')
ellipsoid('head',(x-.38,y,.67),(.20,.18,.21),'Fur')
ellipsoid('muzzle',(x-.54,y-.015,.61),(.15,.115,.095),'FurLight')
ellipsoid('nose',(x-.66,y-.015,.63),(.045,.07,.045),'Black')
for dy in [-.14,.14]:
    rod('ear',(x-.34,y+dy,.74),(x-.42,y+dy*.9,.92),.085,'Fur',.015)
    ellipsoid('eye',(x-.49,y+dy*.96,.72),(.024,.02,.024),'Black',1)
for dx in [-.25,.25]:
    for dy in [-.13,.13]:
        rod('leg',(x+dx,y+dy,.33),(x+dx,y+dy,.08),.07,'Fur')
        ellipsoid('paw',(x+dx-.02,y+dy,.065),(.10,.07,.055),'FurLight')
rod('tail',(x+.30,y,.45),(x+.49,y,.70),.085,'Fur',.04)
rod('collar',(x-.23,y-.20,.47),(x-.23,y+.20,.47),.065,'Oxblood')
for dy in [-.145,.145]:
    ellipsoid('brow',(x-.45,y+dy,.76),(.07,.025,.025),'FurLight')
    ellipsoid('eye_glint',(x-.505,y+dy,.729),(.010,.009,.010),'Ivory')
for dx in [-.25,.25]:
    for dy in [-.13,.13]:
        for toe in [-.025,.025]:
            rod('toe',(x+dx-.09,y+dy+toe,.055),(x+dx-.04,y+dy+toe,.065),.009,'Fur')

GROUP='Ant'
x,y=2.1,1.0
for name,dx,s in [('abdomen',.30,(.34,.22,.23)),('thorax',-.10,(.24,.17,.18)),('head',-.42,(.22,.23,.19))]:
    ellipsoid(name,(x+dx,y,.35),s,'ChitinLight' if name=='head' else 'Chitin')
for dx in [-.23,0,.22]:
    for side in [-1,1]:
        knee=(x+dx+.11,y+side*.38,.27)
        rod('leg_upper',(x+dx,y+side*.10,.33),knee,.045,'Chitin')
        rod('leg_lower',knee,(x+dx+.18,y+side*.56,.04),.033,'Chitin',.012)
for side in [-1,1]:
    rod('antenna',(x-.52,y+side*.12,.47),(x-.70,y+side*.30,.67),.022,'Chitin')
    rod('antenna_tip',(x-.70,y+side*.30,.67),(x-.84,y+side*.38,.64),.019,'Chitin')
    rod('mandible',(x-.56,y+side*.14,.32),(x-.78,y+side*.07,.29),.06,'ChitinLight',.015)
    ellipsoid('eye',(x-.48,y+side*.195,.43),(.06,.035,.055),'Black')
for dx in [.19,.32,.45]:
    ellipsoid('carapace_band',(x+dx,y,.39),(.035,.215,.205),'ChitinLight')

GROUP='Goblin'
x,y=-1.75,1.4
for dx in [-.13,.13]:
    rod('shin',(x+dx,y,.10),(x+dx,y,.47),.09,'Goblin')
    box('foot',(x+dx,y-.07,.08),(.19,.29,.15),'Leather',.035)
rod('jerkin',(x,y,.36),(x,y,.81),.26,'Leather',.18,24)
ellipsoid('head',(x,y-.01,1.0),(.25,.19,.24),'Goblin')
ellipsoid('jaw',(x,y-.10,.88),(.21,.14,.12),'Goblin')
ellipsoid('nose',(x,y-.24,1.0),(.075,.105,.07),'Goblin')
for side in [-1,1]:
    rod('ear',(x+side*.17,y,1.05),(x+side*.42,y+.03,1.15),.10,'Goblin',.012)
    brow=ellipsoid('brow',(x+side*.1,y-.18,1.105),(.12,.05,.045),'GoblinShade')
    brow.rotation_euler.y=side*.18
    ellipsoid('eyeball',(x+side*.105,y-.19,1.04),(.052,.030,.037),'Ivory')
    ellipsoid('iris',(x+side*.105,y-.220,1.041),(.024,.010,.026),'Bronze')
    ellipsoid('pupil',(x+side*.105,y-.231,1.041),(.011,.005,.020),'Black')
    ellipsoid('cheekbone',(x+side*.16,y-.15,.96),(.09,.06,.065),'Goblin')
    ellipsoid('inner_ear',(x+side*.285,y-.035,1.09),(.09,.025,.035),'GoblinShade')
    ellipsoid('nostril',(x+side*.035,y-.326,1.0),(.022,.014,.016),'GoblinShade')
    rod('arm',(x+side*.22,y,.75),(x+side*.36,y-.08,.49),.075,'Goblin')
    ellipsoid('hand',(x+side*.36,y-.08,.49),(.085,.07,.095),'Goblin')
    rod('fang',(x+side*.11,y-.244,.91),(x+side*.10,y-.25,.95),.027,'Ivory',.008)
for i in range(6):
    a=-.14+i*.047; b=a+.047
    rod('mouth',(x+a,y-.24,.902+.12*a*a),(x+b,y-.24,.902+.12*b*b),.012,'GoblinShade')
rod('club',(x+.37,y-.10,.44),(x+.43,y-.10,1.02),.055,'Wood',.115)
cloth('loincloth',x,y,.27,.53,.22,.22)
box('belt',(x,y,.56),(.43,.30,.055),'Oxblood',.015)
box('buckle',(x,y-.16,.56),(.075,.025,.06),'Bronze',.008)

GROUP='Jelly'
x,y=-.9,-.5
ellipsoid('body',(x,y,.25),(.43,.38,.31),'Jelly',3)
for dx,dy,s in [(-.3,-.12,.16),(.28,-.15,.18),(.20,.24,.16),(-.22,.22,.19)]:
    ellipsoid('lobe',(x+dx,y+dy,.12),(s,s,.13),'Jelly',2)
ellipsoid('core',(x+.03,y-.27,.30),(.11,.06,.10),'JellyCore',2)
for dx,dy,dz in [(-.16,-.24,.29),(.17,-.19,.34),(.1,.16,.41),(-.07,.05,.47)]:
    ellipsoid('gel_highlight',(x+dx,y+dy,dz),(.045,.04,.03),'Teal')

# Sculpted geometry plus restrained vertex paint: darker recesses/undersides,
# warmer highlights and broad pigment variation. Export the same paint to UE.
bpy.context.view_layer.update()
for obj in list(bpy.context.scene.objects):
    if obj.type!='MESH': continue
    bpy.context.view_layer.objects.active=obj
    for mod in list(obj.modifiers): bpy.ops.object.modifier_apply(modifier=mod.name)
    mesh=obj.data
    paint=mesh.color_attributes.new(name='Paint',type='FLOAT_COLOR',domain='CORNER')
    mesh.color_attributes.active_color=paint
    zmin=min(v.co.z for v in mesh.vertices); zmax=max(v.co.z for v in mesh.vertices)
    spread=max(.01,zmax-zmin)
    for loop in mesh.loops:
        v=mesh.vertices[loop.vertex_index]
        p=obj.matrix_world@v.co
        n=(obj.matrix_world.to_3x3()@v.normal).normalized()
        height=(v.co.z-zmin)/spread
        brush=math.sin(p.x*10+p.y*7+math.sin(p.z*6))*math.cos(p.y*13+p.z*8)*.035
        strength=min(1.0,max(.46,.65+.24*height+.09*n.z+brush))
        paint.data[loop.index].color=(strength,min(1,strength*.975),min(1,strength*.93),1)

# Export a single mesh per reusable asset family, retaining material slots.
for group in ['Room','Hero','Dog','Ant','Goblin','Jelly']:
    bpy.ops.object.select_all(action='DESELECT')
    objs=[o for o in bpy.context.scene.objects if o.type=='MESH' and o.get('asset_group')==group]
    for obj in objs: obj.select_set(True)
    bpy.context.view_layer.objects.active=objs[0]
    pivot=Vector({'Room':(0,0,0),'Hero':(0,-1.5,0),'Dog':(1.25,-.9,0),
        'Ant':(2.1,1,0),'Goblin':(-1.75,1.4,0),'Jelly':(-.9,-.5,0)}[group])
    for obj in objs: obj.location-=pivot
    bpy.ops.export_scene.fbx(filepath=str(OUT/(group+'.fbx')),use_selection=True,
        object_types={'MESH'},apply_unit_scale=True,add_leaf_bones=False,
        bake_anim=False,axis_forward='-Y',axis_up='Z',use_mesh_modifiers=True,mesh_smooth_type='FACE')
    for obj in objs: obj.location+=pivot

# Editable lighting/camera for artists, and a native Blender reference render.
world=bpy.data.worlds.new('Charcoal environment')
bpy.context.scene.world=world
world.use_nodes=True
world.node_tree.nodes['Background'].inputs[0].default_value=(.07,.09,.12,1)
world.node_tree.nodes['Background'].inputs[1].default_value=.4
for name,location,energy,color,size in [
    ('Warm key',(-3,-4,9),1700,(1,.80,.59),6),
    ('Cool fill',(3,4,6),1100,(.62,.78,1),5)]:
    data=bpy.data.lights.new(name,'AREA'); data.energy=energy; data.color=color; data.shape='DISK'; data.size=size
    obj=bpy.data.objects.new(name,data); bpy.context.collection.objects.link(obj); obj.location=location
    obj.rotation_euler=(-obj.location).to_track_quat('-Z','Y').to_euler()
data=bpy.data.cameras.new('Study camera'); cam=bpy.data.objects.new('Study camera',data)
bpy.context.collection.objects.link(cam); cam.location=(10,-14,17)
cam.rotation_euler=(Vector((0,0,.1))-cam.location).to_track_quat('-Z','Y').to_euler()
data.type='ORTHO'; data.ortho_scale=15
scene=bpy.context.scene; scene.camera=cam
scene.render.engine='CYCLES'; scene.cycles.samples=32
scene.render.resolution_x=1600; scene.render.resolution_y=1100; scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG'
scene.render.filepath=str(OUT/'BlenderStudy.png')
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'MiniatureDungeon.blend'))
if '--no-render' not in sys.argv:
    bpy.ops.render.render(write_still=True)
print('ART_STUDY_BLENDER_READY')
