"""Amend R13 stream membership after accepted R16 macro-root taper bounds audit.

Input: revision 16 scene with `SYLVA_MACRO_ROOT_TAPER_R16` applied.
Scope: metadata only. R01 evaluated bounds now cross Y=0 by ~51 m and therefore touch
X0Y2/X1Y2 in addition to its prior four cells. All other primary-root memberships remain valid.

This script does not alter MESH/CURVE geometry, transforms, terrain, routes, collision,
R14 hierarchy, R15 prefetch policy, or PR6 provider content.
"""
from __future__ import annotations

import bpy

AMENDMENT = "SYLVA_STREAM_MEMBERSHIP_R16_AMENDMENT"
TARGET = "SYLVA_ROOT_PRIMARY_R01"
CELLS = ["X0Y0", "X0Y1", "X0Y2", "X1Y0", "X1Y1", "X1Y2"]


def main():
    root = bpy.data.objects.get("SYLVA_WORLD_ROOT")
    obj = bpy.data.objects.get(TARGET)
    if not root or root.get("build_status") != "WAVE1N_MACRO_ROOT_BIOMECH_R16":
        raise RuntimeError("Expected R16 geometry checkpoint")
    if not obj or obj.get("macro_root_biomech_contract") != "SYLVA_MACRO_ROOT_TAPER_R16":
        raise RuntimeError("Missing accepted R16 R01")
    if obj.get("stream_membership_amendment_contract"):
        raise RuntimeError("R16 membership amendment already applied")

    old_cells = obj.get("stream_cells")
    old_count = obj.get("stream_cell_count")
    obj["stream_cells"] = "|".join(CELLS)
    obj["stream_cell_count"] = len(CELLS)
    obj["stream_membership_amendment_contract"] = AMENDMENT
    obj["stream_membership_amendment_reason"] = "R16_TAPER_EVALUATED_BOUNDS_CROSS_Y0_BY_51M"
    obj["stream_membership_previous_cells"] = str(old_cells)
    obj["stream_membership_previous_count"] = int(old_count) if old_count is not None else 4

    root["stream_membership_amendment_contract"] = AMENDMENT
    root["stream_membership_amendment_objects"] = TARGET
    root["build_status"] = "WAVE1N_R16_ROOT_TAPER_MEMBERSHIP_RECONCILED"

    bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
    return {
        "status": "R16_MEMBERSHIP_AMENDMENT_APPLIED",
        "contract": AMENDMENT,
        "object": TARGET,
        "old_cells": old_cells,
        "new_cells": CELLS,
        "geometry_changed": False,
    }


if __name__ == "__main__":
    print(main())
