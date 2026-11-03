"""Reference revision: fine rounded leaf scales, layered curved pauldrons."""
import math,bpy
from mathutils import Vector
import CreatureGeometry as g
from CreatureGeometry import limb,box

def point(a,z,extra=0):
    radius=.208+.035*math.exp(-((z-.51)/.13)**2)-.044*math.exp(-((z-.28)/.11)**2)
    if z>.59:radius=radius*(1-(z-.59)/.10)+.105*((z-.59)/.10)
    return Vector(((radius+extra)*math.cos(a),(radius+extra)*math.sin(a)*.59,z))
def hole(a,z):return ((z-.515)/.100)**2+(math.sin(a)/.47)**2<1 and abs(math.cos(a))>.80
def mesh(name,verts,faces,pigment,smooth=True):
    data=bpy.data.meshes.new(name);data.from_pydata(verts,[],faces);data.update();o=bpy.data.objects.new(name,data);bpy.context.collection.objects.link(o);g.finish(o,name,pigment)
    for p in data.polygons:p.use_smooth=smooth
    return o

class Leaves:
    def __init__(self):self.verts=[];self.faces=[];self.count=0
    def add(self,c,u,v,n,w,h,relief=.004):
        # Four quadratic Bezier arcs: round upper lobes, a tapered downward tip.
        arcs=[((0,.55),(-1.12,.65),(-1,-.02)),((-1,-.02),(-.80,-.60),(0,-1)),((0,-1),(.80,-.60),(1,-.02)),((1,-.02),(1.12,.65),(0,.55))]
        outline=[]
        for a,b,d in arcs:
            for j in range(6):
                t=j/6;outline.append(((1-t)**2*a[0]+2*t*(1-t)*b[0]+t*t*d[0],(1-t)**2*a[1]+2*t*(1-t)*b[1]+t*t*d[1]))
        base=len(self.verts);N=len(outline);self.verts.append(c+n*relief)
        for r in [1/3,2/3,1]:
            for x,y in outline:self.verts.append(c+u*x*w*r+v*y*h*r+n*(.0007+relief*(1-r*r)))
        for x,y in outline:self.verts.append(c+u*x*w+v*y*h-n*.002)
        for i in range(N):self.faces.append((base,base+1+i,base+1+(i+1)%N))
        for ring in range(3):
            a=base+1+ring*N;b=a+N
            for i in range(N):self.faces.append((a+i,b+i,b+(i+1)%N,a+(i+1)%N))
        self.faces.append(tuple(reversed([base+1+3*N+i for i in range(N)])));self.count+=1
    def finish(self,name,pigment):
        o=mesh(name,self.verts,self.faces,pigment);o['leaf_scale_count']=self.count;o['max_scale_width']=.040;return o

def build(key):
    g.GROUP=key;color=key.split('_')[0];pigment='dragon_'+color;gray=color=='gray';trim='regal_silver' if gray else 'regal_gold'
    # Hollow fitted lining, with rounded arm openings and an actual neck hole.
    N=80;R=40;verts=[point(math.tau*i/N,.09+j*.60/R) for j in range(R+1) for i in range(N)];faces=[]
    for j in range(R):
        for i in range(N):
            if hole(math.tau*(i+.5)/N,.09+(j+.5)*.60/R):continue
            a=j*N+i;b=j*N+(i+1)%N;faces.append((a,b,b+N,a+N))
    used=sorted({i for f in faces for i in f});remap={v:i for i,v in enumerate(used)}
    core=mesh('fitted_hollow_lining',[verts[i] for i in used],[tuple(remap[i] for i in f) for f in faces],'armor_dark');core.modifiers.new('Lining thickness','SOLIDIFY').thickness=.006
    leaves=Leaves()
    for row in range(25):
        z=.106+row*.0225
        for i in range(44):
            a=math.tau*(i+.5*(row%2))/44
            if hole(a,z):continue
            n=Vector((math.cos(a),math.sin(a)/.59,0)).normalized();u=Vector((-n.y,n.x,0))
            leaves.add(point(a,z,.008),u,Vector((0,0,1)),n,.0185,.027,.0038)
    leaves.finish('fine_overlapping_leaf_scales',pigment)
    # Curved overlapping shoulder lames, each tiled with much smaller leaf scales.
    for side in [-1,1]:
        for tier in range(3):
            center=Vector((side*(.217+tier*.024),0,.595-tier*.043));rx=.111-tier*.009;ry=.137-tier*.009;rz=.059
            vv=[center+Vector((rx*math.sin(.08+j*.147)*math.cos(math.tau*i/48),ry*math.sin(.08+j*.147)*math.sin(math.tau*i/48),rz*math.cos(.08+j*.147))) for j in range(11) for i in range(48)]
            ff=[]
            for j in range(10):
                for i in range(48):a=j*48+i;b=j*48+(i+1)%48;ff.append((a,b,b+48,a+48))
            pole=len(vv);vv.append(center+Vector((0,0,rz)))
            for i in range(48):ff.append((pole,(i+1)%48,i))
            cap=mesh('curved_pauldron_lame',vv,ff,pigment);cap.modifiers.new('Formed shoulder thickness','SOLIDIFY').thickness=.004
            detail=Leaves()
            for row in range(5):
                t=.26+row*.255
                for i in range(20):
                    a=math.tau*(i+.5*(row%2))/20
                    p=center+Vector((rx*math.sin(t)*math.cos(a),ry*math.sin(t)*math.sin(a),rz*math.cos(t)))
                    n=Vector((math.sin(t)*math.cos(a)/rx,math.sin(t)*math.sin(a)/ry,math.cos(t)/rz)).normalized();u=Vector((-math.sin(a),math.cos(a),0));v=n.cross(u).normalized()
                    detail.add(p+n*.002,u,v,n,.0115,.016,.0024)
            detail.finish('small_pauldron_leaf_scales',pigment)
            rim=[center+Vector((rx*math.cos(math.tau*i/96),ry*math.sin(math.tau*i/96),0)) for i in range(97)]
            limb('pauldron_fine_rim',rim,[.003]*97,trim)
        # Short integrated outer spurs, subordinate to the curved shoulder layers.
        for y in [-.080,.080]:limb('small_shoulder_spur',[(side*.303,y,.538),(side*.345,y,.558),(side*.359,y,.588)],[.013,.010,.0015],'dragon_horn')
    # Thin V-shaped gorget, waist belt and small fasteners; no giant chest slabs.
    for face in [-1,1]:
        pts=[point(-math.pi/2 if face==-1 else math.pi/2,z,.016) for z in [.595,.57]]
        limb('gorget_V',[( -.15,face*.112,.627),(0,face*.159,.576),(.15,face*.112,.627)],[.006]*3,trim)
    # Belt is a fitted narrow strip, not an inflated torus.
    vv=[point(math.tau*i/96,z,.016) for z in [.257,.282] for i in range(96)];ff=[(i,(i+1)%96,(i+1)%96+96,i+96) for i in range(96)]
    belt=mesh('fitted_waist_belt',vv,ff,'armor_dark');belt.modifiers.new('Belt thickness','SOLIDIFY').thickness=.005
    box('small_belt_clasp',(0,-.113,.270),(.033,.014,.026),trim,.003)
    for x in [-.100,-.060,.060,.100]:
        g.orb('belt_rivet',(x,-.11*math.sqrt(max(.1,1-(x/.17)**2))-.008,.270),(.005,.004,.005),trim)
    if gray:
        # Subtle silver-over-gray leaf spine: small overlapping leaves, not a badge.
        silver=Leaves();inset=Leaves()
        for j in range(7):
            z=.585-j*.038;c=point(-math.pi/2,z,.020)
            silver.add(c,Vector((1,0,0)),Vector((0,0,1)),Vector((0,-1,0)),.023,.030,.003)
            inset.add(c+Vector((0,-.0035,0)),Vector((1,0,0)),Vector((0,0,1)),Vector((0,-1,0)),.019,.027,.003)
        silver.finish('gray_fine_leaf_spine_rim',trim);inset.finish('gray_fine_leaf_spine',pigment)
    for z in [.095,.675]:limb('fine_hem_binding',[point(math.tau*i/96,z,.013) for i in range(97)],[.004]*97,trim)
