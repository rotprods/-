"""UMBRA X100 habitation QA correction.

Precondition: `generate_x100_habitation_culture.py` has produced the 90-root library
and its initial 12-root refuge composition.

QA discovered `ARCH_REFUGE_HUB_BASE` is still a closed 8-vertex / 6-face blockout
volume. Therefore furniture placed inside its bounding box is not a valid visible
interior. This correction relocates the 12 habitation roots into a visible leeward
annex and constructs that annex entirely from the existing X100 architectural kit.

Checkpoint: X100_HABITATION_ANNEX_QA_FIXED_001
"""

import bpy
import math
from mathutils import Vector, Matrix

scene = bpy.context.scene
terrain = bpy.data.objects["ENV_TERRAIN_TWILIGHT_BAND_BLOCKOUT"]
site = bpy.data.collections["93_X100_REFUGE_HABITATION"]
site.name = "94_X100_REFUGE_HABITATION_ANNEX"


def terrain_z(x, y):
    inv = terrain.matrix_world.inverted()
    origin = inv @ Vector((x, y, 250.0))
    direction = (inv.to_3x3() @ Vector((0, 0, -1))).normalized()
    hit, loc, _n, _idx = terrain.ray_cast(origin, direction, distance=700.0)
    if not hit:
        raise RuntimeError(f"No terrain at {x},{y}")
    return (terrain.matrix_world @ loc).z


def descendants(root):
    out, stack = [], list(root.children)
    while stack:
        o = stack.pop()
        out.append(o)
        stack.extend(list(o.children))
    return out


def bottom_offset(root):
    zs = []
    for o in descendants(root):
        if o.type == "MESH":
            zs.extend((o.matrix_world @ Vector(c)).z for c in o.bound_box)
    return min(zs) - root.matrix_world.translation.z if zs else 0.0


def move_root(root, x, y, rz=0):
    bo = bottom_offset(root)
    root.location = (x, y, terrain_z(x, y) + 0.03 - bo)
    root.rotation_euler.z = math.radians(rz)
    root["integration_status"] = "VISIBLE_LEEWARD_HABITATION_ANNEX"
    root["placement_cause"] = "moved from invalid closed-blockout interior after QA; leeward protected annex proposal"


roots = sorted(
    [o for o in site.objects if o.type == "EMPTY" and o.name.startswith("X100HI_REFUGE_")],
    key=lambda o: o.name,
)
layout = [
    (54, 11, 0), (62, 11, 0), (54, 16, 90), (60, 16, 90),
    (82, 11, 0), (86, 16, 0), (91, 11, 90), (90, 16, 90),
    (58, 7, 0), (65, 7, 0), (82, 7, 180), (90, 7, 180),
]
for root, (x, y, rz) in zip(roots, layout):
    move_root(root, x, y, rz)


def source(family, size, variant):
    matches = [
        o for o in bpy.data.objects
        if o.type == "EMPTY"
        and o.get("family") == family
        and o.get("size_variant") == size
        and o.get("fabrication_variant") == variant
    ]
    if not matches:
        raise RuntimeError(f"Missing architectural source {family}:{size}:{variant}")
    return sorted(matches, key=lambda o: o.name)[0]


def clone_arch(src, name, x, y, rz):
    target = Matrix.Translation(
        Vector((x, y, terrain_z(x, y) + 0.03 - bottom_offset(src)))
    ) @ Matrix.Rotation(math.radians(rz), 4, "Z")
    inv = src.matrix_world.inverted()

    root = src.copy()
    root.data = None
    root.parent = None
    root.name = name
    root.matrix_world = target
    for c in list(root.users_collection):
        c.objects.unlink(root)
    site.objects.link(root)
    root["source_stable_id"] = src.get("stable_id", "")
    root["stable_id"] = name
    root["site"] = "REFUGE_HABITATION_ANNEX"
    root["temporal_layer"] = "ERA_1_MODIFICATION"
    root["site_purpose"] = "visible leeward habitation annex structure"
    root["integration_status"] = "SITE_INTEGRATED_PRODUCTION_PROPOSAL"

    for so in descendants(src):
        no = so.copy()
        no.data = so.data
        no.parent = root
        no.matrix_world = target @ inv @ so.matrix_world
        no.name = f"{name}__{so.name}"
        for c in list(no.users_collection):
            c.objects.unlink(no)
        site.objects.link(no)
    return root


structure = []
for i, x in enumerate((53, 59, 65, 80, 86, 92)):
    structure.append(clone_arch(source("GANTRY_FRAME", "L", "FIELD_MODIFIED"), f"X100HA_GANTRY_{i:02d}", x, 12, 0))
    structure.append(clone_arch(source("ACCESS_CANOPY", "L", "WIND_SHIELDED"), f"X100HA_CANOPY_{i:02d}", x, 12, 0))
for i, x in enumerate((53, 59, 65, 80, 86, 92)):
    structure.append(clone_arch(source("HANDRAIL", "L", "WIND_SHIELDED"), f"X100HA_RAIL_{i:02d}", x, 5.5, 0))
structure.append(clone_arch(source("PLATFORM", "L", "STANDARD"), "X100HA_ENTRY_DECK_00", 70.5, 17.5, 90))
structure.append(clone_arch(source("PLATFORM", "L", "STANDARD"), "X100HA_ENTRY_DECK_01", 73.5, 17.5, 90))

scene["checkpoint"] = "X100_HABITATION_ANNEX_QA_FIXED_001"
scene["x100_habitation_site_roots"] = len(roots)
scene["x100_habitation_annex_structure_roots"] = len(structure)
scene["x100_habitation_fix"] = "closed refuge blockout detected; furnishings relocated to visible leeward annex rather than hidden inside solid geometry"
scene["x100_habitation_entry_corridor"] = "x=68..76 from y=5..20 reserved from domestic prefabs; two entry decks bridge to refuge edge"
