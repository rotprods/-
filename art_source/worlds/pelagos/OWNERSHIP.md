# PELAGOS · world art ownership

Run scope reserved on 2026-09-12 from `main@4c2fa044080004609ea6df45f34b2a784536507a`.

## Owned world
- World: `PELAGOS`
- Canon boss: `THALASSA, coral de los mil ojos`
- Discipline: world art direction, Blender source design, environment/architecture/ecology/NPC/enemy/boss/vehicle/prop asset specifications, procedural build tooling, validation contracts and world-specific production tracking.

## Owned paths
- `art_source/worlds/pelagos/**`
- future exported Pelagos candidates under `assets/worlds/pelagos/**` only after source + provenance + audit receipts exist.

## Explicit non-ownership
- `art_source/terra_reliquary_kit/**`, `art_source/production_catalog/**`, `art_source/coordination/**` are reserved by PR #1 and must not be modified here.
- gameplay/runtime scenes, controls, save systems, existing Terra portal assets and shared project state are out of scope unless a later integration PR explicitly reconciles them against current `main`.
- no claim that Pelagos is implemented, AAA-qualified, GPU-qualified or imported into the game until the corresponding gates exist.

## Concurrency contract
Other world agents should select different world IDs and use `art_source/worlds/<world_id>/**`. Shared standards may be proposed in this branch but must remain world-local until reviewed, to avoid edit collisions across parallel agents.

## Completed X100 foundation claims
### `PEL/CIV/PROP-X100-001`
- Mercado civilization/prop systemic kit.
- Scene checkpoint: rev. 32.
- 9 semantic families × 3 variants × 4 causal states; 108 direct configurations / ≥432 with cardinal yaw.
- STRUCTURAL_PASS; source + receipt persisted.
- Remaining gates: semantic GATE-ART, engine import/runtime interaction/LOD thresholds/target-GPU qualification.

### `PEL/MKT/ARCH-X100-002`
- Mercado CommandShell service/listening/memory-custody interior systemic cell.
- Final structurally verified scene checkpoint: rev. 34.
- 280 valid wall layouts × 3 floor patterns × 2 ceiling patterns × 4 temporal states = up to 6,720 credible cell configurations.
- Visible cell envelope ~7.95×5.82×3.37 m; inside CommandShell; bridge clearance >9.2 m beyond bridge bevel; actual east collision threshold gap 2.65 m; reserved 0.90 m central corridor blockers 0; three eras physical; UV/material/scale debt 0.
- Workbench corridor intrusion found at rev. 33 and corrected 0.30 m west at rev. 34.
- Hidden-technical-object QA rule learned: stale `matrix_world` can read origin while `hide_viewport=True`; compose `parent.matrix_world @ matrix_parent_inverse @ matrix_basis` or force depsgraph update before classifying transform drift.
- Source + receipt persisted. Visual artifacts exist; semantic GATE-ART remains pending because signed artifact host could not be pixel-inspected in current execution environment.

### `PEL/MKT/MACH-X100-003`
- Mercado settlement machinery / utility-spine systemic foundation.
- Build checkpoint: rev. 35; final structurally verified checkpoint: **rev. 36**.
- 9 functional families × 3 capacity variants × 4 causal service states = 108 direct / ≥432 cardinal-yaw configurations.
- Physical roots 9; grounded 9; bay overflow 0; physical overlaps 0; UV/material/scale debt 0.
- UtilityRiser maintenance defect found at rev. 35 (~1.06–1.08 m); HOIST + MANIF physical/LOD/collision roots moved 0.25 m west. Final minimum UtilityRiser clearance **1.316 m**; interior-cell minimum clearance **3.625 m**.
- Source + receipt persisted.
- Remaining gates: semantic GATE-ART, engine/runtime fluid/pressure/control/audio bindings, production LOD/HLOD thresholds and target-GPU qualification.

## Active claim — `/EXOVANT-X100`
- Claim ID: `PEL/ECO/SESSILE-X100-004`
- Scope: reversible producer/filter/decomposer sessile ecological guilds for the mnemonic reef / Coro and selected quiet wet infrastructure surfaces. This claim does **not** replace or retcon canonical Medusa mnémica, Anguila de vidrio, Bóvido de arrecife or Coral escriba.
- Why now: X100 coverage after architecture + machinery still leaves producer/decomposer sessile ecology near zero, making the ecology graph trophically incomplete.
- Epistemic rule: detailed Pelagos trophic chain, reproduction cycles and population densities remain `UNKNOWN` in the World Bible. New guilds are therefore **PROPOSAL ecological functions**, not irreversible species canon.
- Planned functional families: current-facing filter fan; photic ribbon producer; detritus/decomposer mat; mineral-tube chemo/decomposer colony; calcifying nursery crust; infrastructure fouling/filter cluster; organic-decay biofilm; sponge-like current biofilter; lee-zone detritus aggregation patch.
- Variation grammar target: 9 functional families × 3 morphology/exposure variants × 4 causal ecological states = 108 direct configurations before orientation/substrate/current/depth placement grammar.
- Placement contract: substrate-, slope-, light-, current- and disturbance-aware. Growth must remain causal: exposed/current-facing filter geometry, photic producers on light-access surfaces, detritus in lee zones, fouling at persistent wet interfaces, decomposers near organic/mineral resource evidence. No random scatter/grunge ecology.
- DoD: stable IDs, metre-scale bounds, ecological role, substrate/depth/current constraints, variants/states, UV/materials/transforms, soft/no-collision policy unless gameplay requires otherwise, LOD strategy, deterministic placement grammar, traversal-clearance QA, receipt and reproducible generator.
- Engine gate: population simulation, spawning, acoustic behavior, ecological persistence/save-state, streaming/HLOD thresholds and target-GPU qualification remain `BLOCKED/PENDING` until engine/gameplay authority.

## Current status
`X100_PRODUCTION_ACTIVE`: machinery is structurally closed; current wave is repairing the near-zero producer/decomposer layer without inventing a complete trophic canon.
