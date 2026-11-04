import sys,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from CreatureGeometry import *
import CreatureGeometry as g
from CreatureBatch30Config import *
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for key,c in {'acid_gel':(.85,.009,.012),'quiver_gel':(.015,.36,.72),'cube_gel':(.88,.16,.012)}.items():
 COLORS[key]=c;m=bpy.data.materials.new(key);m.use_nodes=True;m.diffuse_color=(*c,1);m.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.32;MATS[key]=m
for key in GROUPS:
 g.GROUP=key
 if key=='gelatinous_cube':
  body=box('soft_cube',(0,0,.40),(.84,.79,.80),'cube_gel',.105)
  bpy.context.view_layer.objects.active=body
  for mod in list(body.modifiers):bpy.ops.object.modifier_apply(modifier=mod.name)
  body.data.remesh_voxel_size=.012;bpy.ops.object.voxel_remesh()
  for f in body.data.polygons:f.use_smooth=True
  # Round the geometric planes subtly while retaining the unmistakable cube.
  for v in body.data.vertices:v.co.z+=.012*math.sin(v.co.x*12)*math.cos(v.co.y*10)
 else:
  acid=key=='acid_blob';c='acid_gel' if acid else 'quiver_gel'
  parts=[orb('core',(0,0,.19 if acid else .28),(.25 if acid else .36,.22 if acid else .31,.19 if acid else .28),c)]
  for i in range(7 if acid else 5):
   a=math.tau*i/(7 if acid else 5);r=.19 if acid else .26
   parts.append(orb('rounded_lobe',(r*math.cos(a),r*.82*math.sin(a),.10 if acid else .14),(.11 if acid else .15,.10 if acid else .13,.10 if acid else .14),c))
  body=sculpt_union(parts,'continuous_gel',c,.0055)
 body['anatomy']=True;body['head_z']=.23 if key=='acid_blob' else .36 if key=='quivering_blob' else .5;body['gel_body']=True
 # Floor origin and no detached drops, eyes, head or limb objects.
 low=min((body.matrix_world@v.co).z for v in body.data.vertices);body.location.z-=low

def pigment(o,p,c,colors):
 if not o.get('gel_body'):return c
 key=o['creature'];wave=math.sin(p.x*22+p.z*13)*math.cos(p.y*19-p.z*11)
 if key=='acid_blob':
  mag=max(0,wave)*.8;c=tuple(a*(1-mag)+b*mag for a,b in zip(c,(.85,.005,.70)))
  w=max(0,1-((p.x+.16)/.12)**2-((p.y+.08)/.10)**2-((p.z-.22)/.15)**2)*.85
  return tuple(a*(1-w)+b*w for a,b in zip(c,(.92,.84,.74)))
 if key=='quivering_blob':
  w=(.5+.5*wave)*.72;return tuple(a*(1-w)+b*w for a,b in zip(c,(.76,.85,.82)))
 w=max(0,min(1,(p.z-.39)/.22));c=tuple(a*(1-w)+b*w for a,b in zip(c,(.98,.48,.28)))
 # Green source inclusions are painted into the gel, never inventory contents.
 green=max(0,math.sin(p.x*22+p.y*17)*math.cos(p.z*18))**8*(1-w)*.9
 return tuple(a*(1-green)+b*green for a,b in zip(c,(.17,.85,.004)))
PIGMENT_FUNCTION=pigment
exec(compile(Path(__file__).with_name('CreatureBatch2Pipeline.py').read_text(),'Batch30Pipeline','exec'))
