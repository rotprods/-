"""Deterministic projection of existing catalog and operational evidence, with stable IDs."""
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[1]
def build(root):
    data=json.loads((root/'design/EXOVANT_DATA.json').read_text());nodes=[];edges=[]
    def node(id,type,label,epistemic='fact',status='implemented',path=None):
        n=dict(id=id,type=type,label=label,epistemic=epistemic,status=status,provenance=path or '_project_intelligence/STATE.json')
        if path:n['artifact_path']=path
        nodes.append(n)
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
    for n,line in enumerate((root/'_project_intelligence/BACKLOG.md').read_text().splitlines()):
        if not line.startswith('| EXO-'):continue
        cells=[x.strip() for x in line.split('|')];id=cells[1];node(id,'workunit',cells[2],'proposal','planned','_project_intelligence/BACKLOG.md');edge('project:exovant',id,'NEXT_FRONTIER')
    edge('EXO-005','EXO-004','DEPENDS_ON');edge('EXO-007','EXO-006','DEPENDS_ON');edge('EXO-008','EXO-005','DEPENDS_ON');edge('EXO-012','EXO-007','DEPENDS_ON');edge('EXO-013','EXO-012','DEPENDS_ON')
    return {'schema_version':1,'authority':'Projection only; refer to provenance and STATE','generator':'tools/graphify_project.py','update_policy':'after meaningful change; no background global watcher','nodes':nodes,'edges':edges,'hyperedges':[]}
if __name__=='__main__':
    graph=build(ROOT);(ROOT/'_project_intelligence/graph.json').write_text(json.dumps(graph,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'nodes':len(graph['nodes']),'edges':len(graph['edges'])}))
