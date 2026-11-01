"""Targeted three-asset import; earlier assets remain untouched."""
from pathlib import Path
CREATURE_IMPORT_KEYS=['kobold_shaman','kobold_mummy','kobold_zombie']
exec(compile(Path(__file__).with_name('ImportCreatureInterpretations.py').read_text(encoding='utf-8'),'ImportCreatureInterpretations.py','exec'))
