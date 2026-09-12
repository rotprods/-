"""EXOVANT 2950 — KHEPRI world-macro generator.

Claim: CLM-KHEPRI-WMACRO-001
Agent: AGENT-KHEPRI-WMACRO-001
Verified worker target: Blender 5.2.x / Higgsfield 3D Jutsu
Units: 1 Blender Unit = 1 metre

Scope is deliberately atomic: L0 metadata, L1 orbital proxy, L2 representative
macro terrain cell, optical-infrastructure footprints, mission-derived route
anchors and QA guides. Final architecture, characters, fauna, vehicles and
RA-KHET are excluded.
"""
from __future__ import annotations

import json
import math
import os
from pathlib import Path

import bpy
from mathutils import Vector

WORLD_ID = "khepri"
CLAIM_ID = "CLM-KHEPRI-WMACRO-001"
AGENT_ID = "AGENT-KHEPRI-WMACRO-001"
BASE_SHA = "4c2fa044080004609ea6df45f34b2a784536507a"
SEED = 295006

# DOCUMENTED / CANON INPUTS
GRAVITY_G_CANON = 0.63
TEMPERATURE_C_REFERENCE = 71.0

# KHP-ADR-001 — PROPOSAL, NOT CANON
PLANET_RADIUS_M_PROPOSAL = 5_224_000.0
PLANET_DIAMETER_M_PROPOSAL = 10_448_000.0
PLANET_MASS_EARTH_PROPOSAL = 0.4235
PLANET_DENSITY_G_CM3_PROPOSAL = 4.23

# Representative pipeline-validation cell — PROPOSAL, NOT final playable acreage.
CELL_SIZE_X_M = 6_400.0
CELL_SIZE_Y_M = 4_800.0
GRID_X = 81
GRID_Y = 61


def clear_scene() -> None:
    for obj in list(bpy.data.objects):
        bpy.data.objects.remove(obj, do_unlink=True)
    for collection in list(bpy.data.collections):
        bpy.data.collections.remove(collection)
    master = bpy.data.collections.new("KHP_WM_MASTER")
    bpy.context.scene.collection.children.link(master)


def master() -> bpy.types.Collection:
    return bpy.data.collections["KHP_WM_MASTER"]


def collection(name: str) -> bpy.types.Collection:
    col = bpy.data.collections.new(name)
    master().children.link(col)
    return col


def move(obj: bpy.types.Object, col: bpy.types.Collection) -> None:
    for old in list(obj.users_collection):
        old.objects.unlink(obj)
    col.objects.link(obj)


def material(name, rgb, metallic=0.0, roughness=0.5, emission=None, emission_strength=0.0):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*rgb, 1.0)
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = roughness
    if emission is not None:
        bsdf.inputs["Emission Color"].default_value = (*emission, 1.0)
        bsdf.inputs["Emission Strength"].default_value = emission_strength
    return mat


def tag(obj, asset_id, role, epistemic="PROPOSAL", tier="D") -> None:
    obj["exovant_asset_id"] = asset_id
    obj["world_id"] = WORLD_ID
    obj["claim_id"] = CLAIM_ID
    obj["role"] = role
    obj["epistemic"] = epistemic
    obj["quality_tier"] = tier
    obj["production_status"] = "BLOCKOUT"


def empty(name, location, col, asset_id, role, epistemic="PROPOSAL", **extras):
    obj = bpy.data.objects.new(name, None)
    col.objects.link(obj)
    obj.location = location
    tag(obj, asset_id, role, epistemic)
    for key, value in extras.items():
        obj[key] = value
    return obj


def cylinder(name, location, radius, depth, mat, col, asset_id, role, vertices=12):
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=vertices, radius=radius, depth=depth, location=location
    )
    obj = bpy.context.object
    obj.name = name
    move(obj, col)
    obj.data.materials.append(mat)
    tag(obj, asset_id, role)
    return obj


def look_at(obj, target) -> None:
    obj.rotation_euler = (Vector(target) - obj.location).to_track_quat("-Z", "Y").to_euler()


def terrain_height(x: float, y: float) -> float:
    """Deterministic macro-only elevation; intentionally no micro/noise dressing."""
    broad = 74.0 * math.sin(x / 890.0) * math.cos(y / 730.0)
    secondary = 31.0 * math.sin((x + 0.37 * y) / 370.0)
    tertiary = 13.0 * math.cos((0.28 * x - y) / 210.0)
    glass_sea_basin = -58.0 * math.exp(-((y + 180.0) / 620.0) ** 2)
    crucible_shelf = 44.0 * math.exp(
        -(((x - 1250.0) / 900.0) ** 2 + ((y + 650.0) / 780.0) ** 2)
    )
    return broad + secondary + tertiary + glass_sea_basin + crucible_shelf


def build_terrain(col, mat):
    vertices = []
    faces = []
    for iy in range(GRID_Y):
        y = -CELL_SIZE_Y_M / 2.0 + CELL_SIZE_Y_M * iy / (GRID_Y - 1)
        for ix in range(GRID_X):
            x = -CELL_SIZE_X_M / 2.0 + CELL_SIZE_X_M * ix / (GRID_X - 1)
            vertices.append((x, y, terrain_height(x, y)))
    for iy in range(GRID_Y - 1):
        for ix in range(GRID_X - 1):
            a = iy * GRID_X + ix
            faces.append((a, a + 1, a + GRID_X + 1, a + GRID_X))
    mesh = bpy.data.meshes.new("KHP_WM_MESH_MACROCELL_A")
    mesh.from_pydata(vertices, [], faces)
    mesh.update()
    obj = bpy.data.objects.new("KHP_WM_L2_MACROCELL_A_TERRAIN", mesh)
    col.objects.link(obj)
    obj.data.materials.append(mat)
    tag(obj, "KHP_WM_TERRAIN_A", "macro_terrain")
    obj["cell_size_x_m"] = CELL_SIZE_X_M
    obj["cell_size_y_m"] = CELL_SIZE_Y_M
    obj["grid_x"] = GRID_X
    obj["grid_y"] = GRID_Y
    return obj


def build_orbital_proxy(col, mat):
    # Reduced display object; physical scale is metadata. Never gameplay/collision geometry.
    display_scale = 1.0 / 20_000.0
    display_radius = PLANET_RADIUS_M_PROPOSAL * display_scale
    bpy.ops.mesh.primitive_ico_sphere_add(
        subdivisions=4, radius=display_radius, location=(0.0, 0.0, -1100.0)
    )
    obj = bpy.context.object
    obj.name = "KHP_WM_L1_ORBITAL_PROXY_1_TO_20000"
    move(obj, col)
    obj.data.materials.append(mat)
    tag(obj, "KHP_WM_ORBITAL_PROXY", "orbital_representation")
    obj["display_scale"] = display_scale
    obj["physical_radius_m_proposal"] = PLANET_RADIUS_M_PROPOSAL
    obj["physical_diameter_m_proposal"] = PLANET_DIAMETER_M_PROPOSAL
    obj["non_collision"] = True
    return obj


def build_heliostat_footprints(col, bronze, mirror):
    # One shared panel mesh; footprint proxies only, not architecture ownership.
    bpy.ops.mesh.primitive_cube_add(location=(0.0, 0.0, -9999.0))
    tmp = bpy.context.object
    tmp.dimensions = (36.0, 2.0, 22.0)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    shared = tmp.data.copy()
    shared.name = "KHP_WM_SHARED_HELIOSTAT_PANEL"
    shared.materials.append(mirror)
    bpy.data.objects.remove(tmp, do_unlink=True)

    for row in range(4):
        for column in range(8):
            idx = row * 8 + column
            x = -1800.0 + column * 490.0 + (row % 2) * 120.0
            y = -1550.0 + row * 510.0
            z = terrain_height(x, y)
            mast = cylinder(
                f"KHP_WM_HELIOSTAT_MAST_{idx:02d}",
                (x, y, z + 18.0),
                2.4,
                36.0,
                bronze,
                col,
                f"KHP_WM_HEL_MAST_{idx:02d}",
                "heliostat_footprint",
                vertices=10,
            )
            mast["proxy_only"] = True
            panel = bpy.data.objects.new(f"KHP_WM_HELIOSTAT_PANEL_{idx:02d}", shared)
            col.objects.link(panel)
            panel.location = (x, y, z + 42.0)
            panel.rotation_euler = (
                math.radians(12.0 + row * 2.0),
                0.0,
                math.radians(-18.0 + column * 4.0),
            )
            tag(panel, f"KHP_WM_HEL_PANEL_{idx:02d}", "heliostat_footprint")
            panel["proxy_only"] = True


def build_route_anchors(col):
    documented_function_proxies = {
        "KHP_WM_ROUTE_SHADE": (-2300.0, 900.0),
        "KHP_WM_ROUTE_GLASS_SEA": (-450.0, -140.0),
        "KHP_WM_ROUTE_CRUCIBLE": (1250.0, -650.0),
        "KHP_WM_ROUTE_RAKHET": (2550.0, 650.0),
    }
    anchors = []
    for name, (x, y) in documented_function_proxies.items():
        anchors.append(
            empty(
                name,
                (x, y, terrain_height(x, y)),
                col,
                name,
                "route_interface_anchor",
                "DOCUMENT_DERIVED_PROXY",
                proxy_only=True,
            )
        )
    return anchors


def build_route_guide(col, mat, anchors):
    curve = bpy.data.curves.new("KHP_WM_ROUTE_GUIDE_CURVE", "CURVE")
    curve.dimensions = "3D"
    curve.bevel_depth = 3.0
    curve.bevel_resolution = 0
    spline = curve.splines.new("POLY")
    spline.points.add(len(anchors) - 1)
    for index, anchor in enumerate(anchors):
        x, y, z = anchor.location
        spline.points[index].co = (x, y, z + 7.0, 1.0)
    obj = bpy.data.objects.new("KHP_WM_ROUTE_GUIDE_ONLY", curve)
    col.objects.link(obj)
    curve.materials.append(mat)
    tag(obj, "KHP_WM_ROUTE_GUIDE", "qa_route_guide")
    obj["non_gameplay"] = True


def build_human_scale_guide(col, mat):
    # Exactly 1.85 m overall; QA guide, not a character asset.
    x, y = -2280.0, 900.0
    z = terrain_height(x, y)
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=12, radius=0.22, depth=1.45, location=(x, y, z + 0.725)
    )
    body = bpy.context.object
    body.name = "KHP_WM_GUIDE_HUMAN_1P85M_BODY"
    move(body, col)
    body.data.materials.append(mat)
    tag(body, "KHP_WM_GUIDE_HUMAN_BODY", "scale_guide")
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=12, ring_count=6, radius=0.20, location=(x, y, z + 1.65)
    )
    head = bpy.context.object
    head.name = "KHP_WM_GUIDE_HUMAN_1P85M_HEAD"
    move(head, col)
    head.data.materials.append(mat)
    tag(head, "KHP_WM_GUIDE_HUMAN_HEAD", "scale_guide")


def build_cameras_and_lighting(camera_col, light_col):
    scene = bpy.context.scene
    bpy.ops.object.light_add(type="SUN", location=(0.0, 0.0, 1500.0))
    sun = bpy.context.object
    sun.name = "KHP_WM_LIGHT_SAHRA_KEY"
    sun.data.energy = 3.2
    sun.rotation_euler = (
        math.radians(38.0), math.radians(-22.0), math.radians(-28.0)
    )
    sun["motivated_by"] = "Sahra primary star / macro validation"
    move(sun, light_col)

    bpy.ops.object.camera_add(location=(-4100.0, -3600.0, 1850.0))
    overview = bpy.context.object
    overview.name = "KHP_WM_CAM_OVERVIEW"
    overview.data.lens = 46.0
    move(overview, camera_col)
    look_at(overview, (0.0, -100.0, 50.0))
    scene.camera = overview

    x, y = -2380.0, 880.0
    bpy.ops.object.camera_add(location=(x, y, terrain_height(x, y) + 1.65))
    gameplay = bpy.context.object
    gameplay.name = "KHP_WM_CAM_GAMEPLAY_SCALE"
    gameplay.data.lens = 38.0
    move(gameplay, camera_col)
    look_at(gameplay, (-1200.0, 300.0, terrain_height(-1200.0, 300.0) + 25.0))


def build() -> dict:
    clear_scene()
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 1.0
    scene.render.engine = "BLENDER_EEVEE"
    scene.render.resolution_x = 1280
    scene.render.resolution_y = 720
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"

    # Empty 3D Jutsu projects may have no World datablock.
    if scene.world is None:
        scene.world = bpy.data.worlds.new("KHP_WM_WORLD")
    scene.world.color = (0.012, 0.008, 0.005)

    cols = {
        "meta": collection("KHP_WM_00_META"),
        "orbital": collection("KHP_WM_10_L1_ORBITAL"),
        "terrain": collection("KHP_WM_20_L2_TERRAIN"),
        "optics": collection("KHP_WM_30_OPTICAL_FOOTPRINTS"),
        "anchors": collection("KHP_WM_40_ROUTE_INTERFACES"),
        "guides": collection("KHP_WM_80_QA_GUIDES"),
        "lights": collection("KHP_WM_90_LIGHTS"),
        "cameras": collection("KHP_WM_91_CAMERAS"),
    }
    mats = {
        "glass": material("KHP_WM_MAT_SOLAR_GLASS_BLOCKOUT", (0.16, 0.085, 0.035), 0.10, 0.30),
        "bronze": material("KHP_WM_MAT_BRONZE_BLOCKOUT", (0.22, 0.075, 0.022), 0.76, 0.34),
        "mirror": material("KHP_WM_MAT_MIRROR_BLOCKOUT", (0.36, 0.31, 0.23), 0.86, 0.10),
        "guide": material("KHP_WM_MAT_QA_GUIDE", (0.04, 0.20, 0.22), 0.05, 0.45, (0.02, 0.45, 0.50), 1.0),
        "orbital": material("KHP_WM_MAT_ORBITAL_PROXY", (0.08, 0.035, 0.015), 0.20, 0.60),
    }

    meta = empty(
        "KHP_WM_PLANET_META", (0.0, 0.0, 0.0), cols["meta"],
        "KHP_WM_PLANET_META", "planet_metadata", "MIXED_CANON_PROPOSAL"
    )
    meta["gravity_g_canon"] = GRAVITY_G_CANON
    meta["temperature_c_reference_documented"] = TEMPERATURE_C_REFERENCE
    meta["radius_m_proposal"] = PLANET_RADIUS_M_PROPOSAL
    meta["diameter_m_proposal"] = PLANET_DIAMETER_M_PROPOSAL
    meta["mass_earth_proposal"] = PLANET_MASS_EARTH_PROPOSAL
    meta["density_g_cm3_proposal"] = PLANET_DENSITY_G_CM3_PROPOSAL
    meta["planet_scale_adr"] = "KHP-ADR-001"
    meta["coordinate_contract"] = "local_tangent_cell_xyz_metres_blender_z_up"

    orbital = build_orbital_proxy(cols["orbital"], mats["orbital"])
    terrain = build_terrain(cols["terrain"], mats["glass"])
    build_heliostat_footprints(cols["optics"], mats["bronze"], mats["mirror"])
    anchors = build_route_anchors(cols["anchors"])
    build_route_guide(cols["guides"], mats["guide"], anchors)
    build_human_scale_guide(cols["guides"], mats["guide"])
    build_cameras_and_lighting(cols["cameras"], cols["lights"])

    scene["project"] = "EXOVANT 2950"
    scene["world_id"] = WORLD_ID
    scene["claim_id"] = CLAIM_ID
    scene["agent_id"] = AGENT_ID
    scene["base_main_sha"] = BASE_SHA
    scene["generator_seed"] = SEED
    scene["units_contract"] = "1 BU = 1 metre"
    scene["authoring_coordinate_system"] = "Blender Z-up local tangent cell"
    scene["export_contract"] = "GLB portable export; glTF handles Y-up conversion"
    scene["canon_status"] = "world entry PROPOSED; KHP radius remains PROPOSAL"

    blend_path = os.environ.get("KHP_OUTPUT_BLEND")
    if blend_path:
        Path(blend_path).parent.mkdir(parents=True, exist_ok=True)
        bpy.ops.wm.save_as_mainfile(filepath=blend_path)
    glb_path = os.environ.get("KHP_OUTPUT_GLB")
    if glb_path:
        Path(glb_path).parent.mkdir(parents=True, exist_ok=True)
        bpy.ops.export_scene.gltf(filepath=glb_path, export_format="GLB", export_extras=True)

    return {
        "world_id": WORLD_ID,
        "claim_id": CLAIM_ID,
        "object_count": len(bpy.data.objects),
        "mesh_count": len(bpy.data.meshes),
        "material_count": len(bpy.data.materials),
        "cell_size_m": [CELL_SIZE_X_M, CELL_SIZE_Y_M],
        "planet_radius_m_proposal": PLANET_RADIUS_M_PROPOSAL,
        "gravity_g_canon": GRAVITY_G_CANON,
        "terrain_object": terrain.name,
        "orbital_proxy": orbital.name,
        "route_anchors": [obj.name for obj in anchors],
    }


RESULT = build()
print(json.dumps(RESULT, indent=2, sort_keys=True))
