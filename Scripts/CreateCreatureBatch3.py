"""Parameterised rats and an actual reuse of the existing gnome anatomy.

All three are static drafts, not rigged characters. Crown and rank garments are
detachable art modules; they do not assert the live monster's inventory.
"""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from CreatureGeometry import *
import CreatureGeometry as geometry

bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)

def pigment(key,color,metallic=0,roughness=.82):
    COLORS[key]=color
    mat=bpy.data.materials.new(key); mat.use_nodes=True; mat.diffuse_color=(*color,1)
    shader=mat.node_tree.nodes['Principled BSDF']
    shader.inputs['Roughness'].default_value=roughness
    shader.inputs['Metallic'].default_value=metallic
    MATS[key]=mat

for key,color in {
    'rat_brown':(.43,.105,.006),'rat_ochre':(.59,.185,.015),
    'rat_dark':(.18,.055,.006),'rat_ear':(.38,.14,.055),
    'rat_tail':(.29,.095,.023),'tooth':(.69,.67,.48),
    'nose_blue':(.16,.25,.28),'crown_gold':(.95,.66,.005),
    'rank_dark':(.012,.19,.018),'rank_trim':(.65,.35,.018),
    'jewel':(.87,.09,.004),
}.items(): pigment(key,color)

def rat(key,length,width,body_height,ground_clearance,head_length,head_width,ear_size,tail_length,
        trunk_width_factor,trunk_height_factor):
    """Compatible anatomy, not a uniform scale: length, bulk, skull and legs vary."""
    geometry.GROUP=key
    z=ground_clearance+body_height
    hip=length*.56; shoulder=-length*.51; hx=-length*.86
    hz=ground_clearance+body_height*.62
    # User-approved departure from the squat tile: narrow the trunk and reduce
    # its depth while retaining body/head placement and all facial geometry.
    trunk_width=width*trunk_width_factor; trunk_height=body_height*trunk_height_factor
    parts=[orb('ribcage',(0,0,z),(length,trunk_width,trunk_height),'rat_brown'),
        orb('rump',(hip,0,z),(length*.60,trunk_width*.94,trunk_height*.94),'rat_brown'),
        orb('neck',(shoulder,0,hz+.015),(head_length*.88,head_width*.91,trunk_height*.68),'rat_brown'),
        orb('skull',(hx,0,hz),(head_length,head_width,head_length*.66),'rat_brown'),
        orb('muzzle',(hx-head_length*.78,0,hz-head_length*.28),
            (head_length*.85,head_width*.67,head_length*.38),'rat_brown')]
    for side in [-1,1]:
        parts.append(orb('hind_haunch',(hip,side*trunk_width*.60,z*.67),
            (length*.35,trunk_width*.48,trunk_height*.72),'rat_brown'))
        for back,x in [(False,shoulder),(True,hip)]:
            parts.append(limb('leg',[(x,side*trunk_width*.62,z*.66),
                (x+(.04 if back else 0),side*trunk_width*.94,.06),
                (x-.022,side*trunk_width*1.02,.025)],
                [trunk_width*.27,trunk_width*.17,trunk_width*.12],'rat_brown'))
    sculpt_union(parts,'continuous_anatomy','rat_brown',.006)
    for side in [-1,1]:
        for back,x in [(False,shoulder),(True,hip)]:
            orb('paw',(x-.035,side*trunk_width*1.02,.022),(.047,trunk_width*.25,.021),'rat_ochre')
            for finger in range(5 if back else 4):
                y=side*trunk_width*1.02+(finger-2)*.009
                limb('toe',[(x-.042,y,.023),(x-.075,y,.013)],[.006,.0025],'rat_ochre')
        ex=hx+head_length*.27; ey=side*head_width*.75; ez=hz+head_length*.61
        orb('round_ear',(ex,ey,ez),(ear_size,ear_size*.32,ear_size*1.12),'rat_ochre')
        orb('ear_cup',(ex-.003,ey+side*ear_size*.23,ez+.002),
            (ear_size*.72,ear_size*.13,ear_size*.79),'rat_ear')
        orb('eye_socket',(hx-head_length*.29,side*head_width*.83,hz+head_length*.15),
            (.021,.012,.020),'rat_dark')
        orb('green_eye',(hx-head_length*.36,side*(head_width*.83+.013),hz+head_length*.17),
            (.012,.006,.011),'green')
        orb('eye_glint',(hx-head_length*.39,side*(head_width*.83+.019),hz+head_length*.21),
            (.003,.002,.003),'glint')
        for j in range(3):
            limb('whisker',[(hx-head_length*1.27,side*head_width*.42,hz-head_length*.20),
                (hx-head_length*(1.55-j*.24),side*head_width*1.75,hz+(.02-j*.022))],
                [.002,.0008],'rat_ochre')
    nx=hx-head_length*1.46
    orb('nose',(nx,0,hz-head_length*.25),(.022,.027,.020),'rat_dark')
    orb('cool_nose_glint',(nx-.015,-.012,hz-head_length*.20),(.009,.012,.007),'nose_blue')
    limb('mouth',[(nx+.01,-head_width*.42,hz-head_length*.43),
        (hx-head_length*.65,-head_width*.63,hz-head_length*.44)],[.004,.003],'rat_dark')
    for side in [-1,1]:
        box('incisor',(nx+.022,side*.007,hz-head_length*.52),(.015,.011,.023),'tooth',.003)
    tail=limb('bare_tail',[(hip+length*.34,0,z*.67),
        (hip+length*.65,.025,.07),(hip+tail_length*.67,.09,.045),
        (hip+tail_length,.15,.04),(hip+tail_length*1.06,.20,.053)],
        [width*.24,width*.19,width*.13,width*.065,.002],'rat_tail')
    tail.modifiers.new('Tail smoothing','SUBSURF').levels=2

rat('sewer_rat',.19,.085,.095,.035,.087,.063,.034,.32,.74,.74)
rat('giant_rat',.245,.134,.16,.042,.103,.086,.042,.37,.62,.60)

# Append the exact editable body and clothing, rather than copy/rebuild anatomy.
base=OUT/'CreatureBatch2.blend'
with bpy.data.libraries.load(str(base),link=False) as (available,loaded):
    loaded.objects=[name for name in available.objects if name.startswith('gnome_')]
geometry.GROUP='gnome_ruler'
omitted=('gnome_cap_band','gnome_pointed_cap','gnome_red_cap_tip')
for obj in loaded.objects:
    if obj.name.startswith(omitted) or obj.name.startswith('gnome_belt'):
        bpy.data.objects.remove(obj,do_unlink=True); continue
    bpy.context.scene.collection.objects.link(obj)
    obj.name=obj.name.replace('gnome_','gnome_ruler_',1)
    obj['creature']='gnome_ruler'; obj['preserve_paint']=True
    obj.hide_render=False; obj.hide_viewport=False
    if 'mantle' in obj.name:
        obj['pigment']='rank_dark'; obj['preserve_paint']=False
        obj.data.materials.clear(); obj.data.materials.append(MATS['rank_dark'])
        for attr in list(obj.data.color_attributes): obj.data.color_attributes.remove(attr)
    if 'buckle' in obj.name: obj.location.y=-.165

# A fitted curved belt follows the garment rather than widening a square block.
limb('detachable_rank_belt',[(.209*math.cos(math.tau*i/48),
    .14*math.sin(math.tau*i/48),.38) for i in range(49)],[.017]*49,'leather')

# Hollow crown: an actual band with pointed rim, no floating solid cushion.
verts=[]; faces=[]; n=24
for ring in range(4):
    inner=ring in (1,3); top=ring>=2
    for i in range(n):
        a=math.tau*i/n
        radius_x=.140-(.017 if inner else 0); radius_y=.115-(.017 if inner else 0)
        z=.810 if not top else (.955 if i%4==0 else .910)
        verts.append((radius_x*math.cos(a),radius_y*math.sin(a),z))
for i in range(n):
    j=(i+1)%n
    faces.extend([(i,j,2*n+j,2*n+i),(n+j,n+i,3*n+i,3*n+j),
                  (2*n+i,2*n+j,3*n+j,3*n+i),(j,i,n+i,n+j)])
mesh=bpy.data.meshes.new('Detachable crown'); mesh.from_pydata(verts,[],faces);mesh.update()
crown=bpy.data.objects.new('crown',mesh);bpy.context.collection.objects.link(crown)
finish(crown,'detachable_crown','crown_gold')
bevel=crown.modifiers.new('Soft crown edges','BEVEL');bevel.width=.003;bevel.segments=2
orb('crown_jewel',(0,-.116,.871),(.027,.012,.023),'jewel')
for side in [-1,1]:
    limb('rank_trim',[(side*.18,-.055,.63),(side*.21,.06,.52),(side*.22,.09,.44)],
        [.012,.011,.01],'rank_trim')

GROUPS=['sewer_rat','giant_rat','gnome_ruler']
BLEND_NAME='CreatureBatch3.blend';REPORT_NAME='projection-report-batch3.json'
exec(compile(Path(__file__).with_name('CreatureBatch2Pipeline.py').read_text(),
             'CreatureBatch2Pipeline.py','exec'))
