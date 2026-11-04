from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'Art/CreatureInterpretations'
GROUPS=['gray_ooze','brown_pudding','black_pudding'];INITIAL_GROUP='gray_ooze'
BLEND_NAME='CreatureBatch32.blend';REPORT_NAME='projection-report-batch32.json'
raw=(ROOT/'upstream/NetHack/win/share/monsters.txt').read_text()
tiles={n:[r.strip() for r in rows.strip().splitlines()] for _,n,rows in re.findall(r'^# tile (\d+) \(([^\n]+)\)\s*\{([^}]+)\}',raw,re.M)}
# The lower/right offset A fringe is shadow. Retain enclosed mouth/chest marks.
SPATIAL_MASK_KEYS=GROUPS
PROJECTION_YAWS=[-180,-155,-125]


# Entire black silhouette is retained: no blanket dark-palette removal.
SOURCE_FIGURE_MASKS={"black_pudding":[(x,y) for y,row in enumerate(tiles["black pudding,male"]) for x,ch in enumerate(row) if ch!="."]}
