"""ELYSIUM NULL — EDEN state-graph stage.

Precondition: foundation scene with `EDEN_ARENA_48M_CANON`, W0 EDEN garden modules
and material roles. This script adds three reversible candidate layouts and a visible
State-B relocation footprint. 48 m arena + 1.5 s Reubicación telegraph are canon;
8 m module footprints and 6 m minimum corridor are proposals.
"""

import bpy
import json
import math

scene = bpy.context.scene


def collection(name):
    c = bpy.data.collections.get(name) or bpy.data.collections.new(name)
    if scene.collection.children.get(c.name) is None:
        scene.collection.children.link(c)
    return c


COL = collection("70_EDEN_STATE_GRAPH")
AMBER = bpy.data.materials["MAT_Elysium_ServiceAmber_PROPOSAL"]
DARK = bpy.data.materials["MAT_Elysium_Recess_PROPOSAL"]
CENTER = (0.0, 108.0)
STATE_A = [(-10, 101), (10, 101), (-10, 115), (10, 115)]
STATE_B = [(-14, 101), (14, 101), (-14, 115), (14, 115)]
STATE_C = [(-10, 97), (10, 97), (-10, 119), (10, 119)]


def move_to(obj):
    for old in list(obj.users_collection):
        old.objects.unlink(obj)
    COL.objects.link(obj)


def box(name, location, dimensions, material, bevel=0.0):
    bpy.ops.mesh.primitive_cube_add(location=location)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = dimensions
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.data.materials.append(material)
    move_to(obj)
    if bevel:
        mod = obj.modifiers.new("Bevel_physical", "BEVEL")
        mod.width = bevel
        mod.segments = 3
    return obj


def max_corner_radius(state):
    values = []
    for x, y in state:
        for dx in (-4, 4):
            for dy in (-4, 4):
                values.append(math.hypot(x + dx - CENTER[0], y + dy - CENTER[1]))
    return max(values)


def corridors(state):
    xs = sorted(set(x for x, _ in state))
    ys = sorted(set(y for _, y in state))
    vertical = (xs[1] - 4) - (xs[0] + 4)
    horizontal = (ys[1] - 4) - (ys[0] + 4)
    return vertical, horizontal


checks = {}
for key, state in (("A", STATE_A), ("B", STATE_B), ("C", STATE_C)):
    vertical, horizontal = corridors(state)
    radius = max_corner_radius(state)
    checks[key] = {
        "max_corner_radius_m": round(radius, 3),
        "within_24m_radius": radius <= 24.0,
        "central_vertical_corridor_m": round(vertical, 3),
        "central_horizontal_corridor_m": round(horizontal, 3),
        "min_axis_corridor_m": round(min(vertical, horizontal), 3),
    }

bpy.ops.object.empty_add(type="PLAIN_AXES", location=(0, 108, 0))
root = bpy.context.object
root.name = "META_EDEN_STATE_GRAPH_V1"
move_to(root)
root["status"] = "PROPOSAL"
root["arena_diameter_m_CANON"] = 48.0
root["module_footprint_m"] = "8x8"
root["relocation_telegraph_s_CANON"] = 1.5
root["proposed_min_axis_corridor_m"] = min(item["min_axis_corridor_m"] for item in checks.values())
root["state_A"] = json.dumps(STATE_A)
root["state_B"] = json.dumps(STATE_B)
root["state_C"] = json.dumps(STATE_C)
root["validation"] = json.dumps(checks, sort_keys=True)

for key, state in (("A", STATE_A), ("B", STATE_B), ("C", STATE_C)):
    for index, (x, y) in enumerate(state):
        bpy.ops.object.empty_add(type="CUBE", location=(x, y, 1.0))
        target = bpy.context.object
        target.name = f"EDEN_STATE_{key}_TARGET_{index:02d}"
        target.empty_display_size = 1.5
        target["state"] = key
        target["module_index"] = index
        target["target_xy_m"] = f"{x},{y}"
        move_to(target)

# State-B visible target footprints for the canonical relocation warning.
for index, (x, y) in enumerate(STATE_B):
    z = 0.72
    t = 0.12
    box(f"EDEN_RELOC_B_{index:02d}_N", (x, y + 4, z), (8, t, 0.10), AMBER, 0.02)
    box(f"EDEN_RELOC_B_{index:02d}_S", (x, y - 4, z), (8, t, 0.10), AMBER, 0.02)
    box(f"EDEN_RELOC_B_{index:02d}_E", (x + 4, y, z), (t, 8, 0.10), AMBER, 0.02)
    box(f"EDEN_RELOC_B_{index:02d}_W", (x - 4, y, z), (t, 8, 0.10), AMBER, 0.02)

# Debug-only central clearance guides. Final art must not depend on them.
box("EDEN_DEBUG_CORRIDOR_NS", (0, 108, 0.68), (5.8, 40, 0.06), DARK)
box("EDEN_DEBUG_CORRIDOR_EW", (0, 108, 0.69), (40, 5.8, 0.06), DARK)

print({
    "arena_diameter_m_CANON": 48.0,
    "relocation_telegraph_s_CANON": 1.5,
    "states": {"A": STATE_A, "B": STATE_B, "C": STATE_C},
    "checks": checks,
    "proposed_min_axis_corridor_m": min(item["min_axis_corridor_m"] for item in checks.values()),
})
