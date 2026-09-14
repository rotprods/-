"""Refine the SYLVA PRIME macro terrain from blockout waves into the r6 causal model.

Run after:
1. generate_sylva_macro.py
2. add_sylva_macro_interfaces.py
3. add_vesper_three_terraces.py

This remains a PROPOSAL macro terrain model. It does not invent canonical tectonics,
continents or waterways and deliberately adds no micro-detail. Root-bearing ridges and
catchment depressions are production hypotheses used to make macro form causal and
reviewable. Visible terrain and low-res collision are generated from the exact same
height function.
"""
from __future__ import annotations

import bpy
import math

CLAIM = "CLM-SYLVA-MACRO-001"
MODEL = "R6_BIOGEO_CAUSAL_MACRO_V1"

PUERTO = (-3200.0, -2200.0, 330.0)
BOSQUE = (0.0, 150.0, 350.0)
VESPER = (3200.0, 2300.0, -220.0)

ROOT_LINES = [
    [(-5000,-3500),(-4100,-2800),(-3200,-2200),(-2200,-1200),(-1100,-300)],
    [(-1200,-500),(-700,150),(0,150),(900,700),(1800,1350)],
    [(1700,1200),(2350,1700),(3200,2300),(3900,2800),(4800,3300)],
    [(-3900,-500),(-2500,200),(-900,800),(700,1200),(2300,1800)],
    [(-1700,-3600),(-800,-2200),(200,-900),(900,200),(1450,1300)],
    [(3600,-800),(2800,200),(2100,900),(1800,1600),(2500,2200)],
]
ROOT_AMPLITUDES = [115, 135, 150, 80, 70, 95]
ROOT_WIDTHS_M = [260, 300, 330, 230, 210, 250]

# Production hypotheses, not canon rivers.
DRAIN_LINES = [
    [(-5600,2600),(-4000,1700),(-2400,800),(-900,-200),(400,-1500),(1800,-3200),(3300,-5200)],
    [(-4500,5200),(-3300,3800),(-1800,2600),(-300,1800),(1100,1600),(2600,800),(5000,-200)],
]

ROUTE_NODES = [
    PUERTO,
    (-1800.0, -900.0, 430.0),
    BOSQUE,
    (1650.0, 1150.0, 300.0),
    VESPER,
]


def _distance_to_segment(px, py, a, b):
    ax, ay = a
    bx, by = b
    vx, vy = bx - ax, by - ay
    wx, wy = px - ax, py - ay
    den = vx * vx + vy * vy
    t = 0.0 if den == 0 else max(0.0, min(1.0, (wx * vx + wy * vy) / den))
    cx, cy = ax + t * vx, ay + t * vy
    return math.hypot(px - cx, py - cy), t


def _distance_to_polyline(px, py, line):
    best = (1e30, 0, 0.0)
    for index in range(len(line) - 1):
        dist, t = _distance_to_segment(px, py, line[index], line[index + 1])
        if dist < best[0]:
            best = (dist, index, t)
    return best


def _route_target(px, py):
    best = (1e30, 0.0)
    for index in range(len(ROUTE_NODES) - 1):
        a, b = ROUTE_NODES[index], ROUTE_NODES[index + 1]
        dist, t = _distance_to_segment(px, py, a[:2], b[:2])
        z = a[2] + (b[2] - a[2]) * t
        if dist < best[0]:
            best = (dist, z)
    return best


def terrain_height(x: float, y: float) -> float:
    # Low-frequency substrate only. No microgeometry noise.
    z = (
        95 * math.sin((x + y * 0.22) / 2100.0)
        + 70 * math.cos((y - x * 0.15) / 1750.0)
        + 42 * math.sin((x - y) / 930.0)
        + 25 * math.cos((x * 0.58 + y) / 620.0)
    )
    z += 0.018 * y - 0.006 * x

    # Canon-region support forms.
    z += 155 * math.exp(-(((x + 3200) / 1250.0) ** 2 + ((y + 2200) / 1050.0) ** 2))
    z += 210 * math.exp(-(((x - 100) / 1750.0) ** 2 + ((y - 150) / 1450.0) ** 2))

    # VESPER root-knot basin + outer load rim.
    rv = math.hypot(x - 3200.0, y - 2300.0)
    z += -430 * math.exp(-(rv / 850.0) ** 2)
    z += 110 * math.exp(-((rv - 1050.0) / 420.0) ** 2)

    # Terrain responds to six already-authored macro structural-root corridors.
    for line, amplitude, width in zip(ROOT_LINES, ROOT_AMPLITUDES, ROOT_WIDTHS_M):
        distance, _, _ = _distance_to_polyline(x, y, line)
        z += amplitude * math.exp(-(distance / width) ** 2)

    # Proposed catchments: production shaping only, explicitly not canon waterways.
    for line, amplitude, width in (
        (DRAIN_LINES[0], -95, 260),
        (DRAIN_LINES[1], -70, 220),
    ):
        distance, _, _ = _distance_to_polyline(x, y, line)
        z += amplitude * math.exp(-(distance / width) ** 2)

    # Broad support band around the authored macro route centerline.
    distance, route_z = _route_target(x, y)
    route_weight = math.exp(-((distance / 140.0) ** 4))
    z = z * (1.0 - route_weight) + route_z * route_weight

    # Stable local support under current hero-zone foundations.
    vesper_weight = math.exp(-((rv / 240.0) ** 4))
    z = z * (1.0 - vesper_weight) + (-270.0) * vesper_weight

    rp = math.hypot(x + 3200.0, y + 2200.0)
    puerto_weight = math.exp(-((rp / 230.0) ** 4))
    z = z * (1.0 - puerto_weight) + 335.0 * puerto_weight

    rb = math.hypot(x, y - 150.0)
    bosque_weight = math.exp(-((rb / 240.0) ** 4))
    z = z * (1.0 - bosque_weight) + 350.0 * bosque_weight
    return z


def build():
    terrain = bpy.data.objects.get("SYLVA_TERRAIN_Macro12km_PROPOSAL")
    if terrain is None:
        raise RuntimeError("missing render terrain")

    for vertex in terrain.data.vertices:
        vertex.co.z = terrain_height(float(vertex.co.x), float(vertex.co.y))
    terrain.data.update()
    terrain["classification"] = "PROPOSAL"
    terrain["terrain_model"] = MODEL
    terrain["root_bearing_ridges"] = 6
    terrain["drainage_corridors_proposal"] = 2
    terrain["route_support_halfwidth_m"] = 140.0
    terrain["hero_support_z_m"] = "Puerto=335|Bosque=350|VESPER=-270"
    terrain["micro_detail"] = "EXCLUDED_FROM_R6"

    collision = bpy.data.objects.get("SYLVA_COL_TERRAIN_Macro12km_LowRes_PROPOSAL")
    if collision is None:
        raise RuntimeError("missing collision terrain")

    previous_mesh = collision.data
    n = 33
    size = 12000.0
    vertices, faces = [], []
    for iy in range(n):
        y = -size / 2 + size * iy / (n - 1)
        for ix in range(n):
            x = -size / 2 + size * ix / (n - 1)
            vertices.append((x, y, terrain_height(x, y)))
    for iy in range(n - 1):
        for ix in range(n - 1):
            a = iy * n + ix
            faces.append((a, a + 1, a + 1 + n, a + n))

    mesh = bpy.data.meshes.new("SYLVA_COL_Terrain12km_R6_33x33_Mesh")
    mesh.from_pydata(vertices, [], faces)
    mesh.update()
    collision.data = mesh
    if previous_mesh.users == 0:
        bpy.data.meshes.remove(previous_mesh)

    collision["classification"] = "COLLISION_PROXY_PROPOSAL"
    collision["collision_policy"] = "CUSTOM_LOWRES_HEIGHTFIELD"
    collision["terrain_model"] = MODEL
    collision["grid_resolution"] = "33x33"
    collision["renderable_final"] = False

    meta = bpy.data.objects.get("SYLVA_META_TerrainModel_R6")
    if meta is None:
        meta = bpy.data.objects.new("SYLVA_META_TerrainModel_R6", None)
        meta.empty_display_type = "SPHERE"
        meta.empty_display_size = 24
        bpy.data.collections["SYLVA_00_META"].objects.link(meta)
    meta.location = (0, 0, 0)
    for key, value in {
        "classification": "PROPOSAL_MACRO_TERRAIN_MODEL",
        "owner_claim": CLAIM,
        "model_id": MODEL,
        "geological_claim": "NO_CANON_TECTONICS_INFERRED",
        "root_load_response": "PROPOSAL",
        "drainage_corridors": "PROPOSAL_NOT_CANON_WATERWAYS",
        "route_preservation": True,
        "render_grid": "49x49",
        "collision_grid": "33x33",
        "micro_detail": "DEFERRED",
    }.items():
        meta[key] = value

    root = bpy.data.objects.get("SYLVA_WORLD_ROOT")
    if root:
        root["build_status"] = "WAVE1D_BIOGEO_MACRO_TERRAIN_R6"
        root["terrain_model"] = MODEL
        root["terrain_collision_grid"] = "33x33"

    bpy.ops.object.select_all(action="DESELECT")
    z_values = [float(vertex.co.z) for vertex in terrain.data.vertices]
    return {
        "terrain_vertices": len(terrain.data.vertices),
        "terrain_faces": len(terrain.data.polygons),
        "z_min_m": min(z_values),
        "z_max_m": max(z_values),
        "collision_vertices": len(mesh.vertices),
        "collision_faces": len(mesh.polygons),
        "root_ridges": 6,
        "drainage_proposals": 2,
        "micro_detail_added": False,
        "canon_geology_claimed": False,
    }


if __name__ == "__main__":
    print(build())
