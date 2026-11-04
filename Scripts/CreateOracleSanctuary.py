"""Editable double-sided fluted sanctuary wall, entirely inside one wall cell."""
import sys,math,json,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from CreatureGeometry import *
import CreatureGeometry as g
OUT=ROOT/'Art/OracleSanctuary';OUT.mkdir(parents=True,exist_ok=True)
protected={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'Art').rglob('*.fbx') if OUT not in p.parents}
(OUT/'protected.json').write_text(json.dumps(protected,indent=2))
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False);g.GROUP='oracle_wall'
for key,c,rough,metal in [('oracle_marble',(.68,.64,.53),.36,0),('oracle_base',(.21,.25,.26),.5,0),('oracle_bronze',(.35,.22,.075),.32,.8)]:
 COLORS[key]=c;m=bpy.data.materials.new(key);m.use_nodes=True;m.diffuse_color=(*c,1);s=m.node_tree.nodes['Principled BSDF'];s.inputs['Metallic'].default_value=metal;s.inputs['Roughness'].default_value=rough;MATS[key]=m
box('masonry_core',(0,0,.60),(.98,.64,1.18),'oracle_marble',.012)
for z,w,d,h in [(.055,.98,.96,.11),(.15,.98,.88,.08),(1.08,.98,.88,.08),(1.17,.98,.96,.06)]:box('plinth_or_entablature',(0,0,z),(w,d,h),'oracle_base' if z<.1 else 'oracle_marble',.008)
for side in [-1,1]:
 y=side*.315
 for z,size in [(.195,(.35,.30,.08)),(1.01,(.35,.30,.08))]:box('capital_or_base',(0,y,z),size,'oracle_marble',.008)
 verts=[];faces=[];N=160
 for j in range(17):
  z=.235+j*.044;radius=.136*(1-.12*j/16)+.003*math.sin(math.pi*j/16)
  for i in range(N):a=math.tau*i/N;r=radius-.009*(.5+.5*math.cos(20*a));verts.append((r*math.cos(a),y+r*math.sin(a),z))
 for j in range(16):
  for i in range(N):a=j*N+i;b=j*N+(i+1)%N;faces.append((a,b,b+N,a+N))
 faces += [tuple(reversed(range(N))),tuple(16*N+i for i in range(N))]
 mm=bpy.data.meshes.new('twenty_flutes');mm.from_pydata(verts,[],faces);mm.update();o=bpy.data.objects.new('fluted_column',mm);bpy.context.collection.objects.link(o);g.finish(o,'fluted_column','oracle_marble')
 for p in mm.polygons:p.use_smooth=True
 for x in [-.38,-.19,0,.19,.38]:
  for dx,dz,w,h in [(0,0,.11,.012),(-.05,.022,.012,.05),(.018,.043,.065,.012),(.045,.025,.012,.04)]:box('meander_inlay',(x+dx,side*.445,1.09+dz),(w,.006,h),'oracle_bronze',.001)
GROUPS=['oracle_wall'];BLEND_NAME='OracleSanctuary.blend';REPORT_NAME='projection-report.json';SOURCE_TILE_NAMES={'oracle_wall':'wall'}
SOURCE_TILE_ENTRIES={'wall':['B'*16]*16};SOURCE_FIGURE_MASKS={'oracle_wall':[(x,y) for x in range(1,15) for y in range(1,15)]}
pipeline=Path(__file__).with_name('CreatureBatch2Pipeline.py').read_text()
exec(compile(pipeline,'OracleSanctuaryPipeline','exec'))
