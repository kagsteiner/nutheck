"""Independent constrictor, viper head and continuously joined cobra hood."""
import bpy,math
from mathutils import Vector
from mathutils.bvhtree import BVHTree
import CreatureGeometry as g
from CreatureGeometry import orb,limb,sculpt_union
from SnakeFamily import catmull
SPECS={'python':dict(radius=.068,width=.060,length=.092,skin='python_brown',eye='python_eye'),
       'pit_viper':dict(radius=.052,width=.079,length=.082,skin='viper_black',eye='pale_eye'),
       'cobra':dict(radius=.042,width=.054,length=.075,skin='cobra_black',eye='cobra_eye')}
def path(key):
    if key=='python':return list(map(Vector,[(-.26,-.09,.255),(-.22,-.09,.205),(-.23,.02,.125),(-.11,.18,.090),(.12,.22,.090),(.34,.10,.088),(.36,-.15,.088),(.18,-.30,.090),(-.07,-.31,.090),(-.25,-.23,.090),(-.36,-.03,.092),(-.27,.31,.095),(.03,.40,.100),(.32,.32,.105),(.42,.16,.115)]))
    if key=='cobra':return list(map(Vector,[(-.245,-.04,.515),(-.21,-.04,.415),(-.205,-.02,.280),(-.20,.015,.125),(-.11,.15,.069),(.09,.19,.068),(.28,.08,.068),(.30,-.12,.070),(.13,-.24,.075),(-.08,-.20,.09),(-.12,-.09,.12)]))
    return list(map(Vector,[(-.245,-.04,.365),(-.215,-.035,.280),(-.22,-.015,.180),(-.19,.04,.100),(-.08,.16,.075),(.13,.18,.075),(.29,.03,.075),(.23,-.17,.078),(.04,-.23,.09),(-.10,-.16,.13),(-.12,-.04,.18)]))
def build(key):
    g.GROUP=key;s=SPECS[key];skin=s['skin'];points=catmull(path(key));rad=s['radius'];radii=[]
    for i,p in enumerate(points):
        t=i/(len(points)-1);r=rad*(.64+.36*math.sin(math.pi*min(1,t/.86)));r*=min(1,.025+(1-t)/.22);radii.append(r)
    # Smooth sampled tube, stable transported cross sections, complete capped ends.
    verts=[];faces=[];N=32;up=Vector((0,1,0))
    for i,p in enumerate(points):
        tangent=(points[min(i+1,len(points)-1)]-points[max(0,i-1)]).normalized();up=(up-tangent*up.dot(tangent)).normalized();right=tangent.cross(up).normalized()
        for j in range(N):a=math.tau*j/N;verts.append(p+radii[i]*(up*math.cos(a)+right*math.sin(a)))
    for i in range(len(points)-1):
        for j in range(N):a=i*N+j;b=i*N+(j+1)%N;faces.append((a,b,b+N,a+N))
    faces.extend([tuple(reversed(range(N))),tuple((len(points)-1)*N+j for j in range(N))])
    mesh=bpy.data.meshes.new('Curved snake trunk');mesh.from_pydata(verts,[],faces);mesh.update();o=bpy.data.objects.new('trunk',mesh);bpy.context.collection.objects.link(o);g.finish(o,'trunk',skin)
    head=path(key)[0]+Vector((-.044,0,.009));width=s['width'];length=s['length'];parts=[o,orb('skull',head,(length,width,.041),skin),orb('tapered_snout',head+Vector((-.050,0,-.007)),(length*.63,width*(.60 if key=='pit_viper' else .73),.027),skin)]
    if key=='cobra':
        vv=[];ff=[];rings=[(.270,.036),(.315,.083),(.370,.130),(.430,.137),(.477,.105),(.505,.047)]
        for z,w in rings:
            for j in range(48):
                a=math.tau*j/48;vv.append((-.208+(.031*math.cos(a)),-.04+w*math.sin(a),z))
        for i in range(len(rings)-1):
            for j in range(48):a=i*48+j;b=i*48+(j+1)%48;ff.append((a,b,b+48,a+48))
        ff.extend([tuple(reversed(range(48))),tuple((len(rings)-1)*48+j for j in range(48))])
        mm=bpy.data.meshes.new('Expanded continuous hood');mm.from_pydata(vv,[],ff);mm.update();hood=bpy.data.objects.new('hood',mm);bpy.context.collection.objects.link(hood);g.finish(hood,'hood',skin);parts.append(hood)
    body=sculpt_union(parts,'continuous_body',skin,.0045);body['anatomy']='heavy_coiled_constrictor' if key=='python' else 'broad_headed_viper' if key=='pit_viper' else 'integrated_expanded_hood'
    body['path_samples']=len(points);body['head_width']=width;body['body_radius']=rad;body['hood_width']=.274 if key=='cobra' else 0
    bpy.context.view_layer.update();tree=BVHTree.FromObject(body,bpy.context.evaluated_depsgraph_get())
    for side in [-1,1]:
        origin=head+Vector((-.027,0,.015));direction=Vector((-.1,side,.25)).normalized();hit,normal,_,_=tree.ray_cast(body.matrix_world.inverted()@origin,direction,.25);assert hit is not None
        pos=body.matrix_world@hit;eye=orb('fitted_eye',pos+normal*.001,(.013,.009,.012),s['eye']);eye['eye_side']=side
        pupil=orb('pupil',pos+normal*.009,(.003,.0035,.008),'snake_dark');pupil['pupil_side']=side
        orb('nostril',head+Vector((-.088,side*width*.34,.004)),(.003,.003,.003),'snake_dark')
        limb('mouth_seam',[(head.x-.099,head.y+side*width*.25,head.z-.014),(head.x-.035,head.y+side*width*.79,head.z-.020),(head.x+.042,head.y+side*width*.77,head.z-.015)],[.0018]*3,'snake_dark')
        if key=='pit_viper':
            pit=orb('facial_pit',head+Vector((-.057,side*width*.66,.009)),(.0045,.003,.0045),'snake_dark');pit['facial_pit_side']=side
    if key!='python':
        a=head+Vector((-.10,0,-.016));b=a+Vector((-.038,0,-.002));limb('tongue',[a,b],[.0035,.0025],'snake_red')
        for side in [-1,1]:limb('tongue_fork',[b,b+Vector((-.015,side*.007,0))],[.0025,.001],'snake_red')

def pigment(obj,p,c,colors):
    if not obj.get('anatomy'):return c
    if obj['creature']=='python':
        # Muted brown/orange dorsal saddles, not the source's magenta ASCII colour.
        t=.5+.5*math.sin(p.x*32+p.y*23);blend=.28*t
        c=tuple(a*(1-blend)+b*blend for a,b in zip(c,colors['python_orange']))
    else:
        f=.90+.07*math.sin(p.x*46+p.y*29)*math.sin(p.z*39);c=tuple(v*f for v in c)
    grain=.96+.04*math.sin(p.x*600+p.z*500)*math.sin(p.y*580)
    return tuple(v*grain for v in c)
