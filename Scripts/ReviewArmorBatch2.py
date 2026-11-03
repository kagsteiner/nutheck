from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from ArmorBatch2Config import *
ARMOR_BLEND='ArmorBatch2.blend';ARMOR_KEYS=GROUPS
exec(compile(Path(__file__).with_name('ReviewArmorStudy.py').read_text(),'ReviewArmorBatch2','exec'))
