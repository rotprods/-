import json, pathlib, sys, tempfile, unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"tools"))
from x100_control import world_completeness,effective_weights,gradient_pressure,rank_candidates,family_grade,validate_family,validate_config
from x100_spatial import build_index,validate_index,nearest,spatial_overlap

CFG={
 "protocol_id":"EXOVANT-X100-V2",
 "dimensions":{"macro_world":.08,"meso_architecture":.08,"micro_assets":.07,"ecology":.07,"civilization":.08,"gameplay":.08,"material_causality":.08,"variation":.07,"temporal_states":.06,"storytelling":.08,"audiovisual_language":.05,"optimization":.07,"reusability":.06,"qa":.07},
 "critical_dimensions":["macro_world","meso_architecture","micro_assets","gameplay","material_causality","optimization","qa"],
 "thresholds":{"blockout":[0,15],"playable_foundation":[15,35],"production_world":[35,65],"dense_aaa_world":[65,85],"aaaa_candidate":[85,95],"release_candidate":[95,100]},
 "gradient":{"epsilon":.025,"bottleneck_lambda":1.5,"bottleneck_power":2.0},
 "candidate_weights":{"marginal_gain":4.0,"critical_path":1.2,"dependency_unlock":1.1,"player_visibility":.9,"reuse_value":1.0,"art_importance":1.0,"systemic_yield":1.2,"gameplay_value":1.0,"evidence_confidence":.6,"image_grounding_bonus":.5,"collision_risk":2.5,"unresolved_dependency":3.0,"slop_risk":2.0,"technical_cost":.5},
 "scale_levels":["L0","L1","L2","L3","L4","L5"],
 "hero_support_systemic_target":{"hero":.05,"support":.20,"systemic":.75},
 "kit_thresholds":{"poor_max":9,"acceptable_max":29,"strong_max":99,"production_grade_min":100},
}

def cov(v=.5):return {k:v for k in CFG["dimensions"]}

class X100(unittest.TestCase):
    def test_config(self):self.assertTrue(validate_config(CFG))
    def test_multiplicative_zero_critical_blocks_world(self):
        c=cov(.9);c["qa"]=0;self.assertEqual(world_completeness(c,CFG),0)
    def test_balanced_world_retains_value(self):self.assertAlmostEqual(world_completeness(cov(.8),CFG),.8,places=8)
    def test_gradient_prioritizes_bottleneck(self):
        c=cov(.8);c["micro_assets"]=.1;p=gradient_pressure(c,CFG);self.assertEqual(max(p,key=p.get),"micro_assets");self.assertGreater(effective_weights(c,CFG)["micro_assets"],CFG["dimensions"]["micro_assets"])
    def test_rank_penalizes_collision_even_when_visible(self):
        c=cov(.4);rows=[{"id":"safe","dimension":"micro_assets","expected_delta":.1,"critical_path":.8,"systemic_yield":1,"reuse_value":1,"evidence_confidence":1},{"id":"collision","dimension":"micro_assets","expected_delta":.1,"critical_path":1,"systemic_yield":1,"reuse_value":1,"evidence_confidence":1,"collision_risk":1,"claimed_by_other":True}];self.assertEqual(rank_candidates(rows,c,CFG)[0]["id"],"safe")
    def test_combinatorial_kit(self):
        fam={"size_variants":3,"regional_variants":2,"material_states":4,"temporal_states":4,"gameplay_states":3,"configurations":2};self.assertEqual(family_grade(fam,CFG)["grade"],"production_grade")
    def test_raw_ai_mesh_never_family_complete(self):
        fam={k:True for k in ("dimensions_validated","player_scale_validated","silhouette_pass","manufacturing_logic_pass","uv0","material_slots","pivot","transforms_clean","collision_strategy","gameplay_clearance","lod_strategy","variants","state_variants","optimization","engine_import","visual_qa","technical_qa","receipt","source_persisted","export_persisted","claim_handoff_updated")};fam.update({"stable_id":"A","semantic_purpose":"x","raw_ai_mesh_final":True});self.assertIn("raw_ai_mesh_final_forbidden",validate_family(fam))
    def test_spatial_index_does_not_invent_coordinates(self):
        with tempfile.TemporaryDirectory() as d:
            r=pathlib.Path(d);(r/"design").mkdir();(r/"ops/fleet").mkdir(parents=True);(r/"design/EXOVANT_DATA.json").write_text(json.dumps({"worlds":[{"id":"terra"},{"id":"nacre"}]}));(r/"ops/fleet/registry.json").write_text(json.dumps({"claims":[{"id":"C","branch":"art/world-nacre","owner":"A","epoch":1,"status":"active","scopes":[{"world":"nacre","facet":"art/macro-foundation"}],"paths":[],"asset_ids":[],"project_ids":[]}]}));idx=build_index(r,branch_snapshot=["art/world-nacre","qa/nacre-test","main"]);self.assertEqual(validate_index(idx),[]);claim=next(e for e in idx["entries"] if e["id"]=="claim:C");self.assertIsNone(claim["spatial"]);self.assertEqual(claim["vector"][40:47],[0.0]*7)
    def test_nearest_is_deterministic(self):
        with tempfile.TemporaryDirectory() as d:
            r=pathlib.Path(d);(r/"design").mkdir();(r/"ops/fleet").mkdir(parents=True);(r/"design/EXOVANT_DATA.json").write_text(json.dumps({"worlds":[{"id":"terra"},{"id":"nacre"}]}));claims=[]
            for cid,world in [("A","nacre"),("B","nacre"),("C","terra")]:claims.append({"id":cid,"branch":"b"+cid,"owner":"o","epoch":1,"status":"active","scopes":[{"world":world,"facet":"art/macro-foundation"}],"paths":[],"asset_ids":[],"project_ids":[]})
            (r/"ops/fleet/registry.json").write_text(json.dumps({"claims":claims}));idx=build_index(r,branch_snapshot=[]);n=nearest(idx,"claim:A",2);self.assertEqual(n[0]["id"],"claim:B")
    def test_spatial_overlap_requires_evidence(self):self.assertIsNone(spatial_overlap({"spatial":None},{"spatial":{"center_m":[0,0,0],"extent_m":[1,1,1]}}))

if __name__=="__main__":unittest.main()
