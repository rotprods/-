"""ELYSIUM NULL — EDEN collision + Reubicacion motion stage.

Expected input: ELYSIUM World Master after EDEN_STATE_GRAPH stage (revision-3 equivalent).
Blender observed target: 5.2.0 LTS. Metric units, 1 BU = 1 m.

Canon retained:
- EDEN arena diameter: 48 m.
- Reubicacion destination warning: 1.5 s.

Proposal introduced here:
- 8x8 m movable garden bodies inherited from W1 state-graph candidate.
- 1.0 s physical A->B travel after the warning.
- two-axis linear actuator sled/rail mechanism.
- simplified base + topiary collision proxies.

This script does NOT implement Godot/Unreal gameplay. It authors an editable
Blender motion/collision contract for later engine integration.
"""

import bpy
from mathutils import Matrix

scene = bpy.context.scene
scene.render.fps = 24
scene.frame_start = 1
scene.frame_end = 108


def ensure_collection(name):
    col = bpy.data.collections.get(name) or bpy.data.collections.new(name)
    if scene.collection.children.get(col.name) is None:
        scene.collection.children.link(col)
    return col


MECH = ensure_collection("41_EDEN_MECHANISM")
COLL = ensure_collection("42_EDEN_COLLISION")
META = ensure_collection("43_EDEN_MOTION_META")


def move_to(obj, collection):
    for old in list(obj.users_collection):
        old.objects.unlink(obj)
    collection.objects.link(obj)


def box(name, location, dimensions, material=None, collection=None, bevel=0.0):
    bpy.ops.mesh.primitive_cube_add(location=location)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = dimensions
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if material:
        obj.data.materials.append(material)
    if collection:
        move_to(obj, collection)
    if bevel:
        mod = obj.modifiers.new("Bevel_physical", "BEVEL")
        mod.width = bevel
        mod.segments = 2
    return obj


def cylinder(name, location, radius, depth, material=None, collection=None, vertices=24):
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=vertices,
        radius=radius,
        depth=depth,
        location=location,
    )
    obj = bpy.context.object
    obj.name = name
    if material:
        obj.data.materials.append(material)
    if collection:
        move_to(obj, collection)
    return obj


DARK = bpy.data.materials["MAT_Elysium_Recess_PROPOSAL"]
METAL = bpy.data.materials["MAT_Elysium_SatinMetal_PROPOSAL"]
AMBER = bpy.data.materials["MAT_Elysium_ServiceAmber_PROPOSAL"]
COLMAT = bpy.data.materials.get("MAT_COLLISION_DEBUG") or bpy.data.materials.new("MAT_COLLISION_DEBUG")
COLMAT.diffuse_color = (0.8, 0.12, 0.08, 0.35)

# Layouts from EDEN_STATE_GRAPH v0.1.
A = [(-10, 101, 0), (10, 101, 0), (-10, 115, 0), (10, 115, 0)]
B = [(-14, 101, 0), (14, 101, 0), (-14, 115, 0), (14, 115, 0)]
C = [(-10, 97, 0), (10, 97, 0), (-10, 119, 0), (10, 119, 0)]

roots = []
for i, origin in enumerate(A):
    root = bpy.data.objects.new(f"EDEN_MODULE_ROOT_{i:02d}", None)
    root.location = origin
    META.objects.link(root)
    root["module_id"] = f"ELYS-LVL-EDN-MOD-{i:02d}"
    root["motion_role"] = "KINEMATIC_ROOT"
    root["state_A"] = A[i]
    root["state_B"] = B[i]
    root["state_C"] = C[i]
    roots.append(root)

    # Existing W0 visible components become explicit local children. Using known
    # local offsets avoids transform doubling when roots animate.
    local_components = {
        f"EDEN_MOVABLE_GARDEN_{i:02d}": (0, 0, 0.80),
        f"EDEN_MOVABLE_GARDEN_{i:02d}_SOIL": (0, 0, 1.54),
        f"EDEN_MOVABLE_GARDEN_{i:02d}_TOPIARY": (0, 0, 3.00),
    }
    for child_name, local_position in local_components.items():
        child = bpy.data.objects[child_name]
        child.parent = root
        child.matrix_parent_inverse = Matrix.Identity(4)
        child.location = local_position
        child["root_local_contract"] = "EXPLICIT_LOCAL_COORDINATE"

    ax, ay, _ = origin

    sled = box(
        f"EDEN_ACTUATOR_SLED_{i:02d}",
        (ax, ay, 0.22),
        (6.4, 6.4, 0.28),
        METAL,
        MECH,
        0.08,
    )
    sled.parent = root
    sled.matrix_parent_inverse = Matrix.Identity(4)
    sled.location = (0, 0, 0.22)
    sled["mechanism"] = "2_AXIS_LINEAR_ACTUATOR_SLED"

    xmin = min(A[i][0], B[i][0], C[i][0]) - 5
    xmax = max(A[i][0], B[i][0], C[i][0]) + 5
    ymin = min(A[i][1], B[i][1], C[i][1]) - 5
    ymax = max(A[i][1], B[i][1], C[i][1]) + 5

    box(
        f"EDEN_RAIL_X_{i:02d}",
        ((xmin + xmax) / 2, ay, 0.05),
        (xmax - xmin, 0.34, 0.12),
        DARK,
        MECH,
        0.03,
    )
    box(
        f"EDEN_RAIL_Y_{i:02d}",
        (ax, (ymin + ymax) / 2, 0.06),
        (0.34, ymax - ymin, 0.12),
        DARK,
        MECH,
        0.03,
    )
    box(
        f"EDEN_ACTUATOR_SERVICE_NODE_{i:02d}",
        (ax, ay, 0.38),
        (1.1, 1.1, 0.22),
        AMBER,
        MECH,
        0.08,
    )

    base_col = box(
        f"COL_EDEN_GARDEN_{i:02d}_BASE",
        (ax, ay, 0.80),
        (7.6, 7.6, 1.35),
        COLMAT,
        COLL,
        0.12,
    )
    base_col.parent = root
    base_col.matrix_parent_inverse = Matrix.Identity(4)
    base_col.location = (0, 0, 0.80)
    base_col.hide_render = True
    base_col.display_type = "WIRE"
    base_col["collision_role"] = "GAMEPLAY_BASE_PROXY"
    base_col["shape"] = "BOX"
    base_col["asset_id"] = f"ELYS-COL-EDN-{i:02d}-BASE"

    top_col = cylinder(
        f"COL_EDEN_GARDEN_{i:02d}_TOPIARY",
        (ax, ay, 3.00),
        1.35,
        2.8,
        COLMAT,
        COLL,
        20,
    )
    top_col.parent = root
    top_col.matrix_parent_inverse = Matrix.Identity(4)
    top_col.location = (0, 0, 3.00)
    top_col.hide_render = True
    top_col.display_type = "WIRE"
    top_col["collision_role"] = "GAMEPLAY_TOPIARY_PROXY"
    top_col["shape"] = "CYLINDER"
    top_col["asset_id"] = f"ELYS-COL-EDN-{i:02d}-TOP"

# Timeline: stable A, canonical warning, distinct physical movement, stable B.
for i, root in enumerate(roots):
    root.location = A[i]
    for frame in (1, 24, 25, 60, 61):
        root.keyframe_insert("location", frame=frame)
    root.location = B[i]
    for frame in (84, 108):
        root.keyframe_insert("location", frame=frame)

meta = bpy.data.objects.new("META_EDEN_REUBICACION_R4", None)
META.objects.link(meta)
meta["canonical_warning_s"] = 1.5
meta["fps"] = 24
meta["warning_frames"] = 36
meta["movement_duration_proposal_s"] = 1.0
meta["movement_frames"] = 24
meta["collision_proxy_count"] = 8
meta["motion_state"] = "A_TO_B"
meta["runtime_implementation"] = "PENDING_TARGET_ENGINE"

# Static architecture clearance evidence from current Godot prototype.
meta["prototype_player_capsule_radius_m"] = 0.38
meta["prototype_player_capsule_height_m"] = 1.85
meta["architecture_door_width_m"] = 2.4
meta["architecture_door_height_m"] = 2.7
meta["door_static_geometry_fit"] = "PASS"
meta["dynamic_traversal"] = "PENDING_NATIVE_ENGINE"

print(
    {
        "status": "EDEN_COLLISION_MOTION_STAGE_BUILT",
        "roots": 4,
        "collision_proxies": 8,
        "canonical_warning_s": 1.5,
        "warning_frames": 36,
        "movement_s_proposal": 1.0,
        "movement_frames": 24,
        "runtime": "PENDING",
    }
)
