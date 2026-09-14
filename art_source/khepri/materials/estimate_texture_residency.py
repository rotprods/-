"""KHEPRI texture residency planning estimator.

Pure planning math only. It does NOT qualify target hardware or choose production resolution.
Uses mip-chain geometric-series approximation and a configurable effective VRAM compression ratio.
Actual imported .ctex/GPU residency must be measured on the target renderer/hardware.
"""
from __future__ import annotations

import argparse
import json


def bytes_rgba8_with_mips(size: int) -> float:
    # Full square mip chain approaches 4/3 of base level.
    return size * size * 4.0 * (4.0 / 3.0)


def estimate(size: int, maps: int, compression_ratio: float, resident_materials: int = 1) -> dict:
    if size <= 0 or maps <= 0 or resident_materials <= 0 or compression_ratio <= 0:
        raise ValueError("all inputs must be positive")
    per_map = bytes_rgba8_with_mips(size) / compression_ratio
    total = per_map * maps * resident_materials
    return {
        "resolution": [size, size],
        "maps_per_material": maps,
        "resident_materials": resident_materials,
        "assumed_effective_compression_ratio": compression_ratio,
        "per_map_mib": round(per_map / 1048576.0, 3),
        "per_material_mib": round(per_map * maps / 1048576.0, 3),
        "total_mib": round(total / 1048576.0, 3),
        "status": "PLANNING_ESTIMATE_ONLY",
    }


def matrix() -> list[dict]:
    rows = []
    for size in (512, 1024, 2048, 4096):
        for ratio in (4.0, 6.0):
            rows.append(estimate(size=size, maps=3, compression_ratio=ratio, resident_materials=24))
    return rows


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--size", type=int)
    parser.add_argument("--maps", type=int, default=3)
    parser.add_argument("--compression-ratio", type=float, default=4.0)
    parser.add_argument("--resident-materials", type=int, default=1)
    parser.add_argument("--matrix", action="store_true")
    args = parser.parse_args()
    result = matrix() if args.matrix else estimate(args.size or 1024, args.maps, args.compression_ratio, args.resident_materials)
    print(json.dumps(result, indent=2, sort_keys=True))
