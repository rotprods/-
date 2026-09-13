#!/usr/bin/env python3
"""Export the active VANTA X100 Worker Life state as a clean runtime GLB.

Run inside Blender 5.2 with the VANTA source .blend open:
  blender -b SOURCE.blend --python export_x100_delivery.py -- OUTPUT.glb [RECEIPT.json]

The source .blend may contain all state deltas and LOD source objects. Runtime delivery is
explicitly selected: root + base children + active state delta + _colonly collider.
"""
import bpy
import hashlib
import json
import os
import struct
import sys

args = sys.argv[sys.argv.index("--") + 1 :]
if not args:
    raise SystemExit("usage: -- OUTPUT.glb [RECEIPT.json]")
out_path = os.path.abspath(args[0])
receipt_path = os.path.abspath(args[1]) if len(args) > 1 else out_path + ".receipt.json"
scene = bpy.context.scene
assert scene.get("world_name") == "VANTA"
assert scene.get("VANTA_X100_CLAIM") == "CLM-VANTA-X100-CULTURE-001"
roots = sorted(
    [o for o in bpy.data.objects if o.name.startswith("VAN_X100_CULT_") and o.type == "EMPTY"],
    key=lambda o: o.name,
)
assert len(roots) == 36, len(roots)
selected = []
current_states = {}
for root in roots:
    selected.append(root)
    current_state = str(root.get("current_state"))
    current_states[root.name] = current_state
    for child in root.children:
        state = child.get("x100_state_layer")
        if child.type == "MESH" and (state is None or state == current_state):
            selected.append(child)
    collider = bpy.data.objects.get(root.get("collision_name", ""))
    assert collider is not None, root.name
    selected.append(collider)
for obj in scene.objects:
    obj.select_set(False)
for obj in selected:
    obj.select_set(True)
bpy.context.view_layer.objects.active = roots[0]
os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
bpy.ops.export_scene.gltf(
    filepath=out_path,
    export_format="GLB",
    export_apply=True,
    use_selection=True,
    export_extras=True,
    export_cameras=False,
    export_lights=False,
)
raw = open(out_path, "rb").read()
assert raw[:4] == b"glTF"
pos = 12
payload = None
while pos < len(raw):
    length, chunk_type = struct.unpack_from("<II", raw, pos)
    pos += 8
    data = raw[pos : pos + length]
    pos += length
    if chunk_type == 0x4E4F534A:
        payload = json.loads(data.rstrip(b"\0 \t\r\n"))
assert payload is not None
names = [n.get("name", "") for n in payload.get("nodes", [])]
root_names = [n for n in names if n.startswith("VAN_X100_CULT_") and "__" not in n]
colliders = [n for n in names if n.startswith("COL_VAN_X100_CULT_") and n.endswith("_colonly")]
state_nodes = [n for n in names if "__STATE_" in n]
lod_nodes = [n for n in names if n.startswith("LOD1_")]
inactive = []
for name in state_nodes:
    root_name = name.split("__STATE_")[0]
    expected = current_states[root_name].upper()
    if f"__STATE_{expected}_" not in name:
        inactive.append(name)
uv_bad = []
visual_primitives = 0
for node in payload.get("nodes", []):
    name = node.get("name", "")
    mesh_index = node.get("mesh")
    if mesh_index is None or name.startswith("COL_"):
        continue
    for primitive in payload["meshes"][mesh_index].get("primitives", []):
        if "material" in primitive:
            visual_primitives += 1
            if "TEXCOORD_0" not in primitive.get("attributes", {}):
                uv_bad.append(name)
assert len(root_names) == 36
assert len(colliders) == 36
assert not lod_nodes
assert not inactive
assert not uv_bad
receipt = {
    "schema": "exovant.vanta.x100-runtime-export.v1",
    "blender": bpy.app.version_string,
    "claim": "CLM-VANTA-X100-CULTURE-001",
    "sha256": hashlib.sha256(raw).hexdigest(),
    "bytes": len(raw),
    "nodes": len(names),
    "meshes": len(payload.get("meshes", [])),
    "materials": len(payload.get("materials", [])),
    "images": len(payload.get("images", [])),
    "roots": len(root_names),
    "colliders": len(colliders),
    "active_state_nodes": len(state_nodes),
    "inactive_state_nodes": len(inactive),
    "lod_source_nodes": len(lod_nodes),
    "visual_primitives": visual_primitives,
    "uv_bad": uv_bad,
    "current_states": current_states,
}
with open(receipt_path, "w", encoding="utf-8") as handle:
    json.dump(receipt, handle, indent=2)
    handle.write("\n")
print(json.dumps(receipt, indent=2))
