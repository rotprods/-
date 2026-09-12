"""Acquire the exact official archive previously qualified; no package installation."""
from pathlib import Path
import argparse, hashlib, json, os, tempfile, urllib.request, zipfile

def install(destination):
    lock=json.loads(Path(__file__).with_name('engine.lock.json').read_text())
    destination=Path(destination).resolve();destination.mkdir(parents=True,exist_ok=True)
    out=destination/lock['binary']
    if out.exists():
        if hashlib.sha256(out.read_bytes()).hexdigest()!=lock['binary_sha256']: raise ValueError('existing binary differs; refusing overwrite')
        return out
    with tempfile.TemporaryDirectory() as temp:
        archive=Path(temp)/'godot.zip'
        with urllib.request.urlopen(lock['url'],timeout=90) as response, archive.open('wb') as target:
            import shutil
            shutil.copyfileobj(response,target)
        if hashlib.sha256(archive.read_bytes()).hexdigest()!=lock['archive_sha256']: raise ValueError('archive checksum mismatch')
        with zipfile.ZipFile(archive) as z:
            payload=z.read(lock['binary'])
        if hashlib.sha256(payload).hexdigest()!=lock['binary_sha256']: raise ValueError('binary checksum mismatch')
        # Extract only the exact named executable; no arbitrary archive paths.
        with out.open('xb') as f: f.write(payload)
        out.chmod(0o755)
    return out

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--destination',default='.tools');a=p.parse_args();print(install(a.destination))
