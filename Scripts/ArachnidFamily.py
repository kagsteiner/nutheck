"""Static spiders and separate scorpion: eight walking legs, complete closed bodies."""
import math
import CreatureGeometry as g
from CreatureGeometry import orb,limb

def eye_on_ellipsoid(name,center,radii,direction,size,pigment,side):
    from mathutils import Vector
    d=Vector(direction).normalized();c=Vector(center)
    # Ellipsoid radial intersection; centre is slightly embedded in the carapace.
    t=1/math.sqrt(sum((d[i]/radii[i])**2 for i in range(3)))
    o=orb(name,c+d*(t-size*.30),(size,size,size),pigment);o['eye_side']=side;o['surface_fit']=True
    return o

def spider(key,giant=False):
    g.GROUP=key
    z=.255 if giant else .17;cx=-.16 if giant else -.105
    ceph=(.155,.135,.112) if giant else (.101,.079,.071)
    abdomen=(.245,.187,.175) if giant else (.142,.103,.105)
    coat='spider_brown' if giant else 'spider_cool';light='spider_warm' if giant else 'spider_blue'
    orb('cephalothorax',(cx,0,z),ceph,coat)['anatomy_role']='cephalothorax'
    orb('abdomen',(.165 if giant else .102,0,z+.035),abdomen,coat)['anatomy_role']='abdomen'
    orb('petiole',(-.015 if giant else -.005,0,z),(.07 if giant else .045,.046 if giant else .03,.045 if giant else .03),coat)
    for side in [-1,1]:
        reach=.49 if giant else .315
        for i in range(4):
            rootx=cx+(-.065+i*.043 if giant else -.042+i*.027)
            splay=[-.23,-.105,.10,.22][i]*(1 if giant else .66)
            pts=[(rootx,side*ceph[1]*.65,z),
                 (rootx+splay*.65,side*reach*.48,z+.065),
                 (rootx+splay,side*reach*.86,z-.06),
                 (rootx+splay*.95,side*reach,.015)]
            leg=limb('leg_%d_%d'%(i,side),pts,[.022 if giant else .014,.020 if giant else .012,.012 if giant else .007,.004 if giant else .0025],coat)
            leg['leg_index']=i;leg['leg_side']=side;leg['cephalothorax_root']=True
            orb('knee_%d_%d'%(i,side),pts[1],(.024 if giant else .015,)*3,light)
        fx=cx-ceph[0]*.82
        palp=limb('pedipalp_'+str(side),[(fx,side*ceph[1]*.57,z-.02),(fx-.05,side*ceph[1]*.82,z-.045),(fx-.07,side*ceph[1]*.72,z-.06)],
             [.016 if giant else .010,.012 if giant else .008,.006 if giant else .004],coat);palp['pedipalp_side']=side
        fang=limb('chelicera_'+str(side),[(cx-ceph[0]*.83,side*ceph[1]*.25,z-.035),
             (cx-ceph[0]-.035,side*ceph[1]*.28,z-.065),(cx-ceph[0]-.055,side*.014,z-.11)],
             [.020 if giant else .013,.012 if giant else .008,.002],'spider_fang');fang['fang_side']=side
        eye_on_ellipsoid('eye_'+str(side),(cx,0,z),ceph,(-1,side*.48,.35),.014 if giant else .010,'arachnid_green',side)
        for i in range(3):
            o=eye_on_ellipsoid('small_eye_%d_%d'%(i,side),(cx,0,z),ceph,(-.90+i*.20,side*(.2+i*.33),.68),.0045 if giant else .003,'arachnid_dark',side)
            o['secondary_eye']=True
    # A posterior paired spinneret completion; no web geometry or new native state.
    for side in [-1,1]:
        orb('spinneret_'+str(side),(.395 if giant else .235,side*(.035 if giant else .020),z-.006),(.025 if giant else .015,.014 if giant else .008,.014 if giant else .008),coat)

def scorpion():
    g.GROUP='scorpion';z=.15
    orb('prosoma',(-.19,0,z),(.145,.135,.080),'scorpion_shell')['anatomy_role']='prosoma'
    orb('mesosoma',(.055,0,z+.012),(.21,.145,.085),'scorpion_shell')['anatomy_role']='mesosoma'
    for i in range(6):
        x=-.055+i*.045
        plate=orb('dorsal_plate_'+str(i),(x,0,z+.063),(.037,.132-.007*abs(i-2.5),.032),'scorpion_light');plate['dorsal_segment']=i
    for side in [-1,1]:
        for i in range(4):
            x=-.245+i*.048;splay=[-.08,-.02,.07,.14][i]
            pts=[(x,side*.082,z),(x+splay,side*.205,.19),(x+splay+.025,side*.34,.08),(x+splay-.01,side*.385,.013)]
            leg=limb('leg_%d_%d'%(i,side),pts,[.017,.015,.009,.0035],'scorpion_shell');leg['leg_index']=i;leg['leg_side']=side;leg['cephalothorax_root']=True
        # Pedipalps end in two genuinely separated, closed pincer fingers per claw.
        limb('pedipalp_arm_'+str(side),[(-.27,side*.095,z),(-.36,side*.21,z+.01),(-.47,side*.225,z+.02)],[.03,.027,.035],'scorpion_shell')['pedipalp_side']=side
        claw=orb('pincer_palm_'+str(side),(-.49,side*.22,z+.025),(.070,.048,.038),'scorpion_light');claw['pincer_side']=side
        for finger in [-1,1]:
            claw=limb('pincer_finger_%d_%d'%(side,finger),[(-.525,side*.22+finger*.027,z+.025),(-.59,side*.22+finger*.041,z+.026),(-.63,side*.22+finger*.010,z+.025)],
                [.020,.014,.0025],'scorpion_light');claw['pincer_finger']=finger;claw['pincer_side']=side
        eye_on_ellipsoid('eye_'+str(side),(-.19,0,z),(.145,.135,.08),(-.80,side*.35,.70),.012,'arachnid_green',side)
    # Five individually editable tail segments form one contiguous raised arch.
    points=[(.22,0,.17),(.31,0,.23),(.35,0,.34),(.32,0,.47),(.22,0,.56),(.10,0,.57)]
    for i in range(5):
        o=limb('tail_segment_'+str(i),[points[i],points[i+1]],[.047-i*.004,.044-i*.004],'scorpion_shell');o['tail_segment']=i
        if i<4:orb('tail_joint_'+str(i),points[i+1],(.045-i*.004,)*3,'scorpion_light')
    orb('telson',(.075,0,.565),(.052,.034,.037),'scorpion_light')['telson']=True
    sting=limb('curved_sting',[(.067,0,.55),(.025,0,.515),(.005,0,.465),(.02,0,.44)],[.022,.016,.009,.0015],'spider_fang');sting['source_attack']='AT_STNG/AD_DRST'

def pigment(obj,p,base,colors):
    if obj['creature']=='scorpion':
        if obj.get('pincer_finger'):
            t=max(0,min(.8,(-p.x-.595)*22))
            return tuple(a*(1-t)+b*t for a,b in zip(base,colors['spider_fang']))
    elif obj.get('anatomy_role')=='abdomen':
        t=.09*(.5+.5*math.sin(p.x*43+p.y*21)*math.sin(p.z*37))
        pale=colors['spider_warm' if obj['creature']=='giant_spider' else 'spider_blue']
        return tuple(a*(1-t)+b*t for a,b in zip(base,pale))
    return base
