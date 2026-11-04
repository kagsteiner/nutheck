"""Human male/female Samurai, fixed integrated official-icon costumes."""
import sys,math,re
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from CreatureGeometry import *
import CreatureGeometry as g
import HumanPlayerFamily as human
from PrimateFamily import limb as smooth_limb
human.limb=smooth_limb
GROUPS=['samurai_male_human','samurai_female_human'];BLEND_NAME='Samurai.blend';REPORT_NAME='projection-report-samurai.json'
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
palette={'human_skin':(.76,.43,.29),'human_dark':(.008,.006,.007),'human_sclera':(.79,.79,.69),'human_blue':(.025,.55,.004),'human_green':(.025,.55,.004),'human_lip':(.30,.095,.065),'human_gold':(.008,.006,.007),'human_brow':(.012,.009,.008),'player_leather':(.3,.1,.02),'player_trim':(.3,.1,.02),'player_boot':(.3,.1,.02),'player_belt':(.3,.1,.02),'samurai_magenta':(.74,.003,.52),'samurai_red':(.84,.006,.009),'samurai_cyan':(.006,.43,.70),'samurai_hair':(.008,.006,.007)}
for key,c in palette.items():
 COLORS[key]=c;m=bpy.data.materials.new(key);m.use_nodes=True;m.diffuse_color=(*c,1);m.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.82;MATS[key]=m
for key in GROUPS:
 female='female' in key;body=human.human_player(key,female);g.GROUP=key;hz=body['head_z'];shoulder=body['shoulder_half_width'];hip=.085 if female else .102
 # Retain complete reviewed anatomy/face, replacing earlier role-specific dress.
 for o in list(bpy.data.objects):
  if o.type=='MESH' and o.get('creature')==key and (o.get('pigment','').startswith('player_') or 'braid' in o.name or '_toe' in o.name):bpy.data.objects.remove(o,do_unlink=True)
 shirt=human.garment('wrap_shirt',[(.85,.158 if female else .183,.120),(.98,.128 if female else .164,.105),(1.08,.154 if female else .200,.115),(1.16,.174 if female else .214,.130),(1.27,.175 if female else .216,.116)],'samurai_magenta')
 if female:
  # Fitted fabric follows a feminine chest/waist, with no exposed torso.
  for v in shirt.data.vertices:
   if v.co.y<0:v.co.y-=.028*math.exp(-((v.co.z-1.14)/.075)**2)*(.5+.5*math.cos(v.co.x*18))

 human.garment('wide_obi',[(.85,.163 if female else .193,.126),(.99,.139 if female else .175,.116)],'samurai_cyan')
 human.garment('trouser_hips',[(.73,.169 if female else .186,.128),(.84,.175 if female else .191,.130),(.88,.163 if female else .184,.126)],'samurai_red')
 for side in [-1,1]:
  x=side*(hip+.020);reach=.245 if female else .295
  trouser=smooth_limb('trouser_leg',[(side*hip,.005,.78),(side*(hip+.017),-.01,.46),(x,0,.13)],[.085,.067,.058] if female else [.100,.078,.068],'samurai_red')

  for v in trouser.data.vertices:
   if .10<v.co.z<.70:v.co.y*=1.4
  orb('tabi_shoe',(x,-.044,.037),(.057,.110,.036),'samurai_magenta')
  # Small shoulder panels match the icon, with bare forearms/hands retained.
  smooth_limb('shoulder_panel',[(side*.13,0,1.27),(side*shoulder,0,1.265),(side*(shoulder+.025),0,1.22)],[.075,.090,.080] if female else [.063,.078,.070],'samurai_magenta')
  smooth_limb('red_under_sleeve',[(side*shoulder,0,1.255),(side*(shoulder+.025),-.003,1.185),(side*(shoulder+.045),-.006,1.13)],[.073,.067,.062] if female else [.088,.082,.077],'samurai_red')
 # A short bound topknot is clearly visible in both official tiles.
 smooth_limb('topknot',[(0,.025,hz+.11),(0,.027,hz+.19),(.025,.025,hz+.23),(.050,.025,hz+.23)],[.037,.030,.026,.018],'samurai_hair')
 if female:
  smooth_limb('tied_ponytail',[(0,.055,hz+.17),(0,.12,hz+.12),(.025,.145,hz-.05),(.055,.145,hz-.25),(.07,.12,hz-.33)],[.031,.046,.050,.033,.008],'samurai_hair')
  body['distinct_female_samurai']=True
 for o in bpy.data.objects:
  if o.type=='MESH' and o.get('creature')==key:o['player_form']=key

def consolidate():
 for key in GROUPS:
  parts=[o for o in bpy.data.objects if o.type=='MESH' and o.get('creature')==key];body=next(o for o in parts if o.get('human_player'))
  body['fitted_eye_centers']=[float(c) for o in parts if o.get('eye_center') for c in o['eye_center']];body['fixed_icon_costume']=True
  group=body.vertex_groups.new(name='anatomy');group.add(list(range(len(body.data.vertices))),1.,'REPLACE')
  bpy.ops.object.select_all(action='DESELECT')
  for o in parts:o.select_set(True)
  bpy.context.view_layer.objects.active=body;bpy.ops.object.join();body.name=key+'_character'
def costume_pigment(o,p,c,colors):
 if 'trouser_leg' in o.name and p.z<.37:
  t=max(0,min(1,(.37-p.z)/.04));return tuple(a*(1-t)+b*t for a,b in zip(c,colors['samurai_magenta']))
 return human.human_pigment(o,p,c,colors)
PIGMENT_FUNCTION=costume_pigment;POST_PAINT=consolidate
SOURCE_TILE_NAMES={k:'samurai,'+('female' if 'female' in k else 'male') for k in GROUPS}
raw=(ROOT/'upstream/NetHack/win/share/monsters.txt').read_text();tiles={n:rows.strip().splitlines() for _,n,rows in re.findall(r'^# tile (\d+) \(([^\n]+)\)\s*\{([^}]+)\}',raw,re.M)}
SOURCE_FIGURE_MASKS={k:[(x,y) for y,row in enumerate(tiles[SOURCE_TILE_NAMES[k]]) for x,ch in enumerate(row.strip()) if ch not in {'.','A'} or (ch=='A' and (y<8 or x<9))] for k in GROUPS}
exec(compile(Path(__file__).with_name('CreatureBatch2Pipeline.py').read_text(),'SamuraiPipeline','exec'))
