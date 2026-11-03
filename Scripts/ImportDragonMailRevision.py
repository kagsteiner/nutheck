from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from ArmorBatch2Config import GROUPS
ARMOR_IMPORT_KEYS=GROUPS[3:]
exec(compile(Path(__file__).with_name('ImportArmorBatch2.py').read_text(),'ImportArmorBatch2.py','exec'))
