"""Targeted import of two shared-sex orc undead forms."""
from pathlib import Path
CREATURE_IMPORT_KEYS=['orc_mummy','orc_zombie']
exec(compile(Path(__file__).with_name('ImportCreatureInterpretations.py').read_text(encoding='utf-8'),'ImportCreatureInterpretations.py','exec'))
