# LEVIATHAN · Cold-Recovery Handoff

AGENT: `AGENT-LEVIATHAN-10`  
SESSION: `ART-LEVIATHAN-001-20260912T2123+0200`  
CLAIM: `CLM-W10-WORLD-LEVIATHAN-001`  
BRANCH: `art/world-leviathan-001`  
MAIN LAST OBSERVED: `f78bfdc8bd7b2f6ab52b45d39babcc1589ab3918`  
CLAIM STATUS: **KEEP / IN_PROGRESS**  
NORTH STAR: reproducible LEVIATHAN foundation with causal living-world art, stable gameplay collision beneath visual tissue, and recoverable evidence without invented planet/engine budgets.

## Authority / fleet

- Repository authority: `rotprods/-`.
- Read `AGENTS.md`, `docs/FLEET_COORDINATION.md`, `ops/fleet/registry.json` and issue #7 before every new production wave.
- Fleet registry generation 3 still shows this claim `reserved`; producer ACK exists and integrator owns transition to `active`.
- Producer ACK: issue #7 comment `5648464282`.
- Jardines delta: issue #7 comment `5648515712`.
- SOMA delta: issue #7 comment `5648567162`.
- PR #10 CI/manifest integrator request: issue #7 comment `5648779529`.
- Former manifest/fleet architecture blocker issue #13 is closed; `main@f78bfdc8...` canonical push Gauntlet `34715800243` succeeded.
- Do not edit `main:ops/fleet/registry.json` from this producer branch.

## Canon boundaries

CANON: LEVIATHAN / Soma / EL UMBRAL / Comuna del Pulso / 1.15 g / 38°C / Puerto de la Herida / Jardines Inmunes / Cámara de SOMA / 58 m SOMA chamber.

BLOCKED/UNKNOWN: physical planet radius/diameter, final production engine, target hardware, final playable-region dimensions, final SOMA anatomy.

PROPOSAL: 720×480 m authored L2 cell and all new representative anatomy dimensions unless separately promoted.

## Blender projects / current revisions

Primary working master: `2577a7b6-ebd7-4d31-a645-620e4b73a95d` @ **revision 9**.  
Independent cold project: `37a931c7-f2e6-46bc-9be0-26077e5de1c1` @ **revision 7**.

Primary r9 is r8 plus safe repeated-mesh datablock sharing. It is not a new art pass.

## Representative production checkpoints

### Master foundation
- `build_master_scene.py` cold-rebuilt from empty scene.
- Master-stage semantic fingerprint: `207649cb10842785dd23c2f3823ec654e265c9bcfbd602d460b067266cbccf9f`.
- 1.85 m human scale reference.
- Stable collision separated from visual tissue/contraction.
- SOMA chamber corrected to exact 58 m.
- Non-portable AREA lighting removed.

### Puerto — representative r5
IDs: `LEV-ARCH-001`, `LEV-INF-002`, `LEV-INF-003`.
- Human graft module, hero suture clamp, living valve.
- r4 4.35 m service-door error fixed in r5 to `0.28×1.60×2.60 m`, sill +0.10 m.
- 100 objects / 87 meshes / 10 curves / 13,380 native-mesh triangles.
- Puerto strict family-level raw replay remains matching in the later r9/cold-r7 audit.
- Receipt: `evidence/puerto_microset_r5.json`.

### Jardines — representative r7
IDs: `LEV-INF-005`, `LEV-ECO-001`, `LEV-ECO-004`.
- Lymph pressure conduit + independent 34 m stable service walk.
- Pulse-algae pressure states.
- Functional gardener proposal: six wet-grip limbs, cleaning rasps, digestive sac, sensory cilia.
- Truth correction: 2.6 m = core body; articulated envelope `5.35×5.50×3.37 m`; current collision core-only provisional.
- Evaluated cost including curve tessellation: 21,644 triangles.
- Older high-level semantic fingerprint matched, but strict raw mesh/UV replay later exposed primitive-realization drift in selected R2 primitives. Do not call raw rebuild bit-exact.
- Receipt: `evidence/jardines_microset_r7.json`.

### Cámara de SOMA — representative r8
IDs/interfaces: `LEV-RGN-003`, `LEV-ENV-002`, `LEV-ENV-003`, local `LEV-INF-003` variant.
- v1 rejected before execution because contraction envelope could exceed canonical radius.
- v2 builds cartilage bridges, three safe-valve refuges/bypasses, contraction telegraphs and regulator cradle.
- `SOMA_PROXY_NOT_FINAL` stays `final_anatomy=false`, dimensions `17×17×22 m`, combat-scale/silhouette only.
- Authoritative evaluated-vertex max radius `28.3 m`, leaving `0.7 m` inside canonical 29 m.
- No encounter visual objects in stable collision collection.
- Evaluated cost: 34,308 triangles.
- Older high-level semantic fingerprint matched, but strict raw mesh/UV replay later exposed primitive-realization drift in selected R3 primitives. Do not call raw rebuild bit-exact.
- Receipt: `evidence/soma_encounter_microset_r8.json`.

## Revision 9 structural optimization

Source: `tools/optimize_repeated_mesh_instances_v1.py` @ commit `9030209c9297de0cc5233644524ed383b7f75454`.

Primary r8 -> r9:
- mesh objects: `260 -> 260`;
- mesh datablocks: `260 -> 122`;
- redundant datablocks removed/relinked: `138`;
- strict safe groups: `36`;
- `.blend`: `7,657,188 -> 5,597,471 B` (~26.9% smaller);
- GLB: `8,492,516 -> 6,603,972 B` (~22.2% smaller).

Object-level render-equivalent fingerprint before/after is exactly identical:
`d8b3912446104a1892fc6c759c490f9a77633e2c7d0612d817714baf8af6c19d`.

This proves the primary optimization preserves audited object transforms, geometry, UVs, material assignments, curves, cameras and lights. It **does not** prove runtime FPS/memory behavior.

Cold r6 -> r7 applied only 32 strict groups and reached 127 datablocks. Its strict render-equivalent fingerprint is `9ab4a14e144a790c7732d944b625168f05bce958de05d613ee4d1cb642c78547`, not the primary fingerprint. This exposed a narrower raw primitive realization defect hidden by the older semantic fingerprint.

Exact 1 mm family audit:
- MATCH: `R1_HERO`, `R1_BASE`, `COLLISION`.
- DRIFT: `R2_HERO`, `R2_BASE`, `R3_HERO`, `R3_BASE`, `MACRO_OTHER`.

Sampled suspects have matching transforms, materials, metadata, vertex/polygon counts and nominal dimensions but different local primitive vertex/UV realization. Classification: `STRICT_RAW_PRIMITIVE_REALIZATION_DRIFT`. Fix the generator/helper narrowly; do not normalize unrelated geometry blindly.

Receipt: `evidence/instancing_optimization_r9.json`.

## UV / PBR / LOD truth

Contract: `UV_PBR_LOD_CONTRACT.md`.  
Receipt: `evidence/uv_pbr_lod_audit_r8.json`.

Measured r8 state:
- 260/260 mesh objects have UV layers;
- zero zero-area UV triangles;
- zero UV loops outside 0–1;
- relative UV density is not normalized;
- image textures: **0**;
- portable material roles: 18 Principled constant-role materials;
- curves: 92 (`resolution_u=4`, `bevel_resolution=3`);
- named LOD objects: 0;
- Decimate modifiers: 0.

Therefore UV presence != final unwrap, material role != final PBR and no LOD/performance completion is claimed.

## Runtime / visual blockers

`LEV-BLK-007` runtime transport has now been confirmed by three routes:
1. producer shell cannot resolve/materialize provider signed R2 bytes and has no qualified local engine;
2. secure download path cannot materialize the signed provider URL into the runtime;
3. independent browser attempt returned Cloudflare R2/S3 `InvalidArgument / Authorization` for the signed GLB URL.

No engine import/collision/traversal PASS exists.

Visual render receipts exist, including r8 overview, Puerto and Jardines PNG artifacts, but this producer surface still cannot inspect their pixel bytes. `B_ART` / visual-regression PASS remains open.

## CI truth

Latest deeply diagnosed PR #10 run: `34718006302`.
- 75 Python tests: **PASS**.
- only failing continuity problem: root `MANIFEST.json` drift for the LEVIATHAN added files.
- Godot/native stage skipped after the manifest failure.
- issue #7 comment `5648779529` asks the integrator to regenerate root MANIFEST on the exact merge tree and then run the fleet guard.
- Do not blind-rerun the same known failing state; do not hand-wave this as Blender failure.

## Current tasks

DONE: `W10/WORLD/001`, `W10/WORLD/002`, `W10/BLEND/003` (master-stage semantic DoD only).

REVIEW: `W10/REGION/004`, `005`, `006`, `W10/TECH/007`, `W10/MAT/008`, `W10/ECO/009`, `W10/QA/010`.

No REGION task is DONE because direct art review and runtime integration remain open. `W10/QA/010` also owns the newly exposed strict raw primitive replay defect.

## Open blockers

- `LEV-BLK-001`: planet radius/diameter canon missing.
- `LEV-BLK-002`: production engine not qualified.
- `LEV-BLK-003`: target hardware/preset not qualified; no hard budgets.
- `LEV-BLK-004`: final SOMA anatomy/art/rig decision.
- `LEV-BLK-005`: final playable-region dimensions.
- `LEV-BLK-007`: provider binary transport + qualified runtime colocation unavailable.
- `LEV-BLK-008`: strict raw primitive mesh/UV realization drift in selected R2/R3/macro families.

## Explicit non-claims

- LEVIATHAN is not DONE or AAAA-complete.
- No final calibrated image-textured PBR pass.
- No approved production UV-density/overlap policy.
- No LOD/HLOD chain.
- No final character/NPC/creature rig/animation.
- No target-hardware performance PASS.
- No engine import/traversal PASS.
- No direct human/pixel art PASS in this producer runtime.
- r9 file-size reduction is not runtime performance evidence.
- old semantic fingerprint equality is not raw-mesh bit-exact equality.

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
- `evidence/cold_rebuild_r3.json`
- `evidence/puerto_microset_r5.json`
- `evidence/jardines_microset_r7.json`
- `evidence/soma_encounter_microset_r8.json`
- `evidence/uv_pbr_lod_audit_r8.json`
- `evidence/instancing_optimization_r9.json`
- `evidence/runtime_import_blocker_r5.json`

## Next 3 executable actions

1. Narrowly replace/canonicalize context-dependent primitive creation responsible for R2/R3/macro raw mesh/UV drift; rerun clean staged build and require strict fingerprints rather than the older semantic-only criterion.
2. Have the integrator regenerate root `MANIFEST.json` on the exact PR merge tree, then re-run continuity/native gates; do not modify global registry state from this branch.
3. When exact provider GLB bytes and a qualified engine coexist, execute import → instantiate → scale/material/collision/traversal and bind evidence to the exact GLB hash; direct art review remains separate.

CLAIM STATUS: **KEEP**. PR #10 remains draft. Do not merge as world-complete.
