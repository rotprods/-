#!/usr/bin/env python3
"""Assign backend-agnostic L3 streaming membership to Sylva macro objects.

Claim: CLM-SYLVA-MACRO-001
Input: R12 4x4 L3 terrain/collision tiles plus existing macro geometry.
Output: `stream_cells` metadata on every owned spatial object plus aggregate counts on
`SYLVA_STREAM_L3_*` empties. Terrain tiles have exactly one authoritative owner cell;
other macro objects may belong to multiple cells when their world bounds overlap them.
"""
from __future__ import annotations

import bpy
import re
from mathutils import Vector

CLAIM = "CLM-SYLVA-MACRO-001"
CONTRACT = "SYLVA_STREAM_MEMBERSHIP_R13"
CELLS = {
    f"X{tx}Y{ty}": (-6000 + tx * 3000, -3000 + tx * 3000,
                     -6000 + ty * 3000, -3000 + ty * 3000)
    for tx in range(4) for ty in range(4)
}


def world_bounds(obj):
    if obj.type in {"MESH", "CURVE", "FONT", "SURFACE", "META"} and getattr(obj, "bound_box", None):
        points = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
        return min(p.x for p in points), max(p.x for p in points), min(p.y for p in points), max(p.y for p in points)
    p = obj.matrix_world.translation
    return p.x, p.x, p.y, p.y


def overlaps(bounds, cell, eps=1e-4):
    xmin, xmax, ymin, ymax = bounds
    cx0, cx1, cy0, cy1 = cell
    return xmax >= cx0 - eps and xmin <= cx1 + eps and ymax >= cy0 - eps and ymin <= cy1 + eps


def excluded(obj):
    name = obj.name
    return (
        obj.type in {"CAMERA", "LIGHT"}
        or name.startswith("SYLVA_META_")
        or name == "SYLVA_WORLD_ROOT"
        or name.startswith("SYLVA_STREAM_")
    )


def ensure_meta_collection():
    scene = bpy.context.scene
    collection = bpy.data.collections.get("SYLVA_00_META_STREAMING_R12")
    if collection is None:
        collection = bpy.data.collections.new("SYLVA_00_META_STREAMING_R12")
        scene.collection.children.link(collection)
    return collection


def main():
    assigned = []
    outside = []
    max_cells = 0
    tile_pattern = re.compile(r"_X(\d)Y(\d)$")

    for obj in bpy.data.objects:
        if not obj.name.startswith("SYLVA_") or excluded(obj):
            continue

        if obj.name.startswith("SYLVA_TERRAIN_L3_X") or obj.name.startswith("SYLVA_COL_TERRAIN_L3_X"):
            match = tile_pattern.search(obj.name)
            memberships = [f"X{match.group(1)}Y{match.group(2)}"] if match else []
            policy = "AUTHORITATIVE_TILE_OWNER"
        else:
            bounds = world_bounds(obj)
            memberships = sorted(cid for cid, cell in CELLS.items() if overlaps(bounds, cell))
            policy = "BOUNDING_BOX_OVERLAP"

        memberships = sorted(set(memberships))
        obj["stream_membership_contract"] = CONTRACT
        obj["stream_membership_policy"] = policy
        if memberships:
            obj["stream_cells"] = "|".join(memberships)
            obj["stream_cell_count"] = len(memberships)
            assigned.append((obj.name, memberships))
            max_cells = max(max_cells, len(memberships))
        else:
            obj["stream_cells"] = "OUTSIDE_LOCAL_PATCH"
            obj["stream_cell_count"] = 0
            outside.append(obj.name)

    cell_counts = {cid: 0 for cid in CELLS}
    cross_counts = {cid: 0 for cid in CELLS}
    for _, memberships in assigned:
        for cid in memberships:
            cell_counts[cid] += 1
            if len(memberships) > 1:
                cross_counts[cid] += 1

    for tx in range(4):
        for ty in range(4):
            cid = f"X{tx}Y{ty}"
            stream = bpy.data.objects.get(f"SYLVA_STREAM_L3_{cid}")
            if not stream:
                raise RuntimeError("Missing stream cell " + cid)
            stream["membership_contract"] = CONTRACT
            stream["member_count"] = cell_counts[cid]
            stream["cross_cell_member_count"] = cross_counts[cid]

    meta = bpy.data.objects.new("SYLVA_META_StreamMembershipR13", None)
    ensure_meta_collection().objects.link(meta)
    meta["classification"] = "PROPOSAL_STREAMING_INTERFACE"
    meta["owner_claim"] = CLAIM
    meta["contract"] = CONTRACT
    meta["cell_count"] = 16
    meta["assignment_method"] = "WORLD_BOUNDS_TO_3KM_L3_CELLS"
    meta["terrain_tile_policy"] = "AUTHORITATIVE_SINGLE_CELL"
    meta["cross_cell_policy"] = "MULTI_CELL_MEMBERSHIP_FOR_OVERLAPPING_MACRO_OBJECTS"
    meta["backend"] = "ENGINE_TBD"
    meta["assigned_object_count"] = len(assigned)
    meta["outside_local_patch_count"] = len(outside)
    meta["max_cells_per_object"] = max_cells

    root = bpy.data.objects.get("SYLVA_WORLD_ROOT")
    if root:
        root["build_status"] = "WAVE1K_STREAM_MEMBERSHIP_R13"
        root["stream_membership_contract"] = CONTRACT

    errors = []
    for obj in bpy.data.objects:
        if not obj.name.startswith("SYLVA_") or excluded(obj):
            continue
        if obj.get("stream_membership_contract") != CONTRACT:
            errors.append(obj.name + ":missing_contract")
        if obj.name.startswith("SYLVA_TERRAIN_L3_X") or obj.name.startswith("SYLVA_COL_TERRAIN_L3_X"):
            match = tile_pattern.search(obj.name)
            expected = f"X{match.group(1)}Y{match.group(2)}"
            if obj.get("stream_cells") != expected:
                errors.append(obj.name + ":bad_tile_owner")
            if not obj.parent or obj.parent.name != f"SYLVA_STREAM_L3_{expected}":
                errors.append(obj.name + ":bad_parent")
    if errors:
        raise RuntimeError("Membership QA failed: " + str(errors[:20]))

    bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
    return {
        "assigned_object_count": len(assigned),
        "outside_local_patch": outside,
        "max_cells_per_object": max_cells,
        "cell_counts": cell_counts,
        "cross_cell_counts": cross_counts,
    }


if __name__ == "__main__":
    print(main())
