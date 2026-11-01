"""Full-editor startup entry point: import only the two revised winter forms."""
from pathlib import Path
CREATURE_IMPORT_KEYS=['winter_wolf_cub','winter_wolf']
exec(compile(Path(__file__).with_name('ImportCreatureInterpretations.py').read_text(encoding='utf-8'),
             'ImportCreatureInterpretations.py','exec'))
