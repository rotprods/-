"""EXOVANT 2950 — LEVIATHAN repeated-mesh instancing optimization v1.

Deterministic, visual-equivalence-preserving optimization over revision-8 staged scene.
It only shares mesh datablocks when geometry, topology, UVs, material slots and public
attributes match exactly enough under fixed quantization, and when no shape keys,
vertex groups or mesh animation make sharing unsafe.

Claim: CLM-W10-WORLD-LEVIATHAN-001
This does NOT establish a hardware budget, LOD strategy, art approval or runtime PASS.
"""

import bpy
import hashlib
import json
from collections import defaultdict

STAGE = "REPEATED_MESH_INSTANCING_V1"


def _signature(obj):
    me = obj.data
    payload = {
        "verts": [(round(v.co.x, 6), round(v.co.y, 6), round(v.co.z, 6)) for v in me.vertices],
        "edges": [tuple(e.vertices) for e in me.edges],
        "polys": [tuple(p.vertices) for p in me.polygons],
        "uv": [
            (layer.name, [(round(x.uv.x, 6), round(x.uv.y, 6)) for x in layer.data])
            for layer in me.uv_layers
        ],
        "materials": [m.name if m else None for m in me.materials],
        "attributes": [
            (a.name, a.domain, a.data_type, len(a.data))
            for a in me.attributes
            if not a.name.startswith(".")
        ],
        "shape_keys": bool(me.shape_keys),
    }
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def build():
    scene = bpy.context.scene
    groups = defaultdict(list)
    for obj in scene.objects:
        if obj.type == "MESH":
            groups[_signature(obj)].append(obj)

    candidates = []
    for sig, objects in groups.items():
        if len(objects) < 2:
            continue
        objects = sorted(objects, key=lambda o: o.name)
        blockers = []
        for obj in objects:
            if obj.data.shape_keys:
                blockers.append(f"{obj.name}:shape_keys")
            if obj.vertex_groups:
                blockers.append(f"{obj.name}:vertex_groups")
            if obj.data.animation_data:
                blockers.append(f"{obj.name}:mesh_animation")
        if not blockers:
            candidates.append((sig, objects))

    mesh_datablocks_before = len(bpy.data.meshes)
    mesh_objects_before = sum(1 for o in scene.objects if o.type == "MESH")
    relinked = 0
    groups_applied = []

    for sig, objects in sorted(candidates, key=lambda x: x[1][0].name):
        master = objects[0]
        replaced = []
        for obj in objects[1:]:
            old = obj.data
            obj.data = master.data
            replaced.append(obj.name)
            relinked += 1
            if old.users == 0:
                bpy.data.meshes.remove(old)
        groups_applied.append({
            "signature": sig,
            "master": master.name,
            "instances": [o.name for o in objects],
            "count": len(objects),
        })

    mesh_datablocks_after = len(bpy.data.meshes)
    mesh_objects_after = sum(1 for o in scene.objects if o.type == "MESH")

    scene["optimization_stage"] = STAGE
    scene["instancing_visual_contract"] = "geometry_topology_uv_material_attributes_equal"
    scene["instancing_hardware_budget_claimed"] = False
    scene["instancing_runtime_pass_claimed"] = False

    return {
        "stage": STAGE,
        "groups_applied": len(groups_applied),
        "mesh_objects_before": mesh_objects_before,
        "mesh_objects_after": mesh_objects_after,
        "mesh_datablocks_before": mesh_datablocks_before,
        "mesh_datablocks_after": mesh_datablocks_after,
        "mesh_datablocks_removed": mesh_datablocks_before - mesh_datablocks_after,
        "objects_relinked": relinked,
        "groups": groups_applied,
        "status": "STRUCTURAL_OPTIMIZATION_NOT_RUNTIME_QUALIFIED",
    }


if __name__ == "__main__":
    print(build())
