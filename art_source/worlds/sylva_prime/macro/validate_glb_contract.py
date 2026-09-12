#!/usr/bin/env python3
"""Offline GLB contract validator for SYLVA PRIME macro foundation.

Pure stdlib. It validates transport/header + node naming contract before an engine
import. It does NOT validate visual art, physics behavior, gameplay traversal or GPU cost.

Usage:
    python3 validate_glb_contract.py path/to/sylva.glb
    python3 validate_glb_contract.py path/to/sylva.glb --expected-sha256 HASH --json-out report.json
"""
from __future__ import annotations

import argparse
import hashlib
import json
import struct
import sys
from collections import Counter
from pathlib import Path

MAGIC = b"glTF"
GLB_VERSION = 2
JSON_CHUNK = 0x4E4F534A
BIN_CHUNK = 0x004E4942

EXPECTED_EXACT = {
    "SYLVA_TERRAIN_Macro12km_PROPOSAL",
    "SYLVA_COL_TERRAIN_Macro12km_LowRes_PROPOSAL",
    "SYLVA_COL_PUERTO_Deck",
    "SYLVA_COL_BOSQUE_CentralPad",
    "SYLVA_COL_VESPER_ArenaFloor",
    "SYLVA_STREAM_REGION_PUERTO_INJERTO",
    "SYLVA_STREAM_REGION_BOSQUE_FRASES",
    "SYLVA_STREAM_REGION_CAMARA_VESPER",
    "SYLVA_META_RootKitIntegration",
}

EXPECTED_PREFIX_COUNTS = {
    "SYLVA_STREAM_L3_": 16,
    "SYLVA_STREAM_REGION_": 3,
    "SYLVA_SOCKET_": 8,
    "SYLVA_COL_": 8,
    "SYLVA_TRAV_PathGuide_": 4,
    "SYLVA_ROOT_PRIMARY_": 6,
    "SYLVA_ROOT_SECONDARY_": 8,
}

FORBIDDEN_PROVIDER_NODE_NAMES = {
    "SYL_ROOT_A1_STRAIGHT_08M",
    "SYL_ROOT_A2_CURVE_12M",
    "SYL_ROOT_A3_RISE_10M",
    "SYL_ROOT_B1_FORK",
    "SYL_ROOT_B2_ARCH_14M",
    "SYL_ROOT_C1_BUTTRESS_07M",
    "SYL_ROOT_C2_TERRACE",
    "SYL_ROOT_C3_MEMBRANE_ANCHOR",
}

FORBIDDEN_FINAL_SCOPE_TOKENS = (
    "VESPER_FINAL",
    "EDDA",
    "SIETE-EN-UNO",
    "NICO_FER",
    "CIERVO_DE_ESPORAS",
    "GRAJILLA_MICELAR",
    "ANDADOR_DE_CORTEZA",
)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read_glb(path: Path) -> tuple[dict, dict]:
    data = path.read_bytes()
    if len(data) < 20:
        raise ValueError("GLB_TOO_SMALL")
    magic, version, declared_length = struct.unpack_from("<4sII", data, 0)
    if magic != MAGIC:
        raise ValueError(f"BAD_MAGIC:{magic!r}")
    if version != GLB_VERSION:
        raise ValueError(f"BAD_VERSION:{version}")
    if declared_length != len(data):
        raise ValueError(f"LENGTH_MISMATCH:declared={declared_length}:actual={len(data)}")

    offset = 12
    chunks: list[tuple[int, bytes]] = []
    while offset < len(data):
        if offset + 8 > len(data):
            raise ValueError("TRUNCATED_CHUNK_HEADER")
        chunk_length, chunk_type = struct.unpack_from("<II", data, offset)
        offset += 8
        end = offset + chunk_length
        if end > len(data):
            raise ValueError("TRUNCATED_CHUNK_BODY")
        chunks.append((chunk_type, data[offset:end]))
        offset = end

    json_chunks = [body for typ, body in chunks if typ == JSON_CHUNK]
    if len(json_chunks) != 1:
        raise ValueError(f"JSON_CHUNK_COUNT:{len(json_chunks)}")
    try:
        doc = json.loads(json_chunks[0].rstrip(b"\x00 \t\r\n").decode("utf-8"))
    except Exception as exc:
        raise ValueError(f"JSON_DECODE:{exc}") from exc

    meta = {
        "byte_length": len(data),
        "version": version,
        "chunk_count": len(chunks),
        "json_chunk_count": len(json_chunks),
        "bin_chunk_count": sum(1 for typ, _ in chunks if typ == BIN_CHUNK),
    }
    return doc, meta


def validate(doc: dict, meta: dict, strict_namespace: bool = True) -> dict:
    nodes = doc.get("nodes") or []
    names = [n.get("name") for n in nodes if isinstance(n, dict) and isinstance(n.get("name"), str)]
    name_set = set(names)
    counts = Counter(names)

    missing_exact = sorted(EXPECTED_EXACT - name_set)
    duplicate_names = sorted(name for name, count in counts.items() if count > 1)

    prefix_counts = {
        prefix: sum(1 for name in names if name.startswith(prefix))
        for prefix in EXPECTED_PREFIX_COUNTS
    }
    bad_prefix_counts = {
        prefix: {"expected": expected, "actual": prefix_counts[prefix]}
        for prefix, expected in EXPECTED_PREFIX_COUNTS.items()
        if prefix_counts[prefix] != expected
    }

    provider_nodes = sorted(name_set & FORBIDDEN_PROVIDER_NODE_NAMES)
    final_scope_nodes = sorted(
        name for name in names if any(token in name.upper() for token in FORBIDDEN_FINAL_SCOPE_TOKENS)
    )

    namespace_violations = []
    if strict_namespace:
        namespace_violations = sorted(name for name in names if name and not name.startswith("SYLVA_"))

    unnamed_nodes = len(nodes) - len(names)
    meshes = doc.get("meshes") or []
    materials = doc.get("materials") or []
    scenes = doc.get("scenes") or []

    checks = {
        "glb_v2": meta.get("version") == 2,
        "has_nodes": len(nodes) > 0,
        "has_meshes": len(meshes) > 0,
        "required_exact_names": not missing_exact,
        "prefix_counts": not bad_prefix_counts,
        "unique_named_nodes": not duplicate_names,
        "no_provider_mesh_names": not provider_nodes,
        "no_final_scope_nodes": not final_scope_nodes,
        "namespace": not namespace_violations,
    }
    passed = all(checks.values())

    return {
        "schema_version": 1,
        "contract": "CLM-SYLVA-MACRO-001/R4",
        "passed": passed,
        "checks": checks,
        "transport": meta,
        "gltf_counts": {
            "nodes": len(nodes),
            "named_nodes": len(names),
            "unnamed_nodes": unnamed_nodes,
            "meshes": len(meshes),
            "materials": len(materials),
            "scenes": len(scenes),
        },
        "prefix_counts": prefix_counts,
        "missing_exact": missing_exact,
        "bad_prefix_counts": bad_prefix_counts,
        "duplicate_names": duplicate_names,
        "namespace_violations": namespace_violations,
        "forbidden_provider_nodes": provider_nodes,
        "final_scope_nodes": final_scope_nodes,
        "limitations": [
            "Does not validate human art direction.",
            "Does not validate engine collision/traversal.",
            "Does not validate GPU performance/LOD/HLOD.",
            "Does not prove Blender editability; validate .blend separately.",
        ],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("glb", type=Path)
    parser.add_argument("--expected-sha256")
    parser.add_argument("--json-out", type=Path)
    parser.add_argument("--allow-non-sylva-nodes", action="store_true")
    args = parser.parse_args(argv)

    report: dict
    try:
        actual_sha = sha256_file(args.glb)
        doc, meta = read_glb(args.glb)
        report = validate(doc, meta, strict_namespace=not args.allow_non_sylva_nodes)
        report["artifact"] = {
            "path": str(args.glb),
            "sha256": actual_sha,
            "sha256_expected": args.expected_sha256,
            "sha256_match": args.expected_sha256 is None or actual_sha.lower() == args.expected_sha256.lower(),
        }
        if not report["artifact"]["sha256_match"]:
            report["passed"] = False
            report["checks"]["sha256"] = False
        elif args.expected_sha256:
            report["checks"]["sha256"] = True
    except Exception as exc:
        report = {
            "schema_version": 1,
            "contract": "CLM-SYLVA-MACRO-001/R4",
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
