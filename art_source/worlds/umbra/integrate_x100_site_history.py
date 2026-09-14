"""EXOVANT 2950 / UMBRA / X100 site-history integration.

Input contract:
- UMBRA scene at or beyond X100 service/damage/architecture/micro libraries.
- Required terrain object ENV_TERRAIN_TWILIGHT_BAND_BLOCKOUT.

Purpose:
Integrate reusable X100 libraries into real UMBRA locations so ERA_0/ERA_1/ERA_2
history is visible in geometry. This script intentionally reuses linked mesh data;
it does not duplicate source mesh datablocks or invent blocked canon.

Checkpoint: X100_SITE_HISTORY_INTEGRATION_001
"""

import bpy
import math
from mathutils import Vector, Matrix

scene = bpy.context.scene
terrain = bpy.data.objects["ENV_TERRAIN_TWILIGHT_BAND_BLOCKOUT"]
root_coll = bpy.data.collections.get("W04_UMBRA")
assert root_coll

if bpy.data.collections.get("90_X100_SITE_INTEGRATION"):
    raise RuntimeError("X100 site integration already exists")

master = bpy.data.collections.new("90_X100_SITE_INTEGRATION")
root_coll.children.link(master)


def ensure_coll(name):
    c = bpy.data.collections.get(name)
    if c is None:
        c = bpy.data.collections.new(name)
        master.children.link(c)
    return c


def terrain_z(x, y):
    inv = terrain.matrix_world.inverted()
    origin = inv @ Vector((x, y, 250.0))
    direction = (inv.to_3x3() @ Vector((0, 0, -1))).normalized()
    hit, loc, _n, _idx = terrain.ray_cast(origin, direction, distance=700.0)
    if not hit:
        raise RuntimeError(f"No terrain under ({x}, {y})")
    return (terrain.matrix_world @ loc).z


def source_root(kind, family, size, variant):
    key = {
        "arch": "fabrication_variant",
        "micro": "context_variant",
        "damage": "state_variant",
    }[kind]
    matches = [
        o for o in bpy.data.objects
        if o.type == "EMPTY"
        and o.get("family") == family
        and o.get("size_variant") == size
        and o.get(key) == variant
    ]
    if not matches:
        raise RuntimeError(f"Missing source {kind}:{family}:{size}:{variant}")
    return sorted(matches, key=lambda o: o.name)[0]


def descendants(root):
    out = []
    stack = list(root.children)
    while stack:
        o = stack.pop()
        out.append(o)
        stack.extend(list(o.children))
    return out


def bottom_offset(root):
    zs = []
    for o in descendants(root):
        if o.type != "MESH":
            continue
        zs.extend((o.matrix_world @ Vector(c)).z for c in o.bound_box)
    return min(zs) - root.matrix_world.translation.z if zs else 0.0


def clone_prefab(src, dest_coll, name, x, y, rz_deg, site, era, purpose):
    # Seat every prefab to the authored terrain datum with +4 cm clearance.
    z = terrain_z(x, y) + 0.04 - bottom_offset(src)
    target = Matrix.Translation(Vector((x, y, z))) @ Matrix.Rotation(
        math.radians(rz_deg), 4, "Z"
    )
    inv_src = src.matrix_world.inverted()

    root = src.copy()
    root.data = None
    root.parent = None
    root.name = name
    root.matrix_world = target
    for c in list(root.users_collection):
        c.objects.unlink(root)
    dest_coll.objects.link(root)

    root["source_stable_id"] = src.get("stable_id", "")
    root["stable_id"] = name
    root["x100_site"] = site
    root["temporal_layer"] = era
    root["site_purpose"] = purpose
    root["integration_status"] = "SITE_INTEGRATED_PRODUCTION_PROPOSAL"

    # Flatten source hierarchy under the new root but preserve exact world-relative matrices.
    # Mesh data stays linked/shared.
    for so in descendants(src):
        no = so.copy()
        if so.data is not None:
            no.data = so.data
        no.parent = root
        no.matrix_world = target @ inv_src @ so.matrix_world
        no.name = f"{name}__{so.name}"
        for c in list(no.users_collection):
            c.objects.unlink(no)
        dest_coll.objects.link(no)
    return root


sites = {
    "REFUGE_SERVICE": ensure_coll("91_X100_SITE_REFUGE_SERVICE"),
    "REFLECTOR02": ensure_coll("91_X100_SITE_REFLECTOR02"),
    "REFLECTOR03": ensure_coll("91_X100_SITE_REFLECTOR03"),
    "M03_ARCHIVE": ensure_coll("91_X100_SITE_M03_ARCHIVE"),
    "CARAVAN_REPAIR": ensure_coll("91_X100_SITE_CARAVAN_REPAIR_HISTORY"),
}
placements = []


def add(site, kind, family, size, variant, x, y, rz, era, purpose):
    src = source_root(kind, family, size, variant)
    idx = len(placements)
    name = f"X100I_{site}_{idx:02d}_{family}_{size}_{variant}"
    root = clone_prefab(src, sites[site], name, x, y, rz, site, era, purpose)
    placements.append(root)
    return root


# REFUGE: original protected access -> field retrofit -> current repair evidence.
add("REFUGE_SERVICE", "arch", "PLATFORM", "M", "WIND_SHIELDED", 108, 31, 90, "ERA_0_ORIGINAL", "wind-protected service landing")
add("REFUGE_SERVICE", "arch", "LADDER", "M", "FIELD_MODIFIED", 112, 27, 90, "ERA_1_MODIFICATION", "retrofitted vertical maintenance access")
add("REFUGE_SERVICE", "arch", "HANDRAIL", "M", "WIND_SHIELDED", 108, 34, 90, "ERA_0_ORIGINAL", "fall protection on exposed landing")
add("REFUGE_SERVICE", "arch", "SERVICE_HATCH", "M", "FIELD_MODIFIED", 101, 27, 90, "ERA_1_MODIFICATION", "service-only crawl access")
add("REFUGE_SERVICE", "damage", "POWERBOX", "M", "DAMAGED", 116, 22, 15, "ERA_2_CURRENT", "damaged thermal/power cabinet awaiting service")
add("REFUGE_SERVICE", "micro", "REPAIR_PATCH", "M", "SERVICE_RENEWED", 103, 22, 15, "ERA_2_CURRENT", "recent structural repair evidence")
add("REFUGE_SERVICE", "micro", "CABLE_CLAMP", "M", "WINDWARD_PROTECTED", 110, 20, 15, "ERA_2_CURRENT", "wind-stabilized service route support")

# REFLECTOR 02: original access system -> field reroute -> current overload repair.
add("REFLECTOR02", "arch", "PLATFORM", "L", "WIND_SHIELDED", 187, 112, 0, "ERA_0_ORIGINAL", "reflector service landing")
add("REFLECTOR02", "arch", "LADDER", "L", "STANDARD", 182, 110, 0, "ERA_0_ORIGINAL", "mast maintenance ladder interface")
add("REFLECTOR02", "arch", "HANDRAIL", "L", "WIND_SHIELDED", 188, 117, 0, "ERA_0_ORIGINAL", "exposed platform fall protection")
add("REFLECTOR02", "arch", "CABLE_GLAND", "M", "FIELD_MODIFIED", 176, 106, 0, "ERA_1_MODIFICATION", "retrofit service penetration")
add("REFLECTOR02", "arch", "CONDUIT_JUNCTION", "M", "FIELD_MODIFIED", 179, 104, 0, "ERA_1_MODIFICATION", "field reroute for power/thermal service")
add("REFLECTOR02", "damage", "WINCH", "M", "DAMAGED", 193, 104, -18, "ERA_2_CURRENT", "overloaded tension-service winch")
add("REFLECTOR02", "micro", "WELD_SEAM", "M", "SERVICE_RENEWED", 184, 103, 0, "ERA_2_CURRENT", "recent load-transfer repair weld")
add("REFLECTOR02", "micro", "CABLE_CLAMP", "S", "WINDWARD_PROTECTED", 180, 101, 0, "ERA_2_CURRENT", "vibration/wind cable support")

# REFLECTOR 03: a different retrofit history to prevent repetition.
add("REFLECTOR03", "arch", "GANTRY_FRAME", "L", "FIELD_MODIFIED", 431, 155, 90, "ERA_1_MODIFICATION", "field-added maintenance gantry")
add("REFLECTOR03", "arch", "ACCESS_CANOPY", "M", "WIND_SHIELDED", 438, 153, 90, "ERA_1_MODIFICATION", "wind shield for service crew")
add("REFLECTOR03", "arch", "PLATFORM", "M", "FIELD_MODIFIED", 434, 160, 90, "ERA_1_MODIFICATION", "retrofitted service landing")
add("REFLECTOR03", "damage", "CABLE_REEL", "L", "ABANDONED", 425, 148, 25, "ERA_2_CURRENT", "obsolete cable reel left after reroute")
add("REFLECTOR03", "micro", "ABRASION_GUARD", "M", "WINDWARD_PROTECTED", 440, 148, 25, "ERA_2_CURRENT", "sacrificial windborne abrasion protection")
add("REFLECTOR03", "micro", "REPAIR_PATCH", "L", "STRUCTURAL", 428, 144, 25, "ERA_1_MODIFICATION", "load-transfer plate from older repair campaign")

# M03 archive: original access language plus later service modifications.
add("M03_ARCHIVE", "arch", "ACCESS_DOOR", "M", "WIND_SHIELDED", 173, 211, -8, "ERA_0_ORIGINAL", "archive human access interface")
add("M03_ARCHIVE", "arch", "SERVICE_HATCH", "S", "FIELD_MODIFIED", 177, 215, -8, "ERA_1_MODIFICATION", "later crawl-service insertion")
add("M03_ARCHIVE", "arch", "HANDRAIL", "S", "FIELD_MODIFIED", 184, 211, -8, "ERA_1_MODIFICATION", "field-added entry protection")
add("M03_ARCHIVE", "micro", "GASKET_FLANGE", "S", "SERVICE_RENEWED", 179, 208, -8, "ERA_2_CURRENT", "recent seal replacement around service interface")
add("M03_ARCHIVE", "micro", "HINGE", "S", "SERVICE_RENEWED", 181, 208, -8, "ERA_2_CURRENT", "renewed hinge hardware")
add("M03_ARCHIVE", "micro", "LATCH", "S", "STRUCTURAL", 183, 208, -8, "ERA_0_ORIGINAL", "original latch language retained")

# Caravan maintenance yard: visible succession of equipment generations.
add("CARAVAN_REPAIR", "damage", "SERVICE_STAND", "M", "DAMAGED", -8, -164, 8, "ERA_2_CURRENT", "collapsed/overstressed repair stand")
add("CARAVAN_REPAIR", "damage", "CABLE_REEL", "M", "ABANDONED", 5, -170, 8, "ERA_2_CURRENT", "disconnected old cable spool")
add("CARAVAN_REPAIR", "micro", "REPAIR_PATCH", "M", "SERVICE_RENEWED", 18, -170, 8, "ERA_2_CURRENT", "fresh repair plates near active maintenance route")
add("CARAVAN_REPAIR", "arch", "GANTRY_FRAME", "M", "FIELD_MODIFIED", 30, -166, 8, "ERA_1_MODIFICATION", "improvised caravan maintenance gantry")

scene["checkpoint"] = "X100_SITE_HISTORY_INTEGRATION_001"
scene["x100_site_integration_clusters"] = len(sites)
scene["x100_site_integrated_prefabs"] = len(placements)
scene["x100_world_history"] = "ERA_0 original structure | ERA_1 field modification | ERA_2 current damage/repair"
scene["x100_site_integration_rule"] = "purposeful placement only; linked mesh data; terrain seated; avoid primary traversal centers"

bpy.context.view_layer.update()
