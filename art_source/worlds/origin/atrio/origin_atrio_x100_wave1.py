"""ORIGIN / Atrio de las Rutas — X100 Wave 01 deterministic family generator.

Run inside Blender 5.2 after the base Atrio generator/rev3-equivalent scene exists.
This script deliberately does NOT modify qualified ring/bridge/collision geometry.
It authors the service-infrastructure and El Organismo cultural-memory families
outside the validated traversal bands.
"""
import bpy
import math
from mathutils import Vector

CLAIM_INFRA = "CLM-ORIGIN-INFRA-ATRIO-SERVICE-001"
CLAIM_CULT = "CLM-ORIGIN-CULT-ORGANISM-001"
WAVE = 1


def collection(name):
    c = bpy.data.collections.get(name) or bpy.data.collections.new(name)
    if not any(x == c for x in bpy.context.scene.collection.children):
        bpy.context.scene.collection.children.link(c)
    return c


SVC = collection("06_SERVICE_INFRA_X100")
CULT = collection("07_CULTURE_MEMORY_X100")


def mat(name, color, metallic=0.0, roughness=0.5, emission=None, strength=0.0):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    p = m.node_tree.nodes.get("Principled BSDF")
    p.inputs["Base Color"].default_value = (*color, 1)
    p.inputs["Metallic"].default_value = metallic
    p.inputs["Roughness"].default_value = roughness
    if emission and "Emission Color" in p.inputs:
        p.inputs["Emission Color"].default_value = (*emission, 1)
        p.inputs["Emission Strength"].default_value = strength
    m["origin_material_logic"] = "causal_functional_response_v1"
    return m


BLACK = bpy.data.materials.get("ORG_MAT_BlackMineral_Cut") or mat("ORG_MAT_BlackMineral_Cut", (0.018, 0.022, 0.026), 0.26, 0.42)
LOAD = bpy.data.materials.get("ORG_MAT_BlackMineral_Load") or mat("ORG_MAT_BlackMineral_Load", (0.025, 0.028, 0.032), 0.32, 0.50)
BRONZE = bpy.data.materials.get("ORG_MAT_LivingBronze_Joint") or mat("ORG_MAT_LivingBronze_Joint", (0.24, 0.09, 0.035), 0.9, 0.28)
DEEP = bpy.data.materials.get("ORG_MAT_LivingBronze_Deep") or mat("ORG_MAT_LivingBronze_Deep", (0.12, 0.045, 0.02), 0.86, 0.38)
MEMORY = mat("ORG_MAT_MemoryGlass", (0.055, 0.075, 0.08), 0.12, 0.22, (0.18, 0.42, 0.46), 0.8)
PATINA = mat("ORG_MAT_BronzePatina", (0.045, 0.16, 0.13), 0.64, 0.52)
STONE = mat("ORG_MAT_WitnessStone", (0.16, 0.17, 0.16), 0.08, 0.68)
SIGNAL = bpy.data.materials.get("ORG_MAT_SignalAmber") or mat("ORG_MAT_SignalAmber", (0.28, 0.12, 0.025), 0.18, 0.32, (0.75, 0.18, 0.025), 1.2)


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
        b = o.modifiers.new("X100_BEVEL", "BEVEL")
        b.width = width
        b.segments = 2


def box(name, loc, half, material, c, parent=None, width=0.06):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    o = bpy.context.object
    o.name = name
    o.scale = half
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    move(o, c)
    o.data.materials.append(material)
    bevel(o, width)
    if parent:
        parent_keep_world(o, parent)
    return o


def cylinder(name, loc, radius, depth, material, c, parent=None, vertices=16, width=0.04, rotation=(0, 0, 0)):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=loc, rotation=rotation)
    o = bpy.context.object
    o.name = name
    move(o, c)
    o.data.materials.append(material)
    bevel(o, width)
    if parent:
        parent_keep_world(o, parent)
    return o


def torus(name, loc, major, minor, material, c, parent=None, rotation=(0, 0, 0)):
    bpy.ops.mesh.primitive_torus_add(major_radius=major, minor_radius=minor, major_segments=24, minor_segments=8, location=loc, rotation=rotation)
    o = bpy.context.object
    o.name = name
    move(o, c)
    o.data.materials.append(material)
    if parent:
        parent_keep_world(o, parent)
    return o


def radial(radius, degrees, z=4.45):
    a = math.radians(degrees)
    return Vector((radius * math.cos(a), radius * math.sin(a), z)), a


def local(base, yaw, x, y, z):
    return base + Vector((math.cos(yaw) * x - math.sin(yaw) * y, math.sin(yaw) * x + math.cos(yaw) * y, z))


def asset(asset_id, claim, family, variant, state, role, location, c):
    old = bpy.data.objects.get(asset_id)
    if old:
        bpy.data.objects.remove(old, do_unlink=True)
    e = bpy.data.objects.new(asset_id, None)
    c.objects.link(e)
    e.location = location
    for k, v in {
        "asset_id": asset_id,
        "claim_id": claim,
        "family": family,
        "variant": variant,
        "state": state,
        "semantic_role": role,
        "lod_level": 0,
        "lod_strategy": "LOD0 authored; LOD1/LOD2 pending budget pass",
        "x100_wave": WAVE,
        "truth_state": "authored_family_candidate",
    }.items():
        e[k] = v
    return e


def finish(e):
    for o in e.children_recursive:
        for k in ("asset_id", "claim_id", "family", "variant", "state", "semantic_role", "lod_level", "lod_strategy", "x100_wave", "truth_state"):
            o[k] = e[k]


def conduit(a, deg, variant, state):
    p, y = radial(39.2, deg)
    e = asset(a, CLAIM_INFRA, "service_conduit_spine", variant, state, "power/data routing outside traversal", p, SVC)
    box(a + "_FOOT", local(p, y, 0, 0, -0.15), (0.72, 0.82, 0.18), LOAD, SVC, e)
    box(a + "_SPINE", local(p, y, 0.15, 0, 1.15), (0.32, 0.42, 1.25), BLACK, SVC, e)
    for i, off in enumerate((-0.24, 0, 0.24)):
        cylinder(a + f"_PIPE_{i}", local(p, y, 0.42, off, 1.05), 0.075, 2.05, BRONZE if i != 1 else PATINA, SVC, e, 12, 0.02)
    torus(a + "_COLLAR", local(p, y, 0.15, 0, 2.15), 0.38, 0.08, BRONZE, SVC, e, (math.pi / 2, 0, 0))
    if state == "scarred":
        box(a + "_PATCH", local(p, y, 0.49, 0.20, 1.45), (0.06, 0.18, 0.28), PATINA, SVC, e, 0.02)
    finish(e)


def terminal(a, deg, variant, state):
    p, y = radial(38.7, deg)
    e = asset(a, CLAIM_INFRA, "service_terminal", variant, state, "maintenance diagnostics / memory route status", p, SVC)
    box(a + "_BASE", local(p, y, 0, 0, 0), (0.78, 0.64, 0.18), LOAD, SVC, e)
    box(a + "_PEDESTAL", local(p, y, 0.12, 0, 0.72), (0.38, 0.42, 0.72), BLACK, SVC, e)
    box(a + "_INTERFACE", local(p, y, -0.12, 0, 1.22), (0.08, 0.30, 0.34), MEMORY, SVC, e, 0.03)
    for s in (-1, 1):
        cylinder(a + f"_BRONZE_{s}", local(p, y, 0.25, s * 0.34, 0.74), 0.055, 1.1, BRONZE, SVC, e, 10, 0.02)
    finish(e)


def rail(a, deg, variant, state):
    p, y = radial(38.0, deg)
    e = asset(a, CLAIM_INFRA, "service_rail", variant, state, "edge safety / maintenance tether rail", p, SVC)
    length = {"A": 2.4, "B": 3.2, "C": 4.0}[variant]
    for yy in (-length / 2, length / 2):
        cylinder(a + f"_POST_{yy:.1f}", local(p, y, 0, yy, 0.65), 0.07, 1.3, BRONZE, SVC, e, 10, 0.02)
    box(a + "_TOP", local(p, y, 0, 0, 1.28), (0.08, length / 2, 0.08), BRONZE, SVC, e, 0.025)
    finish(e)


def valve(a, deg, variant, state):
    p, y = radial(39.0, deg)
    e = asset(a, CLAIM_INFRA, "service_valve_housing", variant, state, "pressure / route-energy isolation valve", p, SVC)
    box(a + "_BASE", local(p, y, 0, 0, 0), (0.9, 0.75, 0.22), LOAD, SVC, e)
    cylinder(a + "_DRUM", local(p, y, 0.08, 0, 0.72), 0.58, 1.05, BLACK, SVC, e, 20, 0.05, (math.pi / 2, 0, y))
    torus(a + "_HANDWHEEL", local(p, y, -0.60, 0, 0.78), 0.50, 0.075, BRONZE, SVC, e, (0, math.pi / 2, y))
    finish(e)


def beacon(a, deg, variant, state):
    p, y = radial(39.6, deg)
    e = asset(a, CLAIM_INFRA, "service_beacon", variant, state, "route-state beacon with bounded emission", p, SVC)
    box(a + "_FOOT", local(p, y, 0, 0, -0.05), (0.45, 0.45, 0.14), LOAD, SVC, e)
    cylinder(a + "_MAST", local(p, y, 0, 0, 1.0), 0.10, 2.0, BRONZE, SVC, e, 12, 0.02)
    torus(a + "_CROWN", local(p, y, 0, 0, 1.90), 0.34, 0.06, DEEP, SVC, e)
    cylinder(a + "_LIGHT", local(p, y, 0, 0, 1.90), 0.22, 0.28, SIGNAL, SVC, e, 16, 0.02)
    finish(e)


def plinth(a, deg, variant, state):
    p, y = radial(38.8, deg)
    e = asset(a, CLAIM_INFRA, "maintenance_plinth", variant, state, "service access / removable machinery plinth", p, SVC)
    box(a + "_BASE", local(p, y, 0, 0, 0), (0.85, 0.70, 0.20), LOAD, SVC, e)
    box(a + "_CAP", local(p, y, 0, 0, 0.36), (0.66, 0.52, 0.16), BLACK, SVC, e)
    finish(e)


def trunk(a, deg, variant, state):
    p, y = radial(39.4, deg)
    e = asset(a, CLAIM_INFRA, "cable_trunk", variant, state, "protected bundled memory/power trunk", p, SVC)
    box(a + "_SHELL", local(p, y, 0, 0, 0.35), (0.46, 1.05, 0.38), BLACK, SVC, e)
    for i, yy in enumerate((-0.55, 0, 0.55)):
        cylinder(a + f"_CABLE_{i}", local(p, y, -0.44, yy, 0.35), 0.07, 0.75, BRONZE if i != 1 else PATINA, SVC, e, 12, 0.02, (0, math.pi / 2, y))
    finish(e)


def seal(a, deg, variant, state):
    p, y = radial(28.2, deg)
    e = asset(a, CLAIM_CULT, "route_seal", variant, state, "non-textual route identity / faction mark", p, CULT)
    torus(a + "_RING", local(p, y, 0, 0, 0.58), 0.48, 0.10, BRONZE, CULT, e, (math.pi / 2, 0, y))
    box(a + "_SPINE", local(p, y, 0.02, 0, 0.58), (0.10, 0.50, 0.08), PATINA, CULT, e, 0.025)
    cylinder(a + "_CORE", local(p, y, 0, 0, 0.58), 0.15, 0.18, MEMORY, CULT, e, 16, 0.02, (math.pi / 2, 0, y))
    finish(e)


def reliquary(a, deg, variant, state):
    p, y = radial(28.6, deg)
    e = asset(a, CLAIM_CULT, "memory_reliquary", variant, state, "contained memory witness object", p, CULT)
    box(a + "_FOOT", local(p, y, 0, 0, 0), (0.52, 0.52, 0.18), LOAD, CULT, e)
    cylinder(a + "_VESSEL", local(p, y, 0, 0, 0.92), 0.34, 1.55, MEMORY, CULT, e, 20, 0.04)
    torus(a + "_LOWER", local(p, y, 0, 0, 0.25), 0.39, 0.06, BRONZE, CULT, e)
    torus(a + "_UPPER", local(p, y, 0, 0, 1.58), 0.39, 0.06, BRONZE, CULT, e)
    finish(e)


def votive(a, deg, variant, state):
    p, y = radial(27.8, deg)
    e = asset(a, CLAIM_CULT, "votive_marker", variant, state, "communal memory offering marker", p, CULT)
    hs = {"A": [0.22, 0.38, 0.56], "B": [0.18, 0.31, 0.47, 0.63], "C": [0.26, 0.44]}[variant]
    for i, h in enumerate(hs):
        cylinder(a + f"_TOKEN_{i}", local(p, y, 0, (i - (len(hs) - 1) / 2) * 0.26, h / 2), 0.11, h, STONE if i % 2 == 0 else PATINA, CULT, e, 12, 0.02)
    finish(e)


def stele(a, deg, variant, state):
    p, y = radial(28.8, deg)
    e = asset(a, CLAIM_CULT, "witness_stele", variant, state, "collective witness / memory provenance monument", p, CULT)
    box(a + "_STONE", local(p, y, 0, 0, 1.05), (0.30, 0.62, 1.05), STONE, CULT, e, 0.10)
    torus(a + "_TRACE", local(p, y, -0.32, 0, 1.15), 0.38, 0.045, BRONZE, CULT, e, (0, math.pi / 2, y))
    box(a + "_INSET", local(p, y, -0.31, 0, 0.72), (0.04, 0.22, 0.34), MEMORY, CULT, e, 0.02)
    finish(e)


def socket(a, deg, variant, state):
    p, y = radial(28.0, deg)
    e = asset(a, CLAIM_CULT, "ritual_socket", variant, state, "interface point for communal memory objects", p, CULT)
    cylinder(a + "_WELL", local(p, y, 0, 0, 0.18), 0.52, 0.26, BLACK, CULT, e, 20, 0.04)
    torus(a + "_LIP", local(p, y, 0, 0, 0.34), 0.58, 0.08, BRONZE, CULT, e)
    cylinder(a + "_CORE", local(p, y, 0, 0, 0.27), 0.24, 0.12, MEMORY, CULT, e, 16, 0.02)
    finish(e)


def casket(a, deg, variant, state):
    p, y = radial(28.7, deg)
    e = asset(a, CLAIM_CULT, "memory_casket", variant, state, "portable archival memory container", p, CULT)
    length = {"A": 1.15, "B": 1.45, "C": 1.75}[variant]
    box(a + "_BODY", local(p, y, 0, 0, 0.32), (0.36, length / 2, 0.32), BLACK, CULT, e, 0.10)
    box(a + "_LID", local(p, y, -0.02, 0, 0.68), (0.30, length / 2 - 0.08, 0.07), MEMORY, CULT, e, 0.035)
    finish(e)


def build():
    # angles deliberately avoid qualified bridge/aperture centerlines.
    for args in [
        ("ORG_ATR_SVC_CONDUIT_SPINE_A",15,"A","pristine"),("ORG_ATR_SVC_CONDUIT_SPINE_B",105,"B","used"),("ORG_ATR_SVC_CONDUIT_SPINE_C",225,"C","scarred")]: conduit(*args)
    for args in [("ORG_ATR_SVC_TERMINAL_A",35,"A","pristine"),("ORG_ATR_SVC_TERMINAL_B",155,"B","used"),("ORG_ATR_SVC_TERMINAL_C",275,"C","used")]: terminal(*args)
    for args in [("ORG_ATR_SVC_RAIL_A",22,"A","pristine"),("ORG_ATR_SVC_RAIL_B",142,"B","used"),("ORG_ATR_SVC_RAIL_C",262,"C","scarred")]: rail(*args)
    for args in [("ORG_ATR_SVC_VALVE_HOUSING_A",92,"A","used"),("ORG_ATR_SVC_VALVE_HOUSING_B",332,"B","scarred")]: valve(*args)
    for args in [("ORG_ATR_SVC_BEACON_A",48,"A","active"),("ORG_ATR_SVC_BEACON_B",168,"B","active"),("ORG_ATR_SVC_BEACON_C",288,"C","active")]: beacon(*args)
    for args in [("ORG_ATR_SVC_PLINTH_A",118,"A","used"),("ORG_ATR_SVC_PLINTH_B",238,"B","used")]: plinth(*args)
    for args in [("ORG_ATR_SVC_CABLE_TRUNK_A",8,"A","pristine"),("ORG_ATR_SVC_CABLE_TRUNK_B",128,"B","used"),("ORG_ATR_SVC_CABLE_TRUNK_C",248,"C","scarred")]: trunk(*args)

    for args in [("ORG_CULT_ROUTE_SEAL_A",18,"A","pristine"),("ORG_CULT_ROUTE_SEAL_B",138,"B","used"),("ORG_CULT_ROUTE_SEAL_C",258,"C","scarred")]: seal(*args)
    for args in [("ORG_CULT_MEMORY_RELIQUARY_A",42,"A","sealed"),("ORG_CULT_MEMORY_RELIQUARY_B",162,"B","used"),("ORG_CULT_MEMORY_RELIQUARY_C",282,"C","fractured-contained")]: reliquary(*args)
    for args in [("ORG_CULT_VOTIVE_MARKER_A",75,"A","recent"),("ORG_CULT_VOTIVE_MARKER_B",195,"B","layered"),("ORG_CULT_VOTIVE_MARKER_C",315,"C","weathered")]: votive(*args)
    for args in [("ORG_CULT_WITNESS_STELE_A",98,"A","used"),("ORG_CULT_WITNESS_STELE_B",218,"B","scarred")]: stele(*args)
    for args in [("ORG_CULT_RITUAL_SOCKET_A",125,"A","active"),("ORG_CULT_RITUAL_SOCKET_B",245,"B","dormant"),("ORG_CULT_RITUAL_SOCKET_C",5,"C","used")]: socket(*args)
    for args in [("ORG_CULT_MEMORY_CASKET_A",148,"A","sealed"),("ORG_CULT_MEMORY_CASKET_B",268,"B","used"),("ORG_CULT_MEMORY_CASKET_C",28,"C","scarred")]: casket(*args)

    scene = bpy.context.scene
    scene["x100_protocol_active"] = True
    scene["x100_wave"] = WAVE
    scene["x100_world"] = "ORIGIN"
    scene["navigation_geometry_frozen_from_revision"] = 3
    scene["density_rule"] = "semantic families + causal variants; no random greeble"


if __name__ == "__main__":
    build()
