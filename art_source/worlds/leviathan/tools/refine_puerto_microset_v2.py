"""EXOVANT 2950 — LEVIATHAN Puerto microset refinement v2.

Deterministic corrective stage after build_puerto_microset.py.
Receipt-driving defect: revision-4 service door was 4.35 m tall (2.35x the
1.85 m human reference) and its sill floated above the pressure-core floor.

This stage corrects scale/contact without changing the 24 x 12 x 10 m
module envelope or any cross-scope asset.
"""

import bpy

STAGE = "PUERTO_MICROSET_REFINEMENT_V2"
SOURCE_DEFECT = "R1_HG_A_DOOR height 4.35m / floating sill"


def build():
    scene = bpy.context.scene
    required = [
        "R1_HG_A_DOOR",
        "R1_HG_A_DOOR_FRAME_TOP",
        "R1_HG_A_DOOR_FRAME_L",
        "R1_HG_A_DOOR_FRAME_R",
        "R1_HG_A_DOOR_HANDLE",
        "R1_HG_A_PRESSURE_CORE",
        "REF_HUMAN_1P85M",
    ]
    missing = [n for n in required if n not in bpy.data.objects]
    if missing:
        raise RuntimeError(f"Puerto microset v1 required before refinement: {missing}")

    door = bpy.data.objects["R1_HG_A_DOOR"]
    top = bpy.data.objects["R1_HG_A_DOOR_FRAME_TOP"]
    left = bpy.data.objects["R1_HG_A_DOOR_FRAME_L"]
    right = bpy.data.objects["R1_HG_A_DOOR_FRAME_R"]
    handle = bpy.data.objects["R1_HG_A_DOOR_HANDLE"]
    core = bpy.data.objects["R1_HG_A_PRESSURE_CORE"]

    # Pressure-core lower surface = 9.0 - 9.1/2 = 4.45 m.
    # Service aperture gets a 0.10 m structural sill and 2.60 m clear leaf.
    floor_z = core.location.z - core.dimensions.z * 0.5
    sill_z = floor_z + 0.10
    door_h = 2.60
    door_w = 1.60
    door_center_z = sill_z + door_h * 0.5

    door.location.z = door_center_z
    door.dimensions = (0.28, door_w, door_h)

    frame_side_h = door_h + 0.30
    frame_center_z = sill_z + frame_side_h * 0.5
    left.location.y = -100.0 - (door_w * 0.5 + 0.17)
    right.location.y = -100.0 + (door_w * 0.5 + 0.17)
    left.location.z = frame_center_z
    right.location.z = frame_center_z
    left.dimensions = (0.22, 0.22, frame_side_h)
    right.dimensions = (0.22, 0.22, frame_side_h)

    top.location.z = sill_z + door_h + 0.17
    top.dimensions = (0.22, door_w + 0.56, 0.25)

    handle.location.y = -100.0 + 0.52
    handle.location.z = door_center_z

    # Re-apply dimensions to mesh data so object scale stays 1,1,1.
    for obj in (door, top, left, right):
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        obj.select_set(False)

    door["real_dimensions_m"] = [0.28, door_w, door_h]
    door["human_scale_reference_m"] = 1.85
    door["clearance_ratio_to_human"] = door_h / 1.85
    door["sill_z_m"] = sill_z
    door["scale_defect_fixed"] = SOURCE_DEFECT

    scene["puerto_microset_refinement_stage"] = STAGE

    return {
        "stage": STAGE,
        "door_dimensions_m": [round(float(x), 3) for x in door.dimensions],
        "door_bottom_z_m": round(float(door.location.z - door.dimensions.z * 0.5), 3),
        "core_bottom_z_m": round(float(floor_z), 3),
        "sill_offset_m": round(float((door.location.z - door.dimensions.z * 0.5) - floor_z), 3),
        "door_height_over_human": round(float(door.dimensions.z / 1.85), 3),
        "status": "SCALE_CONTACT_CORRECTED"
    }


if __name__ == "__main__":
    print(build())
