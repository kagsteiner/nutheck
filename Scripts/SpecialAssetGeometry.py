"""Electric arthropod, generic remains and a carved static-water fountain."""
import bpy,math
from mathutils import Vector
import CreatureGeometry as g
from CreatureGeometry import orb,limb,finish,sculpt_union

def grid_bug():
    g.GROUP='grid_bug'
    orb('abdomen',(.075,0,.169),(.125,.095,.132),'bug_white')
    orb('thorax',(-.065,0,.128),(.088,.074,.078),'bug_blue')
    head=orb('head',(-.172,0,.105),(.083,.075,.056),'bug_blue')
    for side in [-1,1]:
        for i in range(3):
            start=Vector((-.10+i*.096,side*.053,.118))
            elbow=Vector((-.235+i*.215,side*(.17+.035*(i==1)),.155-.027*i))
            tip=Vector((-.31+i*.28,side*(.29-.025*i),.009))
            limb('leg_upper',[start,elbow],[.013,.011],'bug_red')
            orb('leg_joint',elbow,(.013,)*3,'bug_red')
            foot=limb('leg_lower',[elbow,tip],[.011,.0035],'bug_red');foot['leg_tip']=True
        at=Vector((-.202,side*.054,.133))
        eye=orb('eye',at,(.015,.009,.013),'bug_yellow');eye['eye_side']=side
        orb('pupil',at+Vector((-.004,side*.007,.003)),(.005,.004,.006),'black')
        limb('antenna_base',[(-.220,side*.032,.132),(-.280,side*.077,.212)],[.0065,.005],'bug_red')
        limb('antenna_tip',[(-.280,side*.077,.212),(-.344,side*.108,.183)],[.005,.002],'bug_red')
        limb('mandible',[(-.224,side*.025,.087),(-.259,side*.036,.071),(-.266,side*.014,.075)],[.009,.007,.002],'bug_yellow')
    # No wings: the source has no M1_FLY despite the catalogue's broad group.

def corpse():
    g.GROUP='corpse'
    parts=[orb('collapsed_mass',(0,0,.078),(.185,.112,.074),'corpse_red'),orb('fold',(.085,.035,.082),(.11,.095,.061),'corpse_red'),orb('fold',(-.093,-.044,.061),(.10,.084,.052),'corpse_red')]
    sculpt_union(parts,'collapsed_remains','corpse_red',.006)
    # Pale closed bone fragments echo the generic icon, without identifying a
    # species, sex, freshness, edibility, poison state or the original body size.
    for i,(a,b) in enumerate([((-.08,-.045,.075),(-.245,-.151,.035)),((.07,-.045,.075),(.252,-.135,.031)),((-.07,.050,.067),(-.227,.152,.036)),((.07,.05,.071),(.234,.145,.034))]):
        limb('bone_shaft',[a,b],[.023,.019],'corpse_bone')
        for side in [-1,1]:
            p=Vector(b)+Vector((side*.016,0,0));orb('bone_end',p,(.024,.021,.019),'corpse_bone')

def lathe(name,profile,pigment,n=96,flutes=0):
    verts=[];faces=[]
    for r,z in profile:
        for i in range(n):
            a=math.tau*i/n;rr=r*(1+flutes*math.cos(a*12));verts.append((rr*math.cos(a),rr*math.sin(a),z))
    for j in range(len(profile)):
        nxt=(j+1)%len(profile)
        for i in range(n):faces.append((j*n+i,j*n+(i+1)%n,nxt*n+(i+1)%n,nxt*n+i))
    mesh=bpy.data.meshes.new(name);mesh.from_pydata(verts,[],faces);mesh.update()
    o=bpy.data.objects.new(name,mesh);bpy.context.collection.objects.link(o)
    for p in mesh.polygons:p.use_smooth=True
    return finish(o,name,pigment)

def cylinder(name,radius,depth,z,pigment,vertices=96):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices,radius=radius,depth=depth,location=(0,0,z))
    o=bpy.context.object;bevel=o.modifiers.new('Soft carved edge','BEVEL');bevel.width=min(.006,depth*.20);bevel.segments=3
    return finish(o,name,pigment)

def water_arc(angle):
    # Static sculpted flow, with a stable tangent frame along its radial plane.
    radial=Vector((math.cos(angle),math.sin(angle),0));tangent=Vector((-math.sin(angle),math.cos(angle),0))
    controls=[Vector((0,0,.792)),radial*.13+Vector((0,0,1.20)),radial*.355+Vector((0,0,.85)),radial*.316+Vector((0,0,.307))]
    verts=[];faces=[];steps=48;n=10
    for j in range(steps+1):
        t=j/steps;s=1-t;p=controls[0]*s**3+controls[1]*3*s*s*t+controls[2]*3*s*t*t+controls[3]*t**3
        d=(controls[1]-controls[0])*3*s*s+(controls[2]-controls[1])*6*s*t+(controls[3]-controls[2])*3*t*t
        up=d.normalized().cross(tangent).normalized();r=.009-.004*t
        for i in range(n):
            a=math.tau*i/n;verts.append(p+r*(math.cos(a)*tangent+math.sin(a)*up))
    for j in range(steps):
        for i in range(n):a=j*n+i;b=j*n+(i+1)%n;faces.append((a,b,b+n,a+n))
    faces += [tuple(reversed(range(n))),tuple(steps*n+i for i in range(n))]
    mesh=bpy.data.meshes.new('Static water arc');mesh.from_pydata(verts,[],faces);mesh.update()
    o=bpy.data.objects.new('Static water arc',mesh);bpy.context.collection.objects.link(o)
    for p in mesh.polygons:p.use_smooth=True
    finish(o,'static_water_arc','fountain_water');o['static_water']=True

def fountain():
    g.GROUP='fountain'
    cylinder('octagonal_foot',.318,.044,.022,'fountain_stone',8)
    cylinder('lower_plinth',.276,.035,.060,'fountain_stone',8)
    lathe('fluted_pedestal',[(.001,.074),(.145,.074),(.146,.098),(.105,.123),(.102,.173),(.18,.189),(.18,.212),(.001,.212)],'fountain_stone',flutes=.025)
    bowl=lathe('carved_basin',[(.16,.181),(.285,.186),(.380,.237),(.424,.319),(.425,.355),(.407,.375),(.386,.351),(.368,.293),(.280,.225),(.16,.218)],'fountain_stone',flutes=.010);bowl['basin']=True
    cylinder('basin_floor',.19,.025,.216,'fountain_stone')
    for z,r in [(.326,.421),(.355,.418)]:
        bpy.ops.mesh.primitive_torus_add(major_segments=96,minor_segments=8,major_radius=r,minor_radius=.006,location=(0,0,z));finish(bpy.context.object,'carved_rim_bead','fountain_light')
    for i in range(12):
        a=math.tau*i/12
        leaf=orb('basin_petal_relief',(.366*math.cos(a),.366*math.sin(a),.262),(.036,.013,.033),'fountain_light');leaf.rotation_euler.z=a+math.pi/2
    cylinder('still_basin_water',.366,.008,.297,'fountain_water')
    lathe('central_fluted_column',[(.001,.301),(.076,.301),(.078,.327),(.048,.362),(.044,.654),(.062,.689),(.067,.712),(.035,.754),(.001,.754)],'fountain_stone',flutes=.065)
    orb('bud_finial',(0,0,.767),(.047,.047,.055),'fountain_light')
    for i in range(6):water_arc(math.tau*i/6)
    for radius in [.12,.22,.31]:
        bpy.ops.mesh.primitive_torus_add(major_segments=80,minor_segments=6,major_radius=radius,minor_radius=.0016,location=(0,0,.302));finish(bpy.context.object,'still_water_ripple','fountain_foam')

def special_pigment(obj,p,color,colors):
    key=obj['creature']
    if key=='grid_bug' and obj['pigment']=='bug_white':
        if p.z<.105:return colors['bug_blue']
        if -.015<p.x<.037 and p.z>.15:return colors['bug_orange']
        if .055<p.x<.098 and p.z>.19:return colors['bug_yellow']
    if key=='corpse' and obj['pigment']=='corpse_red':
        t=.35+.22*math.sin(p.x*43+p.y*29)*math.sin(p.z*37)
        return tuple(a*(1-t)+b*t for a,b in zip(color,colors['corpse_orange']))
    if key=='fountain' and obj['pigment'].startswith('fountain_') and obj['pigment'] not in ['fountain_water','fountain_foam']:
        grain=.94+.025*math.sin(p.x*197+p.y*113+p.z*97)+.018*math.sin(p.x*379-p.y*263)
        return tuple(v*grain for v in color)
    return color
