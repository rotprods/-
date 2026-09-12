"""Opt-in local command telemetry. Arguments and command output never enter the ledger."""
from pathlib import Path
import argparse, collections, datetime, json, subprocess, time, uuid, os

def record(path, *, tool, run_id, status, duration_ms, task_outcome='unverified'):
    if status not in {'returned','error','exception','timeout'}:
        raise ValueError('invalid status')
    if task_outcome not in {'verified_success','verified_failure','unverified'}:
        raise ValueError('invalid task outcome')
    row = dict(event_id=str(uuid.uuid4()), at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
               tool=tool, run_id=run_id, status=status, duration_ms=duration_ms,
               task_outcome=task_outcome, coverage='instrumented_call')
    path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
    # One append write; file ownership is governed by the project's single-writer contract.
    fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_APPEND,0o600)
    try: os.write(fd,(json.dumps(row,ensure_ascii=False)+'\n').encode())
    finally: os.close(fd)
    return row

def summarize(path):
    rows=[json.loads(l) for l in Path(path).read_text().splitlines() if l.strip()]
    counts=collections.Counter((r['tool'],r['status'],r.get('task_outcome','unverified')) for r in rows)
    return {'coverage':'partial; instrumented rows only; no historical total inferred',
            'recorded_calls':len(rows),'by_tool_outcome':[dict(tool=k[0],status=k[1],task_outcome=k[2],count=v) for k,v in sorted(counts.items())]}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--ledger',default='telemetry/tool_calls.jsonl');p.add_argument('--tool');p.add_argument('--run-id');p.add_argument('--summary',action='store_true');p.add_argument('command',nargs=argparse.REMAINDER);a=p.parse_args()
    if a.summary: print(json.dumps(summarize(a.ledger),indent=2));raise SystemExit(0)
    cmd=a.command[1:] if a.command[:1]==['--'] else a.command
    if not cmd or not a.tool or not a.run_id: p.error('tool, run-id and command required')
    start=time.monotonic()
    try:
        r=subprocess.run(cmd,timeout=600)
        record(a.ledger,tool=a.tool,run_id=a.run_id,status='returned' if r.returncode==0 else 'error',duration_ms=round((time.monotonic()-start)*1000))
        raise SystemExit(r.returncode)
    except subprocess.TimeoutExpired:
        record(a.ledger,tool=a.tool,run_id=a.run_id,status='timeout',duration_ms=round((time.monotonic()-start)*1000));raise SystemExit(124)
    except OSError:
        record(a.ledger,tool=a.tool,run_id=a.run_id,status='exception',duration_ms=round((time.monotonic()-start)*1000));raise
