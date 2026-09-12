"""EXOVANT 2950 — KHEPRI world-macro generator.

Scope: CLM-KHEPRI-WMACRO-001
Agent: AGENT-KHEPRI-WMACRO-001
Blender: 5.2.x (3D Jutsu verified worker)
Units: 1 Blender Unit = 1 metre

This script generates ONLY the KHEPRI planetary/world-macro foundation:
- L0 metadata carrier (canon gravity + explicitly proposed radius/mass/density)
- L1 reduced-scale orbital proxy with physical-scale metadata
- L2 representative 6.4 km x 4.8 km local-tangent terrain cell
- mission-derived route anchors as non-authoritative proxies
- heliostat-field footprints (shared mesh data, not final architecture)
- human scale guide, lights and validation cameras

It intentionally does not author final architecture, characters, fauna, vehicles or RA-KHET.
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

# Canon from design/EXOVANT_DATA.json / BIBLIA.
GRAVITY_G_CANON = 0.63
TEMPERATURE_C_REFERENCE = 71.0

# KHP-ADR-001: production proposal, NOT canon.
PLANET_RADIUS_M_PROPOSAL = 5_224_000.0
PLANET_DIAMETER_M_PROPOSAL = 10_448_000.0
PLANET_MASS_EARTH_PROPOSAL = 0.4235
PLANET_DENSITY_G_CM3_PROPOSAL = 4.23

# Local macro validation cell proposal, not final authored acreage.
CELL_SIZE_X_M = 6_400.0
CELL_SIZE_Y_M = 4_800.0
GRID_X = 81
GRID_Y = 61


def clear_scene() -> None:
    for obj in list(bpy.data.objects):
        bpy.data.objects.remove(obj, do_unlink=True)
    for collection in list(bpy.data.collections):
        if collection.name != "Collection":
            bpy.data.collections.remove(collection)
    base = bpy.data.collections.get("Collection")
    if base is None:
        base = bpy.data.collections.new("KHP_WM_MASTER")
        bpy.context.scene.collection.children.link(base)
    else:
        base.name = "KHP_WM_MASTER"


def get_master() -> bpy.types.Collection:
    return bpy.data.collections["KHP_WM_MASTER"]


def new_collection(name: str) -> bpy.types.Collection:
    col = bpy.data.collections.new(name)
    get_master().children.link(col)
    return col


def move_to_collection(obj: bpy.types.Object, col: bpy.types.Collection) -> None:
    for current in list(obj.users_collection):
        current.objects.unlink(obj)
    col.objects.link(obj)


def make_material(name: str, rgb, metallic=0.0, roughness=0.5, emission=None, emission_strength=0.0):
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


def tag(obj: bpy.types.Object, asset_id: str, role: str, epistemic: str, quality_tier: str = "D") -> None:
    obj["exovant_asset_id"] = asset_id
    obj["world_id"] = WORLD_ID
    obj["claim_id"] = CLAIM_ID
    obj["role"] = role
    obj["epistemic"] = epistemic
    obj["quality_tier"] = quality_tier
    obj["production_status"] = "BLOCKOUT"


def add_empty(name, location, col, asset_id, role, epistemic="PROPOSAL", **extra):
    obj = bpy.data.objects.new(name, None)
    col.objects.link(obj)
    obj.location = location
    tag(obj, asset_id, role, epistemic)
    for key, value in extra.items():
        obj[key] = value
    return obj


def add_box(name, location, dimensions, material, col, asset_id, role, epistemic="PROPOSAL"):
    bpy.ops.mesh.primitive_cube_add(location=location)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = dimensions
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    move_to_collection(obj, col)
    obj.data.materials.append(material)
    tag(obj, asset_id, role, epistemic)
    return obj


def add_cylinder(name, location, radius, depth, material, col, asset_id, role, vertices=16, epistemic="PROPOSAL"):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=location)
    obj = bpy.context.object
    obj.name = name
    move_to_collection(obj, col)
    obj.data.materials.append(material)
    tag(obj, asset_id, role, epistemic)
    return obj


def look_at(obj: bpy.types.Object, target) -> None:
    direction = Vector(target) - obj.location
    obj.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()


def terrain_height(x: float, y: float) -> float:
    """Deterministic macro-only terrain. No high-frequency surface noise."""
    broad = 74.0 * math.sin(x / 890.0) * math.cos(y / 730.0)
    secondary = 31.0 * math.sin((x + 0.37 * y) / 370.0)
    tertiary = 13.0 * math.cos((0.28 * x - y) / 210.0)
    # Broad glass-sea basin through the middle of the representative cell.
    basin = -58.0 * math.exp(-((y + 180.0) / 620.0) ** 2)
    # Raised crucible-side shelf; macro interface only.
    shelf = 44.0 * math.exp(-(((x - 1250.0) / 900.0) ** 2 + ((y + 650.0) / 780.0) ** 2))
    return broad + secondary + tertiary + basin + shelf


def build_terrain(col, material):
    verts = []
    faces = []
    for iy in range(GRID_Y):
        y = -CELL_SIZE_Y_M / 2.0 + CELL_SIZE_Y_M * iy / (GRID_Y - 1)
        for ix in range(GRID_X):
            x = -CELL_SIZE_X_M / 2.0 + CELL_SIZE_X_M * ix / (GRID_X - 1)
            verts.append((x, y, terrain_height(x, y)))
    for iy in range(GRID_Y - 1):
        for ix in range(GRID_X - 1):
            a = iy * GRID_X + ix
            b = a + 1
            c = a + GRID_X + 1
            d = a + GRID_X
            faces.append((a, b, c, d))
    mesh = bpy.data.meshes.new("KHP_WM_MESH_MACROCELL_A")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new("KHP_WM_L2_MACROCELL_A_TERRAIN", mesh)
    col.objects.link(obj)
    obj.data.materials.append(material)
    tag(obj, "KHP_WM_TERRAIN_A", "macro_terrain", "PROPOSAL", "D")
    obj["cell_size_x_m"] = CELL_SIZE_X_M
    obj["cell_size_y_m"] = CELL_SIZE_Y_M
    obj["grid_x"] = GRID_X
    obj["grid_y"] = GRID_Y
    return obj


def build_orbital_proxy(col, material):
    # Reduced representation only. Physical radius remains metadata and is never implied by mesh radius.
    display_scale = 1.0 / 20_000.0
    display_radius = PLANET_RADIUS_M_PROPOSAL * display_scale
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=4, radius=display_radius, location=(0.0, 0.0, -1100.0))
    obj = bpy.context.object
    obj.name = "KHP_WM_L1_ORBITAL_PROXY_1_TO_20000"
    move_to_collection(obj, col)
    obj.data.materials.append(material)
    tag(obj, "KHP_WM_ORBITAL_PROXY", "orbital_representation", "PROPOSAL", "D")
    obj["display_scale"] = display_scale
    obj["physical_radius_m_proposal"] = PLANET_RADIUS_M_PROPOSAL
    obj["physical_diameter_m_proposal"] = PLANET_DIAMETER_M_PROPOSAL
    obj["non_collision"] = True
    return obj


def build_heliostat_footprints(col, bronze, mirror):
    # Shared mesh data. These are world-macro footprints, not final architecture.
    bpy.ops.mesh.primitive_cube_add(location=(0.0, 0.0, -9999.0))
    temp = bpy.context.object
    temp.dimensions = (36.0, 2.0, 22.0)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    mirror_mesh = temp.data.copy()
    bpy.data.objects.remove(temp, do_unlink=True)
    mirror_mesh.name = "KHP_WM_SHARED_HELIOSTAT_MIRROR"

    positions = []
    for row in range(4):
        for col_idx in range(8):
            x = -1800.0 + col_idx * 490.0 + (row % 2) * 120.0
            y = -1550.0 + row * 510.0
            positions.append((x, y))

    for idx, (x, y) in enumerate(positions):
        mast = add_cylinder(
            f"KHP_WM_HELIOSTAT_MAST_{idx:02d}",
            (x, y, terrain_height(x, y) + 18.0),
            2.4,
            36.0,
            bronze,
            col,
            f"KHP_WM_HEL_MAST_{idx:02d}",
            "heliostat_footprint",
            vertices=10,
        )
        mast["proxy_only"] = True
        panel = bpy.data.objects.new(f"KHP_WM_HELIOSTAT_PANEL_{idx:02d}", mirror_mesh)
        col.objects.link(panel)
        panel.location = (x, y, terrain_height(x, y) + 42.0)
        panel.rotation_euler = (math.radians(12.0 + row * 2.0), 0.0, math.radians(-18.0 + col_idx * 4.0))
        panel.data.materials.clear()
        panel.data.materials.append(mirror)
        tag(panel, f"KHP_WM_HEL_PANEL_{idx:02d}", "heliostat_footprint", "PROPOSAL", "D")
        panel["proxy_only"] = True


def build_route_anchors(col):
    anchors = {
        "KHP_WM_ROUTE_SHADE": (-2300.0, 900.0),
        "KHP_WM_ROUTE_GLASS_SEA": (-450.0, -140.0),
        "KHP_WM_ROUTE_CRUCIBLE": (1250.0, -650.0),
        "KHP_WM_ROUTE_RAKHET": (2550.0, 650.0),
    }
    result = []
    for name, (x, y) in anchors.items():
        z = terrain_height(x, y)
        obj = add_empty(
            name,
            (x, y, z),
            col,
            name,
            "route_interface_anchor",
            "DOCUMENT_DERIVED_PROXY",
            proxy_only=True,
        )
        result.append(obj)
    return result


def build_route_ribbon(col, material, anchors):
    # A coarse route guide with no gameplay authority.
    curve = bpy.data.curves.new("KHP_WM_ROUTE_GUIDE_CURVE", type="CURVE")
    curve.dimensions = "3D"
    curve.bevel_depth = 3.0
    curve.bevel_resolution = 0
    spline = curve.splines.new("POLY")
    spline.points.add(len(anchors) - 1)
    for idx, anchor in enumerate(anchors):
        x, y, z = anchor.location
        spline.points[idx].co = (x, y, z + 7.0, 1.0)
    obj = bpy.data.objects.new("KHP_WM_ROUTE_GUIDE_ONLY", curve)
    col.objects.link(obj)
    obj.data.materials.append(material)
    tag(obj, "KHP_WM_ROUTE_GUIDE", "qa_route_guide", "PROPOSAL", "D")
    obj["non_gameplay"] = True
    return obj


def build_scale_guide(col, material):
    # 1.85 m guide; not a character asset.
    bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.22, depth=1.45, location=(-2280.0, 900.0, terrain_height(-2280.0, 900.0) + 0.725))
    body = bpy.context.object
    body.name = "KHP_WM_GUIDE_HUMAN_1P85M_BODY"
    move_to_collection(body, col)
    body.data.materials.append(material)
    tag(body, "KHP_WM_GUIDE_HUMAN_BODY", "scale_guide", "PROPOSAL", "D")
    bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=6, radius=0.20, location=(-2280.0, 900.0, terrain_height(-2280.0, 900.0) + 1.65))
    head = bpy.context.object
    head.name = "KHP_WM_GUIDE_HUMAN_1P85M_HEAD"
    move_to_collection(head, col)
    head.data.materials.append(material)
    tag(head, "KHP_WM_GUIDE_HUMAN_HEAD", "scale_guide", "PROPOSAL", "D")


def build_cameras_and_lighting(cam_col, light_col):
    scene = bpy.context.scene
    bpy.ops.object.light_add(type="SUN", location=(0.0, 0.0, 1500.0))
    sun = bpy.context.object
    sun.name = "KHP_WM_LIGHT_SAHRA_KEY"
    sun.data.energy = 3.2
    sun.rotation_euler = (math.radians(38.0), math.radians(-22.0), math.radians(-28.0))
    move_to_collection(sun, light_col)
    sun["motivated_by"] = "Sahra primary star / directional macro validation"

    bpy.ops.object.camera_add(location=(-4100.0, -3600.0, 1850.0))
    overview = bpy.context.object
    overview.name = "KHP_WM_CAM_OVERVIEW"
    overview.data.lens = 46.0
    move_to_collection(overview, cam_col)
    look_at(overview, (0.0, -100.0, 50.0))
    scene.camera = overview

    x, y = -2380.0, 880.0
    z = terrain_height(x, y) + 1.65
    bpy.ops.object.camera_add(location=(x, y, z))
    gameplay = bpy.context.object
    gameplay.name = "KHP_WM_CAM_GAMEPLAY_SCALE"
    gameplay.data.lens = 38.0
    move_to_collection(gameplay, cam_col)
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
    scene.world.color = (0.012, 0.008, 0.005)

    collections = {
        "meta": new_collection("KHP_WM_00_META"),
        "orbital": new_collection("KHP_WM_10_L1_ORBITAL"),
        "terrain": new_collection("KHP_WM_20_L2_TERRAIN"),
        "optics": new_collection("KHP_WM_30_OPTICAL_FOOTPRINTS"),
        "anchors": new_collection("KHP_WM_40_ROUTE_INTERFACES"),
        "guides": new_collection("KHP_WM_80_QA_GUIDES"),
        "lights": new_collection("KHP_WM_90_LIGHTS"),
        "cameras": new_collection("KHP_WM_91_CAMERAS"),
    }

    mats = {
        "glass": make_material("KHP_WM_MAT_SOLAR_GLASS_BLOCKOUT", (0.16, 0.085, 0.035), 0.10, 0.30),
        "bronze": make_material("KHP_WM_MAT_BRONZE_BLOCKOUT", (0.22, 0.075, 0.022), 0.76, 0.34),
        "mirror": make_material("KHP_WM_MAT_MIRROR_BLOCKOUT", (0.36, 0.31, 0.23), 0.86, 0.10),
        "guide": make_material("KHP_WM_MAT_QA_GUIDE", (0.04, 0.20, 0.22), 0.05, 0.45, (0.02, 0.45, 0.50), 1.0),
        "orbital": make_material("KHP_WM_MAT_ORBITAL_PROXY", (0.08, 0.035, 0.015), 0.20, 0.60),
    }

    meta = add_empty(
        "KHP_WM_PLANET_META",
        (0.0, 0.0, 0.0),
        collections["meta"],
        "KHP_WM_PLANET_META",
        "planet_metadata",
        "MIXED_CANON_PROPOSAL",
    )
    meta["gravity_g_canon"] = GRAVITY_G_CANON
    meta["temperature_c_reference_documented"] = TEMPERATURE_C_REFERENCE
    meta["radius_m_proposal"] = PLANET_RADIUS_M_PROPOSAL
    meta["diameter_m_proposal"] = PLANET_DIAMETER_M_PROPOSAL
    meta["mass_earth_proposal"] = PLANET_MASS_EARTH_PROPOSAL
    meta["density_g_cm3_proposal"] = PLANET_DENSITY_G_CM3_PROPOSAL
    meta["planet_scale_adr"] = "production/worlds/khepri/world_macro/decisions/KHP-ADR-001-planet-scale.md"
    meta["coordinate_contract"] = "local_tangent_cell_xyz_metres_blender_z_up"

    orbital = build_orbital_proxy(collections["orbital"], mats["orbital"])
    terrain = build_terrain(collections["terrain"], mats["glass"])
    build_heliostat_footprints(collections["optics"], mats["bronze"], mats["mirror"])
    anchors = build_route_anchors(collections["anchors"])
    build_route_ribbon(collections["guides"], mats["guide"], anchors)
    build_scale_guide(collections["guides"], mats["guide"])
    build_cameras_and_lighting(collections["cameras"], collections["lights"])

    scene["project"] = "EXOVANT 2950"
    scene["world_id"] = WORLD_ID
    scene["claim_id"] = CLAIM_ID
    scene["agent_id"] = AGENT_ID
    scene["base_main_sha"] = BASE_SHA
    scene["generator_seed"] = SEED
    scene["units_contract"] = "1 BU = 1 metre"
    scene["authoring_coordinate_system"] = "Blender Z-up local tangent cell"
    scene["export_contract"] = "GLB portable export; Y-up conversion handled by glTF exporter"
    scene["canon_status"] = "KHEPRI world entry PROPOSED in design; local radius remains PROPOSAL"

    output_blend = os.environ.get("KHP_OUTPUT_BLEND")
    if output_blend:
        Path(output_blend).parent.mkdir(parents=True, exist_ok=True)
        bpy.ops.wm.save_as_mainfile(filepath=output_blend)

    output_glb = os.environ.get("KHP_OUTPUT_GLB")
    if output_glb:
        Path(output_glb).parent.mkdir(parents=True, exist_ok=True)
        bpy.ops.export_scene.gltf(filepath=output_glb, export_format="GLB", export_extras=True)

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
