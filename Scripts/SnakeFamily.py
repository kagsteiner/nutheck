"""Smooth complete limbless bodies, independent dimensions and static coils."""
import bpy,math
from mathutils import Vector
import CreatureGeometry as g
from CreatureGeometry import orb,limb,sculpt_union
SPECS={
 'garter_snake':dict(scale=.80,radius=.037,head_width=.036,head_length=.068,skin='snake_orange',tongue=None),
 'snake':dict(scale=1.0,radius=.050,head_width=.051,head_length=.079,skin='snake_rust',tongue='snake_green'),
 'water_moccasin':dict(scale=1.10,radius=.065,head_width=.075,head_length=.082,skin='snake_black',tongue='snake_red')}

def path(key):
    s=SPECS[key];q=s['scale'];r=s['radius']
    # Head end to tail; rear hook differs per form. Grounded coil has no overlaps.
    pts=[(-.245,-.04,.398),(-.213,-.035,.305),(-.212,-.015,.190),(-.192,.035,.100),(-.10,.137,r+.013),(.055,.17,r+.013),(.217,.10,r+.013),(.254,-.050,r+.015),(.170,-.190,r+.020),(.015,-.213,.110),(-.058,-.135,.170)]
    if key=='garter_snake':pts[-2:]=[(.060,-.224,.090),(-.025,-.20,.130)]
    if key=='water_moccasin':pts[-2:]=[(.035,-.237,.100),(-.065,-.205,.145)]
    return [Vector(p)*q for p in pts]

def catmull(points,steps=12):
    result=[]
    for i in range(len(points)-1):
        a=points[max(0,i-1)];b=points[i];c=points[i+1];d=points[min(len(points)-1,i+2)]
        for j in range(steps):
            t=j/steps
            result.append((2*b+(-a+c)*t+(2*a-5*b+4*c-d)*t*t+(-a+3*b-3*c+d)*t*t*t)*.5)
    return result+[points[-1]]

def snake(key):
    g.GROUP=key;s=SPECS[key];q=s['scale'];skin=s['skin'];centres=catmull(path(key));rad=s['radius']*q
    radii=[]
    for i,p in enumerate(centres):
        t=i/(len(centres)-1);r=rad*(.72+.28*math.sin(math.pi*min(1,t/.70)))
        r*=min(1,.035+(1-t)/.24);radii.append(r)
    # 32-sided sampled tube, with parallel transport frames.
    verts=[];faces=[];n=32;up=Vector((0,1,0))
    for i,p in enumerate(centres):
        tangent=(centres[min(i+1,len(centres)-1)]-centres[max(i-1,0)]).normalized()
        up=(up-tangent*up.dot(tangent)).normalized();right=tangent.cross(up).normalized()
        for j in range(n):
            angle=math.tau*j/n;v=p+radii[i]*(up*math.cos(angle)+right*math.sin(angle));verts.append(v)
    for i in range(len(centres)-1):
        for j in range(n):a=i*n+j;b=i*n+(j+1)%n;faces.append((a,b,b+n,a+n))
    faces.extend([tuple(reversed(range(n))),tuple((len(centres)-1)*n+j for j in range(n))])
    mesh=bpy.data.meshes.new(key+'_swept_body');mesh.from_pydata(verts,[],faces);mesh.update()
    obj=bpy.data.objects.new('swept_body',mesh);bpy.context.collection.objects.link(obj);g.finish(obj,'swept_body',skin)
    head=Vector((-.288,-.04,.410))*q;length=s['head_length']*q;width=s['head_width']*q
    parts=[obj,orb('skull',head,(length,width,.039*q),skin),orb('snout',head+Vector((-.042*q,0,-.008*q)),(length*.72,width*.72,.028*q),skin)]
    body=sculpt_union(parts,'continuous_body',skin,.004*q);body['anatomy']='limbless_single_coil_tapered_tail';body['path_samples']=len(centres);body['head_width']=width;body['body_radius']=rad
    for side in [-1,1]:
        at=head+Vector((-.026*q,side*width*.86,.017*q))
        eye=orb('eye',at,(.012*q,.007*q,.012*q),'snake_eye');eye['eye_side']=side
        pupil=orb('pupil',at+Vector((-.003*q,side*.005*q,0)),(.0035*q,.0035*q,.008*q),'snake_pupil');pupil['pupil_side']=side
        orb('nostril',head+Vector((-.082*q,side*width*.39,.007*q)),(.003*q,.003*q,.003*q),'snake_pupil')
        limb('mouth',[(head.x-.090*q,head.y+side*width*.32,head.z-.017*q),(head.x-.033*q,head.y+side*width*.81,head.z-.020*q),(head.x+.035*q,head.y+side*width*.83,head.z-.015*q)],[.0018*q]*3,'snake_pupil')
    if s['tongue']:
        a=head+Vector((-.096*q,0,-.017*q));b=a+Vector((-.041*q,0,-.003*q))
        limb('tongue',[a,b],[.004*q,.0025*q],s['tongue'])
        for side in [-1,1]:limb('fork',[b,b+Vector((-.019*q,side*.009*q,0))],[.0025*q,.001*q],s['tongue'])

PIGMENT_CENTRES={}
def pigment(obj,p,color,colors):
    if not obj.get('anatomy'):return color
    key=obj['creature'];s=SPECS[key];q=s['scale'];points=path(key)
    # Continuous closest-point sampling avoids paint rings on the raised neck.
    if key not in PIGMENT_CENTRES:
        centres=catmull(points,3)
        PIGMENT_CENTRES[key]=[(a,b-a,(b-a).length_squared) for a,b in zip(centres,centres[1:])]
    nearest=[]
    for a,d,length in PIGMENT_CENTRES[key]:
        c=a+d*max(0,min(1,(p-a).dot(d)/length));nearest.append(((c-p).length_squared,c))
    c=min(nearest,key=lambda v:v[0])[1]
    underside=max(0,min(1,(c.z-p.z)/(.035*q)))
    if key=='garter_snake':
        stripe=max(0,1-abs(p.y-c.y)/(.012*q))*max(0,min(1,(p.z-c.z)/(.022*q)))
        blend=.28*stripe;accent=colors['snake_ochre']
    elif key=='snake':
        blend=.28*(.5+.5*math.sin(p.x*45+p.y*29));accent=colors['snake_brown']
    else:
        blend=.22*(.5+.5*math.sin(p.x*38-p.y*31));accent=colors['snake_charcoal']
    c=tuple(a*(1-blend)+b*blend for a,b in zip(color,accent))
    belly=colors['snake_charcoal' if key=='water_moccasin' else 'snake_ochre']
    c=tuple(a*(1-underside*.30)+b*underside*.30 for a,b in zip(c,belly))
    grain=.96+.04*math.sin(p.x*580+p.z*420)*math.sin(p.y*610)
    return tuple(v*grain for v in c)
