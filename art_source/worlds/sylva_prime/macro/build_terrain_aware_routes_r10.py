"""SYLVA PRIME r10 — terrain-aware macro navigation centerlines + manifold collision ribbons.

Prerequisite scene state: r6 causal macro terrain (later metadata passes are compatible).
Claim: CLM-SYLVA-MACRO-001
Truth: navigation/collision PROPOSAL, not final gameplay or road art.

The solver uses the existing 49x49 visible terrain grid and keeps four stable consumer IDs:
  SYLVA_TRAV_PathGuide_00..03
  SYLVA_COL_ROUTE_00..03

It avoids the invalid side/cap topology found in the first r9 ribbon implementation.
"""
from __future__ import annotations

import heapq
import math

import bmesh
import bpy
from mathutils import Vector

CLAIM = "CLM-SYLVA-MACRO-001"
PROFILE = "BALANCED_FOOT_TERRAIN_AWARE_R10"
SOLVER = "A*_8_NEIGHBOR_SLOPE_WEIGHTED_R10"
HARD_MAX_GRADE_DEG = 22.0
SLOPE_WEIGHT = 1.0
ROUTE_CLEAR_WIDTH_M = 6.0
COLLISION_WIDTH_M = 8.0
COLLISION_THICKNESS_M = 2.4


def terrain_grid():
    terrain = bpy.data.objects["SYLVA_TERRAIN_Macro12km_PROPOSAL"]
    verts = [terrain.matrix_world @ v.co for v in terrain.data.vertices]
    xs = sorted(set(round(v.x, 6) for v in verts))
    ys = sorted(set(round(v.y, 6) for v in verts))
    index = {(round(v.x, 6), round(v.y, 6)): i for i, v in enumerate(verts)}
    z = {
        (ix, iy): verts[index[(xs[ix], ys[iy])]].z
        for ix in range(len(xs))
        for iy in range(len(ys))
    }
    return xs, ys, z


def nearest_grid(xs, ys, point_xy):
    x, y = point_xy
    return (
        min(range(len(xs)), key=lambda i: abs(xs[i] - x)),
        min(range(len(ys)), key=lambda i: abs(ys[i] - y)),
    )


def solve(xs, ys, z, start_xy, goal_xy):
    nx, ny = len(xs), len(ys)
    start = nearest_grid(xs, ys, start_xy)
    goal = nearest_grid(xs, ys, goal_xy)
    queue = [(0.0, start)]
    cost = {start: 0.0}
    came_from = {}

    while queue:
        _, current = heapq.heappop(queue)
        if current == goal:
            break
        ux, uy = current
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)):
            nxt = (ux + dx, uy + dy)
            if not (0 <= nxt[0] < nx and 0 <= nxt[1] < ny):
                continue
            horizontal = math.hypot(xs[nxt[0]] - xs[ux], ys[nxt[1]] - ys[uy])
            dz = z[nxt] - z[current]
            grade = math.degrees(math.atan2(abs(dz), horizontal))
            if grade > HARD_MAX_GRADE_DEG:
                continue
            d3 = math.hypot(horizontal, dz)
            step_cost = d3 * (1.0 + SLOPE_WEIGHT * (grade / 12.0) ** 2)
            candidate = cost[current] + step_cost
            if candidate < cost.get(nxt, float("inf")):
                cost[nxt] = candidate
                came_from[nxt] = current
                heuristic = math.hypot(xs[nxt[0]] - xs[goal[0]], ys[nxt[1]] - ys[goal[1]])
                heapq.heappush(queue, (candidate + heuristic, nxt))

    if goal not in cost:
        raise RuntimeError(f"No route found {start_xy} -> {goal_xy}")

    path = [goal]
    while path[-1] != start:
        path.append(came_from[path[-1]])
    path.reverse()
    return [Vector((xs[ix], ys[iy], z[(ix, iy)] + 2.0)) for ix, iy in path]


def route_metrics(points):
    grades = []
    length = 0.0
    for a, b in zip(points, points[1:]):
        delta = b - a
        horizontal = math.hypot(delta.x, delta.y)
        grade = math.degrees(math.atan2(abs(delta.z), horizontal)) if horizontal > 1e-6 else 90.0
        grades.append(grade)
        length += delta.length
    p95 = sorted(grades)[max(0, math.ceil(len(grades) * 0.95) - 1)]
    return length, max(grades), p95


def route_curve(name, points, collection, material):
    curve = bpy.data.curves.new(name + "_CURVE", "CURVE")
    curve.dimensions = "3D"
    curve.resolution_u = 1
    curve.bevel_depth = 0.65
    curve.bevel_resolution = 2
    spline = curve.splines.new("POLY")
    spline.points.add(len(points) - 1)
    for bp, point in zip(spline.points, points):
        bp.co = (*point, 1.0)
    obj = bpy.data.objects.new(name, curve)
    collection.objects.link(obj)
    if material:
        curve.materials.append(material)
    return obj


def collision_ribbon(name, points, collection):
    half = COLLISION_WIDTH_M / 2.0
    verts = []
    for i, point in enumerate(points):
        previous = points[max(0, i - 1)]
        following = points[min(len(points) - 1, i + 1)]
        tangent = following - previous
        tangent.z = 0.0
        if tangent.length < 1e-6:
            tangent = Vector((1, 0, 0))
        tangent.normalize()
        lateral = Vector((-tangent.y, tangent.x, 0)).normalized()
        top = point + Vector((0, 0, -0.2))
        bottom = top - Vector((0, 0, COLLISION_THICKNESS_M))
        verts.extend(
            [
                tuple(top - lateral * half),
                tuple(top + lateral * half),
                tuple(bottom - lateral * half),
                tuple(bottom + lateral * half),
            ]
        )

    faces = []
    for i in range(len(points) - 1):
        a = 4 * i
        b = 4 * (i + 1)
        faces.extend(
            [
                (a, a + 1, b + 1, b),
                (a + 2, b + 2, b + 3, a + 3),
                (a, b, b + 2, a + 2),
                (a + 1, a + 3, b + 3, b + 1),
            ]
        )
    faces.append((0, 2, 3, 1))
    end = 4 * (len(points) - 1)
    faces.append((end, end + 1, end + 3, end + 2))

    mesh = bpy.data.meshes.new(name + "_R10_MESH")
    mesh.from_pydata(verts, [], faces)
    mesh.update(calc_edges=True)
    if mesh.validate(clean_customdata=False, verbose=False):
        raise RuntimeError(f"{name}: Blender validate had to repair generated mesh")

    bm = bmesh.new()
    bm.from_mesh(mesh)
    nonmanifold = [edge.index for edge in bm.edges if not edge.is_manifold]
    degenerate = [face.index for face in bm.faces if face.calc_area() <= 1e-8]
    bm.free()
    if nonmanifold or degenerate:
        raise RuntimeError(f"{name}: topology invalid nonmanifold={nonmanifold} degenerate={degenerate}")

    obj = bpy.data.objects.new(name, mesh)
    collection.objects.link(obj)
    obj.display_type = "WIRE"
    obj.hide_render = True
    return obj


def build():
    xs, ys, z = terrain_grid()
    collection = bpy.data.collections["SYLVA_60_SCALE_TRAVERSAL"]
    material = bpy.data.materials.get("SYLVA_DIAG_RefugeSignal") or bpy.data.materials.get("SYLVA_DIAG_MemorySignal")

    anchors = [
        (-3200.0, -2200.0),
        (-1800.0, -900.0),
        (0.0, 150.0),
        (1650.0, 1150.0),
        (3200.0, 2300.0),
    ]

    solved = [solve(xs, ys, z, anchors[i], anchors[i + 1]) for i in range(4)]

    # Better authored entry/exit connections while retaining solved interior grid path.
    solved[0][0] = Vector((-3200.0, -2200.0, 370.0))
    bosque = Vector((0.0, 150.0, 352.0))
    solved[1].append(bosque)
    solved[2][0] = bosque
    terrace = bpy.data.objects.get("SYLVA_VESPER_Terrace_00_ENTRY")
    if terrace:
        solved[3][-1] = Vector((terrace.location.x, terrace.location.y, terrace.location.z + terrace.dimensions.z / 2.0))

    rows = []
    for index, points in enumerate(solved):
        route_name = f"SYLVA_TRAV_PathGuide_{index:02d}"
        collision_name = f"SYLVA_COL_ROUTE_{index:02d}"
        for old_name in (route_name, collision_name):
            old = bpy.data.objects.get(old_name)
            if old:
                bpy.data.objects.remove(old, do_unlink=True)

        length, max_grade, p95 = route_metrics(points)
        route = route_curve(route_name, points, collection, material)
        route["diagnostic_width_m"] = ROUTE_CLEAR_WIDTH_M
        route["final_geometry"] = False
        route["route_profile"] = PROFILE
        route["classification"] = "PROPOSAL_NAVIGATION_CENTERLINE"
        route["length_m"] = round(length, 3)
        route["max_grade_deg"] = round(max_grade, 3)
        route["p95_grade_deg"] = round(p95, 3)
        route["solver"] = SOLVER
        route["movement_mode"] = "UNASSIGNED_BASELINE"

        collision = collision_ribbon(collision_name, points, collection)
        collision["owner_claim"] = CLAIM
        collision["classification"] = "COLLISION_PROXY"
        collision["collision_policy"] = "TERRAIN_AWARE_RIBBON_PROXY_MANIFOLD_R10"
        collision["source"] = route_name
        collision["clear_width_m"] = ROUTE_CLEAR_WIDTH_M
        collision["ribbon_width_m"] = COLLISION_WIDTH_M
        collision["thickness_m"] = COLLISION_THICKNESS_M
        collision["route_profile"] = PROFILE

        rows.append(
            {
                "leg": index,
                "length_m": round(length, 3),
                "max_grade_deg": round(max_grade, 3),
                "p95_grade_deg": round(p95, 3),
                "segments": len(points) - 1,
            }
        )

    meta = bpy.data.objects.get("SYLVA_META_NavigationRouteContract")
    if meta is None:
        meta = bpy.data.objects.new("SYLVA_META_NavigationRouteContract", None)
        bpy.data.collections["SYLVA_00_META"].objects.link(meta)
    meta["classification"] = "PROPOSAL_ROUTE_INTERFACE"
    meta["version"] = "SYLVA_NAV_R10"
    meta["route_count"] = 4
    meta["movement_mode"] = "UNASSIGNED_BASELINE"
    meta["terrain_model"] = "R6_BIOGEO_CAUSAL_MACRO_V1"
    meta["solver"] = SOLVER
    meta["hard_max_grade_deg"] = HARD_MAX_GRADE_DEG
    meta["final_route_geometry"] = False
    meta["total_length_m"] = round(sum(row["length_m"] for row in rows), 3)
    meta["max_leg_grade_deg"] = max(row["max_grade_deg"] for row in rows)
    meta["route_collision_topology"] = "MANIFOLD_RIBBON_R10"

    root = bpy.data.objects.get("SYLVA_WORLD_ROOT")
    if root:
        root["build_status"] = "WAVE1H_ROUTE_COLLISION_TOPOLOGY_R10"
        root["navigation_route_contract"] = "SYLVA_NAV_R10"
        root["route_collision_contract"] = "MANIFOLD_RIBBON_R10"

    return rows


if __name__ == "__main__":
    print(build())
