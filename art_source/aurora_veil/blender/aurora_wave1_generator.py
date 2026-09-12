"""AURORA VEIL — deterministic Wave-1 Blender generator.

Purpose: reconstruct the semantic world blockout created live in 3D Jutsu.
Target: Blender 5.2+, metric units, portable Principled materials.
Authority: WORLD_BIBLE.md + ADR-AUR-001 + MASTER_ASSET_LIST.yaml.

IMPORTANT:
- This script generates a BLOCKOUT, not final AAA art.
- 5,900 km planet radius is PROPOSAL metadata only.
- It never creates a monolithic planet mesh.
- Final remote revision 5 remains the execution receipt until this checked-in
  script is replay-tested in a later run.
"""
import bpy
import math
import random
from mathutils import Vector

WORLD_ID = "aurora"
CLAIM_ID = "CLM-AURORA-WORLD-001"
PLANET_RADIUS_M_PROPOSAL = 5_900_000.0
LOCAL_EXTENT_X_M = 5_200.0
LOCAL_EXTENT_Y_M = 3_000.0
STREAM_CELL_M_PROPOSAL = 256.0


def reset_scene():
    for o in list(bpy.data.objects):
        bpy.data.objects.remove(o, do_unlink=True)
    for c in list(bpy.data.collections):
        bpy.data.collections.remove(c)


def new_material(name, color, metallic=0.0, roughness=0.5, emission=None):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    p = m.node_tree.nodes.get("Principled BSDF")
    p.inputs["Base Color"].default_value = (*color, 1.0)
    p.inputs["Metallic"].default_value = metallic
    p.inputs["Roughness"].default_value = roughness
    if emission:
        p.inputs["Emission Color"].default_value = (*emission[0], 1.0)
        p.inputs["Emission Strength"].default_value = emission[1]
    return m


def relink(obj, collection):
    for c in list(obj.users_collection):
        c.objects.unlink(obj)
    collection.objects.link(obj)
    return obj


def add_cube(name, loc, dims, mat, collection, bevel=0.0):
    bpy.ops.mesh.primitive_cube_add(location=loc)
    o = bpy.context.object
    o.name = name
    o.dimensions = dims
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if bevel:
        b = o.modifiers.new("physical_bevel", "BEVEL")
        b.width = bevel
        b.segments = 2
    if mat:
        o.data.materials.append(mat)
    return relink(o, collection)


def add_cylinder(name, loc, radius, depth, mat, collection, rotation=(0, 0, 0), vertices=18):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=loc, rotation=rotation)
    o = bpy.context.object
    o.name = name
    if mat:
        o.data.materials.append(mat)
    return relink(o, collection)


def add_sphere(name, loc, scale, mat, collection, segments=16, rings=8):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=segments, ring_count=rings, location=loc)
    o = bpy.context.object
    o.name = name
    o.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if mat:
        o.data.materials.append(mat)
    return relink(o, collection)


def add_torus(name, loc, major_radius, minor_radius, mat, collection, rotation=(0, 0, 0), segments=36):
    bpy.ops.mesh.primitive_torus_add(
        major_radius=major_radius,
        minor_radius=minor_radius,
        major_segments=segments,
        minor_segments=8,
        location=loc,
        rotation=rotation,
    )
    o = bpy.context.object
    o.name = name
    if mat:
        o.data.materials.append(mat)
    return relink(o, collection)


def add_between(name, a, b, radius, mat, collection, vertices=12):
    a = Vector(a)
    b = Vector(b)
    v = b - a
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=v.length, location=(a + b) / 2)
    o = bpy.context.object
    o.name = name
    o.rotation_euler = v.to_track_quat("Z", "Y").to_euler()
    if mat:
        o.data.materials.append(mat)
    return relink(o, collection)


def add_curve(name, points, radius, mat, collection):
    cu = bpy.data.curves.new(name, "CURVE")
    cu.dimensions = "3D"
    cu.resolution_u = 1
    cu.bevel_depth = radius
    cu.bevel_resolution = 2
    sp = cu.splines.new("POLY")
    sp.points.add(len(points) - 1)
    for i, p in enumerate(points):
        sp.points[i].co = (*p, 1.0)
    o = bpy.data.objects.new(name, cu)
    collection.objects.link(o)
    cu.materials.append(mat)
    return o


def look_at(obj, target):
    obj.rotation_euler = (Vector(target) - obj.location).to_track_quat("-Z", "Y").to_euler()


def terrain_z(x, y):
    base = 2.0 * math.sin(x / 230.0) + 1.3 * math.cos(y / 185.0) + 0.8 * math.sin((x + y) / 110.0)
    d_camp = math.hypot(x + 1600.0, y - 350.0)
    d_plain = math.hypot(x, y + 50.0)
    d_orchard = math.hypot(x - 1650.0, y - 250.0)
    return (
        base
        + 8.0 * math.exp(-((d_camp / 720.0) ** 2))
        - 2.0 * math.exp(-((d_plain / 820.0) ** 2))
        + 7.0 * math.exp(-((d_orchard / 680.0) ** 2))
        - 5.2 * math.exp(-((d_orchard / 220.0) ** 2))
    )


def build():
    reset_scene()
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.length_unit = "METERS"
    scene.unit_settings.scale_length = 1.0
    scene.render.engine = "BLENDER_EEVEE"
    scene["world_id"] = WORLD_ID
    scene["claim_id"] = CLAIM_ID
    scene["agent_id"] = "AGENT-02-AURORA"
    scene["gravity_g"] = 0.94
    scene["temperature_reference_c"] = 11.0
    scene["planet_radius_m_proposal"] = PLANET_RADIUS_M_PROPOSAL
    scene["planet_radius_status"] = "PROPOSAL_ADR_AUR_001"
    scene["temporal_rule"] = "bounded local echoes only; no whole-world rewind"
    scene["streaming_cell_planning_m"] = STREAM_CELL_M_PROPOSAL
    scene["status"] = "SCRIPTED_WAVE1_BLOCKOUT"

    root = bpy.data.collections.new("AURORA_VEIL_ROOT")
    scene.collection.children.link(root)
    names = [
        "00_META", "01_TERRAIN", "02_R01_CAMP", "03_R02_PLAIN", "04_R03_ORCHARD",
        "05_TEMPORAL", "06_ECO_PROXY", "07_POP_PROXY", "08_VEHICLE_PROXY",
        "09_COLLISION", "10_STREAMING", "11_VISTA", "12_LIGHTING", "13_CAMERAS",
    ]
    C = {}
    for n in names:
        C[n] = bpy.data.collections.new(n)
        root.children.link(C[n])

    M = {
        "prairie": new_material("M_AUR_PRAIRIE", (0.07, 0.11, 0.07), roughness=0.9),
        "stone": new_material("M_AUR_STONE", (0.12, 0.14, 0.15), roughness=0.82),
        "ivory": new_material("M_EXO_IVORY_CERAMIC", (0.62, 0.60, 0.52), 0.05, 0.42),
        "steel": new_material("M_AUR_PRECISION_STEEL", (0.055, 0.075, 0.09), 0.78, 0.28),
        "brass": new_material("M_AUR_TIMING_ALLOY", (0.34, 0.18, 0.055), 0.72, 0.32),
        "dark": new_material("M_AUR_TECH_DARK", (0.018, 0.024, 0.028), 0.45, 0.44),
        "echo": new_material("M_AUR_ECHO_CYAN", (0.015, 0.14, 0.17), 0.18, 0.3, ((0.04, 0.95, 1.0), 4.5)),
        "amber": new_material("M_EXO_REFUGE_AMBER", (0.32, 0.12, 0.018), 0.18, 0.38, ((1.0, 0.23, 0.03), 3.5)),
        "hostile": new_material("M_EXO_HOSTILE_VERMILION", (0.30, 0.01, 0.008), 0.15, 0.38, ((1.0, 0.02, 0.01), 4.0)),
        "grass": new_material("M_AUR_TWO_SHADOW_GRASS", (0.075, 0.16, 0.09), roughness=0.78),
        "aurora": new_material("M_AUR_AURORA", (0.03, 0.18, 0.16), 0.0, 0.25, ((0.03, 1.0, 0.65), 6.0)),
    }

    # Terrain: intentionally low-frequency macro topology.
    sx, sy, nx, ny = LOCAL_EXTENT_X_M, LOCAL_EXTENT_Y_M, 81, 49
    verts, faces = [], []
    for j in range(ny):
        y = -sy / 2 + sy * j / (ny - 1)
        for i in range(nx):
            x = -sx / 2 + sx * i / (nx - 1)
            verts.append((x, y, terrain_z(x, y)))
    for j in range(ny - 1):
        for i in range(nx - 1):
            a = j * nx + i
            faces.append((a, a + 1, a + 1 + nx, a + nx))
    me = bpy.data.meshes.new("AURORA_MACRO_TERRAIN_MESH")
    me.from_pydata(verts, [], faces)
    me.update()
    terrain = bpy.data.objects.new("AURORA_MACRO_TERRAIN", me)
    C["01_TERRAIN"].objects.link(terrain)
    me.materials.append(M["prairie"])
    terrain["extent_m"] = [sx, sy]
    for p in me.polygons:
        p.use_smooth = True

    anchors = {
        "AUR_R01_CAMP_SECOND_DAY": (-1600, 350, terrain_z(-1600, 350)),
        "AUR_R02_REPETITION_PLAIN": (0, -50, terrain_z(0, -50)),
        "AUR_R03_AEON_ORCHARD": (1650, 250, terrain_z(1650, 250)),
    }
    for rid, loc in anchors.items():
        e = bpy.data.objects.new(rid, None)
        e.location = loc
        e.empty_display_size = 30
        e["region_id"] = rid
        e["local_tangent_frame"] = True
        C["00_META"].objects.link(e)

    # Campamento del Segundo Día.
    cx, cy, _ = anchors["AUR_R01_CAMP_SECOND_DAY"]
    for i in range(10):
        row, col = divmod(i, 5)
        x = cx - 180 + col * 85
        y = cy - 110 + row * 120
        z = terrain_z(x, y)
        h = add_cube(f"AUR_CAMP_HAB_{i:02d}", (x, y, z + 2.1), (56, 28, 4.2), M["ivory"], C["02_R01_CAMP"], 1.0)
        h["asset_family"] = "AUR-ARC-003"
        add_cube(f"AUR_CAMP_SERVICE_{i:02d}", (x, y + 15.2, z + 2.1), (36, 2, 2.6), M["dark"], C["02_R01_CAMP"], 0.25)

    obs = (cx + 80, cy + 125, terrain_z(cx + 80, cy + 125) + 31)
    # Exact 48 m outer diameter: major radius 22.7 + minor 1.3 = outer radius 24.
    ring = add_torus("AUR_OBSERVATORY_PRIMARY_RING", obs, 22.7, 1.3, M["steel"], C["02_R01_CAMP"], (math.radians(72), 0, math.radians(8)), 56)
    ring["asset_id"] = "AUR-ARC-001"
    ring["outer_diameter_m"] = 48.0
    add_torus("AUR_OBSERVATORY_TIMING_RING", obs, 17.0, 0.7, M["brass"], C["02_R01_CAMP"], (math.radians(72), 0, math.radians(8)), 48)
    for k, a in enumerate([0, 90, 180, 270]):
        r = math.radians(a)
        p = (obs[0] + 19 * math.cos(r), obs[1] + 19 * math.sin(r), terrain_z(obs[0] + 19 * math.cos(r), obs[1] + 19 * math.sin(r)) + 1)
        top = (obs[0] + 17 * math.cos(r), obs[1] + 17 * math.sin(r), obs[2] - 2)
        add_between(f"AUR_OBS_SUPPORT_{k}", p, top, 1.2, M["steel"], C["02_R01_CAMP"])
    mast_ground = terrain_z(cx + 80, cy + 125)
    add_cylinder("AUR_OBSERVATORY_MAST", (cx + 80, cy + 125, mast_ground + 36), 2.8, 72, M["steel"], C["02_R01_CAMP"], vertices=20)
    for h in [12, 28, 44, 60]:
        add_torus(f"AUR_MAST_RING_{h}", (cx + 80, cy + 125, mast_ground + h), 5.5, 0.35, M["brass"], C["02_R01_CAMP"], segments=28)
    for i, (dx, dy) in enumerate([(-250, -45), (-70, 170), (250, -110)]):
        x, y = cx + dx, cy + dy
        z = terrain_z(x, y)
        add_cylinder(f"AUR_CLOCK_SYNC_{i}", (x, y, z + 1.1), 1.2, 2.2, M["steel"], C["02_R01_CAMP"], vertices=16)
        add_torus(f"AUR_CLOCK_DIAL_{i}", (x, y, z + 2.5), 2.2, 0.24, M["brass"], C["02_R01_CAMP"], (math.radians(90), 0, 0), 28)
        add_cylinder(f"AUR_CLOCK_BEACON_{i}", (x, y, z + 4.8), 0.32, 4.7, M["echo"], C["02_R01_CAMP"], vertices=10)

    # Llanura: three bounded local echo fields; never duplicate whole world.
    px, py, _ = anchors["AUR_R02_REPETITION_PLAIN"]
    for fi, (dx, dy) in enumerate([(-430, -180), (50, 110), (460, -120)]):
        x, y = px + dx, py + dy
        z = terrain_z(x, y) + 0.35
        add_torus(f"AUR_ECHO_FIELD_RING_{fi}", (x, y, z), 26, 0.65, M["steel"], C["05_TEMPORAL"], segments=48)
        add_torus(f"AUR_ECHO_FIELD_CUE_{fi}", (x, y, z + 0.3), 21, 0.28, M["echo"], C["05_TEMPORAL"], segments=48)
        for k, a in enumerate([0, 90, 180, 270]):
            r = math.radians(a)
            ax, ay = x + 27 * math.cos(r), y + 27 * math.sin(r)
            az = terrain_z(ax, ay)
            p = add_cylinder(f"AUR_ECHO_ANCHOR_{fi}_{k}", (ax, ay, az + 2.6), 0.55, 5.2, M["steel"], C["05_TEMPORAL"], vertices=10)
            p["delay_rule_s"] = [1.0, 1.4, 1.8][fi]
            add_torus(f"AUR_ECHO_CUE_{fi}_{k}", (ax, ay, az + 5.4), 1.5, 0.18, M["echo"], C["05_TEMPORAL"], (math.radians(90), 0, 0), 20)
        add_cube(f"AUR_ECHO_SOURCE_{fi}", (x - 7, y, terrain_z(x - 7, y) + 4), (6, 6, 8), M["stone"], C["03_R02_PLAIN"], 0.8)
        e = add_cube(f"AUR_ECHO_DELAYED_{fi}", (x + 5, y + 2, terrain_z(x + 5, y + 2) + 4), (6, 6, 8), M["echo"], C["05_TEMPORAL"], 0.8)
        e["delay_rule_s"] = [1.0, 1.4, 1.8][fi]

    # Huerto de AEON — canonical 50 m arena + 3 sectors.
    ox, oy, _ = anchors["AUR_R03_AEON_ORCHARD"]
    arena_z = terrain_z(ox, oy) + 0.7
    floor = add_cylinder("AUR_AEON_ARENA_FLOOR", (ox, oy, arena_z), 25, 1.0, M["stone"], C["04_R03_ORCHARD"], vertices=56)
    floor["asset_id"] = "AUR-AEO-003"
    floor["diameter_m"] = 50.0
    floor["dimension_status"] = "CANON"
    add_torus("AUR_AEON_ARENA_RIM", (ox, oy, arena_z + 0.65), 25, 0.8, M["brass"], C["04_R03_ORCHARD"], segments=56)
    for si, a0 in enumerate([0, 120, 240]):
        r = math.radians(a0)
        ex, ey = ox + 22 * math.cos(r), oy + 22 * math.sin(r)
        ez = terrain_z(ex, ey) + 3.5
        add_between(f"AUR_ARENA_RADIAL_{si}", (ox, oy, arena_z + 0.8), (ex, ey, arena_z + 0.8), 0.45, M["steel"], C["04_R03_ORCHARD"])
        p = add_cylinder(f"AUR_ARENA_ECHO_PYLON_{si}", (ex, ey, ez), 0.8, 7, M["steel"], C["04_R03_ORCHARD"], vertices=14)
        p["echo_sector"] = si
        p["delay_rule"] = "one_visible_delay"
        add_torus(f"AUR_ARENA_ECHO_CLOCK_{si}", (ex, ey, ez + 4), 3.1, 0.3, M["echo"], C["05_TEMPORAL"], (math.radians(90), 0, r), 28)

    for i in range(10):
        a = math.tau * i / 10
        rr = 50 + (i % 2) * 15
        x, y = ox + rr * math.cos(a), oy + rr * math.sin(a)
        z = terrain_z(x, y)
        h = 12 + (i % 4) * 2.5
        t = add_cylinder(f"AUR_ORCHARD_TREE_{i:02d}_TRUNK", (x, y, z + h / 2), 1.2, h, M["steel"], C["04_R03_ORCHARD"], vertices=16)
        t["asset_family"] = "AUR-AEO-002"
        add_torus(f"AUR_ORCHARD_TREE_{i:02d}_BASE", (x, y, z + 0.6), 3.4, 0.45, M["brass"], C["04_R03_ORCHARD"], segments=28)
        for b, off in enumerate([-1, 0, 1]):
            ang = a + off * 0.62
            start = (x, y, z + h * 0.70)
            end = (x + 8 * math.cos(ang), y + 8 * math.sin(ang), z + h + 5 + 2 * b)
            add_between(f"AUR_ORCHARD_TREE_{i:02d}_BRANCH_{b}", start, end, 0.48, M["steel"], C["04_R03_ORCHARD"], 10)
            add_sphere(f"AUR_ORCHARD_TREE_{i:02d}_CAPSULE_{b}", end, (1.6, 1.1, 2.1), M["echo"] if (i + b) % 3 == 0 else M["brass"], C["04_R03_ORCHARD"], 12, 6)

    aeon_base = arena_z + 1
    add_cylinder("AUR_AEON_TRUNK", (ox, oy, aeon_base + 6), 2.6, 12, M["dark"], C["04_R03_ORCHARD"], vertices=20)
    core = add_sphere("AUR_AEON_FUTURE_CORE", (ox, oy, aeon_base + 12.5), (4.2, 4.2, 5.2), M["echo"], C["04_R03_ORCHARD"], 20, 10)
    core["asset_id"] = "AUR-AEO-001"
    core["quality_status"] = "BLOCKOUT_ONLY"
    add_torus("AUR_AEON_CROWN_A", (ox, oy, aeon_base + 15.5), 7.2, 0.7, M["brass"], C["04_R03_ORCHARD"], (math.radians(70), 0, 0), 36)
    add_torus("AUR_AEON_CROWN_B", (ox, oy, aeon_base + 15.5), 7.2, 0.7, M["steel"], C["04_R03_ORCHARD"], (math.radians(70), 0, math.radians(60)), 36)
    for ai, a0 in enumerate([0, 120, 240]):
        r = math.radians(a0)
        end = (ox + 15 * math.cos(r), oy + 15 * math.sin(r), aeon_base + 9 + ai * 1.4)
        arm = add_between(f"AUR_AEON_ARM_{ai}", (ox, oy, aeon_base + 10), end, 0.95, M["steel"], C["04_R03_ORCHARD"], 14)
        arm["sector"] = ai
        add_torus(f"AUR_AEON_ARM_CLOCK_{ai}", end, 2.2, 0.28, M["hostile"], C["04_R03_ORCHARD"], (math.radians(90), 0, r), 24)

    # Semantic population/ecology proxies: intentionally not production characters.
    def human(name, x, y, height, ma, role):
        z = terrain_z(x, y)
        b = add_cylinder(name + "_BODY", (x, y, z + height * 0.5), 0.24, height * 0.56, ma, C["07_POP_PROXY"], vertices=10)
        b["role"] = role
        b["target_height_m"] = height
        add_sphere(name + "_HEAD", (x, y, z + height * 0.89), (0.17, 0.17, 0.2), ma, C["07_POP_PROXY"], 10, 5)

    human("AUR_NPC_ADA_NOX", -1640, 330, 1.72, M["echo"], "npc_chronobiologist")
    human("AUR_NPC_JULIAN_RE", -1620, 330, 1.80, M["ivory"], "npc_explorer")
    human("AUR_NPC_CEA_HORA", -1600, 330, 1.67, M["brass"], "npc_clockmaker")
    human("AUR_ENEMY_DELAYED_CUSTODIAN", 260, 270, 2.35, M["hostile"], "enemy_delayed_action")
    human("AUR_ENEMY_FUTURE_LOOTER", -250, 260, 1.82, M["hostile"], "enemy_delayed_traps")

    # Two-shadow grass blockout.
    random.seed(295009)
    for i in range(40):
        x = random.uniform(-1050, 1050)
        y = random.uniform(-700, 650)
        z = terrain_z(x, y)
        h = random.uniform(0.35, 0.8)
        add_cylinder(f"AUR_GRASS_{i:02d}", (x, y, z + h / 2), 0.035, h, M["grass"], C["06_ECO_PROXY"], vertices=6)
        if i % 5 == 0:
            add_cylinder(f"AUR_GRASS_ECHO_{i:02d}", (x + 0.35, y + 0.15, z + h * 0.46), 0.025, h * 0.92, M["echo"], C["05_TEMPORAL"], vertices=6)

    # Peregrino exact proposal body dimensions.
    vx, vy = -1260, 140
    vz = terrain_z(vx, vy) + 1.5
    veh = add_cube("AUR_PEREGRINO_ROUTE_RECORDER", (vx, vy, vz), (5.8, 2.7, 2.4), M["steel"], C["08_VEHICLE_PROXY"], 0.8)
    veh["asset_id"] = "AUR-VEH-001"
    veh["quality_status"] = "BLOCKOUT_ONLY"
    for wx in (-2.1, 2.1):
        for wy in (-1.45, 1.45):
            add_cylinder(f"AUR_PEREGRINO_WHEEL_{wx}_{wy}", (vx + wx, vy + wy, vz - 0.8), 0.7, 0.55, M["dark"], C["08_VEHICLE_PROXY"], (math.radians(90), 0, 0), 14)
    add_torus("AUR_PEREGRINO_RECORDER_RING", (vx, vy, vz + 2.4), 1.2, 0.18, M["echo"], C["08_VEHICLE_PROXY"], (math.radians(90), 0, 0), 20)

    # Separate collision + engine-neutral planning cells.
    for rid, (x, y, z) in anchors.items():
        col = add_cube("COL_" + rid, (x, y, z - 2), (1040, 840, 4), None, C["09_COLLISION"])
        col.display_type = "WIRE"
        col.hide_render = True
        col["collision_proxy"] = True
    arena_col = add_cylinder("COL_AUR_AEON_ARENA", (ox, oy, arena_z - 0.2), 25, 1.2, None, C["09_COLLISION"], vertices=20)
    arena_col.display_type = "WIRE"
    arena_col.hide_render = True
    arena_col["collision_proxy"] = True

    for rid, (x, y, z) in anchors.items():
        for ix in (-1, 0, 1):
            for iy in (-1, 0, 1):
                cell = add_cube(f"CELL_{rid}_{ix}_{iy}", (x + ix * STREAM_CELL_M_PROPOSAL, y + iy * STREAM_CELL_M_PROPOSAL, z + 50), (256, 256, 100), None, C["10_STREAMING"])
                cell.display_type = "WIRE"
                cell.hide_render = True
                cell["planning_cell_m"] = STREAM_CELL_M_PROPOSAL
                cell["engine_status"] = "PROPOSAL_ONLY"

    # Portable lights and delivery cameras.
    if not scene.world:
        scene.world = bpy.data.worlds.new("AURORA_WORLD")
    scene.world.use_nodes = True
    bg = scene.world.node_tree.nodes.get("Background")
    bg.inputs["Color"].default_value = (0.012, 0.022, 0.035, 1)
    bg.inputs["Strength"].default_value = 0.18

    bpy.ops.object.light_add(type="SUN", location=(-1000, -1200, 2200))
    sun = bpy.context.object
    sun.name = "SUN_VELAR_LOW"
    sun.rotation_euler = (math.radians(38), math.radians(-12), math.radians(-28))
    sun.data.energy = 2.5
    sun.data.color = (0.72, 0.83, 1.0)
    relink(sun, C["12_LIGHTING"])

    bpy.ops.object.camera_add(location=(0, -4300, 2350))
    overview = bpy.context.object
    overview.name = "CAM_AURORA_WORLD_OVERVIEW"
    overview.data.lens = 52
    overview.data.clip_start = 0.05
    overview.data.clip_end = 12000
    look_at(overview, (0, 100, 120))
    relink(overview, C["13_CAMERAS"])
    scene.camera = overview

    bpy.ops.object.camera_add(location=(cx + 620, cy - 720, 260))
    camp_cam = bpy.context.object
    camp_cam.name = "CAM_AURORA_CAMP"
    camp_cam.data.lens = 55
    camp_cam.data.clip_start = 0.05
    camp_cam.data.clip_end = 5000
    look_at(camp_cam, (cx + 50, cy + 60, 28))
    relink(camp_cam, C["13_CAMERAS"])

    bpy.ops.object.camera_add(location=(ox + 170, oy - 210, 95))
    aeon_cam = bpy.context.object
    aeon_cam.name = "CAM_AURORA_AEON"
    aeon_cam.data.lens = 58
    aeon_cam.data.clip_start = 0.05
    aeon_cam.data.clip_end = 2500
    look_at(aeon_cam, (ox, oy, arena_z + 9))
    relink(aeon_cam, C["13_CAMERAS"])

    meta = bpy.data.objects.new("META_AURORA_PLANET", None)
    C["00_META"].objects.link(meta)
    meta["physical_radius_m_proposal"] = PLANET_RADIUS_M_PROPOSAL
    meta["gravity_g_canon"] = 0.94
    meta["temperature_c_canon"] = 11.0
    meta["global_geometry_policy"] = "planet scale is logical metadata; authored geometry uses local tangent frames"

    return {
        "objects": len(bpy.data.objects),
        "materials": len(bpy.data.materials),
        "terrain_dimensions_m": list(terrain.dimensions),
        "claim": CLAIM_ID,
    }


if __name__ == "__main__":
    print(build())
