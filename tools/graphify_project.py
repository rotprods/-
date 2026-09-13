"""Deterministic projection of existing catalog and operational evidence, with stable IDs."""
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[1]
def build(root):
    data=json.loads((root/'design/EXOVANT_DATA.json').read_text());nodes=[];edges=[]
    def node(id,type,label,epistemic='fact',status='implemented',path=None,**extra):
        n=dict(id=id,type=type,label=label,epistemic=epistemic,status=status,provenance=path or '_project_intelligence/STATE.json')
        if path:n['artifact_path']=path
        n.update(extra);nodes.append(n)
    def edge(a,b,kind):edges.append(dict(id=a+'::'+kind+'::'+b,source=a,target=b,type=kind))
    node('project:exovant','project','EXOVANT 2950',status='implemented_prototype')
    node('catalog','artifact','Catálogo original',path='design/EXOVANT_DATA.json');edge('project:exovant','catalog','PLANNED_BY')
    for w in data['worlds']:
        wid='world:'+w['id'];node(wid,'world',w['name'],'proposal','planned','design/EXOVANT_DATA.json');edge('catalog',wid,'PROPOSES')
    for collection in ['quests','assets','weapons','vehicles']:
        for row in data[collection]:
            id=collection+':'+row['id'];node(id,'artifact',row.get('title',row.get('name',row['id'])),'proposal','planned','design/EXOVANT_DATA.json')
            parent='world:'+row['world'] if row.get('world') in {w['id'] for w in data['worlds']} else 'catalog'
            edge(parent,id,'PROPOSES')
    qids={q['id'] for q in data['quests']}
    for q in data['quests']:
        if q['prerequisite'] in qids:edge('quests:'+q['id'],'quests:'+q['prerequisite'],'DEPENDS_ON')
    paths=[('godot','capability','Godot nativo probado','evidence/gauntlet.json'),('mesa','capability','Render CPU llvmpipe','evidence/visual-run.log'),('blender','capability','Portal Blender editable remoto','art_source/reliquary_gate/EXOVANT_Reliquary_Gate.blend'),('native-tests','test','Pruebas de estado e integración','tests/run_gauntlet.py'),('governance','test','Controles de continuidad','tests/test_governance.py'),('hardware','decision','Cualificar host GPU antes de Unreal','docs/HARDWARE.md'),('art','decision','Aprobar kit Terra dentro del motor','docs/ART_PRODUCTION.md')]
    for id,t,label,path in paths:node(id,t,label,'decision' if t=='decision' else 'fact','locally_validated' if t=='capability' else 'implemented',path);edge('project:exovant',id,'USES' if t=='capability' else 'REQUIRES')
    edge('blender','godot','EXPORTED_TO');edge('native-tests','godot','VALIDATES');edge('mesa','hardware','CONSTRAINS')
    for p in sorted((root/'learning/hub/agents').glob('*/chats/*/events/*.json')):
        e=json.loads(p.read_text());id=e['learning_id'];node(id,'learning',e['analysis']['family_or_pattern'],status=e['status'],path=str(p.relative_to(root)));edge('project:exovant',id,'LEARNS');edge(id,'governance','CHECKED_BY')
    plan=json.loads((root/'_project_intelligence/PLAN.json').read_text())
    for g in plan['goals']:
        node(g['id'],'decision',g['title'],'decision','planned','_project_intelligence/PLAN.json');edge('project:exovant',g['id'],'AIMS_FOR')
    for t in plan['tasks']:
        node(t['id'],'workunit',t['title'],'proposal',t['status'],'_project_intelligence/PLAN.json')
        for goal in t['goals']:edge(t['id'],goal,'ADVANCES')
        for dep in t['depends_on']:edge(t['id'],dep,'DEPENDS_ON')
    fleet_path='ops/fleet/registry.json'
    if (root/fleet_path).exists():
        from fleet_control import world_id
        fleet=json.loads((root/fleet_path).read_text())
        node('fleet-registry','artifact','Reservas cooperativas de producción',status='implemented',path=fleet_path)
        edge('project:exovant','fleet-registry','COORDINATES_WITH')
        for claim in fleet['claims']:
            cid='claim:'+claim['id']
            node(cid,'workunit',claim['id']+' / '+claim['owner'],'proposal',claim['status'],fleet_path)
            edge('fleet-registry',cid,'RECORDS')
            for world in sorted({world_id(s['world']) for s in claim['scopes']}):
                if world!='studio':edge(cid,'world:'+world,'BOUNDS_WORK_ON')

    # EXOVANT-X100 V2: generated branch/claim awareness projection.
    # This adds retrieval context; Fleet remains ownership authority.
    x100_tool=root/'tools/x100_spatial.py'
    if x100_tool.exists():
        from x100_spatial import build_index, validate_index
        spatial=build_index(root)
        errors=validate_index(spatial)
        if errors:raise ValueError('invalid X100 spatial index: '+'; '.join(errors))
        spatial_rel='ops/x100/spatial-index.json';spatial_path=root/spatial_rel
        spatial_path.parent.mkdir(parents=True,exist_ok=True)
        spatial_path.write_text(json.dumps(spatial,ensure_ascii=False,indent=2)+'\n')
        node('x100-protocol','decision','EXOVANT-X100 V2 density optimizer','decision','implemented', 'docs/EXOVANT_X100_V2.md')
        edge('project:exovant','x100-protocol','USES')
        node('x100-spatial-index','artifact','X100 spatial-semantic branch/claim projection',status='implemented',path=spatial_rel,vector_length=64)
        edge('x100-protocol','x100-spatial-index','GENERATES')
        edge('x100-spatial-index','fleet-registry','DERIVES_OWNERSHIP_CONTEXT_FROM') if any(n['id']=='fleet-registry' for n in nodes) else None
        for entry in spatial['entries']:
            sid='spatial:'+entry['id']
            node(sid,'spatial_ref',entry.get('branch') or entry['id'],entry.get('epistemic','projection'),entry.get('status','unknown'),spatial_rel,world=entry.get('world'),domain=entry.get('domain'),scale=entry.get('scale'),vector=entry.get('vector'),spatial=entry.get('spatial'))
            edge('x100-spatial-index',sid,'INDEXES')
            if entry.get('world') and any(n['id']=='world:'+entry['world'] for n in nodes):edge(sid,'world:'+entry['world'],'LOCATED_IN_WORLD')
            if entry.get('claim_id') and any(n['id']=='claim:'+entry['claim_id'] for n in nodes):edge(sid,'claim:'+entry['claim_id'],'VECTORIZES')
    return {'schema_version':1,'authority':'Projection only; refer to provenance and STATE','generator':'tools/graphify_project.py','update_policy':'after meaningful change; no background global watcher','nodes':nodes,'edges':edges,'hyperedges':[]}
if __name__=='__main__':
    graph=build(ROOT);(ROOT/'_project_intelligence/graph.json').write_text(json.dumps(graph,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'nodes':len(graph['nodes']),'edges':len(graph['edges'])}))
