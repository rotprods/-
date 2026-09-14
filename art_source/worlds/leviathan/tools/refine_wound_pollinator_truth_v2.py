"""EXOVANT 2950 — LEVIATHAN wound pollinator truth/placement refinement v2.

Corrects two QA findings from representative v1 without changing anatomy:
1. v1 metadata said body length 2.4 m while measured head/thorax/abdomen/reservoir envelope is 2.67 m.
2. v1 root y=88 m placed the aft envelope slightly outside the existing Jardines hero-Y bounds.

This stage moves the complete pollinator root +4 m in Y, moves its QA camera by the same delta,
and truth-labels the measured body envelope. Dimensions remain production proposals, not canon.
"""
import bpy

STAGE = "WOUND_POLLINATOR_TRUTH_REFINEMENT_V2"
ROOT = "R2_HPOLL_ROOT"
CAM = "CAM_R2_POLLINATOR_CLOSE"
MEASURED_BODY_LENGTH_Y_M = 2.67
TARGET_ROOT_Y_M = 92.0


def build():
    scene = bpy.context.scene
    root = bpy.data.objects.get(ROOT)
    cam = bpy.data.objects.get(CAM)
    if root is None or cam is None:
        raise RuntimeError("Pollinator root/camera missing; run v1 first")
    dy = TARGET_ROOT_Y_M - float(root.location.y)
    root.location.y = TARGET_ROOT_Y_M
    cam.location.y += dy
    root["body_length_m_proposal"] = MEASURED_BODY_LENGTH_Y_M
    root["measured_body_length_y_m"] = MEASURED_BODY_LENGTH_Y_M
    root["body_length_contract"] = "MEASURED_HEAD_TO_RESERVOIR_ENVELOPE"
    root["placement_status"] = "REFINED_INSIDE_EXISTING_JARDINES_HERO_Y_RANGE"
    root["dimension_status"] = "MEASURED_PROPOSAL_NOT_CANON"
    root["generator_stage"] = STAGE
    scene["wound_pollinator_stage"] = STAGE
    scene["wound_pollinator_body_length_y_m"] = MEASURED_BODY_LENGTH_Y_M
    scene["wound_pollinator_dimensions_final_claimed"] = False
    return {
        "stage": STAGE,
        "asset_id": root.get("asset_id"),
        "root_y_m": float(root.location.y),
        "camera_y_m": float(cam.location.y),
        "applied_delta_y_m": dy,
        "measured_body_length_y_m": MEASURED_BODY_LENGTH_Y_M,
        "wingspan_m": float(root.get("wingspan_m_proposal")),
        "status": "TRUTH_REFINED_REPRESENTATIVE_NOT_FINAL",
    }

if __name__ == "__main__":
    print(build())
