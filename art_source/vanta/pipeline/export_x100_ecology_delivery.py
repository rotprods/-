#!/usr/bin/env python3
"""Deterministic selected-delivery exporter for VANTA X100 ecology.

Run with Blender 5.2:
  blender -b scene.blend -P export_x100_ecology_delivery.py -- --output /path/ecology.glb

The rich .blend remains authoring authority. This exporter emits only the three in-world
ecology tableaux, active-state geometry already instantiated there, runtime colliders and
animations. Authoring source families, LOD source, cameras, audio/affordance metadata helpers
and influence QA helpers are excluded.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import struct
import sys
from pathlib import Path

import bpy

CLAIM = "CLM-VANTA-X100-ECOLOGY-001"
TABLEAUX = (
    "ECO_TBL_SLAG_NURSERY",
    "ECO_TBL_FILINGS_CORRIDOR",
    "ECO_TBL_RIVET_ROOST",
)
EXCLUDED_PREFIXES = (
    "ECO_INFLUENCE__",
    "AUDIO_",
    "AFFORD_",
    "CAM_",
    "LOD1_",
    "LOD2_",
    "VAN_X100_ECO_",
)


def parse_args() -> argparse.Namespace:
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    p = argparse.ArgumentParser()
    p.add_argument("--output", required=True)
    p.add_argument("--receipt", default=None)
    return p.parse_args(argv)


def descendants(root: bpy.types.Object):
    stack = list(root.children)
    while stack:
        obj = stack.pop()
        yield obj
        stack.extend(obj.children)


def read_glb_json(path: Path) -> dict:
    data = path.read_bytes()
    if data[:4] != b"glTF":
        raise RuntimeError("not a GLB")
    off = 12
    while off < len(data):
        length, ctype = struct.unpack_from("<II", data, off)
        off += 8
        chunk = data[off : off + length]
        off += length
        if ctype == 0x4E4F534A:
            return json.loads(chunk.decode("utf-8").rstrip("\x00 "))
    raise RuntimeError("GLB JSON chunk missing")


def main() -> None:
    args = parse_args()
    scene = bpy.context.scene
    assert scene.get("world_name") == "VANTA", scene.get("world_name")
    assert scene.get("production_branch") == "art/world-vanta-001"
    assert scene.get("VANTA_X100_ECOLOGY_CLAIM") == CLAIM

    roots = []
    selected = set()
    for name in TABLEAUX:
        root = bpy.data.objects.get(name)
        assert root is not None, name
        roots.append(root)
        selected.add(root)
        selected.update(descendants(root))

    selected = {
        obj for obj in selected
        if not obj.name.startswith(EXCLUDED_PREFIXES)
    }

    colliders = sorted(
        obj.name for obj in selected
        if obj.name.startswith("COL_ECO_TBL_") and obj.name.lower().endswith("_colonly")
    )
    assert len(colliders) == 10, colliders

    bpy.ops.object.select_all(action="DESELECT")
    for obj in selected:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = roots[0]

    out = Path(args.output).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.export_scene.gltf(
        filepath=str(out),
        export_format="GLB",
        use_selection=True,
        export_animations=True,
        export_frame_range=True,
        export_extras=True,
    )

    gltf = read_glb_json(out)
    node_names = [node.get("name", "") for node in gltf.get("nodes", [])]
    animations = gltf.get("animations", [])
    receipt = {
        "schema": "exovant.vanta.x100.ecology-clean-export.v1",
        "source_revision": int(scene.get("VANTA_X100_ECOLOGY_SOURCE_REVISION", 26)),
        "blender": bpy.app.version_string,
        "claim": CLAIM,
        "tableaux": list(TABLEAUX),
        "selected_objects": len(selected),
        "bytes": out.stat().st_size,
        "sha256": hashlib.sha256(out.read_bytes()).hexdigest(),
        "nodes": len(node_names),
        "meshes": len(gltf.get("meshes", [])),
        "materials": len(gltf.get("materials", [])),
        "images": len(gltf.get("images", [])),
        "animations": len(animations),
        "animation_channels": sum(len(a.get("channels", [])) for a in animations),
        "colonly_nodes": sum("_colonly" in name.lower() for name in node_names),
        "authoring_source_nodes": sum(name.startswith("VAN_X100_ECO_") for name in node_names),
        "lod_source_nodes": sum(name.startswith(("LOD1_", "LOD2_")) for name in node_names),
        "editor_hook_nodes": sum(
            name.startswith(("AUDIO_", "AFFORD_", "CAM_", "ECO_INFLUENCE__"))
            for name in node_names
        ),
        "runtime_authority": False,
        "note": "Engine reimport is a separate qualification gate; this receipt proves selected export structure only.",
    }
    assert receipt["colonly_nodes"] == 10, receipt
    assert receipt["authoring_source_nodes"] == 0, receipt
    assert receipt["lod_source_nodes"] == 0, receipt
    assert receipt["editor_hook_nodes"] == 0, receipt

    receipt_path = (
        Path(args.receipt).resolve()
        if args.receipt
        else out.with_suffix(".receipt.json")
    )
    receipt_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(receipt, sort_keys=True))


if __name__ == "__main__":
    main()
