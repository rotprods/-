"""Project contract validation, bounded run ownership and generated human projections."""
from pathlib import Path
import argparse,datetime,hashlib,json,os,subprocess,sys,tempfile
from project_control import ROOT,source_digest
from aprende_lifecycle import SessionLifecycle

PLAN='_project_intelligence/PLAN.json'
def load(root):return json.loads((root/PLAN).read_text())
def atomic_json(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    fd,temp=tempfile.mkstemp(prefix='.write-',dir=path.parent)
    try:
        with os.fdopen(fd,'w') as f:json.dump(data,f,ensure_ascii=False,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
        os.replace(temp,path)
    finally:
        if Path(temp).exists():Path(temp).unlink()
def validate(plan):
    errors=[]
    groups={k:{x['id']:x for x in plan[k]} for k in ['goals','phases','gates','tasks']}
    for k,v in groups.items():
        if len(v)!=len(plan[k]):errors.append('duplicate '+k+' ID')
    goals,phases,gates,tasks=(groups[k] for k in ['goals','phases','gates','tasks'])
    if set(plan['north_star']['acceptance_goals'])!=set(goals):errors.append('North Star goal coverage mismatch')
    coverage=set();active=[]
    for id,t in tasks.items():
        if t['phase'] not in phases:errors.append('unknown phase '+id)
        if not t['acceptance'] or not t['required_gates']:errors.append('missing acceptance/gates '+id)
        if set(t['goals'])-goals.keys():errors.append('unknown goal '+id)
        coverage.update(t['goals'])
        if set(t['required_gates'])-gates.keys():errors.append('unknown gate '+id)
        if set(t['depends_on'])-tasks.keys():errors.append('unknown dependency '+id)
        if t['status'] not in {'planned','ready','in_progress','blocked','in_review','done','superseded'}:errors.append('invalid task status '+id)
        if t['status']=='in_progress':active.append(id)
        if t['status']=='done' and not t['evidence']:errors.append('done without evidence '+id)
        if t['status']=='done' and any(tasks.get(d,{}).get('status')!='done' for d in t['depends_on']):errors.append('done before dependency '+id)
    if coverage!=set(goals):errors.append('uncovered goals')
    if len(active)>plan['execution_policy']['max_parallel_workunits']:errors.append('too many active workunits')
    visiting=set();visited=set()
    def visit(id):
        if id in visiting:errors.append('dependency cycle '+id);return
        if id in visited or id not in tasks:return
        visiting.add(id)
        for dep in tasks[id]['depends_on']:visit(dep)
        visiting.remove(id);visited.add(id)
    for id in tasks:visit(id)
    return errors
def done_errors(root,plan,task):
    errors=[];receipts={};current=source_digest(root)
    for ref in task['evidence']:
        p=(root/ref).resolve()
        if not p.is_relative_to(root.resolve()) or not p.is_file():errors.append('missing/unsafe receipt '+ref);continue
        try:r=json.loads(p.read_text())
        except (ValueError,OSError):errors.append('invalid receipt '+ref);continue
        if r.get('task_id')!=task['id'] or r.get('passed') is not True:errors.append('receipt task/result mismatch '+ref)
        if r.get('source_digest')!=current:errors.append('stale source receipt '+ref)
        if not r.get('executed_at') or not r.get('reviewer') or not r.get('evidence_refs'):errors.append('incomplete receipt '+ref)
        for ev in r.get('evidence_refs',[]):
            if ev.startswith('https://'):continue
            e=(root/ev).resolve()
            if not e.is_relative_to(root.resolve()) or not e.is_file():errors.append('missing evidence '+ev)
        receipts[r.get('gate_id')]=r
    for gate in task['required_gates']:
        if gate not in receipts:errors.append('missing required gate '+gate)
    tasks={x['id']:x for x in plan['tasks']}
    for d in task['depends_on']:
        if tasks[d]['status']!='done':errors.append('unresolved dependency '+d)
    return errors
def validate_project(root):
    plan=load(root);errors=validate(plan)
    # A done task's immutable closeout verifies its own source snapshot, not all future commits.
    for task in plan['tasks']:
        if task['status']=='done':
            ref=task.get('closeout')
            if not ref or not (root/ref).is_file():errors.append('done missing closeout '+task['id'])
    return errors
def start(root,task_id,run_id):
    if not run_id or any(c not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_' for c in run_id):raise ValueError('unsafe run ID')
    plan=load(root);tasks={x['id']:x for x in plan['tasks']};task=tasks[task_id]
    problems=validate(plan)
    if problems:raise ValueError(problems)
    if task['status'] in {'done','superseded'}:raise ValueError('task is closed')
    if any(tasks[d]['status']!='done' for d in task['depends_on']):raise ValueError('dependencies are not done')
    if any(t['status']=='in_progress' and t['id']!=task_id for t in tasks.values()):raise ValueError('another task is active')
    lock=root/'.tools/studio.lock';lock.parent.mkdir(exist_ok=True)
    try:lock.mkdir()
    except FileExistsError:raise ValueError('local writer lock already exists; inspect before recovery')
    try:
        head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip()
        readset={p:hashlib.sha256((root/p).read_bytes()).hexdigest() for p in ['AGENTS.md','MEMORY.md','HANDOFF.md','_project_intelligence/STATE.json',PLAN]}
        owner={'run_id':run_id,'task_id':task_id,'base_commit':head,'read_set':readset,'started_at':datetime.datetime.now(datetime.timezone.utc).isoformat()}
        atomic_json(lock/'owner.json',owner)
        life=SessionLifecycle(root/'learning/hub');life.bootstrap('codex-root',run_id,'session-alias',run_id,'EXOVANT')
        task['status']='in_progress';atomic_json(root/PLAN,plan)
        atomic_json(root/f'_project_intelligence/runs/{run_id}/context.json',owner)
        project(root)
        from graphify_project import build
        atomic_json(root/'_project_intelligence/graph.json',build(root))
        return owner
    except Exception:
        if (lock/'owner.json').exists():(lock/'owner.json').unlink()
        lock.rmdir();raise
def finish(root,run_id,outcome,evidence,next_action,learning_ids=None):
    lock=root/'.tools/studio.lock';owner=json.loads((lock/'owner.json').read_text())
    if owner['run_id']!=run_id:raise ValueError('run does not own writer lock')
    if not next_action.strip():raise ValueError('next action required')
    plan=load(root);task=next(t for t in plan['tasks'] if t['id']==owner['task_id'])
    task['evidence']=evidence
    if outcome=='done':
        problems=done_errors(root,plan,task)
        if problems:raise ValueError(problems)
    closeout={'task_id':task['id'],'outcome':outcome,'evidence':evidence,'source_digest':source_digest(root),'next_action':next_action,'executed_at':datetime.datetime.now(datetime.timezone.utc).isoformat()}
    rel=f'_project_intelligence/runs/{run_id}/closeout.json';p=root/rel
    if p.exists() and json.loads(p.read_text())!=closeout:raise ValueError('closeout already exists')
    life=SessionLifecycle(root/'learning/hub')
    life.close('codex-root',run_id,'session-alias',run_id,learning_ids=learning_ids,handoff_ref='HANDOFF.md')
    atomic_json(p,closeout);task['status']='done' if outcome=='done' else 'blocked' if outcome=='blocked' else 'in_review';task['closeout']=rel
    atomic_json(root/PLAN,plan)
    state=json.loads((root/'_project_intelligence/STATE.json').read_text());state['next_action']=next_action;state['last_run']=rel;atomic_json(root/'_project_intelligence/STATE.json',state)
    project(root)
    from graphify_project import build
    atomic_json(root/'_project_intelligence/graph.json',build(root))
    (lock/'owner.json').unlink();lock.rmdir();return closeout
def project(root):
    p=load(root);errors=validate(p)
    if errors:raise ValueError(errors)
    lines=['# Objetivos y North Star','', '> Proyección de _project_intelligence/PLAN.json; no editar estados aquí.','',p['north_star']['statement'],'']
    for g in p['goals']:
        lines+=['## '+g['id']+' · '+g['title'],'']+['- '+x for x in g['success']]+['']
        lines+=['- '+m['id']+': '+m['target']+' ['+m['status']+']' for m in g['metrics']]+['']
    (root/'GOALS.md').write_text('\n'.join(lines)+'\n')
    lines=['# Fases, checkpoints y calendario','', '> Proyección de PLAN.json. Escenarios, no fechas comprometidas.','', '| Fase | Objetivo | Salida |','|---|---|---|']
    lines+=['| '+f['id']+' '+f['title']+' | '+f['goal']+' | '+'; '.join(f['exit_criteria'])+' |' for f in p['phases']]
    lines+=['','| Unidad | Fase | Dependencias | Estado |','|---|---|---|---|']
    lines+=['| '+t['id']+' '+t['title']+' | '+t['phase']+' | '+', '.join(t['depends_on'])+' | '+t['status']+' |' for t in p['tasks']]
    s=p['schedule'];lines+=['','## Capacidad del slice','','Base heredada: '+str(s['slice_person_hours'])+' horas-persona; no estimación de la campaña completa.','', '| Personas equivalentes | Horas productivas/semana | Semanas ideales |','|---|---|---|']
    lines+=['| '+str(n)+' | '+str(n*s['productive_hours_per_person_week'])+' | '+str(round(s['slice_person_hours']/(n*s['productive_hours_per_person_week']),1))+' |' for n in s['team_sizes']]
    lines+=['','Estos escenarios omiten esperas, dependencias no paralelizables y vacaciones. No hay equipo contratado confirmado. Reestimar con productividad observada tras EXO-007/012. Cada fase requiere sus gates antes de iniciar la expansión siguiente.']
    (root/'ROADMAP.md').write_text('\n'.join(lines)+'\n')
    return {'goals':len(p['goals']),'tasks':len(p['tasks'])}
if __name__=='__main__':
    ap=argparse.ArgumentParser();sub=ap.add_subparsers(dest='cmd',required=True)
    sub.add_parser('validate');sub.add_parser('project');sub.add_parser('status')
    a=sub.add_parser('start');a.add_argument('task');a.add_argument('--run',required=True)
    a=sub.add_parser('finish');a.add_argument('--run',required=True);a.add_argument('--outcome',choices=['checkpoint','blocked','done'],required=True);a.add_argument('--evidence',action='append',default=[]);a.add_argument('--next',required=True);a.add_argument('--learning-id',action='append',default=[])
    args=ap.parse_args()
    if args.cmd=='validate':
        errors=validate_project(ROOT);print(json.dumps({'passed':not errors,'problems':errors},indent=2));raise SystemExit(bool(errors))
    elif args.cmd=='project':print(json.dumps(project(ROOT)))
    elif args.cmd=='status':print(json.dumps({'active':[t for t in load(ROOT)['tasks'] if t['status'] in ['in_progress','blocked','in_review']]},ensure_ascii=False,indent=2))
    elif args.cmd=='start':print(json.dumps(start(ROOT,args.task,args.run),indent=2))
    elif args.cmd=='finish':print(json.dumps(finish(ROOT,args.run,args.outcome,args.evidence,args.next,args.learning_id),indent=2))
