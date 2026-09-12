"""Build engine-agnostic THALASSA semantic LOD foundations.

Requires PEL-BOSS-THALASSA hero foundation. Blender 5.2+, metres.
LOD1 is a linked-data semantic subset of the authored hero model. LOD2 is a low-poly
silhouette reconstruction. Runtime switch thresholds are intentionally UNKNOWN until the
production engine/camera profile is qualified. Visual LOD never changes gameplay collision.
"""
import bpy
import math
from mathutils import Vector

ROOT = "PELAGOS_WORLD"
COLLECTION = "42_THALASSA_LOD_V1"
SOURCE_ID = "PEL-BOSS-THALASSA"
LOD1_ID = "PEL-BOSS-THALASSA-LOD1"
LOD2_ID = "PEL-BOSS-THALASSA-LOD2"


def ensure_collections():
    root = bpy.data.collections.get(ROOT)
    if root is None:
        raise RuntimeError("Build Pelagos World Foundation first")
    old = bpy.data.collections.get(COLLECTION)
    if old:
        for child in list(old.children):
            for obj in list(child.objects):
                bpy.data.objects.remove(obj, do_unlink=True)
            bpy.data.collections.remove(child)
        for obj in list(old.objects):
            bpy.data.objects.remove(obj, do_unlink=True)
        bpy.data.collections.remove(old)
    group = bpy.data.collections.new(COLLECTION)
    root.children.link(group)
    lod1 = bpy.data.collections.new("THALASSA_LOD1_SEMANTIC")
    lod2 = bpy.data.collections.new("THALASSA_LOD2_PROXY")
    meta = bpy.data.collections.new("THALASSA_LOD_METADATA")
    group.children.link(lod1)
    group.children.link(lod2)
    group.children.link(meta)
    return group, lod1, lod2, meta


def tag(obj, aid, role, lod):
    obj["asset_id"] = aid
    obj["source_asset_id"] = SOURCE_ID
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
        if str(obj.get("asset_id", "")) == SOURCE_ID
        and not str(obj.get("production_state", "")).startswith("SUPERSEDED")
    ]


def roles(objects):
    result = {}
    for obj in objects:
        result.setdefault(str(obj.get("role", "")), []).append(obj)
    return result


def linked_copy(src, name, collection):
    obj = src.copy()
    obj.data = src.data
    obj.name = name
    collection.objects.link(obj)
    obj.matrix_world = src.matrix_world.copy()
    obj.hide_render = True
    obj.hide_viewport = False
    return tag(obj, LOD1_ID, "lod_visual_part", 1)


def material(*names):
    for name in names:
        mat = bpy.data.materials.get(name)
        if mat:
            return mat
    return None


def set_material(obj, mat):
    if mat and hasattr(obj.data, "materials") and not obj.data.materials:
        obj.data.materials.append(mat)


def low_sphere(collection, name, loc, dims, mat, role):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=6, location=loc)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = dims
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    for old in list(obj.users_collection):
        old.objects.unlink(obj)
    collection.objects.link(obj)
    set_material(obj, mat)
    obj.hide_render = True
    return tag(obj, LOD2_ID, role, 2)


def low_torus(collection, name, loc, major, minor, mat, role):
    bpy.ops.mesh.primitive_torus_add(
        major_radius=major,
        minor_radius=minor,
        major_segments=16,
        minor_segments=6,
        location=loc,
    )
    obj = bpy.context.object
    obj.name = name
    for old in list(obj.users_collection):
        old.objects.unlink(obj)
    collection.objects.link(obj)
    set_material(obj, mat)
    obj.hide_render = True
    return tag(obj, LOD2_ID, role, 2)


def low_curve(collection, name, points, radius, mat, role):
    data = bpy.data.curves.new(name + "_CURVE", "CURVE")
    data.dimensions = "3D"
    data.bevel_depth = radius
    data.bevel_resolution = 0
    data.resolution_u = 1
    spline = data.splines.new("POLY")
    spline.points.add(len(points) - 1)
    for point, xyz in zip(spline.points, points):
        point.co = (*xyz, 1)
    obj = bpy.data.objects.new(name, data)
    collection.objects.link(obj)
    set_material(obj, mat)
    obj.hide_render = True
    return tag(obj, LOD2_ID, role, 2)


def tri_count(objects):
    return sum(
        sum(max(0, len(poly.vertices) - 2) for poly in obj.data.polygons)
        for obj in objects
        if obj.type == "MESH"
    )


def build():
    _, lod1_col, lod2_col, meta_col = ensure_collections()
    source = source_objects()
    by_role = roles(source)

    # LOD1: major structure and encounter/readability features only.
    lod1_sources = []
    for role in (
        "core_lower",
        "core_upper",
        "load_bearing_basal_mass",
        "sensory_crown",
        "human_extraction_collar",
        "pressure_membrane",
        "membrane_support",
        "tentacle_sensory_tip",
    ):
        lod1_sources += by_role.get(role, [])
    lod1_sources += sorted(by_role.get("load_bearing_buttress", []), key=lambda o: o.name)[::2]
    lod1_sources += [o for o in by_role.get("macro_sensory_eye", []) if "_R0_" in o.name]
    lod1_sources += [
        o
        for o in by_role.get("tentacle_segment", [])
        if o.name.endswith("_Seg_00") or o.name.endswith("_Seg_02")
    ]
    lod1_sources += sorted(by_role.get("extraction_hardware", []), key=lambda o: o.name)[::2]
    seen = set()
    lod1 = []
    for src in lod1_sources:
        if src.name in seen or src.type not in {"MESH", "CURVE"}:
            continue
        seen.add(src.name)
        lod1.append(linked_copy(src, "LOD1_" + src.name, lod1_col))

    coral = material("PEL_MAT_LivingCoral_Tissue", "PEL_LivingCoral")
    memory = material("PEL_MAT_MemoryCyan_Biolum", "PEL_Memory_Cyan")
    bronze = material("PEL_MAT_Bronze_Oxidized_Marine", "PEL_Precursor_Bronze")

    # LOD2: low-poly silhouette reconstruction.
    for role, label in (
        ("core_lower", "CoreLower"),
        ("core_upper", "CoreUpper"),
        ("load_bearing_basal_mass", "BasalMass"),
    ):
        srcs = by_role.get(role, [])
        if srcs:
            src = srcs[0]
            low_sphere(
                lod2_col,
                "LOD2_THA_" + label,
                src.matrix_world.translation,
                tuple(float(v) for v in src.dimensions),
                coral,
                "lod2_" + role,
            )

    crown = by_role.get("sensory_crown", [])
    if crown:
        src = crown[0]
        low_torus(
            lod2_col,
            "LOD2_THA_Crown",
            src.matrix_world.translation,
            max(src.dimensions.x, src.dimensions.y) * 0.38,
            max(0.12, src.dimensions.z * 0.10),
            memory,
            "lod2_sensory_crown",
        )
    collar = by_role.get("human_extraction_collar", [])
    if collar:
        src = collar[0]
        low_torus(
            lod2_col,
            "LOD2_THA_ExtractionCollar",
            src.matrix_world.translation,
            max(src.dimensions.x, src.dimensions.y) * 0.38,
            max(0.12, src.dimensions.z * 0.10),
            bronze,
            "lod2_extraction_collar",
        )

    core_sources = (
        by_role.get("core_lower", [])
        + by_role.get("core_upper", [])
        + by_role.get("load_bearing_basal_mass", [])
    )
    center = sum((o.matrix_world.translation for o in core_sources), Vector((0, 0, 0))) / max(1, len(core_sources))
    tips = sorted(
        by_role.get("tentacle_sensory_tip", []),
        key=lambda o: math.atan2(
            o.matrix_world.translation.y - center.y,
            o.matrix_world.translation.x - center.x,
        ),
    )
    for index, tip in enumerate(tips[:8]):
        target = tip.matrix_world.translation.copy()
        radial = Vector((target.x - center.x, target.y - center.y, 0))
        if radial.length == 0:
            radial = Vector((1, 0, 0))
        direction = radial.normalized()
        root = Vector((center.x + direction.x * 5.8, center.y + direction.y * 5.8, center.z - 1.0))
        mid = Vector(((root.x + target.x) * 0.5, (root.y + target.y) * 0.5, center.z - 3.2))
        low_curve(
            lod2_col,
            f"LOD2_THA_Tentacle_{index:02d}",
            [root, mid, target],
            0.42,
            coral,
            "lod2_tentacle",
        )

    ring0 = sorted(
        [o for o in by_role.get("macro_sensory_eye", []) if "_R0_" in o.name],
        key=lambda o: math.atan2(
            o.matrix_world.translation.y - center.y,
            o.matrix_world.translation.x - center.x,
        ),
    )
    for index, src in enumerate(ring0[::2][:8]):
        dims = tuple(max(0.25, float(v) * 0.9) for v in src.dimensions)
        low_sphere(
            lod2_col,
            f"LOD2_THA_Eye_{index:02d}",
            src.matrix_world.translation,
            dims,
            memory,
            "lod2_macro_eye",
        )
    for index, src in enumerate(by_role.get("pressure_membrane", [])):
        dims = (
            max(0.7, src.dimensions.x * 0.55),
            max(0.7, src.dimensions.y * 0.55),
            max(0.15, src.dimensions.z * 0.35),
        )
        low_sphere(
            lod2_col,
            f"LOD2_THA_Membrane_{index:02d}",
            src.matrix_world.translation,
            dims,
            memory,
            "lod2_pressure_membrane",
        )

    meta = bpy.data.objects.new("PEL_THALASSA_LOD_METADATA", None)
    meta_col.objects.link(meta)
    tag(meta, "PEL-BOSS-THALASSA-LODSET", "lod_metadata", "SET")
    meta["source_asset_id"] = SOURCE_ID
    meta["lod1_asset_id"] = LOD1_ID
    meta["lod2_asset_id"] = LOD2_ID
    meta["switch_thresholds"] = "UNKNOWN_PENDING_ENGINE_CAMERA_PROFILE"
    meta["selection_metric"] = "ENGINE_SCREEN_SIZE_OR_DISTANCE_TO_BE_QUALIFIED"
    meta["collision_policy"] = (
        "SHARE_SEPARATE_SOURCE_COLLISION_PROXY; visual LOD must not alter gameplay collision by itself"
    )
    meta["lod0_policy"] = "full HERO_ENGINEERING_BLOCKOUT_V1"
    meta["lod1_policy"] = (
        "major core/collar/membranes + 16 R0 eyes + alternating buttresses + 2 of 4 segments per tentacle + all tips"
    )
    meta["lod2_policy"] = (
        "low-poly core/basal/crown/collar + 8 three-point tentacles + 8 eyes + 4 membrane markers"
    )
    meta["engine_state"] = "NOT_IMPORTED_NOT_SWITCHED"

    lod0_mesh = [
        o
        for o in source
        if o.type == "MESH"
        and not str(o.get("role", "")).startswith("collision_proxy")
        and str(o.get("role", "")) not in {"arena_hydrophone", "ventilated_safe_platform_marker"}
    ]
    return {
        "checkpoint": "PELAGOS-THALASSA-LOD-001",
        "source_lod0_visual_tris_est": tri_count(lod0_mesh),
        "lod1_object_count": len(lod1),
        "lod1_mesh_tris_est": tri_count(lod1),
        "lod2_object_count": len(lod2_col.objects),
        "lod2_mesh_tris_est": tri_count(list(lod2_col.objects)),
        "switch_thresholds": "PENDING_ENGINE",
        "collision": "shared separate source collision proxy; not duplicated",
        "pending": ["runtime switching", "target-hardware performance", "engine camera validation", "human GATE-ART"],
    }


if __name__ == "__main__":
    result = build()
    print(result)
