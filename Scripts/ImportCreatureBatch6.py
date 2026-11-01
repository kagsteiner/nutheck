"""Full-editor entry point: import just this batch, retaining existing meshes."""
from pathlib import Path
CREATURE_IMPORT_KEYS=['dog','large_dog','dingo']
exec(compile(Path(__file__).with_name('ImportCreatureInterpretations.py').read_text(encoding='utf-8'),
             'ImportCreatureInterpretations.py','exec'))
