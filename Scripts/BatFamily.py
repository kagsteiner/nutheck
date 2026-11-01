"""Complete static bat anatomy: forelimb wings, four digits, free thumb and hind feet."""
from CreatureGeometry import *
import CreatureGeometry as geo
from WinterWolfEyes import winter_wolf_eyes

def membrane(name,outline,pigment,thickness):
    mesh=bpy.data.meshes.new(name);mesh.from_pydata(outline,[],[tuple(range(len(outline)))]);mesh.update()
    bm=bmesh.new();bm.from_mesh(mesh)
    bmesh.ops.triangulate(bm,faces=list(bm.faces))
    bmesh.ops.subdivide_edges(bm,edges=list(bm.edges),cuts=3,use_grid_fill=True)
    bm.to_mesh(mesh);bm.free()
    obj=bpy.data.objects.new(name,mesh);bpy.context.scene.collection.objects.link(obj)
    geo.finish(obj,name,pigment)
    for polygon in mesh.polygons:polygon.use_smooth=True
    solid=obj.modifiers.new('Closed membrane thickness','SOLIDIFY');solid.thickness=thickness;solid.offset=0
    obj['wing_membrane']=True;obj['membrane_thickness_m']=thickness
    return obj

def wing_surface(wrist,tips,ankle,flank,shoulder,elbow,pigment,thickness):
    """Curved membrane panels follow the bent digit paths, with scalloped edges."""
    wrist=Vector(wrist);chain=[Vector(p) for p in tips]+[Vector(ankle),Vector(flank),Vector(shoulder),Vector(elbow)]
    verts=[];faces=[];radial=10;across=12
    def path(point,r,bent):
        if not bent:return wrist.lerp(point,r)
        middle=wrist.lerp(point,.53);middle.x-=.012;middle.z+=.007
        return wrist.lerp(middle,r/.53) if r<=.53 else middle.lerp(point,(r-.53)/.47)
    for panel in range(len(chain)-1):
        start=len(verts);verts.append(wrist.copy())
        for row in range(1,radial+1):
            r=row/radial
            for col in range(across+1):
                u=col/across
                t=r*(1-.19*math.sin(math.pi*u)) if panel<4 else r
                p=path(chain[panel],t,panel<4).lerp(path(chain[panel+1],t,panel+1<4),u)
                p.z+=.003*math.sin(math.pi*u)*math.sin(math.pi*r)
                verts.append(p)
        for col in range(across):faces.append((start,start+1+col,start+2+col))
        for row in range(radial-1):
            for col in range(across):
                a=start+1+row*(across+1)+col;faces.append((a,a+1,a+across+2,a+across+1))
    mesh=bpy.data.meshes.new('Curved hand-wing');mesh.from_pydata(verts,[],faces);mesh.update()
    bm=bmesh.new();bm.from_mesh(mesh);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=.000001)
    bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(mesh);bm.free()
    obj=bpy.data.objects.new('wing_membrane',mesh);bpy.context.scene.collection.objects.link(obj)
    geo.finish(obj,'wing_membrane',pigment)
    for polygon in mesh.polygons:polygon.use_smooth=True
    solid=obj.modifiers.new('Closed curved membrane thickness','SOLIDIFY');solid.thickness=thickness;solid.offset=0
    obj['wing_membrane']=True;obj['membrane_thickness_m']=thickness
    return obj

def bat(key,body_length,body_width,head,span,chord,ear_height,coat,skin,rib,iris,vampire=False):
    geo.GROUP=key
    z=.26+body_length*.30;hx=-body_length*.79;hz=z+.045
    parts=[orb('chest',(-body_length*.17,0,z),(body_length*.75,body_width,body_width*1.05),coat),
        orb('pelvis',(body_length*.45,0,z-.018),(body_length*.48,body_width*.84,body_width*.91),coat),
        orb('neck',(hx+.025,0,hz-.01),(head*.66,head*.69,head*.73),coat),
        orb('skull',(hx,0,hz),(head,head*(1.02 if vampire else .86),head*.91),coat)]
    for side in [-1,1]:
        parts.append(limb('hind_leg',[(body_length*.48,side*body_width*.56,z-.018),
            (body_length*.77,side*body_width*.85,z-.070),
            (body_length*.83,side*body_width*.98,z-.108)],
            [body_width*.28,body_width*.18,body_width*.12],coat))
    body=sculpt_union(parts,'continuous_anatomy',coat,.0045)
    body['fur_surface']=True;body['fur_leg_height']=.16
    body['head_to_body_length']=head/body_length;body['half_span']=span
    body['wing_chord']=chord;body['body_length']=body_length;body['head_length']=head
    body['head_x']=hx;body['head_z']=hz;body['bat_variant']='vampire' if vampire else 'insectivore_interpretation'
    for side in [-1,1]:
        y=side*body_width*.98
        for toe in [-1,0,1]:
            limb('hind_toe',[(body_length*.83,y+toe*.008,z-.108),
                (body_length*.92,y+toe*.008,z-.126)],[.004,.002],skin)
            limb('hind_claw',[(body_length*.92,y+toe*.008,z-.126),
                (body_length*.90,y+toe*.008,z-.137)],[.0025,.0006],'claw')
        # Curved pinna cup faces forward (-X), with a rim and a small tragus.
        ey=side*head*.63;ez=hz+head*.53;ew=head*.55
        outline=[]
        for i in range(24):
            a=math.tau*i/24
            outline.append((hx+.012+.008*math.sin(a)**2,
                ey+ew*math.sin(a)*(.75+.25*math.cos(a)),ez+ear_height*(1+math.cos(a))*.5))
        verts=[(hx+.025,ey,ez+ear_height*.40)]+outline
        faces=[(0,i+1,(i+1)%24+1) for i in range(24)]
        mesh=bpy.data.meshes.new('Bat ear cup');mesh.from_pydata(verts,[],faces);mesh.update()
        obj=bpy.data.objects.new('ear',mesh);bpy.context.scene.collection.objects.link(obj);geo.finish(obj,'ear_cup',skin)
        solid=obj.modifiers.new('Pinna shell','SOLIDIFY');solid.thickness=.003
        for polygon in mesh.polygons:polygon.use_smooth=True
        rim=outline+[outline[0]];limb('ear_rim',rim,[.003]*len(rim),coat)
        orb('tragus',(hx+.004,ey-side*ew*.35,ez+ear_height*.16),(.006,ew*.20,ear_height*.17),rib)
    nose_x=hx-head*.92
    orb('short_muzzle',(hx-head*.67,0,hz-head*.25),(head*.53,head*.57,head*.33),skin)
    orb('nose_pad',(nose_x,0,hz-head*.14),(.012,head*(.42 if vampire else .27),.009),rib)
    for side in [-1,1]:
        orb('nostril',(nose_x-.009,side*head*.17,hz-head*.12),(.003,.003,.0025),'black')
        limb('mouth',[(nose_x+.006,side*head*.22,hz-head*.44),
            (hx-head*.43,side*head*.43,hz-head*.44)],[.0017,.0013],'black')
    if vampire:
        for side in [-1,1]:
            limb('short_incisor',[(nose_x+.009,side*.006,hz-head*.43),
                (nose_x+.008,side*.006,hz-head*.51)],[.003,.0006],'tooth')
    bpy.context.view_layer.update()
    winter_wolf_eyes(key,hx,hz,head,body,iris=iris,lid_pigment=coat)
    geo.GROUP=key
    for side in [-1,1]:
        shoulder=(-body_length*.40,side*body_width*.75,z+.010)
        elbow=(body_length*.02,side*span*.28,z+.055)
        wrist=(-body_length*.58,side*span*.53,z+.080)
        limb('wing_arm',[shoulder,elbow,wrist],[body_width*.28,body_width*.19,body_width*.12],rib)
        # Four elongated fingers II-V, in addition to the separate short thumb.
        tips=[(-chord*.34,side*span*.94,z+.055),(-chord*.01,side*span,z-.005),
              (chord*.56,side*span*.77,z-.038),(chord*.83,side*span*.43,z-.067)]
        for digit,tip in enumerate(tips,2):
            a=Vector(wrist);b=Vector(tip)
            middle=a.lerp(b,.53);middle.x-=.012;middle.z+=.007
            obj=limb('wing_digit_'+str(digit),[a,middle,b],[.007,.0045,.0018],rib)
            obj['wing_digit']=digit;obj['wing_side']=side
        thumb_tip=Vector(wrist)+Vector((-.045,side*.008,.030))
        obj=limb('free_thumb',[wrist,thumb_tip],[.007,.0038],rib);obj['wing_side']=side
        obj=limb('thumb_claw',[thumb_tip,thumb_tip+Vector((-.008,-side*.006,-.012))],[.003,.0006],'claw');obj['wing_side']=side
        ankle=(body_length*.83,side*body_width*.98,z-.108)
        obj=wing_surface(wrist,tips,ankle,(body_length*.21,side*body_width*.83,z-.025),
            shoulder,elbow,skin,.003 if key=='bat' else .004)
        obj['wing_side']=side
    # Tail membrane follows the two hind limbs; vampire interpretation has reduced span.
    tail_length=body_length*(.24 if vampire else .65)
    tail_tip=(body_length*.83+tail_length,0,z-.116)
    outline=[(body_length*.28,-body_width*.65,z-.030),
        (body_length*.83,-body_width*.98,z-.108),tail_tip,
        (body_length*.83,body_width*.98,z-.108),(body_length*.28,body_width*.65,z-.030)]
    obj=membrane('tail_membrane',outline,skin,.003);obj['tail_membrane']=True
    limb('tail_support',[(body_length*.50,0,z-.025),tail_tip],[.006,.0018],rib)

