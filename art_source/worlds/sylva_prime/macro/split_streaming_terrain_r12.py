#!/usr/bin/env python3
"""Split the Sylva 12 km R6 macro terrain into 16 independent 3 km L3 tiles.

Input scene contract:
- SYLVA_TERRAIN_Macro12km_PROPOSAL: 49x49 grid, 250 m spacing
- SYLVA_COL_TERRAIN_Macro12km_LowRes_PROPOSAL: 33x33 grid, 375 m spacing
- 16 SYLVA_STREAM_L3_X#Y# empties at 3 km cell centers

Output:
- 16 render tiles, 13x13 each
- 16 collision tiles, 9x9 each
- exact duplicated boundary samples (zero seam height delta)
- cell-local XY coordinates, world Z preserved
- monolithic terrain sources retired

Claim: CLM-SYLVA-MACRO-001
Classification: PROPOSAL streaming interface, backend ENGINE_TBD.
"""
from __future__ import annotations

import bpy
import re

CLAIM = "CLM-SYLVA-MACRO-001"
CONTRACT = "SYLVA_TERRAIN_STREAM_R12"


def ensure_collection(name: str):
    scene = bpy.context.scene
    col = bpy.data.collections.get(name)
    if col is None:
        col = bpy.data.collections.new(name)
        scene.collection.children.link(col)
    return col


def world_grid(obj):
    out = {}
    for vertex in obj.data.vertices:
        point = obj.matrix_world @ vertex.co
        out[(round(point.x, 6), round(point.y, 6))] = float(point.z)
    return out


def build_tile(name, center_x, center_y, xs, ys, grid, collection, materials, classification, kind, parent):
    vertices, faces = [], []
    nx, ny = len(xs), len(ys)
    for y in ys:
        for x in xs:
            vertices.append((x - center_x, y - center_y, grid[(round(x, 6), round(y, 6))]))
    for iy in range(ny - 1):
        for ix in range(nx - 1):
            a = iy * nx + ix
            faces.append((a, a + 1, a + 1 + nx, a + nx))
    mesh = bpy.data.meshes.new(name + "_MESH")
    mesh.from_pydata(vertices, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    collection.objects.link(obj)
    obj.parent = parent
    obj.location = (0, 0, 0)
    obj.rotation_euler = (0, 0, 0)
    obj.scale = (1, 1, 1)
    for material in materials:
        if material:
            mesh.materials.append(material)
    if kind == "render":
        for polygon in mesh.polygons:
            polygon.use_smooth = True
    obj["classification"] = classification
    obj["owner_claim"] = CLAIM
    obj["terrain_model"] = "R6_BIOGEO_CAUSAL_MACRO_V1"
    obj["stream_contract"] = CONTRACT
    obj["tile_size_m"] = 3000
    obj["kind"] = kind
    obj["tile_center_world_xy"] = f"{center_x},{center_y}"
    obj["renderable_final"] = kind == "render"
    return obj


def coordinate_map(objects):
    data = {}
    for obj in objects:
        for vertex in obj.data.vertices:
            point = obj.matrix_world @ vertex.co
            data.setdefault((round(point.x, 6), round(point.y, 6)), []).append(float(point.z))
    return data


def seam_stats(data):
    shared = [values for values in data.values() if len(values) > 1]
    deltas = [max(values) - min(values) for values in shared]
    return len(shared), max(deltas) if deltas else 0.0


def main():
    scene = bpy.context.scene
    terrain = bpy.data.objects.get("SYLVA_TERRAIN_Macro12km_PROPOSAL")
    collision = bpy.data.objects.get("SYLVA_COL_TERRAIN_Macro12km_LowRes_PROPOSAL")
    if not terrain or terrain.type != "MESH" or not collision or collision.type != "MESH":
        raise RuntimeError("R11 monolithic terrain sources missing")
    if any(o.name.startswith("SYLVA_TERRAIN_L3_X") for o in bpy.data.objects):
        raise RuntimeError("R12 terrain tiles already exist")

    render_grid = world_grid(terrain)
    collision_grid = world_grid(collision)
    rx = sorted({key[0] for key in render_grid})
    ry = sorted({key[1] for key in render_grid})
    cx = sorted({key[0] for key in collision_grid})
    cy = sorted({key[1] for key in collision_grid})
    if (len(rx), len(ry), len(cx), len(cy)) != (49, 49, 33, 33):
        raise RuntimeError("Unexpected source grid dimensions")

    render_collection = ensure_collection("SYLVA_11_TERRAIN_STREAM_TILES")
    collision_collection = ensure_collection("SYLVA_66_COLLISION_STREAM_TILES")
    meta_collection = ensure_collection("SYLVA_00_META_STREAMING_R12")
    render_materials = list(terrain.data.materials)
    collision_materials = list(collision.data.materials)
    render_tiles, collision_tiles = [], []

    for tx in range(4):
        for ty in range(4):
            x0, x1 = -6000 + tx * 3000, -3000 + tx * 3000
            y0, y1 = -6000 + ty * 3000, -3000 + ty * 3000
            center_x, center_y = (x0 + x1) / 2, (y0 + y1) / 2
            rxs = [x for x in rx if x0 - 1e-6 <= x <= x1 + 1e-6]
            rys = [y for y in ry if y0 - 1e-6 <= y <= y1 + 1e-6]
            cxs = [x for x in cx if x0 - 1e-6 <= x <= x1 + 1e-6]
            cys = [y for y in cy if y0 - 1e-6 <= y <= y1 + 1e-6]
            if (len(rxs), len(rys), len(cxs), len(cys)) != (13, 13, 9, 9):
                raise RuntimeError(f"Partition mismatch X{tx}Y{ty}")
            stream = bpy.data.objects.get(f"SYLVA_STREAM_L3_X{tx}Y{ty}")
            if not stream:
                raise RuntimeError(f"Missing stream cell X{tx}Y{ty}")
            render_name = f"SYLVA_TERRAIN_L3_X{tx}Y{ty}"
            collision_name = f"SYLVA_COL_TERRAIN_L3_X{tx}Y{ty}"
            render_obj = build_tile(render_name, center_x, center_y, rxs, rys, render_grid, render_collection, render_materials, "L3_STREAM_RENDER_TILE_PROPOSAL", "render", stream)
            collision_obj = build_tile(collision_name, center_x, center_y, cxs, cys, collision_grid, collision_collection, collision_materials, "L3_STREAM_COLLISION_TILE_PROPOSAL", "collision", stream)
            collision_obj.hide_render = True
            collision_obj.display_type = "WIRE"
            collision_obj["collision_policy"] = "CUSTOM_LOWRES_HEIGHTFIELD_TILE"
            stream["terrain_contract"] = CONTRACT
            stream["render_tile"] = render_name
            stream["collision_tile"] = collision_name
            stream["render_grid"] = "13x13"
            stream["collision_grid"] = "9x9"
            stream["seam_policy"] = "SHARED_SOURCE_HEIGHT_EXACT"
            render_tiles.append(render_obj)
            collision_tiles.append(collision_obj)

    retired = [terrain.name, collision.name]
    for obj in (terrain, collision):
        mesh = obj.data
        bpy.data.objects.remove(obj, do_unlink=True)
        if mesh.users == 0:
            bpy.data.meshes.remove(mesh)

    meta = bpy.data.objects.new("SYLVA_META_TerrainStreamingR12", None)
    meta_collection.objects.link(meta)
    meta["classification"] = "PROPOSAL_STREAMING_INTERFACE"
    meta["owner_claim"] = CLAIM
    meta["contract"] = CONTRACT
    meta["source_terrain_model"] = "R6_BIOGEO_CAUSAL_MACRO_V1"
    meta["local_patch_m"] = 12000
    meta["tile_count"] = 16
    meta["tile_size_m"] = 3000
    meta["render_tile_grid"] = "13x13 @250m"
    meta["collision_tile_grid"] = "9x9 @375m"
    meta["seam_policy"] = "EXACT_DUPLICATED_BOUNDARY_SAMPLES"
    meta["origin_policy"] = "CELL_LOCAL_XY_PLUS_WORLD_Z"
    meta["backend"] = "ENGINE_TBD"
    meta["hlod_status"] = "NOT_IMPLEMENTED_TARGET_BACKEND_PENDING"
    meta["monolithic_sources_retired"] = "|".join(retired)

    root = bpy.data.objects.get("SYLVA_WORLD_ROOT")
    if root:
        root["build_status"] = "WAVE1J_STREAMING_TERRAIN_TILES_R12"
        root["terrain_stream_contract"] = CONTRACT

    bpy.context.view_layer.update()
    render_seams = seam_stats(coordinate_map(render_tiles))
    collision_seams = seam_stats(coordinate_map(collision_tiles))
    if render_seams[1] > 1e-8 or collision_seams[1] > 1e-8:
        raise RuntimeError(f"Seam mismatch render={render_seams} collision={collision_seams}")

    pattern = re.compile(r"_X(\d)Y(\d)$")
    for obj in render_tiles + collision_tiles:
        if any(abs(scale - 1.0) > 1e-8 for scale in obj.scale):
            raise RuntimeError("Non-unit tile scale: " + obj.name)
        match = pattern.search(obj.name)
        tx, ty = int(match.group(1)), int(match.group(2))
        expected_parent = f"SYLVA_STREAM_L3_X{tx}Y{ty}"
        if not obj.parent or obj.parent.name != expected_parent:
            raise RuntimeError("Wrong tile parent: " + obj.name)
        if abs(obj.dimensions.x - 3000) > 1e-6 or abs(obj.dimensions.y - 3000) > 1e-6:
            raise RuntimeError("Wrong tile footprint: " + obj.name)

    bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
    return {
        "render_tiles": 16,
        "collision_tiles": 16,
        "render_vertices_total": sum(len(o.data.vertices) for o in render_tiles),
        "collision_vertices_total": sum(len(o.data.vertices) for o in collision_tiles),
        "render_seam_delta_m": render_seams[1],
        "collision_seam_delta_m": collision_seams[1],
    }


if __name__ == "__main__":
    print(main())
