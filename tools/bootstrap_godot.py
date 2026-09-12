"""Acquire the exact official archive previously qualified; no package installation."""
from pathlib import Path
import argparse, hashlib, json, os, tempfile, urllib.request, zipfile, shutil

def install(destination, lock=None, opener=urllib.request.urlopen):
    lock=lock or json.loads(Path(__file__).with_name('engine.lock.json').read_text())
    destination=Path(destination).resolve();destination.mkdir(parents=True,exist_ok=True)
    out=destination/lock['binary']
    if out.exists():
        if hashlib.sha256(out.read_bytes()).hexdigest()!=lock['binary_sha256']: raise ValueError('existing binary differs; refusing overwrite')
        return out
    with tempfile.TemporaryDirectory() as temp:
        archive=Path(temp)/'godot.zip'
        request=urllib.request.Request(lock['url'],headers={'User-Agent':'EXOVANT-Engine-Bootstrap/1.0','Accept':'application/octet-stream'})
        with opener(request,timeout=90) as response, archive.open('wb') as target:
            total=0
            while chunk:=response.read(1024*1024):
                total+=len(chunk)
                if total>lock.get('archive_size',512*1024*1024):raise ValueError('archive exceeds expected size')
                target.write(chunk)
        if 'archive_size' in lock and archive.stat().st_size!=lock['archive_size']:raise ValueError('incomplete archive')
        if hashlib.sha256(archive.read_bytes()).hexdigest()!=lock['archive_sha256']: raise ValueError('archive checksum mismatch')
        with zipfile.ZipFile(archive) as z:
            payload=z.read(lock['binary'])
        if hashlib.sha256(payload).hexdigest()!=lock['binary_sha256']: raise ValueError('binary checksum mismatch')
        # Extract only the exact named executable; no arbitrary archive paths.
        # An interrupted write cannot leave a partially installed final executable.
        fd,staging=tempfile.mkstemp(prefix='.godot-install-',dir=destination)
        try:
            with os.fdopen(fd,'wb') as f:f.write(payload);f.flush();os.fsync(f.fileno())
            os.chmod(staging,0o755)
            os.link(staging,out)  # atomic no-clobber publication on the same filesystem
        finally:os.unlink(staging)
    return out

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--destination',default='.tools');a=p.parse_args();print(install(a.destination))
