"""Build Nácar-2 semantic LOD1/LOD2 foundations.

Blender 5.2+, metres. Requires PEL-VEH-NACAR2 engineering blockout.
Important: source parts are rotated; derive proxy dimensions from evaluated world-space AABBs,
not local object.dimensions, to avoid longitudinal/vertical axis reinterpretation.
Runtime switching thresholds stay UNKNOWN until the production engine/camera profile is qualified.
"""
import bpy
import math
from mathutils import Vector

ROOT = "PELAGOS_WORLD"
GROUP = "82_NACAR2_LOD_V1"
SOURCE = "PEL-VEH-NACAR2"
COLLISION = "PEL-VEH-NACAR2-COL"
LOD1 = "PEL-VEH-NACAR2-LOD1"
LOD2 = "PEL-VEH-NACAR2-LOD2"


def material(*names):
    for name in names:
        mat = bpy.data.materials.get(name)
        if mat:
            return mat
    return None


def set_material(obj, mat):
    if mat and hasattr(obj.data, "materials") and not obj.data.materials:
        obj.data.materials.append(mat)


def world_bbox(obj):
    points = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
    mn = Vector((min(p.x for p in points), min(p.y for p in points), min(p.z for p in points)))
    mx = Vector((max(p.x for p in points), max(p.y for p in points), max(p.z for p in points)))
    return mn, mx, mx - mn


def ensure_collections():
    root = bpy.data.collections.get(ROOT)
    if root is None:
        raise RuntimeError("Build Pelagos World Foundation first")
    old = bpy.data.collections.get(GROUP)
    if old:
        for child in list(old.children):
            for obj in list(child.objects):
                bpy.data.objects.remove(obj, do_unlink=True)
            bpy.data.collections.remove(child)
        for obj in list(old.objects):
            bpy.data.objects.remove(obj, do_unlink=True)
        bpy.data.collections.remove(old)
    group = bpy.data.collections.new(GROUP)
    root.children.link(group)
    lod1 = bpy.data.collections.new("NACAR2_LOD1_SEMANTIC")
    lod2 = bpy.data.collections.new("NACAR2_LOD2_PROXY")
    meta = bpy.data.collections.new("NACAR2_LOD_METADATA")
    group.children.link(lod1)
    group.children.link(lod2)
    group.children.link(meta)
    return lod1, lod2, meta


def tag(obj, aid, role, lod):
    obj["asset_id"] = aid
    obj["source_asset_id"] = SOURCE
    obj["world"] = "pelagos"
    obj["role"] = role
    obj["lod"] = lod
    obj["production_state"] = "LOD_FOUNDATION_V1"
    obj["collision_intent"] = "none"
    return obj


def source_objects():
    return [
        obj
        for obj in bpy.data.objects
        if str(obj.get("asset_id", "")) == SOURCE
        and str(obj.get("production_state", "")) == "ENGINEERING_BLOCKOUT_V1"
        and not obj.name.startswith("PEL_VEH_Nacar2_")
    ]


def group_roles(objects):
    result = {}
    for obj in objects:
        result.setdefault(str(obj.get("role", "")), []).append(obj)
    return result


def linked_lod1(src, collection):
    obj = src.copy()
    obj.data = src.data
    obj.name = "LOD1_" + src.name
    collection.objects.link(obj)
    obj.matrix_world = src.matrix_world.copy()
    obj.hide_render = True
    return tag(obj, LOD1, "lod_visual_part", 1)


def move_to(obj, collection):
    for old in list(obj.users_collection):
        old.objects.unlink(obj)
    collection.objects.link(obj)
    return obj


def low_sphere(collection, name, loc, dims, mat, role):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=6, location=loc)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = dims
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    move_to(obj, collection)
    set_material(obj, mat)
    obj.hide_render = True
    return tag(obj, LOD2, role, 2)


def low_box(collection, name, loc, dims, mat, role, matrix=None):
    bpy.ops.mesh.primitive_cube_add(location=loc)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = dims
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if matrix is not None:
        obj.rotation_euler = matrix.to_euler()
    move_to(obj, collection)
    set_material(obj, mat)
    obj.hide_render = True
    return tag(obj, LOD2, role, 2)


def low_cylinder(collection, name, loc, radius, depth, mat, role):
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=12,
        radius=radius,
        depth=depth,
        location=loc,
        rotation=(0, math.pi / 2, 0),
    )
    obj = bpy.context.object
    obj.name = name
    move_to(obj, collection)
    set_material(obj, mat)
    obj.hide_render = True
    return tag(obj, LOD2, role, 2)


def low_torus(collection, name, loc, major, minor, mat, role, major_segments=12, minor_segments=4):
    bpy.ops.mesh.primitive_torus_add(
        major_radius=major,
        minor_radius=minor,
        major_segments=major_segments,
        minor_segments=minor_segments,
        location=loc,
        rotation=(0, math.pi / 2, 0),
    )
    obj = bpy.context.object
    obj.name = name
    move_to(obj, collection)
    set_material(obj, mat)
    obj.hide_render = True
    return tag(obj, LOD2, role, 2)


def tris(objects):
    return sum(
        sum(max(0, len(poly.vertices) - 2) for poly in obj.data.polygons)
        for obj in objects
        if obj.type == "MESH"
    )


def build():
    lod1_col, lod2_col, meta_col = ensure_collections()
    source = source_objects()
    by = group_roles(source)
    ivory = material("PEL_MAT_IvoryCeramic_Marine", "PEL_Human_IvoryCeramic")
    bronze = material("PEL_MAT_Bronze_Oxidized_Marine", "PEL_Precursor_Bronze")
    dark = material("PEL_MAT_DarkTechnicalComposite", "PEL_TechnicalFabric")
    glass = material("PEL_GlassProxy")
    memory = material("PEL_MAT_MemoryCyan_Biolum", "PEL_Memory_Cyan")
    amber = material("PEL_Refuge_Amber")

    # LOD1 keeps exterior identity but drops cockpit/service/cargo micro-detail.
    keep_roles = [
        "pressure_hull", "hydrodynamic_nose", "stern_fairing", "pressure_canopy",
        "canopy_frame", "access_hatch", "lateral_control_surface",
        "vertical_control_surface", "thruster_duct", "thruster_hub",
        "thruster_blade", "sonar_dome",
    ]
    lod1 = []
    for role in keep_roles:
        for src in by.get(role, []):
            if src.type in {"MESH", "CURVE"}:
                lod1.append(linked_lod1(src, lod1_col))

    # Cheap semantic replacements for expensive ring/guard/light features.
    hyd = by.get("hydrophone_array", [])
    if hyd:
        src = hyd[0]
        obj = low_torus(lod2_col, "TMP_L1_Hydrophone", src.matrix_world.translation,
                        max(src.dimensions.y, src.dimensions.z) * 0.42, 0.10, memory,
                        "lod1_hydrophone", 16, 6)
        move_to(obj, lod1_col); obj["asset_id"] = LOD1; obj["lod"] = 1
    for index, src in enumerate(by.get("thruster_guard", [])):
        obj = low_torus(lod2_col, f"TMP_L1_ThrusterGuard_{index}", src.matrix_world.translation,
                        max(src.dimensions.y, src.dimensions.z) * 0.42, 0.08, bronze,
                        "lod1_thruster_guard", 16, 5)
        move_to(obj, lod1_col); obj["asset_id"] = LOD1; obj["lod"] = 1
    for index, src in enumerate(sorted(by.get("pressure_frame", []), key=lambda o: o.name)[::4]):
        obj = low_torus(lod2_col, f"TMP_L1_Frame_{index}", src.matrix_world.translation,
                        max(src.dimensions.y, src.dimensions.z) * 0.45, 0.08, bronze,
                        "lod1_pressure_frame", 16, 5)
        move_to(obj, lod1_col); obj["asset_id"] = LOD1; obj["lod"] = 1
    for index, src in enumerate(by.get("navigation_light", [])):
        obj = low_sphere(lod2_col, f"TMP_L1_NavLight_{index}", src.matrix_world.translation,
                         (0.16, 0.16, 0.16), amber, "lod1_navigation_light")
        move_to(obj, lod1_col); obj["asset_id"] = LOD1; obj["lod"] = 1

    # LOD2 uses evaluated world AABBs where source local axes are rotated.
    for role, label, mat in (
        ("pressure_hull", "Hull", dark),
        ("hydrodynamic_nose", "Nose", ivory),
        ("stern_fairing", "Stern", ivory),
        ("pressure_canopy", "Canopy", glass),
        ("sonar_dome", "Sonar", memory),
    ):
        items = by.get(role, [])
        if not items:
            continue
        src = items[0]
        mn, mx, size = world_bbox(src)
        low_sphere(lod2_col, "LOD2_N2_" + label, (mn + mx) / 2,
                   tuple(float(v) for v in size), mat, "lod2_" + role)

    for role in ("lateral_control_surface", "vertical_control_surface"):
        for index, src in enumerate(by.get(role, [])):
            obj = low_box(lod2_col, f"LOD2_N2_{role}_{index}", src.matrix_world.translation,
                          tuple(float(v) for v in src.dimensions), bronze, "lod2_" + role,
                          src.matrix_world)

    for index, src in enumerate(by.get("thruster_duct", [])):
        mn, mx, size = world_bbox(src)
        low_cylinder(lod2_col, f"LOD2_N2_Thruster_{index}", (mn + mx) / 2,
                     max(size.y, size.z) * 0.5, size.x, dark, "lod2_thruster_duct")
    for index, src in enumerate(by.get("thruster_guard", [])):
        mn, mx, size = world_bbox(src)
        low_torus(lod2_col, f"LOD2_N2_Guard_{index}", (mn + mx) / 2,
                  max(size.y, size.z) * 0.42, 0.07, bronze, "lod2_thruster_guard")
    if hyd:
        mn, mx, size = world_bbox(hyd[0])
        low_torus(lod2_col, "LOD2_N2_Hydrophone", (mn + mx) / 2,
                  max(size.y, size.z) * 0.42, 0.08, memory, "lod2_hydrophone")

    meta = bpy.data.objects.new("PEL_NACAR2_LOD_METADATA", None)
    meta_col.objects.link(meta)
    tag(meta, "PEL-VEH-NACAR2-LODSET", "lod_metadata", "SET")
    meta["source_asset_id"] = SOURCE
    meta["lod1_asset_id"] = LOD1
    meta["lod2_asset_id"] = LOD2
    meta["switch_thresholds"] = "UNKNOWN_PENDING_ENGINE_CAMERA_PROFILE"
    meta["selection_metric"] = "ENGINE_SCREEN_SIZE_OR_DISTANCE_TO_BE_QUALIFIED"
    meta["collision_policy"] = (
        "SHARE PEL-VEH-NACAR2-COL collision family; visual LOD does not alter vehicle physics collision"
    )
    meta["axis_rule"] = "derive proxy dimensions from source evaluated world AABB for rotated parts"
    meta["engine_state"] = "NOT_IMPORTED_NOT_SWITCHED"

    lod0 = [
        obj for obj in source
        if obj.type == "MESH" and not str(obj.get("role", "")).startswith("collision_proxy")
    ]
    return {
        "checkpoint": "PELAGOS-NACAR2-LOD-002",
        "lod0_tris_est": tris(lod0),
        "lod1_tris_est": tris(list(lod1_col.objects)),
        "lod2_tris_est": tris(list(lod2_col.objects)),
        "collision_family": COLLISION,
        "switch_thresholds": "PENDING_ENGINE",
        "pending": ["runtime switching", "water physics", "engine collision", "performance", "human art review"],
    }


if __name__ == "__main__":
    result = build()
    print(result)
