from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'Art/CreatureInterpretations'
GROUPS=['python','pit_viper','cobra'];INITIAL_GROUP='python'
BLEND_NAME='CreatureBatch27.blend';REPORT_NAME='projection-report-batch27.json'
raw=(ROOT/'upstream/NetHack/win/share/monsters.txt').read_text()
tiles={name:[r.strip() for r in rows.strip().splitlines()] for _,name,rows in re.findall(r'^# tile (\d+) \(([^\n]+)\)\s*\{([^}]+)\}',raw,re.M)}
SPATIAL_MASK_KEYS=GROUPS
SOURCE_FIGURE_MASKS={key:[(x,y) for y,row in enumerate(tiles[key.replace('_',' ')+',male']) for x,ch in enumerate(row) if ch!='.'] for key in ['pit_viper','cobra']}
