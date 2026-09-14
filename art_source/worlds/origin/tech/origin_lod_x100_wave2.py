"""EXOVANT 2950 — ORIGIN X100 Wave 02 LOD generator.

Run inside Blender 5.2+ after the Wave-01 Atrio/Archive generators.
Creates hidden LOD1/LOD2 geometry from tagged ORIGIN source meshes without modifying LOD0.
LOD1 removes presentation bevel cost; LOD2 selectively decimates reducible meshes.
Dimensions remain proposal until engine qualification.
"""

import bpy

CLAIM_ID = "CLM-ORIGIN-TECH-LOD-WAVE01-001"
LOD1_COLLECTION = "70_ORIGIN_LOD1"
LOD2_COLLECTION = "71_ORIGIN_LOD2"
DECIMATE_RATIO = 0.45
MIN_POLYS_FOR_DECIMATE = 24
BOUNDS_DRIFT_LIMIT_M = 0.06


def ensure_collection(name):
    coll = bpy.data.collections.get(name)
    if coll is None:
        coll = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(coll)
    return coll


def purge_generated():
    doomed = [o for o in bpy.data.objects if o.get("origin_generated_lod")]
    for obj in doomed:
        bpy.data.objects.remove(obj, do_unlink=True)


def is_source_mesh(obj):
    if obj.type != "MESH":
        return False
    if not obj.get("origin_asset_id"):
        return False
    if obj.get("origin_generated_lod"):
        return False
    name = obj.name.upper()
    if name.startswith("COL_") or name.startswith("COLLISION_"):
        return False
    return True


def dimensions(obj):
    return tuple(float(v) for v in obj.dimensions)


def max_bounds_drift(a, b):
    return max(abs(x - y) for x, y in zip(dimensions(a), dimensions(b)))


def duplicate_base(source, level, collection):
    dup = source.copy()
    dup.data = source.data.copy()
    dup.animation_data_clear()
    dup.name = f"LOD{level}__{source.name}"
    dup.matrix_world = source.matrix_world.copy()
    for mod in list(dup.modifiers):
        dup.modifiers.remove(mod)
    dup["origin_generated_lod"] = True
    dup["origin_lod"] = level
    dup["origin_lod_source"] = source.name
    dup["origin_asset_id"] = source.get("origin_asset_id")
    dup["origin_claim_id"] = CLAIM_ID
    dup.hide_viewport = True
    dup.hide_render = True
    collection.objects.link(dup)
    return dup


def should_decimate(source):
    asset_id = str(source.get("origin_asset_id", ""))
    # Measured silhouette exception found by adversarial QA in Archive rev3.
    if asset_id == "ORG_ARC_ARCHIVE_CORE_SHELL_A" and source.name.endswith("_CORE"):
        return False
    return len(source.data.polygons) >= MIN_POLYS_FOR_DECIMATE


def apply_decimate(obj):
    mod = obj.modifiers.new(name="ORIGIN_LOD2_DECIMATE", type="DECIMATE")
    mod.ratio = DECIMATE_RATIO
    mod.use_collapse_triangulate = True
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    try:
        bpy.ops.object.modifier_apply(modifier=mod.name)
    finally:
        obj.select_set(False)


def build():
    purge_generated()
    lod1_coll = ensure_collection(LOD1_COLLECTION)
    lod2_coll = ensure_collection(LOD2_COLLECTION)
    sources = sorted((o for o in bpy.data.objects if is_source_mesh(o)), key=lambda o: o.name)

    rows = []
    for source in sources:
        lod1 = duplicate_base(source, 1, lod1_coll)
        lod2 = duplicate_base(source, 2, lod2_coll)
        if should_decimate(source):
            apply_decimate(lod2)
        drift = max_bounds_drift(source, lod2)
        if drift > BOUNDS_DRIFT_LIMIT_M:
            # Deterministic fail-safe: revert only this LOD2 to the unbeveled base mesh.
            old = lod2.data
            lod2.data = source.data.copy()
            if old.users == 0:
                bpy.data.meshes.remove(old)
            drift = max_bounds_drift(source, lod2)
        rows.append({
            "source": source.name,
            "asset_id": source.get("origin_asset_id"),
            "lod1": lod1.name,
            "lod2": lod2.name,
            "lod2_bounds_drift_m": drift,
        })

    bpy.context.scene["origin_lod_claim"] = CLAIM_ID
    bpy.context.scene["origin_lod_source_mesh_count"] = len(sources)
    bpy.context.scene["origin_lod_contract"] = "LOD0 frozen; LOD1 unbeveled; LOD2 selective decimation; <=6cm measured bounds drift"
    return rows


if __name__ == "__main__":
    rows = build()
    print(f"ORIGIN LOD generated for {len(rows)} source meshes")
