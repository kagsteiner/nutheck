"""Read-only comparison against the verified pre-integration save/runtime backup."""
import hashlib,json
from pathlib import Path
from NetHackSaveBackup import verify
root=Path(__file__).resolve().parents[1]
archive=root/'Backups/NetHackSaves/20261104T070800.717411Z.zip'
m=verify(archive)
current={prefix+'/'+p.relative_to(folder).as_posix():p for folder,prefix in [(root/'Saved/NetHack','NetHack'),(root/'Binaries/NetHack','Runtime')] for p in folder.rglob('*') if p.is_file()}
assert set(current)=={i['path'] for i in m['files']},'Played/runtime file set changed'
for i in m['files']:assert hashlib.sha256(current[i['path']].read_bytes()).hexdigest()==i['sha256'],i['path']
result=dict(status='PASS',archive=archive.relative_to(root).as_posix(),verified_files=len(m['files']),all_hashes_unchanged=True,played_file_set_unchanged=True,last_session_pointer_unchanged=True,backend_unchanged=True)
for manifest,label in [('weapon-batch4-protected.json','preceding_fbx'),('weapon-batch4-unreal-protected.json','preceding_unreal_assets')]:
    files=json.loads((root/'Art/ObjectInterpretations'/manifest).read_text())
    for name,digest in files.items():assert hashlib.sha256((root/name).read_bytes()).hexdigest()==digest,name
    result[label]=dict(count=len(files),all_hashes_unchanged=True)
(root/'Art/ObjectInterpretations/weapon-batch4-save-preservation.json').write_text(json.dumps(result,indent=2))
print('WEAPON_BATCH4_SAVE_PRESERVATION PASS '+json.dumps(result))

