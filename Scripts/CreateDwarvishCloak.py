"""Seventh requested garment: native dwarvish cloak / hooded cloak."""
import sys,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from CreatureGeometry import *
import CreatureGeometry as g
OUT=ROOT/'Art/ObjectInterpretations';bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for key,col,rough,metal in [('cloak_wool',(.20,.065,.023),.93,0),('cloak_lining',(.39,.20,.075),.88,0),('cloak_braid',(.62,.36,.10),.8,0),('cloak_bronze',(.43,.22,.045),.35,.85)]:
    COLORS[key]=col;m=bpy.data.materials.new(key);m.use_nodes=True;m.diffuse_color=(*col,1);s=m.node_tree.nodes['Principled BSDF'];s.inputs['Roughness'].default_value=rough;s.inputs['Metallic'].default_value=metal;MATS[key]=m
g.GROUP='dwarvish_cloak'
def cape(t,j):
    a=-.12*math.pi+t*1.24*math.pi;z=.055+j*.545;r=.31*(1-j)+.13*j+.012*math.sin(a*9)*(1-j)
    return Vector((r*math.cos(a),r*math.sin(a)*.78,z))
verts=[cape(i/72,j/24) for j in range(25) for i in range(73)];faces=[]
for j in range(24):
    for i in range(72):a=j*73+i;faces.append((a,a+1,a+74,a+73))
mesh=bpy.data.meshes.new('Draped wool');mesh.from_pydata(verts,[],faces);mesh.update();o=bpy.data.objects.new('cape',mesh);bpy.context.collection.objects.link(o);g.finish(o,'open_front_cape','cloak_wool');o.modifiers.new('Thick wool hem','SOLIDIFY').thickness=.009
for p in mesh.polygons:p.use_smooth=True
for t in [0,1]:
    pts=[cape(t,j/72)+Vector((0,-.003,0)) for j in range(73)];limb('front_braid',pts,[.006]*73,'cloak_braid')
limb('hem_braid',[cape(i/144,0) for i in range(145)],[.006]*145,'cloak_braid')
# Hood uses a curved open-front patch; no hidden head or mannequin.
verts=[];faces=[];n=64;rows=24
for j in range(rows+1):
    z=.575+j*.235/rows;r=.155*math.sqrt(max(.025,1-((z-.65)/.175)**2))
    for i in range(n+1):
        a=-.08*math.pi+i/n*1.16*math.pi
        verts.append((r*math.cos(a),.012+r*math.sin(a)*.93,z))
for j in range(rows):
    for i in range(n):a=j*(n+1)+i;faces.append((a,a+1,a+n+2,a+n+1))
# Close the small crown with a domed patch while leaving the face and base open.
top=len(verts);verts.append((0,.018,.825))
for i in range(n):faces.append((rows*(n+1)+i,rows*(n+1)+i+1,top))
mesh=bpy.data.meshes.new('Open hood');mesh.from_pydata(verts,[],faces);mesh.update();o=bpy.data.objects.new('hood',mesh);bpy.context.collection.objects.link(o);g.finish(o,'open_faced_hood','cloak_wool');o.modifiers.new('Wool thickness','SOLIDIFY').thickness=.009
for p in mesh.polygons:p.use_smooth=True
for side in [0,n]:limb('hood_face_binding',[Vector(verts[j*(n+1)+side])+Vector((0,-.003,0)) for j in range(rows+1)],[.005]*(rows+1),'cloak_braid')
box('square_bronze_clasp',(0,-.084,.571),(.055,.022,.043),'cloak_bronze',.006)
for side in [-1,1]:limb('clasp_tie',[(0,-.081,.57),(side*.11,-.055,.586)],[.005,.005],'cloak_braid')
def pigment(o,p,c,colors):
    if o['pigment']=='cloak_wool':
        f=.92+.07*math.sin(p.x*240)*math.sin(p.z*251+p.y*71)
        return tuple(v*f for v in c)
    return c
GROUPS=['dwarvish_cloak'];BLEND_NAME='DwarvishCloak.blend';REPORT_NAME='projection-report-dwarvish-cloak.json';PIGMENT_FUNCTION=pigment
SOURCE_TILE_NAMES={'dwarvish_cloak':'hooded cloak / dwarvish cloak'};SPATIAL_MASK_KEYS=GROUPS
pipeline=Path(__file__).with_name('CreatureBatch2Pipeline.py').read_text(encoding='utf-8').replace('win/share/monsters.txt','win/share/objects.txt')
exec(compile(pipeline,'DwarvishCloakPipeline','exec'))
