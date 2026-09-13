# LEVIATHAN · Cold-Recovery Handoff

AGENT: `AGENT-LEVIATHAN-10`  
SESSION: `ART-LEVIATHAN-001-20260912T2123+0200`  
CLAIM: `CLM-W10-WORLD-LEVIATHAN-001`  
BRANCH: `art/world-leviathan-001`  
MAIN LAST OBSERVED: `26ae20f5d1b47d1efa0d54b20124ed93cbc0b43e`  
CLAIM STATUS: **KEEP / IN_PROGRESS**

NORTH STAR: reproducible LEVIATHAN foundation with causal living-world art, stable gameplay collision beneath visual tissue, recoverable source/evidence, and no invented planet/engine budgets.

## 0. Resume protocol

1. Read `AGENTS.md`, `docs/FLEET_COORDINATION.md`, `ops/fleet/registry.json`, issue #7 and this file.
2. Fetch live `main`, this branch and PR #10 before any mutation.
3. Primary Blender project: `2577a7b6-ebd7-4d31-a645-620e4b73a95d`.
4. Independent cold replay: `37a931c7-f2e6-46bc-9be0-26077e5de1c1`.
5. Do not self-promote fleet registry and do not touch global runtime/shared state from this claim.

## 1. Fleet / CI truth

- Latest main observed: `26ae20f5...`.
- Fleet registry generation observed: `8`.
- LEVIATHAN remains `reserved`, `ack:null` despite producer ACK/deltas; integrator owns transition to `active`.
- Producer ACK: issue #7 comment `5648464282`.
- Jardines delta: `5648515712`.
- SOMA delta: `5648567162`.
- Manifest/integration request: `5648779529`.
- Main now quarantines automatic Gauntlet triggers to reduce CI spend. Do not burn reruns on a tree known to require root-manifest reconciliation.
- Last deeply diagnosed PR #10 run `34718006302`: **75/75 Python tests PASS**; only failure was root `MANIFEST.json` drift, causing native Godot stage to skip.

## 2. Canon boundaries

CANON: LEVIATHAN / Soma / EL UMBRAL / Comuna del Pulso / 1.15 g / 38 °C / Puerto de la Herida / Jardines Inmunes / Cámara de SOMA / exact 58 m SOMA chamber.

BLOCKED/UNKNOWN: physical planet radius/diameter, final production engine, target hardware/preset, final playable-region dimensions, final SOMA anatomy.

PROPOSAL: 720×480 m authored cell, representative creature dimensions, traversal width and current authored density unless separately promoted.

## 3. Remote truth

Primary working master: **revision 11**.  
Cold project: **revision 9**.

Primary r11 artifacts:
- `.blend`: 4,869,637 B / etag `7ccfdd11e07d845b3e962a802bdefa32`;
- GLB: 5,639,948 B / etag `3ab7e46dc7e2102ca709600b83269ecb`.

Cold r9 artifacts:
- `.blend`: 4,869,637 B / etag `1df2bc94b4ef09c3bb0c21f0f81c0c3e`;
- GLB: 5,643,252 B / etag `1a8147165c232f098e5e01ede32d3cf0`.

Binary GLB equality is not the art reproducibility criterion; evaluated surface/delta equivalence is.

## 4. Representative art checkpoints

### Foundation
- metre scale and 1.85 m human reference;
- three canonical regions;
- exact 58 m SOMA chamber;
- stable collision intentionally independent from deforming visual tissue;
- portable GLB lighting.

### Puerto de la Herida
IDs: `LEV-ARCH-001`, `LEV-INF-002`, `LEV-INF-003`.
- representative human graft module, suture clamp, living valve;
- service-door defect corrected from 4.35 m to `0.28×1.60×2.60 m`;
- microset cost: 13,380 native mesh tris;
- receipt: `evidence/puerto_microset_r5.json`.

### Jardines Inmunes
IDs: `LEV-INF-005`, `LEV-ECO-001`, `LEV-ECO-004`.
- representative lymph pressure conduit + independent stable service walk;
- pulse algae pressure states;
- functional gardener proposal;
- 2.6 m = core body proposal; measured articulated envelope `5.35×5.50×3.37 m`;
- collision remains core-only provisional pending rig/gameplay;
- evaluated cost: 21,644 tris;
- receipt: `evidence/jardines_microset_r7.json`.

### Cámara de SOMA
IDs/interfaces: `LEV-RGN-003`, `LEV-ENV-002`, `LEV-ENV-003`, local `LEV-INF-003` variant.
- representative bridges, three safe-valve refuges, contraction telegraphs, regulator cradle;
- v1 rejected before execution because envelope could violate canonical radius;
- v2 evaluated max radius `28.3 m`, leaving `0.7 m` inside canonical 29 m;
- `SOMA_PROXY_NOT_FINAL` remains combat-scale/silhouette only, `final_anatomy=false`;
- evaluated microset cost: 34,308 tris;
- receipt: `evidence/soma_encounter_microset_r8.json`.

## 5. Structural optimization / reproducibility

`optimize_repeated_mesh_instances_v2.py` uses order-invariant editable-surface signatures.

r8 art baseline → r10:
- 260 mesh objects remain;
- mesh datablocks `260 -> 98`;
- 162 duplicate datablocks removed (**62.3077%**);
- `.blend` `7,657,188 -> 4,842,680 B` (**36.7564%** reduction);
- GLB `8,492,516 -> 5,617,124 B` (**33.858%** reduction).

Primary and cold converged to the same 98 datablocks and canonical evaluated visual surface.

Receipts:
- `evidence/canonical_surface_repro_r9.json`
- `evidence/instancing_optimization_r10_v2.json`

`LEV-BLK-008` is resolved: earlier raw primitive hash drift was internal Blender vertex/face index-order variance, not visual geometry/UV/material drift.

## 6. Stable traversal continuity — revision 11

Source: `tools/build_stable_traversal_ribbon_v1.py` (blob `5161a2f27c77136c4987bd9e3cfeed0f6728e021`).

Purpose: replace eight disconnected collision pads as the only traversal authority with one continuous stable ribbon under the existing organic visual tube and connect it to the SOMA floor.

Measured primary r11:
- centerline length: **541.256 m**;
- ribbon width: **8.0 m** proposal;
- thickness: **0.5 m**;
- 212 verts / 420 tris;
- degenerate polygons: **0**;
- top z: `5 -> 7 m`;
- max segment slope: **7.6923%**;
- width / 0.55 m human reference: **14.545×**;
- minimum real side clearance inside 6 m visual tube after vertical offset: **1.0513 m**;
- ingress side margin: **1.1962–1.2161 m**;
- final ribbon point: `[205,-47,7]`, inside SOMA footprint and exactly on arena top;
- visual ingress is not in collision collection;
- no visual object leaks into `40_COLLISION_PROXY`.

Cold r9 replay produces exactly the same new surfaces:
- ribbon SHA: `65326c41be09e967561907938cf994e389cd1c28ad33390815b5fdd85dde253a`;
- ingress SHA: `3f8b05130e849f7fec36b059d6f11c3fab16cd43b74c8a80dbec446d8fd0e432`.

Receipt: `evidence/traversal_ribbon_r11.json`.

Important: 8 m width and 7.6923% slope are **not final gameplay canon**. Runtime capsule/nav validation remains mandatory.

## 7. UV / PBR / LOD truth

Contract: `UV_PBR_LOD_CONTRACT.md`.

Current measured state:
- 260/260 mesh objects have UV layers;
- zero zero-area UV triangles;
- zero UV loops outside 0–1;
- relative texel density not normalized;
- image textures: **0**;
- material roles: 18 constant/portable Principled roles;
- no committed production LOD chain.

LOD feasibility was measured query-only with temporary Blender Decimate and approximate bidirectional surface error:
- large rings/macro shells tolerate aggressive simplification better than small rounded hero/status/ecology parts;
- a global 50% policy is explicitly rejected;
- small rounded detail should start around a conservative ~80% probe, still requiring screen-space/art validation.

Receipt: `evidence/lod_feasibility_r10.json`.

No final LOD threshold or performance claim exists.

## 8. Current task truth

DONE:
- `W10/WORLD/001`
- `W10/WORLD/002`
- `W10/BLEND/003`

REVIEW:
- `W10/REGION/004`
- `W10/REGION/005`
- `W10/REGION/006`
- `W10/TECH/007`
- `W10/MAT/008`
- `W10/ECO/009`
- `W10/QA/010`

No region is DONE. Direct art review and runtime integration remain open.

## 9. Open blockers

- `LEV-BLK-001`: physical planet radius/diameter absent.
- `LEV-BLK-002`: production engine not qualified.
- `LEV-BLK-003`: target hardware/preset not qualified.
- `LEV-BLK-004`: final SOMA anatomy/art/rig decision.
- `LEV-BLK-005`: final playable-region dimensions.
- `LEV-BLK-007`: exact provider binary + qualified runtime cannot yet coexist in this producer surface. Confirmed via shell, secure-download path and independent browser attempt.

Direct pixel-level art review also remains unavailable despite render artifacts; do not claim `B_ART` or visual-regression PASS.

## 10. Explicit non-claims

- LEVIATHAN is not DONE or AAAA-complete.
- no final image-textured/calibrated PBR pass;
- no approved production texel density/overlap policy;
- no final LOD/HLOD chain;
- no target-hardware FPS/GPU pass;
- no final NPC/creature/SOMA rig/animation;
- no engine import/capsule/nav traversal pass;
- file-size reduction is not runtime performance evidence.

## 11. Recovery files

- `WORLD_BIBLE.md`
- `MASTER_ASSET_LIST.yaml`
- `TASKS.yaml`
- `STATUS.yaml`
- `UV_PBR_LOD_CONTRACT.md`
- `validation.json`
- `tools/build_master_scene.py`
- `tools/build_puerto_microset.py`
- `tools/refine_puerto_microset_v2.py`
- `tools/build_jardines_microset.py`
- `tools/refine_jardines_truth_v2.py`
- `tools/build_soma_encounter_microset_v2.py`
- `tools/optimize_repeated_mesh_instances_v2.py`
- `tools/build_stable_traversal_ribbon_v1.py`
- `evidence/canonical_surface_repro_r9.json`
- `evidence/instancing_optimization_r10_v2.json`
- `evidence/lod_feasibility_r10.json`
- `evidence/traversal_ribbon_r11.json`
- `evidence/runtime_import_blocker_r5.json`

## 12. Next executable actions

1. Publish `LEV-ENV-001` r11 traversal delta to issue #7 and await integrator registry reconciliation; never self-promote.
2. Advance `MAT/008` with an isolated, reversible **portable PBR calibration lab**, not blind texture propagation onto the master.
3. Define/generate engine-neutral LOD candidates from the measured feasibility envelope in an isolated QA stage; keep thresholds proposal-only until screen-space/engine/hardware validation.
4. When exact export bytes and qualified engine coexist, execute import → instantiate → scale/material/collision/capsule/nav traversal and bind evidence to that export.
5. Direct visual review must remain a separate gate.

CLAIM STATUS: **KEEP**. PR #10 remains draft. Do not merge as world-complete.
