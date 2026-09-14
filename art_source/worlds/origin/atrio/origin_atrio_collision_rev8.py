"""EXOVANT 2950 — ORIGIN Atrio rev8 collision corrective generator.

Run after `origin_atrio.py` and before downstream X100/LOD generators.
This deterministic corrective pass converts only the nine ring collision proxies
(A70/B52/C34 x three sectors) from closed low-poly solids into upward-facing,
walkable top surfaces. It preserves visual geometry, bridge/node collision,
asset IDs, transforms and LOD source geometry.

Why this exists:
- exact Atrio rev6 GLB imported successfully in Godot 4.7.2;
- real CharacterBody traversal stopped at r~19.0647 m;
- a horizontal collision audit located an internal vertical wall in
  COL_ORG_ATR_RING_A70_SEG_00 at x=19.220577 m;
- rev7 removed the side walls but adversarial QA caught downward winding;
- rev8 flipped winding upward and the same native Godot canary passed.
"""

import bpy

RING_PREFIXES = (
    "COL_ORG_ATR_RING_A70_SEG_",
    "COL_ORG_ATR_RING_B52_SEG_",
    "COL_ORG_ATR_RING_C34_SEG_",
)
SEMANTICS = "walkable_top_surface_only_upward_v3"
FIX_ID = "REAL_GLB_CHARACTERBODY_BLOCKER_20260914"


def ring_collision_objects():
    return sorted(
        (
            o for o in bpy.data.objects
            if o.type == "MESH" and any(o.name.startswith(p) for p in RING_PREFIXES)
        ),
        key=lambda o: o.name,
    )


def _build_top_only_mesh(obj):
    mesh = obj.data
    if not mesh.vertices or not mesh.polygons:
        raise RuntimeError(f"empty collision mesh: {obj.name}")

    max_z = max(v.co.z for v in mesh.vertices)
    eps = 1e-4
    selected_faces = []
    used = set()
    for poly in mesh.polygons:
        face = list(poly.vertices)
        if face and all(mesh.vertices[i].co.z >= max_z - eps for i in face):
            selected_faces.append(face)
            used.update(face)

    if not selected_faces:
        raise RuntimeError(f"no top polygons found: {obj.name}")

    ordered = sorted(used)
    remap = {old: new for new, old in enumerate(ordered)}
    verts = [mesh.vertices[i].co.copy() for i in ordered]
    faces = [[remap[i] for i in face] for face in selected_faces]

    def make_mesh(name, source_faces):
        out = bpy.data.meshes.new(name)
        out.from_pydata(verts, [], source_faces)
        out.update(calc_edges=True)
        return out

    new_mesh = make_mesh(obj.name + "_WALKABLE_TOP_MESH", faces)
    if min(float(p.normal.z) for p in new_mesh.polygons) < 0.0:
        bpy.data.meshes.remove(new_mesh)
        faces = [list(reversed(face)) for face in faces]
        new_mesh = make_mesh(obj.name + "_WALKABLE_TOP_UPWARD_MESH", faces)

    if min(float(p.normal.z) for p in new_mesh.polygons) < 0.99:
        raise RuntimeError(f"top collision winding not upward: {obj.name}")

    old_mesh = obj.data
    obj.data = new_mesh
    if old_mesh.users == 0:
        bpy.data.meshes.remove(old_mesh)

    obj["collision_policy"] = SEMANTICS
    obj["origin_collision_semantics"] = SEMANTICS
    obj["origin_collision_fix"] = FIX_ID
    obj["origin_collision_top_z_local"] = float(max_z)
    obj.hide_render = True
    obj.display_type = "WIRE"

    return {
        "name": obj.name,
        "polys": len(new_mesh.polygons),
        "verts": len(new_mesh.vertices),
        "min_normal_z": min(float(p.normal.z) for p in new_mesh.polygons),
        "z_span": max(v.co.z for v in new_mesh.vertices) - min(v.co.z for v in new_mesh.vertices),
    }


def apply_rev8_collision_contract():
    rings = ring_collision_objects()
    if len(rings) != 9:
        raise RuntimeError(f"expected 9 ring collision proxies, found {len(rings)}")

    report = [_build_top_only_mesh(obj) for obj in rings]
    if any(r["polys"] != 18 or r["z_span"] > 1e-5 or r["min_normal_z"] < 0.99 for r in report):
        raise RuntimeError("rev8 ring collision contract failed")

    scene = bpy.context.scene
    scene["origin_ring_collision_revision"] = SEMANTICS
    scene["origin_ring_collision_reason"] = (
        "remove internal vertical proxy walls that blocked real Godot CharacterBody traversal "
        "across bridge interfaces; preserve walkable top surfaces only"
    )
    scene["origin_ring_collision_fix_id"] = FIX_ID
    return report


if __name__ == "__main__":
    report = apply_rev8_collision_contract()
    print(f"ORIGIN Atrio rev8 collision contract applied to {len(report)} ring proxies")
    for row in report:
        print(row)
