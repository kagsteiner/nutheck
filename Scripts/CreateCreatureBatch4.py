"""One parameterised feline family, with deliberate juvenile/adult proportions."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from CreatureGeometry import *
import CreatureGeometry as geometry

bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)

for key,color in {
    'cat_orange':(.94,.23,.008),'cat_peach':(.94,.48,.24),
    'cat_cream':(.82,.77,.59),'cat_pink':(.68,.012,.23),
    'cat_red':(.65,.021,.012),'cat_ear':(.53,.15,.13),
    'cat_amber':(.45,.46,.065),'cat_shadow':(.15,.052,.008),
}.items():
    COLORS[key]=color
    mat=bpy.data.materials.new(key);mat.use_nodes=True;mat.diffuse_color=(*color,1)
    mat.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.82
    MATS[key]=mat

def feline_ear(name,x,y,z,width,height,depth,pigment):
    # Broad ear faces forward (-X); thickness extends towards the back of head.
    side=1 if y>0 else -1
    verts=[(x,y-width,z),(x,y+width,z),(x+.008,y+side*.012,z+height),
           (x+depth,y,z+.022)]
    mesh=bpy.data.meshes.new(name);mesh.from_pydata(verts,[],[(0,2,1),(0,1,3),(1,2,3),(2,0,3)]);mesh.update()
    obj=bpy.data.objects.new(name,mesh);bpy.context.collection.objects.link(obj)
    bevel=obj.modifiers.new('Soft pinna edge','BEVEL');bevel.width=.005;bevel.segments=2
    return finish(obj,name,pigment)

def feline(key,length,width,depth,leg_height,head_length,head_width,ear_height,paw_size,tail_height,juvenile=False):
    geometry.GROUP=key
    z=leg_height+depth;shoulder=-length*.61;hip=length*.64
    hx=shoulder-.075;hz=z+.105
    body=[orb('ribcage',(-.018,0,z),(length,width,depth),'cat_orange'),
        orb('pelvis',(hip,0,z-.01),(length*.49,width*.93,depth*.91),'cat_orange'),
        orb('shoulder',(shoulder,0,z+.012),(.09,width*.92,depth*.97),'cat_orange'),
        limb('neck',[(shoulder,0,z+.02),(hx+.035,0,hz-.025)],
             [width*.75,head_width*.72],'cat_orange'),
        orb('skull',(hx,0,hz),(head_length,head_width,head_length*.91),'cat_orange')]
    for back,x in [(False,shoulder),(True,hip)]:
        for side in [-1,1]:
            y=side*width*.65
            # Digitigrade rear hock, straighter forearm and wrist.
            points=[(x,y,z),
                (x+(.046 if back else -.005),side*width*.73,leg_height*.55+.025),
                (x+(.015 if back else -.008),side*width*.81,.045)]
            body.append(limb('leg',points,[width*.32,width*.22,width*.17],'cat_orange'))
            body.append(orb('paw',(x-.018,side*width*.81,.027),
                (paw_size,paw_size*.70,.027),'cat_orange'))
    body=sculpt_union(body,'continuous_anatomy','cat_orange',.006)
    body['coat_marking']='cat_flank';body['body_length']=length
    body['body_width']=width;body['body_center_z']=z
    body['age_variant']='juvenile' if juvenile else 'adult'
    body['head_to_torso_length']=head_length/length
    # Short paired muzzle pads distinguish this family from the long canid snout.
    for side in [-1,1]:
        orb('muzzle_pad',(hx-head_length*.78,side*.025,hz-.033),
            (.037,.033,.027),'cat_peach')
        base_y=side*head_width*.57
        feline_ear('outer_ear',hx+.007,base_y,hz+head_length*.60,
            head_width*.43,ear_height,.04,'cat_orange')
        feline_ear('ear_lining',hx+.002,base_y,hz+head_length*.69,
            head_width*.27,ear_height*.70,.012,'cat_ear')
        ex=hx-head_length*.62;ey=side*head_width*.73;ez=hz+.018
        eye=head_width*.29
        orb('eye_white',(ex,ey,ez),(eye*.90,.009,eye*.62),'cat_cream')
        orb('iris',(ex-.006,ey+side*.006,ez),(eye*.62,.005,eye*.58),'cat_amber')
        orb('vertical_pupil',(ex-.010,ey+side*.011,ez),(.004,.003,eye*.50),'black')
        orb('eye_glint',(ex-.014,ey+side*.014,ez+.006),(.003,.002,.003),'glint')
        for i in range(3):
            limb('whisker',[(hx-head_length*.91,side*.042,hz-.037),
                (hx-head_length*(1.14-i*.16),side*(head_width+(.045 if juvenile else .06)),hz-.019-i*.016)],
                [.0018,.0007],'cat_cream')
        # Tiny toe creases keep the paws readable without exposed claws.
        for x in [shoulder,hip]:
            for j in [-1,1]:
                limb('toe_crease',[(x-.038,side*width*.81+j*.011,.045),
                    (x-.049,side*width*.81+j*.011,.032)],[.0015,.001],'cat_shadow')
    nx=hx-head_length*.99
    pigment='cat_red' if key=='large_cat' else 'cat_pink'
    mesh=bpy.data.meshes.new('Feline nose')
    mesh.from_pydata([(nx-.009,-.018,hz-.027),(nx-.009,.018,hz-.027),
                     (nx-.012,0,hz-.043),(nx+.007,0,hz-.03)],[],[(0,2,1),(0,1,3),(1,2,3),(2,0,3)])
    mesh.update();nose=bpy.data.objects.new('nose',mesh);bpy.context.collection.objects.link(nose);finish(nose,'triangular_nose',pigment)
    limb('mouth',[(nx,0,hz-.043),(nx+.005,0,hz-.055),(nx+.015,-.022,hz-.055)],
        [.0025,.0025,.0015],'cat_shadow')
    orb('chin',(hx-head_length*.75,0,hz-.062),(.027,.032,.012),pigment)
    root_z=z+.025
    tail=limb('upright_tail',[(hip+.025,0,root_z),(hip+.13,.005,z+.14),
        (hip+.15,.008,z+tail_height*.71),(hip+.13,.01,z+tail_height),
        (hip+.08,.01,z+tail_height+.025)],
        [.028,.025,.021,.016,.006],'cat_orange')
    tail['coat_marking']='cat_tail';tail['tail_root_z']=root_z
    tail.modifiers.new('Soft tail curve','SUBSURF').levels=2

# Kitten: shorter torso/legs, relatively larger head/ears/paws. Adults stay lean.
feline('kitten',.175,.077,.085,.115,.105,.085,.12,.039,.31,juvenile=True)
feline('housecat',.245,.090,.100,.185,.112,.086,.115,.043,.39)
feline('large_cat',.285,.103,.113,.220,.124,.095,.12,.048,.44)

GROUPS=['kitten','housecat','large_cat']
BLEND_NAME='CreatureBatch4.blend';REPORT_NAME='projection-report-batch4.json'
exec(compile(Path(__file__).with_name('CreatureBatch2Pipeline.py').read_text(),
             'CreatureBatch2Pipeline.py','exec'))
