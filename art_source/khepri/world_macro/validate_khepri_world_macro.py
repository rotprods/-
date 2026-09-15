"""Validation/audit script for KHEPRI world-macro scene.

Designed for Blender 5.2.x. Measures structure, scale and machine-readable camera composition.
It does not approve artistic quality, engine integration, collision or target-hardware performance.
"""
import json
import math
from collections import Counter

import bpy
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view

REQUIRED = [
    "KHP_WM_PLANET_META",
    "KHP_WM_L1_ORBITAL_PROXY_1_TO_20000",
    "KHP_WM_L2_MACROCELL_A_TERRAIN",
    "KHP_WM_ROUTE_SHADE",
    "KHP_WM_ROUTE_GLASS_SEA",
    "KHP_WM_ROUTE_CRUCIBLE",
    "KHP_WM_ROUTE_RAKHET",
    "KHP_WM_GUIDE_HUMAN_1P85M_BODY",
    "KHP_WM_GUIDE_HUMAN_1P85M_HEAD",
    "KHP_WM_CAM_OVERVIEW",
    "KHP_WM_CAM_GAMEPLAY_SCALE",
]
ANCHORS = [
    "KHP_WM_ROUTE_SHADE",
    "KHP_WM_ROUTE_GLASS_SEA",
    "KHP_WM_ROUTE_CRUCIBLE",
    "KHP_WM_ROUTE_RAKHET",
]

objects = list(bpy.data.objects)
meshes = list(bpy.data.meshes)
scene = bpy.context.scene
names = [obj.name for obj in objects]
asset_ids = [obj.get("exovant_asset_id") for obj in objects if obj.get("exovant_asset_id")]

missing = [name for name in REQUIRED if bpy.data.objects.get(name) is None]
duplicate_names = [name for name, count in Counter(names).items() if count > 1]
duplicate_asset_ids = [name for name, count in Counter(asset_ids).items() if count > 1]
nonfinite = []
negative_scale = []
nonunit_mesh_scale = []
for obj in objects:
    values = [*obj.location, *obj.rotation_euler, *obj.scale]
    if not all(math.isfinite(float(value)) for value in values):
        nonfinite.append(obj.name)
    if any(float(value) < 0 for value in obj.scale):
        negative_scale.append(obj.name)
    if obj.type == "MESH" and any(abs(float(value) - 1.0) > 1e-5 for value in obj.scale):
        nonunit_mesh_scale.append(obj.name)

terrain = bpy.data.objects.get("KHP_WM_L2_MACROCELL_A_TERRAIN")
body = bpy.data.objects.get("KHP_WM_GUIDE_HUMAN_1P85M_BODY")
head = bpy.data.objects.get("KHP_WM_GUIDE_HUMAN_1P85M_HEAD")
panels = [obj for obj in objects if obj.name.startswith("KHP_WM_HELIOSTAT_PANEL_")]
masts = [obj for obj in objects if obj.name.startswith("KHP_WM_HELIOSTAT_MAST_")]
overview = bpy.data.objects.get("KHP_WM_CAM_OVERVIEW")
gameplay = bpy.data.objects.get("KHP_WM_CAM_GAMEPLAY_SCALE")

terrain_dimensions = [round(float(value), 3) for value in terrain.dimensions] if terrain else None
human_height = None
if body and head:
    z_min = min((body.matrix_world @ Vector(corner)).z for corner in body.bound_box)
    z_max = max((head.matrix_world @ Vector(corner)).z for corner in head.bound_box)
    human_height = round(z_max - z_min, 3)

triangles = sum(sum(max(len(poly.vertices) - 2, 0) for poly in mesh.polygons) for mesh in meshes)
vertices = sum(len(mesh.vertices) for mesh in meshes)

# Machine-readable visual composition gates. These are not human art approval.
overview_anchor_metrics = {}
overview_all_in_frame = False
overview_all_within_clip = False
if overview:
    all_frame = []
    all_clip = []
    for name in ANCHORS:
        anchor = bpy.data.objects.get(name)
        if not anchor:
            continue
        ndc = world_to_camera_view(scene, overview, anchor.location)
        distance = (anchor.location - overview.location).length
        in_frame = 0.0 <= ndc.x <= 1.0 and 0.0 <= ndc.y <= 1.0 and ndc.z > 0.0
        within_clip = overview.data.clip_start <= distance <= overview.data.clip_end
        overview_anchor_metrics[name] = {
            "ndc": [round(ndc.x, 4), round(ndc.y, 4), round(ndc.z, 4)],
            "distance_m": round(distance, 2),
            "in_frame": in_frame,
            "within_clip": within_clip,
        }
        all_frame.append(in_frame)
        all_clip.append(within_clip)
    overview_all_in_frame = len(all_frame) == len(ANCHORS) and all(all_frame)
    overview_all_within_clip = len(all_clip) == len(ANCHORS) and all(all_clip)

guide_bbox_ndc = None
guide_projected_height_px = None
guide_in_gameplay_frame = False
if gameplay and body and head:
    points = []
    for obj in (body, head):
        for corner in obj.bound_box:
            points.append(world_to_camera_view(scene, gameplay, obj.matrix_world @ Vector(corner)))
    visible = [point for point in points if point.z > 0.0]
    if visible:
        min_x = min(point.x for point in visible)
        min_y = min(point.y for point in visible)
        max_x = max(point.x for point in visible)
        max_y = max(point.y for point in visible)
        guide_bbox_ndc = [round(min_x, 4), round(min_y, 4), round(max_x, 4), round(max_y, 4)]
        guide_in_gameplay_frame = 0.0 <= min_x and max_x <= 1.0 and 0.0 <= min_y and max_y <= 1.0
        guide_projected_height_px = round((max_y - min_y) * scene.render.resolution_y * scene.render.resolution_percentage / 100.0, 1)

checks = {
    "required_objects_present": not missing,
    "metric_units": scene.unit_settings.system == "METRIC" and abs(scene.unit_settings.scale_length - 1.0) < 1e-8,
    "duplicate_object_names_zero": not duplicate_names,
    "duplicate_asset_ids_zero": not duplicate_asset_ids,
    "nonfinite_transforms_zero": not nonfinite,
    "negative_scale_zero": not negative_scale,
    "nonunit_mesh_scale_zero": not nonunit_mesh_scale,
    "terrain_xy_exact": terrain_dimensions is not None and terrain_dimensions[:2] == [6400.0, 4800.0],
    "human_scale_exact": human_height == 1.85,
    "heliostat_panels_instanced": len(panels) == 32 and len({id(obj.data) for obj in panels}) == 1,
    "heliostat_masts_instanced": len(masts) == 32 and len({id(obj.data) for obj in masts}) == 1,
    "claim_metadata_matches": scene.get("claim_id") == "CLM-KHEPRI-WMACRO-001",
    "world_metadata_matches": scene.get("world_id") == "khepri",
    "overview_lens_contract": overview is not None and abs(overview.data.lens - 32.0) < 1e-5,
    "overview_clip_contract": overview is not None and overview.data.clip_end >= 12000.0,
    "overview_all_route_anchors_in_frame": overview_all_in_frame,
    "overview_all_route_anchors_within_clip": overview_all_within_clip,
    "gameplay_clip_contract": gameplay is not None and gameplay.data.clip_end >= 8000.0,
    "human_guide_visible_in_gameplay_camera": guide_in_gameplay_frame,
    "human_guide_readable_projected_scale": guide_projected_height_px is not None and 60.0 <= guide_projected_height_px <= 120.0,
}

result = {
    "scope": "khepri/world-macro/planetary-foundation",
    "structural_and_machine_visual_pass": all(checks.values()),
    "checks": checks,
    "metrics": {
        "objects": len(objects),
        "mesh_datablocks": len(meshes),
        "materials": len(bpy.data.materials),
        "curves": len(bpy.data.curves),
        "unique_mesh_vertices": vertices,
        "unique_mesh_triangles": triangles,
        "terrain_dimensions_m": terrain_dimensions,
        "human_guide_height_m": human_height,
        "heliostat_panel_objects": len(panels),
        "heliostat_panel_unique_meshes": len({id(obj.data) for obj in panels}),
        "heliostat_mast_objects": len(masts),
        "heliostat_mast_unique_meshes": len({id(obj.data) for obj in masts}),
        "overview_camera": {
            "lens_mm": round(float(overview.data.lens), 3) if overview else None,
            "clip_end_m": round(float(overview.data.clip_end), 3) if overview else None,
            "anchors": overview_anchor_metrics,
        },
        "gameplay_camera": {
            "lens_mm": round(float(gameplay.data.lens), 3) if gameplay else None,
            "clip_end_m": round(float(gameplay.data.clip_end), 3) if gameplay else None,
            "human_guide_ndc_bbox": guide_bbox_ndc,
            "human_guide_projected_height_px": guide_projected_height_px,
        },
    },
    "defects": {
        "missing": missing,
        "duplicate_object_names": duplicate_names,
        "duplicate_asset_ids": duplicate_asset_ids,
        "nonfinite_transforms": nonfinite,
        "negative_scale": negative_scale,
        "nonunit_mesh_scale": nonunit_mesh_scale,
    },
    "explicit_nonclaims": [
        "human artistic approval",
        "engine integration",
        "collision approval",
        "GPU performance",
        "AAA/AAAA finish",
        "final planet radius canon",
    ],
}
print(json.dumps(result, indent=2, sort_keys=True))
