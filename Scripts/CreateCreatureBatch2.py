"""Jackal, fox and gnome: complete static anatomical drafts from official tiles.

Uses the established painted mesh helpers, with a parameterised canid family.
The final pipeline paints corners, fixes normals, exports and compares pixels.
"""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from CreatureGeometry import *
import CreatureGeometry as geometry

bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)

def pigment(key,color):
    COLORS[key]=color
    mat=bpy.data.materials.new(key); mat.use_nodes=True; mat.diffuse_color=(*color,1)
    mat.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.82
    MATS[key]=mat

for key,color in {
    'silver':(.52,.54,.51),'silver_light':(.68,.69,.64),'saddle':(.28,.30,.28),
    'fox_coat':(.90,.205,.012),'fox_light':(1,.31,.018),'ivory':(.80,.75,.62),
    'pink':(.42,.055,.21),'lime':(.13,.77,.012),'forest':(.008,.29,.008),
    'red':(.78,.012,.008),'peach':(.78,.40,.23),'beard':(.64,.67,.60),
}.items(): pigment(key,color)

def canid(key,length,leg_height,head_z,muzzle,ear_height,coat,light,tail_points,tail_radii):
    """Shared anatomy; species dimensions, markings and tail construction differ."""
    geometry.GROUP=key
    shoulder=-length*.62; hip=length*.61; z=leg_height+.13
    parts=[orb('ribcage',(-.04,0,z),(length,.115,.145),coat),
        orb('haunch',(hip,0,z-.015),(.13,.115,.14),coat),
        orb('shoulder',(shoulder,0,z+.015),(.11,.12,.15),coat),
        limb('neck',[(shoulder,0,z),(shoulder-.055,0,head_z-.055)],[.105,.08],coat),
        orb('skull',(shoulder-.09,0,head_z),(.112,.086,.10),coat)]
    for back,x in [(False,shoulder),(True,hip)]:
        for side in [-1,1]:
            points=[(x,side*.075,z),(x+(.065 if back else -.005),side*.085,leg_height*.56),
                    (x+(.025 if back else -.005),side*.09,.055)]
            parts.append(limb('leg',points,[.043,.027,.019],coat))
    body=sculpt_union(parts,'connected_anatomy',coat,.008)
    if key=='jackal': body['coat_marking']='saddle'
    for back,x in [(False,shoulder),(True,hip)]:
        for side in [-1,1]:
            limb('dark_sock',[(x+(.035 if back else -.005),side*.09,.14),
                (x+(.025 if back else -.005),side*.09,.045)],[.022,.02],'saddle' if key=='jackal' else 'black')
            orb('paw',(x+(.005 if back else -.03),side*.09,.026),(.046,.031,.026),'silver_light' if key=='jackal' else 'black')
    hx=shoulder-.09
    snout=orb('tapered_muzzle',(hx-.095,0,head_z-.035),(muzzle,.052,.043),light)
    orb('nose',(hx-.095-muzzle*.85,0,head_z-.023),(.024,.031,.021),'black')
    for side in [-1,1]:
        ear('ear',(hx+.025,side*.052,head_z+.045),(hx+.045,side*.08,head_z+ear_height),.044,.035,coat)
        ear('ear_lining',(hx+.009,side*.052,head_z+.068),(hx+.031,side*.075,head_z+ear_height-.025),.025,.012,'pink')
        orb('eye',(hx-.062,side*.075,head_z+.023),(.024,.013,.022),'black')
        orb('eye_glint',(hx-.069,side*.085,head_z+.033),(.007,.004,.006),'glint')
        limb('mouth',[(hx-.17,side*.04,head_z-.059),(hx-.07,side*.056,head_z-.065)],[.004,.003],'black')
        for j in range(3):
            limb('cheek_fur',[(hx+.01,side*.066,head_z-.015-j*.018),
                (hx+.09,side*.102,head_z-.045-j*.018)],[.029,.002],light)
    orb('throat',(shoulder-.085,0,z+.005),(.046,.093,.10),light)
    tail=limb('tail',tail_points,tail_radii,coat)
    mod=tail.modifiers.new('Smooth tail','SUBSURF'); mod.levels=2
    if key=='fox':
        tip=limb('pale_tail_tip',tail_points[-3:], [tail_radii[-3]*1.015,tail_radii[-2]*1.015,tail_radii[-1]],'ivory')
        tip.modifiers.new('Soft tail tip','SUBSURF').levels=2

canid('jackal',.265,.27,.58,.105,.21,'silver','silver_light',
    [(.20,0,.41),(.32,0,.48),(.36,0,.63),(.32,0,.72),(.27,0,.73)],[.042,.039,.028,.018,.003])
canid('fox',.245,.19,.445,.078,.165,'fox_coat','fox_light',
    [(.18,0,.30),(.32,.015,.31),(.44,.025,.26),(.51,.02,.15),(.53,.015,.09)],[.047,.085,.083,.052,.003])

def gnome(rank=False):
    """Neutral shared body; clothing and future rank attachments stay separate."""
    geometry.GROUP='gnome'
    body=[orb('torso',(0,0,.46),(.16,.105,.20),'peach'),orb('neck',(0,0,.65),(.065,.065,.08),'peach'),
          orb('head',(0,-.012,.76),(.13,.11,.14),'peach'),orb('nose',(0,-.125,.75),(.046,.065,.048),'peach')]
    for side in [-1,1]:
        body.append(limb('leg',[(side*.078,0,.36),(side*.10,0,.20),(side*.10,-.025,.075)],[.058,.044,.033],'peach'))
        body.append(limb('arm',[(side*.135,0,.56),(side*.22,-.01,.43),(side*.22,-.075,.35)],[.044,.035,.029],'peach'))
        body.append(orb('hand',(side*.22,-.075,.335),(.037,.032,.046),'peach'))
    sculpt_union(body,'body','peach',.007)
    tunic=cloth('green_tunic',.27,.63,.205,.185,'lime')
    tunic.location.y=-.055  # Centre the garment on this body's torso.
    cloth('rank_ready_mantle',.43,.65,.225,.19,'forest',True)
    for side in [-1,1]:
        box('boot',(side*.10,-.055,.055),(.115,.18,.11),'forest',.025)
        orb('ear',(side*.13,-.005,.77),(.027,.025,.046),'peach')
        orb('eye',(side*.048,-.11,.79),(.018,.011,.017),'black')
        orb('eye_glint',(side*.049,-.119,.797),(.005,.003,.005),'glint')
        orb('brow',(side*.047,-.108,.817),(.036,.017,.011),'beard')
        for i in range(3):
            limb('beard_lock',[(side*(.025+i*.027),-.093,.72),
                (side*(.012+i*.018),-.123,.60+i*.018)],[.032,.002],'beard')
    orb('beard_chin',(0,-.10,.68),(.064,.045,.065),'beard')
    orb('cap_band',(0,0,.855),(.142,.114,.038),'forest')
    limb('pointed_cap',[(0,0,.86),(-.014,0,.95),(-.047,.005,1.055),(-.09,.006,1.085)], [.132,.103,.047,.005],'lime')
    orb('red_cap_tip',(-.078,-.006,1.065),(.043,.04,.037),'red')
    box('belt',(0,-.005,.38),(.31,.22,.039),'leather',.01)
    box('buckle',(0,-.12,.38),(.048,.022,.04),'brass',.005)
    # Art-only axe cue from black tile mass. Separate objects, not fused to hand.
    limb('detachable_axe_shaft',[(.225,-.075,.17),(.225,-.075,.64)],[.015,.015],'cap')
    box('detachable_axe_head',(.285,-.075,.58),(.17,.045,.12),'steel',.012)
    if rank: raise ValueError('Rank is a future module; no ruler export in this batch')

gnome()
exec(compile((Path(__file__).with_name('CreatureBatch2Pipeline.py')).read_text(),
             'CreatureBatch2Pipeline.py','exec'))
