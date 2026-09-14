import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("aaa_asset_gate", ROOT / "tools" / "aaa_asset_gate.py")
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)


def base_record():
    return {
        "asset_id": "TEST-HERO-001",
        "fidelity_before": "HERO_CANDIDATE",
        "fidelity_after": "HERO_QUALIFIED",
        "intended_exposure": {"role": "hero_closeup", "min_camera_distance_m": 0.35},
        "source_route": "MULTIVIEW_IMAGE_TO_3D",
        "provider_model_version": "provider/model@observed-version",
        "source_master_ref": "art_source/test/source_master.blend",
        "provenance": {"inputs": ["view_a", "view_b", "view_c"]},
        "look_target_refs": ["target_a", "target_b", "target_c"],
        "hero_gate": {k: "PASS" for k in MOD.HERO_CHECKS},
        "raw_reconstruction_final": False,
        "human_gate_art": "PENDING",
        "claims_aaa": False,
    }


class AAAGateTests(unittest.TestCase):
    def test_hero_candidate_can_qualify_with_evidence(self):
        result = MOD.validate(base_record())
        self.assertTrue(result["passed"], result)

    def test_proxy_polish_cannot_jump_to_hero_without_rebuild(self):
        r = base_record()
        r["fidelity_before"] = "PROXY"
        result = MOD.validate(r)
        self.assertFalse(result["passed"])
        self.assertTrue(any("source_rebuild_or_structural_upgrade" in e for e in result["errors"]))

    def test_raw_reconstruction_never_final(self):
        r = base_record()
        r["raw_reconstruction_final"] = True
        result = MOD.validate(r)
        self.assertFalse(result["passed"])

    def test_polycount_not_required_or_sufficient(self):
        r = base_record()
        r["triangle_count"] = 12_000_000
        self.assertTrue(MOD.validate(r)["passed"])
        r["hero_gate"]["silhouette"] = "FAIL"
        self.assertFalse(MOD.validate(r)["passed"])

    def test_aaa_claim_requires_human_and_final_qualification(self):
        r = base_record()
        r["claims_aaa"] = True
        result = MOD.validate(r)
        self.assertFalse(result["passed"])
        self.assertTrue(any("human_gate_art" in e for e in result["errors"]))

    def test_runtime_qualification_requires_runtime_receipts(self):
        r = base_record()
        r["fidelity_after"] = "RUNTIME_QUALIFIED"
        r["runtime_derivative_ref"] = "assets/runtime/test.glb"
        r["runtime"] = {
            "engine_import": "PASS",
            "collision": "PASS",
            "lod_or_screen_space_policy": "PASS",
            "profile_receipt": "PASS",
        }
        result = MOD.validate(r)
        self.assertTrue(result["passed"], result)


if __name__ == "__main__":
    unittest.main()
