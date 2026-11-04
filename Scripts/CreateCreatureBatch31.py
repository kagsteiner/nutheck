import sys,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from CreatureGeometry import *
import CreatureGeometry as g
from CreatureBatch31Config import *
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for key,c in {'blue_gel':(.008,.28,.88),'spotted_gel':(.005,.42,.80),'ochre_gel':(.90,.13,.003)}.items():
 COLORS[key]=c;m=bpy.data.materials.new(key);m.use_nodes=True;m.diffuse_color=(*c,1);m.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.32;MATS[key]=m
for key,width,depth,height,peak in [('blue_jelly',.34,.27,.27,.75),('spotted_jelly',.29,.29,.31,.87),('ochre_jelly',.38,.26,.29,.94)]:
 g.GROUP=key;c={'blue_jelly':'blue_gel','spotted_jelly':'spotted_gel','ochre_jelly':'ochre_gel'}[key]
 parts=[orb('gel_mass',(0,0,height),(width,depth,height),c)]
 # Rounded vertical folds are continuous gel, not heads, limbs or horns.
 for i,y in enumerate([-.17,0,.17]):
  top=peak if i==1 else peak*(.78 if i==0 else .85)
  x=-.10 if key!='spotted_jelly' else (-.08+i*.025)
  parts.append(orb('upright_fold',(x,y,top*.64),(.080 if i==1 else .075,.075,top*.36),c))
 parts.append(orb('flowing_base',(.12,.07,.10),(width*.78,depth*.90,.10),c))
 body=sculpt_union(parts,'continuous_jelly',c,.006);body['anatomy']=True;body['gel_body']=True;body['head_z']=height;body['fold_count']=3
 low=min((body.matrix_world@v.co).z for v in body.data.vertices);body.location.z-=low

def pigment(o,p,c,colors):
 key=o['creature'];wave=math.sin(p.x*18+p.z*12)*math.cos(p.y*17-p.z*8)
 if key=='ochre_jelly':
  red=.45*(.5+.5*math.sin(p.y*9+p.x*6));c=tuple(a*(1-red)+b*red for a,b in zip(c,(.90,.006,.002)))
 else:
  cyan=.45+.23*wave;c=tuple(a*(1-cyan)+b*cyan for a,b in zip(c,(.005,.65,.90)))
  if key=='spotted_jelly':
   t=max(0,min(1,(math.sin(p.x*28+p.y*9)*math.cos(p.z*27-p.y*18)-.34)*4))
   c=tuple(a*(1-t)+b*t for a,b in zip(c,(.98,.22,.004)))
 # Sparse non-paired lime gel inclusions echo the tiles without inventing eyes.
 t=max(0,math.sin(p.x*23+p.z*17)*math.cos(p.y*29+p.z*8))**18*.75
 c=tuple(a*(1-t)+b*t for a,b in zip(c,(.24,.90,.003)))
 pale=max(0,min(1,(p.z-.36)/.35))*.27
 return tuple(a*(1-pale)+b*pale for a,b in zip(c,(.64,.82,.82) if key!='ochre_jelly' else (.98,.52,.24)))
PIGMENT_FUNCTION=pigment
exec(compile(Path(__file__).with_name('CreatureBatch2Pipeline.py').read_text(),'Batch31Pipeline','exec'))
