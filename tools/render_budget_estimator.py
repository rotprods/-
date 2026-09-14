#!/usr/bin/env python3
"""Estimate offline render compute from measured representative frame timings.

The tool intentionally contains no vendor prices. Supply the current rate you actually intend
to pay. Resolution alone is never used to invent seconds/frame.
"""
from __future__ import annotations

import argparse
import json
import math


def estimate(duration_s, fps, easy_s, median_s, worst_s, workers=1,
             parallel_efficiency=0.90, device_hour_rate=0.0, fixed_cost=0.0,
             storage_gb=0.0, storage_gb_rate=0.0, artist_hours=0.0,
             artist_hour_rate=0.0):
    if duration_s <= 0 or fps <= 0:
        raise ValueError("duration_s and fps must be > 0")
    if min(easy_s, median_s, worst_s) < 0:
        raise ValueError("measured seconds/frame cannot be negative")
    if workers < 1:
        raise ValueError("workers must be >= 1")
    if not (0 < parallel_efficiency <= 1):
        raise ValueError("parallel_efficiency must be in (0, 1]")
    frames = math.ceil(duration_s * fps)
    expected_spf = 0.20 * easy_s + 0.60 * median_s + 0.20 * worst_s
    device_hours = frames * expected_spf / 3600.0
    wall_hours = device_hours / (workers * parallel_efficiency)
    render_compute_cost = device_hours * device_hour_rate
    storage_cost = storage_gb * storage_gb_rate
    labor_cost = artist_hours * artist_hour_rate
    return {
        "frames": frames,
        "benchmark_seconds_per_frame": {
            "easy": easy_s,
            "median": median_s,
            "worst": worst_s,
            "expected_weighted": expected_spf,
        },
        "compute": {
            "single_device_equivalent_hours": device_hours,
            "workers": workers,
            "parallel_efficiency": parallel_efficiency,
            "estimated_wall_hours": wall_hours,
        },
        "cost": {
            "device_hour_rate": device_hour_rate,
            "render_compute": render_compute_cost,
            "fixed": fixed_cost,
            "storage": storage_cost,
            "labor": labor_cost,
            "total": fixed_cost + render_compute_cost + storage_cost + labor_cost,
        },
        "warning": "Estimate quality is bounded by measured benchmark-frame representativeness and the supplied live rate."
    }


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--duration", type=float, required=True)
    p.add_argument("--fps", type=float, required=True)
    p.add_argument("--easy", type=float, required=True, help="measured seconds/frame")
    p.add_argument("--median", type=float, required=True, help="measured seconds/frame")
    p.add_argument("--worst", type=float, required=True, help="measured seconds/frame")
    p.add_argument("--workers", type=int, default=1)
    p.add_argument("--parallel-efficiency", type=float, default=0.90)
    p.add_argument("--device-hour-rate", type=float, default=0.0)
    p.add_argument("--fixed-cost", type=float, default=0.0)
    p.add_argument("--storage-gb", type=float, default=0.0)
    p.add_argument("--storage-gb-rate", type=float, default=0.0)
    p.add_argument("--artist-hours", type=float, default=0.0)
    p.add_argument("--artist-hour-rate", type=float, default=0.0)
    a = p.parse_args(argv)
    print(json.dumps(estimate(a.duration, a.fps, a.easy, a.median, a.worst,
                              a.workers, a.parallel_efficiency, a.device_hour_rate,
                              a.fixed_cost, a.storage_gb, a.storage_gb_rate,
                              a.artist_hours, a.artist_hour_rate), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
