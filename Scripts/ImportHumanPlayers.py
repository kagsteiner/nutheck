from pathlib import Path
CREATURE_IMPORT_KEYS=['valkyrie_female_human','barbarian_male_human']
exec(compile(Path(__file__).with_name('ImportCreatureInterpretations.py').read_text(encoding='utf-8'),'ImportCreatureInterpretations.py','exec'))
