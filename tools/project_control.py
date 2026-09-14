"""Small file-based COS assurance gates. No graph service or global daemon."""
from pathlib import Path
import argparse, datetime, hashlib, json, platform, shutil, subprocess, sys

ROOT=Path(__file__).resolve().parents[1]
SKIP={'.git','.godot','.tools','__pycache__'}
def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def tracked_files(root):
    return sorted(p for p in root.rglob('*') if p.is_file() and not any(x in SKIP for x in p.relative_to(root).parts) and not p.name.endswith(('.pyc','.tmp','.bak')) and not p.name.startswith('.write-'))
def source_manifest(root):
    prefixes=('scripts/','scenes/','assets/','tests/','tools/')
    return {str(p.relative_to(root)):digest(p) for p in tracked_files(root) if str(p.relative_to(root)).startswith(prefixes) or p.name=='project.godot'}
def source_digest(root):
    return hashlib.sha256(json.dumps(source_manifest(root),sort_keys=True,separators=(',',':')).encode()).hexdigest()
def validate_graph(graph):
    errors=[];nodes=graph.get('nodes',[]);ids=[n.get('id') for n in nodes]
    if len(set(ids))!=len(ids): errors.append('duplicate node IDs')
    allowed={'project','artifact','test','decision','capability','learning','world','workunit','limitation'}
    for n in nodes:
        if n.get('type') not in allowed or not n.get('provenance'): errors.append('node missing type/provenance: '+str(n.get('id')))
        if n.get('epistemic') not in {'fact','inference','decision','proposal'}:errors.append('node missing epistemic status')
    edge_ids=[];linked=set()
    for e in graph.get('edges',[]):
        edge_ids.append(e.get('id'))
        if e.get('source') not in ids or e.get('target') not in ids:errors.append('dangling edge: '+str(e.get('id')))
        linked.update([e.get('source'),e.get('target')])
    if len(set(edge_ids))!=len(edge_ids):errors.append('duplicate edge IDs')
    if set(ids)-linked:errors.append('orphan nodes')
    return errors
def validate_asset_fidelity_receipts(root):
    """Validate only receipts that opt into the canonical asset-fidelity filename contract.

    Existing historical world receipts are not retroactively reinterpreted. New owners opt in by
    persisting `asset-fidelity*.json` beneath production/receipts; those receipts then fail closed.
    """
    errors=[]
    sys.path.insert(0,str(root/'tools'))
    try:
        from aaa_asset_gate import validate
    except (ImportError, OSError) as exc:
        return ['asset fidelity validator unavailable: '+str(exc)]
    base=root/'production'/'receipts'
    if not base.exists(): return errors
    for path in sorted(base.rglob('asset-fidelity*.json')):
        try:
            result=validate(json.loads(path.read_text()))
        except (OSError,ValueError,TypeError,KeyError,json.JSONDecodeError) as exc:
            errors.append('asset fidelity receipt unreadable '+str(path.relative_to(root))+': '+str(exc));continue
        if not result.get('passed'):
            errors.append('asset fidelity receipt failed '+str(path.relative_to(root))+': '+'; '.join(result.get('errors',[])))
    return errors
def refresh(root):
    files={str(p.relative_to(root)):digest(p) for p in tracked_files(root) if p.name!='MANIFEST.json'}
    (root/'MANIFEST.json').write_text(json.dumps({'algorithm':'sha256','files':files},indent=2)+'\n')
def check(root):
    problems=[]
    for name in ['AGENTS.md','MEMORY.md','PROGRESS.md','ARCHITECTURE.md','HANDOFF.md','_project_intelligence/STATE.json','learning/README.md']:
        if not (root/name).exists():problems.append('missing '+name)
    manifest=json.loads((root/'MANIFEST.json').read_text())['files']
    actual={str(p.relative_to(root)):digest(p) for p in tracked_files(root) if p.name!='MANIFEST.json'}
    if actual!=manifest:problems.append('manifest drift: '+', '.join(sorted(k for k in actual.keys()|manifest.keys() if actual.get(k)!=manifest.get(k))[:15]))
    graph=json.loads((root/'_project_intelligence/graph.json').read_text());problems+=validate_graph(graph)
    for n in graph['nodes']:
        ref=n.get('artifact_path')
        if ref and not (root/ref).exists():problems.append('missing graph artifact '+ref)
    from graphify_project import build
    if graph != build(root):problems.append('graph projection drift')
    from studio import validate_project
    problems+=validate_project(root)
    from fleet_control import validate as validate_fleet, FleetError, REGISTRY
    try: validate_fleet(json.loads((root/REGISTRY).read_text()))
    except (FleetError,ValueError,TypeError,KeyError,OSError) as exc: problems.append('fleet registry: '+str(exc))
    sys.path.insert(0,str(root/'tools'))
    from aprende_runtime import LearningHub
    from aprende_lifecycle import SessionLifecycle
    problems+=LearningHub(root/'learning/hub').audit()
    problems+=SessionLifecycle(root/'learning/hub').audit_receipts()
    problems+=validate_asset_fidelity_receipts(root)
    data=json.loads((root/'design/EXOVANT_DATA.json').read_text())
    for collection in ['worlds','quests','weapons','vehicles','assets']:
        ids=[x['id'] for x in data[collection]]
        if len(ids)!=len(set(ids)):problems.append('duplicate catalog ID '+collection)
    gate=json.loads((root/'evidence/gauntlet.json').read_text())
    if gate.get('passed') is not True:problems.append('native gates not passed')
    if gate.get('source_digest')!=source_digest(root):problems.append('native evidence not bound to current source')
    return problems
def probe(root):
    def read(p):
        try:return Path(p).read_text().strip()
        except OSError:return None
    data={'observed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'platform':platform.platform(),
          'cgroup_cpu_max':read('/sys/fs/cgroup/cpu.max'),'cgroup_memory_max':read('/sys/fs/cgroup/memory.max'),
          'disk_free_bytes':shutil.disk_usage(root).free,'gpu_devices':[str(p) for pattern in ['dri','nvidia*'] for p in Path('/dev').glob(pattern)],
          'engine_in_path':{n:shutil.which(n) for n in ['Godot','godot','UnrealEditor','blender']},
          'interpretation':'No exposed GPU devices was observed here; rerun on target host. PATH absence does not prove no installation anywhere.'}
    (root/'evidence/hardware-probe.json').write_text(json.dumps(data,indent=2)+'\n');return data
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['check','refresh','probe','source-digest']);a=p.parse_args()
    if a.command=='refresh':refresh(ROOT);print('Manifest refreshed')
    elif a.command=='probe':print(json.dumps(probe(ROOT),indent=2))
    elif a.command=='source-digest':print(source_digest(ROOT))
    else:
        errors=check(ROOT)
        print(json.dumps({'passed':not errors,'problems':errors},indent=2));raise SystemExit(bool(errors))
