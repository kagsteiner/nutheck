"""Read-only audit: strict-topmost changes must leave saves AND backend unchanged."""
import sys,json,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from NetHackSaveBackup import verify
root=Path(__file__).resolve().parents[1]
archive=root/'Backups/NetHackSaves/20261103T073300.639492Z.zip'
baseline=verify(archive)
current={prefix+'/'+p.relative_to(folder).as_posix():p for folder,prefix in [(root/'Saved/NetHack','NetHack'),(root/'Binaries/NetHack','Runtime')] for p in folder.rglob('*') if p.is_file()}
assert set(current)=={f['path'] for f in baseline['files']}
for f in baseline['files']:
    p=current[f['path']];assert p.stat().st_size==f['size'] and hashlib.sha256(p.read_bytes()).hexdigest()==f['sha256'],f['path']
result=dict(status='PASS',backup=archive.relative_to(root).as_posix(),files_verified=len(current),player_files=sum(n.startswith('NetHack/') for n in current),runtime_files=sum(n.startswith('Runtime/') for n in current),all_files_and_session_pointer_unchanged=True)
(root/'Art/ObjectInterpretations/topmost-save-preservation.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print('TOPMOST_SAVE_PRESERVATION_PASS '+json.dumps(result))
