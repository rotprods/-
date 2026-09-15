"""Deterministic UV0 handoff for KHEPRI optical field meshes.

Owned by CLM-KHEPRI-WMACRO-001. Adds only UV data; vertices, polygons, material slots,
object transforms and silhouettes must remain unchanged. Intended for tileable KHEPRI material
families. Unique hero/state masks require a later dedicated UV claim.
"""
from __future__ import annotations

import hashlib
import json
import math
import bpy

CONTRACT = "KHP_OPTICAL_UV0_HANDOFF_V1"
UV_LAYER = "UVMap"
METERS_PER_REPEAT = 4.0
UV_PER_METER = 1.0 / METERS_PER_REPEAT
VARIANTS = ("COMPACT", "STANDARD", "WIDE")
EXPECTED = {
    *(f"KHP_WM_X100_MAST_{v}" for v in VARIANTS),
    *(f"KHP_WM_X100_PANEL_{v}" for v in VARIANTS),
    *(f"KHP_WM_X100_LOD1_MAST_{v}" for v in VARIANTS),
    *(f"KHP_WM_X100_LOD1_PANEL_{v}" for v in VARIANTS),
    *(f"KHP_WM_X100_LOD2_MAST_{v}" for v in VARIANTS),
    *(f"KHP_WM_X100_LOD2_PANEL_{v}" for v in VARIANTS),
}


def geometry_payload(mesh):
    return {
        "name": mesh.name,
        "vertices": [[round(v.co.x, 7), round(v.co.y, 7), round(v.co.z, 7)] for v in mesh.vertices],
        "polygons": [list(p.vertices) for p in mesh.polygons],
        "materials": [m.name if m else None for m in mesh.materials],
        "loops": len(mesh.loops),
    }


def geometry_sha(meshes):
    raw = json.dumps([geometry_payload(m) for m in sorted(meshes, key=lambda x: x.name)], sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def project_uv(co, normal):
    ax = max(range(3), key=lambda i: abs(normal[i]))
    if ax == 0:
        u = co.y if normal.x >= 0 else -co.y
        v = co.z
    elif ax == 1:
        u = -co.x if normal.y >= 0 else co.x
        v = co.z
    else:
        u = co.x
        v = co.y if normal.z >= 0 else -co.y
    return (u * UV_PER_METER, v * UV_PER_METER)


def apply():
    meshes = [m for m in bpy.data.meshes if m.name in EXPECTED]
    names = {m.name for m in meshes}
    if names != EXPECTED:
        raise RuntimeError("unexpected optical mesh set: missing=" + json.dumps(sorted(EXPECTED - names)))
    before = geometry_sha(meshes)
    rows = []
    for mesh in sorted(meshes, key=lambda m: m.name):
        mesh.update()
        uv = mesh.uv_layers.get(UV_LAYER)
        if uv is None:
            uv = mesh.uv_layers.new(name=UV_LAYER)
        mesh.uv_layers.active = uv
        if len(uv.data) != len(mesh.loops):
            raise RuntimeError(f"UV loop allocation mismatch: {mesh.name}")
        for poly in mesh.polygons:
            n = poly.normal.copy()
            for li in poly.loop_indices:
                loop = mesh.loops[li]
                uv.data[li].uv = project_uv(mesh.vertices[loop.vertex_index].co, n)
        mesh["uv0_contract"] = CONTRACT
        mesh["uv0_layer"] = UV_LAYER
        mesh["uv0_meters_per_repeat"] = METERS_PER_REPEAT
        mesh["uv0_overlap_policy"] = "INTENTIONAL_TILEABLE_OBJECT_SPACE"
        vals = [(round(d.uv.x, 7), round(d.uv.y, 7)) for d in uv.data]
        if not all(math.isfinite(a) and math.isfinite(b) for a, b in vals):
            raise RuntimeError(f"non-finite UV: {mesh.name}")
        rows.append({"mesh": mesh.name, "loops": len(mesh.loops), "uv_loops": len(uv.data), "min_u": min(x for x,_ in vals), "max_u": max(x for x,_ in vals), "min_v": min(y for _,y in vals), "max_v": max(y for _,y in vals)})
    after = geometry_sha(meshes)
    if before != after:
        raise RuntimeError(f"geometry changed before={before} after={after}")
    uv_raw = json.dumps(rows, sort_keys=True, separators=(",", ":")).encode()
    uv_sha = hashlib.sha256(uv_raw).hexdigest()
    bpy.context.scene["khepri_optical_uv0_contract"] = CONTRACT
    bpy.context.scene["khepri_optical_uv0_sha256"] = uv_sha
    bpy.context.scene["khepri_optical_uv0_geometry_sha256"] = after
    return {"contract": CONTRACT, "meshes": len(meshes), "geometry_sha_before": before, "geometry_sha_after": after, "geometry_unchanged": before == after, "uv_sha256": uv_sha, "meters_per_repeat": METERS_PER_REPEAT, "rows": rows}


if __name__ == "__main__":
    print(json.dumps(apply(), indent=2, sort_keys=True))
