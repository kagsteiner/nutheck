"""Three separate anatomical interpretations of common early-level tiles."""
import bpy,math
from mathutils import Vector
from mathutils.bvhtree import BVHTree
import CreatureGeometry as g
from CreatureGeometry import orb,limb,sculpt_union

def floating_eye():
    g.GROUP='floating_eye'
    globe=orb('globe',(0,0,.64),(.235,.235,.235),'eye_white');globe['hover_clearance']=.405
    # A curved spherical iris follows the globe. Its single pole avoids a ring
    # of degenerate faces; solid thickness closes the rim after export.
    normal=Vector((0,-math.cos(math.radians(20)),math.sin(math.radians(20))))
    right=Vector((1,0,0));up=normal.cross(right).normalized();center=Vector((0,0,.64))
    radius=.237;outer=.139;n=96;rings=16;verts=[center+normal*radius];faces=[]
    for j in range(1,rings+1):
        r=outer*j/rings
        for i in range(n):
            a=math.tau*i/n;verts.append(center+normal*math.sqrt(radius*radius-r*r)+right*r*math.cos(a)+up*r*math.sin(a))
    for i in range(n):faces.append((0,1+i,1+(i+1)%n))
    for j in range(rings-1):
        for i in range(n):
            a=1+j*n+i;b=1+j*n+(i+1)%n;faces.append((a,a+n,b+n,b))
    mesh=bpy.data.meshes.new('Curved iris');mesh.from_pydata(verts,[],faces);mesh.update()
    obj=bpy.data.objects.new('Curved iris',mesh);bpy.context.scene.collection.objects.link(obj);g.finish(obj,'curved_iris','iris_cyan')
    for p in mesh.polygons:p.use_smooth=True
    obj.modifiers.new('Corneal rim thickness','SOLIDIFY').thickness=.001
    obj['iris_surface']=True;obj['iris_outer_radius']=outer

def newt():
    g.GROUP='newt';skin='newt_orange'
    parts=[orb('torso',(-.015,0,.098),(.205,.065,.065),skin),orb('skull',(-.245,0,.108),(.105,.077,.065),skin),
           orb('muzzle',(-.305,-.002,.088),(.066,.063,.038),skin)]
    tail=[(.135,0,.080),(.235,.015,.062),(.325,.065,.043),(.375,.125,.028),(.363,.192,.020)]
    radii=[.048,.036,.023,.012,.003]
    for i in range(len(tail)-1):
        parts.append(limb('tail_segment',tail[i:i+2],radii[i:i+2],skin))
        if i:parts.append(orb('tail_joint',tail[i],(radii[i],)*3,skin))
    for side in [-1,1]:
        for front in [True,False]:
            points=[(-.145,side*.040,.100),(-.210,side*.100,.054),(-.170,side*.149,.026)] if front else [(.095,side*.040,.090),(.159,side*.104,.048),(.110,side*.155,.026)]
            for i in range(2):parts.append(limb('leg_segment',points[i:i+2],[.025,.021] if i==0 else [.021,.014],skin))
            parts.append(orb('elbow',points[1],(.022,.022,.022),skin))
            foot=Vector(points[-1]);parts.append(orb('foot',foot,(.022,.021,.015),skin))
            # Four forefoot / five hindfoot digits are an anatomical completion,
            # not a claim that individual toes can be read from the tiny tile.
            count=4 if front else 5
            for k in range(count):
                dx=(k-(count-1)/2)*.012
                end=foot+Vector((dx,side*(.037-.004*abs(k-(count-1)/2)),-.013))
                parts.append(limb('toe',[foot+Vector((dx*.45,0,-.004)),end],[.007,.0038],skin))
    body=sculpt_union(parts,'continuous_body',skin,.0035);body['anatomy']='four_splayed_legs_and_tapering_tail'
    bpy.context.view_layer.update();tree=BVHTree.FromObject(body,bpy.context.evaluated_depsgraph_get());inv=body.matrix_world.inverted()
    for side in [-1,1]:
        start=Vector((-.263,0,.109));direction=Vector((0,side*.8,.6))
        hit,normal,_,_=tree.ray_cast(inv@start,direction,.2);assert hit is not None
        at=body.matrix_world@hit+normal*.001
        eye=orb('eye',at,(.012,.010,.010),'newt_eye');eye['eye_side']=side
    # No fur, scales, dorsal sail or accessories are inferred.

def lichen():
    g.GROUP='lichen';green='lichen_green'
    parts=[orb('central_thallus',(0,0,.085),(.135,.116,.079),green)]
    for i in range(9):
        a=math.tau*i/9;radius=.110+.012*math.sin(i*2.3)
        o=orb('foliose_lobe',(radius*math.cos(a),radius*math.sin(a),.080+.018*math.sin(i*1.7)),(.120,.077,.038),green)
        # Scallops distort the actual leaf volume, not detached surface blobs.
        for v in o.data.vertices:
            theta=math.atan2(v.co.y/.077,v.co.x/.120)
            f=1+.10*math.sin(theta*5+i)+.045*math.sin(theta*9-i)
            v.co.x*=f;v.co.y*=f;v.co.z+=.008*math.sin(theta*4+i)*(1-abs(v.co.z)/.039)
        o.rotation_euler=(0,math.radians(-23-9*math.sin(i)),a)
        parts.append(o)
    body=sculpt_union(parts,'continuous_foliose_thallus',green,.0035);body['anatomy']='eyeless_headless_limbless_lobed_thallus'
    # Floor anchoring preserves the complete underside, without a display stand.
    bpy.context.view_layer.update();low=min((body.matrix_world@v.co).z for v in body.data.vertices)
    body.location.z+=.003-low

def early_pigment(obj,p,color,colors):
    key=obj['creature']
    if key=='floating_eye' and obj.get('iris_surface'):
        normal=Vector((0,-math.cos(math.radians(20)),math.sin(math.radians(20))))
        q=p-Vector((0,0,.64));r=(q-normal*q.dot(normal)).length
        if r<.046:return colors['eye_pupil']
        if r<.095:return colors['iris_blue']
        return colors['iris_cyan']
    if key=='newt' and not obj.get('eye_side'):
        # Peach flanks/underside and larger orange dorsal masses follow the tile.
        t=max(0,min(1,(.109-p.z)/.070))*.80
        t=max(t,.65*math.exp(-((p.x+.29)/.09)**2-((p.z-.085)/.045)**2))
        return tuple(a*(1-t)+b*t for a,b in zip(color,colors['newt_peach']))
    if key=='lichen':
        patches=[(-.115,-.102,.106,.052),(.102,-.092,.111,.042),(0,-.015,.164,.052),(-.087,.095,.108,.046),(.126,.072,.103,.040)]
        d=min(math.sqrt((p.x-x)**2+(p.y-y)**2+((p.z-z)*.8)**2)/r for x,y,z,r in patches)
        # Orange borders and pale centres remain pigment on the actual thallus.
        if d<.55:return colors['lichen_pale']
        if d<1:return colors['lichen_orange']
        shade=.90+.08*math.sin(p.x*83+p.y*71)*math.sin(p.z*97)
        return tuple(v*shade for v in color)
    return color
