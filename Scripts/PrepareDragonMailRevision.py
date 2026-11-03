"""Preserve the rejected version and every unrelated canonical export."""
from pathlib import Path
import json,hashlib,shutil
from ArmorBatch2Config import ROOT,OUT,GROUPS
dragon=set(GROUPS[3:]);archive=OUT/'DragonMail-v1';archive.mkdir(exist_ok=True)
for p in [OUT/'ArmorBatch2.blend',OUT/'projection-report-armor-batch2.json']+[p for p in OUT.glob('*') if p.is_file() and (any(p.name.startswith(k+'-') for k in dragon) or p.stem in dragon)]:
    target=archive/p.name
    if not target.exists():shutil.copy2(p,target)
manifest=OUT/'dragon-mail-revision-protected.json'
if not manifest.exists():
    files=[p for f in ['CreatureInterpretations','ObjectInterpretations','EnvironmentInterpretations','TileFallback'] for p in (ROOT/'Art'/f).glob('*.fbx') if p.stem not in dragon]
    manifest.write_text(json.dumps({p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in files},indent=2))
refs=ROOT/'Art/ObjectInterpretations/References';refs.mkdir(exist_ok=True)
base=Path('C:/Users/agste/.codex/codex-remote-attachments/01a19c9e-548d-71f1-993c-5b4099449b60/33845996-1DE2-4291-B49C-F3F8DFC71936')
for i in [1,2]:shutil.copy2(base/(str(i)+'-Foto-'+str(i)+'.jpg'),refs/('DragonMail-user-reference-'+str(i)+'.jpg'))
print('DRAGON_REVISION_PREPARED protected='+str(len(json.loads(manifest.read_text()))))
