"""Apply Pelagos coral UV0 tiled foundation v2.

Blender 5.2+, metres. Visibility-independent and deterministic: each polygon is projected
along its dominant normal axis directly into mesh UV data. 1 UV unit = 2 metres.
This is a portable structural foundation, not final hero unwrap/texel-density/bake approval.
"""
import bpy

ASSET_ID = "PEL-BIOME-CORAL-GROWTH"
UV_NAME = "UV0"
TILE_METRES = 2.0


def coral_meshes():
    meshes = {}
    for obj in bpy.data.objects:
        if (
            str(obj.get("asset_id", "")) == ASSET_ID
            and obj.type == "MESH"
            and not str(obj.get("production_state", "")).startswith("SUPERSEDED")
        ):
            meshes[obj.data.name] = obj.data
    return meshes


def project_mesh(mesh, tile_metres=TILE_METRES):
    uv = mesh.uv_layers.get(UV_NAME)
    if uv is None:
        uv = mesh.uv_layers.new(name=UV_NAME)
    uv.active = True
    for poly in mesh.polygons:
        normal = poly.normal
        axis = max(range(3), key=lambda i: abs(normal[i]))
        for loop_index in poly.loop_indices:
            vertex_index = mesh.loops[loop_index].vertex_index
            co = mesh.vertices[vertex_index].co
            if axis == 0:
                u, v = co.y / tile_metres, co.z / tile_metres
            elif axis == 1:
                u, v = co.x / tile_metres, co.z / tile_metres
            else:
                u, v = co.x / tile_metres, co.y / tile_metres
            uv.data[loop_index].uv = (u, v)
    return {
        "mesh": mesh.name,
        "mesh_loops": len(mesh.loops),
        "uv_loops": len(uv.data),
        "all_finite": all(abs(value) < 1e9 for item in uv.data for value in item.uv),
    }


def update_metadata():
    meta = next(
        (
            obj
            for obj in bpy.data.objects
            if obj.get("role") == "procedural_coral_system"
            and str(obj.get("asset_id", "")) == ASSET_ID
        ),
        None,
    )
    if meta:
        meta["uv_foundation"] = "UV0_BOX_PROJECT_TILE_2M_V2"
        meta["uv_tile_metres"] = TILE_METRES
        meta["uv_final_status"] = (
            "STRUCTURAL_TILED_FOUNDATION; hero unwrap/texel density/bake validation pending"
        )
        meta["uv_script"] = "art_source/worlds/pelagos/scripts/apply_coral_uv_v2.py"
    return meta


def apply():
    meshes = coral_meshes()
    reports = [project_mesh(mesh) for _, mesh in sorted(meshes.items())]
    update_metadata()
    return {
        "checkpoint": "PELAGOS-CORAL-UV-002",
        "asset_id": ASSET_ID,
        "projection": "dominant-axis box projection per polygon",
        "tile_metres": TILE_METRES,
        "unique_mesh_count": len(meshes),
        "reports": reports,
        "all_have_uv_data": all(
            r["mesh_loops"] == r["uv_loops"] and r["uv_loops"] > 0 and r["all_finite"]
            for r in reports
        ),
        "pending": [
            "hero seam review",
            "texel-density acceptance",
            "bake validation",
            "engine material/mip validation",
        ],
    }


if __name__ == "__main__":
    result = apply()
    print(result)
