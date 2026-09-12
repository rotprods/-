"""Read-only Aurora scene QA for Blender 5.2+.

This does not approve art direction. It verifies identity, scale, separation of
collision/streaming debug geometry, and current blockout invariants.
"""
import bpy

EXPECTED_CLAIM = "CLM-AURORA-WORLD-001"


def dims(name):
    o = bpy.data.objects.get(name)
    if not o:
        return None
    return [round(v, 3) for v in o.dimensions]


def run():
    scene = bpy.context.scene
    results = {
        "world_id": scene.get("world_id"),
        "claim_id": scene.get("claim_id"),
        "objects": len(bpy.data.objects),
        "materials": len(bpy.data.materials),
        "dimensions": {
            "terrain": dims("AURORA_MACRO_TERRAIN"),
            "observatory_ring": dims("AUR_OBSERVATORY_PRIMARY_RING"),
            "observatory_mast": dims("AUR_OBSERVATORY_MAST"),
            "aeon_arena": dims("AUR_AEON_ARENA_FLOOR"),
            "peregrino": dims("AUR_PEREGRINO_ROUTE_RECORDER"),
        },
        "counts": {
            "echo_anchors": sum(1 for o in bpy.data.objects if o.name.startswith("AUR_ECHO_ANCHOR_")),
            "aeon_sectors": sum(1 for o in bpy.data.objects if o.name.startswith("AUR_ARENA_ECHO_PYLON_")),
            "orchard_trees": sum(1 for o in bpy.data.objects if o.name.startswith("AUR_ORCHARD_TREE_") and o.name.endswith("_TRUNK")),
            "stream_cells": len(bpy.data.collections.get("10_STREAMING").objects),
            "collision_proxies": len(bpy.data.collections.get("09_COLLISION").objects),
        },
    }

    results["gates"] = {
        "claim_match": results["claim_id"] == EXPECTED_CLAIM,
        "world_match": results["world_id"] == "aurora",
        "observatory_48m": results["dimensions"]["observatory_ring"][:2] == [48.0, 48.0],
        "aeon_arena_50m": results["dimensions"]["aeon_arena"][:2] == [50.0, 50.0],
        "peregrino_dimensions": results["dimensions"]["peregrino"] == [5.8, 2.7, 2.4],
        "three_aeon_sectors": results["counts"]["aeon_sectors"] == 3,
        "collision_hidden": all(o.hide_render for o in bpy.data.collections.get("09_COLLISION").objects),
        "stream_hidden": all(o.hide_render for o in bpy.data.collections.get("10_STREAMING").objects),
        "portable_light_types": all(o.data.type in {"SUN", "SPOT", "POINT"} for o in bpy.data.objects if o.type == "LIGHT"),
    }
    results["pass"] = all(results["gates"].values())
    return results


if __name__ == "__main__":
    print(run())
