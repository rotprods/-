#!/usr/bin/env python3
"""Offline GLB contract validator for SYLVA PRIME macro foundation.

Pure stdlib. It validates transport/header + node naming contract before an engine
import. It does NOT validate visual art, physics behavior, gameplay traversal or GPU cost.

Usage:
    python3 validate_glb_contract.py path/to/sylva.glb
    python3 validate_glb_contract.py path/to/sylva.glb --expected-sha256 HASH --json-out report.json
    python3 validate_glb_contract.py --self-test
"""
from __future__ import annotations

import argparse
import hashlib
import json
import struct
import sys
import tempfile
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


def _synthetic_names() -> list[str]:
    names = set(EXPECTED_EXACT)
    names.update(f"SYLVA_STREAM_L3_X{x}Y{y}" for x in range(4) for y in range(4))
    names.update(f"SYLVA_SOCKET_TEST_{i:02d}" for i in range(8))
    names.update(f"SYLVA_COL_ROUTE_{i:02d}" for i in range(4))
    names.update(f"SYLVA_TRAV_PathGuide_{i:02d}" for i in range(4))
    names.update(f"SYLVA_ROOT_PRIMARY_R{i:02d}" for i in range(1, 7))
    names.update(f"SYLVA_ROOT_SECONDARY_{i:02d}" for i in range(8))
    return sorted(names)


def _write_synthetic_glb(path: Path, names: list[str]) -> None:
    doc = {
        "asset": {"version": "2.0", "generator": "SYLVA_CONTRACT_SELF_TEST"},
        "scene": 0,
        "scenes": [{"nodes": list(range(len(names)))}],
        "nodes": [{"name": name} for name in names],
        "meshes": [{"name": "SYLVA_SELFTEST_MESH", "primitives": []}],
        "materials": [{"name": "SYLVA_SELFTEST_MAT"}],
    }
    body = json.dumps(doc, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    body += b" " * ((4 - len(body) % 4) % 4)
    chunk = struct.pack("<II", len(body), JSON_CHUNK) + body
    data = struct.pack("<4sII", MAGIC, GLB_VERSION, 12 + len(chunk)) + chunk
    path.write_bytes(data)


def self_test() -> dict:
    cases: dict[str, bool] = {}
    details: dict[str, object] = {}
    with tempfile.TemporaryDirectory(prefix="sylva-glb-contract-") as tmp:
        root = Path(tmp)
        valid_path = root / "valid.glb"
        valid_names = _synthetic_names()
        _write_synthetic_glb(valid_path, valid_names)
        doc, meta = read_glb(valid_path)
        valid_report = validate(doc, meta)
        cases["valid_contract_passes"] = valid_report["passed"] is True
        details["valid_prefix_counts"] = valid_report["prefix_counts"]

        missing_socket = root / "missing-socket.glb"
        _write_synthetic_glb(missing_socket, [n for n in valid_names if n != "SYLVA_SOCKET_TEST_07"])
        doc2, meta2 = read_glb(missing_socket)
        report2 = validate(doc2, meta2)
        cases["missing_socket_fails"] = report2["passed"] is False and "SYLVA_SOCKET_" in report2["bad_prefix_counts"]

        foreign = root / "foreign.glb"
        _write_synthetic_glb(foreign, valid_names + ["OTHER_WORLD_NODE"])
        doc3, meta3 = read_glb(foreign)
        report3 = validate(doc3, meta3)
        cases["foreign_namespace_fails"] = report3["passed"] is False and "OTHER_WORLD_NODE" in report3["namespace_violations"]

        provider = root / "provider-dup.glb"
        provider_name = sorted(FORBIDDEN_PROVIDER_NODE_NAMES)[0]
        _write_synthetic_glb(provider, valid_names + [provider_name])
        doc4, meta4 = read_glb(provider)
        report4 = validate(doc4, meta4)
        cases["provider_duplication_fails"] = report4["passed"] is False and provider_name in report4["forbidden_provider_nodes"]

        corrupt = root / "corrupt.glb"
        corrupt.write_bytes(b"not-a-glb")
        try:
            read_glb(corrupt)
            corrupt_failed = False
        except ValueError:
            corrupt_failed = True
        cases["corrupt_header_fails"] = corrupt_failed

        expected = "0" * 64
        cases["sha_mismatch_detected"] = sha256_file(valid_path) != expected

    passed = all(cases.values())
    return {
        "schema_version": 1,
        "contract": "CLM-SYLVA-MACRO-001/R4",
        "self_test_passed": passed,
        "cases": cases,
        "details": details,
        "note": "Synthetic transport/contract tests only; actual r4 GLB still requires binary recovery and execution.",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("glb", type=Path, nargs="?")
    parser.add_argument("--expected-sha256")
    parser.add_argument("--json-out", type=Path)
    parser.add_argument("--allow-non-sylva-nodes", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args(argv)

    if args.self_test:
        report = self_test()
        encoded = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
        if args.json_out:
            args.json_out.parent.mkdir(parents=True, exist_ok=True)
            args.json_out.write_text(encoded, encoding="utf-8")
        sys.stdout.write(encoded)
        return 0 if report["self_test_passed"] else 1

    if args.glb is None:
        parser.error("glb is required unless --self-test is used")

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
