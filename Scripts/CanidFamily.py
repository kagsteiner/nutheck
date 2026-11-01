"""Parameterised canid anatomy with explicit coat, eye, muzzle and tail variants."""
from CreatureGeometry import *
import CreatureGeometry as geo
from WinterWolfEyes import winter_wolf_eyes

def canid(key,length,width,depth,leg,head,muzzle,ear_height,paw,domestic=True,
          coat=None,pale=None,inner='canid_inner',iris='canid_amber',nose='black',marking=None,tail_form=None):
    geo.GROUP=key
    coat=coat or ('dog_ginger' if domestic else 'dingo_ginger')
    pale=pale or ('dog_cream' if domestic else 'dingo_pale')
    shoulder=-length*.60;hip=length*.64;z=leg+depth
    hx=shoulder-.085;hz=z+depth*.91
    parts=[orb('ribs',(-.02,0,z),(length,width,depth),coat),
        orb('pelvis',(hip,0,z-.012),(length*.43,width*.94,depth*.92),coat),
        orb('shoulder',(shoulder,0,z+.018),(.11,width*1.03,depth*1.03),coat),
        limb('neck',[(shoulder,0,z),(hx+.02,0,hz-.025)],[width*.85,head*.76],coat),
        orb('skull',(hx,0,hz),(head,head*.80,head*.91),coat)]
    for back,x in [(False,shoulder),(True,hip)]:
        for side in [-1,1]:
            y=side*width*.66
            parts.append(limb('leg',[(x,y,z),
                (x+(.070 if back else -.005),y,leg*.59),
                (x+(.023 if back else -.008),y,.054)],
                [width*.39,width*.25,width*.19],coat))
            parts.append(orb('paw',(x-.018,y,.030),(paw,paw*.69,.030),coat))
    body=sculpt_union(parts,'continuous_anatomy',coat,.007)
    body['coat_marking']=marking or ('canid_bib' if domestic else 'dingo_underside')
    body['body_center_z']=z;body['shoulder_x']=shoulder;body['body_depth']=depth
    body['body_width']=width;body['head_to_torso_length']=head/length
    body['body_length']=length;body['muzzle_length']=muzzle
    body['family_variant']='domestic' if domestic else 'dingo'
    orb('muzzle',(hx-head*.68,0,hz-head*.27),(muzzle,head*.54,head*.40),pale)
    nx=hx-head*.68-muzzle*.84
    orb('nose',(nx,0,hz-head*.16),(head*.20,head*.25,head*.16),nose)
    for side in [-1,1]:
        ear('ear',(hx+.02,side*head*.48,hz+.045),
            (hx+.045,side*head*.67,hz+ear_height),head*.42,.035,coat)
        ear('ear_lining',(hx+.005,side*head*.48,hz+.066),
            (hx+.028,side*head*.64,hz+ear_height-.028),head*.24,.012,inner)
        limb('mouth',[(nx+.015,side*head*.31,hz-head*.53),
            (hx-head*.32,side*head*.50,hz-head*.52)],[.0027,.0022],'black')
    if domestic:
        orb('tongue',(nx+.026,-.009,hz-head*.56),(head*.18,head*.20,head*.085),'tongue')
    bpy.context.view_layer.update()
    winter_wolf_eyes(key,hx,hz,head,body,iris=iris,lid_pigment=coat)
    geo.GROUP=key
    if tail_form=='brush':
        points=[(hip,0,z+.035),(hip+.13,0,z+.09),(hip+.25,.01,z+.12),(hip+.32,.015,z+.14)]
        radii=[width*.34,width*.45,width*.33,.005]
    elif tail_form=='raised':
        points=[(hip,0,z+.035),(hip+.13,0,z+.11),(hip+.18,.01,z+.25),(hip+.16,.015,z+.36),(hip+.10,.015,z+.40)]
        radii=[width*.37,width*.40,width*.29,width*.18,.005]
    elif domestic:
        points=[(hip,0,z+.035),(hip+.135,0,z+.13),
            (hip+.16,.01,z+.27),(hip+.085,.015,z+.35),(hip-.015,.015,z+.32)]
        radii=[width*.40,width*.43,width*.34,width*.23,.006]
    else:
        points=[(hip,0,z+.035),(hip+.14,0,z+.015),
            (hip+.26,.01,z-.055),(hip+.32,.015,z-.16),(hip+.30,.015,z-.23)]
        radii=[width*.35,width*.39,width*.32,width*.22,.005]
    tail=limb('curled_tail' if domestic else 'swept_tail',points,radii,coat)
    tail.modifiers.new('Soft tail curve','SUBSURF').levels=2
    tail['tail_form']=tail_form or ('curled' if domestic else 'swept_down')
    for obj in bpy.context.scene.objects:
        if obj.type=='MESH' and obj.get('creature')==key and obj.get('pigment') in {coat,pale} and not obj.get('eye_side'):
            obj['fur_surface']=True;obj['fur_leg_height']=leg
    return body

