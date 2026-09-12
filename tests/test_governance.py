"""Adversarial continuity controls: reject invented authority, drift and duplicate writes."""
import copy, json, pathlib, sys, tempfile, unittest
ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'tools'))
from aprende_runtime import LearningHub, AprendeError, validate_event
from project_control import validate_graph, source_digest
from tool_ledger import record, summarize
from aprende_lifecycle import SessionLifecycle

class Continuity(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.root=pathlib.Path(self.temp.name)
        self.event=json.loads(next((ROOT/'learning/hub/agents').glob('*/chats/*/events/LRN-EXO-20260912-ART.json')).read_text())
        self.event.pop('_meta',None)
    def tearDown(self):self.temp.cleanup()
    def test_learning_roundtrip_retrieval(self):
        hub=LearningHub(self.root);hub.persist(self.event)
        reopened=LearningHub(self.root)
        self.assertEqual(reopened.retrieve(self.event['learning_id'])[0]['authority'],'L2-persisted')
        self.assertEqual(reopened.audit(),[])
    def test_identical_learning_is_idempotent(self):
        hub=LearningHub(self.root);a=hub.persist(self.event);b=hub.persist(self.event)
        self.assertEqual(a,b);self.assertEqual(len(list(hub.iter_events())),1)
    def test_learning_rewrite_rejected(self):
        hub=LearningHub(self.root);hub.persist(self.event);self.event['analysis']['confidence']=0.1
        with self.assertRaises(AprendeError):hub.persist(self.event)
    def test_unverified_L4_rejected(self):
        self.event['authority_after']='L4-enforced'
        with self.assertRaises(AprendeError):validate_event(self.event)
    def test_projection_drift_detected(self):
        hub=LearningHub(self.root);hub.persist(self.event);(self.root/'events.jsonl').write_text('')
        self.assertIn('events.jsonl projection drift',hub.audit())
    def test_event_digest_tampering_detected(self):
        hub=LearningHub(self.root);p=hub.persist(self.event);d=json.loads(p.read_text());d['analysis']['confidence']=0.1;p.write_text(json.dumps(d))
        self.assertTrue(any('digest mismatch' in x for x in hub.audit()))
    def test_unsafe_identity_rejected(self):
        self.event['provenance']['agent_id']='../outside'
        with self.assertRaises(AprendeError):LearningHub(self.root).persist(self.event)
    def test_dangling_graph_rejected(self):
        g=json.loads((ROOT/'_project_intelligence/graph.json').read_text());g['edges'][0]['target']='missing'
        self.assertTrue(any('dangling' in x for x in validate_graph(g)))
    def test_duplicate_node_rejected(self):
        g=json.loads((ROOT/'_project_intelligence/graph.json').read_text());g['nodes'].append(g['nodes'][0])
        self.assertIn('duplicate node IDs',validate_graph(g))
    def test_orphan_rejected(self):
        g=json.loads((ROOT/'_project_intelligence/graph.json').read_text());n=copy.deepcopy(g['nodes'][0]);n['id']='orphan';g['nodes'].append(n)
        self.assertIn('orphan nodes',validate_graph(g))
    def lifecycle(self):
        hub=LearningHub(self.root);hub.persist(self.event)
        return SessionLifecycle(self.root)
    def test_receipt_close_without_bootstrap_rejected(self):
        with self.assertRaises(AprendeError):self.lifecycle().close('agent','chat','session-alias','run')
    def test_terminal_receipt_idempotent_but_conflict_rejected(self):
        life=self.lifecycle();life.bootstrap('agent','chat','session-alias','run')
        a=life.close('agent','chat','session-alias','run',handoff_ref='HANDOFF.md')
        b=life.close('agent','chat','session-alias','run',handoff_ref='HANDOFF.md');self.assertEqual(a,b)
        with self.assertRaises(AprendeError):life.close('agent','chat','session-alias','run',handoff_ref='OTHER.md')
        self.assertEqual(life.audit_receipts(),[])
    def test_source_change_invalidates_digest(self):
        (self.root/'scripts').mkdir();p=self.root/'scripts/p.gd';p.write_text('a');before=source_digest(self.root);p.write_text('b');self.assertNotEqual(before,source_digest(self.root))
    def test_telemetry_counts_only_recorded_outcomes(self):
        p=self.root/'calls.jsonl'
        record(p,tool='example',run_id='test',status='returned',duration_ms=1)
        record(p,tool='example',run_id='test',status='error',duration_ms=2,task_outcome='verified_failure')
        s=summarize(p);self.assertEqual(s['recorded_calls'],2);self.assertEqual(len(s['by_tool_outcome']),2)
        self.assertNotIn('arguments',p.read_text());self.assertNotIn('verified_success',p.read_text())
    def test_all_twelve_learnings_recoverable(self):
        hub=LearningHub(ROOT/'learning/hub');events=list(hub.iter_events());self.assertGreaterEqual(len(events),12)
        for _,e in events:self.assertTrue(any(hit['learning_id']==e['learning_id'] for hit in hub.retrieve(e['learning_id'])))

if __name__=='__main__':unittest.main()
