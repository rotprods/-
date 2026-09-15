import importlib.util
import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "tools" / "world-compiler" / "world_compiler.py"
spec = importlib.util.spec_from_file_location("world_compiler", MODULE_PATH)
wc = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(wc)


class WorldCompilerContractTests(unittest.TestCase):
    def fixture(self):
        return {
            "schema_version": 1,
            "stable_id": "exo:test:region-001",
            "parent_id": "exo:test",
            "root_seed": "EXO-TEST-SEED-001",
            "compiler_version": "0.1.0",
            "module_versions": {"seed": "1"},
            "ruleset_versions": {"density": "0"},
            "dataset_versions": {},
            "artkit_versions": {"test": "1"},
            "manual_patchset_version": "0",
            "manual_overrides": [],
            "generation_targets": [
                "exo:test:region-001:cell-b",
                "exo:test:region-001:cell-a",
            ],
        }

    def test_same_input_is_byte_stable(self):
        a = wc.compile_manifest(self.fixture())
        b = wc.compile_manifest(json.loads(json.dumps(self.fixture())))
        self.assertEqual(wc.canonical_json(a), wc.canonical_json(b))

    def test_target_order_does_not_change_world(self):
        a = self.fixture()
        b = self.fixture()
        b["generation_targets"].reverse()
        self.assertEqual(wc.compile_manifest(a), wc.compile_manifest(b))

    def test_child_identity_changes_seed(self):
        seed_a = wc.derive_seed("root", "exo:x:a", "generation-target")
        seed_b = wc.derive_seed("root", "exo:x:b", "generation-target")
        self.assertNotEqual(seed_a, seed_b)
        self.assertEqual(len(seed_a), 64)

    def test_generator_domain_separates_seed_space(self):
        a = wc.derive_seed("root", "exo:x:a", "terrain")
        b = wc.derive_seed("root", "exo:x:a", "city")
        self.assertNotEqual(a, b)

    def test_digest_changes_on_compiler_version(self):
        a = self.fixture()
        b = self.fixture()
        b["compiler_version"] = "0.2.0"
        self.assertNotEqual(wc.compile_manifest(a)["output_digest"], wc.compile_manifest(b)["output_digest"])


if __name__ == "__main__":
    unittest.main()
