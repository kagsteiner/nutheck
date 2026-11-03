"""Arachnid records and reviewed dark-pixel shadow separation."""
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'Art/CreatureInterpretations'
GROUPS=['cave_spider','giant_spider','scorpion'];INITIAL_GROUP='cave_spider'
BLEND_NAME='CreatureBatch24.blend';REPORT_NAME='projection-report-batch24.json'
raw=(ROOT/'upstream/NetHack/win/share/monsters.txt').read_text()
tiles={name:[r.strip() for r in rows.strip().splitlines()] for _,name,rows in re.findall(r'^# tile (\d+) \(([^\n]+)\)\s*\{([^}]+)\}',raw,re.M)}
SPATIAL_MASK_KEYS=GROUPS
