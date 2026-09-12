"""Reproducible source snapshot; exclude caches, local locks, credentials and binaries of tools."""
from pathlib import Path
import hashlib,json,zipfile
from project_control import ROOT,tracked_files,check
def package(root,out):
    errors=check(root)
    if errors:raise ValueError(errors)
    out.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in tracked_files(root):
            info=zipfile.ZipInfo(str(p.relative_to(root)),date_time=(2026,1,1,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16
            z.writestr(info,p.read_bytes())
    return {'file':str(out),'bytes':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest()}
if __name__=='__main__':print(json.dumps(package(ROOT,ROOT/'.tools/EXOVANT_SOURCE.zip'),indent=2))
