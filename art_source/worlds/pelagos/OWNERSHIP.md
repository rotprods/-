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

## Active claim — `/EXOVANT-X100`
- Claim ID: `PEL/MKT/MACH-X100-003`
- Scope: settlement machinery / utility-spine systemic family for Mercado de Boyas. No vehicle internals and no boss apparatus.
- Why now: X100 rerank at Blender rev. 34 found **settlement machinery objects = 0**, while L3 interior is no longer zero. This is the next multiplicative bottleneck.
- Planned semantic families: drainage/bilge pump; service filtration skid; ballast/buoyancy transfer unit; mooring tension winch; overload/storm-release unit; pressure/equalization manifold; acoustic relay/conditioning cabinet; fluid heat-exchange skid; service hoist.
- Epistemic rule: these are engineering proposals derived from canonical marine constraints (wet/dry cycling, drainage, buoyancy, mooring, acoustic systems, corrosion, maintainability), not irreversible lore. Exact energy source/control technology remains unspecified.
- Variation grammar: 9 families × 3 capacity variants × 4 causal service states = 108 direct family configurations before orientation/placement grammar.
- Placement target: utility gallery west of the new service/listening cell, inside/adjacent to existing CommandShell service network and near `ServiceChannel_05` / UtilityRiser, while preserving bridge corridors and player clearance.
- DoD: stable IDs, meter-scale dimensions, service input/output sockets, maintenance access, causal wear/repair/decommission states, UV0/materials/clean transforms, collision/query policy, LOD/HLOD strategy, deterministic generator, >100 configuration grammar, structural QA, visual evidence, receipt.
- Engine gate: runtime fluid simulation, interactive controls, power semantics, audio behavior, physics, HLOD thresholds and GPU qualification remain `BLOCKED/PENDING` until production-engine decision.

## Current status
`X100_PRODUCTION_ACTIVE`: current wave closes the settlement-machinery zero without inventing decorative sci-fi machinery.
