"""Adult human icon characters with fixed integrated costuming; front is -Y."""
from CreatureGeometry import *
import CreatureGeometry as geo
from mathutils.bvhtree import BVHTree

def garment(name,rings,color):
    vertices=[];faces=[];n=64
    for z,rx,ry in rings:
        for i in range(n):
            a=math.tau*i/n;vertices.append((rx*math.cos(a),ry*math.sin(a),z))
    for j in range(len(rings)-1):
        for i in range(n):a=j*n+i;b=j*n+(i+1)%n;faces.append((a,b,b+n,a+n))
    mesh=bpy.data.meshes.new(name);mesh.from_pydata(vertices,[],faces);mesh.update()
    obj=bpy.data.objects.new(name,mesh);bpy.context.collection.objects.link(obj);geo.finish(obj,name,color)
    mod=obj.modifiers.new('Leather thickness','SOLIDIFY');mod.thickness=.008
    for p in mesh.polygons:p.use_smooth=True
    return obj

def face_eyes(key,body,hz,coat,iris):
    tree=BVHTree.FromObject(body,bpy.context.evaluated_depsgraph_get());inv=body.matrix_world.inverted()
    for side in [-1,1]:
        def surface(u,v,lift):
            hit,normal,face,distance=tree.ray_cast(inv@Vector((side*.043+u,-.30,hz+.020+v)),Vector((0,1,0)),.4)
            assert hit is not None,(key,side,u,v)
            return body.matrix_world@hit+Vector((0,-lift,0))
        def patch(name,w,h,color,lift,almond=False):
            vertices=[surface(0,0,lift+.0004)]
            for i in range(48):
                a=math.tau*i/48;vertices.append(surface(w*math.cos(a),h*math.sin(a)*(abs(math.sin(a))**.25 if almond else 1),lift))
            mesh=bpy.data.meshes.new(name);mesh.from_pydata(vertices,[],[(0,i+1,(i+1)%48+1) for i in range(48)]);mesh.update()
            obj=bpy.data.objects.new(name,mesh);bpy.context.collection.objects.link(obj);geo.finish(obj,name,color)
            obj['eye_side']=side;obj['eye_surface_conforming']=True
            for f in mesh.polygons:f.use_smooth=True
            return obj
        patch('orbital_rim',.019,.010,'human_dark',.0006,True)
        eye=patch('eye',.017,.008,'human_sclera',.0011,True);eye['eye_center']=list(surface(0,0,.0011))
        patch('iris',.0068,.0068,iris,.0018)
        patch('pupil',.0032,.0032,'human_dark',.0024)
        for upper in [True,False]:
            points=[]
            for i in range(17):
                a=(0 if upper else math.pi)+math.pi*i/16;points.append(surface(.018*math.cos(a),.009*math.sin(a),.0018))
            obj=limb('upper_eyelid' if upper else 'lower_eyelid',points,[.0021 if upper else .0016]*17,coat);obj['eye_side']=side
        orb('eye_glint',surface(-.002,.0025,.0029),(.0011,.0011,.0011),'glint')
        brow=[surface(-.019+i*.0047,.028+.004*math.sin(math.pi*i/8),.002) for i in range(9)]
        limb('eyebrow',brow,[.0025]*8+[.0013],'human_brow')

def hair_cap(hz,color):
    vertices=[];faces=[];n=64;rings=16
    for j in range(rings):
        for i in range(n):
            a=math.tau*i/n;t=(.01+j/(rings-1))*(1.55+.40*math.sin(a)+.025*math.cos(a*6)+.018*math.cos(a*11))
            vertices.append((.108*math.sin(t)*math.cos(a),-.005+.097*math.sin(t)*math.sin(a),hz+.143*math.cos(t)))
    for j in range(rings-1):
        for i in range(n):a=j*n+i;b=j*n+(i+1)%n;faces.append((a,b,b+n,a+n))
    faces.append(tuple(reversed(range(n))))
    mesh=bpy.data.meshes.new('Sculpted hair cap');mesh.from_pydata(vertices,[],faces);mesh.update()
    obj=bpy.data.objects.new('hair_cap',mesh);bpy.context.collection.objects.link(obj);geo.finish(obj,'hair_cap',color)
    obj.modifiers.new('Hair cap thickness','SOLIDIFY').thickness=.006
    for f in mesh.polygons:f.use_smooth=True
    obj['long_hair_mass']=True

def human_player(key,female):
    geo.GROUP=key;coat='human_skin';hz=1.51 if female else 1.56
    shoulder=.177 if female else .217;hip=.085 if female else .102;reach=.245 if female else .295
    ribs=.164 if female else .202;waist=.121 if female else .148;thigh=.073 if female else .087
    parts=[orb('pelvis',(0,0,.80),(.150 if female else .165,.102,.140),coat),
        orb('abdomen',(0,0,1.00),(waist,.089 if female else .105,.205),coat),
        orb('ribcage',(0,0,1.17),(ribs,.099 if female else .117,.186),coat),
        limb('neck',[(0,0,1.29),(0,-.001,hz-.090)],[.066,.055],coat),
        orb('skull',(0,-.005,hz),(.101,.088,.132),coat),
        orb('jaw',(0,-.026,hz-.070),(.077 if female else .086,.073,.068),coat),
        orb('nose_bridge',(0,-.085,hz-.006),(.015,.023,.035),coat),
        orb('nose_tip',(0,-.114,hz-.034),(.020,.023,.016),coat)]
    for side in [-1,1]:
        parts.append(orb('ear',(side*.102,-.003,hz),(.020,.017,.036),coat))
        parts.append(limb('trapezius',[(side*.04,0,1.34),(side*shoulder,0,1.27)],[.050,.052],coat))
        parts.append(orb('deltoid',(side*shoulder,0,1.255),(.059 if female else .076,.065, .084),coat))
        parts.append(limb('arm',[(side*shoulder,0,1.25),(side*(reach-.015),-.008,1.06),(side*reach,-.035,.87)],
            [.050 if female else .067,.039 if female else .049,.027 if female else .034],coat))
        parts.append(orb('hand',(side*reach,-.040,.842),(.030,.026,.046),coat))
        parts.append(limb('leg',[(side*hip,0,.80),(side*(hip+.017),-.012,.46),(side*(hip+.020),0,.085)],[thigh,.052 if female else .060,.035 if female else .043],coat))
        parts.append(orb('calf',(side*(hip+.018),.013,.29),(.054 if female else .063,.053,.135),coat))
        parts.append(orb('ankle',(side*(hip+.020),-.005,.100),(.040 if female else .047,.045,.066),coat))
        parts.append(orb('foot',(side*(hip+.020),-.044,.036),(.050,.099,.035),coat))
    body=sculpt_union(parts,'human_anatomy',coat,.0055)
    body['human_player']=True;body['ancestry']='human';body['sex']='female' if female else 'male';body['head_z']=hz
    body['shoulder_half_width']=shoulder;body['waist_half_width']=waist;body['body_type']='athletic' if female else 'muscular'
    for side in [-1,1]:
        for i in range(4):
            x=side*reach+(i-1.5)*.014
            limb('finger',[(x,-.045,.827),(x,-.055,.790),(x,-.066,.779+abs(i-1.5)*.006)],[.0085,.0078,.0062],coat)
        limb('thumb',[(side*(reach-.019),-.049,.855),(side*(reach-.039),-.065,.824)],[.012,.008],coat)
        for n in [-1,1]:orb('nostril',(n*.012,-.134,hz-.043),(.0045,.002,.003),'human_dark')
    bpy.context.view_layer.update();face_eyes(key,body,hz,coat,'human_blue' if female else 'human_green')
    limb('mouth',[(-.029,-.092,hz-.080),(0,-.105,hz-.078),(.029,-.092,hz-.080)],[.0015,.002,.0015],'human_lip')
    hair_cap(hz,'human_gold')
    if female:
        # Fixed brown torso and legwear follow the icon rather than a dress.
        garment('leather_bodice',[(.84,.156,.113),(.96,.134,.103),(1.11,.177,.119),(1.25,.174,.108)],'player_leather')
        garment('fitted_hip_guard',[(.73,.171,.120),(.82,.169,.119),(.96,.138,.112)],'player_leather')
        for side in [-1,1]:
            limb('shoulder_trim',[(side*.125,-.105,1.23),(side*.135,-.035,1.30),(side*.125,.090,1.245)],[.009,.010,.009],'player_trim')
            x=side*(hip+.020)
            limb('fitted_legwear',[(side*hip,0,.79),(side*(hip+.017),-.012,.46),(side*(hip+.018),.013,.29),(x,0,.10)],
                [.083,.062,.067,.047],'player_leather')
            box('foot_sole',(x,-.045,.009),(.110,.210,.016),'player_trim',.004)
            limb('footstrap',[(x-.045,-.065,.061),(x,-.085,.074),(x+.045,-.065,.061)],[.007,.007,.007],'player_trim')
        # One long braid lies over the left shoulder; a small rear mass covers the nape.
        points=[Vector(p) for p in [(-.101,.003,hz-.02),(-.14,-.035,1.35),(-.178,-.070,1.26),(-.16,-.108,1.12)]]
        for strand in range(3):
            samples=[]
            for i in range(37):
                t=i/36;u=t*3;j=min(2,int(u));p=points[j].lerp(points[j+1],u-j)
                a=t*math.tau*4+strand*math.tau/3;samples.append(p+Vector((.010*math.cos(a),.009*math.sin(a),0)))
            obj=limb('braid_strand',samples,[.012*(1-.35*i/36) for i in range(37)],'human_gold');obj['long_hair_mass']=True
        orb('braid_tie',(-.16,-.108,1.128),(.024,.020,.009),'player_leather')
    else:
        garment('short_waist_garment',[(.755,.201,.132),(.82,.202,.130),(.96,.162,.119)],'player_leather')
        for side in [-1,1]:
            for i in range(5):orb('toe',(side*(hip+.020)+(i-2)*.018,-.124+abs(i-1.5)*.004,.028),(.010,.028,.016),coat)
    garment('belt',[(.944,.165 if not female else .142,.124 if not female else .116),(.982,.160 if not female else .138,.121 if not female else .113)],'player_belt')
    for obj in bpy.context.scene.objects:
        if obj.type=='MESH' and obj.get('creature')==key:obj['player_form']=key
    return body


def fixed_characters():
    """Bake every painted surface into one fixed character object per icon."""
    for key in ['valkyrie_female_human','barbarian_male_human']:
        parts=[o for o in bpy.context.scene.objects if o.type=='MESH' and o.get('creature')==key]
        body=next(o for o in parts if o.get('human_player'))
        body['fitted_eye_centers']=[float(c) for o in parts if o.get('eye_center') for c in o['eye_center']]
        body['fixed_icon_costume']=True
        group=body.vertex_groups.new(name='anatomy');group.add(list(range(len(body.data.vertices))),1.,'REPLACE')
        bpy.ops.object.select_all(action='DESELECT')
        for obj in parts:
            if obj.get('role_module') is not None:del obj['role_module']
            obj.select_set(True)
        bpy.context.view_layer.objects.active=body;bpy.ops.object.join();body.name=key+'_character'
        assert body.data.color_attributes.get('Paint')


def human_pigment(obj,p,pigment,colors):
    if obj.name=='barbarian_male_human_human_anatomy' and p.y<-.075:
        crease=.075*math.exp(-((p.z-1.135)/.020)**2)*math.exp(-(p.x/.15)**4)
        return tuple(c*(1-crease) for c in pigment)
    if 'hair_cap' not in obj.name:return pigment
    # Painted hair flow, rather than a shiny helmet or dense strand geometry.
    a=math.atan2(p.y+.005,p.x);flow=.88+.12*(.5+.5*math.sin(a*26+p.z*19))
    if abs(p.x-.015)<.003 and -.045<p.y<.07:flow*=.55
    return tuple(c*flow for c in pigment)
