from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'Art/CreatureInterpretations'
GROUPS=['yeti','sasquatch','owlbear'];INITIAL_GROUP='yeti'
BLEND_NAME='CreatureBatch29.blend';REPORT_NAME='projection-report-batch29.json'
raw=(ROOT/'upstream/NetHack/win/share/monsters.txt').read_text()
tiles={n:[r.strip() for r in rows.strip().splitlines()] for _,n,rows in re.findall(r'^# tile (\d+) \(([^\n]+)\)\s*\{([^}]+)\}',raw,re.M)}
# The lower/right offset A fringe is shadow. Retain enclosed mouth/chest marks.
SPATIAL_MASK_KEYS=GROUPS
PROJECTION_YAWS=[-180,-155,-125]

SOURCE_FIGURE_MASKS={"yeti":[(x,y) for y,row in enumerate(tiles["yeti,male"]) for x,ch in enumerate(row) if ch not in {".","A","P","B"} or (ch=="A" and y<5 and x<9)]}
