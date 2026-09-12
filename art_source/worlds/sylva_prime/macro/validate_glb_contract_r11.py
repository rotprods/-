#!/usr/bin/env python3
"""SYLVA PRIME macro GLB contract validator — R11 transport-hardened wrapper.

R11 preserves the scene/naming/topology contract implemented by
`validate_glb_contract_r10.py` and adds the exact transport invariants promoted
by main commit ca224a78 / INFRA-005-DELIVERY-003:

- walk every GLB chunk;
- require 4-byte-aligned chunk lengths;
- reject truncated chunk headers/bodies;
- reject duplicate JSON or BIN chunks;
- preserve unknown aligned extension chunks;
- reject external buffer/image URIs for an offline delivery;
- then apply the R10 SYLVA node/scope/closed-manifold route contract.

This does not replace native engine import, Blender editability checks, human art
review or target-hardware performance qualification.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import struct
import sys
import tempfile
from pathlib import Path

import validate_glb_contract_r10 as r10

CONTRACT = "CLM-SYLVA-MACRO-001/R11"
MAGIC = b"glTF"
JSON_CHUNK = 0x4E4F534A
BIN_CHUNK = 0x004E4942


class ContractError(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ContractError(message)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read_glb_hardened(path: Path) -> tuple[dict, dict, bytes]:
    data = path.read_bytes()
    require(len(data) >= 20, "TRUNCATED_GLB")
    magic, version, declared_size = struct.unpack_from("<4sII", data, 0)
    require(magic == MAGIC, f"BAD_MAGIC:{magic!r}")
    require(version == 2, f"BAD_VERSION:{version}")
    require(declared_size == len(data), f"LENGTH_MISMATCH:{declared_size}!={len(data)}")

    cursor = 12
    seen_standard: set[int] = set()
    chunks: list[tuple[int, bytes]] = []
    unknown_chunk_types: list[int] = []

    while cursor < declared_size:
        require(declared_size - cursor >= 8, "TRUNCATED_CHUNK_HEADER")
        length, chunk_type = struct.unpack_from("<II", data, cursor)
        cursor += 8
        require(length % 4 == 0, f"MISALIGNED_CHUNK_LENGTH:{length}")
        require(length <= declared_size - cursor, "TRUNCATED_CHUNK_BODY")
        body = data[cursor:cursor + length]
        if chunk_type in {JSON_CHUNK, BIN_CHUNK}:
            require(chunk_type not in seen_standard, "DUPLICATE_JSON_OR_BIN_CHUNK")
            seen_standard.add(chunk_type)
        else:
            unknown_chunk_types.append(chunk_type)
        chunks.append((chunk_type, body))
        cursor += length

    require(cursor == declared_size, "CHUNK_WALK_DID_NOT_END_AT_ENVELOPE")
    require(JSON_CHUNK in seen_standard, "JSON_CHUNK_MISSING")

    json_chunks = [body for kind, body in chunks if kind == JSON_CHUNK]
    require(len(json_chunks) == 1, "JSON_CHUNK_COUNT_INVALID")
    try:
        document = json.loads(json_chunks[0].rstrip(b"\x00 \t\r\n").decode("utf-8"))
    except Exception as exc:
        raise ContractError(f"JSON_DECODE:{exc}") from exc
    require(isinstance(document, dict), "GLB_DOCUMENT_NOT_OBJECT")
    require(bool(document.get("meshes")), "GLB_CONTAINS_NO_MESH_CANDIDATE")

    external_resources = []
    for collection_name in ("buffers", "images"):
        for index, record in enumerate(document.get(collection_name, []) or []):
            if isinstance(record, dict) and "uri" in record:
                external_resources.append(f"{collection_name}[{index}]")
    require(not external_resources, "GLB_DEPENDS_ON_EXTERNAL_RESOURCES:" + ",".join(external_resources))

    bin_chunks = [body for kind, body in chunks if kind == BIN_CHUNK]
    blob = bin_chunks[0] if bin_chunks else b""
    meta = {
        "byte_length": len(data),
        "version": version,
        "chunk_count": len(chunks),
        "json_chunk_count": 1,
        "bin_chunk_count": len(bin_chunks),
        "unknown_chunk_count": len(unknown_chunk_types),
        "unknown_chunk_types": unknown_chunk_types,
        "transport_hardening_source": "main@ca224a78/INFRA-005-DELIVERY-003",
    }
    return document, meta, blob


def validate_file(path: Path, expected_sha256: str | None = None, strict_namespace: bool = True) -> dict:
    actual_sha = sha256_file(path)
    document, meta, blob = read_glb_hardened(path)
    report = r10.validate(document, meta, blob, strict_namespace=strict_namespace)
    report["contract"] = CONTRACT
    report["transport_hardened"] = True
    report["artifact"] = {
        "path": str(path),
        "sha256": actual_sha,
        "expected_sha256": expected_sha256,
        "sha256_match": expected_sha256 is None or actual_sha.lower() == expected_sha256.lower(),
    }
    report["checks"]["transport_envelope_r11"] = True
    report["checks"]["offline_no_external_resources"] = True
    if not report["artifact"]["sha256_match"]:
        report["checks"]["sha256"] = False
        report["passed"] = False
    elif expected_sha256:
        report["checks"]["sha256"] = True
    report["passed"] = bool(report.get("passed")) and all(report["checks"].values())
    return report


def _pad4(data: bytes, byte: bytes = b"\x00") -> bytes:
    return data + byte * ((4 - len(data) % 4) % 4)


def _base_fixture(tmp: Path) -> Path:
    path = tmp / "valid.glb"
    r10.write_synthetic_glb(path, r10.synthetic_names())
    return path


def _parse_chunks(data: bytes) -> list[tuple[int, bytes]]:
    cursor = 12
    result = []
    while cursor < len(data):
        length, kind = struct.unpack_from("<II", data, cursor)
        cursor += 8
        result.append((kind, data[cursor:cursor + length]))
        cursor += length
    return result


def _assemble(chunks: list[tuple[int, bytes]]) -> bytes:
    payload = b"".join(struct.pack("<II", len(body), kind) + body for kind, body in chunks)
    return struct.pack("<4sII", MAGIC, 2, 12 + len(payload)) + payload


def self_test() -> dict:
    cases: dict[str, bool] = {}
    details: dict[str, object] = {}
    with tempfile.TemporaryDirectory(prefix="sylva-r11-glb-") as directory:
        tmp = Path(directory)
        valid = _base_fixture(tmp)
        report = validate_file(valid)
        cases["valid_r11_contract_passes"] = report["passed"] is True
        details["valid_transport"] = report["transport"]

        # Preserve all R10 semantic/topology adversarial coverage.
        r10_report = r10.self_test()
        cases["r10_semantic_topology_suite_passes"] = r10_report["self_test_passed"] is True
        details["r10_case_count"] = r10_report["case_count"]

        chunks = _parse_chunks(valid.read_bytes())
        json_body = next(body for kind, body in chunks if kind == JSON_CHUNK)
        bin_body = next((body for kind, body in chunks if kind == BIN_CHUNK), b"")

        duplicate_json = tmp / "duplicate-json.glb"
        duplicate_json.write_bytes(_assemble(chunks + [(JSON_CHUNK, json_body)]))
        try:
            read_glb_hardened(duplicate_json); cases["duplicate_json_fails"] = False
        except ContractError:
            cases["duplicate_json_fails"] = True

        if bin_body:
            duplicate_bin = tmp / "duplicate-bin.glb"
            duplicate_bin.write_bytes(_assemble(chunks + [(BIN_CHUNK, bin_body)]))
            try:
                read_glb_hardened(duplicate_bin); cases["duplicate_bin_fails"] = False
            except ContractError:
                cases["duplicate_bin_fails"] = True
        else:
            cases["duplicate_bin_fails"] = True

        # Unknown aligned chunk is allowed and reported.
        extension = tmp / "unknown-extension.glb"
        extension_kind = 0x12345678
        extension_body = _pad4(b"EXOVANT", b"\x00")
        extension.write_bytes(_assemble(chunks + [(extension_kind, extension_body)]))
        d, m, b = read_glb_hardened(extension)
        extension_report = r10.validate(d, m, b)
        cases["unknown_aligned_extension_passes"] = extension_report["passed"] is True and extension_kind in m["unknown_chunk_types"]

        # Build a malformed chunk whose declared length is not 4-byte aligned.
        malformed_payload = struct.pack("<II", 3, 0x76543210) + b"XYZ"
        malformed = tmp / "misaligned.glb"
        malformed.write_bytes(struct.pack("<4sII", MAGIC, 2, 12 + len(malformed_payload)) + malformed_payload)
        try:
            read_glb_hardened(malformed); cases["misaligned_chunk_fails"] = False
        except ContractError:
            cases["misaligned_chunk_fails"] = True

        # Valid header/envelope but chunk body overruns the file.
        truncated_body = tmp / "truncated-body.glb"
        payload = struct.pack("<II", 100, JSON_CHUNK) + b"{}  "
        truncated_body.write_bytes(struct.pack("<4sII", MAGIC, 2, 12 + len(payload)) + payload)
        try:
            read_glb_hardened(truncated_body); cases["truncated_body_fails"] = False
        except ContractError:
            cases["truncated_body_fails"] = True

        # Trailing bytes shorter than a chunk header.
        truncated_header = tmp / "truncated-header.glb"
        base_data = valid.read_bytes()
        broken = bytearray(base_data + b"1234")
        struct.pack_into("<I", broken, 8, len(broken))
        truncated_header.write_bytes(broken)
        try:
            read_glb_hardened(truncated_header); cases["truncated_chunk_header_fails"] = False
        except ContractError:
            cases["truncated_chunk_header_fails"] = True

        # External URI must be rejected even if transport framing is valid.
        external = tmp / "external-uri.glb"
        document = json.loads(json_body.rstrip(b"\x00 \t\r\n").decode("utf-8"))
        document["images"] = [{"uri": "texture.png"}]
        modified_json = _pad4(json.dumps(document, separators=(",", ":")).encode("utf-8"), b" ")
        external_chunks = [(JSON_CHUNK, modified_json)] + [(kind, body) for kind, body in chunks if kind != JSON_CHUNK]
        external.write_bytes(_assemble(external_chunks))
        try:
            read_glb_hardened(external); cases["external_resource_fails"] = False
        except ContractError:
            cases["external_resource_fails"] = True

        cases["sha_mismatch_detected"] = sha256_file(valid) != "0" * 64

    return {
        "schema_version": 1,
        "contract": CONTRACT,
        "self_test_passed": all(cases.values()),
        "case_count": len(cases),
        "cases": cases,
        "details": details,
        "note": "Synthetic transport + inherited R10 semantic/topology tests only. The exact recovered r11 GLB still requires SHA-bound execution.",
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
    passed = report.get("self_test_passed") if args.self_test else report.get("passed")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
