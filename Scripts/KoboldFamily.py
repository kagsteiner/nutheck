"""Dog-faced small humanoids; separate rank garment, no shadow-derived appendages."""
import CreatureGeometry as g
from CreatureGeometry import orb, limb, sculpt_union, ear, cloth, box

def rank_garment(chest,s):
    """Tailored oval cloth shells with enough clearance around the sculpted torso."""
    import math,bpy
    for name,bottom,top,rx,ry,pigment in [
        ('detachable_rank_tunic',.29*s,.57*s,chest+ .029*s,.117*s,'kobold_orange'),
        ('detachable_rank_belt',.355*s,.382*s,chest+ .035*s,.123*s,'kobold_cool')]:
        verts=[];faces=[];n=64
        for j in range(10):
            t=j/9
            for i in range(n):
                a=math.tau*i/n;fold=(.004*s*math.cos(a*10)*(1-t)) if pigment=='kobold_orange' else 0
                verts.append(((rx+fold)*math.cos(a),(ry+fold)*math.sin(a),bottom+(top-bottom)*t))
        for j in range(9):
            for i in range(n):
                a=j*n+i;b=j*n+(i+1)%n;faces.append((a,b,b+n,a+n))
        mesh=bpy.data.meshes.new(name);mesh.from_pydata(verts,[],faces);mesh.update()
        obj=bpy.data.objects.new(name,mesh);bpy.context.collection.objects.link(obj)
        for p in mesh.polygons:p.use_smooth=True
        obj.modifiers.new('Cloth thickness','SOLIDIFY').thickness=.006*s
        g.finish(obj,name,pigment);obj['rank_module']=True

def kobold(key,height,chest,head,arm_span,rank=False):
    g.GROUP=key
    s=height/.88
    def p(x,y,z):return (x*s,y*s,z*s)
    skin='kobold_blue'
    parts=[orb('torso',p(0,0,.43),(chest,.085*s,.165*s),skin),
           orb('neck',p(0,-.005,.60),(.060*s,.060*s,.085*s),skin),
           orb('skull',p(0,-.012,.70),(head,.094*s,.108*s),skin),
           orb('dog_muzzle',p(0,-.107,.672),(.071*s,.073*s,.046*s),skin),
           orb('jaw',p(0,-.084,.642),(.067*s,.062*s,.030*s),skin)]
    for side in [-1,1]:
        parts.append(limb('leg',[p(side*.067,0,.34),p(side*.085,-.018,.19),p(side*.083,.005,.060)],[.047*s,.038*s,.026*s],skin))
        parts.append(orb('foot',p(side*.085,-.045,.030),(.047*s,.081*s,.030*s),skin))
        shoulder=p(side*chest/s*.85,0,.53);elbow=p(side*arm_span,-.015,.42);wrist=p(side*(arm_span-.012),-.064,.32)
        parts.append(limb('upper_arm',[shoulder,elbow],[.039*s,.030*s],skin))
        parts.append(limb('forearm',[elbow,wrist],[.030*s,.024*s],skin))
        parts.append(orb('elbow',elbow,(.031*s,.031*s,.031*s),skin))
        parts.append(orb('shoulder',shoulder,(.041*s,.041*s,.041*s),skin))
        parts.append(orb('hand',p(side*(arm_span-.012),-.064,.304),(.031*s,.031*s,.042*s),skin))
    body=sculpt_union(parts,'continuous_anatomy',skin,.006*s)
    body['family']='kobold';body['height_parameter']=height;body['chest_parameter']=chest;body['head_parameter']=head
    # Paired upright ears: white tile tips are anatomy, not a horned helmet.
    for side in [-1,1]:
        outer=ear('ear',p(side*.087,-.005,.755),p(side*.113,.003,.88),.035*s,.030*s,skin)
        outer['ear_tip_height']=.828*s
        # Dark apertures overlap the skull; small skin brows/lower lids seat them.
        eye=orb('eye',p(side*.047,-.096,.716),(.018*s,.009*s,.018*s),'black')
        eye['eye_side']=side;eye['eye_embedded']=True
        limb('brow',[p(side*.027,-.095,.737),p(side*.047,-.101,.740),p(side*.069,-.089,.735)],[.008*s,.009*s,.007*s],skin)
        limb('lower_lid',[p(side*.030,-.097,.703),p(side*.048,-.101,.699),p(side*.064,-.093,.704)],[.005*s,.005*s,.004*s],skin)
        limb('mouth',[p(side*.060,-.140,.651),p(side*.027,-.161,.646)],[.003*s,.002*s],'black')
        for i in [-1,0,1]:
            limb('finger_seam',[p(side*(arm_span-.012)+i*.009,-.092,.306),p(side*(arm_span-.012)+i*.009,-.091,.282)],[.0014*s,.001*s],'kobold_cool')
    orb('nose',p(0,-.172,.681),(.030*s,.012*s,.019*s),'kobold_cool')
    if rank:
        rank_garment(chest,s)
        # Open hood follows the back/sides of the head and leaves face and ears clear.
        for side in [-1,1]:
            panel=limb('detachable_hood_side',[p(side*.105,.005,.74),p(side*.105,.012,.67),p(side*.12,.012,.57)],[.027*s,.030*s,.037*s],'kobold_orange');panel['rank_module']=True
        hood=orb('detachable_hood_back',p(0,.047,.718),(.119*s,.052*s,.095*s),'kobold_orange');hood['rank_module']=True
    return body
