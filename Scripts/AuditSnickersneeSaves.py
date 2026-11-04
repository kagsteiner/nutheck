"""Verify played files unchanged; record only intended display-bridge replacement."""
import sys,json,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from NetHackSaveBackup import verify
root=Path(__file__).resolve().parents[1];archive=root/'Backups/NetHackSaves/20261104T072145.799461Z.zip';m=verify(archive)
current={prefix+'/'+p.relative_to(folder).as_posix():p for folder,prefix in [(root/'Saved/NetHack','NetHack'),(root/'Binaries/NetHack','Runtime')] for p in folder.rglob('*') if p.is_file()}
assert set(current)=={i['path'] for i in m['files']}
changed=[]
for i in m['files']:
    digest=hashlib.sha256(current[i['path']].read_bytes()).hexdigest()
    if digest!=i['sha256']:changed.append(dict(path=i['path'],before=i['sha256'],after=digest))
assert [c['path'] for c in changed]==['Runtime/NetHackBridge.exe'],changed
compat=(root/'build-snickersnee-compatibility.log').read_text();assert 'BRIDGE_BACKEND_COMPATIBILITY_PASS' in compat
result=dict(status='PASS',backup=archive.relative_to(root).as_posix(),baseline_files=len(m['files']),unchanged_files=len(m['files'])-len(changed),played_files=sum(i['path'].startswith('NetHack/') for i in m['files']),all_played_files_and_pointer_unchanged=True,file_set_unchanged=True,runtime_changes=changed,isolated_old_save_new_runtime_compatibility=True)
for manifest,label in [('snickersnee-protected.json','preceding_fbx'),('snickersnee-unreal-protected.json','preceding_unreal_assets')]:
    files=json.loads((root/'Art/ObjectInterpretations'/manifest).read_text())
    for name,digest in files.items():assert hashlib.sha256((root/name).read_bytes()).hexdigest()==digest,name
    result[label]=dict(count=len(files),all_hashes_unchanged=True)
(root/'Art/ObjectInterpretations/snickersnee-save-preservation.json').write_text(json.dumps(result,indent=2))
print('SNICKERSNEE_SAVE_PRESERVATION PASS '+json.dumps(result),flush=True)
