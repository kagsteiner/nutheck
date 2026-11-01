"""Shared unicorn body with one attached, closed spiral forehead horn."""
from CreatureGeometry import *
import CreatureGeometry as geo
from EquineFamily import equine
from mathutils.bvhtree import BVHTree

def unicorn(key,coat,mane,iris,alignment,tail_pigment):
    body=equine(key,.345,.121,.155,.480,.344,.136,.212,.128,.035,coat,mane,iris=iris)
    # The tail pixels follow the coat, unlike the contrasting rear-neck mane.
    tail=next(o for o in bpy.context.scene.objects if o.get('creature')==key and o.get('tail_form'))
    tail['pigment']=tail_pigment;tail.data.materials.clear();tail.data.materials.append(MATS[tail_pigment])
    body['source_alignment']=alignment;body['family_variant']='unicorn'
    geo.GROUP=key;hx=body['head_x'];hz=body['head_z'];head=body['head_length']
    bpy.context.view_layer.update();tree=BVHTree.FromObject(body,bpy.context.evaluated_depsgraph_get())
    axis=Vector((-.52,0,.854)).normalized()
    seed=Vector((hx-head*.35,0,hz+head*.46));start=seed+axis*.18
    hit,normal,face,distance=tree.ray_cast(body.matrix_world.inverted()@start,-axis,.40)
    assert hit is not None,key
    root=body.matrix_world@hit-axis*.006
    right=Vector((0,1,0));up=axis.cross(right).normalized();length=.245;radius=.022
    vertices=[];faces=[];rings=65;sides=32
    # Mild integrated helical relief, with painted gold/cool grooves. No floating
    # spiral strip, horn socket or decorative headgear.
    for i in range(rings):
        t=i/(rings-1)
        for j in range(sides):
            a=math.tau*j/sides;r=radius*(1-t)**.85*(1+.055*math.cos(a-t*math.tau*4))
            r=max(.00045,r)
            vertices.append(root+axis*(length*t)+(right*math.cos(a)+up*math.sin(a))*r)
    for i in range(rings-1):
        for j in range(sides):
            a=i*sides+j;b=i*sides+(j+1)%sides;faces.append((a,b,b+sides,a+sides))
    faces.extend([tuple(reversed(range(sides))),tuple((rings-1)*sides+j for j in range(sides))])
    mesh=bpy.data.meshes.new('Closed spiral horn');mesh.from_pydata(vertices,[],faces);mesh.update()
    horn=bpy.data.objects.new('forehead_horn',mesh);bpy.context.scene.collection.objects.link(horn);geo.finish(horn,'forehead_horn','unicorn_gold')
    for p in mesh.polygons:p.use_smooth=True
    horn['unicorn_horn']=True;horn['horn_root']=list(root);horn['horn_axis']=list(axis);horn['horn_length']=length
    horn['horn_radius']=radius;horn['coat_marking']='horn_spiral';horn['horn_right']=list(right);horn['horn_up']=list(up)
    return body

def unicorn_pigment(obj,p,pigment,colors):
    if not obj.get('unicorn_horn'):return pigment
    delta=p-Vector(obj['horn_root']);axis=Vector(obj['horn_axis']);t=delta.dot(axis)/obj['horn_length']
    a=math.atan2(delta.dot(Vector(obj['horn_up'])),delta.dot(Vector(obj['horn_right'])))
    wave=.5+.5*math.cos(a-t*math.tau*4)
    shade=max(0,min(1,(wave-.70)/.30))*.78
    return tuple(a*(1-shade)+b*shade for a,b in zip(colors['unicorn_gold'],colors['unicorn_groove']))
