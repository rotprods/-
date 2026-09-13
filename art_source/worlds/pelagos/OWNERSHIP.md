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

## Completed foundation claim
- `PEL/CIV/PROP-X100-001` — Mercado civilization/prop systemic kit.
- Scene checkpoint: rev. 32.
- Result: 9 semantic families × 3 variants × 4 causal states; 108 direct configurations / ≥432 with cardinal yaw; STRUCTURAL_PASS; source + receipt persisted.
- Remaining gates: semantic GATE-ART, engine import/runtime interaction/LOD thresholds/target-GPU qualification.

## Active claim — `/EXOVANT-X100`
- Claim ID: `PEL/MKT/ARCH-X100-002`
- Scope: Mercado CommandShell interior/service-listening-custody cell; interior architecture only, with modular wall/floor/ceiling/service families, current-state assembly and causal three-era history.
- Why now: X100 rerank at Blender rev. 32 found `interior_like_objects: 0` and settlement machinery at zero, making L3 interior the largest near-zero multiplicative dimension after prop expansion.
- Placement: inside `PEL_MKT_CommandShell`; target bay centered near `(-504,-90)` m; floor tied to ring/platform top around z=14 m; connects westward to `PEL_MKT_V1_ServiceChannel_05` / utility system while reserving bridge centerline corridors.
- Configuration grammar: four wall slots × five panel types with functional constraints = 280 valid wall layouts; × three floor patterns × two ceiling patterns × four temporal states = up to 6,720 credible cell configurations before broader district placement.
- Canon constraints: repair-first marine construction, corrosion/drainage/buoyancy/maintainability logic, physical custody/listening functions, no invented faction iconography or unsupported social hierarchy.
- DoD: stable IDs; player-scale clearances; 1.2 m minimum route/threshold clearance; modular snap contract; causal ERA_0/ERA_1/ERA_2 geometry; UV0/materials/clean transforms/pivots; collision/visibility-cell strategy; LOD/HLOD strategy; deterministic grammar; structural QA; visual evidence; receipt; reproducible generator.
- Engine gate: runtime door/interaction/audio bindings, portal/room culling, HLOD thresholds and GPU qualification remain `BLOCKED/PENDING` until production-engine decision.

## Current status
`X100_PRODUCTION_ACTIVE`: current wave is closing the zero-interior gap inside the Mercado rather than adding isolated exterior hero assets.
