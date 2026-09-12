"""Cooperative, offline fleet guard. Git main serializes published reservations.

A local successful transaction is a proposal until its normal Git ref update and
readback succeed. This module neither authenticates agents nor controls providers.
"""
from __future__ import annotations

import argparse
import copy
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = "ops/fleet/registry.json"
HELD = {"reserved", "active", "blocked"}
STATES = HELD | {"released", "abandoned"}
WORLD_NAMES = {
    "terra": "terra", "ares": "ares", "ares-ix": "ares",
    "pelagos": "pelagos", "umbra": "umbra", "sylva": "sylva",
    "sylva-prime": "sylva", "khepri": "khepri", "nacre": "nacre",
    "vanta": "vanta", "aurora": "aurora", "aurora-veil": "aurora",
    "leviathan": "leviathan", "elysium": "elysium",
    "elysium-null": "elysium", "origin": "origin", "studio": "studio",
}
TOKEN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:@/-]*$")


class FleetError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise FleetError(message)


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"),
                                     ensure_ascii=False).encode()).hexdigest()


def world_id(value):
    require(isinstance(value, str), "world must be text")
    key = re.sub(r"[\s_]+", "-", value.strip().lower())
    require(key in WORLD_NAMES, "unknown world: " + value)
    return WORLD_NAMES[key]


def selector(value):
    """Exact relative file, or directory with trailing slash. No glob ambiguity."""
    require(isinstance(value, str) and bool(value), "empty path selector")
    parts = value.rstrip("/").split("/")
    require(not value.startswith("/") and not any(p in {"", ".", ".."} for p in parts)
            and not any(c in value for c in "\\*?[]:\x00\n\r\t"), "unsafe path: " + value)
    require(not any(p in {".git", ".tools", ".godot"} for p in parts), "reserved path: " + value)
    return value


def overlaps(a, b):
    return a == b or (a.endswith("/") and b.startswith(a)) or (b.endswith("/") and a.startswith(b))


def scope_key(scope):
    require(isinstance(scope, dict), "scope must be an object")
    facet = scope.get("facet")
    selector(facet)
    require(not facet.endswith("/"), "facet cannot end with slash")
    return world_id(scope.get("world")) + "/" + facet + "/"


def validate(registry):
    require(isinstance(registry, dict), "registry must be an object")
    require(type(registry.get("schema_version")) is int and registry["schema_version"] == 1, "unsupported registry schema")
    require(type(registry.get("generation")) is int and registry["generation"] >= 1, "invalid generation")
    claims = registry.get("claims")
    require(isinstance(claims, list), "claims must be a list")
    ids = set()
    for c in claims:
        require(isinstance(c, dict), "claim must be an object")
        for key in ("id", "owner", "branch"):
            require(isinstance(c.get(key), str) and TOKEN.fullmatch(c[key]), "invalid claim " + key)
        require(c["id"] not in ids, "duplicate claim ID: " + c["id"])
        ids.add(c["id"])
        require(type(c.get("epoch")) is int and c["epoch"] > 0, "invalid claim epoch")
        require(c.get("status") in STATES, "invalid claim status")
        require(c.get("role") in {"world", "integrator", "gameplay"}, "invalid claim role")
        for key in ("paths", "scopes", "project_ids", "asset_ids"):
            require(isinstance(c.get(key), list), "missing claim " + key)
        require(bool(c["paths"]) and bool(c["scopes"]), "claim needs paths and semantic scope")
        for p in c["paths"]:
            selector(p)
            if c["role"] == "world":
                require(p.startswith("art_source/") or p.startswith("production/worlds/")
                        or (p.startswith("production/claims/") and not p.endswith("/")),
                        "world claim cannot own integration files: " + p)
        keys = [scope_key(s) for s in c["scopes"]]
        require(len(set(keys)) == len(keys), "duplicate semantic scope")
        for key in ("project_ids", "asset_ids"):
            require(all(isinstance(x, str) and TOKEN.fullmatch(x) for x in c[key]), "invalid " + key)
            require(len(set(c[key])) == len(c[key]), "duplicate " + key)
        if c["status"] == "active":
            ack = c.get("ack", {})
            require(isinstance(ack, dict) and ack.get("owner") == c["owner"]
                    and type(ack.get("epoch")) is int and ack["epoch"] == c["epoch"]
                    and bool(ack.get("evidence_ref")), "active claim lacks current owner acknowledgement")
    for i, a in enumerate(claims):
        if a["status"] not in HELD:
            continue
        for b in claims[i + 1:]:
            if b["status"] not in HELD:
                continue
            conflicts = []
            if any(overlaps(x, y) for x in a["paths"] for y in b["paths"]):
                conflicts.append("path")
            if any(overlaps(scope_key(x), scope_key(y)) for x in a["scopes"] for y in b["scopes"]):
                conflicts.append("semantic scope")
            if set(a["project_ids"]) & set(b["project_ids"]):
                conflicts.append("remote project")
            if set(a["asset_ids"]) & set(b["asset_ids"]):
                conflicts.append("asset ID")
            if a["branch"] == b["branch"]:
                conflicts.append("branch")
            require(not conflicts, f"collision {a['id']} / {b['id']}: {', '.join(conflicts)}")
    return registry


def owner_claim(registry, claim_id, owner, epoch):
    validate(registry)
    claim = next((c for c in registry["claims"] if c["id"] == claim_id), None)
    require(claim is not None, "unknown claim")
    require(claim["owner"] == owner and type(epoch) is int and claim["epoch"] == epoch,
            "owner or fencing epoch mismatch")
    return claim


def transition(registry, request):
    """Pure compare-and-swap transition. Released IDs remain immutable tombstones."""
    validate(registry)
    require(isinstance(request, dict), "transition request must be an object")
    require(request.get("expected_digest") == digest(registry), "stale registry; reread main and reconcile")
    result = copy.deepcopy(registry)
    action = request.get("action")
    if action == "reserve":
        c = copy.deepcopy(request["claim"])
        require(isinstance(c, dict), "claim must be an object")
        require(c.get("status") == "reserved" and c.get("epoch") == 1 and not c.get("ack"),
                "new claims start reserved, epoch 1, without acknowledgement")
        result["claims"].append(c)
    elif action in {"ack", "release", "abandon"}:
        c = owner_claim(result, request.get("claim_id"), request.get("owner"), request.get("epoch"))
        require(c["status"] in HELD, "claim is closed; use a new claim ID")
        if action == "ack":
            require(c["status"] == "reserved", "only a reserved claim can be acknowledged")
            require(bool(request.get("evidence_ref")), "acknowledgement needs evidence")
            c["ack"] = {"owner": c["owner"], "epoch": c["epoch"], "evidence_ref": request["evidence_ref"]}
            c["status"] = "active"
        else:
            require(bool(request.get("evidence_ref")), "release needs handoff evidence")
            observations = request.get("remote_observations", {})
            require(isinstance(observations, dict), "remote observations must be an object")
            for project in c["project_ids"]:
                require(project in observations, "reconcile every owned remote before release")
                require(isinstance(observations[project], dict) and observations[project].get("project_id") == project,
                        "remote observation key/project mismatch")
                remote_guard(c, observations[project], observations[project].get("revision"),
                             observations[project].get("scene_sequence"))
            c["status"] = "released" if action == "release" else "abandoned"
            c["epoch"] += 1
            c["close_ref"] = request["evidence_ref"]
    else:
        raise FleetError("unknown transition")
    result["generation"] += 1
    return validate(result)


def remote_guard(claim, observation, revision, sequence):
    require(isinstance(observation, dict) and observation.get("project_id") in claim["project_ids"],
            "remote project not owned by claim")
    require(observation.get("observed_at") and "active_operation_id" in observation,
            "live provider observation required; registry project ID alone is not authority")
    try:
        stamp = datetime.fromisoformat(observation["observed_at"].replace("Z", "+00:00"))
        age = (datetime.now(timezone.utc) - stamp).total_seconds()
        require(0 <= age <= 300, "provider observation is stale or from the future; reread provider")
    except (ValueError, TypeError) as exc:
        raise FleetError("invalid/stale provider observation timestamp") from exc
    operation = observation["active_operation_id"]
    require(operation is None or (isinstance(operation, str) and bool(operation)), "invalid active operation ID")
    require(operation is None, "provider operation pending; reconcile its ID before another mutation")
    require(type(revision) is int and type(sequence) is int and revision >= 0 and sequence >= 0
            and type(observation.get("revision")) is int and type(observation.get("scene_sequence")) is int
            and observation["revision"] == revision and observation["scene_sequence"] == sequence,
            "remote revision/scene sequence changed")


def guard(registry, request, root=None):
    require(isinstance(request, dict), "guard request must be an object")
    require(request.get("expected_digest") == digest(registry), "stale registry; reread main")
    c = owner_claim(registry, request.get("claim_id"), request.get("owner"), request.get("epoch"))
    require(c["status"] == "active", "claim needs current owner acknowledgement")
    require(request.get("branch") == c["branch"], "wrong branch for claim")
    paths = request.get("changed_paths")
    require(isinstance(paths, list), "complete changed_paths list required (both rename endpoints)")
    for p in paths:
        selector(p)
        require(not p.endswith("/"), "changed path must be a file")
        require(any(p == s or (s.endswith("/") and p.startswith(s)) for s in c["paths"]),
                "write outside claim: " + p)
        if root is not None:
            resolved = (Path(root) / p).resolve()
            require(resolved.is_relative_to(Path(root).resolve()), "symlink escapes checkout")
            target = resolved.relative_to(Path(root).resolve()).as_posix()
            require(any(target == s or (s.endswith("/") and target.startswith(s)) for s in c["paths"]),
                    "symlink crosses claim boundary")
    if "remote" in request:
        remote_guard(c, request["remote"], request.get("expected_revision"), request.get("expected_scene_sequence"))
    return {"passed": True, "claim_id": c["id"], "epoch": c["epoch"], "registry_digest": digest(registry),
            "checked_paths": len(paths), "provider_checked": "remote" in request,
            "coverage": "Cooperative preflight only; caller must supply fresh main/provider reads. No daemon or authentication."}


def git_guard(registry, request, root, base):
    """Derive complete changes, including deletions, both rename endpoints and untracked files."""
    def git(*args):
        return subprocess.check_output(["git", *args], cwd=root)
    require(bool(base), "explicit integration base required")
    # Resolve arbitrary ref to an object ID before passing it to diff.
    sha = git("rev-parse", "--verify", "--end-of-options", base + "^{commit}").decode().strip()
    changed = git("diff", "--name-only", "--no-renames", "-z", sha, "--")
    untracked = git("ls-files", "--others", "--exclude-standard", "-z")
    paths = sorted(set(x.decode() for x in (changed + untracked).split(b"\0") if x))
    checked_paths = paths
    generated = []
    if "MANIFEST.json" in paths:
        # A world writer may regenerate the checksum projection on its own branch,
        # but cannot claim arbitrary global metadata or supply a stale manifest.
        from project_control import tracked_files
        expected = {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
                    for p in tracked_files(Path(root)) if p.name != "MANIFEST.json"}
        actual_manifest = json.loads((Path(root) / "MANIFEST.json").read_text())
        require(actual_manifest == {"algorithm": "sha256", "files": expected}, "generated manifest drift")
        checked_paths = [p for p in paths if p != "MANIFEST.json"]
        generated = ["MANIFEST.json"]
    actual = dict(request, changed_paths=checked_paths,
                  branch=git("symbolic-ref", "--short", "HEAD").decode().strip())
    receipt = guard(registry, actual, root)
    receipt.update(base_commit=sha, changed_paths=paths, verified_generated_projections=generated)
    return receipt


def safe_file(root, ref):
    selector(ref)
    path = (Path(root) / ref).resolve()
    require(path.is_relative_to(Path(root).resolve()) and path.is_file(), "missing/unsafe artifact: " + ref)
    return path


def delivery_check(root, delivery):
    """Verify recovered source/export and hash-bound test receipt, not artistic approval."""
    require(isinstance(delivery, dict), "delivery must be an object")
    hashes = {}
    for kind, extension in (("blend", ".blend"), ("glb", ".glb")):
        item = delivery.get(kind, {})
        require(isinstance(item, dict), "artifact record must be an object")
        path = safe_file(root, item.get("path"))
        require(path.suffix.lower() == extension and path.stat().st_size > 0, "wrong/empty " + kind)
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        require(actual == item.get("sha256"), "artifact digest mismatch: " + kind)
        hashes[kind] = actual
    glb = safe_file(root, delivery["glb"]["path"]).read_bytes()
    import struct
    require(len(glb) >= 20, "truncated GLB")
    magic, version, size, chunk_size, chunk_type = struct.unpack_from("<4sIIII", glb)
    require(magic == b"glTF" and version == 2 and size == len(glb) and chunk_type == 0x4E4F534A
            and chunk_size <= size - 20, "invalid GLB header")
    document = json.loads(glb[20:20 + chunk_size])
    require(isinstance(document, dict), "invalid GLB document")
    # The envelope length alone does not validate the remainder of the file.
    # Walk every chunk before trusting a hash-bound provider delivery.
    cursor = 12
    seen = set()
    while cursor < size:
        require(size - cursor >= 8, "truncated GLB chunk header")
        length, kind = struct.unpack_from("<II", glb, cursor)
        cursor += 8
        require(length % 4 == 0 and length <= size - cursor,
                "invalid GLB chunk alignment or bounds")
        if kind in {0x4E4F534A, 0x004E4942}:
            require(kind not in seen, "duplicate GLB JSON/BIN chunk")
            seen.add(kind)
        cursor += length
    require(bool(document.get("meshes")), "GLB contains no playable mesh candidate")
    require(not any("uri" in x for x in document.get("buffers", []) + document.get("images", [])),
            "GLB depends on external resources; runtime must stay offline")
    proof = delivery.get("native_receipt", {})
    require(isinstance(proof, dict), "native receipt record must be an object")
    path = safe_file(root, proof.get("path"))
    require(hashlib.sha256(path.read_bytes()).hexdigest() == proof.get("sha256"), "native receipt digest mismatch")
    receipt = json.loads(path.read_text())
    require(isinstance(receipt, dict), "native receipt must be an object")
    require(receipt.get("passed") is True and receipt.get("artifact_sha256") == hashes["glb"]
            and receipt.get("executed_at") and receipt.get("engine") and receipt.get("evidence_refs"),
            "native receipt is not bound to this exported artifact")
    require(isinstance(receipt["evidence_refs"], list)
            and all(isinstance(ref, str) and bool(ref) for ref in receipt["evidence_refs"]),
            "native evidence_refs must be a list of paths")
    for ref in receipt["evidence_refs"]:
        safe_file(root, ref)
    return {"passed": True, "stage": "candidate_recovered_with_native_receipt", "hashes": hashes,
            "not_claimed": ["AAA/AAAA+", "human approval", "target hardware performance", "campaign integration"],
            "coverage": "Artifact transport/hash/receipt checks; Blender editability and engine tests remain separate gates."}


def transact_file(path, request):
    """Local atomic CAS; mkdir lock protects two processes sharing one registry."""
    path = Path(path)
    lock = path.parent / ".tools" / "fleet-transaction.lock"
    lock.parent.mkdir(exist_ok=True)
    try:
        lock.mkdir()
    except FileExistsError as exc:
        raise FleetError("registry transaction already active; inspect before recovery") from exc
    temporary = None
    try:
        value = transition(json.loads(path.read_text()), request)
        fd, temporary = tempfile.mkstemp(prefix=".write-", dir=path.parent)
        with os.fdopen(fd, "w") as stream:
            json.dump(value, stream, indent=2, ensure_ascii=False)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        return value
    finally:
        if temporary and Path(temporary).exists():
            Path(temporary).unlink()
        lock.rmdir()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["validate", "digest", "guard", "guard-git", "transition", "delivery"])
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--registry", default=REGISTRY)
    parser.add_argument("--request", type=Path)
    parser.add_argument("--base", help="Fetched main SHA used by guard-git")
    args = parser.parse_args()
    try:
        registry = json.loads((args.root / args.registry).read_text())
        request = json.loads(args.request.read_text()) if args.request else {}
        if args.command == "validate":
            validate(registry)
            result = {"passed": True, "generation": registry["generation"], "claims": len(registry["claims"]),
                      "active_acknowledged": sum(c["status"] == "active" for c in registry["claims"])}
        elif args.command == "digest":
            result = {"digest": digest(validate(registry))}
        elif args.command == "guard":
            result = guard(registry, request, args.root)
        elif args.command == "guard-git":
            result = git_guard(registry, request, args.root, args.base)
        elif args.command == "delivery":
            result = delivery_check(args.root, request)
        else:
            result = transact_file(args.root / args.registry, request)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except (FleetError, ValueError, TypeError, KeyError, OSError, subprocess.CalledProcessError) as exc:
        print(json.dumps({"passed": False, "error": str(exc)}))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
