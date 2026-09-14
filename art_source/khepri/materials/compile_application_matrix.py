"""Pure-Python KHEPRI material application matrix compiler.

No bpy dependency. Enumerates family × causal state × manufacturing finish × application scale,
rejects semantic contradictions, and emits the 139 valid X100 applications. The authoring texel
numbers are provisional source targets, NOT final runtime memory budgets.
"""
from __future__ import annotations

import hashlib
import json

SCALES = {
    "hero_insert": {"authoring_px_per_m": 1024, "intent": "close inspection / hero inset"},
    "prop_machine": {"authoring_px_per_m": 512, "intent": "interactive props and machinery"},
    "architectural": {"authoring_px_per_m": 256, "intent": "modular architecture / broad surfaces"},
}

FAMILIES = {
    "solar_glass": {
        "asset_id": "KHP_MAT_GLASS_SOLAR_001",
        "finishes": ["cast_vitrified", "precision_polished"],
        "states": ["calibrated", "service_worn", "thermal_cycled", "repair_laminated"],
    },
    "mirror_optical": {
        "asset_id": "KHP_MAT_MIRROR_OPTICAL_001",
        "finishes": ["broad_reflector", "precision_optic"],
        "states": ["calibrated", "maintenance_cleaning", "service_microabrasion", "repair_recoated"],
    },
    "bronze_synod": {
        "asset_id": "KHP_MAT_BRONZE_SYNOD_001",
        "finishes": ["cast_structural", "machined_service"],
        "states": ["service_clean", "contact_polished", "heat_affected_local", "field_repaired"],
    },
    "ceramic_scorched": {
        "asset_id": "KHP_MAT_CERAMIC_SCORCHED_001",
        "finishes": ["pressed_tile", "cast_shell"],
        "states": ["intact", "heat_cycled", "stress_chipped", "patch_replaced"],
    },
    "fabric_shade": {
        "asset_id": "KHP_MAT_FABRIC_SHADE_001",
        "finishes": ["woven_dense", "laminated_cloth"],
        "states": ["taut_service", "handled_worn", "solar_aged", "stitched_repair"],
    },
    "mineral_dark": {
        "asset_id": "KHP_MAT_MINERAL_DESERT_001",
        "finishes": ["rough_mass", "cut_plate"],
        "states": ["cut_clean", "foot_traffic_worn", "thermal_fissure_proxy", "mechanical_patch"],
    },
}

CAUSE = {
    "calibrated": "base", "intact": "base", "taut_service": "base", "cut_clean": "base",
    "service_worn": "contact_use", "service_microabrasion": "contact_use",
    "contact_polished": "contact_use", "handled_worn": "contact_use", "foot_traffic_worn": "contact_use",
    "maintenance_cleaning": "maintenance", "service_clean": "maintenance",
    "thermal_cycled": "thermal", "heat_affected_local": "thermal", "heat_cycled": "thermal",
    "solar_aged": "thermal", "thermal_fissure_proxy": "thermal",
    "repair_laminated": "repair", "repair_recoated": "repair", "field_repaired": "repair",
    "patch_replaced": "repair", "stitched_repair": "repair", "mechanical_patch": "repair",
    "stress_chipped": "mechanical_stress",
}

# Explicit contradictions discovered during pre-claim contract compilation.
INVALID = {
    ("solar_glass", "thermal_cycled", "precision_polished", "architectural"),
    ("mirror_optical", "service_microabrasion", "precision_optic", "prop_machine"),
    ("bronze_synod", "contact_polished", "machined_service", "architectural"),
    ("fabric_shade", "handled_worn", "laminated_cloth", "architectural"),
    ("mineral_dark", "foot_traffic_worn", "rough_mass", "architectural"),
}


def compile_matrix() -> list[dict]:
    rows: list[dict] = []
    for family, spec in FAMILIES.items():
        for state in spec["states"]:
            for finish in spec["finishes"]:
                for scale, scale_spec in SCALES.items():
                    key = (family, state, finish, scale)
                    if key in INVALID:
                        continue
                    rows.append({
                        "application_id": f"{spec['asset_id']}::{state}::{finish}::{scale}",
                        "family": family,
                        "asset_id": spec["asset_id"],
                        "state": state,
                        "cause": CAUSE[state],
                        "finish": finish,
                        "scale": scale,
                        "authoring_px_per_m": scale_spec["authoring_px_per_m"],
                        "scale_intent": scale_spec["intent"],
                    })
    return rows


def audit() -> dict:
    rows = compile_matrix()
    per_family = {family: sum(row["family"] == family for row in rows) for family in FAMILIES}
    canonical = json.dumps(rows, sort_keys=True, separators=(",", ":")).encode()
    checks = {
        "valid_count_139": len(rows) == 139,
        "unique_application_ids": len({row["application_id"] for row in rows}) == len(rows),
        "six_families": len(per_family) == 6,
        "every_family_ge_20": min(per_family.values()) >= 20,
        "all_states_causal": all(row["cause"] in {"base", "contact_use", "maintenance", "thermal", "repair", "mechanical_stress"} for row in rows),
        "three_scales": {row["scale"] for row in rows} == set(SCALES),
    }
    return {
        "contract": "KHP_MATERIAL_APPLICATION_MATRIX_X100_V1",
        "rows": len(rows),
        "invalid_filtered": len(INVALID),
        "per_family": per_family,
        "matrix_sha256": hashlib.sha256(canonical).hexdigest(),
        "checks": checks,
        "passed": all(checks.values()),
        "boundary": "Authoring application contract only; texel density is provisional and runtime texture budgets require target-hardware qualification.",
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
