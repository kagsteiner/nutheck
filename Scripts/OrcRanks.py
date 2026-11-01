"""Append saved upright orc anatomy, separate caster/rank/shield cues and paint."""
import bpy,math
import CreatureGeometry as g
from CreatureGeometry import limb
from DwarfFamily import shell

def append_orc(key):
    source='mordor_orc'
    with bpy.data.libraries.load(str(g.OUT/'CreatureBatch18.blend'),link=False) as (src,dst):dst.collections=[source]
    col=dst.collections[0];col.name=key;bpy.context.scene.collection.children.link(col);col.hide_viewport=False
    for obj in list(col.objects):
        suffix=obj.name[len(source)+1:]
        if suffix=='held_pale_blade' and key in ['uruk_hai','orc_shaman']:
            bpy.data.objects.remove(obj,do_unlink=True);continue
        obj.name=key+'_'+suffix;obj['creature']=key;obj['source_family_object']=source+'_'+suffix
        obj.hide_render=False;obj.hide_viewport=False
        if 'preserve_paint' in obj:del obj['preserve_paint']
        for attr in list(obj.data.color_attributes):obj.data.color_attributes.remove(attr)
    for obj in list(col.objects):col.objects.unlink(obj);bpy.context.scene.collection.objects.link(obj)
    bpy.data.collections.remove(col);bpy.context.view_layer.update()
    return bpy.data.objects[key+'_body']

def uruk_shield():
    g.GROUP='uruk_hai';verts=[];faces=[];n=16
    # A shallow curved solid panel sits in front of the retained right hand.
    # Red rectangle is pigment on the shield, not an added emblem object.
    for j in range(n+1):
        z=.365+.285*j/n
        for i in range(n+1):
            t=i/n;x=.151+.218*t;y=-.119-.034*math.sin(math.pi*t)
            verts.append((x,y,z))
    for j in range(n):
        for i in range(n):
            a=j*(n+1)+i;faces.append((a,a+1,a+n+2,a+n+1))
    mesh=bpy.data.meshes.new('Curved source shield');mesh.from_pydata(verts,[],faces);mesh.update()
    obj=bpy.data.objects.new('Curved source shield',mesh);bpy.context.scene.collection.objects.link(obj)
    g.finish(obj,'detachable_shield','rank_metal');obj['equipment_module']=True;obj['shield_module']=True
    for p in mesh.polygons:p.use_smooth=True
    obj.modifiers.new('Closed shield thickness','SOLIDIFY').thickness=.014
    grip=limb('shield_back_grip',[(.232,-.070,.548),(.232,-.140,.548)],[.012,.014],'leather');grip['equipment_module']=True

def captain_brim():
    g.GROUP='orc_captain'
    rim=shell('detachable_helmet_rim',[(1.061,.124,.111,0,-.008),(1.071,.158,.125,0,-.008),(1.086,.153,.122,0,-.008),(1.091,.120,.108,0,-.008)],'rank_metal',.004)
    rim['equipment_module']=True;rim['rank_module']=True

def rank_pigment(obj,p,color,colors):
    key=obj['creature'];pigment=obj['pigment'];name=obj.name
    if pigment=='orc_skin':
        # Paired peach cheek pixels appear beside the shared gray nose/face.
        cheek=math.exp(-((abs(p.x)-.071)/.029)**2-((p.z-.992)/.033)**2)
        cheek*=max(0,min(1,(-p.y-.057)/.035))
        return tuple(a*(1-cheek)+b*cheek for a,b in zip(colors['rank_skin'],colors['rank_cheek']))
    if obj.get('shield_module'):
        if abs(p.x-.260)<.052 and abs(p.z-.507)<.062:return colors['rank_red']
        return colors['rank_metal']
    if pigment=='orc_metal' or pigment=='rank_metal':return colors['rank_metal']
    if pigment=='orc_boot':return colors['rank_skin']
    if pigment=='orc_rod':return colors['rank_cyan']
    if pigment=='orc_belt':
        return colors['rank_white'] if key=='uruk_hai' else colors['rank_lime'] if key=='orc_shaman' else colors['rank_brown']
    if pigment=='orc_cloth':
        if key=='orc_shaman':
            if name.endswith('_tunic') and p.y<-.065 and abs(p.x)<.057:return colors['rank_brown']
            return colors['shaman_orange']
        if key=='orc_captain':
            if 'fitted_sleeve' in name and p.z>.762:return colors['rank_red']
            if name.endswith('_tunic') and .548<p.z<.767 and p.y<-.045:return colors['rank_lime']
        return colors['rank_magenta']
    return color
