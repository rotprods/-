#!/usr/bin/env python3
"""Static validator for the fenced SYLVA R14 streaming hierarchy proposal.

Pure stdlib. Validates before Blender execution:
- four 6 km L2 supercells cover all 16 L3 cells exactly once;
- L2 neighbor graphs are symmetric/geometrically correct;
- hero-core and broad-envelope L3 cell sets match circle-vs-cell intersection;
- L2 references are coverage metadata derived from L3 ownership;
- hero residency is explicitly L3-only, never full-L2 residency;
- Bosque remains a four-L2 coverage hotspot without moving geography;
- HLOD remains contract-only while target backend/hardware are unknown.

PASS here does not mean R14 executed in Blender. Fleet activation + single-writer ownership
remain mandatory before `build_stream_hierarchy_r14.py` may run.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ALL_L3 = {f"X{x}Y{y}" for x in range(4) for y in range(4)}
CELL_BOUNDS = {
    f"X{x}Y{y}": (-6000 + x * 3000, -3000 + x * 3000,
                   -6000 + y * 3000, -3000 + y * 3000)
    for x in range(4) for y in range(4)
}
L2_COORDS = {
    "L2_X0Y0": (0, 0), "L2_X0Y1": (0, 1),
    "L2_X1Y0": (1, 0), "L2_X1Y1": (1, 1),
}


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

    if data.get("hero_residency_granularity") != "L3_ONLY":
        errors.append("HERO_RESIDENCY_NOT_L3_ONLY")
    if data.get("l2_hero_semantics") != "COVERAGE_METADATA_ONLY_NOT_FULL_RESIDENCY":
        errors.append("L2_HERO_SEMANTICS_AMBIGUOUS")

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
        resident_l3 = sorted(row.get("resident_l3_cells", []))
        if resident_l3 != expected_core:
            errors.append(f"{hero_name}:RESIDENT_L3_CELLS")
        if sorted(row.get("region_envelope_cells", [])) != expected_envelope:
            errors.append(f"{hero_name}:ENVELOPE_CELLS")
        derived_core_l2 = sorted({cell_to_l2[c] for c in expected_core})
        derived_env_l2 = sorted({cell_to_l2[c] for c in expected_envelope})
        if sorted(row.get("l2_coverage", [])) != derived_core_l2:
            errors.append(f"{hero_name}:L2_COVERAGE")
        if sorted(row.get("region_envelope_l2_coverage", [])) != derived_env_l2:
            errors.append(f"{hero_name}:ENVELOPE_L2_COVERAGE")
        if row.get("l2_full_residency_implied") is not False:
            errors.append(f"{hero_name}:L2_FULL_RESIDENCY_MUST_BE_FALSE")

    bosque = heroes.get("BOSQUE", {})
    if len(bosque.get("l2_coverage", [])) != 4 or bosque.get("streaming_hotspot") != "GLOBAL_L2_JUNCTION":
        errors.append("BOSQUE_HOTSPOT_NOT_EXPLICIT")
    if len(bosque.get("resident_l3_cells", [])) != 4:
        errors.append("BOSQUE_L3_RESIDENCY_GROUP_MISMATCH")

    hlod = data.get("hlod", {})
    if hlod.get("generation_allowed_now") is not False:
        errors.append("HLOD_PREMATURE_GENERATION_ALLOWED")
    if data.get("status") != "READY_NOT_EXECUTED_WRITER_FENCED":
        errors.append("WRITER_FENCE_STATUS_MISMATCH")
    if data.get("backend") != "ENGINE_TBD":
        errors.append("BACKEND_PREMATURELY_SELECTED")

    return {
        "schema_version": 2,
        "contract": data.get("contract_proposal"),
        "passed": not errors,
        "errors": errors,
        "l2_count": len(l2),
        "l3_partition_count": len(set(flattened)),
        "hero_count": len(heroes),
        "bosque_resident_l3_count": len(bosque.get("resident_l3_cells", [])),
        "bosque_l2_coverage_count": len(bosque.get("l2_coverage", [])),
        "l2_full_residency_implied": any(row.get("l2_full_residency_implied") is not False for row in heroes.values()),
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
