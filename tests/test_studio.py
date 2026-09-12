import copy,json,pathlib,shutil,sys,tempfile,unittest
ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'tools'))
from studio import validate,done_errors,start
from project_control import source_digest
from asset_audit import inspect_glb

class Studio(unittest.TestCase):
    def setUp(self):
        self.plan=json.loads((ROOT/'_project_intelligence/PLAN.json').read_text())
        for task in self.plan['tasks']:task['status']='planned';task['evidence']=[]
        self.plan['tasks'][0]['status']='in_progress'
    def test_complete_contract(self):self.assertEqual(validate(self.plan),[])
    def test_dependency_cycle_rejected(self):
        self.plan['tasks'][1]['depends_on']=['EXO-005'];self.assertTrue(any('cycle' in x for x in validate(self.plan)))
    def test_unknown_gate_rejected(self):
        self.plan['tasks'][0]['required_gates'].append('imaginary');self.assertTrue(any('unknown gate' in x for x in validate(self.plan)))
    def test_uncovered_goal_rejected(self):
        for t in self.plan['tasks']:t['goals']=[g for g in t['goals'] if g!='G-RELEASE']
        self.assertIn('uncovered goals',validate(self.plan))
    def test_multiple_workunits_rejected(self):
        self.plan['tasks'][1]['status']='in_progress';self.assertIn('too many active workunits',validate(self.plan))
    def test_done_without_evidence_rejected(self):
        self.plan['tasks'][0]['status']='done';self.assertTrue(any('done without evidence' in x for x in validate(self.plan)))
    def test_done_requires_all_gates(self):
        with tempfile.TemporaryDirectory() as d:self.assertTrue(any('missing required gate' in x for x in done_errors(pathlib.Path(d),self.plan,self.plan['tasks'][0])))
    def test_receipt_from_other_task_or_source_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            r=pathlib.Path(d);(r/'proof.txt').write_text('fixture')
            receipt={'gate_id':'GATE-CONTROL','task_id':'OTHER','passed':True,'source_digest':'0'*64,'executed_at':'2026-09-12','reviewer':'test','evidence_refs':['proof.txt']}
            (r/'receipt.json').write_text(json.dumps(receipt));t=copy.deepcopy(self.plan['tasks'][0]);t['evidence']=['receipt.json']
            errors=done_errors(r,self.plan,t);self.assertTrue(any('mismatch' in x for x in errors));self.assertTrue(any('stale source' in x for x in errors))
    def test_receipt_path_escape_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            t=copy.deepcopy(self.plan['tasks'][0]);t['evidence']=['../outside.json'];self.assertTrue(any('unsafe' in x for x in done_errors(pathlib.Path(d),self.plan,t)))
    def test_existing_writer_lock_rejected_without_overwrite(self):
        with tempfile.TemporaryDirectory() as d:
            r=pathlib.Path(d);(r/'_project_intelligence').mkdir();(r/'_project_intelligence/PLAN.json').write_text(json.dumps(self.plan));(r/'.tools/studio.lock').mkdir(parents=True);(r/'.tools/studio.lock/owner.json').write_text('preserve')
            with self.assertRaises(ValueError):start(r,'INFRA-005','test-run')
            self.assertEqual((r/'.tools/studio.lock/owner.json').read_text(),'preserve')
    def test_glb_truncation_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=pathlib.Path(d)/'asset.glb';p.write_bytes((ROOT/'assets/reliquary_gate.glb').read_bytes()[:100])
            with self.assertRaises(ValueError):inspect_glb(p)
    def test_real_asset_inventory(self):
        a=inspect_glb(ROOT/'assets/reliquary_gate.glb');self.assertGreater(a['indexed_or_vertex_triangles'],0);self.assertGreater(a['meshes'],0)

if __name__=='__main__':unittest.main()
