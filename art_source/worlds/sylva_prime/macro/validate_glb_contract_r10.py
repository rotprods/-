#!/usr/bin/env python3
"""SYLVA PRIME macro GLB contract validator — R10.

Pure stdlib. Validates:
- GLB v2 transport;
- stable SYLVA namespace / required macro interfaces;
- no provider-root-kit duplication or legacy single-floor VESPER arena;
- exact family counts for streaming, sockets, collision and route IDs;
- decoded GLB topology for SYLVA_COL_ROUTE_00..03: closed manifold, no degenerate triangles.

This is still NOT a human art review, gameplay traversal test or GPU benchmark.
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
JSON_CHUNK = 0x4E4F534A
BIN_CHUNK = 0x004E4942
CONTRACT = "CLM-SYLVA-MACRO-001/R10"
ROUTE_COLLISIONS = {f"SYLVA_COL_ROUTE_{i:02d}" for i in range(4)}

EXPECTED_EXACT = {
    "SYLVA_TERRAIN_Macro12km_PROPOSAL",
    "SYLVA_META_RootKitIntegration",
    "SYLVA_META_RootKitSocketConsumerContract",
    "SYLVA_META_NavigationRouteContract",
    "SYLVA_META_VESPER_ThreeTerraceLayout",
    "SYLVA_STREAM_REGION_PUERTO_INJERTO",
    "SYLVA_STREAM_REGION_BOSQUE_FRASES",
    "SYLVA_STREAM_REGION_CAMARA_VESPER",
    "SYLVA_COL_TERRAIN_Macro12km_LowRes_PROPOSAL",
    "SYLVA_COL_PUERTO_Deck",
    "SYLVA_COL_BOSQUE_CentralPad",
    *ROUTE_COLLISIONS,
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
}

EXPECTED_PREFIX_COUNTS = {
    "SYLVA_STREAM_L3_": 16,
    "SYLVA_STREAM_REGION_": 3,
    "SYLVA_SOCKET_": 8,
    "SYLVA_COL_": 12,
    "SYLVA_TRAV_PathGuide_": 4,
    "SYLVA_ROOT_PRIMARY_": 6,
    "SYLVA_ROOT_SECONDARY_": 8,
    "SYLVA_VESPER_TerraceConnector_": 2,
}

FORBIDDEN_LEGACY_ARENA = {"SYLVA_VESPER_ProxyArenaFloor", "SYLVA_COL_VESPER_ArenaFloor"}
FORBIDDEN_PROVIDER = {
    "SYL_ROOT_A1_STRAIGHT_08M", "SYL_ROOT_A2_CURVE_12M", "SYL_ROOT_A3_RISE_10M",
    "SYL_ROOT_B1_FORK", "SYL_ROOT_B2_ARCH_14M", "SYL_ROOT_C1_BUTTRESS_07M",
    "SYL_ROOT_C2_TERRACE", "SYL_ROOT_C3_MEMBRANE_ANCHOR",
}
FORBIDDEN_FINAL_TOKENS = (
    "VESPER_FINAL", "EDDA", "SIETE-EN-UNO", "NICO_FER", "CIERVO_DE_ESPORAS",
    "GRAJILLA_MICELAR", "ANDADOR_DE_CORTEZA",
)
COMPONENT = {5120: ("b", 1), 5121: ("B", 1), 5122: ("h", 2), 5123: ("H", 2), 5125: ("I", 4), 5126: ("f", 4)}
NCOMP = {"SCALAR": 1, "VEC2": 2, "VEC3": 3, "VEC4": 4, "MAT2": 4, "MAT3": 9, "MAT4": 16}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read_glb(path: Path) -> tuple[dict, dict, bytes]:
    data = path.read_bytes()
    if len(data) < 20:
        raise ValueError("GLB_TOO_SMALL")
    magic, version, declared = struct.unpack_from("<4sII", data, 0)
    if magic != MAGIC:
        raise ValueError(f"BAD_MAGIC:{magic!r}")
    if version != 2:
        raise ValueError(f"BAD_VERSION:{version}")
    if declared != len(data):
        raise ValueError(f"LENGTH_MISMATCH:{declared}!={len(data)}")

    offset = 12
    chunks = []
    while offset < len(data):
        if offset + 8 > len(data):
            raise ValueError("TRUNCATED_CHUNK_HEADER")
        length, chunk_type = struct.unpack_from("<II", data, offset)
        offset += 8
        end = offset + length
        if end > len(data):
            raise ValueError("TRUNCATED_CHUNK_BODY")
        chunks.append((chunk_type, data[offset:end]))
        offset = end

    json_chunks = [body for typ, body in chunks if typ == JSON_CHUNK]
    if len(json_chunks) != 1:
        raise ValueError(f"JSON_CHUNK_COUNT:{len(json_chunks)}")
    doc = json.loads(json_chunks[0].rstrip(b"\x00 \t\r\n").decode("utf-8"))
    bin_chunks = [body for typ, body in chunks if typ == BIN_CHUNK]
    blob = bin_chunks[0] if bin_chunks else b""
    return doc, {
        "byte_length": len(data), "version": version, "chunk_count": len(chunks),
        "json_chunk_count": len(json_chunks), "bin_chunk_count": len(bin_chunks),
    }, blob


def decode_accessor(doc: dict, blob: bytes, accessor_index: int):
    accessor = doc["accessors"][accessor_index]
    if "sparse" in accessor:
        raise ValueError("SPARSE_ACCESSOR_UNSUPPORTED")
    view = doc["bufferViews"][accessor["bufferView"]]
    if "extensions" in view:
        raise ValueError("COMPRESSED_BUFFERVIEW_UNSUPPORTED")
    ctype = accessor["componentType"]
    atype = accessor["type"]
    if ctype not in COMPONENT or atype not in NCOMP:
        raise ValueError("ACCESSOR_FORMAT_UNSUPPORTED")
    fmt, scalar_size = COMPONENT[ctype]
    components = NCOMP[atype]
    base = view.get("byteOffset", 0) + accessor.get("byteOffset", 0)
    stride = view.get("byteStride", scalar_size * components)
    unpack = "<" + fmt * components
    values = []
    for index in range(accessor["count"]):
        value = struct.unpack_from(unpack, blob, base + index * stride)
        values.append(value[0] if components == 1 else value)
    return values


def route_topology(doc: dict, blob: bytes) -> tuple[bool, list[dict]]:
    nodes = {n.get("name"): n for n in doc.get("nodes", []) if isinstance(n, dict) and n.get("name")}
    rows = []
    all_pass = True
    for name in sorted(ROUTE_COLLISIONS):
        row = {"name": name, "passed": False}
        node = nodes.get(name)
        if not node or "mesh" not in node:
            row["error"] = "NODE_OR_MESH_MISSING"
            rows.append(row); all_pass = False; continue
        mesh = doc.get("meshes", [])[node["mesh"]]
        primitives = mesh.get("primitives", [])
        if len(primitives) != 1:
            row["error"] = f"PRIMITIVE_COUNT:{len(primitives)}"
            rows.append(row); all_pass = False; continue
        primitive = primitives[0]
        if primitive.get("mode", 4) != 4 or "indices" not in primitive or "POSITION" not in primitive.get("attributes", {}):
            row["error"] = "INDEXED_TRIANGLES_REQUIRED"
            rows.append(row); all_pass = False; continue
        try:
            indices = [int(v) for v in decode_accessor(doc, blob, primitive["indices"])]
            positions = decode_accessor(doc, blob, primitive["attributes"]["POSITION"])
        except Exception as exc:
            row["error"] = f"{type(exc).__name__}:{exc}"
            rows.append(row); all_pass = False; continue
        if len(indices) % 3:
            row["error"] = "INDEX_COUNT_NOT_DIVISIBLE_BY_3"
            rows.append(row); all_pass = False; continue

        edges = Counter()
        degenerate = 0
        for offset in range(0, len(indices), 3):
            a, b, c = indices[offset:offset + 3]
            if len({a, b, c}) < 3:
                degenerate += 1
                continue
            pa, pb, pc = positions[a], positions[b], positions[c]
            ux, uy, uz = pb[0]-pa[0], pb[1]-pa[1], pb[2]-pa[2]
            vx, vy, vz = pc[0]-pa[0], pc[1]-pa[1], pc[2]-pa[2]
            cx, cy, cz = uy*vz-uz*vy, uz*vx-ux*vz, ux*vy-uy*vx
            if cx*cx + cy*cy + cz*cz <= 1e-12:
                degenerate += 1
            for edge in ((a, b), (b, c), (c, a)):
                edges[tuple(sorted(edge))] += 1
        nonmanifold = sum(1 for count in edges.values() if count != 2)
        passed = degenerate == 0 and nonmanifold == 0
        row.update({
            "passed": passed, "triangles": len(indices)//3,
            "degenerate_triangles": degenerate, "nonmanifold_edge_count": nonmanifold,
        })
        rows.append(row)
        all_pass = all_pass and passed
    return all_pass, rows


def validate(doc: dict, meta: dict, blob: bytes, strict_namespace: bool = True) -> dict:
    nodes = doc.get("nodes") or []
    names = [n.get("name") for n in nodes if isinstance(n, dict) and isinstance(n.get("name"), str)]
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
    legacy = sorted(name_set & FORBIDDEN_LEGACY_ARENA)
    provider = sorted(name_set & FORBIDDEN_PROVIDER)
    final_scope = sorted(name for name in names if any(token in name.upper() for token in FORBIDDEN_FINAL_TOKENS))
    namespace = sorted(name for name in names if strict_namespace and name and not name.startswith("SYLVA_"))
    topology_pass, topology_rows = route_topology(doc, blob)

    checks = {
        "glb_v2": meta.get("version") == 2,
        "has_nodes": bool(nodes),
        "has_meshes": bool(doc.get("meshes")),
        "required_exact_names": not missing,
        "prefix_counts": not bad_prefix_counts,
        "unique_named_nodes": not duplicates,
        "no_legacy_single_floor_arena": not legacy,
        "no_provider_mesh_names": not provider,
        "no_final_scope_nodes": not final_scope,
        "namespace": not namespace,
        "route_collision_closed_manifold": topology_pass,
    }
    return {
        "schema_version": 1, "contract": CONTRACT, "passed": all(checks.values()), "checks": checks,
        "transport": meta, "prefix_counts": prefix_counts, "missing_exact": missing,
        "bad_prefix_counts": bad_prefix_counts, "duplicate_names": duplicates,
        "legacy_arena_nodes": legacy, "namespace_violations": namespace,
        "forbidden_provider_nodes": provider, "final_scope_nodes": final_scope,
        "route_collision_topology": topology_rows,
        "limitations": [
            "Does not validate human art direction.",
            "Does not validate runtime traversal or physics response.",
            "Does not validate GPU performance/LOD/HLOD.",
            "Does not prove Blender editability; validate .blend separately.",
        ],
    }


def synthetic_names() -> list[str]:
    names = set(EXPECTED_EXACT)
    names.update(f"SYLVA_STREAM_L3_X{x}Y{y}" for x in range(4) for y in range(4))
    names.update(f"SYLVA_SOCKET_TEST_{i:02d}" for i in range(8))
    names.update(f"SYLVA_TRAV_PathGuide_{i:02d}" for i in range(4))
    names.update(f"SYLVA_ROOT_PRIMARY_R{i:02d}" for i in range(1, 7))
    names.update(f"SYLVA_ROOT_SECONDARY_{i:02d}" for i in range(8))
    return sorted(names)


def write_synthetic_glb(path: Path, names: list[str], open_route: bool = False) -> None:
    positions = [(-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1)]
    indices = [0,2,1,0,3,2,4,5,6,4,6,7,0,1,5,0,5,4,1,2,6,1,6,5,2,3,7,2,7,6,3,0,4,3,4,7]
    if open_route:
        indices = [4,5,6,4,6,7]
    position_bytes = b"".join(struct.pack("<fff", *p) for p in positions)
    position_bytes += b"\x00" * ((4 - len(position_bytes) % 4) % 4)
    index_bytes = b"".join(struct.pack("<H", value) for value in indices)
    index_bytes += b"\x00" * ((4 - len(index_bytes) % 4) % 4)
    blob = position_bytes + index_bytes

    nodes = []
    for name in names:
        node = {"name": name}
        if name in ROUTE_COLLISIONS:
            node["mesh"] = 0
        nodes.append(node)
    doc = {
        "asset": {"version": "2.0", "generator": "SYLVA_R10_CONTRACT_SELFTEST"},
        "scene": 0,
        "scenes": [{"nodes": list(range(len(nodes)))}],
        "nodes": nodes,
        "meshes": [{"name": "SYLVA_ROUTE_COLLISION_R10_TEST_MESH", "primitives": [{"attributes": {"POSITION": 0}, "indices": 1, "mode": 4}]}],
        "bufferViews": [
            {"buffer": 0, "byteOffset": 0, "byteLength": len(position_bytes)},
            {"buffer": 0, "byteOffset": len(position_bytes), "byteLength": len(index_bytes)},
        ],
        "accessors": [
            {"bufferView": 0, "componentType": 5126, "count": len(positions), "type": "VEC3"},
            {"bufferView": 1, "componentType": 5123, "count": len(indices), "type": "SCALAR"},
        ],
        "buffers": [{"byteLength": len(blob)}],
    }
    encoded = json.dumps(doc, separators=(",", ":")).encode("utf-8")
    encoded += b" " * ((4 - len(encoded) % 4) % 4)
    chunks = struct.pack("<II", len(encoded), JSON_CHUNK) + encoded + struct.pack("<II", len(blob), BIN_CHUNK) + blob
    path.write_bytes(struct.pack("<4sII", MAGIC, 2, 12 + len(chunks)) + chunks)


def self_test() -> dict:
    cases = {}
    with tempfile.TemporaryDirectory(prefix="sylva-r10-contract-") as directory:
        root = Path(directory)
        names = synthetic_names()
        valid = root / "valid.glb"
        write_synthetic_glb(valid, names)
        doc, meta, blob = read_glb(valid)
        cases["valid_r10_contract_passes"] = validate(doc, meta, blob)["passed"]

        variants = {
            "missing_socket_fails": [n for n in names if n != "SYLVA_SOCKET_TEST_07"],
            "foreign_namespace_fails": names + ["OTHER_WORLD_NODE"],
            "provider_duplication_fails": names + [sorted(FORBIDDEN_PROVIDER)[0]],
            "missing_consumer_contract_fails": [n for n in names if n != "SYLVA_META_RootKitSocketConsumerContract"],
            "missing_navigation_contract_fails": [n for n in names if n != "SYLVA_META_NavigationRouteContract"],
        }
        for label, variant_names in variants.items():
            path = root / (label + ".glb")
            write_synthetic_glb(path, variant_names)
            d, m, b = read_glb(path)
            cases[label] = not validate(d, m, b)["passed"]

        legacy_nodes = {
            n for n in names
            if n.startswith("SYLVA_VESPER_Terrace_")
            or n.startswith("SYLVA_VESPER_TerraceConnector_")
            or n.startswith("SYLVA_COL_VESPER_Terrace_")
            or n.startswith("SYLVA_COL_VESPER_Connector_")
            or n == "SYLVA_META_VESPER_ThreeTerraceLayout"
        }
        legacy = root / "legacy.glb"
        write_synthetic_glb(legacy, [n for n in names if n not in legacy_nodes] + sorted(FORBIDDEN_LEGACY_ARENA))
        d, m, b = read_glb(legacy)
        cases["legacy_r4_single_floor_fails"] = not validate(d, m, b)["passed"]

        open_mesh = root / "open-route.glb"
        write_synthetic_glb(open_mesh, names, open_route=True)
        d, m, b = read_glb(open_mesh)
        cases["open_route_collision_fails"] = not validate(d, m, b)["passed"]

        corrupt = root / "corrupt.glb"
        corrupt.write_bytes(b"not-a-glb")
        try:
            read_glb(corrupt)
            cases["corrupt_header_fails"] = False
        except ValueError:
            cases["corrupt_header_fails"] = True
        cases["sha_mismatch_detected"] = sha256_file(valid) != "0" * 64

    return {
        "schema_version": 1, "contract": CONTRACT,
        "self_test_passed": all(cases.values()), "case_count": len(cases), "cases": cases,
        "note": "Synthetic contract/topology tests only; exact recovered r10 GLB still requires execution with its SHA-256."
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("glb", nargs="?", type=Path)
    parser.add_argument("--expected-sha256")
    parser.add_argument("--json-out", type=Path)
    parser.add_argument("--allow-non-sylva-nodes", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args(argv)

    if args.self_test:
        report = self_test()
    else:
        if args.glb is None:
            parser.error("glb required unless --self-test")
        try:
            doc, meta, blob = read_glb(args.glb)
            report = validate(doc, meta, blob, strict_namespace=not args.allow_non_sylva_nodes)
            actual = sha256_file(args.glb)
            report["artifact"] = {
                "path": str(args.glb), "sha256": actual,
                "expected_sha256": args.expected_sha256,
                "sha256_match": args.expected_sha256 is None or actual.lower() == args.expected_sha256.lower(),
            }
            if not report["artifact"]["sha256_match"]:
                report["passed"] = False
                report["checks"]["sha256"] = False
            elif args.expected_sha256:
                report["checks"]["sha256"] = True
        except Exception as exc:
            report = {"schema_version": 1, "contract": CONTRACT, "passed": False, "error": type(exc).__name__, "detail": str(exc)}

    encoded = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(encoded, encoding="utf-8")
    sys.stdout.write(encoded)
    passed = report.get("self_test_passed") if args.self_test else report.get("passed")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
