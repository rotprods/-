"""Compile a deterministic material binding plan for KHEPRI heliostat consumer metadata.

Pure Python. Uses the World ArtKit resolver instead of material filenames. The plan separates
semantic assignment from runtime representation: engine-native object/material overrides are
preferred if later qualified; otherwise the portable glTF fallback splits only panel mesh resources
by state while preserving instance reuse.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from resolve_world_material_request import MaterialRequest, resolve

CONTRACT = "KHP_HELIOSTAT_MATERIAL_BINDING_PLAN_V1"
SOURCE = Path(__file__).with_name("heliostat_consumer_state_matrix.json")


def _resolve_exact(context: str, role: str, state: str, finish: str, scale: str) -> str:
    out = resolve(MaterialRequest("khepri", context, role, state, finish, scale))
    if out.get("status") != "RESOLVED":
        raise RuntimeError(f"material request failed: {out}")
    return out["application"]["application_id"]


def compile_plan() -> dict:
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    if source.get("contract") != "KHP_HELIOSTAT_CONSUMER_STATE_MATRIX_V1":
        raise ValueError("unexpected consumer matrix contract")

    bronze = _resolve_exact(
        "heliostat_structure", "structure", "service_clean", "cast_structural", "architectural"
    )
    mirror_operational = _resolve_exact(
        "heliostat_field", "heliostat_reflector", "calibrated", "broad_reflector", "architectural"
    )
    mirror_maintenance = _resolve_exact(
        "heliostat_field", "heliostat_reflector", "maintenance_cleaning", "broad_reflector", "architectural"
    )

    rules = {
        "heliostat_footprint_mast": {
            "operational": {"slot_0": bronze},
            "maintenance": {"slot_0": bronze},
        },
        "heliostat_footprint_panel": {
            "operational": {"slot_0": mirror_operational, "slot_1": bronze},
            "maintenance": {"slot_0": mirror_maintenance, "slot_1": bronze},
        },
    }

    groups = []
    for group in source["groups"]:
        role = group["role"]
        state = group["state"]
        if role not in rules or state not in rules[role]:
            raise RuntimeError(f"unmapped consumer group: {group}")
        groups.append({
            **group,
            "material_slots": rules[role][state],
        })

    # Portable glTF material binding is mesh-data level in the current Blender/export path.
    # Masts share the same material across states, so each size can remain one mesh resource.
    # Panels need two state-specific material variants per size if engine object-level overrides
    # are not qualified: 3 mast resources + 3*2 panel resources = 9 optical mesh resources.
    current_resources = 6
    fallback_resources = 9
    payload = {
        "schema_version": 1,
        "contract": CONTRACT,
        "world_id": "khepri",
        "consumer_asset": source["consumer_asset"],
        "consumer_metadata_sha256": source["metadata_sha256"],
        "object_count": source["objects"],
        "binding_rules": rules,
        "groups": groups,
        "runtime_representation": {
            "preferred": {
                "strategy": "INSTANCE_OR_MATERIAL_OVERRIDE_IF_ENGINE_QUALIFIED",
                "optical_mesh_resource_count": current_resources,
                "status": "DEFERRED_ENGINE_CAPABILITY_GATE",
            },
            "portable_gltf_fallback": {
                "strategy": "STATE_SPLIT_PANEL_MESH_RESOURCES_ONLY",
                "optical_mesh_resource_count": fallback_resources,
                "increase_vs_current": fallback_resources - current_resources,
                "multiplier_vs_current": fallback_resources / current_resources,
                "object_count_unchanged": source["objects"],
                "reason": "panel operational/maintenance states require different reflector materials while mast material is state-invariant",
            },
        },
        "nonclaims": [
            "final engine material-override support",
            "target-hardware performance",
            "runtime LOD state switching",
            "final close-range material art",
        ],
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    payload["plan_sha256"] = hashlib.sha256(canonical).hexdigest()
    return payload


def audit() -> dict:
    plan = compile_plan()
    groups = plan["groups"]
    checks = {
        "objects_214": sum(group["count"] for group in groups) == 214,
        "twelve_groups": len(groups) == 12,
        "three_variants": {group["variant"] for group in groups} == {"compact", "standard", "wide"},
        "two_states": {group["state"] for group in groups} == {"operational", "maintenance"},
        "two_roles": {group["role"] for group in groups} == {"heliostat_footprint_mast", "heliostat_footprint_panel"},
        "maintenance_panel_uses_cleaning_state": all(
            group["material_slots"].get("slot_0", "").startswith("KHP_MAT_MIRROR_OPTICAL_001::maintenance_cleaning")
            for group in groups if group["role"] == "heliostat_footprint_panel" and group["state"] == "maintenance"
        ),
        "operational_panel_uses_calibrated_state": all(
            group["material_slots"].get("slot_0", "").startswith("KHP_MAT_MIRROR_OPTICAL_001::calibrated")
            for group in groups if group["role"] == "heliostat_footprint_panel" and group["state"] == "operational"
        ),
        "mast_material_state_invariant": len({
            group["material_slots"]["slot_0"] for group in groups if group["role"] == "heliostat_footprint_mast"
        }) == 1,
        "portable_fallback_nine_resources": plan["runtime_representation"]["portable_gltf_fallback"]["optical_mesh_resource_count"] == 9,
    }
    return {
        "contract": CONTRACT,
        "plan_sha256": plan["plan_sha256"],
        "checks": checks,
        "passed": all(checks.values()),
        "boundary": "Binding-plan compiler only; runtime representation remains deferred until engine/target qualification.",
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
