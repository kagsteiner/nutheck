"""Full-editor startup entry point: import just this bat family batch."""
from pathlib import Path
CREATURE_IMPORT_KEYS=['bat','giant_bat','vampire_bat']
exec(compile(Path(__file__).with_name('ImportCreatureInterpretations.py').read_text(encoding='utf-8'),
             'ImportCreatureInterpretations.py','exec'))
