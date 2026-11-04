"""Editable Sokoban masonry, paving, boulder, known trap wells and recessed lamp."""
import sys,math,json,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from CreatureGeometry import *
import CreatureGeometry as g
OUT=ROOT/'Art/Sokoban';OUT.mkdir(parents=True,exist_ok=True)
manifest=OUT/'protected.json'
if not manifest.exists():manifest.write_text(json.dumps({p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'Art').rglob('*.fbx') if OUT not in p.parents},indent=2))
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for key,c,rough,metal in [('soko_sandstone',(.49,.37,.235),.86,0),('soko_floor',(.34,.285,.205),.89,0),('soko_basalt',(.12,.14,.15),.83,0),('soko_bronze',(.37,.23,.085),.32,.82),('soko_rock',(.29,.31,.33),.94,0),('soko_pit_earth',(.18,.135,.085),.95,0),('soko_dark',(.006,.008,.010),1,0),('soko_lamp',(.9,.49,.14),.4,0)]:
 COLORS[key]=c;m=bpy.data.materials.new(key);m.use_nodes=True;m.diffuse_color=(*c,1);s=m.node_tree.nodes['Principled BSDF'];s.inputs['Roughness'].default_value=rough;s.inputs['Metallic'].default_value=metal;MATS[key]=m
g.GROUP='soko_wall'
box('recessed_mortar_core',(0,0,.61),(.93,.93,1.16),'soko_basalt',.006)
box('dark_foundation',(0,0,.06),(.98,.98,.12),'soko_basalt',.008)
for row in range(3):
 for x in [-.24,.24]:
  for y in [-.24,.24]:box('sandstone_ashlar',(x,y,.285+row*.30),(.474,.474,.292),'soko_sandstone',.009)
box('massive_capstone',(0,0,1.135),(.98,.98,.13),'soko_sandstone',.008)
for side in [-1,1]:
 for x in [-.45,.45]:box('bronze_joint_tie',(x,side*.486,.16),(.045,.012,.07),'soko_bronze',.002)
g.GROUP='soko_floor'
slab=box('single_square_paving',(0,0,0),(.99,.99,.16),'soko_floor',.006);slab['one_native_square']=True
g.GROUP='soko_boulder'
bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=4,radius=1);rock=bpy.context.object
for v in rock.data.vertices:
 p=v.co.copy();r=1+.055*math.sin(p.x*7+p.z*4)*math.cos(p.y*8)+.026*math.sin(p.z*17+p.x*9)
 v.co=Vector((p.x*.36*r,p.y*.34*r,max(-.31,p.z*.36*r)))
for f in rock.data.polygons:f.use_smooth=True
g.finish(rock,'weathered_heavy_stone','soko_rock');rock['boulder']=True
low=Vector(tuple(min(v.co[i] for v in rock.data.vertices) for i in range(3)));high=Vector(tuple(max(v.co[i] for v in rock.data.vertices) for i in range(3)))
for v in rock.data.vertices:v.co-=Vector(((low.x+high.x)*.5,(low.y+high.y)*.5,low.z))
def well(key,hole):
 g.GROUP=key
 # Four closed paving/rim slabs leave a genuine opening instead of a black decal.
 for side in [-1,1]:
  box('square_rim',(0,side*.4275,0),(.99,.135,.16),'soko_floor',.005)
  box('square_rim',(side*.4275,0,0),(.135,.72,.16),'soko_floor',.005)
 # Closed tapered wall solids run down to just above the common foundation.
 for side in [-1,1]:
  box('inner_lining',(0,side*.354,-.025),(.72,.018,.19),'soko_basalt' if hole else 'soko_pit_earth',.003)
  box('inner_lining',(side*.354,0,-.025),(.018,.70,.19),'soko_basalt' if hole else 'soko_pit_earth',.003)
 box('deep_shadow' if hole else 'visible_pit_bottom',(0,0,-.122),(.708,.708,.008),'soko_dark' if hole else 'soko_pit_earth',.002)
 if not hole:
  for x,y,s in [(-.22,.15,.055),(.16,.20,.04),(.20,-.18,.05),(-.16,-.19,.025)]:orb('bottom_stone',(x,y,-.105),(s,s*.65,.012),'soko_basalt')
well('soko_pit',False);well('soko_hole',True)
g.GROUP='soko_frame'
for side in [-1,1]:
 box('stone_jamb',(side*.445,.43,.62),(.09,.13,1.16),'soko_sandstone',.008)
 box('basalt_jamb_foot',(side*.445,.43,.12),(.10,.14,.16),'soko_basalt',.004)
box('carved_lintel',(0,.43,1.14),(.98,.14,.12),'soko_sandstone',.008)
for x in [-.38,0,.38]:box('lintel_bronze_joint',(x,.352,1.14),(.016,.01,.075),'soko_bronze',.002)
g.GROUP='soko_trim'
for side in [-1,1]:
 for z in [1.065,1.105,1.145]:box('geometric_bronze_cap_band',(0,side*.487,z),(.72,.008,.009),'soko_bronze',.001)
g.GROUP='soko_lamp'
box('recessed_bronze_housing',(0,0,0),(.15,.030,.23),'soko_bronze',.008)
box('amber_window',(0,-.017,0),(.105,.010,.17),'soko_lamp',.004)
for x in [-.035,.035]:box('window_mullion',(x,-.025,0),(.007,.007,.17),'soko_bronze',.001)
def pigment(o,p,c,colors):
 if o['pigment'] in ['soko_floor','soko_sandstone','soko_rock','soko_pit_earth']:
  grain=.91+.055*math.sin(31*p.x+13*p.z)*math.cos(27*p.y-9*p.z)+.025*math.sin(63*p.y+17*p.x)
  return tuple(v*grain for v in c)
 return c
GROUPS=['soko_wall','soko_floor','soko_boulder','soko_pit','soko_hole','soko_frame','soko_trim','soko_lamp']
BLEND_NAME='Sokoban.blend';REPORT_NAME='projection-report.json';PIGMENT_FUNCTION=pigment
SOURCE_TILE_NAMES={k:k for k in GROUPS};SOURCE_TILE_ENTRIES={k:['B'*16]*16 for k in GROUPS};SOURCE_FIGURE_MASKS={k:[(x,y) for x in range(1,15) for y in range(1,15)] for k in GROUPS}
pipeline=Path(__file__).with_name('CreatureBatch2Pipeline.py').read_text(encoding='utf-8').replace('max((high-low).length*1.1,1.1)','max((high-low).length*1.1,.35)')
exec(compile(pipeline,'SokobanPipeline','exec'))
