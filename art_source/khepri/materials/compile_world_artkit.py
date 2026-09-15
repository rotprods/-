"""Compile KHEPRI material source into a World-Compiler-ready ArtKit payload.

Pure Python; no bpy. Bridges the verified material application/recipe contracts to the candidate
Asset Grammar described in EXOVANT_WORLD_SYSTEMS_MASTER_2026-09-14.md. It does not choose final
runtime texture budgets or engine-native optimizations.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from compile_application_matrix import compile_matrix, audit as matrix_audit
from compile_material_recipe import compile_recipe

CONTRACT = "KHP_MATERIAL_WORLD_ARTKIT_X100_V1"
SOURCE = Path(__file__).with_name("world_artkit_source.json")


def load_source() -> dict:
    data = json.loads(SOURCE.read_text(encoding="utf-8"))
    if data.get("contract") != CONTRACT:
        raise ValueError(f"unexpected source contract: {data.get('contract')}")
    return data


def compile_artkit() -> dict:
    source = load_source()
    matrix = compile_matrix()
    matrix_meta = matrix_audit()
    families = source["families"]
    applications = []
    for row in matrix:
        family = families[row["family"]]
        recipe = compile_recipe(row["application_id"])
        applications.append({
            "application_id": row["application_id"],
            "asset_id": row["asset_id"],
            "family": row["family"],
            "civilization": source["civilization"],
            "state": row["state"],
            "cause": row["cause"],
            "manufacturing_finish": row["finish"],
            "application_scale": row["scale"],
            "authoring_px_per_m_proposal": row["authoring_px_per_m"],
            "style_tags": family["style_tags"],
            "semantic_roles": family["semantic_roles"],
            "allowed_contexts": family["allowed_contexts"],
            "forbidden_contexts": family["forbidden_contexts"],
            "performance_class": family["performance_class"],
            "portable_output": recipe["portable_output"],
            "engine_native_optimization": recipe["engine_native_optimization"],
        })
    application_ids = [row["application_id"] for row in applications]
    payload = {
        "schema_version": 1,
        "contract": CONTRACT,
        "artkit_version": source["generator_inputs"]["artkit_version"],
        "world_id": source["world_id"],
        "civilization": source["civilization"],
        "faction": source["faction"],
        "global_rules": source["global_rules"],
        "families": families,
        "applications": applications,
        "provenance": source["provenance"],
        "nonclaims": source["nonclaims"],
        "generation_identity": {
            "application_count": len(applications),
            "matrix_sha256": matrix_meta["matrix_sha256"],
            "application_ids_sha256": hashlib.sha256(json.dumps(application_ids, separators=(",", ":")).encode()).hexdigest(),
        },
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    payload["artkit_sha256"] = hashlib.sha256(canonical).hexdigest()
    return payload


def audit() -> dict:
    payload = compile_artkit()
    apps = payload["applications"]
    families = payload["families"]
    checks = {
        "six_families": len(families) == 6,
        "applications_139": len(apps) == 139,
        "unique_application_ids": len({row["application_id"] for row in apps}) == 139,
        "all_families_resolve": all(row["family"] in families for row in apps),
        "all_have_context_rules": all(row["allowed_contexts"] and row["forbidden_contexts"] for row in apps),
        "all_have_semantic_roles": all(row["semantic_roles"] for row in apps),
        "all_portable_outputs_are_non_emissive": all(row["portable_output"]["emission"] is False for row in apps),
        "runtime_budget_remains_blocked": payload["global_rules"]["runtime_budget_status"] == "BLOCKED_TARGET_HARDWARE_QUALIFICATION",
        "human_gate_remains_open": payload["global_rules"]["human_art_status"] == "PENDING",
    }
    return {
        "contract": CONTRACT,
        "artkit_sha256": payload["artkit_sha256"],
        "matrix_sha256": payload["generation_identity"]["matrix_sha256"],
        "application_ids_sha256": payload["generation_identity"]["application_ids_sha256"],
        "families": len(families),
        "applications": len(apps),
        "checks": checks,
        "passed": all(checks.values()),
        "boundary": "World-Compiler ArtKit bridge only; target-hardware texture budgets and final art remain separate gates.",
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
