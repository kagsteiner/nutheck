"""Targeted import of Uruk-hai, orc shaman and orc-captain."""
from pathlib import Path
CREATURE_IMPORT_KEYS=['uruk_hai','orc_shaman','orc_captain']
exec(compile(Path(__file__).with_name('ImportCreatureInterpretations.py').read_text(encoding='utf-8'),'ImportCreatureInterpretations.py','exec'))
