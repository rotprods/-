#!/usr/bin/env python3
"""Static validator for the fenced SYLVA R14 streaming hierarchy proposal.

Pure stdlib. This validates the proposal before Blender execution:
- four non-overlapping 6 km L2 supercells cover all 16 L3 cells exactly once;
- L2 neighbor graphs are symmetric and geometrically correct;
- hero-core / broad-envelope cell sets exactly match circle-vs-cell intersection;
- hero L2 sets are derived from cell ownership, not manually drifted;
- Bosque is explicitly treated as a 4-L2 hero-residency hotspot;
- HLOD remains contract-only while target backend/hardware are unknown.

Passing this validator does NOT mean R14 has been executed in Blender. The writer fence
must be released by fleet activation before running `build_stream_hierarchy_r14.py`.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

ALL_L3 = {f"X{x}Y{y}" for x in range(4) for y in range(4)}
CELL_BOUNDS = {
    f"X{x}Y{y}": (-6000 + x * 3000, -3000 + x * 3000,
                   -6000 + y * 3000, -3000 + y * 3000)
    for x in range(4) for y in range(4)
}
L2_COORDS = {"L2_X0Y0": (0, 0), "L2_X0Y1": (0, 1), "L2_X1Y0": (1, 0), "L2_X1Y1": (1, 1)}


def circle_rect(cx: float, cy: float, radius: float, bounds: tuple[float, float, float, float]) -> bool:
    x0, x1, y0, y1 = bounds
    qx = min(max(cx, x0), x1)
    qy = min(max(cy, y0), y1)
    return (cx - qx) ** 2 + (cy - qy) ** 2 <= radius ** 2 + 1e-9


def expected_l2_neighbors(name: str, diagonal: bool) -> list[str]:
    x, y = L2_COORDS[name]
    result = []
    for other, (ox, oy) in L2_COORDS.items():
        if other == name:
            continue
        dx, dy = abs(ox - x), abs(oy - y)
        if (diagonal and max(dx, dy) == 1) or (not diagonal and dx + dy == 1):
            result.append(other)
    return sorted(result)


def validate(data: dict) -> dict:
    errors: list[str] = []
    l2 = data.get("l2_supercells", {})
    if set(l2) != set(L2_COORDS):
        errors.append("L2_ID_SET_MISMATCH")

    flattened: list[str] = []
    for name, row in l2.items():
        cells = row.get("l3_cells", [])
        flattened.extend(cells)
        if len(cells) != 4:
            errors.append(f"{name}:L3_CHILD_COUNT")
        if sorted(row.get("neighbors4", [])) != expected_l2_neighbors(name, False):
            errors.append(f"{name}:NEIGHBORS4")
        if sorted(row.get("neighbors8", [])) != expected_l2_neighbors(name, True):
            errors.append(f"{name}:NEIGHBORS8")
    if len(flattened) != 16 or set(flattened) != ALL_L3 or len(set(flattened)) != 16:
        errors.append("L2_DOES_NOT_PARTITION_L3_EXACTLY_ONCE")

    cell_to_l2 = {cell: name for name, row in l2.items() for cell in row.get("l3_cells", [])}
    heroes = data.get("hero_residency_groups", {})
    for hero_name, row in heroes.items():
        center = row.get("center_xyz_m", [])
        if len(center) != 3:
            errors.append(f"{hero_name}:CENTER")
            continue
        cx, cy = float(center[0]), float(center[1])
        core_radius = float(row.get("core_radius_m_proposal", 0))
        envelope_radius = float(row.get("region_envelope_radius_m", 0))
        expected_core = sorted(cid for cid, bounds in CELL_BOUNDS.items() if circle_rect(cx, cy, core_radius, bounds))
        expected_envelope = sorted(cid for cid, bounds in CELL_BOUNDS.items() if circle_rect(cx, cy, envelope_radius, bounds))
        if sorted(row.get("core_cells", [])) != expected_core:
            errors.append(f"{hero_name}:CORE_CELLS")
        if sorted(row.get("region_envelope_cells", [])) != expected_envelope:
            errors.append(f"{hero_name}:ENVELOPE_CELLS")
        derived_core_l2 = sorted({cell_to_l2[c] for c in expected_core})
        derived_env_l2 = sorted({cell_to_l2[c] for c in expected_envelope})
        if sorted(row.get("core_l2", [])) != derived_core_l2:
            errors.append(f"{hero_name}:CORE_L2")
        if sorted(row.get("region_envelope_l2", [])) != derived_env_l2:
            errors.append(f"{hero_name}:ENVELOPE_L2")

    bosque = heroes.get("BOSQUE", {})
    if len(bosque.get("core_l2", [])) != 4 or bosque.get("streaming_hotspot") != "GLOBAL_L2_JUNCTION":
        errors.append("BOSQUE_HOTSPOT_NOT_EXPLICIT")

    hlod = data.get("hlod", {})
    if hlod.get("generation_allowed_now") is not False:
        errors.append("HLOD_PREMATURE_GENERATION_ALLOWED")
    if data.get("status") != "READY_NOT_EXECUTED_WRITER_FENCED":
        errors.append("WRITER_FENCE_STATUS_MISMATCH")
    if data.get("backend") != "ENGINE_TBD":
        errors.append("BACKEND_PREMATURELY_SELECTED")

    return {
        "schema_version": 1,
        "contract": data.get("contract_proposal"),
        "passed": not errors,
        "errors": errors,
        "l2_count": len(l2),
        "l3_partition_count": len(set(flattened)),
        "hero_count": len(heroes),
        "bosque_l2_count": len(bosque.get("core_l2", [])),
        "truth": "Static proposal validation only; no Blender R14 mutation is implied."
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("proposal", type=Path)
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args(argv)
    data = json.loads(args.proposal.read_text(encoding="utf-8"))
    report = validate(data)
    encoded = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(encoded, encoding="utf-8")
    sys.stdout.write(encoded)
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
