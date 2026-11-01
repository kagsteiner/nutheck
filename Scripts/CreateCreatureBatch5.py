"""Wolf family: independent adult/cub anatomy, painted tile accents and coat UVs."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from CreatureGeometry import *
import CreatureGeometry as geometry
from CreatureFur import apply_fur
from WinterWolfEyes import winter_wolf_eyes

bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for key,color in {
    'wolf_blue':(.19,.31,.40),'wolf_light':(.39,.50,.54),
    'winter_white':(.83,.88,.83),'winter_inner':(.39,.34,.32),
    'wolf_red':(.70,.008,.016),'wolf_inner':(.23,.30,.32),
}.items():
    COLORS[key]=color
    mat=bpy.data.materials.new(key);mat.use_nodes=True;mat.diffuse_color=(*color,1)
    mat.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.82
    MATS[key]=mat

def wolf(key,length,width,depth,leg,head,muzzle,ear_height,paw,juvenile=False):
    geometry.GROUP=key
    winter=key!='wolf';coat='winter_white' if winter else 'wolf_blue'
    light=coat if winter else 'wolf_light'
    shoulder=-length*.60;hip=length*.66;z=leg+depth;hx=shoulder-.09;hz=z+depth*.87
    parts=[orb('ribs',(-.025,0,z),(length,width,depth),coat),
        orb('haunch',(hip,0,z-.012),(length*.43,width*.90,depth*.95),coat),
        orb('shoulder',(shoulder,0,z+.02),(.10,width*1.05,depth*1.08),coat),
        limb('neck',[(shoulder,0,z),(hx+.025,0,hz-.035)],[width*.90,head*.78],coat),
        orb('skull',(hx,0,hz),(head,head*.77,head*.90),coat)]
    for back,x in [(False,shoulder),(True,hip)]:
        for side in [-1,1]:
            y=side*width*.65
            parts.append(limb('digitigrade_leg',[(x,y,z),
                (x+(.075 if back else -.006),y,leg*.57),
                (x+(.022 if back else -.008),y,.05)],[width*.39,width*.24,width*.18],coat))
            parts.append(orb('paw',(x-.015,y,.029),(paw,paw*.69,.029),coat))
    body=sculpt_union(parts,'continuous_anatomy',coat,.007)
    body['age_variant']='juvenile' if juvenile else 'adult';body['head_to_torso_length']=head/length
    
    if not winter:body['coat_marking']='wolf_back'
    body['body_center_z']=z;body['body_depth']=depth
    orb('long_muzzle',(hx-head*.66,0,hz-.035),(muzzle,head*.49,head*.39),light)
    orb('red_nose',(hx-head*.66-muzzle*.85,0,hz-.018),(.026,.031,.023),'wolf_red')
    for side in [-1,1]:
        ear('ear',(hx+.025,side*head*.48,hz+.04),(hx+.045,side*head*.62,hz+ear_height),head*.40,.036,coat)
        ear('ear_lining',(hx+.006,side*head*.48,hz+.065),(hx+.027,side*head*.60,hz+ear_height-.025),head*.22,.012,'winter_inner' if winter else 'wolf_inner')
        if not winter:
            orb('eye',(hx-head*.63,side*head*.69,hz+.024),(.020,.012,.023),'glint')
            orb('eye_glint',(hx-head*.69,side*head*.76,hz+.034),(.005,.003,.005),'glint')
        limb('mouth',[(hx-head*.66-muzzle*.65,side*head*.36,hz-.067),(hx-.025,side*head*.57,hz-.070)],[.0035,.0025],'black')
    if winter:
        bpy.context.view_layer.update()
        winter_wolf_eyes(key,hx,hz,head,body)
    tail=limb('lifted_tail',[(hip,0,z+.025),(hip+.13,0,z+.045),
        (hip+.20,.012,z+.17),(hip+.20,.015,z+.32),(hip+.15,.015,z+.37)],
        [.043,.047,.035,.021,.006],coat)
    tail.modifiers.new('Soft tail curve','SUBSURF').levels=2
    for obj in bpy.context.scene.objects:
        if obj.type=='MESH' and obj.get('creature')==key and obj.get('pigment') in {coat,light}:
            obj['fur_surface']=True;obj['fur_leg_height']=leg
    if winter:
        # Named future effect socket; it is deliberately excluded from static FBX.
        hook=bpy.data.objects.new(key+'_cold_breath_socket',None);bpy.context.collection.objects.link(hook)
        hook.location=(hx-head*.66-muzzle,0,hz-.02);hook['creature']=key
        hook['future_effect']='AD_COLD breath; no effect or animation implemented'

wolf('wolf',.29,.115,.145,.29,.119,.119,.20,.052)
wolf('winter_wolf_cub',.205,.092,.112,.19,.112,.086,.185,.046,True)
wolf('winter_wolf',.34,.137,.172,.34,.137,.138,.22,.060)
GROUPS=['wolf','winter_wolf_cub','winter_wolf']
BLEND_NAME='CreatureBatch5.blend';REPORT_NAME='projection-report-batch5.json'
POST_PAINT=lambda:apply_fur([o for o in bpy.context.scene.objects if o.type=='MESH'])
exec(compile(Path(__file__).with_name('CreatureBatch2Pipeline.py').read_text(),'CreatureBatch2Pipeline.py','exec'))
