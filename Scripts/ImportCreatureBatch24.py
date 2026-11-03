"""Targeted import of three painted arachnid forms."""
from pathlib import Path
CREATURE_IMPORT_KEYS=['cave_spider','giant_spider','scorpion']
exec(compile(Path(__file__).with_name('ImportCreatureInterpretations.py').read_text(encoding='utf-8'),'ImportCreatureInterpretations.py','exec'))
