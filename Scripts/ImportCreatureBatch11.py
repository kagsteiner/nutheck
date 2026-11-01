"""Full-editor startup entry point for the three new equines."""
from pathlib import Path
CREATURE_IMPORT_KEYS=['pony','horse','warhorse']
exec(compile(Path(__file__).with_name('ImportCreatureInterpretations.py').read_text(encoding='utf-8'),
             'ImportCreatureInterpretations.py','exec'))
