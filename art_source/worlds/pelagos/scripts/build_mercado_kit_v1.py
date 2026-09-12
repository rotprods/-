"""PELAGOS / Mercado de Boyas modular kit v1.

Applies on top of PELAGOS-WF-001. Blender 5.2 bpy, metres.
The script represents architecture blockout engineering, not final UV/PBR/physics.
"""

import math
import bpy
from mathutils import Vector

KIT_COLLECTION = "11_MERCADO_KIT_V1"
CENTER = (-520.0, -80.0)


def get_material(name):
    m = bpy.data.materials.get(name)
    if m is None:
        raise RuntimeError(f"Required foundation material missing: {name}")
    return m


def ensure_collection(name, parent):
    c = bpy.data.collections.get(name) or bpy.data.collections.new(name)
    if c.name not in parent.children:
        parent.children.link(c)
    return c


def relink(obj, collection):
    for old in list(obj.users_collection):
        old.objects.unlink(obj)
    collection.objects.link(obj)


def tag(obj, asset_id, role, collision="none"):
    obj["asset_id"] = asset_id
    obj["world"] = "pelagos"
    obj["role"] = role
    obj["quality_tier"] = "A"
    obj["collision_intent"] = collision
    obj["production_state"] = "KIT_V1"


def set_material(obj, material):
    if hasattr(obj.data, "materials") and not obj.data.materials:
        obj.data.materials.append(material)


def box(collection, name, loc, dims, material, asset_id, role, rotation=(0, 0, 0), bevel=0.08, collision="simple"):
    bpy.ops.mesh.primitive_cube_add(location=loc, rotation=rotation)
    o = bpy.context.object
    o.name = name
    o.dimensions = dims
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if bevel:
        mod = o.modifiers.new("ManufacturedEdge", "BEVEL")
        mod.width = bevel
        mod.segments = 2
    set_material(o, material)
    relink(o, collection)
    tag(o, asset_id, role, collision)
    return o


def cylinder(collection, name, loc, radius, depth, material, asset_id, role, vertices=20, rotation=(0, 0, 0), collision="simple"):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=loc, rotation=rotation)
    o = bpy.context.object
    o.name = name
    set_material(o, material)
    relink(o, collection)
    tag(o, asset_id, role, collision)
    return o


def torus(collection, name, loc, major, minor, material, asset_id, role, rotation=(0, 0, 0)):
    bpy.ops.mesh.primitive_torus_add(major_radius=major, minor_radius=minor, major_segments=64, minor_segments=12, location=loc, rotation=rotation)
    o = bpy.context.object
    o.name = name
    set_material(o, material)
    relink(o, collection)
    tag(o, asset_id, role)
    return o


def beam(collection, name, a, b, width, thickness, material, asset_id, role, collision="simple"):
    a = Vector(a)
    b = Vector(b)
    v = b - a
    o = box(collection, name, (a + b) / 2, (width, thickness, v.length), material, asset_id, role, bevel=min(0.08, thickness * 0.25), collision=collision)
    o.rotation_euler = v.to_track_quat("Z", "Y").to_euler()
    return o


def tube(collection, name, points, radius, material, asset_id, role):
    cu = bpy.data.curves.new(name + "_CURVE", "CURVE")
    cu.dimensions = "3D"
    cu.bevel_depth = radius
    cu.bevel_resolution = 3
    cu.resolution_u = 2
    spline = cu.splines.new("POLY")
    spline.points.add(len(points) - 1)
    for p, xyz in zip(spline.points, points):
        p.co = (*xyz, 1)
    o = bpy.data.objects.new(name, cu)
    collection.objects.link(o)
    set_material(o, material)
    tag(o, asset_id, role)
    return o


def membrane(collection, name, a, b, c, material, asset_id):
    mesh = bpy.data.meshes.new(name + "_MESH")
    mesh.from_pydata([a, b, c], [], [(0, 1, 2)])
    mesh.update()
    o = bpy.data.objects.new(name, mesh)
    collection.objects.link(o)
    set_material(o, material)
    tag(o, asset_id, "canopy_membrane")
    solidify = o.modifiers.new("FabricThickness", "SOLIDIFY")
    solidify.thickness = 0.055
    return o


def build():
    root = bpy.data.collections.get("PELAGOS_WORLD")
    if root is None:
        raise RuntimeError("Run build_world_foundation.py first")

    existing = bpy.data.collections.get(KIT_COLLECTION)
    if existing:
        for obj in list(existing.objects):
            bpy.data.objects.remove(obj, do_unlink=True)
        bpy.data.collections.remove(existing)
    kit = ensure_collection(KIT_COLLECTION, root)

    ivory = get_material("PEL_Human_IvoryCeramic")
    bronze = get_material("PEL_Precursor_Bronze")
    dark = get_material("PEL_TechnicalFabric")

    cx, cy = CENTER

    # Primary platform: visible load path + distributed buoyancy.
    torus(kit, "PEL_MKT_V1_RingBeam", (cx, cy, 12.7), 37.0, 1.15, bronze, "PEL-MKT-PLAT-A", "ring_beam")
    for i in range(12):
        a = 2 * math.pi * i / 12
        end = (cx + math.cos(a) * 36, cy + math.sin(a) * 36, 12.2)
        beam(kit, f"PEL_MKT_V1_RadialBeam_{i:02d}", (cx, cy, 12.2), end, 1.0, 1.1, bronze, "PEL-MKT-PLAT-A", "radial_load_beam")
        px = cx + math.cos(a) * 32
        py = cy + math.sin(a) * 32
        cylinder(kit, f"PEL_MKT_V1_BuoyPod_{i:02d}", (px, py, 4.5), 3.2, 14.0, dark, "PEL-MKT-KEEL-001", "sealed_buoyancy_pod")
        beam(kit, f"PEL_MKT_V1_PodStrut_{i:02d}", (px, py, 11.6), (px, py, 8.2), 0.65, 0.65, bronze, "PEL-MKT-KEEL-001", "buoyancy_strut")

    # Ballast/service trunk and radial service distribution.
    cylinder(kit, "PEL_MKT_V1_CentralServiceTrunk", (cx, cy, 1.5), 7.2, 23.0, dark, "PEL-MKT-KEEL-001", "service_ballast_trunk", 24)
    torus(kit, "PEL_MKT_V1_HatchCollar", (cx, cy, 14.1), 4.2, 0.45, bronze, "PEL-MKT-UTIL-001", "service_hatch_collar")
    cylinder(kit, "PEL_MKT_V1_Hatch", (cx, cy, 14.25), 3.7, 0.35, ivory, "PEL-MKT-UTIL-001", "service_hatch", 24)
    for i in range(6):
        a = 2 * math.pi * i / 6
        p1 = (cx + math.cos(a) * 6, cy + math.sin(a) * 6, 13.7)
        p2 = (cx + math.cos(a) * 31, cy + math.sin(a) * 31, 13.7)
        beam(kit, f"PEL_MKT_V1_ServiceChannel_{i:02d}", p1, p2, 0.55, 0.18, dark, "PEL-MKT-UTIL-001", "deck_service_channel", collision="none")

    # Service riser/manifolds.
    cylinder(kit, "PEL_MKT_V1_UtilityRiser", (cx + 11, cy - 8, 20.5), 1.5, 14, bronze, "PEL-MKT-UTIL-001", "utility_riser", 16)
    for z in (16.5, 20.5, 24.5):
        torus(kit, f"PEL_MKT_V1_UtilityRiserRing_{int(z)}", (cx + 11, cy - 8, z), 2.0, 0.22, ivory, "PEL-MKT-UTIL-001", "service_manifold")
    box(kit, "PEL_MKT_V1_UtilityAccess", (cx + 11, cy - 9.35, 20), (1.25, 0.24, 3.6), ivory, "PEL-MKT-UTIL-001", "maintenance_panel", bevel=0.04, collision="none")

    # Mooring interface.
    for i in range(8):
        a = 2 * math.pi * i / 8
        box(kit, f"PEL_MKT_V1_MooringCleat_{i:02d}", (cx + math.cos(a) * 38, cy + math.sin(a) * 38, 14.35), (1.8, 0.7, 0.65), bronze, "PEL-MKT-DOCK-001", "mooring_cleat", rotation=(0, 0, a), bevel=0.12)

    # Canopy: separated compression and tension systems.
    mast_top = (cx, cy, 57)
    ring_pts = []
    for i in range(8):
        a = 2 * math.pi * i / 8
        p = (cx + math.cos(a) * 27, cy + math.sin(a) * 27, 31.5)
        ring_pts.append(p)
        beam(kit, f"PEL_MKT_V1_CanopyCompression_{i:02d}", (cx, cy, 55), p, 0.48, 0.48, bronze, "PEL-MKT-MAST-001", "canopy_compression_member", collision="none")
        tube(kit, f"PEL_MKT_V1_TensionCable_{i:02d}", [(cx, cy, 56.5), p], 0.09, bronze, "PEL-MKT-MAST-001", "tension_cable")
    for i in range(0, 8, 2):
        membrane(kit, f"PEL_MKT_V1_CanopyMembrane_{i // 2}", mast_top, ring_pts[i], ring_pts[(i + 2) % 8], dark, "PEL-MKT-MAST-001")

    # Articulated bridge. Rendering segments remain separate for future animation/physics handoff.
    a = Vector((-478, -80, 16.2))
    b = Vector((-462, -24, 16.2))
    d = b - a
    segments = 10
    for i in range(segments):
        p0 = a + d * (i / segments)
        p1 = a + d * ((i + 1) / segments)
        beam(kit, f"PEL_MKT_V1_BridgeDeck_{i:02d}", p0, p1, 5.6, 0.55, ivory, "PEL-MKT-BRIDGE-001", "bridge_deck_segment", collision="simple_walkable")
        if i < segments - 1:
            cylinder(kit, f"PEL_MKT_V1_BridgeHinge_{i:02d}", p1, 0.42, 6.0, bronze, "PEL-MKT-BRIDGE-001", "bridge_hinge", 16, rotation=(math.pi / 2, 0, 0))
    side_axis = Vector((-d.y, d.x, 0)).normalized()
    for side in (-1, 1):
        rail_points = []
        offset = side_axis * 2.45 * side
        for i in range(segments + 1):
            p = a + d * (i / segments) + offset
            rail_points.append((p.x, p.y, p.z + 1.25))
            if i % 2 == 0:
                cylinder(kit, f"PEL_MKT_V1_RailPost_{side}_{i:02d}", (p.x, p.y, p.z + 0.65), 0.08, 1.3, bronze, "PEL-MKT-BRIDGE-001", "rail_post", 10, collision="none")
        tube(kit, f"PEL_MKT_V1_Handrail_{side}", rail_points, 0.09, bronze, "PEL-MKT-BRIDGE-001", "handrail")

    # Nácar-compatible dock finger and impact fenders.
    d0 = Vector((cx - 25, cy - 30, 14.7))
    d1 = Vector((cx - 25, cy - 72, 14.7))
    beam(kit, "PEL_MKT_V1_DockSpine", d0, d1, 7.0, 0.85, ivory, "PEL-MKT-DOCK-001", "dock_deck", collision="simple_walkable")
    for i in range(5):
        t = i / 4
        p = d0 + (d1 - d0) * t
        for side in (-1, 1):
            q = p + Vector((3.7 * side, 0, 0))
            cylinder(kit, f"PEL_MKT_V1_Fender_{side}_{i}", (q.x, q.y, q.z - 1.2), 0.65, 4.5, dark, "PEL-MKT-DOCK-001", "impact_fender", 16)
    for side in (-1, 1):
        tube(kit, f"PEL_MKT_V1_DockRail_{side}", [(d0.x + 3.0 * side, d0.y, d0.z + 1.1), (d1.x + 3.0 * side, d1.y, d1.z + 1.1)], 0.09, bronze, "PEL-MKT-DOCK-001", "dock_handrail")
        cylinder(kit, f"PEL_MKT_V1_Bollard_{side}", (d1.x + 2.1 * side, d1.y + 2, d1.z + 0.7), 0.38, 1.4, bronze, "PEL-MKT-DOCK-001", "dock_bollard", 16)

    # Module specimen strip + explicit grid/pivot contract.
    base = (cx - 185, cy - 10, 20)
    box(kit, "PEL_MKT_KIT_Specimen_Deck", base, (24, 18, 0.8), ivory, "PEL-MKT-PLAT-A", "kit_specimen_deck", bevel=0.16)
    cylinder(kit, "PEL_MKT_KIT_Specimen_Buoy", (base[0] - 7, base[1], base[2] - 7), 3.2, 14, dark, "PEL-MKT-KEEL-001", "kit_specimen_buoy", 20)
    cylinder(kit, "PEL_MKT_KIT_Specimen_Riser", (base[0] + 6, base[1], base[2] + 5), 1.5, 10, bronze, "PEL-MKT-UTIL-001", "kit_specimen_riser", 16)
    bpy.ops.object.empty_add(type="PLAIN_AXES", location=base)
    meta = bpy.context.object
    meta.name = "PEL_MKT_KIT_METADATA"
    relink(meta, kit)
    meta["asset_id"] = "PEL-MKT-KIT-META"
    meta["module_grid_m"] = 2.0
    meta["snap_rotation_deg"] = 15
    meta["pivot_policy"] = "structural datum / deck center or connection face"
    meta["status"] = "KIT_V1_BLOCKOUT"

    return kit


if __name__ == "__main__":
    build()
