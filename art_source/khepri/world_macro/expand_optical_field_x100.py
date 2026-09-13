"""EXOVANT 2950 / KHEPRI — X100 systemic optical-field family generator.

Claim: CLM-KHEPRI-WMACRO-001
Family asset: KHP_WM_HELIOSTAT_FOOTPRINTS

This is a macro-footprint/systemic family, not final close-range heliostat architecture.
It upgrades one fixed 8x4 proxy field into a deterministic configurable family while keeping
variation causal and reversible. The default authored scene is OPERATIONAL_MAINTENANCE only;
damage/abandonment profiles are explicit PROPOSAL_QA modes and are never injected randomly.

The module runs a Blender-independent audit when bpy is unavailable. In Blender it applies the
default representative configuration. All coordinates are metres in the existing KHEPRI local
tangent cell.
"""
from __future__ import annotations

import json
import math

try:
    import bpy  # type: ignore
except ImportError:  # normal CI / contract audit
    bpy = None

FAMILY_ASSET_ID = "KHP_WM_HELIOSTAT_FOOTPRINTS"
TERRAIN_MODEL = "KHP_TERRAIN_V1"
CONTRACT_VERSION = "KHP_OPTICAL_FIELD_X100_V1"
ROUTE_CLEARANCE_M = 140.0
ANCHOR_CLEARANCE_M = 220.0
TILE_MARGIN_M = 350.0
MAX_SLOPE_DEG = 14.0

ANCHORS = [
    (-2300.0, 900.0),
    (-450.0, -140.0),
    (1250.0, -650.0),
    (2550.0, 650.0),
]

SCALE_VARIANTS = {
    "compact": {"mast_h": 28.0, "mast_w": 3.6, "panel_w": 28.0, "panel_h": 17.0, "panel_t": 1.6, "gap": 5.0},
    "standard": {"mast_h": 36.0, "mast_w": 4.8, "panel_w": 36.0, "panel_h": 22.0, "panel_t": 2.0, "gap": 6.0},
    "wide": {"mast_h": 44.0, "mast_w": 5.6, "panel_w": 46.0, "panel_h": 26.0, "panel_t": 2.2, "gap": 7.0},
}
LAYOUTS = ("staggered_bands", "aligned_lattice", "diagonal_bands", "radial_fan")
DENSITIES = {
    "sparse": (10, 7),
    "production": (14, 9),
    "dense": (18, 11),
}
CORRIDOR_PATTERNS = ("dual_ns", "single_ns", "cross")
STATE_PROFILES = ("operational", "maintenance_cycle", "damage_proxy", "abandonment_proxy")
SCALE_MIXES = ("balanced", "compact_bias", "standard_bias")

DEFAULT_CONFIG = {
    "layout": "staggered_bands",
    "density": "production",
    "corridor": "dual_ns",
    "state_profile": "maintenance_cycle",
    "scale_mix": "balanced",
}


def terrain_height(x_m: float, y_m: float) -> float:
    broad = 74.0 * math.sin(x_m / 890.0) * math.cos(y_m / 730.0)
    secondary = 31.0 * math.sin((x_m + 0.37 * y_m) / 370.0)
    tertiary = 13.0 * math.cos((0.28 * x_m - y_m) / 210.0)
    glass_sea_basin = -58.0 * math.exp(-((y_m + 180.0) / 620.0) ** 2)
    crucible_shelf = 44.0 * math.exp(-(((x_m - 1250.0) / 900.0) ** 2 + ((y_m + 650.0) / 780.0) ** 2))
    return broad + secondary + tertiary + glass_sea_basin + crucible_shelf


def slope_deg(x_m: float, y_m: float, eps: float = 1.0) -> float:
    dzdx = (terrain_height(x_m + eps, y_m) - terrain_height(x_m - eps, y_m)) / (2.0 * eps)
    dzdy = (terrain_height(x_m, y_m + eps) - terrain_height(x_m, y_m - eps)) / (2.0 * eps)
    return math.degrees(math.atan(math.hypot(dzdx, dzdy)))


def _dist_segment_2d(px, py, a, b):
    ax, ay = a
    bx, by = b
    vx, vy = bx - ax, by - ay
    wx, wy = px - ax, py - ay
    vv = vx * vx + vy * vy
    t = 0.0 if vv <= 1e-12 else max(0.0, min(1.0, (wx * vx + wy * vy) / vv))
    return math.hypot(px - (ax + t * vx), py - (ay + t * vy))


def route_distance(x, y):
    return min(_dist_segment_2d(x, y, ANCHORS[i], ANCHORS[i + 1]) for i in range(len(ANCHORS) - 1))


def anchor_distance(x, y):
    return min(math.hypot(x - ax, y - ay) for ax, ay in ANCHORS)


def corridor_blocked(x, y, pattern):
    if pattern == "dual_ns":
        return min(abs(x + 900.0), abs(x - 900.0)) < 90.0
    if pattern == "single_ns":
        return abs(x) < 110.0
    if pattern == "cross":
        return abs(x) < 90.0 or abs(y + 350.0) < 90.0
    raise ValueError(pattern)


def scale_variant(index: int, mix: str) -> str:
    if mix == "balanced":
        return ("compact", "standard", "wide", "standard", "standard")[index % 5]
    if mix == "compact_bias":
        return ("compact", "compact", "standard", "compact", "wide")[index % 5]
    if mix == "standard_bias":
        return ("standard", "standard", "standard", "compact", "wide")[index % 5]
    raise ValueError(mix)


def state_variant(index: int, profile: str) -> str:
    if profile == "operational":
        return "operational"
    if profile == "maintenance_cycle":
        return "maintenance" if index % 8 == 0 else "operational"
    if profile == "damage_proxy":
        if index % 13 == 0:
            return "damaged"
        return "maintenance" if index % 7 == 0 else "operational"
    if profile == "abandonment_proxy":
        if index % 5 == 0:
            return "abandoned"
        if index % 7 == 0:
            return "damaged"
        return "maintenance" if index % 3 == 0 else "operational"
    raise ValueError(profile)


def raw_candidates(config):
    cols, rows = DENSITIES[config["density"]]
    xmin, xmax = -3200.0 + TILE_MARGIN_M, 3200.0 - TILE_MARGIN_M
    ymin, ymax = -2400.0 + TILE_MARGIN_M, 2400.0 - TILE_MARGIN_M
    dx = (xmax - xmin) / (cols - 1)
    dy = (ymax - ymin) / (rows - 1)
    layout = config["layout"]
    out = []
    if layout in {"staggered_bands", "aligned_lattice", "diagonal_bands"}:
        for row in range(rows):
            y = ymin + row * dy
            if layout == "staggered_bands":
                offset = dx * 0.5 if row % 2 else 0.0
            elif layout == "diagonal_bands":
                offset = (row % 4) * dx * 0.22
            else:
                offset = 0.0
            for col in range(cols):
                x = xmin + col * dx + offset
                if x <= xmax:
                    out.append((x, y, row, col))
    elif layout == "radial_fan":
        # Deterministic macro fan around the energy/industrial side of the representative cell.
        rings = rows
        sectors = cols
        cx, cy = 700.0, -650.0
        for ring in range(rings):
            radius = 650.0 + ring * (1650.0 / max(1, rings - 1))
            for sector in range(sectors):
                angle = math.radians(-150.0 + sector * (300.0 / max(1, sectors - 1)))
                x = cx + radius * math.cos(angle)
                y = cy + radius * math.sin(angle)
                if xmin <= x <= xmax and ymin <= y <= ymax:
                    out.append((x, y, ring, sector))
    else:
        raise ValueError(layout)
    return out


def placements(config=None):
    config = dict(DEFAULT_CONFIG if config is None else config)
    accepted = []
    for x, y, row, col in raw_candidates(config):
        if route_distance(x, y) < ROUTE_CLEARANCE_M:
            continue
        if anchor_distance(x, y) < ANCHOR_CLEARANCE_M:
            continue
        if corridor_blocked(x, y, config["corridor"]):
            continue
        if slope_deg(x, y) > MAX_SLOPE_DEG:
            continue
        accepted.append((x, y, row, col))
    # Stable spatial ordering makes object IDs deterministic across cold rebuilds.
    accepted.sort(key=lambda item: (round(item[1], 6), round(item[0], 6), item[2], item[3]))
    result = []
    for index, (x, y, row, col) in enumerate(accepted):
        variant = scale_variant(index, config["scale_mix"])
        state = state_variant(index, config["state_profile"])
        # Tracking is explicitly a visual proxy, not a solved heliostat optical equation.
        yaw = max(-22.0, min(22.0, x / 130.0))
        tilt = 12.0 + 2.5 * math.sin(y / 640.0)
        result.append({
            "index": index,
            "x": x,
            "y": y,
            "z": terrain_height(x, y),
            "slope_deg": slope_deg(x, y),
            "route_clearance_m": route_distance(x, y),
            "anchor_clearance_m": anchor_distance(x, y),
            "scale_variant": variant,
            "state": state,
            "yaw_deg": yaw,
            "tilt_deg": tilt,
        })
    return result


def configuration_count():
    return len(LAYOUTS) * len(DENSITIES) * len(CORRIDOR_PATTERNS) * len(STATE_PROFILES) * len(SCALE_MIXES)


def audit_contract():
    default = placements(DEFAULT_CONFIG)
    all_counts = []
    for layout in LAYOUTS:
        for density in DENSITIES:
            for corridor in CORRIDOR_PATTERNS:
                for state_profile in STATE_PROFILES:
                    for scale_mix in SCALE_MIXES:
                        cfg = {"layout": layout, "density": density, "corridor": corridor, "state_profile": state_profile, "scale_mix": scale_mix}
                        all_counts.append(len(placements(cfg)))
    checks = {
        "production_grade_configuration_space": configuration_count() >= 100,
        "default_density_has_at_least_96_units": len(default) >= 96,
        "default_route_clearance": min(p["route_clearance_m"] for p in default) >= ROUTE_CLEARANCE_M,
        "default_anchor_clearance": min(p["anchor_clearance_m"] for p in default) >= ANCHOR_CLEARANCE_M,
        "default_slope_limit": max(p["slope_deg"] for p in default) <= MAX_SLOPE_DEG,
        "all_configurations_nonempty": min(all_counts) > 0,
    }
    return {
        "contract": CONTRACT_VERSION,
        "family_asset_id": FAMILY_ASSET_ID,
        "configuration_count": configuration_count(),
        "implemented_axes": {
            "layouts": list(LAYOUTS),
            "densities": list(DENSITIES),
            "corridors": list(CORRIDOR_PATTERNS),
            "state_profiles": list(STATE_PROFILES),
            "scale_mixes": list(SCALE_MIXES),
        },
        "default_config": dict(DEFAULT_CONFIG),
        "default_instances": len(default),
        "all_config_instance_range": [min(all_counts), max(all_counts)],
        "checks": checks,
        "passed": all(checks.values()),
        "boundary": "Macro systemic footprint family only; final close-range architecture, collision and optical physics remain downstream claims.",
    }


def _append_box(verts, faces, mat_indices, center, dims, mat_index=0):
    cx, cy, cz = center
    dx, dy, dz = [d * 0.5 for d in dims]
    base = len(verts)
    verts.extend([
        (cx-dx, cy-dy, cz-dz), (cx+dx, cy-dy, cz-dz),
        (cx+dx, cy+dy, cz-dz), (cx-dx, cy+dy, cz-dz),
        (cx-dx, cy-dy, cz+dz), (cx+dx, cy-dy, cz+dz),
        (cx+dx, cy+dy, cz+dz), (cx-dx, cy+dy, cz+dz),
    ])
    quads = [(0,1,2,3),(4,7,6,5),(0,4,5,1),(1,5,6,2),(2,6,7,3),(4,0,3,7)]
    for q in quads:
        faces.append(tuple(base+i for i in q))
        mat_indices.append(mat_index)


def _make_mast_mesh(name, spec, bronze):
    verts, faces, mats = [], [], []
    h, w = spec["mast_h"], spec["mast_w"]
    _append_box(verts, faces, mats, (0,0,-h*0.45), (w*1.45,w*1.45,h*0.10), 0)
    _append_box(verts, faces, mats, (0,0,0), (w,w,h*0.82), 0)
    _append_box(verts, faces, mats, (0,0,h*0.45), (w*1.15,w*1.15,h*0.08), 0)
    mesh=bpy.data.meshes.new(name)
    mesh.from_pydata(verts, [], faces); mesh.update()
    mesh.materials.append(bronze)
    for poly, mi in zip(mesh.polygons, mats): poly.material_index=mi
    return mesh


def _make_panel_mesh(name, spec, mirror, bronze):
    verts, faces, mats = [], [], []
    w,h,t = spec["panel_w"], spec["panel_h"], spec["panel_t"]
    _append_box(verts, faces, mats, (0,0,0), (w,t,h), 0)
    # Back spine and hub make the macro silhouette read as engineered hardware, not a floating slab.
    _append_box(verts, faces, mats, (0,-t*0.70,0), (w*0.72,t*0.42,max(0.9,h*0.055)), 1)
    _append_box(verts, faces, mats, (0,-t*0.78,0), (max(3.0,w*0.10),t*0.55,max(3.0,h*0.17)), 1)
    mesh=bpy.data.meshes.new(name)
    mesh.from_pydata(verts, [], faces); mesh.update()
    mesh.materials.append(mirror); mesh.materials.append(bronze)
    for poly, mi in zip(mesh.polygons, mats): poly.material_index=mi
    return mesh


def apply_to_blender(config=None):
    if bpy is None:
        raise RuntimeError("Blender bpy unavailable")
    config = dict(DEFAULT_CONFIG if config is None else config)
    field = placements(config)
    if len(field) < 96:
        raise RuntimeError(f"X100 default field unexpectedly sparse: {len(field)}")
    collection = bpy.data.collections.get("KHP_WM_30_OPTICAL_FOOTPRINTS")
    if collection is None:
        raise RuntimeError("missing KHP_WM_30_OPTICAL_FOOTPRINTS")
    bronze = bpy.data.materials.get("KHP_WM_MAT_BRONZE_BLOCKOUT")
    mirror = bpy.data.materials.get("KHP_WM_MAT_MIRROR_BLOCKOUT")
    if bronze is None or mirror is None:
        raise RuntimeError("missing KHEPRI optical materials")

    # Replace only owned footprint instances and prior X100 family metadata.
    for obj in list(collection.objects):
        if obj.name.startswith("KHP_WM_HELIOSTAT_") or obj.name == "KHP_WM_OPTICAL_FIELD_SYSTEM_META":
            bpy.data.objects.remove(obj, do_unlink=True)
    for mesh in list(bpy.data.meshes):
        if mesh.users == 0 and (mesh.name.startswith("KHP_WM_X100_MAST_") or mesh.name.startswith("KHP_WM_X100_PANEL_") or mesh.name.startswith("KHP_WM_SHARED_HELIOSTAT_")):
            bpy.data.meshes.remove(mesh)

    mast_meshes = {}
    panel_meshes = {}
    for variant, spec in SCALE_VARIANTS.items():
        mast_meshes[variant] = _make_mast_mesh(f"KHP_WM_X100_MAST_{variant.upper()}", spec, bronze)
        panel_meshes[variant] = _make_panel_mesh(f"KHP_WM_X100_PANEL_{variant.upper()}", spec, mirror, bronze)

    counts = {"operational":0,"maintenance":0,"damaged":0,"abandoned":0}
    for item in field:
        i=item["index"]; variant=item["scale_variant"]; state=item["state"]; spec=SCALE_VARIANTS[variant]
        ground=item["z"]
        mast=bpy.data.objects.new(f"KHP_WM_HELIOSTAT_MAST_{i:03d}", mast_meshes[variant])
        mast.location=(item["x"],item["y"],ground+spec["mast_h"]*0.5)
        collection.objects.link(mast)
        mast["exovant_asset_id"]=f"KHP_WM_HEL_MAST_{i:03d}"
        mast["family_asset_id"]=FAMILY_ASSET_ID
        mast["variant_id"]=variant
        mast["state"]=state
        mast["role"]="heliostat_footprint_mast"
        mast["world_id"]="khepri"; mast["claim_id"]="CLM-KHEPRI-WMACRO-001"
        mast["epistemic"]="PROPOSAL_SYSTEMIC_PROXY"; mast["proxy_only"]=True

        # Abandoned proxy intentionally omits a mounted panel; damaged keeps one visibly misaligned.
        if state != "abandoned":
            panel=bpy.data.objects.new(f"KHP_WM_HELIOSTAT_PANEL_{i:03d}", panel_meshes[variant])
            if state == "damaged":
                panel.location=(item["x"],item["y"],ground+spec["mast_h"]+spec["gap"]-3.0)
                panel.rotation_euler=(math.radians(item["tilt_deg"]+18.0),math.radians(7.0),math.radians(item["yaw_deg"]+14.0))
            elif state == "maintenance":
                panel.location=(item["x"],item["y"],ground+spec["mast_h"]+spec["gap"])
                panel.rotation_euler=(math.radians(72.0),0.0,math.radians(item["yaw_deg"]))
            else:
                panel.location=(item["x"],item["y"],ground+spec["mast_h"]+spec["gap"])
                panel.rotation_euler=(math.radians(item["tilt_deg"]),0.0,math.radians(item["yaw_deg"]))
            collection.objects.link(panel)
            panel["exovant_asset_id"]=f"KHP_WM_HEL_PANEL_{i:03d}"
            panel["family_asset_id"]=FAMILY_ASSET_ID
            panel["variant_id"]=variant; panel["state"]=state
            panel["role"]="heliostat_footprint_panel"
            panel["world_id"]="khepri"; panel["claim_id"]="CLM-KHEPRI-WMACRO-001"
            panel["epistemic"]="PROPOSAL_SYSTEMIC_PROXY"; panel["proxy_only"]=True
            panel["tracking_contract"]="PROXY_ORIENTATION_NOT_OPTICAL_SOLUTION"
        counts[state]+=1

    meta=bpy.data.objects.new("KHP_WM_OPTICAL_FIELD_SYSTEM_META", None)
    collection.objects.link(meta)
    meta["family_asset_id"]=FAMILY_ASSET_ID
    meta["role"]="systemic_family_metadata"
    meta["contract"]=CONTRACT_VERSION
    meta["credible_configuration_count"]=configuration_count()
    meta["default_config_json"]=json.dumps(config,sort_keys=True)
    meta["placement_rules_json"]=json.dumps({"route_clearance_m":ROUTE_CLEARANCE_M,"anchor_clearance_m":ANCHOR_CLEARANCE_M,"tile_margin_m":TILE_MARGIN_M,"max_slope_deg":MAX_SLOPE_DEG},sort_keys=True)
    meta["state_epistemic"]="DAMAGE_AND_ABANDONMENT_MODES_ARE_PROPOSAL_QA_ONLY"
    meta["world_id"]="khepri"; meta["claim_id"]="CLM-KHEPRI-WMACRO-001"

    bpy.context.scene["khepri_optical_field_contract"]=CONTRACT_VERSION
    bpy.context.scene["khepri_optical_field_default_config"]=json.dumps(config,sort_keys=True)
    bpy.context.scene["khepri_optical_field_instance_count"]=len(field)
    bpy.context.scene["khepri_optical_field_configuration_count"]=configuration_count()

    return {
        "contract": CONTRACT_VERSION,
        "family_asset_id": FAMILY_ASSET_ID,
        "default_config": config,
        "instances": len(field),
        "state_counts": counts,
        "unique_mast_meshes": len(set(mast_meshes.values())),
        "unique_panel_meshes": len(set(panel_meshes.values())),
        "configuration_count": configuration_count(),
        "min_route_clearance_m": min(p["route_clearance_m"] for p in field),
        "min_anchor_clearance_m": min(p["anchor_clearance_m"] for p in field),
        "max_slope_deg": max(p["slope_deg"] for p in field),
        "terrain_model": TERRAIN_MODEL,
        "boundary": "Macro footprint/systemic family. No final close-range architecture, collision, PBR texture set, optical solve, human art approval or target-hardware qualification claimed."
    }


if __name__ == "__main__":
    if bpy is None:
        print(json.dumps(audit_contract(), indent=2, sort_keys=True))
    else:
        result = apply_to_blender()
        print(json.dumps(result, indent=2, sort_keys=True))
