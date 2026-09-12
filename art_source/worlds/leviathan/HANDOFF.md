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
- SOMA delta: latest LEVIATHAN SOMA ACK comment in issue #7.
- Former manifest/fleet blocker issue #13 is closed; exact `main@f78bfdc8...` push Gauntlet run `34715800243` succeeded.
- Do not edit `main:ops/fleet/registry.json` from this branch.

## Canon boundaries

CANON: LEVIATHAN / Soma / EL UMBRAL / Comuna del Pulso / 1.15 g / 38°C / Puerto de la Herida / Jardines Inmunes / Cámara de SOMA / 58 m SOMA chamber.

BLOCKED/UNKNOWN: physical planet radius/diameter, final production engine, target hardware, final playable-region dimensions, final SOMA anatomy.

PROPOSAL: 720×480 m authored L2 cell and all new representative anatomy dimensions unless separately promoted.

## DONE / receipts

### Deterministic master
- Remote master project: `2577a7b6-ebd7-4d31-a645-620e4b73a95d`.
- Cold project: `37a931c7-f2e6-46bc-9be0-26077e5de1c1`.
- `build_master_scene.py` independently rebuilt from an empty scene.
- Master semantic fingerprint: `207649cb10842785dd23c2f3823ec654e265c9bcfbd602d460b067266cbccf9f`.
- Human reference 1.85 m; stable collision separated from visual contraction.
- SOMA chamber corrected to exact 58 m; non-portable AREA lighting removed.

### Puerto — revision 5 representative checkpoint
Existing IDs only: `LEV-ARCH-001`, `LEV-INF-002`, `LEV-INF-003`.

- Pressure-frame/ceramic-panel human graft module, hero suture clamp, living valve.
- Human-scale defect found in r4 and fixed in r5: service door `0.28×1.60×2.60 m`, sill +0.10 m.
- Microset: 100 objects / 87 meshes / 10 curves / 13,380 native mesh triangles.
- Full staged master==cold fingerprint: `b4fb20302e45afa27bbea9c875cc4cdfc4e2861e61538d1f55405b5f92e1abd5`.
- Receipt: `evidence/puerto_microset_r5.json`.

### Jardines — revision 7 representative checkpoint
Existing IDs only: `LEV-INF-005`, `LEV-ECO-001`, `LEV-ECO-004`.

- Lymph pressure conduit + independent 34 m stable service walk.
- Pulse-algae pressure states.
- Functional gardener-parasite proposal: six wet-grip limbs, cleaning rasps, digestive sac, sensory cilia.
- Truth correction: 2.6 m is proposed core body; measured articulated envelope `5.35×5.50×3.37 m`. Gardener collision is core-only provisional.
- Evaluated cost including curve tessellation: 21,644 triangles.
- Master r7 == cold r5 fingerprint: `1fa569c938fc714fa1668e0c00b45761cec4d15dbd64a3ce5070d87bdd7d23ae`.
- Receipt: `evidence/jardines_microset_r7.json`.

### Cámara de SOMA — revision 8 representative checkpoint
Existing IDs/interfaces: `LEV-RGN-003`, `LEV-ENV-002`, `LEV-ENV-003`, local `LEV-INF-003` variant.

- v1 generator was rejected at source preflight and never executed because its contraction envelope could exceed canonical chamber radius.
- v2 builds representative cartilage bridges, three safe-valve refuges/bypasses, contraction telegraph walls, and regulator cradle.
- Final `SOMA_PROXY_NOT_FINAL` remains `final_anatomy=false`, dimensions `17×17×22 m`, role `COMBAT_SCALE_AND_SILHOUETTE_INTERFACE_ONLY`.
- AABB-corner radius heuristic falsely reported 29.2015 m; authoritative evaluated-vertex gate measured max actual radius **28.3 m**, leaving **0.7 m clearance** inside canonical 29 m.
- No microset visual objects are in stable collision collection.
- Evaluated cost: 98 objects / 54 source meshes / 40 curves / 34,308 evaluated triangles.
- Master r8 == cold r6 fingerprint: `5d59df25bb89a19dfe90dc10e911ee99b20409d03ff9689415e61b89b3e2fba3`.
- Receipt: `evidence/soma_encounter_microset_r8.json`.

Current master r8: 381 objects / 260 meshes / 18 material roles / 13 collections. Editable `.blend` and portable GLB were produced remotely.

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
- `LEV-BLK-007`: this producer runtime cannot colocate exact provider GLB bytes with a qualified engine binary; engine import/collision smoke test is NOT RUN.

Runtime blocker receipt: `evidence/runtime_import_blocker_r5.json`.

## Explicit non-claims

- LEVIATHAN is not DONE or AAAA-complete.
- No final UV/PBR/LOD/HLOD pass.
- No final character/NPC/creature rig/animation.
- No target-hardware performance PASS.
- No engine import/traversal PASS.
- No direct human/pixel art PASS in this producer runtime.
- Provider export success is not engine acceptance.

## Files / recovery entry points

- `WORLD_BIBLE.md`
- `MASTER_ASSET_LIST.yaml`
- `TASKS.yaml`
- `STATUS.yaml`
- `validation.json`
- `tools/build_master_scene.py`
- `tools/build_puerto_microset.py`
- `tools/refine_puerto_microset_v2.py`
- `tools/build_jardines_microset.py`
- `tools/refine_jardines_truth_v2.py`
- `tools/build_soma_encounter_microset_v2.py`
- `evidence/cold_rebuild_r3.json`
- `evidence/puerto_microset_r5.json`
- `evidence/jardines_microset_r7.json`
- `evidence/soma_encounter_microset_r8.json`
- `evidence/runtime_import_blocker_r5.json`

## Next 3 executable actions

1. Re-run ownership/fleet preflight and ingest integrator ACK/registry transition if published; never self-promote main registry.
2. Qualify a runtime where exact r8 GLB bytes and Godot/production-engine binary coexist, then execute import → instantiate → scale/material/collision/traversal smoke test and bind evidence to exact GLB hash.
3. Once engine path and direct art review are available, advance the three representative regions through UV/PBR/LOD rather than blindly increasing geometry; keep final SOMA sculpt separate until LEV-BLK-004 resolves.

CLAIM STATUS: **KEEP**. PR #10 remains draft. Do not merge as world-complete.
