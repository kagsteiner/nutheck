"""Targeted import of three painted reptile forms."""
from pathlib import Path
CREATURE_IMPORT_KEYS=['garter_snake','snake','water_moccasin']
exec(compile(Path(__file__).with_name('ImportCreatureInterpretations.py').read_text(encoding='utf-8'),'ImportCreatureInterpretations.py','exec'))
