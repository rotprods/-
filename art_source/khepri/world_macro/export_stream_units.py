"""KHEPRI world-macro split-export audit.

Claim: CLM-KHEPRI-WMACRO-001
Purpose: prove that the Blender master can emit independent, self-contained L1 orbital
and L2 macrocell GLB units without QA cameras/guides leaking into the gameplay package.

This script is an audit/export helper, not final engine streaming policy. It does not
mutate authored geometry. Run in Blender 5.2.x after the current KHEPRI generator,
optimizer and route-refinement stages.
"""
from __future__ import annotations

import hashlib
import json
import os
import struct
import tempfile
from pathlib import Path

import bpy

PACKS = {
    "L1_ORBITAL": ["KHP_WM_10_L1_ORBITAL"],
    "L2_MACROCELL": [
        "KHP_WM_20_L2_TERRAIN",
        "KHP_WM_30_OPTICAL_FOOTPRINTS",
        "KHP_WM_40_ROUTE_INTERFACES",
    ],
}
EXPORTABLE_TYPES = {"MESH", "EMPTY", "CURVE"}


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


def audit() -> dict:
    results = {}
    previous_active = bpy.context.view_layer.objects.active
    previous_selected = list(bpy.context.selected_objects)
    try:
        for pack_name, collection_names in PACKS.items():
            source = pack_objects(collection_names)
            exportable = [obj for obj in source if obj.type in EXPORTABLE_TYPES]
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

            results[pack_name] = {
                "collections": collection_names,
                "object_count": len(exportable),
                "mesh_object_count": sum(obj.type == "MESH" for obj in exportable),
                "curve_object_count": sum(obj.type == "CURVE" for obj in exportable),
                "source_objects": [obj.name for obj in exportable],
                "bytes": len(data),
                "sha256": hashlib.sha256(data).hexdigest(),
                "glb_magic": "glTF",
                "glb_version": 2,
                "gltf_nodes": len(document.get("nodes", [])),
                "gltf_meshes": len(document.get("meshes", [])),
                "gltf_materials": len(document.get("materials", [])),
                "gltf_cameras": len(document.get("cameras", [])),
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

    results["contract_checks"] = {
        "l1_has_one_mesh_object": results["L1_ORBITAL"]["mesh_object_count"] == 1,
        "l1_no_cameras": results["L1_ORBITAL"]["gltf_cameras"] == 0,
        "l1_self_contained": not results["L1_ORBITAL"]["external_uris"],
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
