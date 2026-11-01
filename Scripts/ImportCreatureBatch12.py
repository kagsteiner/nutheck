"""Full-editor startup entry point for the three new unicorns."""
from pathlib import Path
CREATURE_IMPORT_KEYS=['white_unicorn','gray_unicorn','black_unicorn']
exec(compile(Path(__file__).with_name('ImportCreatureInterpretations.py').read_text(encoding='utf-8'),
             'ImportCreatureInterpretations.py','exec'))
