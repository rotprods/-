# STATUS — CLM-SYLVA-MACRO-001

**Agent:** `AGENT-SYLVA-MACRO-01`  
**Branch:** `art/world-sylva-prime-macro-001`  
**Primary Blender:** `05dce898-753d-4ff6-a4b0-31757dc868d8` @ **revision 15**  
**State:** `IN_PROGRESS / VERIFIED R15 TECHNICAL CHECKPOINT`  
**Claim:** `ACTIVE / KEEP`  
**Fleet epoch:** `1` · owner ACK published  
**Latest main synchronized:** `26ae20f5d1b47d1efa0d54b20124ed93cbc0b43e` via PR #26

## Current truth

This claim owns SYLVA PRIME's metre-scale macro/regional foundation: causal terrain, region placement, terrain-aware route interfaces, VESPER macro encounter layout, streaming/collision contracts and consumer sockets toward the neural-root provider. It is **not final world art**.

Current accepted scene is R15. R14 established backend-neutral L2/L3 hierarchy; R15 corrected its prefetch semantics so **no runtime prefetch policy is falsely approved** before native IO/residency measurements.

PR #6 / `CLM-SYLVA-PROC-NROOT-001` exclusively owns reusable meso neural-root modules. Final VESPER, NPCs, fauna/flora, architecture/interiors, vehicle, final materials/microterrain/foliage, gameplay and final technical-art qualification remain outside this claim.

## Wave lineage

- r1 — 12 km local terrain blockout + canonical region foundations.
- r2 — portable lighting/review cameras.
- r3 — camera-range correction + render-signal QA.
- r4 — L3 cell interfaces, regional envelopes, sockets and collision interfaces.
- r5 — canon correction: 3 VESPER terraces + 2 wide connectors.
- r6 — causal biogeomorphic macro terrain.
- r7 — root-kit consumer basis + provider-pivot blocker.
- r8 — semantic socket support map; zero provider transforms snapped.
- r9 — failed terrain-aware route-collision topology; **forbidden checkpoint**.
- r10 — terrain-aware navigation + closed-manifold route collisions.
- r11 — navigation/socket metadata normalized + shared GLB delivery hardening.
- r12 — monolithic terrain retired; 16 render + 16 collision terrain tiles.
- r13 — spatial stream membership assigned to owned macro objects.
- r14 — 4 L2 supercells, neighbor graphs and L3-only hero-residency overlays.
- r15 — prefetch policy normalized to `RUNTIME_EXPERIMENT_REQUIRED`; four candidate policies retained for native comparison.

## R15 remote identity

- `.blend`: **2,848,052 B**, etag `d95ef102d90bf84db182c8d8be85b1bd`;
- GLB: **1,218,436 B**, etag `d5de5a68ca567167b1f696ceefdba088`;
- Blender revision: **15**;
- sceneSequence: **0**.

These are remote-provider identities, not recovered SHA-bound delivery receipts.

## Geometry invariance R13 → R14 → R15

Deterministic source fingerprint over every MESH/CURVE world transform, mesh topology, curve splines, material names, modifier names/types and render visibility:

`003760384ade90b7b0b792de6850a2eae90322d22f2ca246f8211395cb3e6224`

Identical at accepted r13, r14 and r15. R14/R15 therefore introduced **metadata/hierarchy only, zero geometry delta**.

Receipt: `qa/R15_PREFETCH_POLICY_NORMALIZATION.json`.

## Terrain and partition

Morphology: `R6_BIOGEO_CAUSAL_MACRO_V1`.

### R12 terrain streaming

Contract: `SYLVA_TERRAIN_STREAM_R12`.

Render:
- 16 × `SYLVA_TERRAIN_L3_X#Y#`;
- each 3,000 × 3,000 m;
- 13×13 vertices @ 250 m;
- total 2,704 verts / 2,304 faces;
- 285 shared seam samples;
- max/mean seam Δz = **0 m**.

Collision:
- 16 × `SYLVA_COL_TERRAIN_L3_X#Y#`;
- 9×9 vertices @ 375 m;
- total 1,296 verts / 1,024 faces;
- 189 shared seam samples;
- max/mean seam Δz = **0 m**.

Legacy monoliths remain forbidden.

### R13 stream membership

Contract: `SYLVA_STREAM_MEMBERSHIP_R13`.

- 147 spatial objects assigned at the original R13 checkpoint;
- 0 outside the authored patch;
- 34 cross-cell objects;
- max 6 cells touched by one macro object;
- terrain tiles use authoritative single-cell ownership;
- large roots/routes use multi-cell bounds membership.

## R14 hierarchy

Contract: `SYLVA_STREAM_HIERARCHY_R14`.

- 4 L2 supercells @ 6 km;
- 16 L3 cells @ 3 km;
- 4- and 8-neighbor graphs symmetric;
- backend: `ENGINE_TBD`;
- HLOD IDs are contract-only; no HLOD geometry exists.

Hero overlays are **L3-granular**:
- Puerto: `X0Y1 | X1Y1`, radius proposal 550 m;
- Bosque: `X1Y1 | X1Y2 | X2Y1 | X2Y2`, radius proposal 200 m;
- VESPER: `X2Y2 | X3Y2`, radius proposal 400 m.

Bosque covers all four L2 supercells only as metadata; `hero_l2_full_residency_implied=false`. Geography is not moved to simplify streaming.

## R15 prefetch policy

Contract: `SYLVA_PREFETCH_POLICY_R15`.

State: `RUNTIME_EXPERIMENT_REQUIRED`.  
Production policy approved: **false**.

Candidates:
1. `P0_CURRENT_ONLY`;
2. `P1_CURRENT_PLUS_4`;
3. `P2_CURRENT_PLUS_8`;
4. `P3_DIRECTIONAL_ROUTE_WINDOW` — primary runtime candidate, not approved.

Pressure study upper bound for current+8: **72.8%** of current spatial-object cardinality. Selection rule is to promote the **least-resident** policy that passes real visual/collision/traversal/IO gates.

Exact route seam probes are preserved in `PREFETCH_POLICY_R14_EXPERIMENT.json` and `NATIVE_STREAM_RESIDENCY_TEST_PLAN.md`.

## Navigation R10 retained

`SYLVA_NAV_R10` / `BALANCED_FOOT_TERRAIN_AWARE_R10`:
- leg00: 1,963.093 m / max 18.490°;
- leg01: 2,382.483 m / max 15.131°;
- leg02: 2,188.103 m / max 7.285°;
- leg03: 2,364.615 m / max 20.530°;
- total: **8,898.294 m**.

All four route collision ribbons still pass: 0 nonmanifold edges, 0 degenerate faces.

## VESPER macro layout retained

- terraces: 116 / 124 / 112 m diameter;
- connectors: 142.215 m @ 12.178° and 145.685 m @ 12.689°;
- 18 m visible / 16 m collision width;
- no precision jumps;
- obsolete single-floor arena absent;
- final VESPER excluded.

## Root-kit provider dependency

Consumer contracts:
- `SYLVA_SOCKET_CONSUMER_V1`;
- `SYLVA_SOCKET_SUPPORT_MAP_V1`;
- basis `+X forward / +Z up / metres / scale 1`;
- sockets: 8;
- provider instances: 0;
- provider geometry copied: 0;
- snapped transforms: 0.

Latest provider re-audit: PR #6 HEAD `5ba1ea6758e4c08ed82d95deb96f1bbcae1581f5` has a green Gauntlet, but is still **NOT_READY for consumption** because:
- current provider manifest still has invalid YAML structure around `materials`/`note`;
- generator still authors module mesh coordinates in preview/world space and exposes no per-asset pivot normalization/anchor transform;
- render/collision anchor parity and pivot-policy version are not proven.

Current blocker was re-posted on PR #6. CI PASS is not treated as provider-contract PASS.

## Production authority created

Current branch now includes:
- `WORLD_ASSET_COVERAGE_R14.json` — world-wide coverage/gaps;
- `SYLVA_PARALLEL_SHARDING_R14.json` — proposed non-overlapping future cells, not reservations;
- `ART_DIRECTION_BIBLE_R14.md` — region/material/shape/lighting/anti-drift rules;
- `BIOLOGICAL_REALISM_REFERENCE_PACK_R14.md` — plant mechanics translated into modeling rules;
- `BLENDER_PRODUCTION_STANDARD_R14.md` — geometry/UV/material/collision/export standard;
- `HLOD_STRATEGY_R14_PROPOSAL.md` — feature-aware HLOD policy, no premature budgets;
- `PREFETCH_POLICY_R14_EXPERIMENT.json` — native policy experiment design;
- `NATIVE_STREAM_RESIDENCY_TEST_PLAN.md` — runtime seam/residency gauntlet.

## Fleet / concurrency

Published registry now reports this claim **ACTIVE**, owner ACK epoch 1. Main was synchronized one-way through PR #26 before R14.

Writer epoch `SYLVA-MACRO-WRITER-EPOCH-3-R14-20260913` is **CLOSED_ACCEPTED_R15**. No new mutation is authorized by that epoch.

Orbital project `c796230b-0463-4e17-9446-2e746c5c4933` remains EMPTY r0 and unregistered; do not mutate it.

## Delivery / engine status

Current source-level scene QA: PASS.  
Exact `.blend`/GLB SHA-bound recovery: **OPEN / environment-dependent**.  
Native import/residency/traversal: **NOT_RUN** for this exact artifact.  
Human art review: **PENDING**.  
Target-hardware HLOD/LOD performance: **BLOCKED_TARGET_HARDWARE**.

Remote GLB existence never substitutes for shared `fleet_control.py delivery`, claim-local GLB validation or native import.

## Open P0/P1

P0:
1. Recover exact R15 `.blend` + GLB, bind SHA-256, run shared delivery and current claim validator.
2. Import exact artifact into a qualified runtime and execute the four seam probes + route/VESPER traversal.
3. Keep PR #6 consumption blocked until manifest + anchors/pivots + collision parity are proven.
4. Human macro-composition/art-direction review before irreversible density/material waves.

P1:
5. Create/assign future atomic claims from the sharding proposal for final Puerto architecture, materials, vegetation, fauna, NPCs, vehicle and VESPER — only after live collision audit.
6. Qualify feature-aware HLOD candidates in target renderer/hardware; no global percentage decimation.
7. Resolve/defer canonical planet scale before orbital/L0-L1 promotion.

## Gates

| Gate | State |
|---|---|
| Canon regions / VESPER layout | PASS_BLOCKOUT |
| Terrain causality | PASS_R6 |
| Terrain partition / seams | PASS_R12_ZERO_DELTA |
| Stream membership | PASS_R13_SOURCE |
| L2/L3 hierarchy | PASS_R14_SOURCE |
| Prefetch semantics | PASS_R15_POLICY_UNAPPROVED |
| Geometry invariance R13→R15 | PASS_SHA_IDENTICAL |
| Navigation/collision topology | PASS_R10 |
| Root-kit consumer contract | PASS |
| Root-kit provider contract | BLOCKED |
| Remote editable/export source | PASS_R15_REMOTE |
| Exact SHA-bound delivery | NOT_YET_QUALIFIED |
| Native residency/traversal | NOT_RUN |
| Human art review | PENDING |
| HLOD/target performance | BLOCKED_TARGET_HARDWARE |
| Planet radius canon | PROPOSAL_PENDING_DECISION |
