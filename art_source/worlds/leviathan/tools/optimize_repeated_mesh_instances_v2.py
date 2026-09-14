"""EXOVANT 2950 — LEVIATHAN repeated-mesh instancing optimization v2.

v1 was intentionally conservative but its mesh signature depended on Blender's internal
vertex/face ordering. Primary and independent cold builds were later proven to have exactly
the same evaluated visual surface while some UV-sphere primitives used different internal
index ordering.

v2 canonicalizes local mesh topology/surface, UVs, face materials, smoothing and sharp-face
state independently of vertex/face numbering. It only shares mesh datablocks when that
canonical editable-surface contract matches and when no shape keys, vertex groups, mesh
animation, color attributes or unknown public mesh attributes make sharing unsafe.

Claim: CLM-W10-WORLD-LEVIATHAN-001.
This is a source/export structural optimization. It does NOT establish runtime performance,
LOD completion, engine acceptance or art approval.
"""

import bpy
import hashlib
import json
from collections import defaultdict

STAGE = "REPEATED_MESH_INSTANCING_V2"
PRECISION = 6
ALLOWED_PUBLIC_ATTRIBUTES = {"position", "UVMap", "sharp_face"}


def _norm(value):
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    try:
        if hasattr(value, "to_list"):
            return [_norm(x) for x in value.to_list()]
    except Exception:
        pass
    try:
        if not isinstance(value, (str, bytes, dict)):
            return [_norm(x) for x in list(value)]
    except Exception:
        pass
    if isinstance(value, dict):
        return {str(k): _norm(v) for k, v in sorted(value.items(), key=lambda kv: str(kv[0]))}
    return str(value)


def _canonical_cycle(values):
    values = tuple(values)
    if not values:
        return values
    n = len(values)
    rotations = [values[i:] + values[:i] for i in range(n)]
    reverse = tuple(reversed(values))
    rotations.extend(reverse[i:] + reverse[:i] for i in range(n))
    return min(rotations, key=repr)


def _eligible(obj):
    if obj.type != "MESH":
        return False, "not_mesh"
    mesh = obj.data
    if mesh.shape_keys:
        return False, "shape_keys"
    if obj.vertex_groups:
        return False, "vertex_groups"
    if mesh.animation_data:
        return False, "mesh_animation"
    if mesh.color_attributes:
        return False, "color_attributes"
    unknown = [
        attr.name
        for attr in mesh.attributes
        if not attr.name.startswith(".") and attr.name not in ALLOWED_PUBLIC_ATTRIBUTES
    ]
    if unknown:
        return False, "unknown_attributes:" + ",".join(sorted(unknown))
    return True, None


def _signature(obj):
    mesh = obj.data
    uv_layers = list(mesh.uv_layers)

    vertices = sorted(
        (round(v.co.x, PRECISION), round(v.co.y, PRECISION), round(v.co.z, PRECISION))
        for v in mesh.vertices
    )

    edges = []
    for edge in mesh.edges:
        a = mesh.vertices[edge.vertices[0]].co
        b = mesh.vertices[edge.vertices[1]].co
        endpoints = sorted(
            [
                (round(a.x, PRECISION), round(a.y, PRECISION), round(a.z, PRECISION)),
                (round(b.x, PRECISION), round(b.y, PRECISION), round(b.z, PRECISION)),
            ]
        )
        seam = bool(getattr(edge, "use_seam", False))
        sharp = bool(getattr(edge, "use_edge_sharp", False)) if hasattr(edge, "use_edge_sharp") else False
        edges.append((tuple(endpoints), seam, sharp))
    edges.sort(key=repr)

    sharp_face = mesh.attributes.get("sharp_face")
    faces = []
    for poly in mesh.polygons:
        corners = []
        for loop_index in poly.loop_indices:
            vertex_index = mesh.loops[loop_index].vertex_index
            co = mesh.vertices[vertex_index].co
            uvs = []
            for layer in uv_layers:
                uv = layer.data[loop_index].uv
                uvs.append((layer.name, round(uv.x, PRECISION), round(uv.y, PRECISION)))
            corners.append(
                (
                    round(co.x, PRECISION),
                    round(co.y, PRECISION),
                    round(co.z, PRECISION),
                    tuple(uvs),
                )
            )
        normal = (
            round(poly.normal.x, PRECISION),
            round(poly.normal.y, PRECISION),
            round(poly.normal.z, PRECISION),
        )
        is_sharp_face = bool(sharp_face.data[poly.index].value) if sharp_face else False
        material = (
            mesh.materials[poly.material_index].name
            if poly.material_index < len(mesh.materials) and mesh.materials[poly.material_index]
            else None
        )
        faces.append(
            (
                _canonical_cycle(tuple(corners)),
                normal,
                material,
                bool(poly.use_smooth),
                is_sharp_face,
            )
        )
    faces.sort(key=repr)

    payload = {
        "vertices": vertices,
        "edges": edges,
        "faces": faces,
        "materials": [m.name if m else None for m in mesh.materials],
        "mesh_properties": {k: _norm(mesh[k]) for k in sorted(mesh.keys()) if k != "_RNA_UI"},
    }
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def build():
    scene = bpy.context.scene
    groups = defaultdict(list)
    blocked = []

    for obj in scene.objects:
        if obj.type != "MESH":
            continue
        ok, reason = _eligible(obj)
        if not ok:
            blocked.append({"object": obj.name, "reason": reason})
            continue
        groups[_signature(obj)].append(obj)

    candidates = []
    for signature, objects in groups.items():
        if len(objects) < 2:
            continue
        candidates.append((signature, sorted(objects, key=lambda o: o.name)))

    before_datablocks = len(bpy.data.meshes)
    before_objects = sum(1 for o in scene.objects if o.type == "MESH")
    relinked = 0
    changed_groups = 0
    applied_groups = []

    for signature, objects in sorted(candidates, key=lambda item: item[1][0].name):
        master = objects[0]
        changed = False
        for obj in objects[1:]:
            old = obj.data
            if old == master.data:
                continue
            obj.data = master.data
            relinked += 1
            changed = True
            if old.users == 0:
                bpy.data.meshes.remove(old)
        if changed:
            changed_groups += 1
        applied_groups.append(
            {
                "signature": signature,
                "master": master.name,
                "count": len(objects),
                "instances": [o.name for o in objects],
                "changed": changed,
            }
        )

    after_datablocks = len(bpy.data.meshes)
    after_objects = sum(1 for o in scene.objects if o.type == "MESH")

    scene["optimization_stage"] = STAGE
    scene["instancing_signature_contract"] = "order_invariant_local_topology_uv_material_smoothing_sharpface"
    scene["instancing_visual_contract"] = "canonical_evaluated_surface_must_remain_equal"
    scene["instancing_hardware_budget_claimed"] = False
    scene["instancing_runtime_pass_claimed"] = False

    return {
        "stage": STAGE,
        "candidate_groups": len(candidates),
        "changed_groups": changed_groups,
        "objects_in_candidate_groups": sum(len(objects) for _, objects in candidates),
        "mesh_objects_before": before_objects,
        "mesh_objects_after": after_objects,
        "mesh_datablocks_before": before_datablocks,
        "mesh_datablocks_after": after_datablocks,
        "mesh_datablocks_removed": before_datablocks - after_datablocks,
        "objects_relinked": relinked,
        "blocked": blocked,
        "groups": applied_groups,
        "status": "STRUCTURAL_OPTIMIZATION_NOT_RUNTIME_QUALIFIED",
    }


if __name__ == "__main__":
    print(build())
