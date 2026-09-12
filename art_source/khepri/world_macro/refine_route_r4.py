"""KHEPRI world-macro R4 route refinement.

Claim: CLM-KHEPRI-WMACRO-001
Purpose: replace the four-point straight 3D QA ribbon with a deterministic terrain-conforming
polyline. This remains an interface/QA guide, NOT navmesh, road geometry or final level design.

Precondition: run generate_khepri_world_macro.py, then optimize_khepri_world_macro.py.
Blender target: 5.2.x.
"""
import math
import bpy

ROUTE_OBJECT = "KHP_WM_ROUTE_GUIDE_ONLY"
ANCHOR_NAMES = [
    "KHP_WM_ROUTE_SHADE",
    "KHP_WM_ROUTE_GLASS_SEA",
    "KHP_WM_ROUTE_CRUCIBLE",
    "KHP_WM_ROUTE_RAKHET",
]
SAMPLE_SPACING_M = 10.0
CLEARANCE_M = 7.0


def terrain_height(x: float, y: float) -> float:
    return (
        74.0 * math.sin(x / 890.0) * math.cos(y / 730.0)
        + 31.0 * math.sin((x + 0.37 * y) / 370.0)
        + 13.0 * math.cos((0.28 * x - y) / 210.0)
        - 58.0 * math.exp(-((y + 180.0) / 620.0) ** 2)
        + 44.0 * math.exp(-(((x - 1250.0) / 900.0) ** 2 + ((y + 650.0) / 780.0) ** 2))
    )


route = bpy.data.objects.get(ROUTE_OBJECT)
if route is None or route.type != "CURVE":
    raise RuntimeError(f"Missing expected curve {ROUTE_OBJECT}; run KHEPRI generator first")

anchors = []
for name in ANCHOR_NAMES:
    obj = bpy.data.objects.get(name)
    if obj is None:
        raise RuntimeError(f"Missing route anchor {name}")
    anchors.append(obj)

points = []
segment_samples = []
for segment_index, (a, b) in enumerate(zip(anchors, anchors[1:])):
    dx = b.location.x - a.location.x
    dy = b.location.y - a.location.y
    horizontal_distance = math.hypot(dx, dy)
    sample_count = max(2, int(math.ceil(horizontal_distance / SAMPLE_SPACING_M)))
    segment_samples.append(sample_count + 1)
    for i in range(sample_count + 1):
        # Do not duplicate the first point of later segments.
        if segment_index > 0 and i == 0:
            continue
        t = i / sample_count
        x = a.location.x + dx * t
        y = a.location.y + dy * t
        z = terrain_height(x, y) + CLEARANCE_M
        points.append((x, y, z, 1.0))

curve = route.data
curve.splines.clear()
spline = curve.splines.new("POLY")
spline.points.add(len(points) - 1)
for index, point in enumerate(points):
    spline.points[index].co = point

route["route_refinement"] = "R4_TERRAIN_CONFORMING"
route["sample_spacing_m"] = SAMPLE_SPACING_M
route["target_clearance_m"] = CLEARANCE_M
route["point_count"] = len(points)
route["non_gameplay"] = True
bpy.context.scene["route_guide_contract"] = (
    "R4 terrain-conforming QA/interface polyline; 10m target sampling; 7m visual clearance; not navmesh"
)

result = {
    "route_object": route.name,
    "anchors": ANCHOR_NAMES,
    "point_count": len(points),
    "sample_spacing_m": SAMPLE_SPACING_M,
    "target_clearance_m": CLEARANCE_M,
    "segment_samples_including_endpoints": segment_samples,
    "status": "R4_TERRAIN_CONFORMING",
}
