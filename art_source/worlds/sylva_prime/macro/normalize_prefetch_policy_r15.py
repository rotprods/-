"""SYLVA PRIME — normalize R14 prefetch metadata after pressure-study review.

Input scene: accepted R14 (`SYLVA_STREAM_HIERARCHY_R14`).
Output: metadata-only R15 policy-normalization checkpoint.

Reason:
R14 correctly established L2/L3 hierarchy and L3-only hero residency, but its metadata
still encoded `ADJACENT_8_PLUS_L3_HERO_RESIDENCY_GROUP` as the active prefetch policy.
Read-only pressure study showed current+8 can conservatively touch up to 72.8% of the
current spatial-object set. Runtime IO/residency latency, memory and draw cost remain
unmeasured, so no prefetch policy may be production-approved yet.

R15 changes only custom properties on existing metadata/empty objects. It must not create,
delete, move or alter any MESH/CURVE geometry, route, collision, region or hero asset.
"""
from __future__ import annotations

import bpy

CLAIM = "CLM-SYLVA-MACRO-001"
R14_CONTRACT = "SYLVA_STREAM_HIERARCHY_R14"
R15_POLICY_CONTRACT = "SYLVA_PREFETCH_POLICY_R15"
POLICY_STATE = "RUNTIME_EXPERIMENT_REQUIRED"
CANDIDATES = [
    "P0_CURRENT_ONLY",
    "P1_CURRENT_PLUS_4",
    "P2_CURRENT_PLUS_8",
    "P3_DIRECTIONAL_ROUTE_WINDOW",
]
EXPERIMENT_SOURCE = "PREFETCH_POLICY_R14_EXPERIMENT.json"
PRESSURE_SOURCE = "qa/R14_PREFETCH_PRESSURE_STUDY.json"


def main():
    root = bpy.data.objects.get("SYLVA_WORLD_ROOT")
    meta = bpy.data.objects.get("SYLVA_META_StreamHierarchyR14")
    if not root or root.get("build_status") != "WAVE1L_STREAM_HIERARCHY_R14":
        raise RuntimeError("Expected accepted R14 scene before R15 normalization")
    if not meta or meta.get("contract") != R14_CONTRACT:
        raise RuntimeError("Missing/invalid R14 hierarchy metadata")

    l3 = sorted(
        [o for o in bpy.data.objects if o.name.startswith("SYLVA_STREAM_L3_")],
        key=lambda o: o.name,
    )
    if len(l3) != 16:
        raise RuntimeError(f"Expected 16 L3 cells, got {len(l3)}")

    # Preserve hierarchy contract; normalize only policy semantics.
    for cell in l3:
        if cell.get("stream_hierarchy_contract") != R14_CONTRACT:
            raise RuntimeError("L3 hierarchy contract drift: " + cell.name)
        cell["prefetch_policy"] = POLICY_STATE
        cell["prefetch_policy_contract"] = R15_POLICY_CONTRACT
        cell["prefetch_candidate_ids"] = "|".join(CANDIDATES)
        cell["prefetch_primary_runtime_candidate"] = "P3_DIRECTIONAL_ROUTE_WINDOW"
        cell["prefetch_policy_approved"] = False
        cell["prefetch_experiment_source"] = EXPERIMENT_SOURCE
        cell["prefetch_pressure_source"] = PRESSURE_SOURCE

    meta["prefetch_policy"] = POLICY_STATE
    meta["prefetch_policy_contract"] = R15_POLICY_CONTRACT
    meta["prefetch_candidate_ids"] = "|".join(CANDIDATES)
    meta["prefetch_primary_runtime_candidate"] = "P3_DIRECTIONAL_ROUTE_WINDOW"
    meta["prefetch_policy_approved"] = False
    meta["prefetch_selection_rule"] = (
        "PROMOTE_LEAST_RESIDENT_POLICY_THAT_PASSES_RUNTIME_VISUAL_COLLISION_TRAVERSAL_GATES"
    )
    meta["prefetch_experiment_source"] = EXPERIMENT_SOURCE
    meta["prefetch_pressure_source"] = PRESSURE_SOURCE
    meta["current_plus8_world_fraction_upper_bound_observed"] = 0.728

    root["build_status"] = "WAVE1M_PREFETCH_POLICY_NORMALIZATION_R15"
    root["prefetch_policy_contract"] = R15_POLICY_CONTRACT
    root["prefetch_policy_approved"] = False

    # Hero residency remains explicit L3 overlay and is not changed here.
    for region_name in (
        "SYLVA_STREAM_REGION_PUERTO_INJERTO",
        "SYLVA_STREAM_REGION_BOSQUE_FRASES",
        "SYLVA_STREAM_REGION_CAMARA_VESPER",
    ):
        region = bpy.data.objects.get(region_name)
        if not region or region.get("hero_residency_policy") != "L3_OVERLAY_DO_NOT_MOVE_GEOGRAPHY":
            raise RuntimeError("Hero residency contract drift: " + region_name)
        region["prefetch_policy_contract"] = R15_POLICY_CONTRACT
        region["prefetch_policy_approved"] = False

    bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
    return {
        "status": "R15_PREFETCH_POLICY_NORMALIZED",
        "hierarchy_contract_retained": R14_CONTRACT,
        "prefetch_policy_contract": R15_POLICY_CONTRACT,
        "policy_state": POLICY_STATE,
        "candidates": CANDIDATES,
        "primary_runtime_candidate": "P3_DIRECTIONAL_ROUTE_WINDOW",
        "production_policy_approved": False,
        "geometry_changed": False,
        "l3_cells_updated": len(l3),
    }


if __name__ == "__main__":
    print(main())
