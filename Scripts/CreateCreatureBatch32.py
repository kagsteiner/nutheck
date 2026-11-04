import sys,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from CreatureGeometry import *
import CreatureGeometry as g
from PrimateFamily import limb
from CreatureBatch32Config import *
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for key,c in {'ooze_slate':(.17,.31,.41),'pudding_brown':(.29,.077,.004),'pudding_black':(.012,.015,.020)}.items():
 COLORS[key]=c;m=bpy.data.materials.new(key);m.use_nodes=True;m.diffuse_color=(*c,1);m.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.32;MATS[key]=m
for key in GROUPS:
 g.GROUP=key
 if key=='gray_ooze':
  c='ooze_slate';parts=[orb('flowing_sheet',(0,0,.12),(.39,.26,.12),c),orb('low_crest',(-.18,.04,.20),(.18,.16,.17),c),orb('leading_lobe',(-.32,-.09,.09),(.17,.16,.09),c),orb('trailing_lobe',(.31,.04,.075),(.19,.14,.075),c)]
  body=sculpt_union(parts,'ooze_body',c,.006)
 elif key=='brown_pudding':
  c='pudding_brown';parts=[orb('pudding_mass',(-.04,0,.24),(.30,.29,.24),c),orb('lopsided_shoulder',(.12,.08,.28),(.20,.22,.24),c),orb('flowing_foot',(.16,.04,.10),(.28,.23,.10),c),limb('curled_fold',[(.11,.09,.34),(.23,.10,.48),(.31,.11,.58),(.35,.12,.56)],[.10,.065,.037,.014],c)]
  body=sculpt_union(parts,'pudding_body',c,.006)
 else:
  c='pudding_black';body=limb('continuous_black_body',[(.48,.03,.035),(.34,.02,.06),(.16,0,.14),(-.02,0,.29),(-.17,.01,.50),(-.20,.02,.74),(-.16,.03,.94),(-.10,.035,1.03)],[.014,.047,.095,.13,.14,.12,.060,.012],c)
  # This is one full gel volume, not an animal with a reconstructed head/tail.
 body['anatomy']=True;body['gel_body']=True;body['head_z']=.18 if key=='gray_ooze' else .30 if key=='brown_pudding' else .70
 low=min((body.matrix_world@v.co).z for v in body.data.vertices);body.location.z-=low
 if key in ['brown_pudding','black_pudding']:
  from PuddingEyes import add_eyes
  add_eyes(key,body)

def pigment(o,p,c,colors):
 key=o['creature']
 if o.get('tile_eye'):
  if key=='black_pudding':return (.98,.008+.23*max(0,min(1,(p.z-.76)/.04)),.002)
  return c
 wave=math.sin(p.x*20+p.z*14)*math.cos(p.y*23-p.x*9)
 if key=='gray_ooze':
  t=max(0,wave)*.65;c=tuple(a*(1-t)+b*t for a,b in zip(c,(.005,.52,.78)))
  amber=max(0,min(1,(p.x-.27)/.17))*.85
  return tuple(a*(1-amber)+b*amber for a,b in zip(c,(.65,.17,.004)))
 if key=='brown_pudding':
  t=max(0,wave)**7*.65;c=tuple(a*(1-t)+b*t for a,b in zip(c,(.82,.23,.014)))
  return c
 return c
PIGMENT_FUNCTION=pigment
exec(compile(Path(__file__).with_name('CreatureBatch2Pipeline.py').read_text(),'Batch32Pipeline','exec'))
