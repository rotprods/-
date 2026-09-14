#!/usr/bin/env python3
"""Validate the Pelagos rev44 external runtime handoff manifest.

Stdlib-only by design so a cold checkout can run it before Godot import.
This validates the art/runtime boundary contract; it does not prove GLB node presence,
Godot collision, gameplay interaction, persistence migration, LOD/HLOD or performance.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

EXPECTED = {
    "cultural_families": 30,
    "machinery_families": 9,
    "machinery_socket_groups": 9,
    "sessile_families": 9,
    "damage_families": 8,
    "total_stateful_or_semantic_family_groups": 56,
}

CULTURAL_STATES_001 = {"pristine", "used", "damaged", "abandoned"}
CULTURAL_STATES_002_003 = {"pristine", "used", "damaged_repaired", "abandoned"}
SESSILE_STATES = {"colonizing", "mature", "disturbed_recovering", "senescent"}
DAMAGE_STATES = {"stressed", "damaged", "field_repaired", "abandoned"}


def fail(errors: list[str], msg: str) -> None:
    errors.append(msg)


def required_str(d: dict, key: str, ctx: str, errors: list[str]) -> str:
    v = d.get(key)
    if not isinstance(v, str) or not v:
        fail(errors, f"{ctx}: {key} must be a non-empty string")
        return ""
    return v


def validate_stateful(
    rows: list,
    ctx: str,
    expected_states_for,
    errors: list[str],
) -> set[str]:
    ids: set[str] = set()
    for i, row in enumerate(rows):
        p = f"{ctx}[{i}]"
        if not isinstance(row, dict):
            fail(errors, f"{p}: record must be an object")
            continue
        aid = required_str(row, "asset_id", p, errors)
        if aid in ids:
            fail(errors, f"{p}: duplicate asset_id {aid}")
        ids.add(aid)
        states = row.get("states")
        if not isinstance(states, list) or not all(isinstance(s, str) for s in states):
            fail(errors, f"{p}: states must be an array of strings")
            continue
        expected = expected_states_for(row)
        if set(states) != expected:
            fail(errors, f"{p}: states {sorted(set(states))} != expected {sorted(expected)}")
        cur = row.get("current_state")
        if cur not in states:
            fail(errors, f"{p}: current_state {cur!r} not in states")
        if "state_nodes" in row:
            sn = row["state_nodes"]
            if not isinstance(sn, dict) or set(sn) != set(states):
                fail(errors, f"{p}: state_nodes keys must exactly match states")
            elif len(set(sn.values())) != len(sn):
                fail(errors, f"{p}: state_nodes values must be unique")
        elif "node_template" in row:
            t = row["node_template"]
            if not isinstance(t, str) or t.count("{STATE}") != 1:
                fail(errors, f"{p}: node_template must contain exactly one {{STATE}} token")
        else:
            fail(errors, f"{p}: missing state_nodes or node_template")
    return ids


def validate(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return [f"JSON parse failed: {exc}"]

    if data.get("schema_version") != 1:
        fail(errors, "schema_version must be 1")
    if data.get("world_id") != "PELAGOS":
        fail(errors, "world_id must be PELAGOS")
    source = data.get("source")
    if not isinstance(source, dict) or source.get("world_master_revision") != 44:
        fail(errors, "source.world_master_revision must be 44")
    target = data.get("runtime_target")
    if not isinstance(target, dict) or target.get("engine") != "Godot" or target.get("version") != "4.7.2":
        fail(errors, "runtime_target must be Godot 4.7.2")

    cultural = data.get("cultural_families")
    machinery = data.get("machinery_families")
    sessile = data.get("sessile_families")
    damage = data.get("damage_families")
    if not isinstance(cultural, list): cultural = []; fail(errors, "cultural_families must be an array")
    if not isinstance(machinery, list): machinery = []; fail(errors, "machinery_families must be an array")
    if not isinstance(sessile, list): sessile = []; fail(errors, "sessile_families must be an array")
    if not isinstance(damage, list): damage = []; fail(errors, "damage_families must be an array")

    cultural_ids = validate_stateful(
        cultural,
        "cultural_families",
        lambda r: CULTURAL_STATES_001 if r.get("claim") == "PEL/CIV/PROP-X100-001" else CULTURAL_STATES_002_003,
        errors,
    )
    sessile_ids = validate_stateful(sessile, "sessile_families", lambda _r: SESSILE_STATES, errors)
    damage_ids = validate_stateful(damage, "damage_families", lambda _r: DAMAGE_STATES, errors)

    machine_ids: set[str] = set()
    socket_ids: set[str] = set()
    socket_nodes: set[str] = set()
    for i, row in enumerate(machinery):
        p = f"machinery_families[{i}]"
        if not isinstance(row, dict):
            fail(errors, f"{p}: record must be an object")
            continue
        aid = required_str(row, "asset_id", p, errors)
        if aid in machine_ids: fail(errors, f"{p}: duplicate machinery asset_id {aid}")
        machine_ids.add(aid)
        node = required_str(row, "node", p, errors)
        sid = required_str(row, "socket_asset_id", p, errors)
        if sid in socket_ids: fail(errors, f"{p}: duplicate socket_asset_id {sid}")
        socket_ids.add(sid)
        if sid != aid + "-SOCKET": fail(errors, f"{p}: socket_asset_id must equal asset_id + '-SOCKET'")
        nodes = row.get("socket_nodes")
        if not isinstance(nodes, list) or not nodes or not all(isinstance(n, str) and n for n in nodes):
            fail(errors, f"{p}: socket_nodes must be a non-empty string array")
        else:
            for n in nodes:
                if n in socket_nodes: fail(errors, f"{p}: duplicate socket node {n}")
                socket_nodes.add(n)
        if not node: pass

    # Stable IDs must not cross semantic types.
    domains = [("cultural", cultural_ids), ("machinery", machine_ids), ("sessile", sessile_ids), ("damage", damage_ids)]
    for i, (an, aset) in enumerate(domains):
        for bn, bset in domains[i+1:]:
            overlap = aset & bset
            if overlap: fail(errors, f"stable asset IDs overlap across {an}/{bn}: {sorted(overlap)}")

    counts = data.get("counts")
    if not isinstance(counts, dict):
        fail(errors, "counts must be an object")
        counts = {}
    actual = {
        "cultural_families": len(cultural_ids),
        "machinery_families": len(machine_ids),
        "machinery_socket_groups": len(socket_ids),
        "sessile_families": len(sessile_ids),
        "damage_families": len(damage_ids),
        "total_stateful_or_semantic_family_groups": len(cultural_ids) + len(machine_ids) + len(sessile_ids) + len(damage_ids),
    }
    for k, expected in EXPECTED.items():
        if counts.get(k) != expected:
            fail(errors, f"counts.{k}={counts.get(k)!r}, expected {expected}")
        if actual[k] != expected:
            fail(errors, f"actual {k}={actual[k]}, expected {expected}")

    return errors


def main(argv: list[str]) -> int:
    path = Path(argv[1]) if len(argv) > 1 else Path(__file__).with_name("pelagos_runtime_manifest.rev44.json")
    errors = validate(path)
    if errors:
        print("PELAGOS_RUNTIME_MANIFEST_FAIL")
        for e in errors:
            print("-", e)
        return 1
    print("PELAGOS_RUNTIME_MANIFEST_PASS")
    print("world=PELAGOS revision=44 cultural=30 machinery=9 sessile=9 damage=8 total=56")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
