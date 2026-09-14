"""EXOVANT 2950 — LEVIATHAN Jardines truth refinement v2.

No art-shape change. Corrects semantic measurement labels discovered by r6 QA:
- 2.6 m is the gardener core-body length, not the full articulated envelope.
- 34 m is the stable service-walk length, not the complete visual conduit extent.
- current gardener collision is core-only provisional until a rig/gameplay hit model exists.
"""

import bpy
from mathutils import Vector

STAGE = "JARDINES_TRUTH_REFINEMENT_V2"


def _bounds(prefix):
    scene = bpy.context.scene
    objs = [o for o in scene.objects if o.name.startswith(prefix)]
    deps = bpy.context.evaluated_depsgraph_get()
    mins = Vector((1e9, 1e9, 1e9))
    maxs = Vector((-1e9, -1e9, -1e9))
    for obj in objs:
        eo = obj.evaluated_get(deps)
        for corner in eo.bound_box:
            p = eo.matrix_world @ Vector(corner)
            mins.x = min(mins.x, p.x); mins.y = min(mins.y, p.y); mins.z = min(mins.z, p.z)
            maxs.x = max(maxs.x, p.x); maxs.y = max(maxs.y, p.y); maxs.z = max(maxs.z, p.z)
    return [round(float(x), 3) for x in (maxs - mins)]


def build():
    scene = bpy.context.scene
    channel = bpy.data.objects["R2_HERO_LYMPH_CHANNEL_ROOT"]
    gardener = bpy.data.objects["R2_HERO_GARDENER_PARASITE_ROOT"]
    collision = bpy.data.objects["COLL_R2_GARDENER_REPRESENTATIVE"]

    channel_bounds = _bounds("R2_HLC_")
    gardener_bounds = _bounds("R2_HGP_")

    if "representative_length_m" in channel:
        del channel["representative_length_m"]
    channel["stable_service_walk_length_m"] = 34.0
    channel["visual_conduit_measured_envelope_m"] = channel_bounds
    channel["visual_envelope_note"] = "visual anatomy exceeds stable traversable span; it is not collision authority"

    if "proposed_body_length_m" in gardener:
        del gardener["proposed_body_length_m"]
    gardener["proposed_core_body_length_m"] = 2.6
    gardener["measured_articulated_envelope_m"] = gardener_bounds
    gardener["envelope_note"] = "full envelope includes six limbs, cleaning arms and sensory cilia; dimensions are proposal, not canon"

    collision["collision_role"] = "CORE_ONLY_STATIC_PROXY_NOT_RIGGED"
    collision["does_not_cover_appendages"] = True
    collision["unblock_for_final_collision"] = "approved rig + locomotion + combat/hit contract"

    scene["jardines_truth_refinement_stage"] = STAGE

    return {
        "stage": STAGE,
        "stable_service_walk_length_m": 34.0,
        "visual_conduit_measured_envelope_m": channel_bounds,
        "gardener_core_body_length_m": 2.6,
        "gardener_measured_articulated_envelope_m": gardener_bounds,
        "gardener_collision": "CORE_ONLY_STATIC_PROXY_NOT_RIGGED",
        "status": "TRUTH_METADATA_RECONCILED"
    }


if __name__ == "__main__":
    print(build())
