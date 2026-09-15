#!/usr/bin/env python3
"""Deterministic EXOVANT World Compiler kernel.

This is deliberately engine-agnostic. It establishes stable identity, hierarchical
seed derivation, canonical hashing and compiler receipts before geometry systems
are allowed to depend on them.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

DOMAIN = b"EXOVANT-WORLD-SEED-V1\0"


def canonical_json(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sha256_hex(value: Any) -> str:
    return hashlib.sha256(canonical_json(value)).hexdigest()


def derive_seed(parent_seed: str, stable_child_id: str, domain: str) -> str:
    """Derive a 256-bit seed without depending on traversal/order/runtime RNG state."""
    h = hashlib.sha256()
    h.update(DOMAIN)
    h.update(domain.encode("utf-8"))
    h.update(b"\0")
    h.update(parent_seed.encode("utf-8"))
    h.update(b"\0")
    h.update(stable_child_id.encode("utf-8"))
    return h.hexdigest()


def compile_manifest(manifest: dict[str, Any]) -> dict[str, Any]:
    source = dict(manifest)
    source.pop("input_digest", None)
    source.pop("output_digest", None)
    input_digest = sha256_hex(source)

    targets = sorted(set(source.get("generation_targets", [])))
    children = [
        {
            "stable_id": target,
            "seed": derive_seed(source["root_seed"], target, "generation-target"),
        }
        for target in targets
    ]
    compiled = {
        "schema_version": 1,
        "stable_id": source["stable_id"],
        "input_digest": input_digest,
        "compiler_version": source["compiler_version"],
        "children": children,
        "override_precedence": ["LOCK", "PATCH", "OVERRIDE", "EXCLUDE", "GENERATED"],
    }
    compiled["output_digest"] = sha256_hex(compiled)
    return compiled


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    result = compile_manifest(manifest)
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(encoded, encoding="utf-8")
    else:
        print(encoded, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
