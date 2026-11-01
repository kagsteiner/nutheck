"""Targeted import of two shared-sex dwarf undead forms."""
from pathlib import Path
CREATURE_IMPORT_KEYS=['dwarf_mummy','dwarf_zombie']
exec(compile(Path(__file__).with_name('ImportCreatureInterpretations.py').read_text(encoding='utf-8'),'ImportCreatureInterpretations.py','exec'))
