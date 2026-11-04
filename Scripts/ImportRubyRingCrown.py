"""Targeted ring-only reimport, reusing all existing batch materials unchanged."""
import unreal
from pathlib import Path
root=Path(unreal.Paths.project_dir()).resolve();source=root/'Art/ObjectInterpretations'
dest='/Game/AppearanceBatch1';tools=unreal.AssetToolsHelpers.get_asset_tools()
materials={name:unreal.load_asset(dest+'/'+name) for name in ['M_ObjectRuby','M_ObjectGold']}
assert all(materials.values())
code=(root/'Scripts/ImportAppearanceBatch1.py').read_text(encoding='utf-8')
code=code[code.index("for key in ['ruby_ring','spherical_amulet','oak_wand']:"):]
code=code.replace("['ruby_ring','spherical_amulet','oak_wand']","['ruby_ring']").replace('APPEARANCE_BATCH1_IMPORT_READY count=3','RUBY_CROWN_IMPORTED')
exec(compile(code,'RingOnlyImport','exec'))
