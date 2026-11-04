"""Editable hafted weapon batch: forged bearded axe, flanged mace, poll/pick hammer."""
import sys,math,json,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from CreatureGeometry import *
import CreatureGeometry as g
OUT=ROOT/'Art/ObjectInterpretations';GROUPS=['axe','mace','war_hammer']
manifest=OUT/'weapon-batch3-protected.json'
if not manifest.exists():
    files=sorted(p for p in (ROOT/'Art').rglob('*.fbx') if p.stem not in GROUPS)
    manifest.write_text(json.dumps({p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in files},indent=2))
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for key,c,rough,metal in [('weapon3_iron',(.32,.37,.40),.26,1),('weapon3_edge',(.62,.68,.72),.18,1),('weapon3_brass',(.40,.24,.065),.32,.8),('weapon3_leather',(.052,.027,.018),.78,0),('weapon3_wood',(.20,.083,.025),.58,0)]:
    COLORS[key]=c;m=bpy.data.materials.new(key);m.use_nodes=True;m.diffuse_color=(*c,1);s=m.node_tree.nodes['Principled BSDF'];s.inputs['Roughness'].default_value=rough;s.inputs['Metallic'].default_value=metal;MATS[key]=m

def ring(name,z,r,depth,color='weapon3_iron',x=0):
    bpy.ops.mesh.primitive_cylinder_add(vertices=32,radius=r,depth=depth,location=(x,0,z));o=bpy.context.object;g.finish(o,name,color)
    mod=o.modifiers.new('Turned fitting bevel','BEVEL');mod.width=min(.0015,depth*.15);mod.segments=3
    return o

def solid(name,verts,faces,color,bevel=0):
    mm=bpy.data.meshes.new(name);mm.from_pydata(verts,[],faces);mm.update();o=bpy.data.objects.new(name,mm);bpy.context.collection.objects.link(o);g.finish(o,name,color)
    if bevel:
        mod=o.modifiers.new('Forged edge bevel','BEVEL');mod.width=bevel;mod.segments=3
    return o

def cut_eye(o,z):
    bpy.ops.mesh.primitive_cylinder_add(vertices=48,radius=.020,depth=.30,location=(0,0,z));cutter=bpy.context.object
    # Recalculate outward normals before the solid difference.
    bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free()
    bpy.context.view_layer.objects.active=o
    for m in list(o.modifiers):bpy.ops.object.modifier_apply(modifier=m.name)
    mod=o.modifiers.new('Real haft eye','BOOLEAN');mod.operation='DIFFERENCE';mod.object=cutter;bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cutter,do_unlink=True)
    o.data.materials.clear();o.data.materials.append(MATS[o['pigment']])
    for polygon in o.data.polygons:polygon.material_index=0
    o['haft_eye']=True

def haft(key,top):
    if key=='axe':
        limb('curved_ash_haft',[(-.025,0,.025),(-.037,0,.12),(-.025,0,.30),(-.008,0,.53),(0,0,top)],[.023,.020,.018,.017,.018],'weapon3_wood')
        ring('butt_ferrule',.028,.024,.030,'weapon3_iron',x=-.025)
        for j in range(12):ring('grip_binding',.075+j*.010,.021,.003,'weapon3_leather',x=-.035+j*.0004)
    else:
        limb('tapered_haft',[(0,0,.035),(0,0,.24),(0,0,top)],[.020,.017,.018], 'weapon3_iron' if key=='mace' else 'weapon3_wood')
        limb('leather_grip',[(0,0,.065),(0,0,.14),(0,0,.25)],[.022,.021,.020],'weapon3_leather')
        for z in [.052,.262]:ring('grip_collar',z,.024,.012,'weapon3_brass')
        for j in range(14):ring('spiral_grip_seams',.075+j*.012,.022,.002,'weapon3_leather')
        orb('butt_cap',(0,0,.022),(.024,.022,.022),'weapon3_iron')

for key in GROUPS:
    g.GROUP=key
    if key=='axe':
        haft(key,.787)
        # Convex cheeks taper to a curved, thin cutting bit; lower beard is real geometry.
        stations=[(-.052,.657,.740,.025),(-.025,.647,.750,.032),(0,.643,.756,.034),(.035,.628,.763,.030),(.075,.600,.775,.024),(.120,.572,.784,.017),(.165,.556,.784,.009),(.202,.565,.773,.0009)]
        verts=[];faces=[]
        for x,low,high,d in stations:
            # Rounded rectangular section around each X station.
            for yy,zz in [(-.65,0),(-1,.12),(-1,.88),(-.65,1),(.65,1),(1,.88),(1,.12),(.65,0)]:verts.append((x,yy*d,low+zz*(high-low)))
        for j in range(len(stations)-1):
            for i in range(8):a=j*8+i;b=j*8+(i+1)%8;faces.append((a,b,b+8,a+8))
        faces += [tuple(reversed(range(8))),tuple((len(stations)-1)*8+i for i in range(8))]
        head=solid('bearded_axe_head',verts,faces,'weapon3_iron');cut_eye(head,.71);head['crafted_head']=True
        # The visible wooden end and wedge cap close the haft eye without hiding it in the editable scene.
        box('haft_end_wedge',(0,0,.788),(.025,.008,.009),'weapon3_iron',.001)
        for side in [-1,1]:
            limb('cheek_border',[(.045,side*.030,.724),(.083,side*.023,.733),(.125,side*.016,.740)],[.0011]*3,'weapon3_brass')
    elif key=='mace':
        haft(key,.70)
        ring('head_core',.617,.028,.190)
        for z in [.515,.716]:ring('head_collar',z,.037,.016,'weapon3_brass')
        # Eight individually editable, solid, bevelled flanges form the crown.
        outline=[(.025,.530),(.047,.536),(.072,.560),(.088,.603),(.085,.646),(.064,.687),(.039,.706),(.025,.702)]
        for j in range(8):
            verts=[(x,y,z) for y in [-.004,.004] for x,z in outline];n=len(outline)
            faces=[tuple(reversed(range(n))),tuple(n+i for i in range(n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
            o=solid('forged_flange_%d'%j,verts,faces,'weapon3_iron',.0016);o.rotation_euler.z=math.tau*j/8
            bpy.context.view_layer.objects.active=o;o.select_set(True);bpy.ops.object.transform_apply(location=False,rotation=True,scale=True);o.select_set(False);o['crafted_head']=True
        orb('crown_finial',(0,0,.736),(.026,.026,.024),'weapon3_iron')
        for side in [-1,1]:
            for z in [.34,.43]:orb('haft_pin',(0,side*.018,z),(.003,.002,.003),'weapon3_brass')
    else:
        haft(key,.735)
        head=box('forged_hammer_head',(.025,0,.687),(.205,.066,.083),'weapon3_iron',.007);cut_eye(head,.687);head['crafted_head']=True
        # A broad square poll and a tapered descending pick give an asymmetric profile.
        box('hardened_striking_face',(.141,0,.687),(.030,.078,.090),'weapon3_edge',.004)
        box('poll_neck',(.112,0,.687),(.030,.055,.063),'weapon3_iron',.004)
        limb('rear_pick',[(-.074,0,.687),(-.128,0,.679),(-.181,0,.652),(-.216,0,.617)],[.028,.024,.014,.0009],'weapon3_iron')
        ring('socket_ferrule',.623,.025,.026,'weapon3_brass')
        box('top_wedge',(0,0,.736),(.025,.009,.007),'weapon3_iron',.001)
        for side in [-1,1]:
            box('cheek_reinforcement',(0,side*.020,.54),(.022,.006,.170),'weapon3_iron',.002)
            for z in [.48,.59]:orb('langet_rivet',(0,side*.024,z),(.0035,.002,.0035),'weapon3_brass')

def pigment(o,p,c,colors):
    if o.get('creature')=='axe' and o.get('crafted_head') and p.x>.15:return colors['weapon3_edge']
    if o['pigment']=='weapon3_wood':
        f=.82+.15*math.sin(p.x*670+p.y*720+math.sin(p.z*17));return tuple(v*f for v in c)
    return c
BLEND_NAME='WeaponBatch3.blend';REPORT_NAME='projection-report-weapon-batch3.json';PIGMENT_FUNCTION=pigment
SOURCE_TILE_NAMES={k:k.replace('_',' ') for k in GROUPS};SPATIAL_MASK_KEYS=GROUPS
pipeline=Path(__file__).with_name('CreatureBatch2Pipeline.py').read_text().replace('win/share/monsters.txt','win/share/objects.txt')
pipeline=pipeline.replace('target_width=max(x for x,y in target)-min(x for x,y in target)+1','target_width=13').replace('target_height=max(y for x,y in target)-min(y for x,y in target)+1','target_height=13')
pipeline=pipeline.replace('max((high-low).length*1.1,1.1)','max((high-low).length*1.1,.1)')
strip_lights="""
for at,power in [((-1,-3,1.7),650),((2,2,1.5),450)]:
    data=bpy.data.lights.new('Forged metal reflection strip','AREA');data.energy=power;data.shape='RECTANGLE';data.size=2.;data.size_y=3.
    o=bpy.data.objects.new('Forged metal reflection strip',data);bpy.context.collection.objects.link(o);o.location=at;o.rotation_euler=(Vector((0,0,.5))-o.location).to_track_quat('-Z','Y').to_euler()
"""
pipeline=pipeline.replace('scene.render.film_transparent=True;',strip_lights+'\nscene.render.film_transparent=True;')
exec(compile(pipeline,'WeaponBatch3Pipeline','exec'))
