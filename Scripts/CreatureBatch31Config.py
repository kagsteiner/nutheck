from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'Art/CreatureInterpretations'
GROUPS=['blue_jelly','spotted_jelly','ochre_jelly'];INITIAL_GROUP='blue_jelly'
BLEND_NAME='CreatureBatch31.blend';REPORT_NAME='projection-report-batch31.json'
raw=(ROOT/'upstream/NetHack/win/share/monsters.txt').read_text()
tiles={n:[r.strip() for r in rows.strip().splitlines()] for _,n,rows in re.findall(r'^# tile (\d+) \(([^\n]+)\)\s*\{([^}]+)\}',raw,re.M)}
# The lower/right offset A fringe is shadow. Retain enclosed mouth/chest marks.
SPATIAL_MASK_KEYS=GROUPS
PROJECTION_YAWS=[-180,-155,-125]

