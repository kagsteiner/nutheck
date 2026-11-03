"""Complete static bee family and separately reviewed mosquito-like xan anatomy."""
import math,bpy
from mathutils import Vector
import CreatureGeometry as g
from CreatureGeometry import orb,limb

def wing(name,root,tip,chord,pigment,side,pair):
    root=Vector(root);tip=Vector(tip);d=(tip-root).normalized()
    cross=d.cross(Vector((0,0,1))).normalized();up=d.cross(cross).normalized()
    if up.z<0:up=-up
    verts=[];faces=[];steps=24;n=12
    for j in range(steps+1):
        t=j/steps;p=root.lerp(tip,t)+Vector((0,0,.014*math.sin(math.pi*t)))
        width=.003+chord*math.sin(math.pi*t)**.7;thick=.0015+.0010*math.sin(math.pi*t)
        for i in range(n):
            a=math.tau*i/n;verts.append(p+cross*(width*math.cos(a))+up*(thick*math.sin(a)))
    for j in range(steps):
        for i in range(n):a=j*n+i;b=j*n+(i+1)%n;faces.append((a,b,b+n,a+n))
    faces.extend([tuple(reversed(range(n))),tuple(steps*n+i for i in range(n))])
    mesh=bpy.data.meshes.new(name);mesh.from_pydata(verts,[],faces);mesh.update()
    obj=bpy.data.objects.new(name,mesh);bpy.context.collection.objects.link(obj);g.finish(obj,name,pigment)
    for p in mesh.polygons:p.use_smooth=True
    obj['insect_wing']=True;obj['wing_side']=side;obj['wing_pair']=pair;obj['closed_thickness_m']=.003
    obj['wing_root']=list(root);obj['wing_tip']=list(tip)
    # Small closed veins sit on the real upper surface; no alpha planes or animation.
    points=[root.lerp(tip,t)+Vector((0,0,.014*math.sin(math.pi*t)+.003)) for t in [0,.25,.5,.75,.94]]
    vein=limb(name+'_vein',points,[.0024,.0023,.0018,.0015,.0008],'bee_vein' if pigment=='bee_wing' else 'xan_vein');vein['wing_vein']=True
    return obj

def bee(key,queen=False):
    g.GROUP=key;z=.48;torso=1.12 if queen else 1.;span=.55 if queen else .48
    thorax=orb('thorax',(-.10,0,z),(.145*torso,.105*torso,.12*torso),'bee_brown')
    thorax['fur_surface']=True;thorax['fur_leg_height']=.12;thorax['anatomy_role']='thorax'
    abdomen=orb('abdomen',(.22 if queen else .17,0,.45 if queen else z),(.285 if queen else .215,.16 if queen else .13,.175 if queen else .14),'bee_gold')
    abdomen.rotation_euler.y=.24 if queen else .06;abdomen['striped_abdomen']=True;abdomen['abdomen_length']=.285 if queen else .215
    sub=abdomen.modifiers.new('Band pigment sampling','SUBSURF');sub.subdivision_type='SIMPLE';sub.levels=2
    orb('petiole',(.015,0,z),(.08,.064,.068),'bee_dark')
    head=orb('head',(-.29,0,z-.015),(.112,.104,.092),'bee_brown');head['anatomy_role']='head'
    for side in [-1,1]:
        eye=orb('compound_eye_'+str(side),(-.335,side*.082,z),(.053,.028,.057),'bee_eye');eye['eye_side']=side
        orb('eye_glint_'+str(side),(-.357,side*.104,z+.017),(.014,.005,.016),'bee_glint')
        limb('antenna_'+str(side),[(-.36,side*.044,z+.044),(-.43,side*.075,z+.15),(-.47,side*.105,z+.165)],[.007,.005,.003],'bee_brown')
        limb('mandible_'+str(side),[(-.37,side*.035,z-.045),(-.413,side*.045,z-.055),(-.43,side*.012,z-.045)],[.016,.012,.002],'bee_dark')
        for i,x in enumerate([-.18,-.10,-.02]):
            splay=[-.10,.015,.13][i];reach=1.12 if queen else 1.
            leg=limb('leg_%d_%d'%(i,side),[(x,side*.065,z-.035),(x+splay,side*.16,z-.13),(x+splay+.02,side*.23*reach,z-.27),(x+splay-.015,side*.25*reach,z-.29)],[.012,.010,.007,.0035],'bee_brown')
            leg['leg_side']=side;leg['leg_index']=i;leg['thoracic_root']=True
        wing('forewing_'+str(side),(-.16,side*.07,z+.07),(-.29,side*span,z+.28),.102 if queen else .090,'bee_wing',side,0)
        wing('hindwing_'+str(side),(-.035,side*.07,z+.065),(.12,side*span*.78,z+.21),.074 if queen else .064,'bee_wing',side,1)
    tailx=.48 if queen else .365;tailz=.387 if queen else .468
    sting=limb('sting',[(tailx,0,tailz),(tailx+.055,0,tailz-.025),(tailx+.08,0,tailz-.055)],[.016,.009,.001],'bee_dark');sting['source_attack']='AT_STNG/AD_DRST'
    abdomen['queen_proportions']=queen

def xan():
    g.GROUP='xan';z=.48
    thorax=orb('thorax',(-.105,0,z),(.125,.075,.095),'xan_green');thorax['anatomy_role']='thorax'
    # Slender, raised green abdomen rather than a striped bee gaster.
    abdomen=limb('abdomen',[(0,0,z),(.13,0,z+.045),(.28,0,z+.14),(.38,0,z+.205)],[.065,.067,.055,.026],'xan_green');abdomen['mosquito_abdomen']=True
    head=orb('head',(-.275,0,z-.07),(.102,.093,.085),'xan_green');head['anatomy_role']='head'
    for side in [-1,1]:
        eye=orb('eye_'+str(side),(-.305,side*.069,z-.066),(.055,.042,.055),'xan_white');eye['eye_side']=side
        orb('pupil_'+str(side),(-.337,side*.098,z-.066),(.024,.018,.026),'black')
        limb('antenna_'+str(side),[(-.306,side*.03,z-.008),(-.39,side*.08,z+.07),(-.45,side*.13,z+.08)],[.005,.004,.002],'xan_gold')
        for i,x in enumerate([-.18,-.10,-.02]):
            splay=[-.17,.025,.23][i]
            leg=limb('leg_%d_%d'%(i,side),[(x,side*.05,z-.035),(x+splay,side*.16,z-.14),(x+splay+.015,side*.29,z-.30),(x+splay-.025,side*.32,z-.32)],[.009,.007,.0045,.002],'xan_gold')
            leg['leg_side']=side;leg['leg_index']=i;leg['thoracic_root']=True
        wing('wing_'+str(side),(-.10,side*.055,z+.055),(.14,side*.43,z+.23),.060,'xan_wing',side,0)
        # Two short balancing knobs distinguish the one-pair wing plan.
        limb('haltere_stalk_'+str(side),[(-.015,side*.065,z+.02),(.018,side*.103,z+.06)],[.004,.003],'xan_green')
        orb('haltere_knob_'+str(side),(.018,side*.103,z+.06),(.008,)*3,'xan_gold')
    proboscis=limb('proboscis',[(-.35,0,z-.11),(-.45,0,z-.17),(-.54,0,z-.22)],[.010,.007,.0015],'xan_green');proboscis['source_attack']='AT_STNG/AD_LEGS'

def pigment(obj,p,base,colors):
    if obj.get('striped_abdomen'):
        q=obj.matrix_world.inverted()@p;length=obj['abdomen_length']
        stripe=.5+.5*math.cos((q.x/length)*math.pi*3.2)
        t=max(0,min(1.,(stripe-.35)*3.))
        return tuple(a*(1-t)+b*t for a,b in zip(base,colors['bee_dark']))
    if obj.get('insect_wing'):
        root=Vector(obj['wing_root']);tip=Vector(obj['wing_tip']);t=(p-root).dot(tip-root)/(tip-root).length_squared
        if obj['creature']!='xan' and t<.22:
            amount=.5*(1-max(0,t)/.22)
            return tuple(a*(1-amount)+b*amount for a,b in zip(base,colors['bee_wing_root']))
    if obj['creature']=='xan' and obj.get('mosquito_abdomen'):
        t=.14*(.5+.5*math.sin(p.x*95))
        return tuple(a*(1-t)+b*t for a,b in zip(base,colors['xan_pale']))
    return base
