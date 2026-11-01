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

