"""Targeted import of floating eye, newt and lichen."""
from pathlib import Path
CREATURE_IMPORT_KEYS=['floating_eye','newt','lichen']
exec(compile(Path(__file__).with_name('ImportCreatureInterpretations.py').read_text(encoding='utf-8'),'ImportCreatureInterpretations.py','exec'))
