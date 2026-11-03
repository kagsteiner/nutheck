"""Targeted import of five reviewed insect forms."""
from pathlib import Path
CREATURE_IMPORT_KEYS=['soldier_ant','soldier_ant_female','fire_ant','fire_ant_female','giant_beetle']
exec(compile(Path(__file__).with_name('ImportCreatureInterpretations.py').read_text(encoding='utf-8'),'ImportCreatureInterpretations.py','exec'))
