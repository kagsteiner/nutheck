"""Build only Valkyrie quest assets; never launch a game."""
import unreal
from pathlib import Path
root=Path(unreal.Paths.project_dir()).resolve()
for name in ['CreateValkyrieMaterials.py','ImportOrbOfFate.py','CreateValkyrieSky.py']:
 p=root/'Scripts'/name
 exec(compile(p.read_text(),str(p),'exec'))
unreal.SystemLibrary.quit_editor()
