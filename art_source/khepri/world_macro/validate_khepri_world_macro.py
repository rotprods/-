"""Validation/audit script for KHEPRI world-macro scene.

Designed for Blender 5.2.x. It measures structure; it does not approve artistic quality,
engine integration, collision or performance on target hardware.
"""
import json
import math
from collections import Counter

import bpy
from mathutils import Vector

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

terrain_dimensions = [round(float(value), 3) for value in terrain.dimensions] if terrain else None
human_height = None
if body and head:
    z_min = min((body.matrix_world @ Vector(corner)).z for corner in body.bound_box)
    z_max = max((head.matrix_world @ Vector(corner)).z for corner in head.bound_box)
    human_height = round(z_max - z_min, 3)

triangles = sum(sum(max(len(poly.vertices) - 2, 0) for poly in mesh.polygons) for mesh in meshes)
vertices = sum(len(mesh.vertices) for mesh in meshes)

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
}

result = {
    "scope": "khepri/world-macro/planetary-foundation",
    "structural_pass": all(checks.values()),
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
        "artistic approval",
        "engine integration",
        "collision approval",
        "GPU performance",
        "AAA/AAAA finish",
        "final planet radius canon",
    ],
}
print(json.dumps(result, indent=2, sort_keys=True))
