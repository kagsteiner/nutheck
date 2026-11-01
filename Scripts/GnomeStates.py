"""Saved gnome ancestry, native-tile caster/undead modules and fitted linen."""
import bpy,math
import CreatureGeometry as g
from KoboldStates import wrap_ribbon

def append_gnome(key):
    with bpy.data.libraries.load(str(g.OUT/'CreatureBatch2.blend'),link=False) as (src,dst):dst.collections=['gnome']
    col=dst.collections[0];col.name=key;bpy.context.scene.collection.children.link(col);col.hide_viewport=False
    omitted=['red_cap_tip','detachable_axe','belt']
    if key=='gnome_mummy':omitted+=['green_tunic','rank_ready_mantle','buckle']
    if key.endswith('_female'):omitted+=['beard_lock','beard_chin']
    for obj in list(col.objects):
        suffix=obj.name[len('gnome_'):]
        if any(suffix.startswith(n) for n in omitted):bpy.data.objects.remove(obj,do_unlink=True);continue
        obj.name=key+'_'+suffix;obj['creature']=key;obj['source_family_object']='gnome_'+suffix
        obj.hide_render=False;obj.hide_viewport=False
        if 'preserve_paint' in obj:del obj['preserve_paint']
        for attr in list(obj.data.color_attributes):obj.data.color_attributes.remove(attr)
        if suffix.startswith('eye') and not suffix.startswith('eye_glint'):
            obj['eye_side']=1 if obj.location.x>0 else -1
        if suffix.startswith('buckle'):obj.location.y=-.166
        if key.endswith('_female') and suffix.startswith('brow'):obj['female_brow']=True
        if any(n in suffix for n in ['tunic','mantle','cap','boot']):obj['costume_module']=True
    bpy.context.view_layer.update()
    return col,bpy.data.objects[key+'_body']

def fitted_belt(key):
    g.GROUP=key;verts=[];faces=[];n=64
    for rx,ry,z in [(.232,.157,.367),(.226,.151,.367),(.232,.157,.393),(.226,.151,.393)]:
        for i in range(n):
            a=math.tau*i/n;verts.append((rx*math.cos(a),ry*math.sin(a),z))
    for i in range(n):
        j=(i+1)%n
        faces.extend([(i,j,2*n+j,2*n+i),(n+j,n+i,3*n+i,3*n+j),(2*n+i,2*n+j,3*n+j,3*n+i),(j,i,n+i,n+j)])
    mesh=bpy.data.meshes.new('Fitted belt');mesh.from_pydata(verts,[],faces);mesh.update()
    obj=bpy.data.objects.new('Fitted belt',mesh);bpy.context.scene.collection.objects.link(obj);g.finish(obj,'fitted_costume_belt','leather');obj['costume_module']=True

def gnome_linen(body,key):
    wrap_ribbon(body,key,'torso_linen',(0,0,.305),(0,0,.574),6,.044,'mummy_linen')
    # A low neck wrap stays below the retained beard, leaving eyes/nose clear.
    wrap_ribbon(body,key,'neck_linen',(0,0,.620),(0,0,.648),1.2,.022,'mummy_linen')
    for side in [-1,1]:
        wrap_ribbon(body,key,'upper_arm_linen',(side*.152,-.002,.536),(side*.207,-.009,.454),2.5,.028,'mummy_linen')
        wrap_ribbon(body,key,'forearm_linen',(side*.22,-.020,.414),(side*.22,-.064,.365),2,.027,'mummy_linen')
        wrap_ribbon(body,key,'upper_leg_linen',(side*.083,-.003,.320),(side*.097,-.015,.225),3,.028,'mummy_linen')
        wrap_ribbon(body,key,'lower_leg_linen',(side*.100,-.020,.185),(side*.100,-.024,.123),2,.026,'mummy_linen')

def gnome_state_pigment(obj,p,color,colors):
    key=obj.get('creature');pigment=obj['pigment'];name=obj.name
    female=key.endswith('_female');key=key.removesuffix('_female')
    if female and obj.get('female_brow'):pigment='peach';color=colors['peach']
    if key in ['gnome_mummy','gnome_zombie'] and obj.get('eye_side'):return colors['undead_red']
    if key=='gnomish_wizard':
        if pigment=='lime':return colors['wizard_green']
        return color
    if key=='gnome_mummy':
        if pigment=='peach':return colors['gnome_dry_skin']
        if 'boot' in name:return colors['mummy_linen']
        if pigment=='mummy_linen':
            f=.95+.03*math.sin(p.z*125+p.x*29)+.02*math.sin(p.y*97)
            return tuple(v*f for v in colors['mummy_linen'])
        return color
    if key=='gnome_zombie':
        if pigment=='peach':
            light=.25+.45*math.exp(-((p.x+.05)/.09)**2-((p.z-.77)/.12)**2)
            return tuple(a*(1-light)+b*light for a,b in zip(colors['gnome_rot_green'],colors['gnome_rot_light']))
        if pigment=='beard':return colors['gnome_ash_beard']
        if pigment=='lime':return colors['zombie_cloth']
    return color
