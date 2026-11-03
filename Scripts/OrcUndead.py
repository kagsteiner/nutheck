"""Saved upright orc ancestry with source-derived mummy/zombie states."""
import bpy,math
import CreatureGeometry as g
from CreatureGeometry import orb
from KoboldStates import wrap_ribbon

def append_orc_undead(key):
    source='mordor_orc'
    with bpy.data.libraries.load(str(g.OUT/'CreatureBatch18.blend'),link=False) as (src,dst):dst.collections=[source]
    col=dst.collections[0];col.name=key;bpy.context.scene.collection.children.link(col);col.hide_viewport=False
    for obj in list(col.objects):
        suffix=obj.name[len(source)+1:]
        omit=suffix.startswith('held_') or (key=='orc_mummy' and any(suffix.startswith(n) for n in ['tunic','belt','trouser','fitted_sleeve']))
        if omit:bpy.data.objects.remove(obj,do_unlink=True);continue
        obj.name=key+'_'+suffix;obj['creature']=key;obj['source_family_object']=source+'_'+suffix
        obj.hide_render=False;obj.hide_viewport=False
        if 'preserve_paint' in obj:del obj['preserve_paint']
        for a in list(obj.data.color_attributes):obj.data.color_attributes.remove(a)
    for obj in list(col.objects):col.objects.unlink(obj);bpy.context.scene.collection.objects.link(obj)
    bpy.data.collections.remove(col);bpy.context.view_layer.update()
    return bpy.data.objects[key+'_body']

def orc_linen(body,key):
    wrap_ribbon(body,key,'torso_linen',(0,0,.39),(0,0,.738),9,.043,'orc_linen')
    wrap_ribbon(body,key,'forehead_linen',(0,-.008,1.038),(0,-.008,1.048),1,.020,'orc_linen')
    wrap_ribbon(body,key,'jaw_linen',(0,-.035,.896),(0,-.035,.919),1.4,.026,'orc_linen')
    for side in [-1,1]:
        wrap_ribbon(body,key,'upper_arm_linen',(side*.171,0,.782),(side*.213,-.010,.701),3,.029,'orc_linen')
        wrap_ribbon(body,key,'forearm_linen',(side*.225,-.022,.651),(side*.232,-.063,.584),2.5,.027,'orc_linen')
        wrap_ribbon(body,key,'upper_leg_linen',(side*.078,0,.430),(side*.092,0,.300),4,.031,'orc_linen')
        wrap_ribbon(body,key,'lower_leg_linen',(side*.098,-.002,.240),(side*.105,-.005,.102),4,.030,'orc_linen')
    # The ambiguous diagonal orange pixels become an overlaid cloth accent,
    # not an invented held weapon or gore. Lift clears the underlying linen.
    wrap_ribbon(body,key,'orange_linen_accent',(0,0,.394),(0,0,.612),.75,.024,'undead_orange',.006)

def zombie_pupils():
    g.GROUP='orc_zombie'
    for side in [-1,1]:
        o=orb('small_pupil',(side*.041,-.111,1.013),(.004,.003,.005),'black');o['pupil_module']=True

def orc_undead_pigment(obj,p,color,colors):
    key=obj['creature'];pigment=obj['pigment'];name=obj.name
    if key=='orc_mummy':
        if obj.get('eye_side'):return colors['undead_red']
        if pigment=='orc_skin':return colors['dry_orc_skin']
        if pigment=='orc_boot':return colors['orc_linen']
        if pigment=='orc_linen':
            f=.95+.025*math.sin(p.z*125+p.x*29)+.02*math.sin(p.y*97)
            return tuple(v*f for v in color)
    if key=='orc_zombie':
        if obj.get('eye_side') or 'brow' in name or 'lower_lid' in name:return colors['zombie_lime']
        if pigment=='orc_skin':
            if abs(p.x)>.174:return colors['zombie_cyan']
            if p.y<-.105 and .927<p.z<.954:return colors['zombie_green']
            return colors['undead_gray']
        if pigment=='orc_cloth':
            if 'trouser' in name:return colors['undead_gray']
            if 'fitted_sleeve' in name:return colors['undead_orange']
            return colors['undead_orange'] if p.z>.72 else colors['zombie_brown']
        if pigment=='orc_boot':return colors['undead_gray']
        if pigment=='orc_belt':return colors['zombie_lime']
    if pigment=='orc_metal':return colors['undead_metal']
    return color
