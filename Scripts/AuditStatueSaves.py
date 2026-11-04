"""Verify played files unchanged; record only intended display-bridge replacement."""
import sys,json,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from NetHackSaveBackup import verify
root=Path(__file__).resolve().parents[1];archive=root/'Backups/NetHackSaves/20261103T114902.378796Z.zip';m=verify(archive)
current={prefix+'/'+p.relative_to(folder).as_posix():p for folder,prefix in [(root/'Saved/NetHack','NetHack'),(root/'Binaries/NetHack','Runtime')] for p in folder.rglob('*') if p.is_file()}
assert set(current)=={i['path'] for i in m['files']}
changed=[]
for i in m['files']:
    digest=hashlib.sha256(current[i['path']].read_bytes()).hexdigest()
    if digest!=i['sha256']:changed.append(dict(path=i['path'],before=i['sha256'],after=digest))
assert [c['path'] for c in changed]==['Runtime/NetHackBridge.exe'],changed
compat=(root/'build-statues-compatibility.log').read_text();assert 'BRIDGE_BACKEND_COMPATIBILITY_PASS' in compat
result=dict(status='PASS',backup=archive.relative_to(root).as_posix(),baseline_files=len(m['files']),unchanged_files=len(m['files'])-len(changed),played_files=sum(i['path'].startswith('NetHack/') for i in m['files']),all_played_files_and_pointer_unchanged=True,file_set_unchanged=True,runtime_changes=changed,isolated_old_save_new_runtime_compatibility=True)
(root/'Art/CreatureInterpretations/statues-save-preservation.json').write_text(json.dumps(result,indent=2))
print('STATUES_SAVE_PRESERVATION PASS '+json.dumps(result),flush=True)
