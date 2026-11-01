"""Mixed creature/object/terrain source references and canonical export paths."""
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'Art/SpecialBatch1'
GROUPS=['grid_bug','corpse','fountain'];INITIAL_GROUP='grid_bug'
BLEND_NAME='SpecialBatch1.blend';REPORT_NAME='projection-report-special1.json'
SOURCE_TILE_NAMES={'grid_bug':'grid bug,male','corpse':'corpse','fountain':'fountain'}
SOURCE_TILE_ENTRIES={}
for category,label in [('objects','corpse'),('other','fountain')]:
    text=(ROOT/f'upstream/NetHack/win/share/{category}.txt').read_text(encoding='utf-8')
    for _,name,rows in re.findall(r'^# tile (\d+) \(([^\n]+)\)[^{]*\{([^}]+)\}',text,re.M):
        if name==label:SOURCE_TILE_ENTRIES[label]=rows.strip().splitlines()
EXPORT_PATHS={key:ROOT/'Art'/folder/(key+'.fbx') for key,folder in [('grid_bug','CreatureInterpretations'),('corpse','ObjectInterpretations'),('fountain','EnvironmentInterpretations')]}
for p in EXPORT_PATHS.values():p.parent.mkdir(parents=True,exist_ok=True)
SPATIAL_MASK_KEYS=GROUPS
