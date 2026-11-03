from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from ArmorBatch2Config import GROUPS
ARMOR_BLEND='ArmorBatch2.blend';ARMOR_KEYS=GROUPS[3:]
source=Path(__file__).with_name('ReviewArmorStudy.py').read_text().replace('resolution_x=600;scene.render.resolution_y=600','resolution_x=480;scene.render.resolution_y=480').replace('scene.cycles.samples=12','scene.cycles.samples=6')
exec(compile(source,'ReviewDragonMailRevision','exec'))
