"""EXOVANT 2950 / PELAGOS World Foundation generator.

World-local source for PELAGOS-WF-001. Designed for Blender 5.2+ `bpy`.
1 Blender Unit = 1 metre for this scope.

This script intentionally builds a production blockout, not final art. It keeps
planet-scale metadata separated from the 2.2 km authored master cell.

Usage example:
  blender --background --python build_world_foundation.py -- \
    --blend /tmp/pelagos_foundation.blend --glb /tmp/pelagos_foundation.glb
"""

import argparse
import math
import random
import sys
from pathlib import Path

import bpy
from mathutils import Vector

PROJECT_ID = "39930c08-62bb-4034-b35d-70d0ce51c9d9"
CHECKPOINT = "PELAGOS-WF-001"
SEED = 2950


def args_after_double_dash():
    if "--" not in sys.argv:
        return []
    return sys.argv[sys.argv.index("--") + 1 :]


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--blend")
    p.add_argument("--glb")
    return p.parse_args(args_after_double_dash())


def collection(name, parent=None):
    scene = bpy.context.scene
    c = bpy.data.collections.get(name) or bpy.data.collections.new(name)
    target = scene.collection if parent is None else parent
    if c.name not in target.children:
        target.children.link(c)
    return c


def relink(obj, c):
    for old in list(obj.users_collection):
        old.objects.unlink(obj)
    c.objects.link(obj)
    return obj


def tag(obj, asset_id, role, lod="L0_BLOCKOUT", collision="none"):
    obj["asset_id"] = asset_id
    obj["world"] = "pelagos"
    obj["role"] = role
    obj["lod_state"] = lod
    obj["collision_intent"] = collision
    return obj


def material(name, color, metallic=0.0, roughness=0.5, emission=None, strength=0.0):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = color
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = roughness
    if emission is not None:
        if "Emission Color" in bsdf.inputs:
            bsdf.inputs["Emission Color"].default_value = emission
            bsdf.inputs["Emission Strength"].default_value = strength
        elif "Emission" in bsdf.inputs:
            bsdf.inputs["Emission"].default_value = emission
    return m


def set_material(obj, m):
    if hasattr(obj.data, "materials") and not obj.data.materials:
        obj.data.materials.append(m)


def cube(name, loc, dims, mat, c, asset_id, role, bevel=0.0, collision="simple"):
    bpy.ops.mesh.primitive_cube_add(location=loc)
    o = bpy.context.object
    o.name = name
    o.dimensions = dims
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if bevel:
        mod = o.modifiers.new("BEVEL_NONDESTRUCTIVE", "BEVEL")
        mod.width = bevel
        mod.segments = 2
    set_material(o, mat)
    relink(o, c)
    return tag(o, asset_id, role, collision=collision)


def cylinder(name, loc, radius, depth, mat, c, asset_id, role, vertices=24, collision="simple"):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=loc)
    o = bpy.context.object
    o.name = name
    set_material(o, mat)
    relink(o, c)
    return tag(o, asset_id, role, collision=collision)


def sphere(name, loc, scale, mat, c, asset_id, role):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=12, location=loc)
    o = bpy.context.object
    o.name = name
    o.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    set_material(o, mat)
    relink(o, c)
    return tag(o, asset_id, role)


def torus(name, loc, major, minor, mat, c, asset_id, role):
    bpy.ops.mesh.primitive_torus_add(
        major_radius=major,
        minor_radius=minor,
        major_segments=48,
        minor_segments=10,
        location=loc,
    )
    o = bpy.context.object
    o.name = name
    set_material(o, mat)
    relink(o, c)
    return tag(o, asset_id, role)


def curve(name, points, bevel, mat, c, asset_id, role):
    data = bpy.data.curves.new(name + "_CURVE", "CURVE")
    data.dimensions = "3D"
    data.resolution_u = 3
    data.bevel_depth = bevel
    data.bevel_resolution = 3
    spline = data.splines.new("BEZIER")
    spline.bezier_points.add(len(points) - 1)
    for point, xyz in zip(spline.bezier_points, points):
        point.co = xyz
        point.handle_left_type = "AUTO"
        point.handle_right_type = "AUTO"
    o = bpy.data.objects.new(name, data)
    c.objects.link(o)
    set_material(o, mat)
    return tag(o, asset_id, role)


def look_at(obj, target):
    obj.rotation_euler = (Vector(target) - obj.location).to_track_quat("-Z", "Y").to_euler()


def camera(name, loc, target, lens, c):
    data = bpy.data.cameras.new(name + "_DATA")
    data.lens = lens
    data.sensor_width = 36
    o = bpy.data.objects.new(name, data)
    c.objects.link(o)
    o.location = loc
    look_at(o, target)
    return o


def spot(name, loc, energy, color, target, c):
    data = bpy.data.lights.new(name + "_DATA", "SPOT")
    data.energy = energy
    data.color = color
    data.spot_size = math.radians(55)
    data.spot_blend = 0.55
    o = bpy.data.objects.new(name, data)
    c.objects.link(o)
    o.location = loc
    look_at(o, target)
    return o


def humanoid_proxy(prefix, loc, accent, mats, c, asset_id, role):
    dark, ivory = mats
    x, y, z = loc
    cylinder(prefix + "_Torso", (x, y, z + 1.05), 0.32, 1.1, dark, c, asset_id, role, 12)
    sphere(prefix + "_Head", (x, y, z + 1.82), (0.24, 0.24, 0.28), ivory, c, asset_id, role)
    cube(prefix + "_ChestMark", (x, y - 0.31, z + 1.15), (0.22, 0.07, 0.28), accent, c, asset_id, role, 0.03, "none")


def build():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for c in list(bpy.data.collections):
        if c.name != "Collection":
            bpy.data.collections.remove(c)

    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 1.0
    scene.render.engine = "BLENDER_EEVEE"
    if scene.world is None:
        scene.world = bpy.data.worlds.new("PELAGOS_WORLD_ENV")
    scene.world.use_nodes = True
    bg = scene.world.node_tree.nodes.get("Background")
    if bg:
        bg.inputs["Color"].default_value = (0.008, 0.018, 0.026, 1)
        bg.inputs["Strength"].default_value = 0.20

    root = collection("PELAGOS_WORLD")
    groups = {
        "terrain": collection("00_BATHYMETRY", root),
        "market": collection("10_MERCADO_BOYAS", root),
        "reef": collection("20_CORO_ARRECIFE", root),
        "trench": collection("30_FOSA_MIL_MIRADAS", root),
        "boss": collection("40_THALASSA_ARENA", root),
        "eco": collection("50_ECOLOGY", root),
        "npc": collection("60_NPCS", root),
        "enemy": collection("70_ENEMIES", root),
        "vehicle": collection("80_NACAR2", root),
        "guides": collection("90_NAV_SCALE_GUIDES", root),
        "lights": collection("91_LIGHTS", root),
        "cameras": collection("92_CAMERAS", root),
    }

    m = {
        "water": material("PEL_WaterProxy", (0.015, 0.105, 0.14, 1), roughness=0.18),
        "seabed": material("PEL_Seabed_BlackMineral", (0.028, 0.040, 0.043, 1), 0.05, 0.86),
        "ivory": material("PEL_Human_IvoryCeramic", (0.72, 0.73, 0.64, 1), 0.12, 0.34),
        "dark": material("PEL_TechnicalFabric", (0.018, 0.035, 0.045, 1), 0.0, 0.74),
        "bronze": material("PEL_Precursor_Bronze", (0.18, 0.27, 0.23, 1), 0.72, 0.40),
        "coral": material("PEL_LivingCoral", (0.22, 0.40, 0.36, 1), 0.0, 0.66),
        "coral_pale": material("PEL_LivingCoral_Pale", (0.43, 0.58, 0.48, 1), 0.0, 0.58),
        "cyan": material("PEL_Memory_Cyan", (0.03, 0.30, 0.40, 1), 0.05, 0.28, (0.05, 0.55, 0.78, 1), 3.0),
        "amber": material("PEL_Refuge_Amber", (0.32, 0.13, 0.02, 1), 0.1, 0.30, (0.96, 0.36, 0.04, 1), 2.5),
        "red": material("PEL_Hostile_Vermilion", (0.30, 0.018, 0.008, 1), 0.1, 0.32, (0.85, 0.035, 0.01, 1), 2.2),
        "glass": material("PEL_GlassProxy", (0.08, 0.20, 0.22, 1), 0.05, 0.15),
    }

    bpy.ops.object.empty_add(type="PLAIN_AXES", location=(0, 0, 0))
    meta = bpy.context.object
    meta.name = "PELAGOS_WORLD_METADATA"
    relink(meta, groups["guides"])
    meta["checkpoint"] = CHECKPOINT
    meta["planet_radius_km_status"] = "PROPOSAL"
    meta["planet_radius_km"] = 6000.0
    meta["planet_mass_earth_status"] = "DERIVED_PROPOSAL"
    meta["planet_mass_earth"] = 0.8071
    meta["surface_gravity_g_status"] = "CANON"
    meta["surface_gravity_g"] = 0.91
    meta["temperature_c_status"] = "CANON"
    meta["temperature_c"] = 8.0
    meta["playable_master_extent_m_status"] = "PROPOSAL"
    meta["playable_master_extent_m"] = 2200.0

    # Bathymetry.
    n = 49
    extent = 2200.0
    half = extent / 2
    vertices = []
    faces = []
    for j in range(n):
        y = -half + extent * j / (n - 1)
        for i in range(n):
            x = -half + extent * i / (n - 1)
            z = -58.0
            z += 82.0 * math.exp(-((x + 80) ** 2 + (y - 40) ** 2) / (2 * 260 ** 2))
            z += 36.0 * math.exp(-((x + 520) ** 2 + (y - 80) ** 2) / (2 * 220 ** 2))
            z -= 145.0 * math.exp(-((x - 520) ** 2 + (y - 230) ** 2) / (2 * 190 ** 2))
            z += 6.0 * math.sin(x * 0.012) * math.cos(y * 0.010)
            vertices.append((x, y, z))
    for j in range(n - 1):
        for i in range(n - 1):
            a = j * n + i
            faces.append((a, a + 1, a + n + 1, a + n))
    mesh = bpy.data.meshes.new("PEL_BathymetryMesh")
    mesh.from_pydata(vertices, [], faces)
    mesh.update()
    terrain = bpy.data.objects.new("PEL_ENV_Bathymetry_2200m", mesh)
    groups["terrain"].objects.link(terrain)
    set_material(terrain, m["seabed"])
    tag(terrain, "PEL-ENV-001", "bathymetry", collision="complex_candidate")
    cube("PEL_ENV_MeanSea_2200m", (0, 0, 0), (2200, 2200, 1.2), m["water"], groups["terrain"], "PEL-ENV-002", "water_proxy", collision="none")

    for v in (-1000, -500, 0, 500, 1000):
        curve(f"PEL_GUIDE_X_{v}", [(-1100, v, 2), (1100, v, 2)], 0.55, m["cyan"], groups["guides"], "PEL-GUIDE", "streaming_grid")
        curve(f"PEL_GUIDE_Y_{v}", [(v, -1100, 2), (v, 1100, 2)], 0.55, m["cyan"], groups["guides"], "PEL-GUIDE", "streaming_grid")

    # Mercado.
    platform_positions = [(-520, -80), (-420, -20), (-610, 10), (-520, 70), (-700, -120), (-360, -150), (-600, -210)]
    for idx, (x, y) in enumerate(platform_positions):
        cylinder(f"PEL_MKT_Platform_{idx:02d}", (x, y, 10 + idx % 2 * 2), 42 if idx < 4 else 30, 7, m["ivory"], groups["market"], f"PEL-MKT-PLAT-{idx:02d}", "floating_platform", 12)
        cylinder(f"PEL_MKT_BuoyKeel_{idx:02d}", (x, y, -5), 14, 30, m["dark"], groups["market"], f"PEL-MKT-BUOY-{idx:02d}", "buoy_keel", 16)
        cylinder(f"PEL_MKT_Mast_{idx:02d}", (x, y, 35), 1.5, 45, m["bronze"], groups["market"], f"PEL-MKT-MAST-{idx:02d}", "mast", 12)
        for k in range(4):
            a = k * math.pi / 2
            curve(f"PEL_MKT_CanopyRib_{idx:02d}_{k}", [(x, y, 54), (x + math.cos(a) * 28, y + math.sin(a) * 28, 31)], 0.7, m["ivory"], groups["market"], "PEL-MKT-CANOPY", "canopy_rib")
        sphere(f"PEL_MKT_RefugeLight_{idx:02d}", (x, y, 56), (2, 2, 2), m["amber"], groups["market"], "PEL-MKT-LIGHT", "refuge_signal")
    for a, b in [(0, 1), (0, 2), (0, 3), (2, 4), (1, 5), (0, 6)]:
        x1, y1 = platform_positions[a]
        x2, y2 = platform_positions[b]
        curve(f"PEL_MKT_Bridge_{a}_{b}", [(x1, y1, 16), (x2, y2, 16)], 3.0, m["bronze"], groups["market"], "PEL-MKT-BRIDGE", "walkway")
    sphere("PEL_MKT_CommandShell", (-520, -80, 23), (22, 16, 9), m["ivory"], groups["market"], "PEL-MKT-HERO-001", "market_shell")

    # Coro.
    random.seed(SEED)
    for i in range(34):
        x = random.uniform(-260, 260)
        y = random.uniform(-260, 260)
        if (x + 520) ** 2 + (y + 80) ** 2 < 180 ** 2:
            continue
        h = random.uniform(18, 75)
        bend = random.uniform(-18, 18)
        points = [(x, y, 2), (x + bend * 0.4, y - bend * 0.2, h * 0.45), (x + bend, y + bend * 0.25, h)]
        curve(f"PEL_REEF_Spire_{i:02d}", points, random.uniform(1.8, 4.5), m["coral_pale"] if i % 4 == 0 else m["coral"], groups["reef"], f"PEL-REEF-SPIRE-{i:02d}", "coral_spire")
        if i % 3 == 0:
            sphere(f"PEL_REEF_MemoryNode_{i:02d}", points[-1], (2.4, 2.4, 2.4), m["cyan"], groups["reef"], f"PEL-REEF-NODE-{i:02d}", "memory_node")
    for i, r in enumerate((80, 145, 215)):
        points = []
        for step in range(13):
            a = math.radians(-65 + step * (130 / 12))
            points.append((math.cos(a) * r, math.sin(a) * r + 40, 18 + 34 * math.sin((step / 12) * math.pi)))
        curve(f"PEL_REEF_AcousticArch_{i}", points, 3.2, m["bronze"], groups["reef"], f"PEL-REEF-ARCH-{i}", "acoustic_arch")
    cylinder("PEL_REEF_ChorusMast", (0, 40, 50), 8, 100, m["bronze"], groups["reef"], "PEL-REEF-HERO-001", "chorus_landmark", 20)
    for z in (28, 50, 72, 94):
        torus(f"PEL_REEF_ResonanceRing_{z}", (0, 40, z), 18 + (z % 20), 1.8, m["cyan"], groups["reef"], "PEL-REEF-RING", "resonance_ring")

    # Fosa and THALASSA arena.
    trench = (520, 230)
    torus("PEL_TRENCH_Rim", (520, 230, 4), 112, 6, m["bronze"], groups["trench"], "PEL-TRN-HERO-001", "trench_rim")
    for i in range(12):
        a = 2 * math.pi * i / 12
        x = 520 + math.cos(a) * 105
        y = 230 + math.sin(a) * 105
        cylinder(f"PEL_TRENCH_Anchor_{i:02d}", (x, y, -40), 3.5, 90, m["bronze"], groups["trench"], f"PEL-TRN-ANCH-{i:02d}", "descent_anchor", 12)
        sphere(f"PEL_TRENCH_EyeGuide_{i:02d}", (x, y, 11), (2.6, 2.6, 2.6), m["cyan"], groups["trench"], "PEL-TRN-GUIDE", "descent_signal")
    curve("PEL_TRENCH_Approach", [(250, 120, 14), (380, 180, 12), (430, 210, 10)], 4.5, m["ivory"], groups["trench"], "PEL-TRN-WALK-001", "approach_walkway")

    arena_z = -92
    cylinder("PEL_BOSS_ArenaFloor", (520, 230, arena_z), 26, 3, m["dark"], groups["boss"], "PEL-BOSS-ARENA-001", "boss_arena_floor", 48, "complex_candidate")
    torus("PEL_BOSS_ArenaRing", (520, 230, arena_z + 2), 25, 1.4, m["bronze"], groups["boss"], "PEL-BOSS-ARENA-RING", "arena_ring")
    for i in range(8):
        a = 2 * math.pi * i / 8
        x = 520 + math.cos(a) * 21
        y = 230 + math.sin(a) * 21
        cylinder(f"PEL_BOSS_Column_{i:02d}", (x, y, arena_z + 11), 2.2, 22, m["ivory"], groups["boss"], f"PEL-BOSS-COL-{i:02d}", "line_of_sight_column", 12)
    for i, a in enumerate((0, math.pi / 2, math.pi, 3 * math.pi / 2)):
        x = 520 + math.cos(a) * 15
        y = 230 + math.sin(a) * 15
        cube(f"PEL_BOSS_DryPlatform_{i}", (x, y, arena_z + 2), (9, 7, 1.2), m["ivory"], groups["boss"], f"PEL-BOSS-DRY-{i}", "dry_platform", 0.6)
    sphere("PEL_BOSS_Thalassa_Core", (520, 230, arena_z + 12), (9, 9, 15), m["coral_pale"], groups["boss"], "PEL-BOSS-THALASSA-CORE", "boss_core")
    for i in range(18):
        a = 2 * math.pi * i / 18
        z = arena_z + 8 + (i % 5) * 3.1
        r = 9.2 + ((i % 3) - 1)
        sphere(f"PEL_BOSS_Eye_{i:02d}", (520 + math.cos(a) * r, 230 + math.sin(a) * r, z), (1.5, 1.2, 1.5), m["cyan"], groups["boss"], f"PEL-BOSS-EYE-{i:02d}", "boss_eye")
    for i in range(8):
        a = 2 * math.pi * i / 8
        curve(f"PEL_BOSS_Tentacle_{i:02d}", [(520 + math.cos(a) * 6, 230 + math.sin(a) * 6, arena_z + 6), (520 + math.cos(a) * 18, 230 + math.sin(a) * 18, arena_z + 8 + (i % 2) * 4), (520 + math.cos(a) * 32, 230 + math.sin(a) * 32, arena_z + 3)], 2.8, m["coral"], groups["boss"], f"PEL-BOSS-TENT-{i:02d}", "boss_tentacle")

    # Ecology proxies.
    for i, (x, y, z) in enumerate([(-80, 180, 38), (40, 220, 50), (130, 150, 32)]):
        sphere(f"PEL_ECO_MnemonicJelly_Bell_{i}", (x, y, z), (7, 7, 3), m["cyan"], groups["eco"], f"PEL-ECO-JELLY-{i}", "mnemonic_jellyfish")
        for t in range(5):
            dx = (t - 2) * 1.5
            curve(f"PEL_ECO_MnemonicJelly_Tent_{i}_{t}", [(x + dx, y, z - 2), (x + dx * 1.4, y + 2, z - 10), (x + dx * 0.6, y - 1, z - 20)], 0.35, m["cyan"], groups["eco"], f"PEL-ECO-JELLY-{i}", "jelly_tentacle")
    curve("PEL_ECO_GlassEel", [(-220, 80, 14), (-170, 100, 18), (-120, 70, 16), (-60, 105, 20)], 2.4, m["glass"], groups["eco"], "PEL-ECO-EEL-001", "glass_eel")
    sphere("PEL_ECO_ReefBovine_Body", (150, -120, 12), (9, 4.5, 5.5), m["coral_pale"], groups["eco"], "PEL-ECO-BOV-001", "reef_bovine")
    for i, (dx, dy) in enumerate([(-5, -2.5), (-5, 2.5), (5, -2.5), (5, 2.5)]):
        cylinder(f"PEL_ECO_ReefBovine_Leg_{i}", (150 + dx, -120 + dy, 6), 1.1, 9, m["coral"], groups["eco"], "PEL-ECO-BOV-001", "reef_bovine_leg", 10)
    for i in range(7):
        a = 2 * math.pi * i / 7
        curve(f"PEL_ECO_ScribeCoral_{i}", [(210, -20, 3), (210 + math.cos(a) * 9, -20 + math.sin(a) * 9, 18), (210 + math.cos(a) * 16, -20 + math.sin(a) * 16, 35)], 1.3, m["cyan"], groups["eco"], "PEL-ECO-SCRIBE-001", "scribe_coral")

    # Human/NPC/enemy proxies.
    humanoid_proxy("PEL_NPC_Nara", (-485, -65, 16), m["cyan"], (m["dark"], m["ivory"]), groups["npc"], "PEL-NPC-NARA", "npc_nara")
    humanoid_proxy("PEL_NPC_Damian", (-450, -30, 16), m["amber"], (m["dark"], m["ivory"]), groups["npc"], "PEL-NPC-DAMIAN", "npc_damian")
    humanoid_proxy("PEL_NPC_Tea", (-30, 50, 12), m["cyan"], (m["dark"], m["ivory"]), groups["npc"], "PEL-NPC-TEA", "npc_tea")
    humanoid_proxy("PEL_EN_ExtractionDiver", (300, 60, 7), m["red"], (m["dark"], m["ivory"]), groups["enemy"], "PEL-EN-DIVER", "enemy_extraction_diver")
    curve("PEL_EN_DiverHarpoonCable", [(300, 60, 8), (320, 70, 6), (340, 85, 7)], 0.15, m["red"], groups["enemy"], "PEL-EN-DIVER-WPN", "cuttable_harpoon_cable")
    sphere("PEL_EN_PolypGuard", (260, -80, 8), (3.6, 3.6, 6.5), m["coral"], groups["enemy"], "PEL-EN-POLYP", "enemy_polyp_guard")
    for i in range(6):
        a = 2 * math.pi * i / 6
        curve(f"PEL_EN_PolypArm_{i}", [(260, -80, 9), (260 + math.cos(a) * 5, -80 + math.sin(a) * 5, 10), (260 + math.cos(a) * 9, -80 + math.sin(a) * 9, 5)], 0.8, m["coral"], groups["enemy"], "PEL-EN-POLYP", "polyp_arm")
    curve("PEL_EN_SentinelEel", [(360, -180, 8), (400, -140, 14), (450, -170, 10), (490, -125, 17)], 2.8, m["red"], groups["enemy"], "PEL-EN-EEL", "enemy_sentinel_eel")

    # Nácar-2 proxy.
    sphere("PEL_VEH_Nacar2_Hull", (-250, -360, 16), (7.5, 3.2, 2.7), m["ivory"], groups["vehicle"], "PEL-VEH-NACAR2", "submersible_hull")
    sphere("PEL_VEH_Nacar2_Canopy", (-248, -360, 18.5), (3.3, 2.4, 1.3), m["glass"], groups["vehicle"], "PEL-VEH-NACAR2", "submersible_canopy")
    for side in (-1, 1):
        cube(f"PEL_VEH_Nacar2_Fin_{side}", (-251, -360 + side * 5, 15), (4.5, 4, 0.45), m["bronze"], groups["vehicle"], "PEL-VEH-NACAR2", "submersible_fin", 0.25, "none")
        cylinder(f"PEL_VEH_Nacar2_Thruster_{side}", (-257, -360 + side * 2.5, 16), 1.3, 2.3, m["dark"], groups["vehicle"], "PEL-VEH-NACAR2", "thruster", 16)
    humanoid_proxy("PEL_SCALE_Human", (-238, -360, 12.3), m["amber"], (m["dark"], m["ivory"]), groups["guides"], "PEL-SCALE-HUMAN", "scale_reference")

    # Cameras and motivated lighting.
    overview = camera("CAM_PELAGOS_WORLD_OVERVIEW", (820, -1080, 620), (0, 0, -15), 46, groups["cameras"])
    camera("CAM_PELAGOS_GAME_35MM", (-655, -330, 40), (-510, -50, 15), 35, groups["cameras"])
    camera("CAM_PELAGOS_THALASSA", (578, 172, -64), (520, 230, -82), 42, groups["cameras"])
    scene.camera = overview

    sun_data = bpy.data.lights.new("TALAS_K2V_SUN_DATA", "SUN")
    sun_data.energy = 3.0
    sun_data.color = (1.0, 0.78, 0.58)
    sun_data.angle = math.radians(7)
    sun = bpy.data.objects.new("TALAS_K2V_SUN", sun_data)
    groups["lights"].objects.link(sun)
    sun.rotation_euler = (math.radians(32), math.radians(-18), math.radians(24))
    spot("PEL_MARKET_REFUGE_SPOT", (-520, -160, 160), 6200, (1.0, 0.33, 0.07), (-520, -60, 10), groups["lights"])
    spot("PEL_REEF_MEMORY_SPOT", (0, 80, 220), 7200, (0.06, 0.45, 0.75), (0, 40, 15), groups["lights"])
    spot("PEL_TRENCH_WARNING_SPOT", (520, 120, 180), 6800, (0.8, 0.05, 0.015), (520, 230, 0), groups["lights"])

    return scene


def main():
    options = parse_args()
    build()
    if options.blend:
        Path(options.blend).parent.mkdir(parents=True, exist_ok=True)
        bpy.ops.wm.save_as_mainfile(filepath=str(Path(options.blend)))
    if options.glb:
        Path(options.glb).parent.mkdir(parents=True, exist_ok=True)
        bpy.ops.export_scene.gltf(filepath=str(Path(options.glb)), export_format="GLB")


if __name__ == "__main__":
    main()
