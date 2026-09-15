"""KHEPRI world-macro split-export audit.

Claim: CLM-KHEPRI-WMACRO-001
Purpose: prove that the Blender master can emit independent, self-contained L1 orbital
and L2 macrocell GLB units without QA cameras/guides leaking into the gameplay package.

The L1 orbital proxy is deliberately parked below the macrocell inside the authoring master.
That preview-only offset must NOT leak into a standalone L1 package, so this exporter
recenters L1 temporarily, exports, and restores the scene exactly.

This is an audit/export helper, not final engine streaming policy. It does not persist
scene mutations. Run in Blender 5.2.x after generator, optimizer and route refinement.
"""
from __future__ import annotations

import hashlib
import json
import os
import struct
import tempfile
from pathlib import Path

import bpy
from mathutils import Vector

PACKS = {
    "L1_ORBITAL": {
        "collections": ["KHP_WM_10_L1_ORBITAL"],
        "origin_object": "KHP_WM_L1_ORBITAL_PROXY_1_TO_20000",
    },
    "L2_MACROCELL": {
        "collections": [
            "KHP_WM_20_L2_TERRAIN",
            "KHP_WM_30_OPTICAL_FOOTPRINTS",
            "KHP_WM_40_ROUTE_INTERFACES",
        ],
        "origin_object": None,
    },
}
EXPORTABLE_TYPES = {"MESH", "EMPTY", "CURVE"}
PROVIDER_EXTRAS = {"hf_id"}


def descendants(collection: bpy.types.Collection):
    objects = list(collection.objects)
    for child in collection.children:
        objects.extend(descendants(child))
    return objects


def pack_objects(collection_names: list[str]):
    by_name = {}
    for collection_name in collection_names:
        collection = bpy.data.collections.get(collection_name)
        if collection is None:
            raise RuntimeError(f"Missing KHEPRI collection: {collection_name}")
        for obj in descendants(collection):
            by_name[obj.name] = obj
    return [by_name[name] for name in sorted(by_name)]


def parse_glb(path: str):
    data = Path(path).read_bytes()
    if len(data) < 12:
        raise RuntimeError("GLB too small")
    magic, version, declared_length = struct.unpack("<4sII", data[:12])
    if magic != b"glTF" or version != 2 or declared_length != len(data):
        raise RuntimeError(
            f"Bad GLB header: {magic!r}, v{version}, declared={declared_length}, actual={len(data)}"
        )
    offset = 12
    chunks = []
    while offset + 8 <= len(data):
        length, chunk_type = struct.unpack("<I4s", data[offset : offset + 8])
        offset += 8
        payload = data[offset : offset + length]
        offset += length
        chunks.append((chunk_type, payload))
    json_chunk = next((payload for kind, payload in chunks if kind == b"JSON"), None)
    document = (
        json.loads(json_chunk.decode("utf-8").rstrip(" \t\r\n\x00"))
        if json_chunk
        else {}
    )
    return data, document


def normalize_gltf(value):
    """Drop provider-only identity while retaining authored/export semantics."""
    if isinstance(value, dict):
        return {
            key: normalize_gltf(item)
            for key, item in value.items()
            if key not in PROVIDER_EXTRAS
        }
    if isinstance(value, list):
        return [normalize_gltf(item) for item in value]
    return value


def normalized_json_sha256(document: dict) -> str:
    normalized = normalize_gltf(document)
    raw = json.dumps(normalized, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def apply_pack_origin(exportable, origin_object_name: str | None):
    """Temporarily move one pack into an export-local coordinate frame.

    Returns an object->location snapshot that must always be restored.
    L2 is already a local tangent cell centered on terrain origin, so it uses no shift.
    """
    original = {obj.name: obj.location.copy() for obj in exportable}
    if origin_object_name is None:
        return original, Vector((0.0, 0.0, 0.0))

    origin_object = bpy.data.objects.get(origin_object_name)
    if origin_object is None or origin_object not in exportable:
        raise RuntimeError(f"Missing export origin object: {origin_object_name}")
    offset = origin_object.location.copy()
    for obj in exportable:
        if obj.parent is not None:
            raise RuntimeError(
                f"Pack origin normalization requires root objects; parented object: {obj.name}"
            )
        obj.location -= offset
    bpy.context.view_layer.update()
    return original, offset


def restore_locations(original):
    for name, location in original.items():
        obj = bpy.data.objects.get(name)
        if obj is not None:
            obj.location = location
    bpy.context.view_layer.update()


def audit() -> dict:
    results = {}
    previous_active = bpy.context.view_layer.objects.active
    previous_selected = list(bpy.context.selected_objects)
    try:
        for pack_name, spec in PACKS.items():
            collection_names = spec["collections"]
            source = pack_objects(collection_names)
            exportable = [obj for obj in source if obj.type in EXPORTABLE_TYPES]
            original_locations = {}
            offset = Vector((0.0, 0.0, 0.0))
            try:
                original_locations, offset = apply_pack_origin(
                    exportable, spec["origin_object"]
                )
                bpy.ops.object.select_all(action="DESELECT")
                for obj in exportable:
                    obj.select_set(True)
                if exportable:
                    bpy.context.view_layer.objects.active = exportable[0]

                path = os.path.join(
                    tempfile.gettempdir(), f"khepri_{pack_name.lower()}_audit.glb"
                )
                bpy.ops.export_scene.gltf(
                    filepath=path,
                    export_format="GLB",
                    use_selection=True,
                    export_extras=True,
                    export_cameras=False,
                    export_lights=False,
                )
                data, document = parse_glb(path)
                os.remove(path)
            finally:
                if original_locations:
                    restore_locations(original_locations)

            root_indices = (
                document.get("scenes", [{}])[document.get("scene", 0)].get("nodes", [])
                if document.get("scenes")
                else []
            )
            root_nodes = [document.get("nodes", [])[index] for index in root_indices]
            results[pack_name] = {
                "collections": collection_names,
                "origin_object": spec["origin_object"],
                "origin_offset_removed_blender_xyz_m": [round(float(x), 6) for x in offset],
                "object_count": len(exportable),
                "mesh_object_count": sum(obj.type == "MESH" for obj in exportable),
                "curve_object_count": sum(obj.type == "CURVE" for obj in exportable),
                "source_objects": [obj.name for obj in exportable],
                "bytes": len(data),
                "sha256": hashlib.sha256(data).hexdigest(),
                "normalized_gltf_json_sha256": normalized_json_sha256(document),
                "glb_magic": "glTF",
                "glb_version": 2,
                "gltf_nodes": len(document.get("nodes", [])),
                "gltf_meshes": len(document.get("meshes", [])),
                "gltf_materials": len(document.get("materials", [])),
                "gltf_cameras": len(document.get("cameras", [])),
                "root_translations": [node.get("translation", [0, 0, 0]) for node in root_nodes],
                "external_uris": [
                    entry["uri"]
                    for collection in (document.get("buffers", []), document.get("images", []))
                    for entry in collection
                    if entry.get("uri")
                ],
            }
    finally:
        bpy.ops.object.select_all(action="DESELECT")
        for obj in previous_selected:
            if obj.name in bpy.data.objects:
                obj.select_set(True)
        if previous_active and previous_active.name in bpy.data.objects:
            bpy.context.view_layer.objects.active = previous_active

    l1_roots = results["L1_ORBITAL"]["root_translations"]
    results["contract_checks"] = {
        "l1_has_one_mesh_object": results["L1_ORBITAL"]["mesh_object_count"] == 1,
        "l1_no_cameras": results["L1_ORBITAL"]["gltf_cameras"] == 0,
        "l1_self_contained": not results["L1_ORBITAL"]["external_uris"],
        "l1_origin_centered": all(
            all(abs(float(axis)) <= 1e-6 for axis in translation)
            for translation in l1_roots
        ),
        "l2_has_terrain": "KHP_WM_L2_MACROCELL_A_TERRAIN"
        in results["L2_MACROCELL"]["source_objects"],
        "l2_has_optics": any(
            name.startswith("KHP_WM_HELIOSTAT_")
            for name in results["L2_MACROCELL"]["source_objects"]
        ),
        "l2_has_route_anchors": all(
            name in results["L2_MACROCELL"]["source_objects"]
            for name in (
                "KHP_WM_ROUTE_SHADE",
                "KHP_WM_ROUTE_GLASS_SEA",
                "KHP_WM_ROUTE_CRUCIBLE",
                "KHP_WM_ROUTE_RAKHET",
            )
        ),
        "l2_excludes_qa_route": "KHP_WM_ROUTE_GUIDE_ONLY"
        not in results["L2_MACROCELL"]["source_objects"],
        "l2_excludes_human_guide": not any(
            name.startswith("KHP_WM_GUIDE_HUMAN_")
            for name in results["L2_MACROCELL"]["source_objects"]
        ),
        "l2_no_cameras": results["L2_MACROCELL"]["gltf_cameras"] == 0,
        "l2_self_contained": not results["L2_MACROCELL"]["external_uris"],
    }
    results["passed"] = all(results["contract_checks"].values())
    return results


RESULT = audit()
print(json.dumps(RESULT, indent=2, sort_keys=True))
