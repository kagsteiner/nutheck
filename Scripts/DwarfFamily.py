"""Stout dwarf ancestry, shared sex appearance, separate cap and rank modules."""
import math
import bpy
import CreatureGeometry as g
from CreatureGeometry import orb,limb,box,sculpt_union
from mathutils import Vector

def sleeve_tube(side):
    # A consistent frame avoids the general tube helper's axis change near
    # vertical bends, which can twist a fitted sleeve through the elbow.
    points=[(side*.153,0,.666),(side*.213,-.002,.610),(side*.259,-.004,.555),(side*.274,-.045,.460)]
    radii=[.073,.068,.059,.046];verts=[];faces=[];n=32
    for j,p in enumerate(points):
        direction=(Vector(points[min(j+1,len(points)-1)])-Vector(points[max(j-1,0)])).normalized()
        right=direction.cross(Vector((0,1,0))).normalized();up=direction.cross(right).normalized()
        for i in range(n):
            a=math.tau*i/n;verts.append(Vector(p)+radii[j]*(right*math.cos(a)+up*math.sin(a)))
    for j in range(len(points)-1):
        for i in range(n):
            a=j*n+i;b=j*n+(i+1)%n;faces.append((a,b,b+n,a+n))
    faces.extend([tuple(reversed(range(n))),tuple((len(points)-1)*n+i for i in range(n))])
    mesh=bpy.data.meshes.new('fitted_sleeve');mesh.from_pydata(verts,[],faces);mesh.update()
    obj=bpy.data.objects.new('fitted_sleeve',mesh);bpy.context.collection.objects.link(obj)
    return g.finish(obj,'blue_sleeve','dwarf_blue')

def shell(name,rings,pigment,thickness=.005,closed=False):
    verts=[];faces=[];n=64
    for z,rx,ry,dx,dy in rings:
        for i in range(n):
            a=math.tau*i/n
            verts.append((dx+rx*math.cos(a),dy+ry*math.sin(a),z))
    for j in range(len(rings)-1):
        for i in range(n):
            a=j*n+i;b=j*n+(i+1)%n;faces.append((a,b,b+n,a+n))
    if closed:faces.extend([tuple(reversed(range(n))),tuple((len(rings)-1)*n+i for i in range(n))])
    mesh=bpy.data.meshes.new(name);mesh.from_pydata(verts,[],faces);mesh.update()
    obj=bpy.data.objects.new(name,mesh);bpy.context.collection.objects.link(obj)
    for p in mesh.polygons:p.use_smooth=True
    if not closed:obj.modifiers.new('Closed cloth thickness','SOLIDIFY').thickness=thickness
    return g.finish(obj,name,pigment)

def dwarf():
    g.GROUP='dwarf'
    skin='dwarf_skin'
    parts=[orb('torso',(0,0,.54),(.175,.125,.215),skin),
           orb('neck',(0,0,.746),(.078,.075,.085),skin),
           orb('skull',(0,-.006,.842),(.126,.111,.139),skin),
           orb('jaw',(0,-.037,.768),(.105,.091,.075),skin),
           orb('nose',(0,-.119,.830),(.034,.043,.040),skin)]
    for side in [-1,1]:
        parts.extend([limb('leg',[(side*.086,0,.40),(side*.107,0,.23),(side*.111,-.012,.073)],[.068,.051,.040],skin),
                      orb('foot',(side*.111,-.048,.039),(.065,.100,.038),skin),
                      limb('arm',[(side*.153,0,.666),(side*.259,-.004,.555),(side*.279,-.060,.424)],[.061,.047,.035],skin),
                      orb('shoulder',(side*.172,0,.654),(.073,.069,.077),skin),
                      orb('elbow',(side*.259,-.004,.555),(.048,.047,.047),skin),
                      orb('hand',(side*.279,-.060,.404),(.041,.038,.052),skin)])
    body=sculpt_union(parts,'body',skin,.0065)
    body['family']='dwarf';body['shared_ancestry']=True
    for side in [-1,1]:
        orb('ear',(side*.121,-.002,.834),(.026,.022,.041),skin)
        eye=orb('eye',(side*.046,-.110,.862),(.015,.009,.014),'black');eye['eye_side']=side
        limb('brow',[(side*.023,-.107,.880),(side*.045,-.115,.884),(side*.069,-.099,.878)],[.009,.011,.008],'dwarf_beard')
        limb('lower_lid',[(side*.032,-.111,.851),(side*.048,-.114,.848),(side*.060,-.104,.851)],[.005,.005,.004],skin)
        # Closed fitted leg/sleeve masses sit over the continuous ancestry.
        limb('blue_trouser',[(side*.086,0,.390),(side*.107,0,.23),(side*.111,-.012,.080)],[.074,.058,.047],'dwarf_blue')
        sleeve=[orb('blue_shoulder',(side*.172,0,.654),(.079,.075,.083),'dwarf_blue'),
                sleeve_tube(side)]
        sculpt_union(sleeve,'fitted_sleeve','dwarf_blue',.004)
        boot=orb('blue_boot',(side*.111,-.049,.043),(.067,.103,.042),'dwarf_blue');boot['boot']=True
        for finger in [-1,0,1]:
            limb('finger_seam',[(side*.279+finger*.010,-.095,.416),(side*.279+finger*.010,-.095,.389)],[.0015,.0011],'dwarf_skin_shade')
    shirt=shell('blue_tunic',[(.352,.156,.113,0,0),(.40,.177,.130,0,0),(.48,.185,.137,0,0),(.56,.182,.137,0,0),(.64,.198,.132,0,0),(.70,.158,.112,0,0),(.735,.090,.083,0,0)],'dwarf_blue')
    shirt['garment_module']=True
    # Full pale beard follows the chin and upper chest, rather than a floating slab.
    beard_parts=[orb('beard_chin',(0,-.108,.762),(.086,.049,.071),'dwarf_beard')]
    for side in [-1,1]:
        for i in range(3):
            beard_parts.append(limb('beard_lock',[(side*(.023+i*.024),-.097,.801-i*.006),(side*(.024+i*.021),-.143,.737),(side*(.010+i*.019),-.144,.665+i*.022)],[.030,.029,.008],'dwarf_beard'))
        limb('moustache',[(side*.005,-.145,.800),(side*.034,-.149,.790),(side*.060,-.130,.780)],[.014,.018,.008],'dwarf_beard')
    beard=sculpt_union(beard_parts,'fitted_beard','dwarf_beard',.0035);beard['beard_module']=True
    cap=shell('blue_cap_band',[(.925,.128,.111,0,-.006),(.955,.130,.113,0,-.006),(.974,.117,.103,0,0)],'dwarf_blue');cap['cap_module']=True
    cap=shell('pointed_blue_cap',[(.957,.119,.105,0,0),(.980,.113,.100,-.003,.002),(1.01,.097,.086,-.008,.004),(1.04,.074,.065,-.018,.006),(1.065,.050,.044,-.030,.008),(1.085,.027,.024,-.043,.010),(1.104,.002,.002,-.055,.010)],'dwarf_blue',closed=True)
    cap['pointed_cap']=True
    return body

def crown_details():
    for i in range(8):
        a=math.tau*i/8;radial=Vector((math.cos(a),math.sin(a),0));tangent=Vector((-math.sin(a),math.cos(a),0))
        center=Vector((.131*math.cos(a),-.004+.115*math.sin(a),0))
        outline=[(-.026,.970),(.026,.970),(.016,1.065),(0,1.098),(-.016,1.065)]
        verts=[center+tangent*x+radial*depth+Vector((0,0,z)) for depth in [-.005,.005] for x,z in outline]
        faces=[tuple(reversed(range(5))),tuple(range(5,10))]+[(j,(j+1)%5,(j+1)%5+5,j+5) for j in range(5)]
        mesh=bpy.data.meshes.new('crown_point');mesh.from_pydata(verts,[],faces);mesh.update()
        obj=bpy.data.objects.new('crown_point',mesh);bpy.context.collection.objects.link(obj)
        bevel=obj.modifiers.new('Soft metal edge','BEVEL');bevel.width=.002;bevel.segments=2
        g.finish(obj,'detachable_crown_point','dwarf_gold');obj['rank_module']=True
    for side in [-1,1]:
        jewel=orb('detachable_orange_inlay',(side*.061,-.111,.962),(.013,.008,.012),'dwarf_orange');jewel['rank_module']=True

def variants():
    base=[o for o in bpy.context.scene.objects if o.type=='MESH' and o.get('creature')=='dwarf']
    for key in ['dwarf_leader','dwarf_ruler']:
        for obj in base:
            if key=='dwarf_ruler' and obj.get('pointed_cap'):continue
            copy=obj.copy();copy.data=obj.data.copy();copy.name=key+obj.name[len('dwarf'):];copy['creature']=key
            bpy.context.collection.objects.link(copy)
        g.GROUP=key
        band=shell('detachable_gold_band',[(.942,.133,.117,0,-.004),(.977,.133,.117,0,-.004)],'dwarf_gold',.008)
        band['rank_module']=True
        if key=='dwarf_ruler':
            crown_details()

def dwarf_pigment(obj,p,pigment,colors):
    if obj.get('pigment')=='dwarf_blue':
        # Source blue/cyan masses are interpreted as two-tone fabric lighting.
        t=max(0,min(1,(.06-p.x)/.24))*.55
        return tuple(a*(1-t)+b*t for a,b in zip(pigment,colors['dwarf_cyan']))
    return pigment
