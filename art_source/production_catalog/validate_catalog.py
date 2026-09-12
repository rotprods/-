#!/usr/bin/env python3
"""Validate source coverage, dependency references and honest delivery status.

This is an offline catalog gate. It neither opens Blender nor certifies the art.
"""
from __future__ import annotations
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent

def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def digest(path: Path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def validate():
    errors = []
    source_path = ROOT / "design/EXOVANT_DATA.json"
    source = read(source_path)
    manifest = read(HERE / "ASSET_MANIFEST.json")
    profiles = read(HERE / "CATEGORY_PROFILES.json")["profiles"]
    worlds = read(HERE / "WORLD_ART_DIRECTION.json")["worlds"]
    modules = read(HERE / "TERRA_MODULES.json")["modules"]
    expected = source["assets"]
    rows = manifest["assets"]
    ids = [row["id"] for row in rows]
    expected_ids = [row["id"] for row in expected]
    def require(condition, message):
        if not condition:
            errors.append(message)
    require(ids == expected_ids, "Canonical IDs/order differ from source catalog")
    require(len(ids) == len(set(ids)), "Duplicate catalog IDs")
    require(len(rows) == source["meta"]["asset_row_count"] == 318, "Expected 318 source rows")
    require(manifest["source_catalog_sha256"] == digest(source_path), "Source catalog hash changed")
    require(manifest["source_bible_sha256"] == digest(ROOT / "design/EXOVANT_BIBLIA.md"), "Design bible hash changed")
    require({w["id"] for w in worlds} == {w["id"] for w in source["worlds"]}, "World direction coverage differs")
    require(len(worlds) == 12 and len({w["id"] for w in worlds}) == 12, "Expected exactly 12 distinct worlds")
    expected_by_id = {row["id"]: row for row in expected}
    row_by_id = {row["id"]: row for row in rows}
    known = set(ids) | set(manifest["external_dependency_ids"])
    dependency_graph = {}
    categories = Counter(row["category"] for row in rows)
    require(dict(categories) == manifest["counts"]["categories"], "Manifest category summary drift")
    require(manifest["counts"]["rows"] == len(rows), "Manifest row summary drift")
    require(set(profiles) == set(categories), "Category profiles do not cover exactly the source categories")
    require(manifest["counts"]["completed_models_claimed"] == 0, "Design catalog must not claim completed models")
    for row in rows:
        ident = row["id"]
        original = expected_by_id.get(ident)
        if original is None:
            continue
        for key in ("name", "category", "world"):
            require(row[key] == original[key], f"{ident}: source {key} changed")
        require(row["scope"]["quantity_target"] == original["quantity"], f"{ident}: quantity drift")
        require(row["scope"]["unit"] == original["unit"], f"{ident}: unit drift")
        require(row["scope"]["phase_from_design"] == original["phase"], f"{ident}: phase drift")
        source_row_hash = hashlib.sha256(json.dumps(original, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        require(row["source_row_sha256"] == source_row_hash, f"{ident}: source row hash mismatch")
        expected_deps = [d.strip() for d in original["dependencies"].split(";") if d.strip() and d.strip() != "NONE"]
        require(row["dependencies"]["catalog"] == expected_deps, f"{ident}: inherited dependencies changed")
        deps = row["dependencies"]["catalog"] + row["dependencies"]["production"]
        require(all(d in known for d in deps), f"{ident}: unresolved dependency {set(deps) - known}")
        require(ident not in deps, f"{ident}: self dependency")
        dependency_graph[ident] = [d for d in deps if d in row_by_id]
        require(row["technical_profile_ref"] == row["category"], f"{ident}: invalid technical profile reference")
        require(row["status"] == "planned", f"{ident}: catalog is a design projection, not a production receipt")
        require(not row["evidence"], f"{ident}: add candidate evidence in an explicit production record, not this design snapshot")
        require(row["delivery_status_ref"] == "planned_no_delivery", f"{ident}: unknown delivery template")
        require(not any(manifest["delivery_templates"][row["delivery_status_ref"]].values()), f"{ident}: planned row claims delivery evidence")
        require(row["priority"] in range(4), f"{ident}: invalid priority")
        design = row["design"]
        for field in ("function", "silhouette", "scale", "specific_acceptance"):
            require(bool(design.get(field)), f"{ident}: empty {field} brief")
        if row["category"] in {"biota", "npc", "enemy", "boss", "weapon", "vehicle", "armor", "tool"} and row["world"] != "shared":
            require(bool(design["materials"]), f"{ident}: physical entity without material intent")
        if "child_brief_names" in design:
            require(len(design["child_brief_names"]) == row["scope"]["quantity_target"], f"{ident}: child brief count differs from family target")
            require(len(set(design["child_brief_names"])) == len(design["child_brief_names"]), f"{ident}: duplicate child names")
        if "module_allocation" in design:
            require(sum(design["module_allocation"].values()) == row["scope"]["quantity_target"], f"{ident}: module allocation differs from target")
        if design.get("anatomy_family") == "static_growth":
            require(row.get("rig_override") is not None, f"{ident}: static biota needs explicit exception to inherited mobile rig gate")
    # Dependencies may exist only as design contracts; reject cycles regardless of status.
    visiting, visited = set(), set()
    def visit(node, path):
        if node in visiting:
            errors.append("Dependency cycle: " + " -> ".join(path + [node]))
            return
        if node in visited:
            return
        visiting.add(node)
        for dep in dependency_graph.get(node, []):
            visit(dep, path + [node])
        visiting.remove(node)
        visited.add(node)
    for ident in ids:
        visit(ident, [])
    require(len(modules) == 28, "Expected 28 scoped Terra module briefs")
    require(len({m["id"] for m in modules}) == len(modules), "Duplicate Terra child module IDs")
    for module in modules:
        ident = module["id"]
        require(module["parent_catalog_id"] in row_by_id, f"{ident}: missing canonical parent")
        require(row_by_id.get(module["parent_catalog_id"], {}).get("world") == "terra", f"{ident}: child parent outside Terra")
        require(module["status"] == "planned" and not module["actual_artifacts"], f"{ident}: brief must not claim a model")
        require(all(isinstance(v, (int, float)) and v > 0 for v in module["dimension_target_m"].values()), f"{ident}: invalid proposed dimensions")
    files = ["ASSET_MANIFEST.json", "CATEGORY_PROFILES.json", "WORLD_ART_DIRECTION.json", "TERRA_MODULES.json"]
    return dict(
        schema_version=1,
        checked_at=datetime.now(timezone.utc).isoformat(),
        gate="offline_catalog_coverage_and_contracts",
        passed=not errors,
        checks=["exact source IDs/order/name/world/category/quantity/unit/phase/acceptance",
                "full source and per-row hashes", "21 category profiles and 12 world directions",
                "dependency references, exceptions and acyclic graph", "family allocations and child names",
                "28 Terra child briefs and canonical parents", "planned status without artifact/approval claims"],
        rows=len(rows), worlds=len(worlds), categories=dict(categories),
        terra_module_briefs=len(modules), terra_priority_zero_briefs=sum(m["batch_priority"] == 0 for m in modules),
        planet_prop_brief_names=sum(len(w["prop_brief_names"]) for w in worlds),
        candidate_models_accepted_by_this_gate=0,
        limitations=["Does not run Blender, inspect geometry or certify AAA quality",
                     "Does not measure hardware performance or complete any human gate",
                     "Only validates this design snapshot; production records are separate"],
        file_sha256={name: digest(HERE / name) for name in files}, errors=errors)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-report", action="store_true", help="Write COVERAGE_EVIDENCE.json next to the catalog")
    args = parser.parse_args()
    try:
        report = validate()
    except (OSError, KeyError, TypeError, ValueError) as error:
        print(f"Catalog validation failed: {error}", file=sys.stderr)
        return 1
    if args.write_report:
        (HERE / "COVERAGE_EVIDENCE.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: report[k] for k in ("passed", "rows", "worlds", "terra_module_briefs", "errors")}, ensure_ascii=False))
    return 0 if report["passed"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
