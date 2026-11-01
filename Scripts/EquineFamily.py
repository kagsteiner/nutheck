"""Complete horse-family anatomy: upright neck, long head, jointed legs and single hooves."""
from CreatureGeometry import *
import CreatureGeometry as geo
from EquineEyes import equine_eyes
from mathutils.bvhtree import BVHTree

def fit_ear_lining(outer,base,height,side):
    """Lay the inner leaf on the evaluated closed ear rather than floating forward."""
    bpy.context.view_layer.update();tree=BVHTree.FromObject(outer,bpy.context.evaluated_depsgraph_get())
    x,y,z=base
    def point(u,t):
        target=Vector((x-.10,y+side*.018*t+u,z+height*t))
        hit,normal,face,distance=tree.ray_cast(target,Vector((1,0,0)),.25)
        assert hit is not None,(outer.name,u,t)
        return hit+Vector((-.0005,0,0))
    vertices=[point(0,.50)]
    for i in range(48):
        a=math.tau*i/48;vertices.append(point(.010*math.sin(a),.50+.27*math.cos(a)))
    mesh=bpy.data.meshes.new('Fitted inner ear');mesh.from_pydata(vertices,[],[(0,i+1,(i+1)%48+1) for i in range(48)]);mesh.update()
    obj=bpy.data.objects.new('ear_lining',mesh);bpy.context.scene.collection.objects.link(obj);geo.finish(obj,'ear_lining','equine_inner')
    obj['ear_surface_conforming']=True
    for p in mesh.polygons:p.use_smooth=True
    return obj

def fitted_mane(key,body,color):
    """Attach a continuous long-hair ridge to the actual rear neck silhouette."""
    geo.GROUP=key;tree=BVHTree.FromObject(body,bpy.context.evaluated_depsgraph_get());inverse=body.matrix_world.inverted()
    z=body['body_center_z'];depth=body['body_depth'];hx=body['head_x'];hz=body['head_z'];head=body['head_length']
    points=[]
    for i in range(10):
        level=z+depth*1.12+(hz+head*.60-z-depth*1.12)*i/9
        hit,normal,face,distance=tree.ray_cast(inverse@Vector((hx+.65,0,level)),Vector((-1,0,0)),1.20)
        assert hit is not None,(key,level)
        p=body.matrix_world@hit;points.append((p.x+.012,0,level))
    points.append((hx-head*.25,0,hz+head*.66))
    crest=limb('mane',points,[.011]+[.028]*8+[.028,.007],color)
    crest.modifiers.new('Soft mane curve','SUBSURF').levels=2;crest['mane_mass']=True;crest['mane_fitted_to_neck']=True
    return crest

def leaf_ear(name,base,height,side,color):
    x,y,z=base;vertices=[];faces=[];n=12
    for j,(t,r) in enumerate([(0,.75),(.25,1),(.67,.72),(1,.045)]):
        for i in range(n):
            a=math.tau*i/n
            vertices.append((x+.018*t+.012*r*math.cos(a),y+side*.018*t+.025*r*math.sin(a),z+height*t))
    for j in range(3):
        for i in range(n):
            a=j*n+i;b=j*n+(i+1)%n;faces.append((a,b,b+n,a+n))
    faces.extend([tuple(reversed(range(n))),tuple(3*n+i for i in range(n))])
    mesh=bpy.data.meshes.new(name);mesh.from_pydata(vertices,[],faces);mesh.update()
    obj=bpy.data.objects.new(name,mesh);bpy.context.scene.collection.objects.link(obj);geo.finish(obj,name,color)
    sub=obj.modifiers.new('Soft leaf ear','SUBSURF');sub.levels=2
    for f in mesh.polygons:f.use_smooth=True
    obj['ear_base']=list(base);obj['ear_height']=height;obj['ear_side']=side
    fit_ear_lining(obj,base,height,side)
    return obj

def hoof(name,x,y,size,color):
    vertices=[];faces=[];n=12
    for z,scale,shift in [(.003,1,-.010),(size*1.35,.79,0)]:
        for i in range(n):
            a=math.tau*i/n
            vertices.append((x+shift+size*1.30*scale*math.cos(a),y+size*scale*math.sin(a),z))
    for i in range(n):faces.append((i,(i+1)%n,(i+1)%n+n,i+n))
    faces.extend([tuple(reversed(range(n))),tuple(n+i for i in range(n))])
    mesh=bpy.data.meshes.new(name);mesh.from_pydata(vertices,[],faces);mesh.update()
    obj=bpy.data.objects.new(name,mesh);bpy.context.scene.collection.objects.link(obj);geo.finish(obj,name,color)
    bevel=obj.modifiers.new('Rounded horn edge','BEVEL');bevel.width=.004;bevel.segments=2
    obj['single_hoof']=True
    return obj

def equine(key,length,width,depth,leg,neck_height,head,nose_length,ear_height,hoof_size,coat,mane,iris='equine_blue'):
    geo.GROUP=key;shoulder=-length*.63;hip=length*.66;z=leg+depth;hx=shoulder-.115;hz=z+neck_height
    parts=[orb('ribcage',(-.015,0,z),(length,width,depth),coat),
        orb('barrel',(.045,0,z-.025),(length*.80,width*1.015,depth*.95),coat),
        orb('haunch',(hip,0,z+.005),(length*.45,width*.99,depth*1.07),coat),
        orb('shoulder',(shoulder,0,z+.025),(length*.36,width*.97,depth*1.08),coat)]
    neck=orb('upright_neck',(shoulder-.035,0,z+neck_height*.50),(head*.90,width*.73,neck_height*.76),coat)
    neck.rotation_euler.y=-.32;parts.append(neck)
    parts.extend([orb('poll',(hx,0,hz),(head*.70,head*.56,head*.74),coat),
        orb('jaw',(hx-head*.22,0,hz-head*.36),(head*.64,head*.56,head*.54),coat)])
    bridge=orb('nasal_bridge',(hx-nose_length*.46,0,hz-head*.34),(nose_length*.70,head*.43,head*.43),coat)
    bridge.rotation_euler.y=-.40;parts.append(bridge)
    mx=hx-nose_length*.94;mz=hz-head*.70
    parts.append(orb('muzzle',(mx,0,mz),(nose_length*.35,head*.52,head*.32),coat))
    for back,x in [(False,shoulder),(True,hip)]:
        for side in [-1,1]:
            y=side*width*.68
            if back:
                path=[(x,y,z+.01),(x-.040,y,z-depth*.75),(x+.075,y,leg*.48),(x+.027,y,.105)]
                radii=[width*.49,width*.37,width*.22,width*.18]
            else:
                path=[(x,y,z+.03),(x+.015,y,leg*.78),(x-.010,y,leg*.46),(x-.022,y,.105)]
                radii=[width*.40,width*.29,width*.23,width*.18]
            parts.append(limb('hind_leg' if back else 'fore_leg',path,radii,coat))
            fx=path[-1][0]
            parts.append(limb('pastern',[(fx,y,.115),(fx-.013,y,hoof_size*1.08)],[width*.22,hoof_size*.65],coat))
            parts.append(orb('fetlock',(fx,y,.115),(width*.26,width*.25,.035),coat))
            hoof('hoof',fx-.015,y,hoof_size,'equine_horn')
    body=sculpt_union(parts,'continuous_anatomy',coat,.0065)
    for k,v in dict(body_length=length,body_width=width,body_depth=depth,body_center_z=z,leg_height=leg,
        neck_height=neck_height,head_length=head,head_x=hx,head_z=hz,muzzle_length=nose_length,
        head_to_body_length=head/length,hoof_size=hoof_size,family_variant=key).items():body[k]=v
    body['fur_surface']=True;body['fur_leg_height']=leg;body['coat_marking']='equine_coat'
    for side in [-1,1]:
        leaf_ear('ear',(hx+.017,side*head*.36,hz+head*.53),ear_height,side,coat)
        nostril=orb('nostril',(mx-nose_length*.11,side*head*.475,mz+head*.05),
            (head*.095,.006,head*.060),'equine_dark');nostril['nostril_side']=side
        limb('mouth',[(mx-nose_length*.27,side*head*.26,mz-head*.17),
            (mx-nose_length*.08,side*head*.47,mz-head*.19),(mx+nose_length*.21,side*head*.43,mz-head*.19)],
            [.0017,.002,.0012],'equine_dark')
    bpy.context.view_layer.update();equine_eyes(key,hx,hz,head,body,coat,iris=iris);geo.GROUP=key
    # Mane and tail are continuous long-hair masses essential to the silhouette,
    # rather than individual strands or a sculpted short-fur clump treatment.
    fitted_mane(key,body,mane)
    tail=limb('tail',[(hip+length*.22,0,z+.035),(hip+length*.46,.006,z-.045),
        (hip+length*.60,.010,z-.22),(hip+length*.63,.013,z-leg*.83),(hip+length*.67,.017,z-leg*.94)],
        [.028,.041,.047,.038,.006],mane)
    tail.modifiers.new('Soft tail curve','SUBSURF').levels=2;tail['tail_form']='flowing_equine';tail['long_hair_mass']=True
    for o in bpy.context.scene.objects:
        if o.type=='MESH' and o.get('creature')==key and o.get('pigment')==coat and not o.get('eye_side'):
            o['fur_surface']=True;o['fur_leg_height']=leg
    return body
