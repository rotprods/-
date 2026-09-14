#!/usr/bin/env python3
"""Prepare SYLVA PRIME L2/L3 streaming hierarchy metadata on accepted R13.

DO NOT execute while `REMOTE_WRITER_FENCE.json` is FROZEN_PENDING_FLEET_ACTIVE.
Execution precondition: fleet registry must publish CLM-SYLVA-MACRO-001 as active
with current owner ACK, and exactly one writer session must own the primary project wave.

This script is backend-neutral. It creates no HLOD meshes and does not change terrain,
routes, hero geometry, collisions or canonical geography.

Important semantic rule: hero residency is L3-granular. L2 references are coverage/HLOD
metadata only; a hero crossing several L2 supercells does not imply all those L2s must be
fully resident.
"""
from __future__ import annotations

import bpy

CLAIM = "CLM-SYLVA-MACRO-001"
CONTRACT = "SYLVA_STREAM_HIERARCHY_R14"
PREFETCH = "ADJACENT_8_PLUS_L3_HERO_RESIDENCY_GROUP"

L2_MAP = {
    "L2_X0Y0": ["X0Y0", "X0Y1", "X1Y0", "X1Y1"],
    "L2_X0Y1": ["X0Y2", "X0Y3", "X1Y2", "X1Y3"],
    "L2_X1Y0": ["X2Y0", "X2Y1", "X3Y0", "X3Y1"],
    "L2_X1Y1": ["X2Y2", "X2Y3", "X3Y2", "X3Y3"],
}
L2_CENTERS = {
    "L2_X0Y0": (-3000, -3000, 0),
    "L2_X0Y1": (-3000, 3000, 0),
    "L2_X1Y0": (3000, -3000, 0),
    "L2_X1Y1": (3000, 3000, 0),
}
HERO = {
    "PUERTO": {
        "region": "SYLVA_STREAM_REGION_PUERTO_INJERTO",
        "center_cell": "X0Y1",
        "core_radius_m": 550.0,
        "resident_l3_cells": ["X0Y1", "X1Y1"],
        "l2_coverage": ["L2_X0Y0"],
    },
    "BOSQUE": {
        "region": "SYLVA_STREAM_REGION_BOSQUE_FRASES",
        "center_cell": "X2Y2",
        "core_radius_m": 200.0,
        "resident_l3_cells": ["X1Y1", "X1Y2", "X2Y1", "X2Y2"],
        "l2_coverage": ["L2_X0Y0", "L2_X0Y1", "L2_X1Y0", "L2_X1Y1"],
    },
    "VESPER": {
        "region": "SYLVA_STREAM_REGION_CAMARA_VESPER",
        "center_cell": "X3Y2",
        "core_radius_m": 400.0,
        "resident_l3_cells": ["X2Y2", "X3Y2"],
        "l2_coverage": ["L2_X1Y1"],
    },
}


def neighbor_graph(size: int, diagonal: bool):
    graph = {}
    for x in range(size):
        for y in range(size):
            cell = f"X{x}Y{y}"
            neighbors = []
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    if dx == 0 and dy == 0:
                        continue
                    if not diagonal and abs(dx) + abs(dy) != 1:
                        continue
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < size and 0 <= ny < size:
                        neighbors.append(f"X{nx}Y{ny}")
            graph[cell] = sorted(neighbors)
    return graph


def l2_neighbor_graph(diagonal: bool):
    coords = {
        "L2_X0Y0": (0, 0), "L2_X0Y1": (0, 1),
        "L2_X1Y0": (1, 0), "L2_X1Y1": (1, 1),
    }
    graph = {}
    for name, (x, y) in coords.items():
        neighbors = []
        for other, (ox, oy) in coords.items():
            if other == name:
                continue
            dx, dy = abs(ox - x), abs(oy - y)
            if (diagonal and max(dx, dy) == 1) or (not diagonal and dx + dy == 1):
                neighbors.append(other)
        graph[name] = sorted(neighbors)
    return graph


def ensure_collection(name: str):
    scene = bpy.context.scene
    collection = bpy.data.collections.get(name)
    if collection is None:
        collection = bpy.data.collections.new(name)
        scene.collection.children.link(collection)
    return collection


def main():
    # Scene-side input guard. External fleet-active readback is still mandatory before mutation.
    root = bpy.data.objects.get("SYLVA_WORLD_ROOT")
    if not root or root.get("build_status") != "WAVE1K_STREAM_MEMBERSHIP_R13":
        raise RuntimeError("Expected accepted R13 scene before R14 hierarchy")
    if bpy.data.objects.get("SYLVA_META_StreamHierarchyR14"):
        raise RuntimeError("R14 hierarchy already exists")

    l3_4 = neighbor_graph(4, diagonal=False)
    l3_8 = neighbor_graph(4, diagonal=True)
    l2_4 = l2_neighbor_graph(diagonal=False)
    l2_8 = l2_neighbor_graph(diagonal=True)
    cell_to_l2 = {cell: l2 for l2, cells in L2_MAP.items() for cell in cells}

    collection = ensure_collection("SYLVA_00_META_STREAMING_R12")
    created = []
    for l2, l3_cells in L2_MAP.items():
        obj = bpy.data.objects.new("SYLVA_STREAM_" + l2, None)
        collection.objects.link(obj)
        obj.location = L2_CENTERS[l2]
        obj.empty_display_type = "CUBE"
        obj.empty_display_size = 300.0
        obj["classification"] = "PROPOSAL_L2_SUPERCELL"
        obj["owner_claim"] = CLAIM
        obj["stream_hierarchy_contract"] = CONTRACT
        obj["size_m"] = 6000
        obj["l3_children"] = "|".join(l3_cells)
        obj["neighbors4"] = "|".join(l2_4[l2])
        obj["neighbors8"] = "|".join(l2_8[l2])
        obj["hlod_id_proposal"] = "SYLVA_HLOD_" + l2
        obj["hlod_status"] = "CONTRACT_ONLY_TARGET_BACKEND_PENDING"
        created.append(obj.name)

    for x in range(4):
        for y in range(4):
            cid = f"X{x}Y{y}"
            cell = bpy.data.objects.get("SYLVA_STREAM_L3_" + cid)
            if not cell:
                raise RuntimeError("Missing R13 L3 cell " + cid)
            cell["stream_hierarchy_contract"] = CONTRACT
            cell["l2_supercell"] = cell_to_l2[cid]
            cell["neighbors4"] = "|".join(l3_4[cid])
            cell["neighbors8"] = "|".join(l3_8[cid])
            cell["prefetch_policy"] = PREFETCH

    # Hero residency overlay is L3-only. L2 is coverage metadata, not a full-residency command.
    for hero_id, spec in HERO.items():
        region = bpy.data.objects.get(spec["region"])
        if not region:
            raise RuntimeError("Missing hero stream region: " + spec["region"])
        region["stream_hierarchy_contract"] = CONTRACT
        region["hero_core_radius_m_proposal"] = spec["core_radius_m"]
        region["authoritative_center_cell"] = spec["center_cell"]
        region["hero_resident_l3_cells"] = "|".join(spec["resident_l3_cells"])
        region["hero_l2_coverage"] = "|".join(spec["l2_coverage"])
        region["hero_l2_full_residency_implied"] = False
        region["hero_residency_policy"] = "L3_OVERLAY_DO_NOT_MOVE_GEOGRAPHY"
        region["hero_core_basis"] = "OBSERVED_GEOMETRY_EXTENT_PLUS_50M_ROUNDED25"

    meta = bpy.data.objects.new("SYLVA_META_StreamHierarchyR14", None)
    collection.objects.link(meta)
    meta["classification"] = "PROPOSAL_STREAMING_INTERFACE"
    meta["owner_claim"] = CLAIM
    meta["contract"] = CONTRACT
    meta["l2_count"] = 4
    meta["l2_size_m"] = 6000
    meta["l3_count"] = 16
    meta["l3_size_m"] = 3000
    meta["prefetch_policy"] = PREFETCH
    meta["hero_residency_granularity"] = "L3_ONLY"
    meta["l2_hero_semantics"] = "COVERAGE_METADATA_ONLY_NOT_FULL_RESIDENCY"
    meta["backend"] = "ENGINE_TBD"
    meta["hlod_status"] = "CONTRACT_ONLY_TARGET_BACKEND_PENDING"
    meta["bosque_hotspot"] = "HERO_CORE_SPANS_ALL_FOUR_L2_SUPERCELLS_BUT_ONLY_4_L3_RESIDENT"
    meta["center_tie_policy"] = "HALF_OPEN_BINS_BOUNDARY_TO_POSITIVE_AXIS"

    root["build_status"] = "WAVE1L_STREAM_HIERARCHY_R14"
    root["stream_hierarchy_contract"] = CONTRACT

    flattened = [cell for cells in L2_MAP.values() for cell in cells]
    expected_l3 = {f"X{x}Y{y}" for x in range(4) for y in range(4)}
    if len(flattened) != 16 or set(flattened) != expected_l3 or len(set(flattened)) != 16:
        raise RuntimeError("L2 mapping does not cover all L3 cells exactly once")
    for graph in (l3_4, l3_8):
        for a, neighbors in graph.items():
            for b in neighbors:
                if a not in graph[b]:
                    raise RuntimeError(f"Asymmetric L3 graph: {a}/{b}")
    for graph in (l2_4, l2_8):
        for a, neighbors in graph.items():
            for b in neighbors:
                if a not in graph[b]:
                    raise RuntimeError(f"Asymmetric L2 graph: {a}/{b}")
    for spec in HERO.values():
        if any(cell not in cell_to_l2 for cell in spec["resident_l3_cells"]):
            raise RuntimeError("Hero residency references unknown L3 cell")

    bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
    return {
        "contract": CONTRACT,
        "l2_nodes_created": created,
        "l3_cells_enriched": 16,
        "hero_overlays": len(HERO),
        "bosque_resident_l3_count": len(HERO["BOSQUE"]["resident_l3_cells"]),
        "bosque_l2_coverage_count": len(HERO["BOSQUE"]["l2_coverage"]),
        "l2_full_residency_implied": False,
        "geometry_changed": False,
    }


if __name__ == "__main__":
    print(main())
