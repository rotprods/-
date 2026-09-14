"""Build Nácar-2 engineering blockout on top of the Pelagos foundation.

Blender 5.2+, metres. The generator intentionally leaves energy storage,
pressure certification and runtime hydrodynamics unresolved rather than inventing them.
"""
import math
import bpy
from mathutils import Vector

COLLECTION = "81_NACAR2_ENGINEERING_V1"
ORIGIN = Vector((-250.0, -360.0, 16.0))
AID = "PEL-VEH-NACAR2"


def material(name):
    m = bpy.data.materials.get(name)
    if not m:
        raise RuntimeError(f"Missing foundation material {name}")
    return m


def local_material(name, color, metallic=0.0, roughness=0.5):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = color
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = roughness
    return m


def ensure_collection():
    root = bpy.data.collections.get("PELAGOS_WORLD")
    if root is None:
        raise RuntimeError("Build Pelagos world foundation first")
    old = bpy.data.collections.get(COLLECTION)
    if old:
        for obj in list(old.objects):
            bpy.data.objects.remove(obj, do_unlink=True)
        bpy.data.collections.remove(old)
    col = bpy.data.collections.new(COLLECTION)
    root.children.link(col)
    return col


def tag(obj, role, collision="none"):
    obj["asset_id"] = AID if not role.startswith("collision_proxy") else "PEL-VEH-NACAR2-COL"
    obj["world"] = "pelagos"
    obj["role"] = role
    obj["quality_tier"] = "S"
    obj["collision_intent"] = collision
    obj["production_state"] = "ENGINEERING_BLOCKOUT_V1"
    return obj


def set_material(obj, mat):
    if hasattr(obj.data, "materials") and not obj.data.materials:
        obj.data.materials.append(mat)


def relink(obj, col):
    for old in list(obj.users_collection):
        old.objects.unlink(obj)
    col.objects.link(obj)


def box(col, name, loc, dims, mat, role, rotation=(0, 0, 0), bevel=0.08, collision="simple"):
    bpy.ops.mesh.primitive_cube_add(location=loc, rotation=rotation)
    o = bpy.context.object
    o.name = name
    o.dimensions = dims
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if bevel:
        mod = o.modifiers.new("ManufacturedEdge", "BEVEL")
        mod.width = bevel
        mod.segments = 2
    set_material(o, mat)
    relink(o, col)
    return tag(o, role, collision)


def cylinder(col, name, loc, radius, depth, mat, role, vertices=32, rotation=(0, 0, 0), collision="simple"):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=loc, rotation=rotation)
    o = bpy.context.object
    o.name = name
    set_material(o, mat)
    relink(o, col)
    return tag(o, role, collision)


def sphere(col, name, loc, scale, mat, role, collision="none"):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, location=loc)
    o = bpy.context.object
    o.name = name
    o.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    set_material(o, mat)
    relink(o, col)
    return tag(o, role, collision)


def torus(col, name, loc, major, minor, mat, role, rotation=(0, 0, 0)):
    bpy.ops.mesh.primitive_torus_add(major_radius=major, minor_radius=minor, major_segments=48, minor_segments=12, location=loc, rotation=rotation)
    o = bpy.context.object
    o.name = name
    set_material(o, mat)
    relink(o, col)
    return tag(o, role)


def curve(col, name, points, radius, mat, role):
    cu = bpy.data.curves.new(name + "_CURVE", "CURVE")
    cu.dimensions = "3D"
    cu.bevel_depth = radius
    cu.bevel_resolution = 2
    sp = cu.splines.new("POLY")
    sp.points.add(len(points) - 1)
    for p, xyz in zip(sp.points, points):
        p.co = (*xyz, 1)
    o = bpy.data.objects.new(name, cu)
    col.objects.link(o)
    set_material(o, mat)
    return tag(o, role)


def empty(col, name, loc, role):
    o = bpy.data.objects.new(name, None)
    col.objects.link(o)
    o.location = loc
    return tag(o, role)


def parent_keep_world(child, parent):
    """Parent without moving the child in world space."""
    world = child.matrix_world.copy()
    child.parent = parent
    child.matrix_parent_inverse = parent.matrix_world.inverted()
    child.matrix_world = world


def bounds(col, role_exclusions=()):
    bpy.context.view_layer.update()
    meshes = [o for o in col.objects if o.type == "MESH" and not o.hide_render and not str(o.get("role", "")).startswith("collision_proxy") and o.get("role") not in role_exclusions]
    mn = Vector((1e9, 1e9, 1e9))
    mx = Vector((-1e9, -1e9, -1e9))
    for o in meshes:
        for corner in o.bound_box:
            p = o.matrix_world @ Vector(corner)
            mn = Vector((min(mn.x, p.x), min(mn.y, p.y), min(mn.z, p.z)))
            mx = Vector((max(mx.x, p.x), max(mx.y, p.y), max(mx.z, p.z)))
    return mx - mn


def build():
    col = ensure_collection()
    ivory = material("PEL_Human_IvoryCeramic")
    bronze = material("PEL_Precursor_Bronze")
    dark = material("PEL_TechnicalFabric")
    glass = material("PEL_GlassProxy")
    cyan = material("PEL_Memory_Cyan")
    amber = material("PEL_Refuge_Amber")
    structural = local_material("PEL_Nacar_StructuralMetal", (0.12, 0.16, 0.17, 1), 0.7, 0.32)
    interior = local_material("PEL_Nacar_Interior", (0.08, 0.09, 0.085, 1), 0.15, 0.56)
    collision_mat = local_material("PEL_Collision_Debug", (0.12, 0.03, 0.15, 1), 0.0, 0.85)

    x, y, z = ORIGIN
    cylinder(col, "PEL_N2_PressureHull", (x, y, z), 2.35, 9.4, structural, "pressure_hull", 48, (0, math.pi / 2, 0), "render")
    sphere(col, "PEL_N2_NoseFairing", (x + 5.3, y, z), (2.8, 2.45, 2.25), ivory, "hydrodynamic_nose")
    sphere(col, "PEL_N2_SternFairing", (x - 5.25, y, z), (2.3, 2.15, 2.05), ivory, "stern_fairing")
    for off in (-3.8, -1.9, 0, 1.9, 3.8):
        torus(col, f"PEL_N2_FrameRing_{off}", (x + off, y, z), 2.42, 0.13, bronze, "pressure_frame", (0, math.pi / 2, 0))
    sphere(col, "PEL_N2_CanopyWindow", (x + 1.4, y, z + 2.15), (3.1, 1.75, 1.1), glass, "pressure_canopy")
    torus(col, "PEL_N2_CanopyRim", (x + 1.4, y - 1.5, z + 2.0), 1.7, 0.16, bronze, "canopy_frame", (math.pi / 2, 0, 0))

    for idx, xoff in enumerate((1.55, -0.1)):
        box(col, f"PEL_N2_SeatBase_{idx}", (x + xoff, y, z + 0.05), (1.0, 1.0, 0.3), interior, "cockpit_seat", bevel=0.12, collision="none")
        box(col, f"PEL_N2_SeatBack_{idx}", (x + xoff - 0.35, y, z + 0.9), (0.3, 1.0, 1.55), interior, "cockpit_seat_back", (0, math.radians(-8), 0), 0.12, "none")
    box(col, "PEL_N2_ControlConsole", (x + 3.25, y, z + 0.9), (0.5, 2.0, 1.2), ivory, "control_console", (0, math.radians(-12), 0), 0.12, "none")

    hatch_pivot = empty(col, "PEL_N2_HatchHinge", (x - 0.9, y, z + 2.5), "hatch_hinge")
    hatch = cylinder(col, "PEL_N2_AccessHatch", (x, y, z + 2.52), 0.72, 0.18, ivory, "access_hatch", 32)
    parent_keep_world(hatch, hatch_pivot)
    hatch["clear_diameter_m"] = 1.25
    hatch_pivot["intended_range_deg"] = [0, 105]
    for side in (-1.0, 1.0):
        curve(col, f"PEL_N2_Handhold_{side}", [(x - 0.15, y + side, z + 1.8), (x - 0.15, y + side, z + 2.7)], 0.06, bronze, "access_handhold")

    box(col, "PEL_N2_ServiceBay", (x - 3.55, y, z), (2.2, 3.5, 3.0), interior, "service_bay", bevel=0.18, collision="none")
    for side in (-1, 1):
        box(col, f"PEL_N2_ServicePanel_{side}", (x - 3.55, y + side * 1.8, z), (1.7, 0.12, 1.8), ivory, "removable_service_panel", bevel=0.08, collision="none")
    box(col, "PEL_N2_CargoBay", (x - 1.8, y, z - 0.65), (2.6, 2.6, 1.4), interior, "cargo_bay", bevel=0.1, collision="none")

    for side in (-1, 1):
        yy = y + side * 2.65
        pivot = empty(col, f"PEL_N2_ThrusterPivot_{side}", (x - 4.9, yy, z), "thruster_gimbal_pivot")
        parts = [
            cylinder(col, f"PEL_N2_ThrusterDuct_{side}", (x - 5.35, yy, z), 1.05, 1.5, structural, "thruster_duct", 32, (0, math.pi / 2, 0)),
            torus(col, f"PEL_N2_ThrusterGuard_{side}", (x - 6.12, yy, z), 1.05, 0.12, bronze, "thruster_guard", (0, math.pi / 2, 0)),
            cylinder(col, f"PEL_N2_ThrusterHub_{side}", (x - 5.4, yy, z), 0.22, 1.0, bronze, "thruster_hub", 20, (0, math.pi / 2, 0), "none"),
        ]
        for blade in range(4):
            a = blade * math.pi / 2
            parts.append(box(col, f"PEL_N2_PropBlade_{side}_{blade}", (x - 5.85, yy + math.cos(a) * 0.45, z + math.sin(a) * 0.45), (0.16, 0.7, 0.22), bronze, "thruster_blade", (a, 0, 0), 0.04, "none"))
        for part in parts:
            parent_keep_world(part, pivot)
        pivot["gimbal_range_deg"] = [-12, 12]

    for side in (-1, 1):
        pivot = empty(col, f"PEL_N2_LateralFinPivot_{side}", (x - 1.7, y + side * 3.1, z), "control_surface_hinge")
        fin = box(col, f"PEL_N2_LateralFin_{side}", (x - 1.7, y + side * 4.25, z), (3.0, 2.3, 0.22), bronze, "lateral_control_surface", bevel=0.14, collision="none")
        parent_keep_world(fin, pivot)
        pivot["range_deg"] = [-22, 22]
    v_pivot = empty(col, "PEL_N2_VerticalFinPivot", (x - 4.0, y, z + 2.0), "control_surface_hinge")
    fin = box(col, "PEL_N2_VerticalFin", (x - 4.3, y, z + 3.4), (3.4, 0.22, 2.8), bronze, "vertical_control_surface", bevel=0.14, collision="none")
    parent_keep_world(fin, v_pivot)
    v_pivot["range_deg"] = [-18, 18]

    torus(col, "PEL_N2_HydrophoneRing", (x + 4.55, y, z), 2.0, 0.16, cyan, "hydrophone_array", (0, math.pi / 2, 0))
    sphere(col, "PEL_N2_SonarDome", (x + 7.0, y, z), (1.0, 1.15, 1.0), cyan, "sonar_dome")
    for side in (-1, 1):
        sphere(col, f"PEL_N2_NavLight_{side}", (x + 1.2, y + side * 2.42, z + 1.3), (0.18, 0.18, 0.18), amber, "navigation_light")
    for xoff in (-2.5, 2.7):
        torus(col, f"PEL_N2_DockHardpoint_{xoff}", (x + xoff, y - 2.45, z), 0.35, 0.08, bronze, "dock_hardpoint", (math.pi / 2, 0, 0))
    for i in range(5):
        cylinder(col, f"PEL_N2_EqualizationPort_{i}", (x - 2.0 + i, y + 2.42, z - 0.6), 0.12, 0.2, dark, "equalization_port", 12, (math.pi / 2, 0, 0), "none")

    proxy = box(col, "PEL_N2_COLLISION_MainHull", (x, y, z), (11.2, 5.0, 4.8), collision_mat, "collision_proxy_main", bevel=0.6, collision="primitive_proxy")
    proxy.hide_render = True
    proxy.display_type = "WIRE"
    for side in (-1, 1):
        proxy = box(col, f"PEL_N2_COLLISION_Thruster_{side}", (x - 5.35, y + side * 2.65, z), (1.8, 2.3, 2.3), collision_mat, "collision_proxy_thruster", bevel=0.25, collision="primitive_proxy")
        proxy.hide_render = True
        proxy.display_type = "WIRE"

    meta = empty(col, "PEL_N2_METADATA", ORIGIN, "vehicle_metadata")
    cruise = bounds(col)
    dock = bounds(col, {"lateral_control_surface", "vertical_control_surface"})
    meta["dimensions_status"] = "PROPOSAL_MEASURED_BLOCKOUT"
    meta["overall_cruise_length_m"] = round(cruise.x, 3)
    meta["overall_cruise_beam_m"] = round(cruise.y, 3)
    meta["overall_cruise_height_m"] = round(cruise.z, 3)
    meta["rigid_docking_length_m"] = round(dock.x, 3)
    meta["rigid_docking_beam_m"] = round(dock.y, 3)
    meta["rigid_docking_height_m"] = round(dock.z, 3)
    meta["crew_capacity"] = 2
    meta["solo_operation"] = "CANON"
    meta["energy_storage"] = "UNKNOWN_NOT_MODELED"
    meta["pressure_rating"] = "UNKNOWN"
    meta["water_physics"] = "BLOCKED_RUNTIME_INTERFACE"
    meta["docking_configuration"] = "fold/neutralize control surfaces at berth"
    return col


if __name__ == "__main__":
    build()
