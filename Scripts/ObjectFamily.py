"""Closed wooden containers and a representative gold-piece cluster."""
import math
import CreatureGeometry as g
from CreatureGeometry import bpy,box,finish

def curved_lid(name,x0,x1,z,ry,rz,pigment):
    # Solid half-cylinder with end faces; no open underside or alpha geometry.
    n=32;verts=[];faces=[]
    for x in [x0,x1]:
        for i in range(n+1):
            a=math.pi*i/n;verts.append((x,ry*math.cos(a),z+rz*math.sin(a)))
    for i in range(n):faces.append((i,i+1,i+n+2,i+n+1))
    faces+=[tuple(reversed(range(n+1))),tuple(range(n+1,2*(n+1))),(0,n+1,2*n+1,n)]
    mesh=bpy.data.meshes.new(name);mesh.from_pydata(verts,[],faces);mesh.update()
    o=bpy.data.objects.new(name,mesh);bpy.context.collection.objects.link(o)
    return finish(o,name,pigment)

def container(key,rounded=False):
    g.GROUP=key
    width=.72;depth=.50;base=0;height=.37 if rounded else .46
    box('dark_seam_core',(0,0,(height+base)*.5),(width-.018,depth-.018,height-base),'wood_dark',.010)
    # Individual planks with shallow seams, complete on all four sides.
    for i in range(6):
        x=-width/2+(i+.5)*width/6
        for side in [-1,1]:box('front_back_plank',(x,side*(depth/2-.012),(height+base)*.5),(width/6-.004,.027,height-base),'wood',.005)
    for i in range(4):
        y=-depth/2+(i+.5)*depth/4
        for side in [-1,1]:box('end_plank',(side*(width/2-.012),y,(height+base)*.5),(.027,depth/4-.004,height-base),'wood',.005)
    for z in [base+.025,height-.025]:
        for side in [-1,1]:box('horizontal_frame',(0,side*(depth/2+.006),z),(width+.016,.030,.042),'wood_edge',.006)
        for side in [-1,1]:box('end_frame',(side*(width/2+.006),0,z),(.030,depth,.042),'wood_edge',.006)
    for x in [-.22,.22]:
        for side in [-1,1]:box('vertical_brace',(x,side*(depth/2+.012),(height+base)*.5),(.034,.035,height-base),'wood_edge',.005)
    if rounded:
        for i in range(6):
            x=-width/2+i*width/6
            lid=curved_lid('rounded_lid_plank',x+.002,x+width/6-.002,height+.008,depth/2,.215,'wood')
            lid['lid_part']=True
        for x in [-.22,.22]:
            # Closed thin raised wood bands, following the lid arch.
            lid=curved_lid('lid_brace',x-.017,x+.017,height+.011,depth/2+.007,.220,'wood_edge');lid['lid_part']=True
        for x in [-.25,.25]:box('rear_hinge',(x,depth/2+.017,height-.01),(.055,.025,.10),'object_brass',.007)
        box('latch_plate',(0,-depth/2-.029,height-.035),(.074,.018,.15),'object_brass',.007)
        box('latch_fold',(0,-depth/2-.043,height+.005),(.035,.020,.065),'object_brass',.006)
    else:
        for i in range(6):
            x=-width/2+(i+.5)*width/6
            lid=box('flat_lid_plank',(x,0,height+.024),(width/6-.004,depth,.040),'wood',.005);lid['lid_part']=True
        for x in [-.22,.22]:box('flat_lid_brace',(x,0,height+.047),(.034,depth+.012,.020),'wood_edge',.005)
        box('latch_plate',(0,-depth/2-.032,height*.57),(.070,.018,.060),'object_brass',.007)
    # Tiny dark nail heads remain material-scaled to the plank construction.
    for x in [-.22,.22]:
        for z in [base+.028,height-.026]:
            for side in [-1,1]:box('nail',(x,side*(depth/2+.032),z),(.011,.006,.011),'wood_dark',.003)

def coins():
    g.GROUP='gold_piece'
    layout=[(-.12,-.07,.012,0),(-.12,-.07,.027,12),(-.12,-.07,.042,22),(.015,.055,.012,18),(.015,.055,.027,30),(.13,-.045,.012,-12),(.20,.10,.012,8),(-.22,.10,.012,0),(.055,-.15,.012,-18)]
    for i,(x,y,z,angle) in enumerate(layout):
        z-=.0055
        bpy.ops.mesh.primitive_cylinder_add(vertices=48,radius=.071,depth=.013,location=(x,y,z))
        o=bpy.context.object;o.rotation_euler.z=math.radians(angle)
        bevel=o.modifiers.new('Worn coin edge','BEVEL');bevel.width=.002;bevel.segments=2
        finish(o,'coin_'+str(i),'object_gold');o['coin_disc']=True
        bpy.ops.mesh.primitive_torus_add(major_segments=40,minor_segments=6,location=(x,y,z+.007),major_radius=.056,minor_radius=.0015)
        finish(bpy.context.object,'coin_rim_'+str(i),'object_gold')

def object_pigment(obj,p,color,colors):
    if obj['pigment'] in ['wood','wood_edge']:
        grain=.94+.035*math.sin(p.x*173+p.z*7)+.025*math.sin(p.x*47+p.z*21)
        return tuple(c*grain for c in color)
    return color
