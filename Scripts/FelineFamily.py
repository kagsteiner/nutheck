"""Extend the established paired-muzzle/digitigrade feline construction to wild cats."""
from CreatureGeometry import *
import CreatureGeometry as geo
from WinterWolfEyes import winter_wolf_eyes

def feline(key,length,width,depth,leg,head,head_width,ear_height,paw,tail_height,
           coat,pale,nose,iris,lynx=False,marking='plain_panther'):
    geo.GROUP=key
    z=leg+depth;shoulder=-length*.61;hip=length*.64;hx=shoulder-.075;hz=z+.105
    parts=[orb('ribcage',(-.018,0,z),(length,width,depth),coat),
        orb('pelvis',(hip,0,z-.01),(length*.49,width*.93,depth*.91),coat),
        orb('shoulder',(shoulder,0,z+.012),(.11,width*.97,depth*1.02),coat),
        limb('neck',[(shoulder,0,z+.02),(hx+.035,0,hz-.025)],[width*.75,head_width*.72],coat),
        orb('skull',(hx,0,hz),(head,head_width,head*.90),coat)]
    for back,x in [(False,shoulder),(True,hip)]:
        for side in [-1,1]:
            y=side*width*.65
            points=[(x,y,z),(x+(.055 if back else -.005),side*width*.73,leg*.56+.025),
                (x+(.015 if back else -.008),side*width*.81,.047)]
            parts.append(limb('leg',points,[width*(.38 if key=='jaguar' else .34),width*.25,width*.19],coat))
            parts.append(orb('paw',(x-.018,side*width*.81,.031),(paw,paw*.76,.031),coat))
    body=sculpt_union(parts,'continuous_anatomy',coat,.006)
    body['coat_marking']=marking;body['body_length']=length;body['body_width']=width
    body['body_center_z']=z;body['body_depth']=depth;body['leg_height']=leg
    body['head_to_body_length']=head/length;body['head_length']=head
    body['head_x']=hx;body['head_z']=hz;body['paw_length']=paw
    body['fur_surface']=True;body['fur_leg_height']=leg
    for side in [-1,1]:
        pad=orb('muzzle_pad',(hx-head*.75,side*head_width*.25,hz-head*.28),
            (head*.38,head_width*.39,head*.28),pale)
        pad['fur_surface']=True
        if lynx:
            base=(hx+.008,side*head_width*.65,hz+head*.60)
            tip=(hx+.020,side*head_width*.71,hz+head*.60+ear_height)
            ear('pointed_ear',base,tip,head_width*.40,.034,coat)
            ear('ear_lining',(base[0]-.012,base[1],base[2]+.014),
                (tip[0]-.012,tip[1],tip[2]-.018),head_width*.23,.012,'wild_cat_inner')
            limb('ear_tuft',[(tip[0]-.004,tip[1]-side*.004,tip[2]-.035),
                (tip[0]+.004,tip[1]+side*.006,tip[2]+.030)], [.006,.0008],'wild_cat_dark')
        else:
            orb('rounded_ear',(hx+.030,side*head_width*.70,hz+head*.75),
                (.029,head_width*.36,ear_height*.52),coat)
            orb('ear_lining',(hx+.004,side*head_width*.70,hz+head*.75),
                (.006,head_width*.24,ear_height*.34),'wild_cat_inner' if key!='panther' else 'panther_muzzle')
        for i in range(3):
            limb('whisker',[(hx-head*.96,side*head_width*.40,hz-head*.30),
                (hx-head*(1.20-i*.15),side*(head_width+.065),hz-head*.18-i*.015)],
                [.0014,.0005],'panther_whisker' if key=='panther' else pale)
        for x in [shoulder,hip]:
            for j in [-1,0,1]:
                limb('toe_crease',[(x-.040,side*width*.81+j*.013,.050),
                    (x-.061,side*width*.81+j*.013,.035)],[.0013,.0008],'wild_cat_dark')
    nx=hx-head*1.02-.006;nz=hz-head*.23
    mesh=bpy.data.meshes.new('Feline triangular nose')
    mesh.from_pydata([(nx-.007,-head_width*.20,nz),(nx-.007,head_width*.20,nz),
        (nx-.009,0,nz-head*.13),(nx+.008,0,nz+.002)],[],[(0,2,1),(0,1,3),(1,2,3),(2,0,3)]);mesh.update()
    obj=bpy.data.objects.new('nose',mesh);bpy.context.scene.collection.objects.link(obj);geo.finish(obj,'triangular_nose',nose)
    limb('philtrum',[(nx,0,nz-head*.13),(nx+.004,0,hz-head*.46)], [.002,.0015],'wild_cat_dark')
    for side in [-1,1]:
        limb('mouth',[(nx+.004,0,hz-head*.46),(nx+.020,side*head_width*.31,hz-head*.45)], [.0018,.0012],'wild_cat_dark')
    bpy.context.view_layer.update()
    winter_wolf_eyes(key,hx,hz,head,body,iris=iris,lid_pigment=coat,
        seed_offset=(-.84,.43,.18),normal_hint=(-.84,.69,.22),horizontal_hint=(.635,.773,0))
    geo.GROUP=key
    if lynx:
        points=[(hip+.025,0,z+.025),(hip+.090,.004,z+.075),(hip+.125,.008,z+.10)]
        radii=[.026,.023,.010]
    else:
        points=[(hip+.025,0,z+.025),(hip+.13,.004,z+.13),(hip+.17,.008,z+tail_height*.65),
            (hip+.15,.01,z+tail_height),(hip+.095,.012,z+tail_height+.024)]
        radii=[.032,.030,.025,.018,.006]
    tail=limb('bob_tail' if lynx else 'raised_tail',points,radii,coat)
    tail.modifiers.new('Soft tail curve','SUBSURF').levels=2
    tail['fur_surface']=True;tail['tail_form']='bobbed' if lynx else 'raised_long'
    tail['coat_marking']='lynx_tail_tip' if lynx else 'jaguar_tail' if key=='jaguar' else 'plain'
    tail['tail_root_z']=z+.025;tail['tail_tip_x']=points[-1][0]

