# KHEPRI World Macro — recoverable handoff

AGENT: `AGENT-KHEPRI-WMACRO-001`  
SESSION: `SESSION-20260912-KHEPRI-001`  
CLAIM: `CLM-KHEPRI-WMACRO-001`  
BRANCH: `art/world-khepri-001`  
PR: `#8` draft  
LATEST QUALIFIED MAIN: `758a9b6326a7d061f1e304abe9b1593b6b2d1a66`  
MAIN PUSH GAUNTLET: `34720800915` SUCCESS  
MASTER 3D PROJECT: `040f0c45-83a7-483c-9ee7-1e31c640a587` rev `4`  
COLD 3D PROJECT: `4c01fdbb-7093-4229-9a49-8237583280bc` rev `3`  
CLAIM STATUS: **KEEP / REVIEW**

## NORTH STAR
Deliver KHEPRI `WORLD_MACRO / PLANETARY_FOUNDATION` as a reproducible metre-scale Blender foundation preserving canon, separating L0/L1/L2 scale, exposing stable cross-domain interfaces, and never promoting proposal/blockout values to canon/final art without their gates.

## CURRENT TRUTH
This is a **reproducible world-macro blockout**. It is not KHEPRI DONE, not AAAA-qualified final art, not engine-integrated production terrain and not a human-approved art target.

## VERIFIED MASTER R4
- 77 objects / 6 mesh datablocks / 5 materials / 1 curve.
- 5,697 unique mesh vertices / 11,092 unique triangles.
- Terrain: `6400 × 4800 × 228.805 m`.
- 1.85 m human QA reference.
- 32 heliostat panels → one shared panel mesh.
- 32 heliostat masts → one shared mast mesh.
- Zero duplicate object names/asset IDs, non-finite transforms, negative scales or non-unit mesh scales.
- `.blend`: `1,379,495 B`, etag `6d81d2c81e19a841056f018926e32944`.
- GLB: `822,272 B`, etag `40d610951c4f0d8d3d83c7d4e67519dc`.

## R3 CAMERA / SCALE GAUNTLET
R2 had two real defects:
1. default Blender `clip_end=1000 m` for kilometre-scale targets;
2. human scale guide outside gameplay frame.

Fixed by versioned generator/validator:
- overview 32 mm / 12 km clip;
- gameplay 38 mm / 8 km clip;
- 1.85 m guide at 30 m on view axis, ~84.7 px high at 720p;
- all 4 route anchors in overview frame and clip range.

R3 clean rebuild master/cold semantic SHA matched:
`7d80db30181cde1bded58d357384095c07cce0d2ca65e1b728b841aa93b252ca`.

## R4 ROUTE GAUNTLET
R3 slope context was moderate (route p95 `10.08°`, max `10.64°`), but the four-point route ribbon was geometrically wrong:
- min clearance `-23.36 m`;
- max `+83.22 m`;
- 152/575 audit samples below terrain.

`refine_route_r4.py` replaced it with a deterministic terrain-conforming 576-point POLY interface at 7 m target clearance.

Post-fix audit (`khepri.route.clearance.audit.r4`):
- 2,876 samples including between route points;
- min `6.9963 m`, max `7.0043 m`, mean `7.0001 m`;
- maximum target error `4.3 mm`;
- below-terrain samples `0`;
- samples outside 6–8 m band `0`.

R4 cold-rebuild semantic SHA master/cold:
`04c527c61ee814753f09e9c0f651495ad80ed51aafc48c77b6acb4e82a3612ec`.
Master/cold artifact sizes also match exactly: `.blend 1,379,495 B`, GLB `822,272 B`.

## R4 VISUAL EVIDENCE
Operation `khepri.visual.r4.gauntlet` succeeded at 1280×720 Eevee:
- overview artifact `6526469581c767eb9e18ca73de270031`, `700,678 B`;
- gameplay artifact `f07432f0acc50e5ccddab570cbae0f6f`, `747,184 B`.

Machine visual gates pass, but this runtime still cannot inspect signed provider PNG pixels. Human GATE-ART remains pending.

## R4 HELIOSTAT / PORTABILITY QA
Heliostat contact audit:
- mast ground contact error range `−0.000004…+0.000004 m`;
- panel centers consistently 6 m above mast top;
- minimum mast spacing 490 m;
- one shared mast mesh and one shared panel mesh.

Portable blockout audit:
- 5 materials, Principled BSDF + Material Output only;
- zero external images or absolute image paths;
- portable SUN light only;
- zero unsupported light types;
- zero unused mesh/curve/material/camera/light datablocks.

## CI / FLEET EXACT DIAGNOSIS
Fleet claim is `active` in `ops/fleet/registry.json`.

Latest inspected PR merge run: `34720826636`.
- **82/82 Python tests PASS**.
- Fleet/governance/studio tests PASS.
- Only failure: `python3 tools/project_control.py check` → `manifest drift`.
- Reported drift is KHEPRI-owned paths only.
- Native Godot stages were skipped only because the manifest check exited first.

Therefore the remaining producer CI blocker is exactly:
`EXACT_MANIFEST_REFRESH_IN_REAL_COMBINED_CHECKOUT`.

Do not rerun CI unchanged: it would spend Actions while reproducing the same deterministic failure.

## BLOCKED
### HUMAN_VISUAL_REVIEW
Provider renders and interactive scene exist; pixel-level human/art review remains open.

### BINARY_PERSISTENCE_TRANSPORT
Provider `.blend`/GLB are verified and recoverable but not local/repo/LFS persisted with SHA256/native receipt. Signed provider URL is not sufficient under fleet policy.

### EXACT_MANIFEST_REFRESH_IN_REAL_COMBINED_CHECKOUT
Required transaction:
1. start from latest exact `main` whose push Gauntlet is terminal SUCCESS;
2. overlay only owned KHEPRI paths:
   - `production/claims/CLM-KHEPRI-WMACRO-001.yaml`
   - `production/worlds/khepri/**`
   - `art_source/khepri/world_macro/**`
3. run `python3 tools/project_control.py refresh` on real combined checkout;
4. run fleet `guard-git` against current registry epoch/digest;
5. do not carry stale producer `STATE/PLAN/AGENTS/HANDOFF` projections;
6. require PR #8 exact-SHA Gauntlet SUCCESS.

## IMPORTANT DECISIONS
- Canon gravity remains `0.63 g`; proposed 5,224 km radius remains reversible ADR, not canon.
- Local tangent metre-scale cells replace any monolithic gameplay planet mesh.
- `SHADE`, `GLASS_SEA`, `CRUCIBLE`, `RAKHET` are cross-domain route interfaces, not final route art.
- Final architecture, materials, characters, fauna, vehicles and RA-KHET are separate claim leaves.
- Semantic fingerprints canonicalize irrelevant primitive vertex index order while preserving actual geometry/topology-by-coordinate, transforms, materials, metadata and camera contracts.

## NEXT 3 ACTIONS
1. Consume the integrator/real-checkout transaction for exact MANIFEST refresh and require PR #8 exact-SHA Gauntlet SUCCESS.
2. Recover R4 `.blend`/GLB on a binary-capable worker, compute local SHA256, persist native receipt and execute fleet delivery gate.
3. Obtain human/pixel GATE-ART review of the R4 overview/gameplay renders before any promotion beyond blockout.

Until P0 #1 closes, **do not add new world density**. QA/receipts may continue, ownership scope remains atomic.

CLAIM STATUS: **KEEP / REVIEW**
