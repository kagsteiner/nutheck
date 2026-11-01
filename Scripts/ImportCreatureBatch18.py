"""Targeted import of three shared-sex dwarf forms."""
from pathlib import Path
CREATURE_IMPORT_KEYS=['hobgoblin','hill_orc','mordor_orc']
exec(compile(Path(__file__).with_name('ImportCreatureInterpretations.py').read_text(encoding='utf-8'),'ImportCreatureInterpretations.py','exec'))
