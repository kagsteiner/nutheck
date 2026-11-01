"""Five physical forms for the three new gnome identities."""
from pathlib import Path
CREATURE_IMPORT_KEYS=['gnomish_wizard','gnome_mummy','gnome_zombie','gnomish_wizard_female','gnome_zombie_female']
exec(compile(Path(__file__).with_name('ImportCreatureInterpretations.py').read_text(encoding='utf-8'),'ImportCreatureInterpretations.py','exec'))
