"""Blender: turn named official sprites into repeatable coloured volume proxies.

This preserves the front silhouette/pixels. Depth is inferred from silhouette
distance, so the result is an inflated sprite, not reconstructed anatomy.
"""
import bpy
import json
import math
import re
import sys
from pathlib import Path
from mathutils import Vector

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'Art/DefaultTiles'; OUT.mkdir(parents=True,exist_ok=True)
text=(ROOT/'upstream/NetHack/win/share/monsters.txt').read_text()
palette={m[0]:tuple(int(c)/255 for c in m[1:]) for m in re.findall(r'^(\S)\s*=\s*\(\s*(\d+),\s*(\d+),\s*(\d+)\s*\)',text,re.M)}
entries=re.findall(r'^# tile (\d+) \(([^\n]+)\)\s*\{([^}]+)\}',text,re.M)
roles=['archeologist','barbarian','cave dweller','healer','knight','monk','cleric','ranger','rogue','samurai','tourist','valkyrie','wizard']
animals=['giant ant','killer bee','acid blob','jackal','fox','coyote','little dog','dog','large dog','wolf','floating eye','kitten','housecat','large cat','goblin','hobgoblin','orc','kobold','newt','lichen','blue jelly','gnome','dwarf','sewer rat','giant rat']
selected=set(roles+animals)
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
bpy.context.scene.unit_settings.system='METRIC'
bpy.context.scene.unit_settings.scale_length=1
mat=bpy.data.materials.new('DefaultTilePixels'); mat.use_nodes=True
shader=mat.node_tree.nodes.get('Principled BSDF'); shader.inputs['Roughness'].default_value=.85
paint=mat.node_tree.nodes.new('ShaderNodeVertexColor'); paint.layer_name='Paint'
mat.node_tree.links.new(paint.outputs['Color'],shader.inputs['Base Color'])
manifest=[]; models={}
for index,label,pixels in entries:
    if ',' not in label: continue
    name,sex=label.rsplit(',',1)
    if name not in selected: continue
    lines=[s.strip() for s in pixels.strip().splitlines()]
    # The official '.' palette entry is the transparent background convention.
    colored={(x,y) for y,row in enumerate(lines) for x,ch in enumerate(row) if ch!='.' and max(palette[ch])>.02}
    occupied=set(colored)
    # Trim the black fringe to one pixel around the nearest coloured scanlines.
    # Interior black (eyes, clothing and stripes) remains part of the sprite.
    for y,row in enumerate(lines):
        scan=[x for x,cy in colored if cy==y]
        if not scan: scan=[x for x,cy in colored if abs(cy-y)<=1]
        if not scan: continue
        for x,ch in enumerate(row):
            if ch!='.' and max(palette[ch])<=.02 and min(scan)-1<=x<=max(scan)+1:
                occupied.add((x,y))
    if not occupied: continue
    xmin=min(x for x,y in occupied); xmax=max(x for x,y in occupied)
    ymin=min(y for x,y in occupied); ymax=max(y for x,y in occupied)
    height=1.15 if name in roles else .70 if name in ['goblin','hobgoblin','orc','kobold','gnome','dwarf'] else .48
    if name in ['floating eye','blue jelly']: height=.65
    pitch=min(.88/(xmax-xmin+1),height/(ymax-ymin+1))
    width=(xmax-xmin+1)*pitch
    verts=[]; faces=[]; colors=[]
    for x,y in sorted(occupied):
        edge=min(math.hypot(x-a,y-b) for a in range(x-5,x+6) for b in range(y-5,y+6) if (a,b) not in occupied)
        depth=min(.22,.04+edge*.045)
        u=(x-xmin)*pitch-width*.5; v=(ymax-y)*pitch+.025
        base=len(verts)
        verts.extend([(-depth,u,v),(-depth,u+pitch,v),(-depth,u+pitch,v+pitch),(-depth,u,v+pitch),
                      (depth,u,v),(depth,u+pitch,v),(depth,u+pitch,v+pitch),(depth,u,v+pitch)])
        # Cube face winding is outward. Internal overlap is acceptable for this proxy.
        quads=[(0,3,2,1),(4,5,6,7),(0,4,7,3),(1,2,6,5),(0,1,5,4),(3,7,6,2)]
        rgb=palette[lines[y][x]]
        for j,quad in enumerate(quads):
            faces.append(tuple(base+k for k in quad))
            shade=1 if j in [0,1,5] else .82
            colors.append(tuple((c**2.2)*shade for c in rgb))
    mesh=bpy.data.meshes.new(label); mesh.from_pydata(verts,[],faces); mesh.update()
    key=re.sub('[^a-z0-9]+','_',name.lower()).strip('_')+'_'+sex
    obj=bpy.data.objects.new(key,mesh); bpy.context.collection.objects.link(obj); mesh.materials.append(mat)
    layer=mesh.color_attributes.new(name='Paint',type='FLOAT_COLOR',domain='CORNER'); mesh.color_attributes.active_color=layer
    for polygon,color in zip(mesh.polygons,colors):
        for loop_index in polygon.loop_indices: layer.data[loop_index].color=(*color,1)
    bevel=obj.modifiers.new('Small pixel edge','BEVEL'); bevel.width=pitch*.045; bevel.segments=2
    bpy.ops.object.select_all(action='DESELECT'); obj.select_set(True); bpy.context.view_layer.objects.active=obj
    bpy.ops.export_scene.fbx(filepath=str(OUT/(key+'.fbx')),use_selection=True,object_types={'MESH'},
        apply_unit_scale=True,axis_forward='-Y',axis_up='Z',add_leaf_bones=False,bake_anim=False,mesh_smooth_type='FACE')
    manifest.append(dict(key=key,name=name,sex=sex,source_index=int(index),pixels=len(occupied),height_m=height,method='silhouette-distance extrusion',shadow_fringe='trimmed to one pixel around colored scanlines'))
    models[key]=obj
    obj.hide_render=True
(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2))
if len(manifest)!=len(selected)*2: raise RuntimeError('A selected named tile is missing')

# Regular, neutral masonry for the live early dungeon; origins match UE cubes.
grey=bpy.data.materials.new('GreyStone'); grey.diffuse_color=(.3,.31,.32,1)
for asset in ['GreyFloor','GreyWall']:
    parts=[]
    specifications=[]
    if asset=='GreyFloor':
        specifications=[((x,y,0),(.49,.49,1)) for x in [-.25,.25] for y in [-.25,.25]]
    else:
        for course in range(3):
            z=-.5+(course+.5)/3
            specifications+=([((0,0,z),(.99,.99,.32))] if course==1 else [((x,0,z),(.485,.99,.32)) for x in [-.25,.25]])
    for at,size in specifications:
        bpy.ops.mesh.primitive_cube_add(size=1,location=at); piece=bpy.context.object
        piece.dimensions=size; bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
        bevel=piece.modifiers.new('Stone edge','BEVEL'); bevel.width=.018; bevel.segments=2
        piece.data.materials.append(grey); parts.append(piece)
    bpy.ops.object.select_all(action='DESELECT')
    for piece in parts: piece.select_set(True)
    bpy.context.view_layer.objects.active=parts[0]
    bpy.ops.export_scene.fbx(filepath=str(OUT/(asset+'.fbx')),use_selection=True,object_types={'MESH'},
        apply_unit_scale=True,axis_forward='-Y',axis_up='Z',add_leaf_bones=False,bake_anim=False,mesh_smooth_type='FACE')
    for piece in parts: bpy.data.objects.remove(piece,do_unlink=True)

# A source-editable gallery of representative proxies, separate from live play.
gallery=['giant_ant_male','little_dog_male','kitten_male','goblin_male','newt_male','floating_eye_male','blue_jelly_male','valkyrie_female']
for i,key in enumerate(gallery):
    obj=models[key]; obj.hide_render=False; obj.location=((i%4-1.5)*1.5,(i//4-.5)*2,0)
    obj.rotation_euler.z=-math.pi/2
    bpy.ops.object.text_add(location=(obj.location.x-.55,obj.location.y-.65,.02))
    caption=bpy.context.object; caption.data.body=key.replace('_',' '); caption.data.size=.12
    caption.data.extrude=0; caption.rotation_euler=(0,0,0)
bpy.ops.mesh.primitive_cube_add(size=1,location=(0,0,-.1)); floor=bpy.context.object; floor.scale=(7,5,.15)
floor_mat=bpy.data.materials.new('Grey stage'); floor_mat.diffuse_color=(.16,.17,.18,1); floor_mat.use_nodes=True
floor_mat.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=(.16,.17,.18,1)
floor.data.materials.append(floor_mat)
caption_mat=bpy.data.materials.new('Caption'); caption_mat.use_nodes=True
caption_mat.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=(.025,.03,.035,1)
for obj in bpy.context.scene.objects:
    if obj.type=='FONT': obj.data.materials.append(caption_mat)
world=bpy.data.worlds.new('Neutral world'); bpy.context.scene.world=world; world.use_nodes=True
world.node_tree.nodes['Background'].inputs[0].default_value=(.10,.11,.13,1)
world.node_tree.nodes['Background'].inputs[1].default_value=.5
for location,power in [((0,-3,7),850),((4,3,5),450)]:
    data=bpy.data.lights.new('Gallery softbox','AREA'); data.energy=power; data.size=5
    light=bpy.data.objects.new('Gallery softbox',data); bpy.context.collection.objects.link(light); light.location=location
    light.rotation_euler=(-light.location).to_track_quat('-Z','Y').to_euler()
camera_data=bpy.data.cameras.new('Gallery camera'); camera=bpy.data.objects.new('Gallery camera',camera_data)
bpy.context.collection.objects.link(camera); camera.location=(4,-8,9)
camera.rotation_euler=(Vector((0,0,.25))-camera.location).to_track_quat('-Z','Y').to_euler()
camera_data.type='ORTHO'; camera_data.ortho_scale=8.4
scene=bpy.context.scene; scene.camera=camera; scene.render.engine='CYCLES'; scene.cycles.samples=24
scene.render.resolution_x=1600; scene.render.resolution_y=1050; scene.render.resolution_percentage=100
scene.render.filepath=str(OUT/'DefaultTileVolumes.png')
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'DefaultTileVolumes.blend'))
if '--no-render' not in sys.argv: bpy.ops.render.render(write_still=True)
print(f'DEFAULT_TILE_FIGURES_READY count={len(manifest)}',flush=True)
