"""KHEPRI macro-terrain tiling contract.

Claim: CLM-KHEPRI-WMACRO-001

This module is deliberately Blender-independent so terrain continuity can be tested in CI.
It defines how neighboring local-tangent authoring cells sample one deterministic GLOBAL
height field while storing their mesh vertices in LOCAL metre coordinates.

It does NOT declare 6.4 x 4.8 km to be a final engine streaming tile size and does not
canonize KHP-ADR-001 planet radius. Engine world-partition/origin-rebasing remains downstream.
"""
from __future__ import annotations

import json
import math
from dataclasses import dataclass

CELL_SIZE_X_M = 6_400.0
CELL_SIZE_Y_M = 4_800.0
GRID_X = 81
GRID_Y = 61
GRID_SPACING_X_M = CELL_SIZE_X_M / (GRID_X - 1)
GRID_SPACING_Y_M = CELL_SIZE_Y_M / (GRID_Y - 1)
HEIGHT_MODEL_VERSION = "KHP_TERRAIN_V1"
PLANET_RADIUS_M_PROPOSAL = 5_224_000.0  # KHP-ADR-001; NOT CANON.


@dataclass(frozen=True)
class TileAddress:
    x: int
    y: int

    @property
    def origin_xy_m(self) -> tuple[float, float]:
        return self.x * CELL_SIZE_X_M, self.y * CELL_SIZE_Y_M


def terrain_height_global(x_m: float, y_m: float) -> float:
    """Deterministic macro-only height field used by KHEPRI blockout v1.

    x_m/y_m are GLOBAL tangent-grid coordinates. Keeping the procedural function in global
    space is the seam contract; local tile coordinates are only a storage/precision frame.
    """
    broad = 74.0 * math.sin(x_m / 890.0) * math.cos(y_m / 730.0)
    secondary = 31.0 * math.sin((x_m + 0.37 * y_m) / 370.0)
    tertiary = 13.0 * math.cos((0.28 * x_m - y_m) / 210.0)
    glass_sea_basin = -58.0 * math.exp(-((y_m + 180.0) / 620.0) ** 2)
    crucible_shelf = 44.0 * math.exp(
        -(((x_m - 1250.0) / 900.0) ** 2 + ((y_m + 650.0) / 780.0) ** 2)
    )
    return broad + secondary + tertiary + glass_sea_basin + crucible_shelf


def local_xy(ix: int, iy: int) -> tuple[float, float]:
    if not 0 <= ix < GRID_X or not 0 <= iy < GRID_Y:
        raise IndexError((ix, iy))
    return (
        -CELL_SIZE_X_M / 2.0 + GRID_SPACING_X_M * ix,
        -CELL_SIZE_Y_M / 2.0 + GRID_SPACING_Y_M * iy,
    )


def global_xy(tile: TileAddress, ix: int, iy: int) -> tuple[float, float]:
    local_x, local_y = local_xy(ix, iy)
    origin_x, origin_y = tile.origin_xy_m
    return origin_x + local_x, origin_y + local_y


def vertex_local(tile: TileAddress, ix: int, iy: int) -> tuple[float, float, float]:
    """Return local mesh vertex; height is evaluated in global coordinates."""
    local_x, local_y = local_xy(ix, iy)
    global_x, global_y = global_xy(tile, ix, iy)
    return local_x, local_y, terrain_height_global(global_x, global_y)


def normal_global(x_m: float, y_m: float, epsilon_m: float = 1.0):
    """Seam-stable normal source for future smooth-shaded terrain.

    A global-space central difference makes the normal independent of which tile owns a border
    vertex. The current blockout need not promote these to authored custom normals yet.
    """
    dz_dx = (
        terrain_height_global(x_m + epsilon_m, y_m)
        - terrain_height_global(x_m - epsilon_m, y_m)
    ) / (2.0 * epsilon_m)
    dz_dy = (
        terrain_height_global(x_m, y_m + epsilon_m)
        - terrain_height_global(x_m, y_m - epsilon_m)
    ) / (2.0 * epsilon_m)
    vector = (-dz_dx, -dz_dy, 1.0)
    length = math.sqrt(sum(component * component for component in vector))
    return tuple(component / length for component in vector)


def angle_deg(a, b) -> float:
    dot = sum(left * right for left, right in zip(a, b))
    return math.degrees(math.acos(max(-1.0, min(1.0, dot))))


def audit_pair(a: TileAddress, b: TileAddress, direction: str) -> dict:
    pairs = []
    if direction == "E":
        pairs = [((GRID_X - 1, iy), (0, iy)) for iy in range(GRID_Y)]
    elif direction == "W":
        pairs = [((0, iy), (GRID_X - 1, iy)) for iy in range(GRID_Y)]
    elif direction == "N":
        pairs = [((ix, GRID_Y - 1), (ix, 0)) for ix in range(GRID_X)]
    elif direction == "S":
        pairs = [((ix, 0), (ix, GRID_Y - 1)) for ix in range(GRID_X)]
    else:
        raise ValueError(direction)

    height_errors = []
    normal_errors = []
    coordinate_errors = []
    for (a_ix, a_iy), (b_ix, b_iy) in pairs:
        a_gx, a_gy = global_xy(a, a_ix, a_iy)
        b_gx, b_gy = global_xy(b, b_ix, b_iy)
        coordinate_errors.append(math.hypot(a_gx - b_gx, a_gy - b_gy))
        height_errors.append(
            abs(terrain_height_global(a_gx, a_gy) - terrain_height_global(b_gx, b_gy))
        )
        normal_errors.append(
            angle_deg(normal_global(a_gx, a_gy), normal_global(b_gx, b_gy))
        )

    return {
        "samples": len(pairs),
        "max_global_coordinate_error_m": max(coordinate_errors, default=0.0),
        "max_height_error_m": max(height_errors, default=0.0),
        "max_normal_angle_error_deg": max(normal_errors, default=0.0),
    }


def curvature_context(radius_m: float = PLANET_RADIUS_M_PROPOSAL) -> dict:
    """Quantify the flat local-tangent approximation; radius remains PROPOSAL."""
    half_diagonal = math.hypot(CELL_SIZE_X_M / 2.0, CELL_SIZE_Y_M / 2.0)
    sagitta = radius_m - math.sqrt(radius_m * radius_m - half_diagonal * half_diagonal)
    return {
        "radius_m_proposal": radius_m,
        "half_cell_diagonal_m": half_diagonal,
        "flat_cell_corner_sagitta_m_proposal": sagitta,
        "canon_status": "PROPOSAL_CONTEXT_ONLY",
    }


def audit() -> dict:
    center = TileAddress(0, 0)
    neighbors = {
        "E": TileAddress(1, 0),
        "W": TileAddress(-1, 0),
        "N": TileAddress(0, 1),
        "S": TileAddress(0, -1),
    }
    audits = {
        direction: audit_pair(center, neighbor, direction)
        for direction, neighbor in neighbors.items()
    }
    max_coordinate = max(item["max_global_coordinate_error_m"] for item in audits.values())
    max_height = max(item["max_height_error_m"] for item in audits.values())
    max_normal = max(item["max_normal_angle_error_deg"] for item in audits.values())
    checks = {
        "grid_is_uniform_80m": GRID_SPACING_X_M == 80.0 and GRID_SPACING_Y_M == 80.0,
        "neighbor_coordinates_match": max_coordinate <= 1e-9,
        "neighbor_heights_match": max_height <= 1e-9,
        "global_normals_match": max_normal <= 1e-4,
        "tile_vertices_remain_local": vertex_local(center, 0, 0)[:2]
        == (-CELL_SIZE_X_M / 2.0, -CELL_SIZE_Y_M / 2.0),
    }
    return {
        "height_model_version": HEIGHT_MODEL_VERSION,
        "cell_size_m": [CELL_SIZE_X_M, CELL_SIZE_Y_M],
        "grid": [GRID_X, GRID_Y],
        "grid_spacing_m": [GRID_SPACING_X_M, GRID_SPACING_Y_M],
        "seams": audits,
        "max_global_coordinate_error_m": max_coordinate,
        "max_height_error_m": max_height,
        "max_normal_angle_error_deg": max_normal,
        "curvature_context": curvature_context(),
        "checks": checks,
        "passed": all(checks.values()),
        "boundary": (
            "Authoring continuity proof only; no final engine tile size, planet curvature, "
            "collision, navmesh, HLOD or world-partition implementation is claimed."
        ),
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
