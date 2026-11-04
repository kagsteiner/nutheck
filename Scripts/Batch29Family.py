import bpy,math
from mathutils import Vector
import CreatureGeometry as g
from CreatureGeometry import orb,sculpt_union
from PrimateFamily import limb
import HairyBipeds as hairy

def build(key):
 if key!='owlbear':
  hairy.build(key)
  for o in bpy.data.objects:
   if o.type=='MESH' and o.get('creature')==key:
    original=o['pigment'];o['pigment']=('yeti_white' if original in ['primate_coat','primate_skin'] else 'primate_dark' if original=='primate_blue' else original) if key=='yeti' else ('sasquatch_brown' if original in ['primate_coat','primate_skin'] else 'sasquatch_eye' if original=='primate_blue' else original)
    if 'mouth' in o.name and key=='yeti':o['pigment']='primate_red'
    o.data.materials.clear();o.data.materials.append(g.MATS[o['pigment']])
  if key=='yeti':
   from YetiClub import add_club
   add_club()
  return
 g.GROUP=key;coat='owl_coat';parts=[orb('bear_haunch',(0,0,.40),(.25,.22,.31),coat),orb('bear_chest',(-.02,0,.73),(.28,.31,.38),coat),orb('owl_skull',(-.06,0,1.10),(.22,.26,.25),coat)]
 for side in [-1,1]:
  parts += [limb('bear_arm',[(-.02,side*.25,.86),(-.10,side*.37,.62),(-.23,side*.35,.48)],[.12,.10,.075],coat),orb('paw',(-.23,side*.35,.46),(.11,.10,.09),coat),limb('bear_leg',[(.02,side*.15,.40),(-.03,side*.17,.22),(-.04,side*.18,.09)],[.14,.11,.08],coat),orb('foot',(-.12,side*.18,.07),(.17,.12,.07),coat),orb('ear_tuft',(-.03,side*.20,1.30),(.08,.065,.15),coat)]
 body=sculpt_union(parts,'bear_owl_anatomy',coat,.007);body['anatomy']=True;body['fur_surface']=True;body['head_z']=1.10;body['shoulder_width']=.62
 for side in [-1,1]:
  orb('facial_disc',(-.235,side*.115,1.125),(.045,.122,.142),'owl_disc')
  orb('eye',(-.278,side*.115,1.135),(.018,.043,.052),'owl_eye')
  orb('pupil',(-.294,side*.115,1.135),(.009,.020,.038),'primate_dark')
  for j in range(4):
   limb('hand_claw',[(-.29,side*.35+(j-1.5)*.042,.44),(-.36,side*.35+(j-1.5)*.042,.40),(-.36,side*.35+(j-1.5)*.042,.37)],[.018,.012,.003],'owl_claw')
   limb('foot_claw',[(-.23,side*.18+(j-1.5)*.046,.07),(-.31,side*.18+(j-1.5)*.046,.045)],[.017,.003],'owl_claw')
 limb('hooked_beak',[(-.25,0,1.075),(-.33,0,1.035),(-.32,0,.97)],[.070,.043,.003],'owl_beak')
 orb('short_tail',(.24,0,.39),(.14,.075,.09),coat)

def pigment(o,p,c,colors):
 if o.get("held_club"):
  grain=.82+.13*math.sin(p.x*92+p.y*77)+.035*math.sin(p.z*157)
  return tuple(v*grain for v in c)
 return c
