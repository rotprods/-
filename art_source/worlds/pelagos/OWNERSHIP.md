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

## Active claim — `/EXOVANT-X100`
- Claim ID: `PEL/CIV/PROP-X100-001`
- Scope: Mercado de Boyas civilization/prop systemic kit; daily life, maintenance, storage, memory-custody, consent/trade signalling and funeral-buoy families only.
- Why now: X100 audit at Blender rev. 30 found ecology/hero engineering materially ahead of prop/cultural/temporal-state coverage. Prop inventory is the highest-value multiplicative gap.
- Canon constraints: World Bible §7, §8, §13–14. Repair-first manufacturing, corrosion-driven construction, buoyancy/maintainability logic; no invented faction iconography or irreversible lore.
- DoD: stable IDs; player-scale dimensions; semantic family graph; causal pristine/used/damaged/abandoned states where justified; UV0/material slots/transforms/pivots; collision/query policy; LOD strategy; deterministic placement sockets/rules; 100+ credible kit configurations; structural/visual QA; receipt; reproducible generator.
- Engine gate: runtime interaction, HLOD/switch thresholds, physics semantics and GPU qualification remain `BLOCKED/PENDING` until production-engine decision.

## Current status
`X100_PRODUCTION_ACTIVE`: world foundation, hero ecology/characters/enemies/vehicle and several Blender-side LOD/collision foundations exist; current work is densifying missing civilization/prop/state layers rather than adding isolated hero assets.
