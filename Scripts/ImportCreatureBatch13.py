"""Targeted full-editor startup import for three kobolds."""
from pathlib import Path
CREATURE_IMPORT_KEYS=['kobold','large_kobold','kobold_leader']
exec(compile(Path(__file__).with_name('ImportCreatureInterpretations.py').read_text(encoding='utf-8'),'ImportCreatureInterpretations.py','exec'))
