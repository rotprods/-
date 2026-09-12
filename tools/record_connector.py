"""Record metadata for an observed connector call. Never accept raw arguments or responses."""
import argparse
from project_control import ROOT
from tool_ledger import record
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--tool',required=True);p.add_argument('--run',required=True);p.add_argument('--status',choices=['returned','error','exception','timeout'],required=True);p.add_argument('--duration-ms',type=int,required=True);p.add_argument('--outcome',choices=['unverified','verified_success','verified_failure'],default='unverified');a=p.parse_args()
    row=record(ROOT/'telemetry/tool_calls.jsonl',tool=a.tool,run_id=a.run,status=a.status,duration_ms=a.duration_ms,task_outcome=a.outcome)
    print(row['event_id'])
