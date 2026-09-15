"""Resolve semantic World-Compiler requests against the KHEPRI material ArtKit.

Pure Python. The resolver fails closed: wrong world, forbidden contexts, impossible causal/material
combinations and under-specified ambiguous requests are rejected instead of silently choosing a
random or semantically-adjacent material.
"""
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass

from compile_world_artkit import compile_artkit

CONTRACT = "KHP_MATERIAL_WORLD_ARTKIT_RESOLVER_V1"


@dataclass(frozen=True)
class MaterialRequest:
    world_id: str
    context: str
    semantic_role: str
    state: str | None = None
    finish: str | None = None
    scale: str | None = None


def _apps_for_role(artkit: dict, role: str) -> list[dict]:
    return [row for row in artkit["applications"] if role in row["semantic_roles"]]


def resolve(request: MaterialRequest) -> dict:
    artkit = compile_artkit()
    if request.world_id != artkit["world_id"]:
        return {
            "contract": CONTRACT,
            "status": "REJECTED",
            "reason": "WORLD_MISMATCH",
            "request": request.__dict__,
            "expected_world_id": artkit["world_id"],
        }

    role_apps = _apps_for_role(artkit, request.semantic_role)
    if not role_apps:
        return {
            "contract": CONTRACT,
            "status": "REJECTED",
            "reason": "UNKNOWN_SEMANTIC_ROLE",
            "request": request.__dict__,
        }

    # If the requested context is explicitly forbidden by any family that can satisfy the semantic
    # role, reject it as a hard boundary rather than falling through to a generic material.
    if any(request.context in row["forbidden_contexts"] for row in role_apps):
        return {
            "contract": CONTRACT,
            "status": "REJECTED",
            "reason": "FORBIDDEN_CONTEXT",
            "request": request.__dict__,
        }

    candidates = [row for row in role_apps if request.context in row["allowed_contexts"]]
    filters = {
        "state": request.state,
        "manufacturing_finish": request.finish,
        "application_scale": request.scale,
    }
    for key, value in filters.items():
        if value is not None:
            candidates = [row for row in candidates if row[key] == value]

    candidates = sorted(candidates, key=lambda row: row["application_id"])
    if not candidates:
        return {
            "contract": CONTRACT,
            "status": "REJECTED",
            "reason": "NO_VALID_APPLICATION",
            "request": request.__dict__,
        }
    if len(candidates) > 1:
        return {
            "contract": CONTRACT,
            "status": "AMBIGUOUS",
            "reason": "AUTHORED_SELECTOR_REQUIRED",
            "request": request.__dict__,
            "candidate_count": len(candidates),
            "candidate_application_ids": [row["application_id"] for row in candidates],
        }

    row = candidates[0]
    return {
        "contract": CONTRACT,
        "status": "RESOLVED",
        "request": request.__dict__,
        "application": row,
        "artkit_version": artkit["artkit_version"],
        "artkit_sha256": artkit["artkit_sha256"],
    }


def audit() -> dict:
    cases = {
        "heliostat_bronze": (
            MaterialRequest("khepri", "heliostat_structure", "structure", "service_clean", "cast_structural", "architectural"),
            "RESOLVED",
            "KHP_MAT_BRONZE_SYNOD_001::service_clean::cast_structural::architectural",
        ),
        "heliostat_mirror": (
            MaterialRequest("khepri", "heliostat_field", "heliostat_reflector", "calibrated", "broad_reflector", "architectural"),
            "RESOLVED",
            "KHP_MAT_MIRROR_OPTICAL_001::calibrated::broad_reflector::architectural",
        ),
        "decorative_mirror_forbidden": (
            MaterialRequest("khepri", "decorative_mirror", "heliostat_reflector", "calibrated", "broad_reflector", "architectural"),
            "REJECTED",
            "FORBIDDEN_CONTEXT",
        ),
        "cross_world_forbidden": (
            MaterialRequest("vanta", "heliostat_field", "heliostat_reflector", "calibrated", "broad_reflector", "architectural"),
            "REJECTED",
            "WORLD_MISMATCH",
        ),
        "underspecified_crucible": (
            MaterialRequest("khepri", "crisol_de_rakhet", "structure"),
            "AMBIGUOUS",
            "AUTHORED_SELECTOR_REQUIRED",
        ),
    }
    results = {}
    passed = True
    for name, (req, expected_status, expected_detail) in cases.items():
        out = resolve(req)
        if expected_status == "RESOLVED":
            detail = out.get("application", {}).get("application_id")
        else:
            detail = out.get("reason")
        ok = out.get("status") == expected_status and detail == expected_detail
        passed &= ok
        results[name] = {"passed": ok, "status": out.get("status"), "detail": detail}
    return {
        "contract": CONTRACT,
        "cases": results,
        "passed": passed,
        "boundary": "Resolver selects/rejects authored material applications only; it does not place assets or invent story/environment state.",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--audit", action="store_true")
    parser.add_argument("--world-id")
    parser.add_argument("--context")
    parser.add_argument("--semantic-role")
    parser.add_argument("--state")
    parser.add_argument("--finish")
    parser.add_argument("--scale")
    args = parser.parse_args()
    if args.audit:
        print(json.dumps(audit(), indent=2, sort_keys=True))
    else:
        if not (args.world_id and args.context and args.semantic_role):
            parser.error("--world-id, --context and --semantic-role are required unless --audit is used")
        req = MaterialRequest(args.world_id, args.context, args.semantic_role, args.state, args.finish, args.scale)
        print(json.dumps(resolve(req), indent=2, sort_keys=True))
