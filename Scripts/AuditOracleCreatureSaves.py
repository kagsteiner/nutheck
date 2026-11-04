"""Read-only comparison against the verified pre-integration save/runtime backup."""
import hashlib,json
from pathlib import Path
from NetHackSaveBackup import verify
root=Path(__file__).resolve().parents[1]
archive=root/'Backups/NetHackSaves/20261103T100726.125114Z.zip'
m=verify(archive)
current={prefix+'/'+p.relative_to(folder).as_posix():p for folder,prefix in [(root/'Saved/NetHack','NetHack'),(root/'Binaries/NetHack','Runtime')] for p in folder.rglob('*') if p.is_file()}
assert set(current)=={i['path'] for i in m['files']},'Played/runtime file set changed'
for i in m['files']:assert hashlib.sha256(current[i['path']].read_bytes()).hexdigest()==i['sha256'],i['path']
result=dict(status='PASS',archive=archive.relative_to(root).as_posix(),verified_files=len(m['files']),all_hashes_unchanged=True,played_file_set_unchanged=True,last_session_pointer_unchanged=True,backend_unchanged=True)
(root/'Art/CreatureInterpretations/oracle-save-preservation.json').write_text(json.dumps(result,indent=2))
print('ORACLE_CREATURE_SAVE_PRESERVATION PASS '+json.dumps(result))

