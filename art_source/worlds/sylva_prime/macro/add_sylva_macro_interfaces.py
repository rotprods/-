"""SYLVA PRIME macro streaming/collision/root-kit interface pass.

Run AFTER generate_sylva_macro.py.
Scope: CLM-SYLVA-MACRO-001 only.
Consumes metadata contract from CLM-SYLVA-PROC-NROOT-001 but never copies/owns its meso root meshes.
All streaming sizes, hero-zone radii, collision proxies and socket placements are PROPOSAL/INTERFACE,
not planetary canon.
"""
from __future__ import annotations

import bpy
import math

PREFIX = "SYLVA_"
CLAIM = "CLM-SYLVA-MACRO-001"
ROOT_CLAIM = "CLM-SYLVA-PROC-NROOT-001"
ROOT_MANIFEST = "production/manifests/sylva/procedural/SYL_NEURAL_ROOT_KIT_001.yaml"
CELL_M = 3000.0  # PROPOSAL
LOCAL_ENVELOPE_M = 12000.0  # PROPOSAL inherited from macro blockout


def _ensure_col(name: str):
    full = PREFIX + name
    col = bpy.data.collections.get(full)
    if col is None:
        col = bpy.data.collections.new(full)
        bpy.context.scene.collection.children.link(col)
    return col


def _clear_col(col):
    for obj in list(col.objects):
        bpy.data.objects.remove(obj, do_unlink=True)


def _empty(name, loc, props, col, size=30.0, display="CUBE"):
    obj = bpy.data.objects.new(name, None)
    obj.location = loc
    obj.empty_display_type = display
    obj.empty_display_size = size
    col.objects.link(obj)
    for key, value in props.items():
        obj[key] = value
    return obj


def _material(name, base, metallic=0.0, rough=0.7):
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*base, 1.0)
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = rough
    return mat


def _assign(obj, material):
    if hasattr(obj.data, "materials") and len(obj.data.materials) == 0:
        obj.data.materials.append(material)


def _move(obj, col):
    for c in list(obj.users_collection):
        c.objects.unlink(obj)
    col.objects.link(obj)


def _cube(name, loc, scale, material, col, rotation_quaternion=None):
    bpy.ops.mesh.primitive_cube_add(location=loc)
    obj = bpy.context.object
    obj.name = name
    obj.scale = scale
    if rotation_quaternion is not None:
        obj.rotation_mode = "QUATERNION"
        obj.rotation_quaternion = rotation_quaternion
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    _move(obj, col)
    _assign(obj, material)
    return obj


def _cylinder(name, loc, radius, depth, material, col, vertices=20):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=loc)
    obj = bpy.context.object
    obj.name = name
    _move(obj, col)
    _assign(obj, material)
    return obj


def _height(x: float, y: float) -> float:
    broad = 180 * math.sin(x / 1500) + 120 * math.cos(y / 1250) + 55 * math.sin((x - y) / 700)
    puerto = 160 * math.exp(-(((x + 3200) / 1300) ** 2 + ((y + 2200) / 1200) ** 2))
    bosque = 240 * math.exp(-(((x - 150) / 2000) ** 2 + ((y - 150) / 1700) ** 2))
    vesper = -460 * math.exp(-(((x - 3200) / 1050) ** 2 + ((y - 2300) / 1000) ** 2))
    return broad + puerto + bosque + vesper


def build_interfaces():
    stream = _ensure_col("05_STREAMING_META")
    sockets = _ensure_col("25_ROOTKIT_SOCKETS")
    collision = _ensure_col("65_COLLISION_ENVELOPES")
    for col in (stream, sockets, collision):
        _clear_col(col)

    _empty(
        "SYLVA_META_RootKitIntegration",
        (0, 0, 0),
        {
            "classification": "INTERFACE",
            "owner_claim": CLAIM,
            "consumes_claim": ROOT_CLAIM,
            "manifest": ROOT_MANIFEST,
            "validated_rootkit_revision": 4,
            "mesh_ownership": "NO_MESO_ROOT_MESH_OWNERSHIP",
        },
        stream,
        20,
        "SPHERE",
    )

    # L3 cell proposal: 4 x 4 cells, 3 km each over the 12 km local authored patch.
    for iy in range(4):
        for ix in range(4):
            cx = -4500.0 + ix * CELL_M
            cy = -4500.0 + iy * CELL_M
            _empty(
                f"SYLVA_STREAM_L3_X{ix}Y{iy}",
                (cx, cy, 0),
                {
                    "classification": "PROPOSAL",
                    "level": "L3_GAMEPLAY_CELL",
                    "cell_size_m": CELL_M,
                    "owner_claim": CLAIM,
                    "render_geometry": False,
                    "streaming_backend": "ENGINE_TBD",
                },
                stream,
                CELL_M * 0.46,
                "CUBE",
            )

    regions = [
        ("PUERTO_INJERTO", (-3200, -2200, 330), 1200.0),
        ("BOSQUE_FRASES", (0, 150, 350), 1700.0),
        ("CAMARA_VESPER", (3200, 2300, -220), 1200.0),
    ]
    for key, loc, radius in regions:
        _empty(
            f"SYLVA_STREAM_REGION_{key}",
            loc,
            {
                "classification": "PROPOSAL",
                "level": "L4_HERO_ZONE_ENVELOPE",
                "radius_m": radius,
                "canonical_region": True,
                "owner_claim": CLAIM,
                "streaming_backend": "ENGINE_TBD",
            },
            stream,
            radius * 0.12,
            "SPHERE",
        )

    # Typed sockets only. Provider meshes stay in PR #6 ownership.
    socket_specs = [
        ("PUERTO_EXIT_A1", (-2860, -1870, 430), "SYL_ROOT_A1_STRAIGHT_08M", 0.45),
        ("PUERTO_MEMBRANE_C3", (-3370, -2050, 505), "SYL_ROOT_C3_MEMBRANE_ANCHOR", 1.20),
        ("BOSQUE_APPROACH_A2", (-820, -380, 500), "SYL_ROOT_A2_CURVE_12M", 0.15),
        ("BOSQUE_FORK_B1", (120, 260, 470), "SYL_ROOT_B1_FORK", 0.05),
        ("BOSQUE_RISE_A3", (780, 850, 520), "SYL_ROOT_A3_RISE_10M", 0.65),
        ("VESPER_APPROACH_A2", (2380, 1650, 210), "SYL_ROOT_A2_CURVE_12M", 0.45),
        ("VESPER_BUTTRESS_C1", (2870, 2500, -120), "SYL_ROOT_C1_BUTTRESS_07M", 1.15),
        ("VESPER_MEMBRANE_C3", (3500, 2490, -10), "SYL_ROOT_C3_MEMBRANE_ANCHOR", 2.10),
    ]
    for name, loc, asset_id, yaw in socket_specs:
        obj = _empty(
            "SYLVA_SOCKET_" + name,
            loc,
            {
                "classification": "INTERFACE",
                "owner_claim": CLAIM,
                "provider_claim": ROOT_CLAIM,
                "provider_asset_id": asset_id,
                "manifest": ROOT_MANIFEST,
                "snap_units": "metres",
                "scale_contract": [1.0, 1.0, 1.0],
                "final_placement_requires_art_review": True,
            },
            sockets,
            24,
            "ARROWS",
        )
        obj.rotation_euler = (0, 0, yaw)

    preview = _material("SYLVA_PREVIEW_MacroCollision", (0.36, 0.02, 0.30), 0.05, 0.72)

    # Low-resolution deterministic collision terrain.
    n = 17
    verts, faces = [], []
    for iy in range(n):
        y = -LOCAL_ENVELOPE_M / 2 + LOCAL_ENVELOPE_M * iy / (n - 1)
        for ix in range(n):
            x = -LOCAL_ENVELOPE_M / 2 + LOCAL_ENVELOPE_M * ix / (n - 1)
            verts.append((x, y, _height(x, y)))
    for iy in range(n - 1):
        for ix in range(n - 1):
            a = iy * n + ix
            faces.append((a, a + 1, a + 1 + n, a + n))
    mesh = bpy.data.meshes.new("SYLVA_COL_Terrain12km_LowRes_Mesh")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    terrain = bpy.data.objects.new("SYLVA_COL_TERRAIN_Macro12km_LowRes_PROPOSAL", mesh)
    collision.objects.link(terrain)
    _assign(terrain, preview)
    terrain["classification"] = "COLLISION_PROXY_PROPOSAL"
    terrain["collision_policy"] = "CUSTOM_LOWRES_HEIGHTFIELD"
    terrain["owner_claim"] = CLAIM
    terrain["renderable_final"] = False

    puerto = _cube("SYLVA_COL_PUERTO_Deck", (-3200, -2200, 352), (150, 95, 6), preview, collision)
    puerto["collision_policy"] = "BOX_PROXY"; puerto["owner_claim"] = CLAIM
    bosque = _cylinder("SYLVA_COL_BOSQUE_CentralPad", (0, 150, 370), 95, 12, preview, collision, 24)
    bosque["collision_policy"] = "CYLINDER_PROXY"; bosque["owner_claim"] = CLAIM
    vesper = _cylinder("SYLVA_COL_VESPER_ArenaFloor", (3200, 2300, -266), 92, 10, preview, collision, 32)
    vesper["collision_policy"] = "CYLINDER_PROXY"; vesper["owner_claim"] = CLAIM

    for i in range(4):
        source = bpy.data.objects.get(f"SYLVA_TRAV_PathGuide_{i:02d}")
        if source is None:
            continue
        proxy = _cube(
            f"SYLVA_COL_ROUTE_{i:02d}",
            source.location,
            (source.dimensions.x * 0.5, 4.0, 1.2),
            preview,
            collision,
            source.rotation_quaternion.copy(),
        )
        proxy["collision_policy"] = "BOX_CORRIDOR_PROXY"
        proxy["owner_claim"] = CLAIM
        proxy["source_guide"] = source.name
        proxy["clear_width_m"] = 6.0

    root = bpy.data.objects.get("SYLVA_WORLD_ROOT")
    if root:
        root["build_status"] = "WAVE1B_STREAM_COLLISION_INTERFACES_R4"
        root["streaming_cell_size_m_proposal"] = CELL_M
        root["streaming_cell_count"] = 16
        root["rootkit_socket_count"] = len(socket_specs)
        root["collision_proxy_count"] = len(collision.objects)
        root["consumes_rootkit_claim"] = ROOT_CLAIM

    bpy.ops.object.select_all(action="DESELECT")
    return {
        "streaming_cells": 16,
        "region_envelopes": 3,
        "rootkit_sockets": len(socket_specs),
        "collision_objects": len(collision.objects),
        "rootkit_meshes_copied": 0,
    }


if __name__ == "__main__":
    print(build_interfaces())
