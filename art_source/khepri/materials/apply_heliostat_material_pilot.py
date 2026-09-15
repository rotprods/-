"""Guarded KHEPRI heliostat material pilot adapter.

This script is NOT authorized to mutate the geometry-owner branch until both:
1) CLM-KHEPRI-MATERIALS-001 is active in the fleet registry, and
2) CLM-KHEPRI-WMACRO-001 explicitly hands off UV-ready integration geometry.

It replaces material roles only, verifies UV0 preconditions, and proves mesh geometry identity did
not change. Run inside Blender 5.2+ with `-- <material_library.blend>` as the final argument.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
import bpy

PILOT_CONTRACT = "KHP_HELIOSTAT_MATERIAL_PILOT_V1"
MESH_PREFIXES = ("KHP_WM_X100_MAST_", "KHP_WM_X100_PANEL_")
MATERIAL_MAP = {
    "KHP_WM_MAT_BRONZE_BLOCKOUT": "KHP_MAT_BRONZE_SYNOD_001__SERVICE_CLEAN",
    "KHP_WM_MAT_MIRROR_BLOCKOUT": "KHP_MAT_MIRROR_OPTICAL_001__CALIBRATED",
}
APPLICATION_IDS = {
    "KHP_MAT_BRONZE_SYNOD_001__SERVICE_CLEAN": "KHP_MAT_BRONZE_SYNOD_001::service_clean::cast_structural::architectural",
    "KHP_MAT_MIRROR_OPTICAL_001__CALIBRATED": "KHP_MAT_MIRROR_OPTICAL_001::calibrated::broad_reflector::architectural",
}
EXPECTED_MESHES = {
    "KHP_WM_X100_MAST_COMPACT",
    "KHP_WM_X100_MAST_STANDARD",
    "KHP_WM_X100_MAST_WIDE",
    "KHP_WM_X100_PANEL_COMPACT",
    "KHP_WM_X100_PANEL_STANDARD",
    "KHP_WM_X100_PANEL_WIDE",
}


def mesh_semantic_payload(mesh: bpy.types.Mesh) -> dict:
    return {
        "name": mesh.name,
        "vertices": [[round(v.co.x, 7), round(v.co.y, 7), round(v.co.z, 7)] for v in mesh.vertices],
        "polygons": [list(poly.vertices) for poly in mesh.polygons],
        "loops": len(mesh.loops),
        "uv_layers": [layer.name for layer in mesh.uv_layers],
        "uv_loop_counts": {layer.name: len(layer.data) for layer in mesh.uv_layers},
    }


def geometry_sha(meshes: list[bpy.types.Mesh]) -> str:
    payload = [mesh_semantic_payload(mesh) for mesh in sorted(meshes, key=lambda item: item.name)]
    return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def require_uv(meshes: list[bpy.types.Mesh]) -> None:
    failures = []
    for mesh in meshes:
        uv = mesh.uv_layers.get("UVMap") or mesh.uv_layers.active
        if uv is None or len(uv.data) != len(mesh.loops):
            failures.append({"mesh": mesh.name, "uv": uv.name if uv else None, "uv_loops": len(uv.data) if uv else 0, "mesh_loops": len(mesh.loops)})
    if failures:
        raise RuntimeError("UV0_HANDOFF_NOT_READY: " + json.dumps(failures, sort_keys=True))


def append_materials(library_path: str) -> dict[str, bpy.types.Material]:
    wanted = set(MATERIAL_MAP.values())
    existing = {name: bpy.data.materials.get(name) for name in wanted}
    missing = {name for name, material in existing.items() if material is None}
    if missing:
        if not os.path.isfile(library_path):
            raise RuntimeError(f"material library not found: {library_path}")
        with bpy.data.libraries.load(library_path, link=False) as (source, target):
            unavailable = sorted(missing - set(source.materials))
            if unavailable:
                raise RuntimeError("missing materials in library: " + ",".join(unavailable))
            target.materials = sorted(missing)
    result = {name: bpy.data.materials.get(name) for name in wanted}
    if any(material is None for material in result.values()):
        raise RuntimeError("material append failed")
    return result


def apply(library_path: str) -> dict:
    meshes = [mesh for mesh in bpy.data.meshes if mesh.name.startswith(MESH_PREFIXES)]
    names = {mesh.name for mesh in meshes}
    if names != EXPECTED_MESHES:
        raise RuntimeError(f"unexpected mesh set: expected={sorted(EXPECTED_MESHES)} observed={sorted(names)}")
    require_uv(meshes)
    before_sha = geometry_sha(meshes)
    appended = append_materials(library_path)

    replacements = []
    for mesh in meshes:
        for index, current in enumerate(list(mesh.materials)):
            current_name = current.name if current else ""
            target_name = MATERIAL_MAP.get(current_name)
            if target_name:
                mesh.materials[index] = appended[target_name]
                replacements.append({
                    "mesh": mesh.name,
                    "slot": index,
                    "from": current_name,
                    "to": target_name,
                    "application_id": APPLICATION_IDS[target_name],
                })

    if len(replacements) != 9:  # 3 mast bronze + 3 panel mirror + 3 panel bronze.
        raise RuntimeError(f"unexpected material replacement count: {len(replacements)}")

    after_sha = geometry_sha(meshes)
    if before_sha != after_sha:
        raise RuntimeError(f"GEOMETRY_MUTATION_DETECTED before={before_sha} after={after_sha}")

    bpy.context.scene["khepri_material_pilot_contract"] = PILOT_CONTRACT
    bpy.context.scene["khepri_material_pilot_geometry_sha"] = after_sha
    bpy.context.scene["khepri_material_pilot_replacements_json"] = json.dumps(replacements, sort_keys=True)

    return {
        "contract": PILOT_CONTRACT,
        "geometry_sha_before": before_sha,
        "geometry_sha_after": after_sha,
        "geometry_unchanged": True,
        "meshes": len(meshes),
        "replacements": replacements,
    }


def _library_arg() -> str:
    args = sys.argv
    if "--" not in args or args.index("--") == len(args) - 1:
        raise RuntimeError("usage: blender --background scene.blend --python apply_heliostat_material_pilot.py -- material_library.blend")
    return args[args.index("--") + 1]


if __name__ == "__main__":
    print(json.dumps(apply(_library_arg()), indent=2, sort_keys=True))
