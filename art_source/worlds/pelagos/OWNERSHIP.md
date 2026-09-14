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

## Active claim — `/EXOVANT-X100`
- Claim ID: `PEL/MKT/DAMAGE-X100-005`
- Scope: reversible architecture-damage / recovery kit for Mercado de Boyas structures. Overlay/replacement modules only; base architecture is not destructively edited.
- Why now: coverage rerank at rev. 37 measured **2 explicit damage/recovery asset families**, below the X100 5–15 planning range and far below the 63-family architecture layer. Damage therefore remains a multiplicative temporal/story/gameplay gap.
- Planned semantic families: deck impact/spall patch; canopy membrane tear/field patch; articulated-bridge hinge deformation/jam; service-hatch corrosion/seal breach; buoyancy-pod impact/leak clamp; mooring-cleat overload/tear-out plate; utility-channel flood/exposed-service repair; CommandShell stress-crack/emergency brace.
- Causal drivers: storm loading, docking impact, salt/wet-dry corrosion, repeated flex cycles, overload at mooring/load paths, service access, fluid ingress and field repair. No random crack decals, uniform edge wear or decorative destruction.
- State grammar target: 8 damage families × 4 causal states (`stressed`, `damaged`, `field_repaired`, `abandoned`) = 32 physical state exemplars / 96+ authored variant combinations before placement/orientation grammar.
- Placement rule: attach to real Mercado structural targets or an existing test/specimen surface while preserving traversal clearances and keeping the damage system reversible and independently removable.
- DoD: stable IDs; causal damage mechanism; state variants; structural attachment logic; no floating geometry; player/traversal clearance; UV0/materials/clean transforms; soft/query collision unless a state explicitly blocks route; LOD/HLOD policy; deterministic generator; structural QA; receipt.
- Engine gate: runtime fracture, destructibility, navmesh updates, physics debris, persistence/save-state, network replication, production HLOD thresholds and GPU qualification remain `BLOCKED/PENDING` until engine/gameplay authority.

## Current status
`X100_PRODUCTION_ACTIVE`: props, first L3 interior, machinery and sessile ecology are structurally closed. Current wave targets architecture damage/recovery, the next measured multiplicative gap.
