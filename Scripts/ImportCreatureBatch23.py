"""Targeted import of two bee forms and separate xan."""
from pathlib import Path
CREATURE_IMPORT_KEYS=['killer_bee','queen_bee','xan']
exec(compile(Path(__file__).with_name('ImportCreatureInterpretations.py').read_text(encoding='utf-8'),'ImportCreatureInterpretations.py','exec'))
