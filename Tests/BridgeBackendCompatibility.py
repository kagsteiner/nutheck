"""Old-runtime save -> current runtime, strictly in fresh isolated directories."""
from BridgeGameplay import Game, ROOT
import BridgeGameplay
import hashlib,json,sys,uuid,zipfile

archive=ROOT/sys.argv[1]
root=ROOT/'Saved/NetHackGameplayTests'/('backend-compatibility-'+uuid.uuid4().hex)
with zipfile.ZipFile(archive) as z:
    manifest=json.loads(z.read('manifest.json'))
    for e in manifest['files']:
        if not e['path'].startswith('Runtime/'):continue
        data=z.read(e['path']);assert hashlib.sha256(data).hexdigest()==e['sha256']
        target=root/e['path'];target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
new_exe=BridgeGameplay.EXE
BridgeGameplay.EXE=root/'Runtime/NetHackBridge.exe'
old=Game(root/'session')
try:
    old.settle();old.command('.')
    expected=(old.position,old.state['moves'],old.state['hp'])
finally:old.close()
assert old.proc.returncode==0
BridgeGameplay.EXE=new_exe
new=Game(root/'session')
try:
    new.settle();actual=(new.position,new.state['moves'],new.state['hp'])
    assert actual==expected,(actual,expected)
    new.command('.');assert new.state['moves']>expected[1]
finally:new.close()
assert new.proc.returncode==0
print('BRIDGE_BACKEND_COMPATIBILITY_PASS '+json.dumps(dict(backup=str(archive),session=str(root/'session'),state=expected)),flush=True)
