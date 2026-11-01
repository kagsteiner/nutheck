"""Full-editor startup entry point: only the reference-repainted jaguar."""
from pathlib import Path
CREATURE_IMPORT_KEYS=['jaguar']
exec(compile(Path(__file__).with_name('ImportCreatureInterpretations.py').read_text(encoding='utf-8'),
             'ImportCreatureInterpretations.py','exec'))
