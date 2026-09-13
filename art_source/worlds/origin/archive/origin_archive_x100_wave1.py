"""ORIGIN / Archivo de la Primera Herida — X100 Wave 01 generator.

Blender 5.2 deterministic reusable structural-kit source. Dimensions are proposals
until native Godot assembly/traversal validates them. The script intentionally excludes
Corazón de EXOVANT, final boss assets and final narrative-state logic.
"""
import bpy
import math
from mathutils import Vector

CLAIM = "CLM-ORIGIN-ARCH-ARCHIVE-001"


def ensure_collection(name):
    c = bpy.data.collections.get(name) or bpy.data.collections.new(name)
    if not any(x == c for x in bpy.context.scene.collection.children):
        bpy.context.scene.collection.children.link(c)
    return c


STR = ensure_collection("01_ARCH_STRUCTURE")
MEM = ensure_collection("02_ARCH_MEMORY")
BRZ = ensure_collection("03_ARCH_BRONZE")
COL = ensure_collection("04_ARCH_COLLISION")
PRE = ensure_collection("90_PREVIEW")


def material(name, color, metal=0.0, rough=0.5, emission=None, strength=0.0):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    p = m.node_tree.nodes.get("Principled BSDF")
    p.inputs["Base Color"].default_value = (*color, 1)
    p.inputs["Metallic"].default_value = metal
    p.inputs["Roughness"].default_value = rough
    if emission and "Emission Color" in p.inputs:
        p.inputs["Emission Color"].default_value = (*emission, 1)
        p.inputs["Emission Strength"].default_value = strength
    m["material_phase"] = "PBR_RESPONSE_V1"
    m["texture_state"] = "NO_TEXTURE_MAPS_YET"
    return m


BLACK = material("ORG_ARC_MAT_BlackMineral", (0.018, 0.022, 0.027), 0.28, 0.46)
LOAD = material("ORG_ARC_MAT_LoadStone", (0.035, 0.038, 0.041), 0.18, 0.58)
BRONZE = material("ORG_ARC_MAT_LivingBronze", (0.22, 0.075, 0.028), 0.90, 0.30)
PATINA = material("ORG_ARC_MAT_Patina", (0.045, 0.15, 0.12), 0.62, 0.54)
MEMORY = material("ORG_ARC_MAT_MemoryGlass", (0.05, 0.072, 0.078), 0.10, 0.20, (0.15, 0.36, 0.40), 0.65)
SCAR = material("ORG_ARC_MAT_WoundTrace", (0.18, 0.032, 0.026), 0.24, 0.44, (0.48, 0.045, 0.025), 0.35)
COLMAT = material("ORG_ARC_MAT_CollisionPreview", (0.08, 0.18, 0.25), 0.0, 0.8)


def move(o, c):
    for u in list(o.users_collection):
        u.objects.unlink(o)
    c.objects.link(o)


def parent_keep_world(o, parent):
    world = o.matrix_world.copy()
    o.parent = parent
    o.matrix_parent_inverse = parent.matrix_world.inverted()
    o.matrix_world = world


def bevel(o, width=0.06):
    if o.type == "MESH" and width > 0:
        b = o.modifiers.new("ARC_BEVEL", "BEVEL")
        b.width = width
        b.segments = 2


def box(name, loc, half, mat, collection, parent=None, width=0.06):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    o = bpy.context.object
    o.name = name
    o.scale = half
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    move(o, collection)
    o.data.materials.append(mat)
    bevel(o, width)
    if parent:
        parent_keep_world(o, parent)
    return o


def cylinder(name, loc, radius, depth, mat, collection, parent=None, vertices=16, width=0.04, rotation=(0, 0, 0)):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=loc, rotation=rotation)
    o = bpy.context.object
    o.name = name
    move(o, collection)
    o.data.materials.append(mat)
    bevel(o, width)
    if parent:
        parent_keep_world(o, parent)
    return o


def torus(name, loc, major, minor, mat, collection, parent=None, rotation=(0, 0, 0)):
    bpy.ops.mesh.primitive_torus_add(major_radius=major, minor_radius=minor, major_segments=24, minor_segments=8, location=loc, rotation=rotation)
    o = bpy.context.object
    o.name = name
    move(o, collection)
    o.data.materials.append(mat)
    if parent:
        parent_keep_world(o, parent)
    return o


def asset(asset_id, family, variant, state, role, location):
    old = bpy.data.objects.get(asset_id)
    if old:
        bpy.data.objects.remove(old, do_unlink=True)
    e = bpy.data.objects.new(asset_id, None)
    STR.objects.link(e)
    e.location = location
    for k, v in {
        "asset_id": asset_id,
        "claim_id": CLAIM,
        "family": family,
        "variant": variant,
        "state": state,
        "semantic_role": role,
        "lod_level": 0,
        "lod_strategy": "LOD0 authored; LOD1 target 45-60% triangles; LOD2 target 15-25%; HLOD by corridor cluster",
        "truth_state": "authored_family_candidate",
        "dimension_status": "PROPOSAL_UNTIL_ENGINE_ASSEMBLY",
    }.items():
        e[k] = v
    return e


def finish(e, proxy_half, proxy_z):
    c = box("COL_" + e.name, Vector((e.location.x, e.location.y, proxy_z)), proxy_half, COLMAT, COL, e, 0)
    c.hide_render = True
    c.display_type = "WIRE"
    c["collision_proxy"] = True
    for o in e.children_recursive:
        for k in ("asset_id", "claim_id", "family", "variant", "state", "semantic_role", "lod_level", "lod_strategy", "truth_state", "dimension_status"):
            o[k] = e[k]
    c["collision_proxy"] = True


POSITIONS = [Vector((x, y, 0)) for y in (12, 0, -12) for x in (-24, -16, -8, 0, 8, 16, 24)]
_position_index = 0


def next_position():
    global _position_index
    p = POSITIONS[_position_index]
    _position_index += 1
    return p


def rib_wall(a, variant, state):
    p = next_position()
    e = asset(a, "archive_rib_wall", variant, state, "load-bearing archive rib with maintenance void", p)
    h = {"A": 5.0, "B": 6.5, "C": 8.0}[variant]
    gap = {"A": 3.4, "B": 4.2, "C": 5.0}[variant]
    for s in (-1, 1):
        box(a + f"_PIER_{s}", p + Vector((s * (gap / 2 + 0.45), 0, h / 2)), (0.42, 0.70, h / 2), LOAD, STR, e, 0.10)
        box(a + f"_LOADTRACE_{s}", p + Vector((s * (gap / 2 + 0.08), -0.74, h * 0.55)), (0.12, 0.10, h * 0.34), BRONZE, BRZ, e, 0.025)
    box(a + "_LINTEL", p + Vector((0, 0, h - 0.35)), (gap / 2 + 0.9, 0.70, 0.35), BLACK, STR, e, 0.12)
    box(a + "_WOUND", p + Vector((0, -0.72, h * 0.38)), (gap / 2, 0.05, 0.06), SCAR, MEM, e, 0.02)
    finish(e, (gap / 2 + 0.9, 0.55, h / 2), h / 2)


def vault_frame(a, variant, state):
    p = next_position()
    e = asset(a, "archive_vault_frame", variant, state, "sealed memory-vault threshold frame", p)
    w = {"A": 4.2, "B": 5.0, "C": 6.0}[variant]
    h = {"A": 4.6, "B": 5.5, "C": 6.5}[variant]
    for s in (-1, 1):
        box(a + f"_JAMB_{s}", p + Vector((s * w / 2, 0, h / 2)), (0.34, 0.82, h / 2), BLACK, STR, e, 0.10)
    box(a + "_HEADER", p + Vector((0, 0, h)), (w / 2 + 0.34, 0.82, 0.34), LOAD, STR, e, 0.10)
    torus(a + "_SEAL", p + Vector((0, -0.86, h * 0.55)), min(w * 0.28, h * 0.25), 0.07, BRONZE, BRZ, e, (math.pi / 2, 0, 0))
    finish(e, (w / 2 + 0.34, 0.64, h / 2), h / 2)


def bridge_socket(a, variant, state):
    p = next_position()
    e = asset(a, "archive_bridge_socket", variant, state, "standard bridge docking / load-transfer node", p)
    size = {"A": 2.4, "B": 3.0, "C": 3.6}[variant]
    box(a + "_BLOCK", p + Vector((0, 0, 1.1)), (size / 2, 1.1, 1.1), LOAD, STR, e, 0.12)
    torus(a + "_DOCK", p + Vector((0, -1.14, 1.15)), size * 0.26, 0.10, BRONZE, BRZ, e, (math.pi / 2, 0, 0))
    for x in (-size * 0.3, size * 0.3):
        cylinder(a + f"_PIN_{x:.1f}", p + Vector((x, -1.18, 1.15)), 0.09, 0.42, PATINA, BRZ, e, 12, 0.02, (math.pi / 2, 0, 0))
    finish(e, (size / 2, 0.95, 1.1), 1.1)


def memory_cell(a, variant, state):
    p = next_position()
    e = asset(a, "archive_memory_cell", variant, state, "modular witness-memory storage cell", p)
    h = {"A": 2.4, "B": 3.2, "C": 4.0}[variant]
    r = {"A": 0.65, "B": 0.78, "C": 0.92}[variant]
    cylinder(a + "_VESSEL", p + Vector((0, 0, h / 2 + 0.25)), r, h, MEMORY, MEM, e, 20, 0.05)
    torus(a + "_LOW", p + Vector((0, 0, 0.28)), r + 0.10, 0.07, BRONZE, BRZ, e)
    torus(a + "_HIGH", p + Vector((0, 0, h + 0.25)), r + 0.10, 0.07, BRONZE, BRZ, e)
    box(a + "_TRACE", p + Vector((r + 0.03, 0, h * 0.58)), (0.05, 0.18, h * 0.20), SCAR, MEM, e, 0.02)
    finish(e, (r, r, h / 2), h / 2 + 0.25)


def floor_spine(a, variant, state):
    p = next_position()
    e = asset(a, "archive_floor_spine", variant, state, "load-bearing floor spine / snap baseline", p)
    length = {"A": 5.0, "B": 7.5}[variant]
    box(a + "_DECK", p + Vector((0, 0, 0.22)), (length / 2, 1.6, 0.22), BLACK, STR, e, 0.08)
    box(a + "_LOAD", p + Vector((0, 0, -0.08)), (length / 2, 0.55, 0.12), LOAD, STR, e, 0.05)
    for x in (-length * 0.35, 0, length * 0.35):
        cylinder(a + f"_PORT_{x:.1f}", p + Vector((x, -1.45, 0.28)), 0.12, 0.18, BRONZE, BRZ, e, 12, 0.02, (math.pi / 2, 0, 0))
    finish(e, (length / 2, 1.5, 0.22), 0.22)


def ceiling_rib(a, variant, state):
    p = next_position()
    e = asset(a, "archive_ceiling_rib", variant, state, "ceiling load rib / conduit carrier", p)
    span = {"A": 4.5, "B": 5.5, "C": 6.5}[variant]
    z = 4.6
    box(a + "_BEAM", p + Vector((0, 0, z)), (span / 2, 0.38, 0.28), LOAD, STR, e, 0.09)
    for s in (-1, 1):
        box(a + f"_DROP_{s}", p + Vector((s * (span / 2 - 0.35), 0, z - 0.8)), (0.18, 0.38, 0.82), BLACK, STR, e, 0.06)
    box(a + "_CHANNEL", p + Vector((0, -0.40, z - 0.05)), (span / 2 - 0.25, 0.06, 0.07), BRONZE, BRZ, e, 0.02)
    finish(e, (span / 2, 0.32, 0.28), z)


def threshold(a, variant, state):
    p = next_position()
    e = asset(a, "archive_threshold", variant, state, "floor threshold indicating archive access state", p)
    w = {"A": 4.0, "B": 5.5}[variant]
    box(a + "_STONE", p + Vector((0, 0, 0.12)), (w / 2, 0.65, 0.12), LOAD, STR, e, 0.05)
    for s in (-1, 1):
        box(a + f"_BRONZE_{s}", p + Vector((s * (w / 2 - 0.2), -0.02, 0.22)), (0.08, 0.55, 0.08), BRONZE, BRZ, e, 0.02)
    box(a + "_MEMLINE", p + Vector((0, -0.62, 0.20)), (w / 2 - 0.35, 0.035, 0.035), MEMORY, MEM, e, 0.01)
    finish(e, (w / 2, 0.60, 0.12), 0.12)


def core_shell(a, variant, state):
    p = next_position()
    e = asset(a, "archive_core_shell", variant, state, "non-boss archival index shell", p)
    r = {"A": 2.2, "B": 2.8}[variant]
    h = {"A": 3.6, "B": 4.4}[variant]
    cylinder(a + "_CORE", p + Vector((0, 0, h / 2)), r, h, BLACK, STR, e, 24, 0.10)
    for z in (0.6, h / 2, h - 0.55):
        torus(a + f"_RING_{z:.1f}", p + Vector((0, 0, z)), r + 0.08, 0.08, BRONZE, BRZ, e)
    cylinder(a + "_INDEX", p + Vector((0, -r - 0.05, h * 0.58)), r * 0.36, 0.18, MEMORY, MEM, e, 20, 0.03, (math.pi / 2, 0, 0))
    finish(e, (r * 0.92, r * 0.92, h / 2), h / 2)


def build():
    global _position_index
    _position_index = 0
    for args in [("ORG_ARC_RIB_WALL_A","A","pristine"),("ORG_ARC_RIB_WALL_B","B","used"),("ORG_ARC_RIB_WALL_C","C","scarred")]: rib_wall(*args)
    for args in [("ORG_ARC_VAULT_FRAME_A","A","sealed"),("ORG_ARC_VAULT_FRAME_B","B","used"),("ORG_ARC_VAULT_FRAME_C","C","repaired")]: vault_frame(*args)
    for args in [("ORG_ARC_BRIDGE_SOCKET_A","A","pristine"),("ORG_ARC_BRIDGE_SOCKET_B","B","used"),("ORG_ARC_BRIDGE_SOCKET_C","C","scarred")]: bridge_socket(*args)
    for args in [("ORG_ARC_MEMORY_CELL_A","A","sealed"),("ORG_ARC_MEMORY_CELL_B","B","used"),("ORG_ARC_MEMORY_CELL_C","C","fractured-contained")]: memory_cell(*args)
    for args in [("ORG_ARC_FLOOR_SPINE_A","A","used"),("ORG_ARC_FLOOR_SPINE_B","B","repaired")]: floor_spine(*args)
    for args in [("ORG_ARC_CEILING_RIB_A","A","pristine"),("ORG_ARC_CEILING_RIB_B","B","used"),("ORG_ARC_CEILING_RIB_C","C","scarred")]: ceiling_rib(*args)
    for args in [("ORG_ARC_THRESHOLD_A","A","active"),("ORG_ARC_THRESHOLD_B","B","dormant")]: threshold(*args)
    for args in [("ORG_ARC_ARCHIVE_CORE_SHELL_A","A","sealed"),("ORG_ARC_ARCHIVE_CORE_SHELL_B","B","used")]: core_shell(*args)

    scene = bpy.context.scene
    if scene.world is None:
        scene.world = bpy.data.worlds.new("ORIGIN_ARCHIVE_WORLD")
    scene.world.color = (0.004, 0.005, 0.008)
    scene["x100_protocol_active"] = True
    scene["x100_wave"] = 1
    scene["world"] = "ORIGIN"
    scene["region"] = "Archivo de la Primera Herida"
    scene["claim_id"] = CLAIM
    scene["corridor_dimensions"] = "PROPOSAL"
    scene["boss_or_heart_included"] = False
    scene["design_contract"] = "recursive load ribs + living bronze traces + bounded memory glass; causal wear only"


if __name__ == "__main__":
    build()
