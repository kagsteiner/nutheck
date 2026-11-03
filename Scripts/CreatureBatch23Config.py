"""Selected forms and explicit shadow masks for winged insect source tiles."""
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'Art/CreatureInterpretations'
GROUPS=['killer_bee','queen_bee','xan'];INITIAL_GROUP='killer_bee'
BLEND_NAME='CreatureBatch23.blend';REPORT_NAME='projection-report-batch23.json'
raw=(ROOT/'upstream/NetHack/win/share/monsters.txt').read_text()
tiles={name:[r.strip() for r in rows.strip().splitlines()] for _,name,rows in re.findall(r'^# tile (\d+) \(([^\n]+)\)\s*\{([^}]+)\}',raw,re.M)}
SOURCE_FIGURE_MASKS={}
for key in GROUPS:
    rows=tiles[key.replace('_',' ')+',male']
    # Bee shadows are detached at the bottom. Keep actual black abdomen bands.
    if key=='killer_bee':keep={(x,y) for y in range(12) for x in range(16) if rows[y][x]!='.'}
    elif key=='queen_bee':keep={(x,y) for y in range(14) for x in range(16) if rows[y][x]!='.'}
    else:
        # Xan's black right/lower mass is cast shadow; real enclosed pupils remain.
        keep={(x,y) for y,row in enumerate(rows) for x,ch in enumerate(row) if ch not in {'.','A'}}|{(1,10),(6,12)}
    SOURCE_FIGURE_MASKS[key]=sorted(keep)
