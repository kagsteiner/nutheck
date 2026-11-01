"""Verified whole-session snapshots and non-overwriting staged recovery."""
from pathlib import Path, PurePosixPath
from datetime import datetime, timezone
import argparse,csv,hashlib,io,json,os,subprocess,zipfile

ROOT=Path(__file__).resolve().parents[1]

def stopped():
    if os.name!='nt':return
    for name in ['NetHackBridge.exe','NetHack.exe']:
        result=subprocess.run(['tasklist','/FI','IMAGENAME eq '+name,'/FO','CSV','/NH'],capture_output=True,check=True,creationflags=subprocess.CREATE_NO_WINDOW)
        # Target executable names are ASCII; localized tasklist messages may use
        # the Windows OEM code page rather than Python's default text encoding.
        output=result.stdout.decode('utf-8',errors='replace')
        if any(row and row[0].lower()==name.lower() for row in csv.reader(io.StringIO(output))):
            raise RuntimeError('A NetHack backend is running. Save and exit normally first; it has not been stopped.')

def valid_name(name):
    p=PurePosixPath(name)
    if p.is_absolute() or '..' in p.parts or '\\' in name or ':' in name:raise ValueError('Unsafe archive path: '+name)
    if not p.parts or p.parts[0] not in ['NetHack','Runtime']:raise ValueError('Unexpected archive path: '+name)
    return p

def verify(path):
    with zipfile.ZipFile(path) as z:
        manifest=json.loads(z.read('manifest.json'))
        entries=manifest['files'];names=[x['path'] for x in entries]
        if len(names)!=len(set(names)) or len(z.namelist())!=len(set(z.namelist())):raise ValueError('Duplicate archive paths')
        if set(z.namelist())!=set(names)|{'manifest.json'}:raise ValueError('Archive contents differ from manifest')
        for item in entries:
            valid_name(item['path']);data=z.read(item['path'])
            if len(data)!=item['size'] or hashlib.sha256(data).hexdigest()!=item['sha256']:raise ValueError('Backup verification failed: '+item['path'])
    return manifest

def backup(reason):
    stopped();source=ROOT/'Saved/NetHack'
    if not source.is_dir():raise RuntimeError('No Saved/NetHack directory; nothing has been changed.')
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ');dest=ROOT/'Backups/NetHackSaves';dest.mkdir(parents=True,exist_ok=True)
    path=dest/(stamp+'.zip');partial=dest/(stamp+'.partial')
    manifest=dict(schema=1,created_utc=stamp,reason=reason,quiescent_backend=True,files=[])
    with zipfile.ZipFile(partial,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for folder,prefix in [(source,'NetHack'),(ROOT/'Binaries/NetHack','Runtime')]:
            for p in sorted(folder.rglob('*')):
                if p.is_symlink():raise ValueError('Refusing linked source file: '+str(p))
                if not p.is_file():continue
                data=p.read_bytes();name=prefix+'/'+p.relative_to(folder).as_posix()
                z.writestr(name,data);manifest['files'].append(dict(path=name,size=len(data),sha256=hashlib.sha256(data).hexdigest()))
        z.writestr('manifest.json',json.dumps(manifest,indent=2))
    verify(partial);stopped()
    # Ensure no source file appeared, disappeared or changed during the copy.
    current={prefix+'/'+p.relative_to(folder).as_posix():p for folder,prefix in [(source,'NetHack'),(ROOT/'Binaries/NetHack','Runtime')] for p in folder.rglob('*') if p.is_file()}
    if set(current)!={i['path'] for i in manifest['files']}:raise RuntimeError('Source file set changed during backup; partial archive retained.')
    for item in manifest['files']:
        if hashlib.sha256(current[item['path']].read_bytes()).hexdigest()!=item['sha256']:raise RuntimeError('Source changed during backup; partial archive retained.')
    partial.rename(path)
    print(json.dumps(dict(status='BACKUP_VERIFIED',archive=str(path),files=len(manifest['files']),bytes=sum(i['size'] for i in manifest['files']))))

def recover(path,destination):
    manifest=verify(path)
    if destination.exists():raise FileExistsError('Recovery destination must be new; existing files are never overwritten.')
    destination.mkdir(parents=True)
    with zipfile.ZipFile(path) as z:
        for item in manifest['files']:
            target=destination.joinpath(*valid_name(item['path']).parts);target.parent.mkdir(parents=True,exist_ok=True)
            with target.open('xb') as f:f.write(z.read(item['path']))
            if hashlib.sha256(target.read_bytes()).hexdigest()!=item['sha256']:raise ValueError('Recovery verification failed: '+str(target))
    print(json.dumps(dict(status='RECOVERY_STAGED_AND_VERIFIED',destination=str(destination),files=len(manifest['files']),live_saves_unchanged=True)))

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);sub=parser.add_subparsers(dest='command',required=True)
    p=sub.add_parser('backup');p.add_argument('--reason',default='manual')
    p=sub.add_parser('verify');p.add_argument('archive',type=Path)
    p=sub.add_parser('recover');p.add_argument('archive',type=Path);p.add_argument('destination',type=Path)
    args=parser.parse_args()
    if args.command=='backup':backup(args.reason)
    elif args.command=='verify':m=verify(args.archive);print(json.dumps(dict(status='BACKUP_VERIFIED',files=len(m['files']),archive=str(args.archive))))
    else:recover(args.archive,args.destination)
