"""EXOVANT 2950 — LEVIATHAN stable traversal ribbon v1.

Corrects a measured foundation defect without making deforming visual tissue the collision
authority. The existing organic visual route is a 6 m-radius curve whose eight stable pads
have 32-42 m plan gaps. This stage adds one continuous 8 m-wide stable mesh ribbon inside
that visual tube and a short visual+stable ingress to the north edge of the 58 m SOMA arena.

The 8 m width is a production proposal, not final gameplay canon. It is derived to fit inside
the worst measured visual-tube chord at z=5 (>=10.39 m) while giving generous clearance to
the 0.55 m human reference. Runtime capsule/nav validation remains required.

Claim: CLM-W10-WORLD-LEVIATHAN-001
Existing asset interfaces only: LEV-ENV-001 stable substrate / LEV-ENV-003 cartilage route.
"""

import bpy
import math
from mathutils import Vector

STAGE = "STABLE_TRAVERSAL_RIBBON_V1"
RIBBON_WIDTH_M = 8.0
RIBBON_THICKNESS_M = 0.5
MAIN_TOP_Z_M = 5.0
ARENA_TOP_Z_M = 7.0
SAMPLES_PER_BEZIER_SEGMENT = 8


def _bezier(p0, p1, p2, p3, t):
    u = 1.0 - t
    return p0 * (u ** 3) + p1 * (3.0 * u * u * t) + p2 * (3.0 * u * t * t) + p3 * (t ** 3)


def _sample_visual_path(path):
    spline = path.data.splines[0]
    if spline.type != "BEZIER" or len(spline.bezier_points) < 2:
        raise RuntimeError("Expected TRAVERSAL_MAIN_ORGANIC_PATH as non-empty Bezier spline")
    pts = []
    bp = spline.bezier_points
    for i in range(len(bp) - 1):
        a, b = bp[i], bp[i + 1]
        for j in range(SAMPLES_PER_BEZIER_SEGMENT):
            if i and j == 0:
                continue
            t = j / SAMPLES_PER_BEZIER_SEGMENT
            local = _bezier(a.co, a.handle_right, b.handle_left, b.co, t)
            world = path.matrix_world @ local
            pts.append(Vector((world.x, world.y, MAIN_TOP_Z_M)))
    end = path.matrix_world @ bp[-1].co
    pts.append(Vector((end.x, end.y, MAIN_TOP_Z_M)))
    return pts


def _append_soma_ingress(points):
    arena = bpy.data.objects.get("R3_ARENA_STABLE_FLOOR")
    if arena is None:
        raise RuntimeError("R3_ARENA_STABLE_FLOOR missing")
    # Arena north edge is y = center_y + half_y = -46 m in the current 58 m canonical shell.
    edge_y = float(arena.location.y + arena.dimensions.y / 2.0)
    x = float(points[-1].x)
    start = points[-1]
    # Two deterministic ramp points produce a mild 2 m rise across the ~26 m ingress.
    mid = Vector((x, (start.y + edge_y) * 0.5, (MAIN_TOP_Z_M + ARENA_TOP_Z_M) * 0.5))
    end = Vector((x, edge_y - 1.0, ARENA_TOP_Z_M))  # 1 m overlap inside arena footprint.
    points.extend([mid, end])
    return edge_y


def _ribbon_mesh(points, width, thickness):
    half = width / 2.0
    top_left = []
    top_right = []
    for i, p in enumerate(points):
        if i == 0:
            tangent = points[1] - points[0]
        elif i == len(points) - 1:
            tangent = points[-1] - points[-2]
        else:
            tangent = points[i + 1] - points[i - 1]
        tangent.z = 0.0
        if tangent.length < 1e-6:
            raise RuntimeError(f"Degenerate route tangent at point {i}")
        tangent.normalize()
        normal = Vector((-tangent.y, tangent.x, 0.0))
        top_left.append(p + normal * half)
        top_right.append(p - normal * half)

    verts = []
    for l, r in zip(top_left, top_right):
        verts.extend([tuple(l), tuple(r), tuple(l - Vector((0, 0, thickness))), tuple(r - Vector((0, 0, thickness)))])

    faces = []
    # top/bottom and side walls per strip segment
    for i in range(len(points) - 1):
        a = i * 4
        b = (i + 1) * 4
        faces.extend([
            (a + 0, b + 0, b + 1, a + 1),
            (a + 2, a + 3, b + 3, b + 2),
            (a + 0, a + 2, b + 2, b + 0),
            (a + 1, b + 1, b + 3, a + 3),
        ])
    # end caps
    faces.extend([(0, 1, 3, 2), (len(verts)-4, len(verts)-2, len(verts)-1, len(verts)-3)])
    return verts, faces


def build():
    scene = bpy.context.scene
    root = bpy.data.collections.get("LEV_W10_MASTER")
    collision_collection = bpy.data.collections.get("40_COLLISION_PROXY")
    visual_parent = bpy.data.collections.get("10_L2_WORLD_CELL")
    path = bpy.data.objects.get("TRAVERSAL_MAIN_ORGANIC_PATH")
    arena = bpy.data.objects.get("R3_ARENA_STABLE_FLOOR")
    human = bpy.data.objects.get("REF_HUMAN_1P85M")
    if not all([root, collision_collection, visual_parent, path, arena, human]):
        raise RuntimeError("Required LEVIATHAN master route objects/collections missing")

    # Idempotent cleanup.
    for name in ["COLL_MAIN_ORGANIC_ROUTE_RIBBON", "TRAVERSAL_R3_INGRESS_VISUAL"]:
        old = bpy.data.objects.get(name)
        if old:
            bpy.data.objects.remove(old, do_unlink=True)
    old_col = bpy.data.collections.get("27_TRAVERSAL_INGRESS_FIX")
    if old_col:
        for obj in list(old_col.all_objects):
            bpy.data.objects.remove(obj, do_unlink=True)
        bpy.data.collections.remove(old_col)

    debug = bpy.data.materials.get("DEBUG_COLLISION_STABLE")
    cartilage = bpy.data.materials.get("LEV_MAT_CARTILAGE")
    if debug is None or cartilage is None:
        raise RuntimeError("Required route materials missing")

    points = _sample_visual_path(path)
    visual_endpoint = points[-1].copy()
    arena_north_edge_y = _append_soma_ingress(points)

    verts, faces = _ribbon_mesh(points, RIBBON_WIDTH_M, RIBBON_THICKNESS_M)
    mesh = bpy.data.meshes.new("COLL_MAIN_ORGANIC_ROUTE_RIBBON_MESH")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    ribbon = bpy.data.objects.new("COLL_MAIN_ORGANIC_ROUTE_RIBBON", mesh)
    collision_collection.objects.link(ribbon)
    mesh.materials.append(debug)
    ribbon["asset_id"] = "LEV-ENV-001"
    ribbon["collision_role"] = "STABLE_CONTINUOUS_ORGANIC_ROUTE_RIBBON"
    ribbon["width_m"] = RIBBON_WIDTH_M
    ribbon["thickness_m"] = RIBBON_THICKNESS_M
    ribbon["route_width_status"] = "PROPOSAL_DERIVED_FROM_VISUAL_TUBE_CLEARANCE"
    ribbon["human_width_multiple"] = round(RIBBON_WIDTH_M / float(human.dimensions.x), 4)
    ribbon["main_top_z_m"] = MAIN_TOP_Z_M
    ribbon["arena_ingress_top_z_m"] = ARENA_TOP_Z_M
    ribbon["visual_tissue_collision_authority"] = "NONE"
    ribbon["generator_stage"] = STAGE

    # Visual connector from the existing tube endpoint to the arena edge. It remains visual-only.
    visual_col = bpy.data.collections.new("27_TRAVERSAL_INGRESS_FIX")
    root.children.link(visual_col)
    curve = bpy.data.curves.new("TRAVERSAL_R3_INGRESS_VISUAL_CURVE", "CURVE")
    curve.dimensions = "3D"
    curve.resolution_u = 4
    curve.bevel_depth = 6.0
    curve.bevel_resolution = 3
    spline = curve.splines.new("BEZIER")
    spline.bezier_points.add(2)
    visual_points = [
        Vector((visual_endpoint.x, visual_endpoint.y, 8.0)),
        Vector((visual_endpoint.x, (visual_endpoint.y + arena_north_edge_y) * 0.5, 9.0)),
        Vector((visual_endpoint.x, arena_north_edge_y - 1.0, 10.0)),
    ]
    for bp, co in zip(spline.bezier_points, visual_points):
        bp.co = co
        bp.handle_left_type = "AUTO"
        bp.handle_right_type = "AUTO"
    connector = bpy.data.objects.new("TRAVERSAL_R3_INGRESS_VISUAL", curve)
    visual_col.objects.link(connector)
    curve.materials.append(cartilage)
    connector["asset_id"] = "LEV-ENV-003"
    connector["production_state"] = "REPRESENTATIVE_ROUTE_CONNECTOR_NOT_FINAL"
    connector["collision_authority"] = "NONE_VISUAL_ONLY"
    connector["generator_stage"] = STAGE

    scene["stable_traversal_ribbon_stage"] = STAGE
    scene["stable_traversal_ribbon_width_m"] = RIBBON_WIDTH_M
    scene["stable_traversal_ribbon_final_gameplay_width_claimed"] = False

    mesh.calc_loop_triangles()
    return {
        "stage": STAGE,
        "route_samples": len(points),
        "ribbon_vertices": len(mesh.vertices),
        "ribbon_triangles": len(mesh.loop_triangles),
        "ribbon_width_m": RIBBON_WIDTH_M,
        "ribbon_top_z_range_m": [min(p.z for p in points), max(p.z for p in points)],
        "human_width_multiple": round(RIBBON_WIDTH_M / float(human.dimensions.x), 4),
        "arena_north_edge_y_m": arena_north_edge_y,
        "visual_connector_radius_m": curve.bevel_depth,
        "status": "STATIC_CONTINUITY_FIX_NOT_RUNTIME_QUALIFIED",
    }


if __name__ == "__main__":
    print(build())
