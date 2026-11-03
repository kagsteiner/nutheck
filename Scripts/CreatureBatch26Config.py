"""Reptile records and reviewed dark-pixel shadow separation."""
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'Art/CreatureInterpretations'
GROUPS=['garter_snake','snake','water_moccasin'];INITIAL_GROUP='garter_snake'
BLEND_NAME='CreatureBatch26.blend';REPORT_NAME='projection-report-batch26.json'
raw=(ROOT/'upstream/NetHack/win/share/monsters.txt').read_text()
tiles={name:[r.strip() for r in rows.strip().splitlines()] for _,name,rows in re.findall(r'^# tile (\d+) \(([^\n]+)\)\s*\{([^}]+)\}',raw,re.M)}
SPATIAL_MASK_KEYS=GROUPS


SOURCE_FIGURE_MASKS={'water_moccasin':[(x,y) for y,line in enumerate(tiles['water moccasin,male']) for x,ch in enumerate(line) if ch!='.']}
# Keep enclosed dark marks, then remove the reviewed blue-gray offset shadow.
rows=tiles['garter snake,male']
foreground={(x,y) for y,row in enumerate(rows) for x,ch in enumerate(row) if ch not in {'.','A'}}
outside=set();pending=[(x,y) for x in range(16) for y in range(16) if x in {0,15} or y in {0,15}]
while pending:
    x,y=pending.pop()
    if not (0<=x<16 and 0<=y<16) or (x,y) in outside or (x,y) in foreground:continue
    outside.add((x,y));pending.extend([(x-1,y),(x+1,y),(x,y-1),(x,y+1)])
black={(x,y) for y,row in enumerate(rows) for x,ch in enumerate(row) if ch=='A' and (x,y) not in outside}
SOURCE_FIGURE_MASKS['garter_snake']=[(x,y) for x,y in foreground|black if rows[y][x]!='P']

