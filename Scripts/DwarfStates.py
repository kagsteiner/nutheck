"""Saved dwarf ancestry with separate tile-supported linen/undead treatments."""
import bpy,math
import CreatureGeometry as g
from KoboldStates import wrap_ribbon

def append_dwarf(key):
    with bpy.data.libraries.load(str(g.OUT/'CreatureBatch16.blend'),link=False) as (src,dst):
        dst.collections=['dwarf']
    col=dst.collections[0];col.name=key;bpy.context.scene.collection.children.link(col);col.hide_viewport=False
    for obj in list(col.objects):
        suffix=obj.name[len('dwarf_'):]
        if key=='dwarf_mummy' and (suffix.startswith('blue_tunic') or suffix.startswith('fitted_sleeve') or suffix.startswith('blue_trouser')):
            bpy.data.objects.remove(obj,do_unlink=True);continue
        obj.name=key+'_'+suffix;obj['creature']=key;obj['source_family_object']='dwarf_'+suffix
        obj.hide_render=False;obj.hide_viewport=False
        if 'preserve_paint' in obj:del obj['preserve_paint']
        for attr in list(obj.data.color_attributes):obj.data.color_attributes.remove(attr)
    bpy.context.view_layer.update()
    return col,bpy.data.objects[key+'_body']

def dwarf_linen(body,key):
    wrap_ribbon(body,key,'torso_linen',(0,0,.37),(0,0,.69),8,.047,'mummy_linen')
    wrap_ribbon(body,key,'forehead_linen',(0,-.006,.900),(0,-.006,.913),1.2,.020,'mummy_linen')
    for side in [-1,1]:
        wrap_ribbon(body,key,'upper_arm_linen',(side*.175,0,.647),(side*.235,-.003,.586),2.5,.031,'mummy_linen')
        wrap_ribbon(body,key,'forearm_linen',(side*.265,-.016,.528),(side*.277,-.052,.444),3,.029,'mummy_linen')
        wrap_ribbon(body,key,'upper_leg_linen',(side*.090,0,.330),(side*.104,0,.246),3,.032,'mummy_linen')
        wrap_ribbon(body,key,'lower_leg_linen',(side*.109,-.004,.200),(side*.111,-.012,.091),3.5,.032,'mummy_linen')
    # The isolated red shin pixel is ambiguous: a small cloth accent is an art
    # interpretation, not evidence of blood, a wound or live equipment.
    wrap_ribbon(body,key,'red_linen_accent',(.109,-.002,.219),(.109,-.002,.225),1,.014,'linen_red')

def dwarf_state_pigment(obj,p,color,colors):
    key=obj['creature'];pigment=obj['pigment']
    if key=='dwarf_mummy':
        if obj.get('eye_side'):return colors['undead_red']
        if pigment=='dwarf_skin':return colors['dry_skin']
        if pigment=='dwarf_beard' or obj.get('boot'):return colors['mummy_linen']
        if pigment=='mummy_linen':
            shade=.95+.03*math.sin(p.z*125+p.x*29)+.02*math.sin(p.y*97)
            return tuple(v*shade for v in colors['mummy_linen'])
    elif key=='dwarf_zombie':
        if pigment in {'dwarf_skin','dwarf_skin_shade'}:
            weight=.25+.45*math.exp(-((p.x+.05)/.09)**2-((p.z-.84)/.12)**2)
            return tuple(a*(1-weight)+b*weight for a,b in zip(colors['rot_green'],colors['rot_light']))
        if pigment=='dwarf_beard':return colors['ash_beard']
    if pigment=='dwarf_blue':
        t=max(0,min(1,(.06-p.x)/.24))*.55
        return tuple(a*(1-t)+b*t for a,b in zip(color,colors['dwarf_cyan']))
    return color
