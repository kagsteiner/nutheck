"""Full-editor startup entry point: only coyote, warg and rabid rat."""
from pathlib import Path
CREATURE_IMPORT_KEYS=['coyote','warg','rabid_rat']
exec(compile(Path(__file__).with_name('ImportCreatureInterpretations.py').read_text(encoding='utf-8'),
             'ImportCreatureInterpretations.py','exec'))
