"""ELYSIUM NULL — W1 modular architecture stage.

Precondition:
- Run after generate_foundation.py or against a scene containing the W0 material roles.

This stage is deliberately additive and keeps its geometry in `60_W1_ARCH_KIT`.
All grid/clearance dimensions are PROPOSAL until runtime-controller validation.
"""

import bpy
from mathutils import Vector

scene = bpy.context.scene


def get_collection(name):
    col = bpy.data.collections.get(name) or bpy.data.collections.new(name)
    if scene.collection.children.get(col.name) is None:
        scene.collection.children.link(col)
    return col


COL = get_collection("60_W1_ARCH_KIT")


def move_to(obj, target):
    for old in list(obj.users_collection):
        old.objects.unlink(obj)
    target.objects.link(obj)


def box(name, location, dimensions, material, bevel=0.0):
    bpy.ops.mesh.primitive_cube_add(location=location)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = dimensions
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.data.materials.append(material)
    move_to(obj, COL)
    if bevel:
        mod = obj.modifiers.new("Bevel_physical", "BEVEL")
        mod.width = bevel
        mod.segments = 3
    return obj


def linked_copy(proto, name, location, rotation=(0, 0, 0)):
    obj = bpy.data.objects.new(name, proto.data)
    obj.location = location
    obj.rotation_euler = rotation
    COL.objects.link(obj)
    return obj


def look_at(obj, target):
    obj.rotation_euler = (Vector(target) - obj.location).to_track_quat("-Z", "Y").to_euler()


WHITE = bpy.data.materials["MAT_Elysium_WhiteCeramic_PROPOSAL"]
DARK = bpy.data.materials["MAT_Elysium_Recess_PROPOSAL"]
METAL = bpy.data.materials["MAT_Elysium_SatinMetal_PROPOSAL"]

bpy.ops.object.empty_add(type="PLAIN_AXES", location=(0, 0, 0))
root = bpy.context.object
root.name = "META_W1_ARCH_GRID_PROPOSAL"
move_to(root, COL)
root["status"] = "PROPOSAL"
root["planning_grid_m"] = 1.0
root["primary_bay_m"] = 4.0
root["span_family_m"] = "8,12,16"
root["player_clearance_validation"] = "PENDING_RUNTIME_CONTROLLER"

column = box("KIT_COL_0p4x0p4x4_PROTO", (48, -108, 2), (0.4, 0.4, 4), METAL, 0.05)
column["module_id"] = "ELYS-ARCH-MOD-COL-040-400"
column["grid_m"] = 1.0

beam = box("KIT_BEAM_4x0p4x0p5_PROTO", (52, -108, 4.15), (4, 0.4, 0.5), METAL, 0.05)
beam["module_id"] = "ELYS-ARCH-MOD-BEAM-400"

panel = box("KIT_PANEL_SOLID_4x4_PROTO", (58, -108, 2), (4, 0.24, 4), WHITE, 0.08)
panel["module_id"] = "ELYS-ARCH-MOD-PANEL-SOLID-400"

reveal = box("KIT_PANEL_REVEAL_4x4_PROTO", (64, -108, 2), (4, 0.24, 4), WHITE, 0.08)
reveal["module_id"] = "ELYS-ARCH-MOD-PANEL-REVEAL-400"
box("KIT_PANEL_REVEAL_SHADOW", (64, -108.135, 2), (0.16, 0.05, 3.55), DARK, 0.01)

# 2.4 × 2.7 m clear door candidate.
box("KIT_DOOR_SHADOW_2p4x2p7", (70, -108.14, 1.35), (2.4, 0.05, 2.7), DARK, 0.02)
box("KIT_DOOR_JAMB_L", (68.65, -108, 1.6), (0.3, 0.28, 3.2), WHITE, 0.06)
box("KIT_DOOR_JAMB_R", (71.35, -108, 1.6), (0.3, 0.28, 3.2), WHITE, 0.06)
box("KIT_DOOR_HEADER", (70, -108, 3.05), (3.0, 0.28, 0.3), WHITE, 0.06)

box("KIT_SERVICE_HATCH_1p2", (48, -100, 1.15), (1.2, 0.18, 1.2), DARK, 0.04)
box("KIT_SERVICE_HATCH_FRAME", (48, -99.88, 1.15), (1.45, 0.12, 1.45), METAL, 0.05)

for index, span in enumerate((8, 12, 16)):
    obj = box(f"KIT_SPAN_{span:02d}M", (56 + index * 2, -96 + index * 6, 5.0), (span, 0.45, 0.65), WHITE, 0.12)
    obj["module_id"] = f"ELYS-ARCH-MOD-SPAN-{span:02d}M"
    obj["span_m"] = span

box("KIT_CANOPY_4M", (48, -88, 3.15), (4, 4, 0.28), WHITE, 0.10)
box("KIT_CANOPY_SERVICE_RIB", (48, -88, 2.92), (0.28, 4, 0.18), METAL, 0.04)

# A single mesh shared by 32 arrival façade object instances.
facade = box("KIT_FACADE_TILE_3p8x3p6_PROTO", (48, -78, 1.8), (0.24, 3.8, 3.6), WHITE, 0.07)
facade.hide_render = True
facade.hide_viewport = True
facade["module_id"] = "ELYS-ARCH-MOD-FACADE-380x360"

for side in (-1, 1):
    x = side * 17.86
    side_name = "W" if side < 0 else "E"
    for row, z in enumerate((2.0, 5.8, 9.6, 13.4)):
        for col_index, y in enumerate((-95.7, -91.8, -87.9, -84.0)):
            obj = linked_copy(facade, f"ARC_ARRIVAL_{side_name}_FACADE_R{row}C{col_index}", (x, y, z))
            obj["module_source"] = "ELYS-ARCH-MOD-FACADE-380x360"
            obj["grid_bay_m"] = 4.0

# Door readability at both inward-facing arrival cores.
for side in (-1, 1):
    x = side * 17.68
    side_name = "W" if side < 0 else "E"
    box(f"ARC_ARRIVAL_{side_name}_DOOR_SHADOW", (x, -90, 1.35), (0.08, 2.4, 2.7), DARK, 0.01)
    box(f"ARC_ARRIVAL_{side_name}_DOOR_HEADER", (x - side * 0.02, -90, 2.82), (0.18, 3.0, 0.22), METAL, 0.03)
    for y in (-91.35, -88.65):
        box(f"ARC_ARRIVAL_{side_name}_DOOR_JAMB_{y:+.2f}", (x - side * 0.02, y, 1.45), (0.18, 0.22, 2.9), METAL, 0.03)

# Dedicated detail camera for review.
bpy.ops.object.camera_add(location=(39, -116, 18))
camera = bpy.context.object
camera.name = "CAM_W1_ARCH_DETAIL"
camera.data.lens = 52
look_at(camera, (18, -90, 7))
move_to(camera, bpy.data.collections["90_LIGHTS_CAM"])

facades = [obj for obj in bpy.data.objects if obj.name.startswith("ARC_ARRIVAL_") and "_FACADE_" in obj.name]
print(
    {
        "status": "W1_ARCH_KIT_V1",
        "objects_in_kit_collection": len(COL.objects),
        "facade_instances": len(facades),
        "facade_shared_mesh_users": facade.data.users,
        "all_facades_share_mesh": all(obj.data == facade.data for obj in facades),
        "planning_grid_m": 1.0,
        "bay_m": 4.0,
        "spans_m": [8, 12, 16],
        "door_clearance_proposal_m": [2.4, 2.7],
    }
)
