#!/usr/bin/env python3
"""Static validator for the Pelagos rev44 Godot runtime manifest.

This gate proves manifest structure only. It does not prove native GLB import,
node resolution, collision, traversal, performance, or art quality.
"""
from __future__ import annotations

import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
MANIFEST = HERE / "runtime_manifest.json"
EXPECTED_SCHEMA = "EXOVANT.PELAGOS.GODOT_RUNTIME_EXPORT.v1"
EXPECTED_CLAIM = "CLM-PELAGOS-RUNTIME-GODOT-001"
EXPECTED_COUNTS = {
    "cultural": 30,
    "machinery": 9,
    "socket_groups": 9,
    "sessile": 9,
    "damage": 8,
    "stateful": 47,
    "families": 56,
    "required_nodes": 224,
}
VALID_COLLISION = {
    "unbound",
    "query_only_until_gameplay_binding",
    "none_or_soft_query",
    "none_or_query_until_runtime_damage_binding",
}


def fail(message: str) -> None:
    raise SystemExit(f"PELAGOS_RUNTIME_MANIFEST_FAIL: {message}")


def node_for(record: dict, state: str) -> str:
    nodes = record.get("nodes")
    if isinstance(nodes, dict):
        return nodes.get(state, "")
    pattern = record.get("node_pattern", "")
    if not isinstance(pattern, str) or "{STATE}" not in pattern:
        return ""
    return pattern.replace("{STATE}", state.upper())


def main() -> int:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if data.get("schema") != EXPECTED_SCHEMA:
        fail("schema mismatch")
    if data.get("claim") != EXPECTED_CLAIM:
        fail("claim mismatch")
    source = data.get("source", {})
    if source.get("engine") != "Godot 4.7.2" or source.get("revision") != 44:
        fail("engine/revision mismatch")
    if source.get("glb") != "res://runtime/pelagos/assets/pelagos_world_rev44.glb":
        fail("GLB path mismatch")
    if source.get("offline") is not True:
        fail("offline runtime contract missing")

    counts = data.get("counts", {})
    for key, expected in EXPECTED_COUNTS.items():
        if counts.get(key) != expected:
            fail(f"count {key}: expected {expected}, got {counts.get(key)!r}")

    domains = data.get("domains", {})
    if set(domains) != {"cultural", "machinery", "sessile", "damage"}:
        fail("domain set mismatch")
    if len(domains["cultural"]) != 30 or len(domains["machinery"]) != 9:
        fail("cultural/machinery count mismatch")
    if len(domains["sessile"]) != 9 or len(domains["damage"]) != 8:
        fail("sessile/damage count mismatch")

    asset_ids: set[str] = set()
    node_names: set[str] = set()
    stateful = 0

    for domain_name in ("cultural", "sessile", "damage"):
        for record in domains[domain_name]:
            stateful += 1
            asset_id = record.get("id")
            if not isinstance(asset_id, str) or not asset_id or asset_id in asset_ids:
                fail(f"missing/duplicate asset id {asset_id!r}")
            asset_ids.add(asset_id)
            states = record.get("states")
            current = record.get("current")
            if not isinstance(states, list) or not states or current not in states:
                fail(f"{asset_id}: state contract invalid")
            for state in states:
                node = node_for(record, state)
                if not node or node in node_names:
                    fail(f"{asset_id}: duplicate/missing state node {node!r}")
                node_names.add(node)
            if domain_name == "damage":
                target = record.get("target")
                if not isinstance(target, str) or not target or target in node_names:
                    fail(f"{asset_id}: duplicate/missing damage target {target!r}")
                node_names.add(target)
            if record.get("collision") not in VALID_COLLISION:
                fail(f"{asset_id}: invalid collision policy")

    for record in domains["machinery"]:
        asset_id = record.get("id")
        if not isinstance(asset_id, str) or not asset_id or asset_id in asset_ids:
            fail(f"missing/duplicate machinery id {asset_id!r}")
        asset_ids.add(asset_id)
        node = record.get("node")
        if not isinstance(node, str) or not node or node in node_names:
            fail(f"{asset_id}: duplicate/missing machinery node {node!r}")
        node_names.add(node)
        sockets = record.get("sockets")
        if not isinstance(sockets, list) or not sockets:
            fail(f"{asset_id}: socket group missing")
        for socket in sockets:
            if not isinstance(socket, str) or not socket or socket in node_names:
                fail(f"{asset_id}: duplicate/missing socket {socket!r}")
            node_names.add(socket)
        if not record.get("socket_id"):
            fail(f"{asset_id}: socket id missing")
        if record.get("collision") not in VALID_COLLISION:
            fail(f"{asset_id}: invalid collision policy")

    if stateful != 47 or len(asset_ids) != 56 or len(node_names) != 224:
        fail(
            f"registry invariant mismatch stateful={stateful} "
            f"families={len(asset_ids)} nodes={len(node_names)}"
        )
    if data.get("approved_interactions") != []:
        fail("interaction allowlist must remain empty until gameplay approval")
    authority = data.get("authority", {})
    if authority.get("manifest_patterns_are_explicit") is not True:
        fail("manifest pattern authority missing")
    if authority.get("prefix_inference_forbidden") is not True:
        fail("prefix inference prohibition missing")
    if authority.get("visible_mesh_collision_inference_forbidden") is not True:
        fail("visible-mesh collision prohibition missing")

    print(
        "PELAGOS_RUNTIME_MANIFEST_PASS "
        f"families={len(asset_ids)} stateful={stateful} "
        f"required_nodes={len(node_names)} revision={source['revision']}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
