"""Coyote/warg family variants and actual reuse of the reviewed lean rat body."""
import sys,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from CreatureGeometry import *
import CreatureGeometry as geo
from CanidFamily import canid
from CreatureFur import apply_fur
from CreatureSaliva import rat_saliva
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for key,color in {
    'coyote_brown':(.48,.165,.025),'coyote_light':(.64,.36,.12),
    'warg_charcoal':(.13,.145,.155),'warg_cool':(.22,.285,.34),
    'wild_inner':(.27,.16,.13),'wild_eye':(.65,.66,.52),'wild_red':(.65,.012,.016),
    'warg_gum':(.46,.013,.024),'fang_ivory':(.82,.79,.65),'saliva':(.78,.79,.72),
}.items():
    COLORS[key]=color
    mat=bpy.data.materials.new(key);mat.use_nodes=True;mat.diffuse_color=(*color,1)
    mat.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.82
    MATS[key]=mat

body=canid('coyote',.265,.092,.114,.266,.107,.122,.197,.047,domestic=False,
    coat='coyote_brown',pale='coyote_light',inner='wild_inner',iris='wild_eye',
    nose='wild_red',marking='coyote_shading',tail_form='brush')
body['family_variant']='coyote'
body=canid('warg',.345,.158,.182,.310,.159,.156,.205,.072,domestic=False,
    coat='warg_charcoal',pale='warg_charcoal',inner='wild_inner',iris='wild_eye',
    marking='warg_mottle',tail_form='raised')
body['family_variant']='warg'
geo.GROUP='warg';hx=-.345*.6-.085;hz=.310+.182+.182*.91;head=.159;muzzle=.156
# A separate lower jaw and oral surfaces; no invented coat/shadow geometry.
for obj in list(bpy.data.objects):
    if obj.get('creature')=='warg' and obj.name.startswith('warg_mouth'):bpy.data.objects.remove(obj,do_unlink=True)
orb('oral_cavity',(hx-head*.68,0,hz-head*.70),(muzzle*.88,head*.53,.026),'black')
orb('lower_jaw',(hx-head*.67,0,hz-head*.88-.012),(muzzle*.88,head*.50,.024),'warg_charcoal')
orb('tongue',(hx-head*.98,0,hz-head*.78-.004),(.046,.047,.009),'wild_red')
for side in [-1,1]:
    limb('gum',[(hx-head*1.18,side*head*.44,hz-head*.62),
        (hx-head*.38,side*head*.50,hz-head*.58)],[.007,.005],'warg_gum')
    for x in [hx-head*1.15,hx-head*.43]:
        limb('upper_fang',[(x,side*head*.43,hz-head*.59),
            (x-.006,side*head*.43,hz-head*.86)],[.008,.001],'fang_ivory')

# Append the saved approved sewer-rat anatomy and facial details exactly.
# Rabid rat is a separate displayed identity/state, not an obese new body.
with bpy.data.libraries.load(str(OUT/'CreatureBatch3.blend'),link=False) as (available,loaded):
    loaded.objects=[name for name in available.objects if name.startswith('sewer_rat_')]
for obj in loaded.objects:
    bpy.context.scene.collection.objects.link(obj)
    obj.name=obj.name.replace('sewer_rat_','rabid_rat_',1)
    obj['creature']='rabid_rat';obj['preserve_paint']=True
    obj.hide_render=False;obj.hide_viewport=False
    if obj.name=='rabid_rat_continuous_anatomy':obj['fur_surface']=True;obj['fur_leg_height']=.055
geo.GROUP='rabid_rat'
# Pale mouth mass in this tile is interpreted as a detachable saliva state cue.
# Keep whiskers, muzzle, ears, green eyes and lean body from the reviewed rat.
rat_saliva()
GROUPS=['coyote','warg','rabid_rat'];BLEND_NAME='CreatureBatch7.blend';REPORT_NAME='projection-report-batch7.json'
POST_PAINT=lambda:apply_fur([o for o in bpy.context.scene.objects if o.type=='MESH'])
exec(compile(Path(__file__).with_name('CreatureBatch2Pipeline.py').read_text(encoding='utf-8'),'CreatureBatch2Pipeline.py','exec'))
