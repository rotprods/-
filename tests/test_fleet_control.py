"""Adversarial fleet checks; identity is cooperative, not authentication.

Temporary local repositories exercise real non-force Git publication races. No
provider requests or network access are made by this suite.
"""
from __future__ import annotations

import copy
from datetime import datetime, timedelta, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import struct
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import fleet_control as fleet


def claim(name="alpha", *, world="Ares IX", facet="environment", status="reserved"):
    value = {
        "id": "CLM-" + name, "owner": "agent-" + name,
        "branch": "art/" + name, "epoch": 1, "status": status,
        "role": "world", "paths": ["art_source/" + name + "/"],
        "scopes": [{"world": world, "facet": facet}],
        "project_ids": ["project-" + name], "asset_ids": ["asset-" + name],
    }
    if status == "active":
        value["ack"] = {"owner": value["owner"], "epoch": 1, "evidence_ref": "issue:123"}
    return value


def registry(*claims):
    return {"schema_version": 1, "generation": 1, "claims": list(claims)}


def request(value, action, **fields):
    return {"action": action, "expected_digest": fleet.digest(value), **fields}


def remote(project="project-alpha", *, revision=3, sequence=7, operation=None):
    return {"project_id": project, "revision": revision, "scene_sequence": sequence,
            "observed_at": datetime.now(timezone.utc).isoformat(), "active_operation_id": operation}


class FleetReservations(unittest.TestCase):
    def test_world_aliases_share_one_semantic_namespace(self):
        for a, b in (("Ares IX", "ares"), ("sylva_prime", "Sylva"),
                     ("Aurora Veil", "aurora"), ("Elysium Null", "elysium")):
            with self.subTest(a=a, b=b):
                self.assertEqual(fleet.world_id(a), fleet.world_id(b))
                with self.assertRaisesRegex(fleet.FleetError, "semantic scope"):
                    fleet.validate(registry(claim(world=a), claim("beta", world=b)))

    def test_each_exclusive_resource_conflicts_independently(self):
        first = claim()
        changes = {
            "path": ("paths", ["art_source/alpha/nested/"]),
            "remote project": ("project_ids", first["project_ids"]),
            "asset ID": ("asset_ids", first["asset_ids"]),
            "branch": ("branch", first["branch"]),
        }
        for reason, (key, value) in changes.items():
            with self.subTest(reason=reason):
                other = claim("beta", world="nacre")
                other[key] = value
                with self.assertRaisesRegex(fleet.FleetError, reason):
                    fleet.validate(registry(first, other))

    def test_semantic_parent_covers_descendants_but_not_siblings(self):
        with self.assertRaisesRegex(fleet.FleetError, "semantic scope"):
            fleet.validate(registry(claim(facet="environment"),
                                   claim("beta", facet="environment/roots")))
        fleet.validate(registry(claim(facet="environment/macro"),
                                claim("beta", facet="environment/root-kit")))

    def test_directory_boundaries_and_exact_files_do_not_overreach(self):
        self.assertFalse(fleet.overlaps("art_source/ares/", "art_source/ares2/model.glb"))
        self.assertFalse(fleet.overlaps("art_source/a.json", "art_source/a.json.backup"))
        self.assertTrue(fleet.overlaps("art_source/ares/", "art_source/ares/model.glb"))
        self.assertTrue(fleet.overlaps("art_source/a.json", "art_source/a.json"))

    def test_world_writer_cannot_reserve_global_state_or_tooling(self):
        for path in ("_project_intelligence/STATE.json", "tools/fleet_control.py", "AGENTS.md"):
            c = claim()
            c["paths"] = [path]
            with self.subTest(path=path), self.assertRaisesRegex(fleet.FleetError, "integration files"):
                fleet.validate(registry(c))

    def test_closed_tombstones_allow_replacement_but_preserve_unique_ids(self):
        for status in ("released", "abandoned"):
            old = claim(status=status)
            replacement = copy.deepcopy(old)
            replacement.update(id="CLM-new", owner="agent-new", status="reserved")
            fleet.validate(registry(old, replacement))
            replacement["id"] = old["id"]
            with self.assertRaisesRegex(fleet.FleetError, "duplicate claim ID"):
                fleet.validate(registry(old, replacement))

    def test_blocked_claim_is_not_silently_taken_over(self):
        with self.assertRaisesRegex(fleet.FleetError, "collision"):
            fleet.validate(registry(claim(status="blocked"), claim("beta")))

    def test_reserve_is_pure_and_stale_proposal_cannot_win_twice(self):
        initial = registry()
        original = copy.deepcopy(initial)
        proposal = request(initial, "reserve", claim=claim())
        updated = fleet.transition(initial, proposal)
        self.assertEqual(initial, original)
        self.assertEqual(updated["generation"], 2)
        with self.assertRaisesRegex(fleet.FleetError, "stale registry"):
            fleet.transition(updated, request(initial, "reserve", claim=claim("beta", world="nacre")))

    def test_ack_requires_matching_owner_epoch_and_evidence(self):
        initial = registry(claim())
        fields = {"claim_id": "CLM-alpha", "owner": "agent-alpha", "epoch": 1, "evidence_ref": "issue:123"}
        for key, bad in (("owner", "someone-else"), ("epoch", 2), ("epoch", True), ("evidence_ref", "")):
            with self.subTest(key=key, bad=bad), self.assertRaises(fleet.FleetError):
                fleet.transition(initial, request(initial, "ack", **{**fields, key: bad}))
        updated = fleet.transition(initial, request(initial, "ack", **fields))
        self.assertEqual(updated["claims"][0]["status"], "active")

    def test_release_reconciles_provider_and_fences_old_owner(self):
        initial = registry(claim(status="active"))
        fields = {"claim_id": "CLM-alpha", "owner": "agent-alpha", "epoch": 1, "evidence_ref": "handoff:123"}
        with self.assertRaisesRegex(fleet.FleetError, "reconcile every"):
            fleet.transition(initial, request(initial, "release", **fields))
        pending = {"project-alpha": remote(operation="in-flight-001")}
        with self.assertRaisesRegex(fleet.FleetError, "operation pending"):
            fleet.transition(initial, request(initial, "release", **fields, remote_observations=pending))
        closed = fleet.transition(initial, request(initial, "release", **fields,
                                  remote_observations={"project-alpha": remote()}))
        self.assertEqual(closed["claims"][0]["epoch"], 2)
        self.assertEqual(closed["claims"][0]["status"], "released")
        with self.assertRaisesRegex(fleet.FleetError, "fencing epoch"):
            fleet.owner_claim(closed, "CLM-alpha", "agent-alpha", 1)
        fields["epoch"] = 2
        with self.assertRaisesRegex(fleet.FleetError, "closed"):
            fleet.transition(closed, request(closed, "ack", **fields))

    def test_release_cannot_reuse_one_project_observation_for_another(self):
        c = claim(status="active")
        c["project_ids"] = ["project-alpha", "project-beta"]
        initial = registry(c)
        with self.assertRaises(fleet.FleetError):
            fleet.transition(initial, request(initial, "release", claim_id=c["id"], owner=c["owner"], epoch=1,
                evidence_ref="handoff:123", remote_observations={
                    "project-alpha": remote("project-beta"), "project-beta": remote("project-beta")}))

    def test_malformed_configuration_cannot_be_approved(self):
        bad_values = [registry(claim()), registry(claim()), registry(claim()), registry(claim())]
        bad_values[0]["generation"] = True
        bad_values[1]["claims"][0]["epoch"] = True
        bad_values[2]["claims"][0]["scopes"] = [{"world": "invented-world", "facet": "environment"}]
        bad_values[3]["claims"][0]["status"] = "complete"
        for value in bad_values:
            with self.subTest(value=value), self.assertRaises(fleet.FleetError):
                fleet.validate(value)

    def test_malformed_shapes_fail_with_a_structured_fleet_error(self):
        malformed_ack = claim(status="active")
        malformed_ack["ack"] = None
        for value in ([], None, registry(None), registry(malformed_ack)):
            with self.subTest(value=value), self.assertRaises(fleet.FleetError):
                fleet.validate(value)

    def test_boolean_schema_is_not_version_one(self):
        value = registry()
        value["schema_version"] = True
        with self.assertRaises(fleet.FleetError):
            fleet.validate(value)

    def test_active_claim_without_current_ack_is_rejected(self):
        c = claim(status="active")
        for ack in ({}, {"owner": c["owner"], "epoch": 4, "evidence_ref": "issue:123"}):
            c["ack"] = ack
            with self.assertRaisesRegex(fleet.FleetError, "acknowledgement"):
                fleet.validate(registry(c))


class FleetGuards(unittest.TestCase):
    def setUp(self):
        self.registry = registry(claim(status="active"))
        self.request = request(self.registry, "guard", claim_id="CLM-alpha", owner="agent-alpha",
                               epoch=1, branch="art/alpha", changed_paths=["art_source/alpha/model.glb"])

    def test_valid_guard_reports_only_checked_capabilities(self):
        result = fleet.guard(self.registry, self.request)
        self.assertTrue(result["passed"])
        self.assertFalse(result["provider_checked"])
        self.assertEqual(result["checked_paths"], 1)

    def test_wrong_branch_owner_epoch_or_digest_is_rejected(self):
        for key, bad in (("branch", "main"), ("owner", "another-agent"), ("epoch", 2),
                         ("expected_digest", "0" * 64)):
            with self.subTest(key=key), self.assertRaises(fleet.FleetError):
                fleet.guard(self.registry, {**self.request, key: bad})

    def test_rename_source_and_destination_both_require_scope(self):
        for paths in (["art_source/alpha/old.glb", "art_source/beta/new.glb"],
                      ["art_source/beta/old.glb", "art_source/alpha/new.glb"]):
            with self.subTest(paths=paths), self.assertRaisesRegex(fleet.FleetError, "outside claim"):
                fleet.guard(self.registry, {**self.request, "changed_paths": paths})

    def test_unsafe_paths_are_rejected_before_write(self):
        for path in ("/tmp/a", "art_source/alpha/../beta/a", "art_source//alpha/a", "art_source/alpha/./a",
                     "art_source/alpha/\\escape", "art_source/alpha/*.glb", "art_source/alpha/.git/config"):
            with self.subTest(path=path), self.assertRaises(fleet.FleetError):
                fleet.guard(self.registry, {**self.request, "changed_paths": [path]})

    def test_symlink_cannot_escape_checkout_even_inside_owned_prefix(self):
        with tempfile.TemporaryDirectory() as checkout, tempfile.TemporaryDirectory() as outside:
            root = Path(checkout)
            (root / "art_source").mkdir()
            (root / "art_source/alpha").symlink_to(outside, target_is_directory=True)
            with self.assertRaisesRegex(fleet.FleetError, "symlink escapes"):
                fleet.guard(self.registry, self.request, root)

    def test_symlink_within_checkout_cannot_alias_another_agents_scope(self):
        with tempfile.TemporaryDirectory() as checkout:
            root = Path(checkout)
            (root / "art_source/alpha").mkdir(parents=True)
            (root / "art_source/beta").mkdir()
            (root / "art_source/alpha/link").symlink_to("../beta", target_is_directory=True)
            with self.assertRaises(fleet.FleetError):
                fleet.guard(self.registry, {**self.request,
                            "changed_paths": ["art_source/alpha/link/model.glb"]}, root)

    def test_provider_guard_checks_identity_pending_work_revision_and_sequence(self):
        base = {**self.request, "remote": remote(), "expected_revision": 3, "expected_scene_sequence": 7}
        self.assertTrue(fleet.guard(self.registry, base)["provider_checked"])
        mutations = [
            {"remote": remote("project-other")}, {"remote": remote(operation="pending-123")},
            {"expected_revision": 2}, {"expected_scene_sequence": 6}, {"expected_revision": True},
            {"remote": {k: v for k, v in remote().items() if k != "active_operation_id"}},
        ]
        for mutation in mutations:
            with self.subTest(mutation=mutation), self.assertRaises(fleet.FleetError):
                fleet.guard(self.registry, {**base, **mutation})

    def test_provider_observations_expire_and_need_unambiguous_timezones(self):
        for timestamp in ((datetime.now(timezone.utc) - timedelta(minutes=6)).isoformat(),
                          (datetime.now(timezone.utc) + timedelta(minutes=1)).isoformat(),
                          datetime.now().isoformat(), "not-a-timestamp"):
            observation = {**remote(), "observed_at": timestamp}
            with self.subTest(timestamp=timestamp), self.assertRaises(fleet.FleetError):
                fleet.guard(self.registry, {**self.request, "remote": observation,
                            "expected_revision": 3, "expected_scene_sequence": 7})

    def test_malformed_pending_state_cannot_be_interpreted_as_idle(self):
        for pending in ({}, [], 0, False):
            with self.subTest(pending=pending), self.assertRaises(fleet.FleetError):
                fleet.guard(self.registry, {**self.request, "remote": remote(operation=pending),
                            "expected_revision": 3, "expected_scene_sequence": 7})


@unittest.skipUnless(shutil.which("git"), "Git unavailable: diff-derived ownership gate cannot execute")
class FleetGitGuards(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.env = {**os.environ, "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull,
                    "GIT_TERMINAL_PROMPT": "0"}
        self.git("init", "--initial-branch=art/alpha")
        self.git("config", "user.name", "Fleet guard test")
        self.git("config", "user.email", "fleet-test@example.invalid")
        for scope in ("alpha", "beta"):
            directory = self.root / "art_source" / scope
            directory.mkdir(parents=True)
            (directory / "model.glb").write_text("tracked source fixture")
        self.git("add", "art_source")
        self.git("commit", "-m", "guard base")
        self.base = self.git("rev-parse", "HEAD").strip()
        self.registry = registry(claim(status="active"))
        # Deliberately incomplete caller list and invented branch: git_guard must
        # derive the real checkout state rather than trusting either field.
        self.request = request(self.registry, "guard", claim_id="CLM-alpha", owner="agent-alpha",
                               epoch=1, branch="pretend-branch", changed_paths=[])

    def git(self, *arguments):
        result = subprocess.run(["git", "-c", "core.hooksPath=/dev/null", *arguments],
                                cwd=self.root, env=self.env, capture_output=True, text=True, timeout=15)
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout

    def test_diff_derived_guard_accepts_owned_changes_and_actual_branch(self):
        (self.root / "art_source/alpha/model.glb").write_text("updated source fixture")
        result = fleet.git_guard(self.registry, self.request, self.root, self.base)
        self.assertTrue(result["passed"])
        self.assertEqual(result["changed_paths"], ["art_source/alpha/model.glb"])
        self.assertEqual(result["base_commit"], self.base)

    def test_rename_from_outside_scope_cannot_hide_source_deletion(self):
        self.git("mv", "art_source/beta/model.glb", "art_source/alpha/moved.glb")
        with self.assertRaisesRegex(fleet.FleetError, "outside claim"):
            fleet.git_guard(self.registry, self.request, self.root, self.base)

    def test_deleted_file_outside_scope_is_detected(self):
        (self.root / "art_source/beta/model.glb").unlink()
        with self.assertRaisesRegex(fleet.FleetError, "outside claim"):
            fleet.git_guard(self.registry, self.request, self.root, self.base)

    def test_untracked_file_outside_scope_is_detected(self):
        (self.root / "art_source/beta/new.glb").write_text("untracked source fixture")
        with self.assertRaisesRegex(fleet.FleetError, "outside claim"):
            fleet.git_guard(self.registry, self.request, self.root, self.base)

    def test_actual_wrong_branch_cannot_be_hidden_by_request(self):
        self.git("switch", "-c", "art/beta")
        self.request["branch"] = "art/alpha"
        with self.assertRaisesRegex(fleet.FleetError, "wrong branch"):
            fleet.git_guard(self.registry, self.request, self.root, self.base)

    def test_valid_generated_manifest_is_allowed_with_owned_asset_changes(self):
        from project_control import refresh
        (self.root / "art_source/alpha/model.glb").write_text("updated source fixture")
        refresh(self.root)
        result = fleet.git_guard(self.registry, self.request, self.root, self.base)
        self.assertTrue(result["passed"])
        self.assertEqual(result["verified_generated_projections"], ["MANIFEST.json"])
        self.assertEqual(result["changed_paths"], ["MANIFEST.json", "art_source/alpha/model.glb"])
        self.assertEqual(result["checked_paths"], 1)

    def test_stale_or_tampered_generated_manifest_is_rejected(self):
        from project_control import refresh
        refresh(self.root)
        (self.root / "art_source/alpha/model.glb").write_text("changed after manifest generation")
        with self.assertRaisesRegex(fleet.FleetError, "manifest drift"):
            fleet.git_guard(self.registry, self.request, self.root, self.base)
        for tamper in ("hash", "algorithm", "omission"):
            refresh(self.root)
            manifest_path = self.root / "MANIFEST.json"
            manifest = json.loads(manifest_path.read_text())
            if tamper == "hash":
                manifest["files"]["art_source/alpha/model.glb"] = "0" * 64
            elif tamper == "algorithm":
                manifest["algorithm"] = "unverified"
            else:
                del manifest["files"]["art_source/beta/model.glb"]
            manifest_path.write_text(json.dumps(manifest))
            with self.subTest(tamper=tamper), self.assertRaisesRegex(fleet.FleetError, "manifest drift"):
                fleet.git_guard(self.registry, self.request, self.root, self.base)

    def test_valid_generated_manifest_cannot_cover_an_unowned_global_change(self):
        from project_control import refresh
        intelligence = self.root / "_project_intelligence"
        intelligence.mkdir()
        (intelligence / "STATE.json").write_text(json.dumps({"unauthorized_global_change": True}))
        (self.root / "art_source/alpha/model.glb").write_text("owned change plus unowned global change")
        refresh(self.root)
        with self.assertRaisesRegex(fleet.FleetError, "outside claim: _project_intelligence/STATE.json"):
            fleet.git_guard(self.registry, self.request, self.root, self.base)


class FleetDeliveries(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        # Deliberately a transport fixture, not a claim of Blender editability.
        (self.root / "source.blend").write_bytes(b"source fixture for transport hashes")
        self.write_glb({"asset": {"version": "2.0"}, "meshes": [{"primitives": []}]})
        (self.root / "engine.log").write_text("fixture receipt evidence; not an actual engine execution")
        self.receipt = {"passed": True, "artifact_sha256": self.sha("model.glb"),
                        "executed_at": "2026-09-12T19:40:00Z", "engine": "fixture-only",
                        "evidence_refs": ["engine.log"]}
        self.delivery = {"blend": self.item("source.blend"), "glb": self.item("model.glb")}
        self.save_receipt()

    def sha(self, path):
        return hashlib.sha256((self.root / path).read_bytes()).hexdigest()

    def item(self, path):
        return {"path": path, "sha256": self.sha(path)}

    def write_glb(self, document):
        chunk = json.dumps(document).encode()
        chunk += b" " * (-len(chunk) % 4)
        (self.root / "model.glb").write_bytes(struct.pack("<4sIIII", b"glTF", 2, 20 + len(chunk),
                                                        len(chunk), 0x4E4F534A) + chunk)

    def save_receipt(self):
        (self.root / "receipt.json").write_text(json.dumps(self.receipt))
        self.delivery["native_receipt"] = self.item("receipt.json")

    def test_transport_receipt_does_not_promote_artistic_or_hardware_approval(self):
        result = fleet.delivery_check(self.root, self.delivery)
        self.assertTrue(result["passed"])
        self.assertIn("human approval", result["not_claimed"])
        self.assertIn("target hardware performance", result["not_claimed"])

    def test_modified_blend_or_export_breaks_hash_binding(self):
        for kind, path in (("blend", "source.blend"), ("glb", "model.glb")):
            original = (self.root / path).read_bytes()
            (self.root / path).write_bytes(original + b"changed")
            with self.subTest(kind=kind), self.assertRaisesRegex(fleet.FleetError, "digest mismatch"):
                fleet.delivery_check(self.root, self.delivery)
            (self.root / path).write_bytes(original)

    def test_receipt_must_be_successful_and_bound_to_current_export(self):
        for key, bad in (("passed", False), ("artifact_sha256", "0" * 64), ("engine", ""), ("evidence_refs", [])):
            original = copy.deepcopy(self.receipt)
            self.receipt[key] = bad
            self.save_receipt()
            with self.subTest(key=key), self.assertRaisesRegex(fleet.FleetError, "not bound"):
                fleet.delivery_check(self.root, self.delivery)
            self.receipt = original
        self.save_receipt()

    def test_receipt_digest_and_referenced_evidence_are_required(self):
        (self.root / "receipt.json").write_text("{}")
        with self.assertRaisesRegex(fleet.FleetError, "receipt digest mismatch"):
            fleet.delivery_check(self.root, self.delivery)
        self.save_receipt()
        (self.root / "engine.log").unlink()
        with self.assertRaisesRegex(fleet.FleetError, "missing/unsafe artifact"):
            fleet.delivery_check(self.root, self.delivery)

    def test_external_glb_resource_is_rejected_even_with_current_hashes(self):
        self.write_glb({"asset": {"version": "2.0"}, "meshes": [{}], "buffers": [{"uri": "remote.bin"}]})
        self.delivery["glb"] = self.item("model.glb")
        self.receipt["artifact_sha256"] = self.sha("model.glb")
        self.save_receipt()
        with self.assertRaisesRegex(fleet.FleetError, "external resources"):
            fleet.delivery_check(self.root, self.delivery)

    def test_truncated_export_and_source_path_escape_are_rejected(self):
        (self.root / "model.glb").write_bytes(b"glTF")
        self.delivery["glb"] = self.item("model.glb")
        with self.assertRaisesRegex(fleet.FleetError, "truncated"):
            fleet.delivery_check(self.root, self.delivery)
        self.delivery["blend"]["path"] = "../source.blend"
        with self.assertRaisesRegex(fleet.FleetError, "unsafe path"):
            fleet.delivery_check(self.root, self.delivery)


class FleetPublicationRaces(unittest.TestCase):
    def test_two_processes_with_same_registry_parent_have_exactly_one_winner(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            initial = registry()
            path = root / "registry.json"
            path.write_text(json.dumps(initial))
            script = ("import json,sys; sys.path.insert(0,sys.argv[1]); import fleet_control as f; "
                      "req=json.loads(sys.stdin.readline()); "
                      "f.transact_file(sys.argv[2],req)")
            processes = [subprocess.Popen([sys.executable, "-c", script, str(ROOT / "tools"), str(path)],
                         stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                         for _ in range(2)]
            try:
                for index, proc in enumerate(processes):
                    value = claim("race-" + str(index), world="ares" if index == 0 else "nacre")
                    proc.stdin.write(json.dumps(request(initial, "reserve", claim=value)) + "\n")
                    proc.stdin.flush()
                results = [proc.communicate(timeout=15) for proc in processes]
                codes = [proc.returncode for proc in processes]
                self.assertEqual(sorted(codes), [0, 1], results)
                stored = json.loads(path.read_text())
                fleet.validate(stored)
                self.assertEqual(stored["generation"], 2)
                self.assertEqual(len(stored["claims"]), 1)
                self.assertFalse((root / ".tools/fleet-transaction.lock").exists())
                losing_error = results[codes.index(1)][1]
                self.assertTrue("stale registry" in losing_error or "transaction already active" in losing_error,
                                losing_error)
            finally:
                for proc in processes:
                    if proc.poll() is None:
                        proc.kill()
                        proc.communicate()

    def test_existing_transaction_lock_is_preserved(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "registry.json"
            initial = registry()
            path.write_text(json.dumps(initial))
            lock = root / ".tools/fleet-transaction.lock"
            lock.mkdir(parents=True)
            (lock / "owner.json").write_text("preserve existing writer")
            with self.assertRaisesRegex(fleet.FleetError, "already active"):
                fleet.transact_file(path, request(initial, "reserve", claim=claim()))
            self.assertEqual(json.loads(path.read_text()), initial)
            self.assertEqual((lock / "owner.json").read_text(), "preserve existing writer")

    @unittest.skipUnless(shutil.which("git"), "Git unavailable: actual non-force race gate cannot execute")
    def test_real_git_rejects_second_sibling_commit_without_force(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            env = {**os.environ, "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull,
                   "GIT_TERMINAL_PROMPT": "0"}

            def git(cwd, *arguments, check=True):
                result = subprocess.run(["git", "-c", "core.hooksPath=/dev/null", *arguments],
                                        cwd=cwd, env=env, capture_output=True, text=True, timeout=15)
                if check:
                    self.assertEqual(result.returncode, 0, result.stderr)
                return result

            remote_repo = root / "remote.git"
            a, b = root / "writer-a", root / "writer-b"
            git(root, "init", "--bare", "--initial-branch=main", str(remote_repo))
            git(root, "clone", str(remote_repo), str(a))
            for config in (("user.name", "Fleet test"), ("user.email", "fleet-test@example.invalid")):
                git(a, "config", *config)
            (a / "registry.json").write_text(json.dumps(registry()))
            git(a, "add", "registry.json")
            git(a, "commit", "-m", "initial registry")
            git(a, "push", "origin", "main")
            parent = git(a, "rev-parse", "HEAD").stdout.strip()
            git(root, "clone", str(remote_repo), str(b))
            for config in (("user.name", "Fleet test"), ("user.email", "fleet-test@example.invalid")):
                git(b, "config", *config)
            heads = []
            for index, writer in enumerate((a, b)):
                value = registry(claim("writer-" + str(index), world="ares" if index == 0 else "nacre"))
                value["generation"] = 2
                (writer / "registry.json").write_text(json.dumps(value))
                git(writer, "add", "registry.json")
                git(writer, "commit", "-m", "independent reservation")
                self.assertEqual(git(writer, "rev-parse", "HEAD^").stdout.strip(), parent)
                heads.append(git(writer, "rev-parse", "HEAD").stdout.strip())
            self.assertNotEqual(heads[0], heads[1])
            git(a, "push", "origin", "main")
            rejected = git(b, "push", "origin", "main", check=False)
            self.assertNotEqual(rejected.returncode, 0)
            self.assertIn("rejected", rejected.stderr.lower())
            self.assertEqual(git(remote_repo, "rev-parse", "refs/heads/main").stdout.strip(), heads[0])
            stored = json.loads(git(remote_repo, "show", "main:registry.json").stdout)
            self.assertEqual(stored["claims"][0]["id"], "CLM-writer-0")


if __name__ == "__main__":
    unittest.main()
