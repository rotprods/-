"""KHEPRI R6 terrain normal optimization.

Claim: CLM-KHEPRI-WMACRO-001
Stage order: generator -> mast instancing -> route R4 -> THIS STAGE.

Purpose:
- switch the 81x61 macro terrain from flat shading to smooth shading;
- assign deterministic GLOBAL-gradient custom normals so independently authored neighbor
  tiles do not derive incompatible one-sided border normals;
- reduce glTF/runtime vertex duplication without changing positions, topology or triangles.

This stage does not change terrain heights, tile dimensions, collision, route geometry,
materials, planet radius, or final engine/world-partition policy.
"""
from __future__ import annotations

import json
import math

import bpy
from mathutils import Vector

TERRAIN_OBJECT = "KHP_WM_L2_MACROCELL_A_TERRAIN"
GRID_X = 81
GRID_Y = 61
CELL_SIZE_X_M = 6400.0
CELL_SIZE_Y_M = 4800.0
NORMAL_EPSILON_M = 1.0
NORMAL_CONTRACT = "KHP_GLOBAL_GRADIENT_NORMAL_V1"


def terrain_height_global(x_m: float, y_m: float) -> float:
    broad = 74.0 * math.sin(x_m / 890.0) * math.cos(y_m / 730.0)
    secondary = 31.0 * math.sin((x_m + 0.37 * y_m) / 370.0)
    tertiary = 13.0 * math.cos((0.28 * x_m - y_m) / 210.0)
    glass_sea_basin = -58.0 * math.exp(-((y_m + 180.0) / 620.0) ** 2)
    crucible_shelf = 44.0 * math.exp(
        -(((x_m - 1250.0) / 900.0) ** 2 + ((y_m + 650.0) / 780.0) ** 2)
    )
    return broad + secondary + tertiary + glass_sea_basin + crucible_shelf


def global_normal(x_m: float, y_m: float, epsilon_m: float = NORMAL_EPSILON_M) -> Vector:
    dz_dx = (
        terrain_height_global(x_m + epsilon_m, y_m)
        - terrain_height_global(x_m - epsilon_m, y_m)
    ) / (2.0 * epsilon_m)
    dz_dy = (
        terrain_height_global(x_m, y_m + epsilon_m)
        - terrain_height_global(x_m, y_m - epsilon_m)
    ) / (2.0 * epsilon_m)
    normal = Vector((-dz_dx, -dz_dy, 1.0))
    normal.normalize()
    return normal


def apply() -> dict:
    terrain = bpy.data.objects.get(TERRAIN_OBJECT)
    if terrain is None or terrain.type != "MESH":
        raise RuntimeError(f"Missing terrain mesh object: {TERRAIN_OBJECT}")
    mesh = terrain.data
    expected_vertices = GRID_X * GRID_Y
    if len(mesh.vertices) != expected_vertices:
        raise RuntimeError(
            f"Unexpected terrain vertex count: {len(mesh.vertices)} != {expected_vertices}"
        )
    if int(terrain.get("grid_x", 0)) != GRID_X or int(terrain.get("grid_y", 0)) != GRID_Y:
        raise RuntimeError("Terrain grid metadata does not match R6 normal contract")

    before_smooth = sum(bool(poly.use_smooth) for poly in mesh.polygons)
    for polygon in mesh.polygons:
        polygon.use_smooth = True

    # Macrocell A is tile address (0,0), so local XY == global tangent-grid XY.
    normals = [global_normal(vertex.co.x, vertex.co.y) for vertex in mesh.vertices]
    mesh.normals_split_custom_set_from_vertices(normals)
    mesh.update()

    terrain["terrain_shading_contract"] = "SMOOTH_CUSTOM_GLOBAL"
    terrain["terrain_normal_contract"] = NORMAL_CONTRACT
    terrain["terrain_normal_epsilon_m"] = NORMAL_EPSILON_M
    terrain["terrain_normal_coordinate_frame"] = "global_tangent_grid_xy_metres"
    bpy.context.scene["khepri_content_revision"] = "R6_TERRAIN_GLOBAL_NORMALS"

    return {
        "terrain": TERRAIN_OBJECT,
        "vertices": len(mesh.vertices),
        "polygons": len(mesh.polygons),
        "smooth_polygons_before": before_smooth,
        "smooth_polygons_after": sum(bool(poly.use_smooth) for poly in mesh.polygons),
        "normal_contract": NORMAL_CONTRACT,
        "normal_epsilon_m": NORMAL_EPSILON_M,
        "positions_topology_changed": False,
    }


RESULT = apply()
print(json.dumps(RESULT, indent=2, sort_keys=True))
