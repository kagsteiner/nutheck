"""Tiger and juvenile/adult hell hounds, complete family anatomy and painted coats."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from CreatureGeometry import *
import CreatureGeometry as geo
from FelineFamily import feline
from CanidFamily import canid
from CreatureFur import apply_fur
from CreatureBatch10Paint import batch10_pigment
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for key,color in {
    'tiger_coat':(.78,.235,.018),'tiger_pale':(.88,.81,.64),'tiger_stripe':(.010,.008,.006),
    'wild_cat_inner':(.36,.13,.09),'wild_cat_dark':(.012,.010,.008),'tiger_nose':(.48,.035,.042),
    'tiger_green':(.12,.58,.018),'hell_coat':(.77,.115,.012),'hell_rust':(.33,.035,.006),
    'hell_muzzle':(.62,.085,.008),'hell_inner':(.29,.025,.014),'hell_red':(.83,.006,.008),
    'hell_mouth':(.16,.006,.008),'hell_tongue':(.95,.39,.008),'hell_ivory':(.86,.77,.56),
}.items():
    COLORS[key]=color
    mat=bpy.data.materials.new(key);mat.use_nodes=True;mat.diffuse_color=(*color,1)
    mat.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.82;MATS[key]=mat

feline('tiger',.372,.158,.181,.310,.154,.138,.084,.074,.460,
    'tiger_coat','tiger_pale','tiger_nose','tiger_green',marking='tiger_stripes')
for key,dims in [
    ('hell_hound_pup',(.232,.100,.117,.205,.117,.087,.163,.047)),
    ('hell_hound',(.331,.143,.168,.326,.135,.147,.205,.062)),
]:
    length,width,depth,leg,head,muzzle,ear_height,paw=dims
    body=canid(key,*dims,domestic=False,coat='hell_coat',pale='hell_muzzle',inner='hell_inner',
        iris='hell_red',marking='hell_coat',tail_form='raised')
    body['family_variant']=key;body['leg_height']=leg
    body['head_length']=head;body['head_to_body_length']=head/length
    hx=-length*.60-.085;hz=leg+depth+depth*.91
    body['head_x']=hx;body['head_z']=hz
    geo.GROUP=key
    # An open jaw and warm tongue echo the tile's fire-at-mouth cue. No static
    # hovering flame plume is substituted for a future animated breath effect.
    for obj in list(bpy.data.objects):
        if obj.get('creature')==key and obj.name.startswith(key+'_mouth'):bpy.data.objects.remove(obj,do_unlink=True)
    orb('oral_cavity',(hx-head*.68,0,hz-head*.62),(muzzle*.88,head*.49,head*.13),'hell_mouth')
    jaw=orb('lower_jaw',(hx-head*.68,0,hz-head*.83),(muzzle*.86,head*.49,head*.12),'hell_coat')
    jaw['fur_surface']=True;jaw['fur_leg_height']=leg
    orb('warm_tongue',(hx-head*.78-muzzle*.25,0,hz-head*.71),(muzzle*.52,head*.28,head*.040),'hell_tongue')
    for side in [-1,1]:
        for offset in [.20,.85]:
            x=hx-head*.68-muzzle*offset
            limb('upper_canine',[(x,side*head*.38,hz-head*.52),(x-.003,side*head*.38,hz-head*.73)],
                [head*.046,head*.006],'hell_ivory')
    body['breath_effect_hook']=[hx-head*.68-muzzle,0,hz-head*.67]

GROUPS=['tiger','hell_hound_pup','hell_hound'];BLEND_NAME='CreatureBatch10.blend';REPORT_NAME='projection-report-batch10.json'
PIGMENT_FUNCTION=batch10_pigment
POST_PAINT=lambda:apply_fur([o for o in bpy.context.scene.objects if o.type=='MESH'])
exec(compile(Path(__file__).with_name('CreatureBatch2Pipeline.py').read_text(encoding='utf-8'),'CreatureBatch2Pipeline.py','exec'))
