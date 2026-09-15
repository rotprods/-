#!/usr/bin/env python3
"""VANTA deterministic Blender blockout generator.

Target: Blender 5.2 LTS, metric units, editable source. This generator rebuilds
VANTA's production blockout and silhouette targets from an empty scene.

It does NOT create final AAA assets. Its purpose is to establish scale,
composition, functional silhouettes, collection contracts and reproducible
editable source before high-detail production.
"""
from __future__ import annotations

import math
import bpy
from mathutils import Vector

WORLD_ID = "vanta"
BRANCH = "art/world-vanta-001"
LINEAR = "ROT-114"
PLANET_RADIUS_M_PROPOSED = 7_600_000.0
DISTRICT_SIZE_M = 24_000.0
STREAM_CELL_M = 4_000.0
FERRUM_ARENA_DIAMETER_M = 72.0
FERRUM_TARGET_HEIGHT_M = 30.0

COLLECTIONS = [
    "00_CONTROL",
    "01_PLANETARY_CONTEXT",
    "02_TERRAIN_MACRO",
    "03_PORT_OF_HANDS",
    "04_IRON_RAIN",
    "05_FALLEN_RING",
    "06_FERRUM_ARENA",
    "07_HERO_BLOCKOUT",
    "08_NPC_TARGETS",
    "09_ENEMY_TARGETS",
    "10_BIOTA_TARGETS",
    "11_COLLISION_GUIDES",
    "12_LIGHTS",
    "13_CAMERAS",
    "14_ROUTE_GUIDES",
]


def clean() -> None:
    for obj in list(bpy.data.objects):
        bpy.data.objects.remove(obj, do_unlink=True)
    for col in list(bpy.data.collections):
        bpy.data.collections.remove(col)


def get_collection(name: str):
    col = bpy.data.collections.get(name)
    if col is None:
        col = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(col)
    return col


def move_to(obj, col):
    for owner in list(obj.users_collection):
        owner.objects.unlink(obj)
    col.objects.link(obj)
    return obj


def material(name, rgb, metallic=0.0, roughness=0.5, emission=None, strength=0.0):
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*rgb, 1.0)
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = roughness
    if emission is not None:
        bsdf.inputs["Emission Color"].default_value = (*emission, 1.0)
        bsdf.inputs["Emission Strength"].default_value = strength
    return mat


def tag(obj, state="BLOCKOUT"):
    obj["world"] = WORLD_ID
    obj["production_state"] = state
    return obj


def cube(name, loc, dims, mat, col, bevel=0.0, rot=(0, 0, 0), parent=None, state="BLOCKOUT"):
    bpy.ops.mesh.primitive_cube_add(location=loc, rotation=rot)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = dims
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if mat:
        obj.data.materials.append(mat)
    if bevel:
        mod = obj.modifiers.new("BEVEL", "BEVEL")
        mod.width = bevel
        mod.segments = 2
    move_to(obj, col)
    obj.parent = parent
    return tag(obj, state)


def cyl(name, loc, radius, depth, mat, col, vertices=24, rot=(0, 0, 0), parent=None, state="BLOCKOUT"):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=loc, rotation=rot)
    obj = bpy.context.object
    obj.name = name
    if mat:
        obj.data.materials.append(mat)
    move_to(obj, col)
    obj.parent = parent
    return tag(obj, state)


def sphere(name, loc, radius, mat, col, segments=24, rings=12, parent=None, state="BLOCKOUT"):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=segments, ring_count=rings, radius=radius, location=loc)
    obj = bpy.context.object
    obj.name = name
    if mat:
        obj.data.materials.append(mat)
    move_to(obj, col)
    obj.parent = parent
    return tag(obj, state)


def empty(name, loc, col, asset_id=None, state="SILHOUETTE_TARGET"):
    obj = bpy.data.objects.new(name, None)
    obj.empty_display_type = "PLAIN_AXES"
    obj.empty_display_size = 2
    obj.location = loc
    col.objects.link(obj)
    tag(obj, state)
    if asset_id:
        obj["asset_id"] = asset_id
    return obj


def aim(obj, target):
    obj.rotation_euler = (Vector(target) - obj.location).to_track_quat("-Z", "Y").to_euler()


def setup_scene():
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 1.0
    scene.render.engine = "BLENDER_EEVEE"
    scene.render.resolution_x = 1280
    scene.render.resolution_y = 720
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    if scene.world is None:
        scene.world = bpy.data.worlds.new("WORLD_VANTA")
    scene.world.use_nodes = True
    bg = scene.world.node_tree.nodes.get("Background")
    bg.inputs["Color"].default_value = (0.006, 0.009, 0.014, 1.0)
    bg.inputs["Strength"].default_value = 0.22
    metadata = {
        "world_id": WORLD_ID,
        "world_name": "VANTA",
        "world_status": "ART_BLOCKOUT_PLANNED",
        "gravity_design_g": 1.86,
        "temperature_reference_c": -12.0,
        "planet_radius_m_proposed": PLANET_RADIUS_M_PROPOSED,
        "planet_diameter_m_proposed": PLANET_RADIUS_M_PROPOSED * 2,
        "planet_design_note": "PROPOSED iron-rich super-Earth scale; astrophysics qualification pending.",
        "production_branch": BRANCH,
        "linear_issue": LINEAR,
        "map_primary_district_x_m": DISTRICT_SIZE_M,
        "map_primary_district_y_m": DISTRICT_SIZE_M,
        "streaming_cell_m": STREAM_CELL_M,
    }
    for key, value in metadata.items():
        scene[key] = value
    return scene


def build_materials():
    return {
        "ground": material("M_VANTA_GROUND_OXIDE", (0.055, 0.045, 0.042), 0.15, 0.88),
        "slag": material("M_VANTA_SLAG", (0.022, 0.026, 0.030), 0.68, 0.45),
        "steel": material("M_VANTA_STEEL", (0.105, 0.125, 0.145), 0.90, 0.29),
        "rust": material("M_VANTA_RUST", (0.245, 0.052, 0.021), 0.72, 0.57),
        "union": material("M_VANTA_UNION_YELLOW", (0.64, 0.30, 0.03), 0.58, 0.40),
        "magnet": material("M_VANTA_MAGNET", (0.028, 0.068, 0.086), 0.84, 0.26),
        "field": material("M_VANTA_FIELD_EMISSIVE", (0.015, 0.085, 0.12), 0.22, 0.24, (0.02, 0.58, 0.96), 5.0),
        "warning": material("M_VANTA_WARNING_RED", (0.30, 0.016, 0.01), 0.44, 0.34, (1.0, 0.018, 0.006), 2.6),
    }


def build_planet_context(c, m):
    # Display proxy only. Physical dimensions remain metadata; do not author the
    # chapter at planetary coordinates.
    obj = sphere("CTX_VANTA_PLANET_1_TO_1000", (0, 0, -9000), 7600, m["ground"], c["01_PLANETARY_CONTEXT"], 48, 24)
    obj["physical_radius_m"] = PLANET_RADIUS_M_PROPOSED
    obj["display_scale"] = "1:1000"
    obj.hide_render = True
    obj.hide_viewport = True


def build_terrain(c, m):
    cell = STREAM_CELL_M
    for ix in range(-3, 3):
        for iy in range(-3, 3):
            x, y = (ix + 0.5) * cell, (iy + 0.5) * cell
            z = -18.0 + ((ix * 17 + iy * 11) % 7) * 4.0
            obj = cube(f"TERRAIN_CELL_{ix+3:02d}_{iy+3:02d}", (x, y, z), (cell, cell, 28), m["ground"], c["02_TERRAIN_MACRO"])
            obj["stream_cell_x"] = ix + 3
            obj["stream_cell_y"] = iy + 3
            obj["cell_size_m"] = cell
    ridges = [
        (-7200, -1800, 95, 4200, 520, 220), (-3500, 900, 150, 3000, 420, 340),
        (0, -1600, 105, 5200, 380, 240), (3600, 1200, 190, 3600, 500, 420),
        (7200, -1300, 120, 3000, 420, 300), (-1500, 5200, 90, 5800, 360, 220),
        (2400, -5200, 130, 4600, 520, 300),
    ]
    for i, (x, y, z, sx, sy, sz) in enumerate(ridges):
        obj = cube(f"MACRO_RIDGE_{i:02d}", (x, y, z), (sx, sy, sz), m["slag"], c["02_TERRAIN_MACRO"], 25)
        obj.rotation_euler[2] = math.radians((i * 17) % 35 - 17)


def build_port(c, m):
    col = c["03_PORT_OF_HANDS"]
    for i in range(7):
        x, y = -5650 + i * 190, -200 + (i % 2) * 240
        cube(f"PORT_WORKSHOP_{i:02d}", (x, y, 48), (150, 190, 96), m["steel"], col, 6)
        cube(f"PORT_ROOF_{i:02d}", (x, y, 108), (170, 210, 24), m["rust"], col, 4)
    for i in range(4):
        cube(f"PORT_SHELTER_{i:02d}", (-5550 + i * 340, 430, 33), (250, 130, 66), m["slag"], col, 8)
    cube("PORT_UNION_HALL", (-5000, 0, 85), (520, 360, 170), m["union"], col, 12)
    cube("PORT_DRYDOCK_DECK", (-5000, -650, 12), (1200, 520, 24), m["steel"], col)
    for i in range(5):
        cube(f"PORT_DOCK_RIB_{i:02d}", (-5480 + i * 240, -650, 95), (34, 520, 190), m["rust"], col, 5)
    for i in range(3):
        x = -5600 + i * 520
        cube(f"PORT_CRANE_MAST_{i}", (x, -970, 165), (42, 42, 330), m["union"], col, 3)
        cube(f"PORT_CRANE_ARM_{i}", (x + 135, -970, 315), (310, 30, 30), m["steel"], col, 3)
        cube(f"PORT_CRANE_CABLE_{i}", (x + 250, -970, 230), (5, 5, 170), m["slag"], col)
    for i in range(12):
        x, y = -5850 + (i % 6) * 145, 820 + (i // 6) * 120
        cube(f"PORT_CONTAINER_{i:02d}", (x, y, 32), (120, 90, 64), m["rust"] if i % 3 else m["union"], col, 2)


def build_iron_rain(c, m):
    col = c["04_IRON_RAIN"]
    for i, y in enumerate([-480, -160, 160, 480]):
        cube(f"IRON_RAILBED_{i}", (0, y, 18), (2500, 34, 36), m["steel"], col)
        for j in range(-5, 6):
            cube(f"IRON_SLEEPER_{i}_{j}", (j * 220, y, 30), (28, 110, 18), m["rust"], col)
    for i, x in enumerate([-900, -300, 300, 900]):
        cube(f"MAG_ARCH_L_{i}", (x, -620, 140), (42, 42, 280), m["magnet"], col)
        cube(f"MAG_ARCH_R_{i}", (x, 620, 140), (42, 42, 280), m["magnet"], col)
        cube(f"MAG_ARCH_TOP_{i}", (x, 0, 270), (42, 1280, 42), m["magnet"], col, 5)
        cyl(f"MAG_FIELD_CORE_{i}", (x, 0, 270), 22, 70, m["field"], col, 24, (math.radians(90), 0, 0))
    for i in range(18):
        x, y = -1200 + (i % 6) * 470, -980 + (i // 6) * 980
        sx, sy, sz = 180 + ((i * 37) % 170), 120 + ((i * 53) % 120), 65 + ((i * 29) % 110)
        obj = cube(f"IRON_SCRAP_BANK_{i:02d}", (x, y, sz / 2), (sx, sy, sz), m["slag"] if i % 2 else m["rust"], col, 10)
        obj.rotation_euler[2] = math.radians((i * 23) % 70 - 35)
    for i, (x, y) in enumerate([(-1100, -1150), (1100, -1150), (-1100, 1150), (1100, 1150)]):
        cyl(f"STORM_BEACON_{i}", (x, y, 95), 18, 190, m["steel"], col, 16)
        cyl(f"STORM_BEACON_LIGHT_{i}", (x, y, 196), 28, 12, m["warning"], col, 16)


def build_fallen_ring(c, m):
    col = c["05_FALLEN_RING"]
    cube("RING_DRYDOCK_SPINE", (5200, 0, 55), (2200, 180, 110), m["steel"], col, 10)
    for i in range(9):
        x = 4300 + i * 225
        cube(f"RING_HULL_RIB_L_{i}", (x, -640, 180), (34, 360, 360), m["rust"], col, 8)
        cube(f"RING_HULL_RIB_R_{i}", (x, 640, 180), (34, 360, 360), m["rust"], col, 8)
        cube(f"RING_RIB_BRIDGE_{i}", (x, 0, 350), (34, 1280, 36), m["steel"], col, 5)
    for i in range(3):
        x = 4650 + i * 550
        cube(f"RING_MAGNET_TOWER_{i}", (x, 0, 330), (90, 90, 660), m["magnet"], col, 8)
        cyl(f"RING_MAGNET_COIL_{i}", (x, 0, 650), 86, 34, m["field"], col, 32)


def build_arena(c, m):
    col = c["06_FERRUM_ARENA"]
    cx, cy = 6600, 1600
    cyl("FERRUM_ARENA_DECK", (cx, cy, 12), FERRUM_ARENA_DIAMETER_M / 2, 24, m["steel"], col, 64)
    cyl("FERRUM_ARENA_INNER", (cx, cy, 26), 23, 8, m["slag"], col, 64)
    for i in range(8):
        a = math.tau * i / 8
        cube(f"ARENA_ANCHOR_{i}", (cx + 31 * math.cos(a), cy + 31 * math.sin(a), 44), (4, 8, 64), m["magnet"], col, 0.8)
    for i in range(4):
        a = math.tau * i / 4
        cyl(f"ARENA_POLARITY_NODE_{i}", (cx + 27 * math.cos(a), cy + 27 * math.sin(a), 52), 2.2, 5, m["field"], col, 24)


def build_route_and_npc_refs(c, m):
    for i, x in enumerate([-5000, -4000, -3000, -2000, -1000, 0, 1000, 2000, 3000, 4000, 5200]):
        cyl(f"ROUTE_PYLON_{i:02d}", (x, -1550, 35), 10, 70, m["field"], c["14_ROUTE_GUIDES"], 12)
    for x, name in [(-5000, "MIKA"), (-4930, "CIRO"), (-4860, "BEL")]:
        cyl(f"NPC_{name}_BODY", (x, -250, 0.83), 0.24, 1.30, m["union"], c["08_NPC_TARGETS"], 16)
        sphere(f"NPC_{name}_HEAD", (x, -250, 1.63), 0.18, m["union"], c["08_NPC_TARGETS"], 20, 12)


def build_ferrum(c, m):
    col = c["07_HERO_BLOCKOUT"]
    cx, cy = 6600, 1600
    root = empty("FERRUM_ROOT", (cx, cy, 24), col, "VANTA_BOSS_FERRUM")
    root["target_height_m"] = FERRUM_TARGET_HEIGHT_M
    root["role"] = "custodian_colossus"
    def q(name, loc, dims, mat, bevel=0.0, rot=(0,0,0)):
        return cube(name, loc, dims, mat, col, bevel, rot, root, "SILHOUETTE_TARGET")
    def y(name, loc, r, depth, mat, vertices=24, rot=(0,0,0)):
        return cyl(name, loc, r, depth, mat, col, vertices, rot, root, "SILHOUETTE_TARGET")
    q("FERRUM_PELVIS", (cx, cy, 31), (12, 8, 5), m["steel"], 0.8)
    y("FERRUM_POLARITY_CORE", (cx, cy - 4.25, 32), 2.4, 1.6, m["field"], 32, (math.radians(90), 0, 0))
    q("FERRUM_TORSO_MAIN", (cx, cy, 38), (14, 9, 8), m["rust"], 1.0)
    q("FERRUM_TORSO_ARMOR_L", (cx - 5.8, cy - 4.6, 39), (4, 1.1, 7), m["slag"], 0.5)
    q("FERRUM_TORSO_ARMOR_R", (cx + 5.8, cy - 4.6, 39), (4, 1.1, 7), m["slag"], 0.5)
    q("FERRUM_MEMORY_CABIN", (cx, cy - 4.9, 41), (6, 1.4, 4), m["magnet"], 0.35)
    for i in range(5):
        q(f"FERRUM_MEMORY_WINDOW_{i}", (cx - 2.2 + i * 1.1, cy - 5.65, 41), (0.7, 0.2, 2.2), m["field"], 0.08)
    q("FERRUM_SENSOR_HEAD", (cx, cy, 44), (5, 4, 3), m["steel"], 0.6)
    for sx in (-1.3, 1.3):
        y(f"FERRUM_EYE_{sx:+.1f}", (cx + sx, cy - 2.05, 44.2), 0.45, 0.35, m["warning"], 20, (math.radians(90),0,0))
    for i, (dx, dy) in enumerate([(-5,-3), (5,-3), (-5,3), (5,3)]):
        q(f"FERRUM_LEG_UP_{i}", (cx+dx, cy+dy, 28), (3.4,3.4,7), m["steel"], 0.5)
        q(f"FERRUM_LEG_SHIN_{i}", (cx+dx*1.25, cy+dy*1.25, 23.5), (2.7,2.7,6), m["rust"], 0.45)
        q(f"FERRUM_FOOT_{i}", (cx+dx*1.45, cy+dy*1.45, 20.5), (5.2,5.0,1.6), m["magnet"], 0.3)
    q("FERRUM_SHOULDER_BEAM", (cx,cy,41), (24,3,3.2), m["steel"], 0.5)
    q("FERRUM_ARM_L_UPPER", (cx-11,cy,38), (9,3.2,3.2), m["rust"], 0.45, (0,math.radians(-8),0))
    y("FERRUM_ARM_L_JOINT", (cx-15.5,cy,37.4), 2.2,3.8,m["magnet"],24,(math.radians(90),0,0))
    q("FERRUM_HAMMER_HANDLE", (cx-20,cy,35.8), (8,2.2,2.2), m["steel"],0.35,(0,math.radians(-12),0))
    q("FERRUM_HAMMER_QUILL", (cx-24,cy,34.9), (5.6,5.2,6.6), m["slag"],0.65)
    q("FERRUM_ARM_R_UPPER", (cx+11,cy,39), (9,3.4,3.4), m["steel"],0.45,(0,math.radians(7),0))
    y("FERRUM_ARM_R_JOINT", (cx+15.5,cy,39.5),2.3,4.0,m["magnet"],24,(math.radians(90),0,0))
    q("FERRUM_CLAW_FOREARM", (cx+19,cy,40), (6,2.8,2.8), m["rust"],0.4)
    for i, a in enumerate((-35,0,35)):
        q(f"FERRUM_CLAW_TINE_{i}", (cx+23,cy+(i-1)*2.0,40), (5.5,1.0,1.0), m["magnet"],0.2,(0,math.radians(a*0.2),0))
    for i, z in enumerate([34,37,40]):
        y(f"FERRUM_TORSO_COIL_{i}", (cx,cy,z), 7.8,0.35,m["magnet"],32)


def build_vehicle(c, m):
    col = c["07_HERO_BLOCKOUT"]
    root = empty("DRAV_TUG_ROOT", (-4700,-1650,4), col, "VANTA_VEH_DRAV_TUG")
    root["target_length_m"] = 22.0
    cube("DRAV_TUG_HULL", (-4700,-1650,5.4), (22,8.5,5.0), m["steel"], col,0.8,parent=root,state="SILHOUETTE_TARGET")
    cube("DRAV_TUG_CAB", (-4760,-1650,8.2), (6,7.4,3.1), m["magnet"], col,0.5,parent=root,state="SILHOUETTE_TARGET")
    for side in (-1,1):
        cyl(f"DRAV_TUG_THRUSTER_{side}", (-4625,-1650+side*3.1,5.2),1.6,4.2,m["rust"],col,24,(0,math.radians(90),0),root,"SILHOUETTE_TARGET")
        cube(f"DRAV_TUG_MAG_SKID_{side}", (-4700,-1650+side*4.3,3.0),(15,1.1,1.0),m["magnet"],col,0.25,parent=root,state="SILHOUETTE_TARGET")
    for i in range(4):
        cube(f"DRAV_TUG_WINDOW_{i}", (-4789,-1650-2.4+i*1.6,8.4),(0.25,1.0,1.0),m["field"],col,0.05,parent=root,state="SILHOUETTE_TARGET")


def build_enemy_targets(c, m):
    col = c["09_ENEMY_TARGETS"]
    ex, ey = -4450, 250
    root = empty("ENEMY_COLLECTOR_ROOT", (ex,ey,0), col, "VANTA_ENEMY_SHIPYARD_COLLECTOR")
    root["target_height_m"] = 2.25
    cyl("COLLECTOR_BODY",(ex,ey,1.15),0.38,1.45,m["steel"],col,16,parent=root,state="SILHOUETTE_TARGET")
    sphere("COLLECTOR_HEAD",(ex,ey,2.02),0.25,m["rust"],col,parent=root,state="SILHOUETTE_TARGET")
    cube("COLLECTOR_SHIELD",(ex-0.65,ey-0.18,1.25),(0.20,1.25,1.55),m["magnet"],col,0.08,parent=root,state="SILHOUETTE_TARGET")
    cyl("COLLECTOR_MACE_SHAFT",(ex+0.62,ey,1.25),0.07,1.8,m["steel"],col,12,(0,math.radians(8),0),root,"SILHOUETTE_TARGET")
    sphere("COLLECTOR_MACE_HEAD",(ex+0.72,ey,0.35),0.28,m["rust"],col,parent=root,state="SILHOUETTE_TARGET")

    sx, sy = -180, 980
    root = empty("ENEMY_RIVET_SWARM_ROOT",(sx,sy,2.5),col,"VANTA_ENEMY_RIVET_SWARM")
    for i in range(24):
        a, rr, z = math.tau*i/24, 1.4+(i%4)*0.28, 2.2+((i*7)%6)*0.22
        cyl(f"RIVET_SWARM_{i:02d}",(sx+math.cos(a)*rr,sy+math.sin(a)*rr,z),0.08,0.42,m["steel"],col,10,(math.radians(75),0,a),root,"SILHOUETTE_TARGET")
    cyl("RIVET_SWARM_FIELD_CORE",(sx,sy,2.5),0.42,0.8,m["field"],col,20,parent=root,state="SILHOUETTE_TARGET")

    ax, ay = 780, 1020
    root = empty("ENEMY_AUTO_TUG_ROOT",(ax,ay,2.0),col,"VANTA_ENEMY_AUTO_TUG")
    root["target_length_m"] = 8.0
    cube("AUTO_TUG_BODY",(ax,ay,2.8),(8,4.2,2.8),m["rust"],col,0.45,parent=root,state="SILHOUETTE_TARGET")
    for side in (-1,1):
        cyl(f"AUTO_TUG_ROTOR_{side}",(ax-3.7,ay+side*1.7,2.9),0.72,1.0,m["magnet"],col,20,(0,math.radians(90),0),root,"SILHOUETTE_TARGET")
    cube("AUTO_TUG_ANCHOR",(ax+4.2,ay,2.1),(1.2,2.2,1.3),m["steel"],col,0.2,parent=root,state="SILHOUETTE_TARGET")


def build_biota_targets(c, m):
    col = c["10_BIOTA_TARGETS"]
    bx, by = 350, -1050
    root = empty("BIOTA_LITHOPHAGE_ROOT",(bx,by,0),col,"VANTA_BIOTA_MAG_LITHOPHAGE")
    sphere("LITHO_BODY",(bx,by,0.55),0.62,m["slag"],col,parent=root,state="SILHOUETTE_TARGET")
    for side in (-1,1):
        for i in range(3):
            cube(f"LITHO_LEG_{side}_{i}",(bx+side*(0.55+i*0.18),by+(i-1)*0.32,0.34),(0.72,0.12,0.12),m["rust"],col,0.04,(0,math.radians(side*10),math.radians((i-1)*22)),root,"SILHOUETTE_TARGET")
        cube(f"LITHO_MANDIBLE_{side}",(bx+side*0.55,by-0.48,0.45),(0.72,0.14,0.12),m["magnet"],col,0.03,(0,0,math.radians(side*28)),root,"SILHOUETTE_TARGET")

    rx, ry = -620, -980
    root = empty("BIOTA_FILINGS_RAY_ROOT",(rx,ry,3.0),col,"VANTA_BIOTA_FILINGS_RAY")
    root["target_wingspan_m"] = 3.8
    cube("FILINGS_RAY_BODY",(rx,ry,3.0),(1.7,0.55,0.28),m["slag"],col,0.12,parent=root,state="SILHOUETTE_TARGET")
    for side in (-1,1):
        cube(f"FILINGS_RAY_WING_{side}",(rx+side*1.25,ry,3.0),(2.1,1.2,0.10),m["magnet"],col,0.06,(0,math.radians(side*6),math.radians(side*12)),root,"SILHOUETTE_TARGET")

    cx, cy = -5100, 600
    root = empty("BIOTA_RIVET_CROW_ROOT",(cx,cy,2.5),col,"VANTA_BIOTA_RIVET_CROW")
    sphere("RIVET_CROW_BODY",(cx,cy,2.5),0.24,m["steel"],col,parent=root,state="SILHOUETTE_TARGET")
    sphere("RIVET_CROW_HEAD",(cx,cy-0.27,2.68),0.15,m["rust"],col,parent=root,state="SILHOUETTE_TARGET")
    for side in (-1,1):
        cube(f"RIVET_CROW_WING_{side}",(cx+side*0.33,cy,2.52),(0.62,0.14,0.06),m["slag"],col,0.02,(0,math.radians(side*8),math.radians(side*15)),root,"SILHOUETTE_TARGET")
    cube("RIVET_CROW_BEAK",(cx,cy-0.48,2.69),(0.12,0.28,0.08),m["union"],col,0.01,parent=root,state="SILHOUETTE_TARGET")

    for i in range(12):
        x, y = 4200 + (i % 4) * 160, -1080 + (i // 4) * 180
        obj = cube(f"SLAG_BIOFILM_PATCH_{i:02d}",(x,y,0.08),(110+15*(i%3),90+12*((i+1)%3),0.16),m["field"] if i%4==0 else m["slag"],col,0.03,state="SILHOUETTE_TARGET")
        obj["asset_id"] = "VANTA_BIOTA_SLAG_BIOFILM"
        obj["instance_candidate"] = True


def build_hero_anchors(c, m):
    col = c["07_HERO_BLOCKOUT"]
    for i, x in enumerate([-5200,-5000,-4800]):
        root = empty(f"HERO_MAG_ANCHOR_ROOT_{i}",(x,1100,0),col,"VANTA_PROP_MAG_ANCHOR")
        cube(f"HERO_MAG_ANCHOR_BASE_{i}",(x,1100,0.6),(3.5,3.5,1.2),m["steel"],col,0.2,parent=root,state="SILHOUETTE_TARGET")
        cyl(f"HERO_MAG_ANCHOR_COIL_{i}",(x,1100,3.0),1.2,4.2,m["magnet"],col,28,parent=root,state="SILHOUETTE_TARGET")
        cyl(f"HERO_MAG_ANCHOR_LIGHT_{i}",(x,1100,5.25),1.35,0.3,m["field"],col,28,parent=root,state="SILHOUETTE_TARGET")


def build_cameras_lights(scene, c):
    bpy.ops.object.camera_add(location=(-9100,-10300,5200))
    cam = bpy.context.object
    cam.name = "CAM_VANTA_MASTER_WIDE"
    cam.data.lens = 42
    cam.data.sensor_width = 36
    cam.data.clip_end = 50000
    move_to(cam, c["13_CAMERAS"])
    aim(cam, (1000,0,250))
    scene.camera = cam
    for name, loc, target, lens in [
        ("CAM_PORT_QA",(-6800,-3100,1500),(-5000,0,120),50),
        ("CAM_RAIN_QA",(-1800,-3300,1200),(0,0,170),55),
        ("CAM_RING_QA",(3400,-3400,1700),(5300,0,240),55),
        ("CAM_ARENA_QA",(6550,1500,52),(6600,1600,32),32),
    ]:
        bpy.ops.object.camera_add(location=loc)
        obj = bpy.context.object
        obj.name = name
        obj.data.lens = lens
        obj.data.clip_end = 30000
        move_to(obj, c["13_CAMERAS"])
        aim(obj, target)

    bpy.ops.object.light_add(type="SUN", location=(0,0,5000))
    sun = bpy.context.object
    sun.name = "SUN_DRAV"
    sun.data.energy = 2.1
    sun.data.angle = math.radians(6)
    sun.rotation_euler = (math.radians(38),math.radians(-22),math.radians(28))
    move_to(sun, c["12_LIGHTS"])
    for name, loc, energy, color in [
        ("L_PORT_WARM",(-5000,-300,650),1700,(1.0,0.32,0.08)),
        ("L_RAIN_COLD",(0,0,750),1400,(0.08,0.42,1.0)),
        ("L_RING_COLD",(5300,0,850),1800,(0.12,0.55,1.0)),
        ("L_ARENA_RED",(6600,1600,280),900,(1.0,0.03,0.01)),
    ]:
        bpy.ops.object.light_add(type="POINT", location=loc)
        light = bpy.context.object
        light.name = name
        light.data.energy = energy
        light.data.color = color
        light.data.shadow_soft_size = 160
        move_to(light, c["12_LIGHTS"])


def validate(scene):
    arena = bpy.data.objects["FERRUM_ARENA_DECK"]
    terrain = [o for o in scene.objects if o.name.startswith("TERRAIN_CELL_")]
    assert len(terrain) == 36, len(terrain)
    assert abs(arena.dimensions.x - 72.0) < 1e-3
    assert abs(arena.dimensions.y - 72.0) < 1e-3
    assert bpy.data.objects.get("FERRUM_ROOT") is not None
    assert bpy.data.objects.get("DRAV_TUG_ROOT") is not None
    assert scene.unit_settings.system == "METRIC"
    return {
        "world": WORLD_ID,
        "objects": len(scene.objects),
        "meshes": len([o for o in scene.objects if o.type == "MESH"]),
        "collections": len(bpy.data.collections),
        "materials": len(bpy.data.materials),
        "terrain_cells": len(terrain),
        "arena_diameter_m": arena.dimensions.x,
        "ferrum_parts": len([o for o in scene.objects if o.name.startswith("FERRUM_")]),
    }


def main():
    clean()
    scene = setup_scene()
    collections = {name: get_collection(name) for name in COLLECTIONS}
    materials = build_materials()
    build_planet_context(collections, materials)
    build_terrain(collections, materials)
    build_port(collections, materials)
    build_iron_rain(collections, materials)
    build_fallen_ring(collections, materials)
    build_arena(collections, materials)
    build_route_and_npc_refs(collections, materials)
    build_ferrum(collections, materials)
    build_vehicle(collections, materials)
    build_enemy_targets(collections, materials)
    build_biota_targets(collections, materials)
    build_hero_anchors(collections, materials)
    build_cameras_lights(scene, collections)
    result = validate(scene)
    print(result)
    return result


if __name__ == "__main__":
    main()
