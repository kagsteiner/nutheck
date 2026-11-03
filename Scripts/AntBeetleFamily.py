"""Static painted insect anatomy; reuses the original ant construction, not its export.

Body axes match giant_ant: biting head toward -X; all six legs root in thorax.
Female ant thoraces and leg reach are independently enlarged after sex-tile review.
Beetle has broad joined thoracic plan and closed paired elytra, without ant waist.
"""
import CreatureGeometry as G
from CreatureGeometry import orb,limb,COLORS

def elytron(side):
    import math
    from mathutils import Vector
    # Closed half ellipsoid with a planar medial cut: paired domes meet at 12mm seam.
    n=48;rings=12;verts=[(.18,side*.271,.30)];faces=[]
    for ring in range(1,rings+1):
        phi=math.pi*.5*ring/rings
        for j in range(n):
            a=math.tau*j/n
            verts.append((.18+.34*math.sin(phi)*math.cos(a),side*(.006+.265*math.cos(phi)),.30+.235*math.sin(phi)*math.sin(a)))
    for j in range(n):faces.append((0,1+j,1+(j+1)%n))
    for ring in range(rings-1):
        for j in range(n):
            a=1+ring*n+j;b=1+ring*n+(j+1)%n;faces.append((a,a+n,b+n,b))
    faces.append(tuple(reversed([1+(rings-1)*n+j for j in range(n)])))
    mesh=G.bpy.data.meshes.new('Closed elytron');mesh.from_pydata(verts,[],faces);mesh.update()
    o=G.bpy.data.objects.new('elytron',mesh);G.bpy.context.collection.objects.link(o)
    for p in mesh.polygons:p.use_smooth=len(p.vertices)==4 or len(p.vertices)==3
    G.finish(o,'elytron_'+str(side),'beetle_red');o['closed_elytron']=side
    return o

def ant(key,female=False):
    G.GROUP=key;fire=key.startswith('fire');sx=1.06 if female else 1.;sy=1.10 if female else 1.
    shell='fire_shell' if fire else 'shell';light='fire_light' if fire else 'shell_light';joint='fire_joint' if fire else 'joint'
    # Compatible saved giant-ant recipe, with separately parameterised soldier head.
    orb('gaster',(.25,0,.26),(.24,.15,.17),shell)
    thorax=orb('thorax',(-.055,0,.27),(.15*sx,.105*sy,.12*(1.07 if female else 1)),light)
    thorax['anatomy_role']='thorax';thorax['female_form']=female
    orb('petiole',(.105,0,.25),(.07,.065,.06),joint)
    headsize=(.16,.145,.115) if fire else (.205,.18,.135)
    head=orb('head',(-.285 if fire else -.32,0,.255),headsize,light);head['anatomy_role']='head'
    # Gentle segment paint replaces the old raised gaster ridges on new forms.
    for i,dx in enumerate([-.13,-.045,.04]):
        for side in [-1,1]:
            splay=[-.16,0,.16][i];reach=.43*sy
            leg=limb('leg_%d_%d'%(i,side),[(dx,side*.075,.27),(dx+splay,side*.24*sy,.30),(dx+splay+.035,side*.39*sy,.12),(dx+splay-.02,side*reach,.027)],[.027,.024,.016,.007],joint)
            leg['leg_index']=i;leg['leg_side']=side;leg['root_thorax']=True
            orb('leg_joint_%d_%d'%(i,side),(dx+splay,side*.24*sy,.30),(.03,.028,.027),shell)
    for side in [-1,1]:
        x=-.31 if fire else -.36;y=.125 if fire else .16
        eye=orb('compound_eye_'+str(side),(x,side*y,.30),(.045,.021,.037),'black');eye['eye_side']=side
        orb('eye_accent_'+str(side),(x-.018,side*(y+.017),.307),(.016,.006,.011),'fire_eye' if fire else 'cyan')
        limb('antenna_'+str(side),[(-.34,side*.075,.34),(-.44,side*.18,.43),(-.56,side*.20,.40)],[.012,.009,.006],shell)
        if fire:pts=[(-.39,side*.085,.23),(-.49,side*.10,.22),(-.54,side*.025,.23)];r=[.041,.032,.005]
        else:pts=[(-.47,side*.105,.22),(-.61,side*.14,.18),(-.66,side*.055,.17)];r=[.048,.035,.006]
        jaw=limb('mandible_'+str(side),pts,r,light);jaw['mandible_side']=side
    if not fire:
        sting=limb('sting',[(.43,0,.23),(.51,0,.19),(.53,0,.145)],[.033,.018,.002],joint);sting['source_attack_hook']='AT_STNG/AD_DRST'

def beetle(key='giant_beetle'):
    G.GROUP=key
    # Broad uninterrupted abdomen/pronotum, six stout thoracic legs, small head.
    orb('abdomen',(.18,0,.30),(.31,.23,.195),'beetle_dark')
    pron=orb('pronotum',(-.17,0,.29),(.21,.245,.18),'beetle_orange');pron['anatomy_role']='thorax'
    head=orb('head',(-.385,0,.235),(.14,.17,.105),'beetle_red');head['anatomy_role']='head'
    for side in [-1,1]:
        # Closed convex half-ellipsoids follow the dome; slight central parting.
        elytron(side)
        for i,x in enumerate([-.28,-.16,-.035]):
            splay=[-.16,.015,.22][i]
            leg=limb('leg_%d_%d'%(i,side),[(x,side*.15,.255),(x+splay,side*.29,.27),(x+splay+.015,side*.40,.10),(x+splay-.03,side*.44,.025)],[.035,.033,.021,.009],'beetle_dark')
            leg['leg_index']=i;leg['leg_side']=side;leg['root_thorax']=True
        eye=orb('compound_eye_'+str(side),(-.41,side*.152,.255),(.035,.016,.027),'black');eye['eye_side']=side
        orb('eye_accent_'+str(side),(-.423,side*.165,.262),(.015,.005,.012),'cyan')
        limb('antenna_'+str(side),[(-.44,side*.10,.28),(-.53,side*.20,.31),(-.57,side*.23,.29)],[.012,.009,.008],'beetle_orange')
        jaw=limb('mandible_'+str(side),[(-.48,side*.09,.205),(-.57,side*.10,.17),(-.61,side*.035,.17)],[.033,.026,.003],'beetle_dark');jaw['mandible_side']=side

def insect_pigment(obj,p,base,colors):
    import math
    if 'gaster' in obj.name:
        # Integument shading only: no extra ring/saddle geometry.
        band=.10*(.5+.5*math.cos((p.x-.10)*64))
        return tuple(c*(1-band) for c in base)
    if obj.get('closed_elytron'):
        # Tile orange/peach dorsal reflection, red flanks; sculpt remains continuous.
        t=max(0,min(.72,(p.z-.37)*4))*(.65+.35*math.cos(p.x*8))
        return tuple(a*(1-t)+b*t for a,b in zip(base,colors['beetle_highlight']))
    return base
