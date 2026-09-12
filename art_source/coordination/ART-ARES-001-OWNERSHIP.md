# ART-ARES-001 · ARES IX world production ownership

Date: 2026-09-12. User directive: run a bounded, multi-week 3D world-production stream for one EXOVANT 2950 world, coordinated with parallel world/art agents.

Base: `4c2fa044080004609ea6df45f34b2a784536507a` (`main` observed before branch creation).
Branch: `art/ares-ix-world-001`.
World: `ares` / **ARES IX**.
Canonical source refs: `AGENTS.md`, `_project_intelligence/STATE.json`, `_project_intelligence/PLAN.json`, `design/EXOVANT_DATA.json`, `docs/ART_PRODUCTION.md`, `learning/.../LRN-EXO-20260912-BLENDER.json`.

## Owned paths

- `art_source/worlds/ares_ix/**`
- `art_source/coordination/ART-ARES-001-OWNERSHIP.md`

All runtime Godot scenes/scripts, Terra asset paths, existing portal sources, shared project STATE/PLAN/HANDOFF and other agents' branches are outside this branch's direct edit scope. Shared-state changes are proposed through the PR/handoff and must be reconciled by the integrator against the newest `main`.

## Remote Blender

- Route: Higgsfield 3D Jutsu `bpy`, per persisted project learning `LRN-EXO-20260912-BLENDER`.
- Dedicated project: `1fe12f5b-3c86-42ca-a04a-1c8c36f509d3` (`EXOVANT 2950 — ARES IX World Master — ART-ARES-001`).
- Blender observed: `5.2.0 LTS`.
- Initial scene: empty, revision `0`, scene sequence `0`, metric scale `1 BU = 1 m`.
- Delivery contract: preserve editable `.blend`, generator/source Python, portable GLB/export, previews and evidence. Remote visual success is not engine acceptance.

## Concurrency contract

Parallel world agents MUST use branch-per-world and disjoint owned paths. A single integration authority reconciles shared files into `main`; no agent force-updates refs. Cross-world reusable assets are proposed by manifest ID and integrated only after collision/name/style review. Local scene locks are not distributed repository locks.

## Scope status

`STARTED / BLOCKOUT`. No claim that ARES IX, its characters or its planet are production-complete. First checkpoint establishes world scale, art language, complete asset registry, master Blender scene hierarchy, regional blockout, hero POIs, NPC/enemy/ecology proxies, quality gates and a deterministic generator.