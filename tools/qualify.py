"""Run repeatable local gates and emit task/source-bound receipts; external gates remain separate."""
from pathlib import Path
import argparse,datetime,json,re,subprocess,sys,time
from project_control import ROOT,source_digest,refresh
from tool_ledger import record,summarize
from studio import project,atomic_json
from graphify_project import build

def qualify(root,task,engine):
    project(root);atomic_json(root/'_project_intelligence/graph.json',build(root))
    gates=[('GATE-CONTROL',['-m','unittest','discover','-s','tests','-p','test_*.py','-v']),('GATE-GRAPH',['tools/studio.py','validate']),('GATE-ASSET',['tools/asset_audit.py']),('GATE-NATIVE',['tests/run_gauntlet.py','--godot',str(Path(engine).resolve())])]
    receipts=[]
    for gate,args in gates:
        start=time.monotonic();run=subprocess.run([sys.executable,*args],cwd=root,capture_output=True,text=True,timeout=300)
        text=run.stdout+run.stderr;log='evidence/'+gate.lower()+'.log';(root/log).write_text(text)
        ok=run.returncode==0
        record(root/'telemetry/tool_calls.jsonl',tool='qualify.'+gate,run_id=task,status='returned' if ok else 'error',duration_ms=round((time.monotonic()-start)*1000),task_outcome='verified_success' if ok else 'verified_failure')
        receipt={'gate_id':gate,'task_id':task,'passed':ok,'executed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_digest':source_digest(root),'evidence_refs':[log],'reviewer':'automated-local-runner','command':['python3',*args]}
        if gate=='GATE-CONTROL':
            match=re.search(r'Ran (\d+) tests?',text);receipt['tests_run']=int(match.group(1)) if match else None
        path='evidence/gates/'+task+'-'+gate+'.json';atomic_json(root/path,receipt);receipts.append(path)
        print(json.dumps({'gate':gate,'passed':ok,'receipt':path}),flush=True)
        if not ok:raise RuntimeError(gate+' failed: '+text[-2000:])
    atomic_json(root/'telemetry/summary.json',summarize(root/'telemetry/tool_calls.jsonl'))
    refresh(root);return receipts
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--task',required=True);p.add_argument('--godot',required=True);a=p.parse_args();qualify(ROOT,a.task,a.godot)
