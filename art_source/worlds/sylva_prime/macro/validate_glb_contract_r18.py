#!/usr/bin/env python3
"""SYLVA PRIME macro GLB contract validator — R18.

Composes the accepted R13 streamed-world validator and adds portable semantics introduced
by R14/R18:
- 4 L2 supercell nodes in addition to the 16 L3 cells;
- all six primary kilometre roots must be mesh-backed nodes;
- no experimental R17 helper-profile nodes may leak into delivery;
- root family cardinality remains exactly six.

R15/R16/R18 custom-property semantics are source-scene contracts and may not survive every
glTF importer/export-extra configuration, so this validator intentionally does not pretend
to prove them from portable node names alone. Native import must separately prove metadata
adapter behavior.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import validate_glb_contract_r11 as r11
import validate_glb_contract_r13 as r13

CONTRACT = "CLM-SYLVA-MACRO-001/R18"
PRIMARY_ROOTS = {f"SYLVA_ROOT_PRIMARY_R0{i}" for i in range(1, 7)}
L2_CELLS = {f"SYLVA_STREAM_L2_X{x}Y{y}" for x in range(2) for y in range(2)}
REQUIRED_R14_PLUS = {
    "SYLVA_META_StreamHierarchyR14",
    *L2_CELLS,
    *PRIMARY_ROOTS,
}
FORBIDDEN_HELPER_PREFIXES = (
    "SYLVA_PROFILE_R17_",
    "SYLVA_ROOT_PRIMARY_R01__R17_TMP",
    "SYLVA_ROOT_PRIMARY_R03__R17_TMP",
    "SYLVA_ROOT_PRIMARY_R02__R18_TMP",
    "SYLVA_ROOT_PRIMARY_R04__R18_TMP",
    "SYLVA_ROOT_PRIMARY_R05__R18_TMP",
    "SYLVA_ROOT_PRIMARY_R06__R18_TMP",
)


def validate_document(document: dict, meta: dict, blob: bytes, strict_namespace: bool = True) -> dict:
    base = r13.validate_document(document, meta, blob, strict_namespace=strict_namespace)
    nodes = document.get("nodes") or []
    named_nodes = [node for node in nodes if isinstance(node, dict) and isinstance(node.get("name"), str)]
    names = [node["name"] for node in named_nodes]
    name_set = set(names)
    node_by_name = {node["name"]: node for node in named_nodes}

    missing_r18 = sorted(REQUIRED_R14_PLUS - name_set)
    roots_without_mesh = sorted(name for name in PRIMARY_ROOTS if name in node_by_name and "mesh" not in node_by_name[name])
    root_names = sorted(name for name in names if name.startswith("SYLVA_ROOT_PRIMARY_"))
    leaked_helpers = sorted(name for name in names if any(name.startswith(prefix) for prefix in FORBIDDEN_HELPER_PREFIXES))

    checks = dict(base.get("checks", {}))
    checks.update(
        {
            "required_r14_r18_names": not missing_r18,
            "primary_root_count_exactly_six": len(root_names) == 6 and set(root_names) == PRIMARY_ROOTS,
            "all_primary_roots_mesh_backed": not roots_without_mesh,
            "no_r17_r18_helper_nodes": not leaked_helpers,
        }
    )

    limitations = list(base.get("limitations", []))
    limitations.extend(
        [
            "Portable GLB validation does not prove R16 taper multipliers or R18 serialized source-curve custom properties unless extras are explicitly preserved and separately validated.",
            "Does not prove that the six root meshes match the accepted Blender fingerprint 7b1a4c5c...; exact artifact SHA plus source receipt binds that identity.",
            "Does not replace native engine residency/traversal, target-hardware profiling or human GATE-ART.",
        ]
    )

    return {
        **base,
        "schema_version": 1,
        "contract": CONTRACT,
        "passed": all(checks.values()),
        "checks": checks,
        "missing_r14_r18": missing_r18,
        "primary_root_nodes": root_names,
        "primary_roots_without_mesh": roots_without_mesh,
        "leaked_helper_nodes": leaked_helpers,
        "limitations": limitations,
    }


def validate_file(path: Path, expected_sha256: str | None = None, strict_namespace: bool = True) -> dict:
    document, meta, blob = r11.read_glb_hardened(path)
    report = validate_document(document, meta, blob, strict_namespace=strict_namespace)
    actual_sha = r11.sha256_file(path)
    match = expected_sha256 is None or actual_sha.lower() == expected_sha256.lower()
    report["artifact"] = {
        "path": str(path),
        "sha256": actual_sha,
        "expected_sha256": expected_sha256,
        "sha256_match": match,
    }
    if expected_sha256:
        report["checks"]["sha256"] = match
    if not match:
        report["passed"] = False
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
        report = {
            "schema_version": 1,
            "contract": CONTRACT,
            "passed": False,
            "error": type(exc).__name__,
            "detail": str(exc),
        }
    encoded = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(encoded, encoding="utf-8")
    sys.stdout.write(encoded)
    return 0 if report.get("passed") else 1


if __name__ == "__main__":
    raise SystemExit(main())
