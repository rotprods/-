"""Exercise recovery from remote source in a new directory, without an import cache."""
from pathlib import Path
import argparse,datetime,json,subprocess,sys,tempfile
from project_control import ROOT
def restore(engine,ref=None):
    with tempfile.TemporaryDirectory(prefix='exovant-restore-') as folder:
        r=Path(folder)/'game'
        subprocess.run(['git','-c','core.hooksPath=/dev/null','clone','--no-recurse-submodules','https://github.com/rotprods/-.git',str(r)],check=True,capture_output=True,text=True,timeout=120)
        if ref:subprocess.run(['git','checkout','--detach',ref],cwd=r,check=True,capture_output=True,text=True)
        sha=subprocess.check_output(['git','rev-parse','HEAD'],cwd=r,text=True).strip()
        stages=[]
        for name,args in [('integrity',['tools/project_control.py','check']),('control',['-m','unittest','discover','-s','tests','-p','test_*.py']),('native',['tests/run_gauntlet.py','--godot',str(Path(engine).resolve())])]:
            run=subprocess.run([sys.executable,*args],cwd=r,capture_output=True,text=True,timeout=240)
            stages.append({'stage':name,'passed':run.returncode==0,'exit_code':run.returncode})
            if run.returncode:raise RuntimeError(name+' failed: '+(run.stdout+run.stderr)[-3000:])
        return {'passed':True,'commit':sha,'stages':stages,'executed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'fresh public clone, full manifest including binary hashes, no .godot cache; engine path explicitly supplied','native_receipt':json.loads((r/'evidence/gauntlet.json').read_text())}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--godot',required=True);p.add_argument('--ref');a=p.parse_args();d=restore(a.godot,a.ref);(ROOT/'evidence/remote-restore.json').write_text(json.dumps(d,indent=2)+'\n');print(json.dumps(d,indent=2))
