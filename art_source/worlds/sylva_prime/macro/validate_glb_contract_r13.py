#!/usr/bin/env python3
"""SYLVA PRIME macro GLB contract validator — R13 streaming-aware.

Builds on:
- R11 transport envelope hardening (all chunks walked, 4-byte alignment, unique JSON/BIN,
  no external resources);
- R10 route-collision closed-manifold topology validation.

R13 updates scene semantics for the streamed terrain:
- 16 render terrain tiles + 16 collision terrain tiles;
- monolithic R6 terrain nodes are forbidden legacy;
- 16 L3 cell nodes + R12 terrain-streaming metadata + R13 object-membership metadata;
- 27 total `SYLVA_COL_*` nodes (16 terrain + 11 pre-existing macro collisions).

This does not validate native residency/prefetch behavior, art direction or GPU cost.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

import validate_glb_contract_r10 as r10
import validate_glb_contract_r11 as r11

CONTRACT = "CLM-SYLVA-MACRO-001/R13"
TERRAIN_RENDER = {f"SYLVA_TERRAIN_L3_X{x}Y{y}" for x in range(4) for y in range(4)}
TERRAIN_COLLISION = {f"SYLVA_COL_TERRAIN_L3_X{x}Y{y}" for x in range(4) for y in range(4)}
STREAM_CELLS = {f"SYLVA_STREAM_L3_X{x}Y{y}" for x in range(4) for y in range(4)}
FORBIDDEN_MONOLITHIC = {
    "SYLVA_TERRAIN_Macro12km_PROPOSAL",
    "SYLVA_COL_TERRAIN_Macro12km_LowRes_PROPOSAL",
}

EXPECTED_EXACT = {
    "SYLVA_META_RootKitIntegration",
    "SYLVA_META_RootKitSocketConsumerContract",
    "SYLVA_META_NavigationRouteContract",
    "SYLVA_META_VESPER_ThreeTerraceLayout",
    "SYLVA_META_TerrainStreamingR12",
    "SYLVA_META_StreamMembershipR13",
    "SYLVA_STREAM_REGION_PUERTO_INJERTO",
    "SYLVA_STREAM_REGION_BOSQUE_FRASES",
    "SYLVA_STREAM_REGION_CAMARA_VESPER",
    "SYLVA_COL_PUERTO_Deck",
    "SYLVA_COL_BOSQUE_CentralPad",
    "SYLVA_COL_ROUTE_00",
    "SYLVA_COL_ROUTE_01",
    "SYLVA_COL_ROUTE_02",
    "SYLVA_COL_ROUTE_03",
    "SYLVA_VESPER_Terrace_00_ENTRY",
    "SYLVA_VESPER_Terrace_01_MIDDLE",
    "SYLVA_VESPER_Terrace_02_UPPER",
    "SYLVA_VESPER_TerraceConnector_00",
    "SYLVA_VESPER_TerraceConnector_01",
    "SYLVA_COL_VESPER_Terrace_00_ENTRY",
    "SYLVA_COL_VESPER_Terrace_01_MIDDLE",
    "SYLVA_COL_VESPER_Terrace_02_UPPER",
    "SYLVA_COL_VESPER_Connector_00",
    "SYLVA_COL_VESPER_Connector_01",
    *TERRAIN_RENDER,
    *TERRAIN_COLLISION,
    *STREAM_CELLS,
}

EXPECTED_PREFIX_COUNTS = {
    "SYLVA_STREAM_L3_": 16,
    "SYLVA_STREAM_REGION_": 3,
    "SYLVA_SOCKET_": 8,
    "SYLVA_COL_": 27,
    "SYLVA_COL_TERRAIN_L3_": 16,
    "SYLVA_TERRAIN_L3_": 16,
    "SYLVA_TRAV_PathGuide_": 4,
    "SYLVA_ROOT_PRIMARY_": 6,
    "SYLVA_ROOT_SECONDARY_": 8,
    "SYLVA_VESPER_TerraceConnector_": 2,
}


def validate_document(document: dict, meta: dict, blob: bytes, strict_namespace: bool = True) -> dict:
    nodes = document.get("nodes") or []
    named_nodes = [n for n in nodes if isinstance(n, dict) and isinstance(n.get("name"), str)]
    names = [n["name"] for n in named_nodes]
    name_set = set(names)
    counts = Counter(names)

    missing = sorted(EXPECTED_EXACT - name_set)
    duplicates = sorted(name for name, count in counts.items() if count > 1)
    prefix_counts = {prefix: sum(name.startswith(prefix) for name in names) for prefix in EXPECTED_PREFIX_COUNTS}
    bad_prefix_counts = {
        prefix: {"expected": expected, "actual": prefix_counts[prefix]}
        for prefix, expected in EXPECTED_PREFIX_COUNTS.items()
        if prefix_counts[prefix] != expected
    }
    legacy = sorted(name_set & (r10.FORBIDDEN_LEGACY_ARENA | FORBIDDEN_MONOLITHIC))
    provider = sorted(name_set & r10.FORBIDDEN_PROVIDER)
    final_scope = sorted(name for name in names if any(token in name.upper() for token in r10.FORBIDDEN_FINAL_TOKENS))
    namespace = sorted(name for name in names if strict_namespace and name and not name.startswith("SYLVA_"))

    node_by_name = {node["name"]: node for node in named_nodes}
    terrain_render_without_mesh = sorted(name for name in TERRAIN_RENDER if name in node_by_name and "mesh" not in node_by_name[name])
    terrain_collision_without_mesh = sorted(name for name in TERRAIN_COLLISION if name in node_by_name and "mesh" not in node_by_name[name])
    route_topology_pass, route_topology_rows = r10.route_topology(document, blob)

    checks = {
        "transport_envelope_r11": True,
        "has_nodes": bool(nodes),
        "has_meshes": bool(document.get("meshes")),
        "required_exact_names": not missing,
        "prefix_counts": not bad_prefix_counts,
        "unique_named_nodes": not duplicates,
        "no_legacy_monolithic_or_single_floor_nodes": not legacy,
        "no_provider_mesh_names": not provider,
        "no_final_scope_nodes": not final_scope,
        "namespace": not namespace,
        "terrain_render_tiles_have_mesh": not terrain_render_without_mesh,
        "terrain_collision_tiles_have_mesh": not terrain_collision_without_mesh,
        "route_collision_closed_manifold": route_topology_pass,
    }
    return {
        "schema_version": 1,
        "contract": CONTRACT,
        "passed": all(checks.values()),
        "checks": checks,
        "transport": meta,
        "prefix_counts": prefix_counts,
        "missing_exact": missing,
        "bad_prefix_counts": bad_prefix_counts,
        "duplicate_names": duplicates,
        "legacy_nodes": legacy,
        "namespace_violations": namespace,
        "forbidden_provider_nodes": provider,
        "final_scope_nodes": final_scope,
        "terrain_render_without_mesh": terrain_render_without_mesh,
        "terrain_collision_without_mesh": terrain_collision_without_mesh,
        "route_collision_topology": route_topology_rows,
        "limitations": [
            "Does not validate Blender stream-membership custom properties after an importer discards extras.",
            "Does not execute engine cell residency/prefetch/HLOD behavior.",
            "Does not validate human art direction or target-hardware performance.",
        ],
    }


def validate_file(path: Path, expected_sha256: str | None = None, strict_namespace: bool = True) -> dict:
    document, meta, blob = r11.read_glb_hardened(path)
    report = validate_document(document, meta, blob, strict_namespace=strict_namespace)
    actual_sha = r11.sha256_file(path)
    report["artifact"] = {
        "path": str(path),
        "sha256": actual_sha,
        "expected_sha256": expected_sha256,
        "sha256_match": expected_sha256 is None or actual_sha.lower() == expected_sha256.lower(),
    }
    if not report["artifact"]["sha256_match"]:
        report["checks"]["sha256"] = False
        report["passed"] = False
    elif expected_sha256:
        report["checks"]["sha256"] = True
    report["passed"] = bool(report["passed"]) and all(report["checks"].values())
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("glb", type=Path)
    parser.add_argument("--expected-sha256")
    parser.add_argument("--json-out", type=Path)
    parser.add_argument("--allow-non-sylva-nodes", action="store_true")
    args = parser.parse_args(argv)
    try:
        report = validate_file(args.glb, args.expected_sha256, strict_namespace=not args.allow_non_sylva_nodes)
    except Exception as exc:
        report = {"schema_version": 1, "contract": CONTRACT, "passed": False, "error": type(exc).__name__, "detail": str(exc)}
    encoded = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(encoded, encoding="utf-8")
    sys.stdout.write(encoded)
    return 0 if report.get("passed") else 1


if __name__ == "__main__":
    raise SystemExit(main())
