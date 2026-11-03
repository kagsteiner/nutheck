from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from ArmorBatch2Config import *
ARMOR_BLEND='ArmorBatch2.blend';ARMOR_KEYS=GROUPS;ARMOR_REPORT='armor-batch2-inspection.json'
source=Path(__file__).with_name('InspectArmorStudy.py').read_text().replace('armor-study-protected.json','armor-batch2-protected.json').replace('==96','==104').replace('previous_96','previous_104')
exec(compile(source,'InspectArmorBatch2','exec'))
for key in GROUPS[3:]:
    parts=[o for o in bpy.data.objects if o.type=='MESH' and o.get('creature')==key]
    assert sum(o.get('leaf_scale_count',0) for o in parts)>1400,key
    assert sum('curved_pauldron_lame' in o.name for o in parts)==6,key
    assert not any('great_chest_scute' in o.name or 'gray_pectoral' in o.name for o in parts)
assert sum('gray_fine_leaf_spine_rim' in o.name for o in bpy.data.objects)==1
print('ARMOR_BATCH2_ANATOMY_CHECK PASS variants=10 gray_showpiece=True')
