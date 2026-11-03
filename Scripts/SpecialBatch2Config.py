"""One shared shopkeeper form and five displayed altar appearances."""
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'Art/SpecialBatch2';OUT.mkdir(parents=True,exist_ok=True)
ALTARS=['unaligned','chaotic','neutral','lawful','other']
GROUPS=['shopkeeper']+['altar_'+k for k in ALTARS];INITIAL_GROUP='shopkeeper'
BLEND_NAME='SpecialBatch2.blend';REPORT_NAME='projection-report-special2.json'
SOURCE_TILE_NAMES={'shopkeeper':'shopkeeper,male',**{'altar_'+k:k+' altar' for k in ALTARS}}
SOURCE_TILE_ENTRIES={}
text=(ROOT/'upstream/NetHack/win/share/other.txt').read_text()
for _,name,rows in re.findall(r'^# tile (\d+) \(([^\n]+)\)[^{]*\{([^}]+)\}',text,re.M):
    if name in SOURCE_TILE_NAMES.values():SOURCE_TILE_ENTRIES[name]=rows.strip().splitlines()
EXPORT_PATHS={key:ROOT/'Art'/('CreatureInterpretations' if key=='shopkeeper' else 'EnvironmentInterpretations')/(key+'.fbx') for key in GROUPS}
SPATIAL_MASK_KEYS=GROUPS
SOURCE_FIGURE_MASKS={'shopkeeper':[(x,y) for y in range(2,14) for x in range(4,11)]}
