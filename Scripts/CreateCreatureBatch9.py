"""Jaguar, lynx and panther: shared feline anatomy, distinct silhouettes and paint."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from CreatureGeometry import *
from FelineFamily import feline
from CreatureFur import apply_fur
from WildCatPaint import wild_cat_pigment
from JaguarCoat import jaguar_shade
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for key,color in {
    'jaguar_gold':(.68,.36,.085),'jaguar_muzzle':(.84,.77,.59),'jaguar_spot':(.010,.006,.003),
    'lynx_coat':(.68,.235,.030),'lynx_pale':(.83,.48,.25),
    'panther_coat':(.022,.027,.028),'panther_muzzle':(.035,.038,.037),
    'panther_whisker':(.18,.19,.17),'wild_cat_dark':(.014,.017,.015),
    'wild_cat_inner':(.37,.20,.15),'wild_cat_nose':(.58,.024,.040),
    'wild_cat_green':(.13,.58,.020),'panther_yellow':(.82,.65,.008),
}.items():
    COLORS[key]=color
    mat=bpy.data.materials.new(key);mat.use_nodes=True;mat.diffuse_color=(*color,1)
    mat.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.82
    MATS[key]=mat

feline('jaguar',.320,.148,.170,.255,.143,.128,.080,.068,.305,
    'jaguar_gold','jaguar_muzzle','wild_cat_nose','wild_cat_green',marking='jaguar_rosettes')
feline('lynx',.260,.109,.130,.275,.127,.109,.104,.075,.110,
    'lynx_coat','lynx_pale','wild_cat_nose','wild_cat_green',lynx=True,marking='lynx_flank')
feline('panther',.345,.129,.145,.300,.132,.113,.083,.062,.490,
    'panther_coat','panther_muzzle','wild_cat_dark','panther_yellow')
GROUPS=['jaguar','lynx','panther'];BLEND_NAME='CreatureBatch9.blend';REPORT_NAME='projection-report-batch9.json'
PIGMENT_FUNCTION=wild_cat_pigment
SHADE_FUNCTION=jaguar_shade
POST_PAINT=lambda:apply_fur([o for o in bpy.context.scene.objects if o.type=='MESH'])
exec(compile(Path(__file__).with_name('CreatureBatch2Pipeline.py').read_text(encoding='utf-8'),'CreatureBatch2Pipeline.py','exec'))
