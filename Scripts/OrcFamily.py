"""Saved goblin-derived hobgoblin and a compatible upright orc family."""
import bpy,math
import CreatureGeometry as g
from CreatureGeometry import orb,limb,sculpt_union
from DwarfFamily import shell

def remove_degenerate_faces(o):
    bad=[p for p in o.data.polygons if p.area<=1e-12]
    if not bad:return
    old=o.data;mesh=bpy.data.meshes.new(old.name+'_clean')
    mesh.from_pydata([v.co[:] for v in old.vertices],[],[p.vertices[:] for p in old.polygons if p.area>1e-12]);mesh.update()
    for m in old.materials:mesh.materials.append(m)
    for p in mesh.polygons:p.use_smooth=True
    o.data=mesh;o['removed_degenerate_faces']=len(bad)

def hobgoblin():
    with bpy.data.libraries.load(str(g.OUT/'CreatureInterpretations.blend'),link=False) as (src,dst):dst.collections=['goblin']
    col=dst.collections[0];bpy.context.scene.collection.children.link(col);col.hide_viewport=False
    for o in list(col.objects):
        suffix=o.name[len('goblin_'):];o.name='hobgoblin_'+suffix;o['creature']='hobgoblin';o['source_family_object']='goblin_'+suffix
        # Retain saved local mesh vertices; change stature through object transforms.
        for i,s in enumerate((1.06,1.05,1.10)):o.location[i]*=s;o.scale[i]*=s
        o.hide_render=False;o.hide_viewport=False
        if 'preserve_paint' in o:del o['preserve_paint']
        for a in list(o.data.color_attributes):o.data.color_attributes.remove(a)
        remove_degenerate_faces(o)
        if 'dagger' in suffix:o['equipment_module']=True
        col.objects.unlink(o);bpy.context.scene.collection.objects.link(o)
    bpy.data.collections.remove(col)

def upright_orc():
    g.GROUP='hill_orc';skin='orc_skin'
    parts=[orb('torso',(0,0,.65),(.163,.108,.228),skin),orb('hips',(0,0,.43),(.145,.105,.101),skin),
           orb('neck',(0,0,.861),(.065,.063,.082),skin),orb('skull',(0,-.008,.995),(.112,.101,.141),skin),
           orb('jaw',(0,-.047,.914),(.090,.079,.061),skin),orb('nose',(0,-.115,.983),(.030,.040,.038),skin)]
    for side in [-1,1]:
        parts += [orb('shoulder',(side*.158,0,.802),(.067,.065,.073),skin),
                  limb('upper_arm',[(side*.158,0,.802),(side*.222,-.014,.674)],[.059,.046],skin),
                  orb('elbow',(side*.222,-.014,.674),(.046,.045,.047),skin),
                  limb('forearm',[(side*.222,-.014,.674),(side*.232,-.07,.568)],[.046,.033],skin),
                  orb('hand',(side*.232,-.07,.548),(.038,.036,.050),skin),
                  limb('leg',[(side*.075,0,.456),(side*.094,0,.271),(side*.105,-.005,.077)],[.064,.048,.035],skin),
                  orb('foot',(side*.105,-.045,.040),(.058,.091,.039),skin)]
    body=sculpt_union(parts,'body',skin,.007);body['family']='upright_orc';body['shared_ancestry']=True
    for side in [-1,1]:
        orb('ear',(side*.109,-.005,.990),(.027,.022,.041),skin)
        eye=orb('eye',(side*.041,-.103,1.013),(.013,.008,.012),'black');eye['eye_side']=side
        limb('brow',[(side*.021,-.101,1.032),(side*.040,-.109,1.035),(side*.062,-.095,1.030)],[.007,.009,.006],skin)
        limb('lower_lid',[(side*.030,-.104,1.003),(side*.044,-.106,1.001),(side*.054,-.098,1.003)],[.004,.004,.003],skin)
        limb('trouser',[(side*.075,0,.448),(side*.094,0,.271),(side*.105,-.005,.090)],[.070,.054,.041],'orc_cloth')
        boot=orb('boot',(side*.105,-.046,.043),(.061,.095,.042),'orc_boot');boot['costume_module']=True
        sleeve=limb('sleeve',[(side*.160,0,.799),(side*.213,-.010,.698)],[.070,.057],'orc_cloth')
        shoulder=orb('cloth_shoulder',(side*.158,0,.802),(.074,.072,.080),'orc_cloth')
        sleeve=sculpt_union([sleeve,shoulder],'fitted_sleeve','orc_cloth',.0045);sleeve['costume_module']=True
    tunic=shell('tunic',[(.335,.153,.114,0,0),(.48,.163,.120,0,0),(.61,.176,.121,0,0),(.73,.172,.120,0,0),(.81,.177,.112,0,0),(.852,.082,.071,0,0)],'orc_cloth');tunic['costume_module']=True
    belt=shell('belt',[(.505,.169,.125,0,0),(.54,.175,.127,0,0)],'orc_belt',.005);belt['costume_module']=True
    helm=shell('helmet',[(1.055,.118,.105,0,-.008),(1.095,.120,.107,0,-.006),(1.133,.095,.086,0,-.003),(1.155,.055,.051,0,0),(1.165,.002,.002,0,0)],'orc_metal',closed=True);helm['equipment_module']=True
    # Simple source-colour held rods; no invented axe head, insignia or inventory lookup.
    rod=limb('held_rod',[(-.232,-.078,.195),(-.232,-.078,.591)],[.016,.016],'orc_rod');rod['equipment_module']=True
    blade=limb('held_pale_blade',[(.232,-.072,.548),(.329,-.072,.662)],[.019,.001],'orc_metal');blade['equipment_module']=True
    for o in list(bpy.context.scene.objects):
        if o.type=='MESH' and o.get('creature')=='hill_orc':
            c=o.copy();c.data=o.data.copy();c.name='mordor_orc'+o.name[len('hill_orc'):];c['creature']='mordor_orc';bpy.context.scene.collection.objects.link(c)

def orc_pigment(obj,p,color,colors):
    key=obj['creature'];pigment=obj['pigment']
    if key=='hobgoblin':return colors['hob_yellow'] if pigment=='green' else color
    if key=='mordor_orc':
        return colors.get({'orc_skin':'mordor_skin','orc_cloth':'mordor_cloth','orc_boot':'mordor_boot','orc_belt':'mordor_red','orc_rod':'mordor_cyan'}.get(pigment,''),color)
    if pigment=='orc_cloth':
        t=max(0,min(1,(.06-p.x)/.24))*.4
        return tuple(a*(1-t)+b*t for a,b in zip(color,colors['hill_lime']))
    return color
