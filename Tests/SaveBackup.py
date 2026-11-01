"""Integrity, staged recovery, overwrite refusal and active-backend protection."""
import contextlib,io,json,sys,unittest,uuid,zipfile,subprocess
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'Scripts'))
import NetHackSaveBackup as backup

class SaveBackupTests(unittest.TestCase):
    def setUp(self):
        self.root=backup.ROOT/'Saved/SaveBackupChecks'/uuid.uuid4().hex
        self.source=self.root/'Saved/NetHack';self.source.mkdir(parents=True)
        (self.source/'LastSession.txt').write_bytes(b'example-session')
        (self.source/'.hidden-config').write_bytes(b'preserve hidden files')
        (self.source/'native-save').write_bytes(bytes(range(256))*4)
        runtime=self.root/'Binaries/NetHack';runtime.mkdir(parents=True)
        (runtime/'NetHackBridge.exe').write_bytes(b'fixture, never executed')
        with patch.object(backup,'ROOT',self.root),patch.object(backup,'stopped'),contextlib.redirect_stdout(io.StringIO()):backup.backup('test fixture')
        self.archive=next((self.root/'Backups/NetHackSaves').glob('*.zip'))

    def test_verified_recovery_keeps_source(self):
        manifest=backup.verify(self.archive);self.assertEqual(len(manifest['files']),4)
        target=self.root/'recovered'
        with contextlib.redirect_stdout(io.StringIO()):backup.recover(self.archive,target)
        for name in ['LastSession.txt','.hidden-config','native-save']:
            self.assertEqual((target/'NetHack'/name).read_bytes(),(self.source/name).read_bytes())
        self.assertEqual((target/'Runtime/NetHackBridge.exe').read_bytes(),b'fixture, never executed')

    def test_refuses_overwrite(self):
        target=self.root/'existing';target.mkdir();(target/'sentinel').write_bytes(b'newer run')
        with self.assertRaises(FileExistsError):backup.recover(self.archive,target)
        self.assertEqual((target/'sentinel').read_bytes(),b'newer run')

    def test_corruption_rejected_before_extract(self):
        damaged=self.root/'damaged.zip'
        with zipfile.ZipFile(self.archive) as source,zipfile.ZipFile(damaged,'w') as dest:
            for name in source.namelist():dest.writestr(name,b'corrupted' if name=='NetHack/native-save' else source.read(name))
        with self.assertRaises(ValueError):backup.recover(damaged,self.root/'should-not-exist')
        self.assertFalse((self.root/'should-not-exist').exists())

    @unittest.skipUnless(sys.platform=='win32','Windows guard')
    def test_active_backend_blocks_backup(self):
        result=subprocess.CompletedProcess([],0,b'"NetHackBridge.exe","123","Console","1","1024 K"\r\n',b'')
        with patch.object(backup.subprocess,'run',return_value=result):
            with self.assertRaisesRegex(RuntimeError,'running'):backup.stopped()

if __name__=='__main__':unittest.main()
