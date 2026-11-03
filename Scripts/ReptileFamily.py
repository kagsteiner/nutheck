"""Complete static squamate bodies; proportions and detailing are artistic inference."""
import bpy,math
from mathutils import Vector
from mathutils.bvhtree import BVHTree
import CreatureGeometry as g
from CreatureGeometry import orb,limb,sculpt_union

SPECS={
 'gecko':dict(length=.22,width=.075,height=.105,head=.095,neck=-.22,tail=.35,skin='gecko_pale'),
 'iguana':dict(length=.26,width=.092,height=.155,head=.090,neck=-.275,tail=.53,skin='iguana_green'),
 'lizard':dict(length=.245,width=.060,height=.112,head=.078,neck=-.265,tail=.43,skin='lizard_green')}

def reptile(key):
    g.GROUP=key;s=SPECS[key];skin=s['skin'];z=s['height'];h=s['head'];nx=s['neck'];parts=[]
    parts.append(orb('trunk',(0,0,z),(s['length'],s['width'],z*.60),skin))
    parts.append(orb('neck',(nx+.065,0,z+.025),(.100,s['width']*.72,.055),skin))
    parts.append(orb('skull',(nx-.012,0,z+.035),(h,h*(.84 if key=='gecko' else .66),.063 if key=='iguana' else .045),skin))
    parts.append(orb('snout',(nx-h*.65,0,z+.012),(h*.65,h*.62,.033),skin))
    tail=[(s['length']*.65,0,z*.8),(.26,.015,z*.67),(.26+s['tail']*.35,.055,z*.48),(.26+s['tail']*.68,.13,z*.32),(.24+s['tail']*.87,.22,z*.20)]
    radii=[s['width']*.70,.040,.026,.013,.0025]
    parts.append(limb('tail',tail,radii,skin))
    for side in [-1,1]:
        for front in [True,False]:
            x=-s['length']*.65 if front else s['length']*.60
            elbow=(x+(-.055 if front else .075),side*(s['width']+.065),z*.62)
            foot=Vector((x+(.005 if front else -.045),side*(s['width']+.12),.025))
            pts=[(x,side*s['width']*.65,z),elbow,foot]
            parts.append(limb('leg',pts,[.035 if not front else .025,.024,.014],skin))
            parts.append(orb('elbow',elbow,(.026,)*3,skin))
            parts.append(orb('palm',foot,(.025,.026,.017),skin))
            for k in range(5):
                a=(k-2)*.43;distance=(.045 if key=='gecko' else .063)*(1-.12*abs(k-2))
                end=foot+Vector((math.sin(a)*distance,side*math.cos(a)*distance,-.012))
                parts.append(limb('digit',[foot,end],[.007,.004],skin))
                if key=='gecko':parts.append(orb('adhesive_pad',end,(.010,.011,.006),skin))
                else:parts.append(limb('claw',[end,end+Vector((-.006,side*.009,-.003))],[.004,.0009],'claw'))
    body=sculpt_union(parts,'continuous_body',skin,.0035)
    body['anatomy']='four_legs_five_digits_tapered_tail';body['digit_count']=20;body['toe_pads']=key=='gecko'
    if key!='gecko':
        # Small red source-tile accent interpreted as a static tongue tip.
        end=nx-h*1.30
        limb('tongue',[(nx-h*.95,0,z+.001),(end,0,z-.002)],[.005,.0035],'tongue_red')
        for side in [-1,1]:limb('tongue_tip',[(end,0,z-.002),(end-.016,side*.007,z-.002)],[.0035,.0015],'tongue_red')
    if key=='iguana':
        # Fitted throat fan, not a floating accessory. Dorsal spines join the trunk.
        fan=orb('dewlap',(nx+.045,0,z-.047),(.084,.012,.069),'iguana_green');fan['dewlap']=True
        for i in range(13):
            x=-.22+i*.043;top=z+z*.60*math.sqrt(max(.02,1-(x/s['length'])**2))
            spine=limb('dorsal_spine',[(x,0,top-.008),(x+.009,0,top+.045*(1-i/19))],[.013,.0013],'iguana_lime');spine['dorsal_spine']=i
    bpy.context.view_layer.update();tree=BVHTree.FromObject(body,bpy.context.evaluated_depsgraph_get())
    for side in [-1,1]:
        origin=Vector((nx-.035,0,z+.042));direction=Vector((-.12,side,.33)).normalized()
        hit,normal,_,_=tree.ray_cast(body.matrix_world.inverted()@origin,direction,.3);assert hit is not None
        pos=body.matrix_world@hit
        eye=orb('eye',pos+normal*.002,(.016,.012,.016),'eye_red' if key=='gecko' else 'eye_gold');eye['eye_side']=side
        pupil=orb('vertical_pupil',pos+normal*.012,(.003,.004,.011),'reptile_dark');pupil['pupil_side']=side
        nostril=orb('nostril',(nx-h*.95,side*h*.36,z+.031),(.005,.004,.004),'reptile_dark')
        limb('mouth_seam',[(nx-h*1.07,side*h*.30,z-.002),(nx-h*.50,side*h*.62,z-.007),(nx+.022,side*h*.66,z-.004)],[.0018,.002,.0015],'reptile_dark')
    # Every foot sits above the floor; no floor volume or baked shadow geometry.

def pigment(obj,p,color,colors):
    key=obj['creature'];s=SPECS[key]
    if not obj.name.endswith('continuous_body'):return color
    z=s['height'];belly=max(0,min(1,(z*.85-p.z)/(.060)))
    if key=='gecko':
        dorsal=max(0,min(1,(p.z-z*.95)/.055))
        c=tuple(a*(1-dorsal*.85)+b*dorsal*.85 for a,b in zip(color,colors['gecko_peach']))
    else:
        stripe=.5+.5*math.sin(p.x*27+p.y*17)
        blend=(.60 if key=='iguana' else .70)*stripe*max(0,min(1,(p.z-z*.65)/.06))
        accent=colors['iguana_lime' if key=='iguana' else 'lizard_brown']
        c=tuple(a*(1-blend)+b*blend for a,b in zip(color,accent))
        c=tuple(a*(1-belly*.55)+b*belly*.55 for a,b in zip(c,colors['reptile_belly']))
    # Fine pigment grain reads as scales close up, without extruded beads.
    grain=.95+.05*math.sin(p.x*780)*math.sin(p.y*750+p.z*600)
    return tuple(v*grain for v in c)
