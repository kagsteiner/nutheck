"""Full-editor startup entry point for the three new wild felines."""
from pathlib import Path
CREATURE_IMPORT_KEYS=['jaguar','lynx','panther']
exec(compile(Path(__file__).with_name('ImportCreatureInterpretations.py').read_text(encoding='utf-8'),
             'ImportCreatureInterpretations.py','exec'))
