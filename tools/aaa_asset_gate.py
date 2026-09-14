#!/usr/bin/env python3
"""EXOVANT AAA source-asset fidelity gate.

This validator does NOT judge artistic quality from polycount. It validates that an asset
promotion has the evidence required by docs/AAA_ASSET_FIDELITY_GATE_V1.md.

Usage:
    python3 tools/aaa_asset_gate.py path/to/asset-fidelity.json

Exit 0 = evidence contract passes for requested target state.
Exit 2 = contract fails closed.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

STATES = [
    "BLOCKOUT",
    "PROXY",
    "SUPPORT_CANDIDATE",
    "HERO_CANDIDATE",
    "HERO_QUALIFIED",
    "RUNTIME_QUALIFIED",
    "CINEMATIC_QUALIFIED",
]

HERO_CHECKS = [
    "silhouette",
    "proportion",
    "construction_logic",
    "semantic_part_separation",
    "material_domain_readiness",
    "uv_bake_readiness",
    "closeup_stress",
]

SOURCE_ROUTES = {
    "MANUAL_MODEL",
    "PROCEDURAL_MODEL",
    "CAD_SOURCE",
    "PHOTOGRAMMETRY_SCAN",
    "GAUSSIAN_SPLAT_STATIC",
    "MULTIVIEW_IMAGE_TO_3D",
    "SINGLE_IMAGE_TO_3D",
    "HYBRID_RECONSTRUCTION",
}


def _bool_pass(value):
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.upper() in {"PASS", "TRUE", "QUALIFIED"}
    if isinstance(value, dict):
        state = str(value.get("status", "")).upper()
        return state in {"PASS", "TRUE", "QUALIFIED"}
    return False


def validate(record):
    errors = []
    warnings = []

    asset_id = record.get("asset_id")
    if not asset_id:
        errors.append("missing asset_id")

    before = record.get("fidelity_before")
    after = record.get("fidelity_after")
    if before not in STATES:
        errors.append(f"invalid fidelity_before: {before!r}")
    if after not in STATES:
        errors.append(f"invalid fidelity_after: {after!r}")

    intended = record.get("intended_exposure")
    if not isinstance(intended, dict):
        errors.append("intended_exposure must be an object")
    else:
        if intended.get("max_camera_distance_m") is None and intended.get("min_camera_distance_m") is None:
            warnings.append("camera exposure distance is unmeasured")
        if not intended.get("role"):
            errors.append("intended_exposure.role is required")

    source_route = record.get("source_route")
    if source_route not in SOURCE_ROUTES:
        errors.append(f"invalid or missing source_route: {source_route!r}")

    provenance = record.get("provenance")
    if not provenance:
        errors.append("missing provenance")

    if source_route in {"MULTIVIEW_IMAGE_TO_3D", "SINGLE_IMAGE_TO_3D", "HYBRID_RECONSTRUCTION"}:
        if not record.get("provider_model_version"):
            errors.append("reconstruction route requires provider_model_version")
        if not record.get("source_master_ref"):
            errors.append("reconstruction route requires source_master_ref")
        if source_route == "SINGLE_IMAGE_TO_3D" and after in {"HERO_QUALIFIED", "RUNTIME_QUALIFIED", "CINEMATIC_QUALIFIED"}:
            warnings.append("single-image reconstruction is high-risk for hero promotion; independent structural correction evidence expected")

    if after in {"HERO_QUALIFIED", "RUNTIME_QUALIFIED", "CINEMATIC_QUALIFIED"}:
        targets = record.get("look_target_refs")
        if not isinstance(targets, list) or not targets:
            errors.append("hero-or-higher promotion requires look_target_refs")
        if not record.get("source_master_ref"):
            errors.append("hero-or-higher promotion requires source_master_ref")
        gates = record.get("hero_gate", {})
        for check in HERO_CHECKS:
            if not _bool_pass(gates.get(check)):
                errors.append(f"hero_gate.{check} must PASS")
        if record.get("raw_reconstruction_final") is True:
            errors.append("raw reconstruction may not be final hero asset")

    if after == "RUNTIME_QUALIFIED":
        runtime = record.get("runtime", {})
        for key in ["engine_import", "collision", "lod_or_screen_space_policy", "profile_receipt"]:
            if not _bool_pass(runtime.get(key)):
                errors.append(f"runtime.{key} must PASS for RUNTIME_QUALIFIED")
        if not record.get("runtime_derivative_ref"):
            errors.append("RUNTIME_QUALIFIED requires runtime_derivative_ref")

    if after == "CINEMATIC_QUALIFIED":
        cinematic = record.get("cinematic", {})
        for key in ["representative_frame_review", "render_receipt"]:
            if not _bool_pass(cinematic.get(key)):
                errors.append(f"cinematic.{key} must PASS for CINEMATIC_QUALIFIED")
        if not record.get("cinematic_derivative_ref"):
            errors.append("CINEMATIC_QUALIFIED requires cinematic_derivative_ref")

    if record.get("claims_aaa") is True:
        if after not in {"RUNTIME_QUALIFIED", "CINEMATIC_QUALIFIED"}:
            errors.append("AAA claim requires runtime or cinematic qualification, not source fidelity alone")
        if not _bool_pass(record.get("human_gate_art")):
            errors.append("AAA claim requires human_gate_art PASS")

    # Explicit anti-pattern: a proxy cannot be promoted only by cosmetic polish evidence.
    if before in {"BLOCKOUT", "PROXY"} and after in {"HERO_QUALIFIED", "RUNTIME_QUALIFIED", "CINEMATIC_QUALIFIED"}:
        route_evidence = record.get("source_rebuild_or_structural_upgrade")
        if not _bool_pass(route_evidence):
            errors.append("BLOCKOUT/PROXY -> hero-or-higher requires source_rebuild_or_structural_upgrade PASS")

    return {
        "asset_id": asset_id,
        "passed": not errors,
        "errors": errors,
        "warnings": warnings,
        "policy": "BLOCKOUT != HERO_ASSET; MORE_POLYGONS != MORE_REALISM",
    }


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    args = parser.parse_args(argv)
    record = json.loads(args.manifest.read_text(encoding="utf-8"))
    result = validate(record)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
