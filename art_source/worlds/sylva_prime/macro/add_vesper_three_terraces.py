"""SYLVA PRIME macro encounter-layout correction for Cámara de VESPER.

Run after:
1. generate_sylva_macro.py
2. add_sylva_macro_interfaces.py

Scope: CLM-SYLVA-MACRO-001 only.
This creates macro encounter-layout proxies, not final VESPER art and not reusable
meso root-kit modules (owned by CLM-SYLVA-PROC-NROOT-001 / PR #6).
"""
from __future__ import annotations

import bpy
import math
from mathutils import Vector

CLAIM = "CLM-SYLVA-MACRO-001"
CANON_SUMMARY = (
    "Three terraces connected by wide roots; vertical traversal uses routes/anchors, "
    "not surprise precision jumps."
)


def ensure_col(name: str):
    scene = bpy.context.scene
    col = bpy.data.collections.get(name)
    if col is None:
        col = bpy.data.collections.new(name)
        scene.collection.children.link(col)
    return col


def material(name, base, metallic=0.0, roughness=0.8, emission=None, strength=0.0):
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*base, 1.0)
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = roughness
    if emission:
        if "Emission Color" in bsdf.inputs:
            bsdf.inputs["Emission Color"].default_value = (*emission, 1.0)
        elif "Emission" in bsdf.inputs:
            bsdf.inputs["Emission"].default_value = (*emission, 1.0)
        if "Emission Strength" in bsdf.inputs:
            bsdf.inputs["Emission Strength"].default_value = strength
    return mat


def move_to(obj, col):
    for old in list(obj.users_collection):
        old.objects.unlink(obj)
    col.objects.link(obj)


def assign(obj, mat):
    if len(obj.data.materials) == 0:
        obj.data.materials.append(mat)


def cylinder(name, loc, radius, depth, mat, col, vertices=48):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=loc)
    obj = bpy.context.object
    obj.name = name
    move_to(obj, col)
    assign(obj, mat)
    return obj


def cube_between(name, a, b, width, thickness, mat, col):
    a, b = Vector(a), Vector(b)
    delta = b - a
    obj_mid = (a + b) * 0.5
    bpy.ops.mesh.primitive_cube_add(location=obj_mid)
    obj = bpy.context.object
    obj.name = name
    obj.scale = (delta.length * 0.5, width * 0.5, thickness * 0.5)
    obj.rotation_mode = "QUATERNION"
    obj.rotation_quaternion = delta.to_track_quat("X", "Z")
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    move_to(obj, col)
    assign(obj, mat)
    return obj


def add_empty(name, loc, props, col, size=20.0):
    obj = bpy.data.objects.new(name, None)
    obj.location = loc
    obj.empty_display_type = "SPHERE"
    obj.empty_display_size = size
    col.objects.link(obj)
    for key, value in props.items():
        obj[key] = value
    return obj


def build():
    vesper_col = ensure_col("SYLVA_50_CAMARA_VESPER")
    collision_col = ensure_col("SYLVA_65_COLLISION_ENVELOPES")
    meta_col = ensure_col("SYLVA_00_META")

    soil = material("SYLVA_DIAG_Soil", (0.018, 0.035, 0.022), roughness=0.96)
    root = material("SYLVA_DIAG_RootFiber", (0.055, 0.095, 0.045), roughness=0.86)
    cyan = material(
        "SYLVA_DIAG_MemorySignal", (0.02, 0.09, 0.10), metallic=0.18, roughness=0.38,
        emission=(0.03, 0.70, 0.82), strength=3.2,
    )
    colmat = material("SYLVA_PREVIEW_MacroCollision", (0.36, 0.02, 0.30), metallic=0.05, roughness=0.72)

    # Replace the obsolete single circular arena proxy.
    for name in ("SYLVA_VESPER_ProxyArenaFloor", "SYLVA_COL_VESPER_ArenaFloor"):
        obj = bpy.data.objects.get(name)
        if obj:
            bpy.data.objects.remove(obj, do_unlink=True)

    # Idempotent r5 rebuild.
    prefixes = (
        "SYLVA_VESPER_Terrace_",
        "SYLVA_VESPER_TerraceConnector_",
        "SYLVA_COL_VESPER_Terrace_",
        "SYLVA_COL_VESPER_Connector_",
    )
    for obj in list(bpy.data.objects):
        if obj.name.startswith(prefixes) or obj.name == "SYLVA_META_VESPER_ThreeTerraceLayout":
            bpy.data.objects.remove(obj, do_unlink=True)

    terraces = [
        {"id": "00_ENTRY", "center": Vector((3115.0, 2190.0, -246.0)), "radius": 58.0},
        {"id": "01_MIDDLE", "center": Vector((3200.0, 2300.0, -216.0)), "radius": 62.0},
        {"id": "02_UPPER", "center": Vector((3290.0, 2410.0, -184.0)), "radius": 56.0},
    ]

    for terrace in terraces:
        center = terrace["center"]
        tid = terrace["id"]
        radius = terrace["radius"]
        visible = cylinder(f"SYLVA_VESPER_Terrace_{tid}", center, radius, 8.0, soil, vesper_col, 48)
        visible["classification"] = "MACRO_ENCOUNTER_LAYOUT_PROXY"
        visible["canon_role"] = "one_of_three_terraces"
        visible["owner_claim"] = CLAIM
        visible["final_art"] = False

        bpy.ops.mesh.primitive_torus_add(
            major_radius=radius * 0.84,
            minor_radius=1.5,
            major_segments=48,
            minor_segments=6,
            location=(center.x, center.y, center.z + 5.0),
        )
        ring = bpy.context.object
        ring.name = f"SYLVA_VESPER_Terrace_{tid}_SignalRing"
        move_to(ring, vesper_col)
        assign(ring, cyan)
        ring["classification"] = "DIAGNOSTIC_ROUTE_SIGNAL"

        coll = cylinder(
            f"SYLVA_COL_VESPER_Terrace_{tid}",
            (center.x, center.y, center.z - 1.0),
            radius * 0.96,
            7.0,
            colmat,
            collision_col,
            32,
        )
        coll["collision_policy"] = "CYLINDER_PROXY"
        coll["owner_claim"] = CLAIM
        coll["source_layout"] = visible.name

    connector_receipts = []
    for index in range(2):
        a, b = terraces[index]["center"], terraces[index + 1]["center"]
        delta = b - a
        horizontal = math.sqrt(delta.x * delta.x + delta.y * delta.y)
        slope_deg = math.degrees(math.atan2(abs(delta.z), horizontal))

        visible = cube_between(
            f"SYLVA_VESPER_TerraceConnector_{index:02d}", a, b, 18.0, 5.0, root, vesper_col
        )
        visible["classification"] = "MACRO_WIDE_ROOT_ROUTE_PROXY"
        visible["owner_claim"] = CLAIM
        visible["final_root_module"] = False
        visible["precision_jump_required"] = False
        visible["slope_deg"] = slope_deg
        visible["width_m"] = 18.0

        coll = cube_between(
            f"SYLVA_COL_VESPER_Connector_{index:02d}", a, b, 16.0, 3.5, colmat, collision_col
        )
        coll["collision_policy"] = "BOX_ROUTE_PROXY"
        coll["owner_claim"] = CLAIM
        coll["source_layout"] = visible.name
        coll["slope_deg"] = slope_deg
        coll["clear_width_m"] = 16.0
        coll["precision_jump_required"] = False

        connector_receipts.append(
            {
                "id": index,
                "length_m": round(delta.length, 3),
                "horizontal_m": round(horizontal, 3),
                "vertical_delta_m": round(delta.z, 3),
                "slope_deg": round(slope_deg, 3),
                "visual_width_m": 18.0,
                "collision_width_m": 16.0,
            }
        )

    add_empty(
        "SYLVA_META_VESPER_ThreeTerraceLayout",
        (3200, 2300, -216),
        {
            "classification": "CANON_ALIGNED_MACRO_LAYOUT_PROXY",
            "owner_claim": CLAIM,
            "terrace_count": 3,
            "connector_count": 2,
            "wide_root_routes": True,
            "precision_jumps_required": False,
            "final_boss_mesh": "EXCLUDED",
            "canon_summary": CANON_SUMMARY,
        },
        meta_col,
        30,
    )

    root_obj = bpy.data.objects.get("SYLVA_WORLD_ROOT")
    if root_obj:
        root_obj["build_status"] = "WAVE1C_VESPER_THREE_TERRACES_R5"
        root_obj["vesper_terrace_count"] = 3
        root_obj["vesper_connector_count"] = 2
        root_obj["vesper_precision_jumps_required"] = False
        root_obj["collision_proxy_count"] = len(
            [obj for obj in bpy.data.objects if obj.name.startswith("SYLVA_COL_")]
        )

    bpy.ops.object.select_all(action="DESELECT")
    return {
        "terraces": 3,
        "connectors": 2,
        "connector_metrics": connector_receipts,
        "precision_jumps_required": False,
        "final_vesper_created": False,
    }


if __name__ == "__main__":
    print(build())
