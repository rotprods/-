import json, pathlib, tempfile, unittest, sys
ROOT=pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'ops/x100'))
from x100_director import *
CFG={"candidate_weights":{"marginal_gain":4.0,"critical_path":1.2,"dependency_unlock":1.1,"player_visibility":.9,"reuse_value":1.0,"art_importance":1.0,"systemic_yield":1.2,"gameplay_value":1.0,"evidence_confidence":.6,"image_grounding_bonus":.5,"collision_risk":2.5,"unresolved_dependency":3.0,"slop_risk":2.0,"technical_cost":.5},"dimensions":{"macro_world":.08,"meso_architecture":.08,"micro_assets":.07,"ecology":.07,"civilization":.08,"gameplay":.08,"material_causality":.08,"variation":.07,"temporal_states":.06,"storytelling":.08,"audiovisual_language":.05,"optimization":.07,"reusability":.06,"qa":.07},"critical_dimensions":["macro_world","meso_architecture","micro_assets","gameplay","material_causality","optimization","qa"],"gradient":{"epsilon":.025,"bottleneck_lambda":1.5,"bottleneck_power":2.0}}
def receipt(world='nacre', maturity='locally_validated'):
 return {"receipt_id":"R1","world_id":world,"claim_id":"C1","branch":"art/world-nacre","evidence":[{"dimension":"macro_world","cell":"regional_layout","maturity":maturity,"evidence_refs":["qa.json"]},{"dimension":"qa","cell":"geometry_uv_material","maturity":"empirically_qualified","evidence_refs":["qa.json"]}]}
class T(unittest.TestCase):
 def test_84_cells(self):
  w=empty_world('n');self.assertEqual(sum(len(x) for x in w['cells'].values()),84)
 def test_unknown_critical_blocks_score(self):
  worlds=aggregate(['nacre'],[receipt()]);s=summarize(worlds,CFG)[0];self.assertEqual(s['strict_score_pct'],0);self.assertGreater(s['known_evidence_geomean_pct'],0)
 def test_stronger_receipt_wins_without_double_count(self):
  a=receipt();b=receipt(maturity='empirically_qualified');b['receipt_id']='R2';w=aggregate(['nacre'],[a,b])['nacre'];c=w['cells']['macro_world']['regional_layout'];self.assertEqual(c['maturity'],'empirically_qualified');self.assertEqual(len(c['receipts']),2)
 def test_invalid_cell_rejected(self):
  r=receipt();r['evidence'][0]['cell']='invented'
  with self.assertRaises(DirectorError):validate_receipt(r)
 def test_nonunknown_requires_receipt_ref(self):
  r=receipt();r['evidence'][0]['evidence_refs']=[]
  with self.assertRaises(DirectorError):validate_receipt(r)
 def test_queue_does_not_claim(self):
  worlds=aggregate(['nacre'],[]);s=summarize(worlds,CFG);q=candidate_queue(s,{"claims":[{"id":"C","owner":"A","status":"active","scopes":[{"world":"nacre","facet":"art/macro-foundation"}]}]});self.assertTrue(q[0]['requires_fleet_preflight']);self.assertEqual(q[0]['existing_claims'][0]['claim_id'],'C')
 def test_unknown_cells_are_visible_even_with_known_progress(self):
  s=summarize(aggregate(['nacre'],[receipt()]),CFG)[0];self.assertGreater(s['unknown_cells'],0);self.assertGreater(len(s['bottleneck_cells']),0)
 def test_evidence_coverage_is_not_world_completion(self):
  s=summarize(aggregate(['nacre'],[receipt()]),CFG)[0];self.assertGreater(s['evidence_cell_coverage_pct'],0);self.assertEqual(s['strict_score_pct'],0)
 def test_portfolio_penalizes_claim_collision_hard(self):
  worlds=aggregate(['nacre'],[receipt()]);a={"id":"safe","world_id":"nacre","dimension":"material_causality","expected_delta":.2,"critical_path":1,"reuse_value":1};b=dict(a,id="collision",claimed_by_other=True);self.assertEqual(rank_portfolio([b,a],worlds,CFG)[0]['id'],'safe')
 def test_portfolio_can_favor_image_grounded_hero_work(self):
  worlds=aggregate(['nacre'],[receipt()]);a={"id":"look","world_id":"nacre","dimension":"material_causality","expected_delta":.2,"art_importance":1,"image_grounding_bonus":1,"systemic_yield":.7};b={"id":"noise","world_id":"nacre","dimension":"material_causality","expected_delta":.2,"slop_risk":1};self.assertEqual(rank_portfolio([b,a],worlds,CFG)[0]['id'],'look')
if __name__=='__main__':unittest.main()
