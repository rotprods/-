# LEVIATHAN · Cold-Recovery Handoff

AGENT: `AGENT-LEVIATHAN-10`  
SESSION: `ART-LEVIATHAN-001-20260912T2123+0200`  
CLAIM: `CLM-W10-WORLD-LEVIATHAN-001`  
BRANCH: `art/world-leviathan-001`  
MAIN LAST OBSERVED: `be6162064ceb475d5f7a7aa1388a7873f25d3258`  
CLAIM STATUS: **KEEP / IN_PROGRESS**  
NORTH STAR: reproducible LEVIATHAN foundation with causal living-world art, stable gameplay collision beneath visual tissue, and recoverable evidence without invented planet/engine budgets.

## Authority / fleet

- Repository authority: `rotprods/-`.
- Re-run ownership preflight before each significant production wave.
- Latest registry observed: generation 8 on `main@be616206…`.
- LEVIATHAN remains `reserved`, `ack:null`; do **not** self-promote to active.
- Producer ACK: issue #7 comment `5648464282`.
- Jardines delta: issue #7 comment `5648515712`.
- SOMA delta: issue #7 comment `5648567162`.
- PR #10 manifest/integration request: issue #7 comment `5648779529`.
- Main remediation reconciled five other producers and metadata-shard admission but not this claim yet.
- Do not edit `main:ops/fleet/registry.json` from this producer branch.

## Canon boundaries

CANON: LEVIATHAN / Soma / EL UMBRAL / Comuna del Pulso / 1.15 g / 38°C / Puerto de la Herida / Jardines Inmunes / Cámara de SOMA / 58 m SOMA chamber.

BLOCKED/UNKNOWN: physical planet radius/diameter, final production engine, target hardware, final playable-region dimensions, final SOMA anatomy.

PROPOSAL: 720×480 m authored L2 cell and all new representative anatomy dimensions unless separately promoted.

## Blender projects / current revisions

Primary working master: `2577a7b6-ebd7-4d31-a645-620e4b73a95d` @ **revision 10**.  
Independent cold project: `37a931c7-f2e6-46bc-9be0-26077e5de1c1` @ **revision 8**.

Primary and cold both contain the same representative art surface and now converge to **98 mesh datablocks** under the order-invariant instancing optimizer v2.

## Representative production checkpoints

### Master foundation
- `build_master_scene.py` cold-rebuilt from empty scene.
- 1.85 m human scale reference.
- Stable collision separated from visual tissue/contraction.
- SOMA chamber corrected to exact 58 m.
- Non-portable AREA lighting removed.

### Puerto — representative r5
IDs: `LEV-ARCH-001`, `LEV-INF-002`, `LEV-INF-003`.
- Human graft module, hero suture clamp, living valve.
- r4 4.35 m service-door error fixed in r5 to `0.28×1.60×2.60 m`, sill +0.10 m.
- 100 objects / 87 meshes / 10 curves / 13,380 native-mesh triangles.
- Receipt: `evidence/puerto_microset_r5.json`.

### Jardines — representative r7 art stage
IDs: `LEV-INF-005`, `LEV-ECO-001`, `LEV-ECO-004`.
- Lymph pressure conduit + independent 34 m stable service walk.
- Pulse-algae pressure states.
- Functional gardener proposal: six wet-grip limbs, cleaning rasps, digestive sac, sensory cilia.
- Truth correction: 2.6 m = core body; articulated envelope `5.35×5.50×3.37 m`; current collision core-only provisional.
- Evaluated cost including curve tessellation: 21,644 triangles.
- Receipt: `evidence/jardines_microset_r7.json`.

### Cámara de SOMA — representative r8 art stage
IDs/interfaces: `LEV-RGN-003`, `LEV-ENV-002`, `LEV-ENV-003`, local `LEV-INF-003` variant.
- v1 rejected before execution because contraction envelope could exceed canonical radius.
- v2 builds cartilage bridges, three safe-valve refuges/bypasses, contraction telegraphs and regulator cradle.
- `SOMA_PROXY_NOT_FINAL` stays `final_anatomy=false`, dimensions `17×17×22 m`, combat-scale/silhouette only.
- Authoritative evaluated-vertex max radius `28.3 m`, leaving `0.7 m` inside canonical 29 m.
- Evaluated cost: 34,308 triangles.
- Receipt: `evidence/soma_encounter_microset_r8.json`.

## Canonical visual reproducibility

An earlier order-sensitive mesh hash reported raw primitive drift between primary and cold. That was investigated rather than accepted.

Complete order-invariant evaluated-surface comparison proves primary/cold are visually equivalent:
- evaluated world-space triangles;
- UV per triangle corner;
- face material;
- smoothing;
- evaluated normals;
- modifiers;
- cameras, lights and material-node parameters.

Canonical surface fingerprint for primary r9 and cold r7:
`6c06329ff60fe34383394bece0c80f66bb9e4486793712854e462c3af8eea26a`.

Suspect primitives differed only in internal Blender vertex/face numbering. `LEV-BLK-008` is therefore resolved as `INTERNAL_INDEX_ORDER_VARIANCE`, not geometry/material drift.

Receipt: `evidence/canonical_surface_repro_r9.json`.

## Revision 10 structural optimization

`tools/optimize_repeated_mesh_instances_v2.py` uses an order-invariant editable-surface signature instead of Blender index order.

Primary r8 art baseline → r10:
- mesh objects stay `260`;
- mesh datablocks `260 -> 98` (**162 removed / 62.3077% reduction**);
- `.blend` `7,657,188 -> 4,842,680 B` (**36.7564% reduction**);
- GLB `8,492,516 -> 5,617,124 B` (**33.858% reduction**).

Cold replay also converges to `98` mesh datablocks and identical `.blend` size `4,842,680 B`.

Primary r9, primary r10 and cold r8 canonical visual-surface fingerprint:
`1b9d885f7fd612a30c4fd289bbc79da6b06472b710867e8f63bafa9c87827a5d`.

This is a **source/export structural optimization**, not runtime FPS/GPU evidence.

Receipt: `evidence/instancing_optimization_r10_v2.json`.

## UV / PBR / LOD truth

Contract: `UV_PBR_LOD_CONTRACT.md`.  
Receipt: `evidence/uv_pbr_lod_audit_r8.json`.

Measured art-surface state:
- 260/260 mesh objects have UV layers;
- zero zero-area UV triangles;
- zero UV loops outside 0–1;
- relative UV density is not normalized;
- image textures: **0**;
- portable material roles: 18 Principled constant-role materials;
- curves: 92 (`resolution_u=4`, `bevel_resolution=3`);
- named LOD objects: 0;
- Decimate modifiers: 0.

UV presence != approved unwrap, material role != final PBR, and no LOD/performance completion is claimed.

## Runtime / visual blockers

`LEV-BLK-007` binary/runtime colocation was confirmed blocked by three routes: producer shell, secure-download path and independent browser signed-URL attempt. No engine import/collision/traversal PASS exists.

Visual render receipts exist, including r8 overview, Puerto and Jardines PNG artifacts, but this producer surface still cannot inspect their pixel bytes. `B_ART` / visual-regression PASS remains open.

## CI truth

Deeply diagnosed PR #10 run `34718006302`:
- all 75 Python tests PASS;
- only failure was root `MANIFEST.json` drift for new LEVIATHAN files;
- native Godot stage skipped only because continuity exited first.

Latest `main@be616206…` admits world metadata shards in fleet policy but leaves `tools/project_control.py` exact-root MANIFEST comparison and Gauntlet structure unchanged. Therefore PR integration still requires a real merge-tree `project_control.py refresh` transaction by the integrator; do not synthesize hashes or blind-rerun the known failing tree.

## Current tasks

DONE: `W10/WORLD/001`, `W10/WORLD/002`, `W10/BLEND/003`.

REVIEW: `W10/REGION/004`, `005`, `006`, `W10/TECH/007`, `W10/MAT/008`, `W10/ECO/009`, `W10/QA/010`.

No REGION task is DONE because direct art review and runtime integration remain open.

## Open blockers

- `LEV-BLK-001`: planet radius/diameter canon missing.
- `LEV-BLK-002`: production engine not qualified.
- `LEV-BLK-003`: target hardware/preset not qualified; no hard budgets.
- `LEV-BLK-004`: final SOMA anatomy/art/rig decision.
- `LEV-BLK-005`: final playable-region dimensions.
- `LEV-BLK-007`: provider binary transport + qualified runtime colocation unavailable.

Resolved: `LEV-BLK-006` global fleet/manifest architecture; `LEV-BLK-008` suspected raw geometry drift (proved index-order-only).

## Explicit non-claims

- LEVIATHAN is not DONE or AAAA-complete.
- No final calibrated image-textured PBR pass.
- No approved production UV-density/overlap policy.
- No LOD/HLOD chain or target-hardware performance PASS.
- No final character/NPC/creature rig/animation.
- No engine import/traversal PASS.
- No direct human/pixel art PASS in this producer runtime.
- file-size reduction is not runtime performance evidence.

## Recovery entry points

- `WORLD_BIBLE.md`
- `MASTER_ASSET_LIST.yaml`
- `TASKS.yaml`
- `STATUS.yaml`
- `validation.json`
- `UV_PBR_LOD_CONTRACT.md`
- `tools/build_master_scene.py`
- `tools/build_puerto_microset.py`
- `tools/refine_puerto_microset_v2.py`
- `tools/build_jardines_microset.py`
- `tools/refine_jardines_truth_v2.py`
- `tools/build_soma_encounter_microset_v2.py`
- `tools/optimize_repeated_mesh_instances_v1.py`
- `tools/optimize_repeated_mesh_instances_v2.py`
- `evidence/cold_rebuild_r3.json`
- `evidence/puerto_microset_r5.json`
- `evidence/jardines_microset_r7.json`
- `evidence/soma_encounter_microset_r8.json`
- `evidence/uv_pbr_lod_audit_r8.json`
- `evidence/canonical_surface_repro_r9.json`
- `evidence/instancing_optimization_r10_v2.json`
- `evidence/runtime_import_blocker_r5.json`

## Next 3 executable actions

1. Measure an engine-neutral LOD feasibility envelope on representative high-cost meshes using temporary non-destructive decimation plus geometric error metrics; do not commit final LODs or invent hardware thresholds.
2. Integrator: reconcile LEVIATHAN ACK/asset IDs and root MANIFEST on the exact PR merge tree; producer remains inside owned paths.
3. When exact provider GLB bytes and a qualified engine coexist, execute import → instantiate → scale/material/collision/traversal and bind evidence to the exact GLB hash; direct art review remains separate.

CLAIM STATUS: **KEEP**. PR #10 remains draft. Do not merge as world-complete.
