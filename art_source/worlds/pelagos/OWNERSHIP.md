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
- Visible cell envelope ~7.95×5.82×3.37 m; inside CommandShell; bridge clearance >9.2 m beyond bridge bevel; east collision threshold gap 2.65 m; 0.90 m central corridor blockers 0; three eras physical; UV/material/scale debt 0.
- Hidden-object QA rule learned: stale `matrix_world` can read origin while `hide_viewport=True`; compose parent/local transforms or force depsgraph evaluation before classifying transform drift.
- Source + receipt persisted. Semantic GATE-ART remains pending.

### `PEL/MKT/MACH-X100-003`
- Mercado settlement machinery / utility-spine systemic foundation.
- Build rev. 35; final structurally verified rev. **36**.
- 9 functional families × 3 capacity variants × 4 causal service states = 108 direct / ≥432 cardinal-yaw configurations.
- Physical roots 9; grounded 9; bay overflow 0; physical overlaps 0; UV/material/scale debt 0.
- UtilityRiser clearance defect corrected by moving HOIST + MANIF systems 0.25 m west. Final minimum UtilityRiser clearance **1.316 m**; interior-cell minimum clearance **3.625 m**.
- Source + receipt persisted.

### `PEL/ECO/SESSILE-X100-004`
- Coro functional producer/filter/decomposer sessile ecology foundation.
- Final structurally verified scene checkpoint: **rev. 37**.
- 9 reversible functional guild families × 3 morphology variants × 4 ecological states = 108 direct configurations before substrate/slope/current/light/disturbance grammar.
- 36 physical state roots / 399 new objects; exact bathymetry BVH/raycast contact; local +Z aligned to measured substrate normal.
- State counts exact: 9 colonizing / 9 mature / 9 disturbed-recovering / 9 senescent.
- Minimum root separation 10.0 m; approximate minimum clearance to existing local coral/memory-node geometry 19.504 m; explicit traversal overlap 0; UV/material/scale debt 0; visible technical geometry 0.
- These are FUNCTIONAL GUILD PROPOSALS only. Detailed trophic chain, reproduction and population density remain UNKNOWN.
- Source + receipt persisted; Workbench QA artifacts generated; semantic/cinematic GATE-ART remains pending because pixels could not be inspected from the signed artifact host.

### `PEL/MKT/DAMAGE-X100-005`
- Reversible Mercado architecture damage/recovery state-swap foundation.
- Final structurally verified scene checkpoint: **rev. 38**.
- 8 semantic damage families × 4 co-located states × 3 severity variants = 32 authored state roots / 96 direct variant-state combinations.
- Exactly one current state visible per family; alternate states and 8 LOD1 proxies fully hidden.
- Surface attachment and measured normals: PASS; UV/material/scale debt 0; visible technical geometry 0.
- Bridge repair remains 2.728 m from route centerline against 1.5 m reserved half-width — PASS.
- Base architecture is not destructively modified. Runtime fracture/navmesh/debris/persistence remain engine blockers.
- Source + receipt persisted.

## Active claim — `/EXOVANT-X100`
- Claim ID: `PEL/CIV/PROP-X100-006`
- Scope: Mercado cultural/everyday prop expansion II, adding 12 systemic families beyond the first custody/listening/funeral/maintenance kit.
- Why now: post-rev.38 planning-floor ranking puts props at **9 / 30 families = 0.30 floor ratio**, the lowest Blender-addressable multiplier gap. Machinery and sessile ecology are each 9/10; traversal is 5/5; damage is 8/5.
- Target post-wave breadth: at least **21 prop families** total.
- Planned families: wet work surface/seating; tethered hand tools; dry personal lockbox; food/water service vessels; wet first-aid/medical kit; trade measurement/exchange objects; portable refuge lighting; textile drying/repair; waste sorting/bio-safe disposal; weather-screen/storm-stowage module; portable navigation/acoustic marker; market display/modular goods bin.
- Culture DNA constraints: repair-first marine construction; wet/gloved ergonomics; tether points; drainage; corrosion resistance; low heavy mass; detachable/serviceable modules; no invented faction iconography/social hierarchy.
- State grammar target: 12 families × 4 causal states (`pristine`, `used`, `damaged_repaired`, `abandoned`) = 48 authored state roots; 3 semantic variants per family = 144 direct variant-state combinations before placement/orientation grammar.
- Placement rule: integrate across measured Mercado platform/deck bays rather than a single random scatter field; exactly one current state visible per placed family while alternate roots remain authored and hidden.
- DoD: stable IDs; metre/player-scale bounds; functional construction logic; four causal states; three variants; UV0/materials/clean transforms; no floating geometry; no route obstruction; LOD/query collision policy; deterministic generator; structural QA; receipt; post-wave rerank.
- Engine gate: runtime pickup/use, inventory, animation, audio, dynamic state swaps, physics interaction, HLOD thresholds and target-GPU qualification remain `BLOCKED/PENDING` until gameplay/engine authority.

## Current status
`X100_PRODUCTION_ACTIVE`: rev. 38 closes the first machinery, sessile-ecology and damage/recovery gaps. The active production cell is cultural/everyday props II, the current lowest planning-floor ratio.
