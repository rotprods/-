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

### `PEL/MKT/ARCH-X100-002`
- Mercado CommandShell service/listening/memory-custody interior systemic cell.
- Final structurally verified scene checkpoint: rev. 34.
- Up to 6,720 credible layout/state configurations; geometry, corridor and technical-debt gates passed.
- Semantic GATE-ART remains pending.

### `PEL/MKT/MACH-X100-003`
- Mercado settlement machinery / utility-spine systemic foundation.
- Final structurally verified rev. **36**.
- 9 functional families × 3 variants × 4 service states = 108 direct / ≥432 cardinal-yaw configurations.
- Final minimum UtilityRiser clearance 1.316 m; physical overlap/UV/material/scale debt 0.

### `PEL/ECO/SESSILE-X100-004`
- Coro functional producer/filter/decomposer sessile ecology foundation.
- Final structurally verified rev. **37**.
- 9 functional guild families × 3 variants × 4 ecological states = 108 direct configurations.
- 36 physical state roots; exact bathymetry contact; local-normal alignment; 10 m minimum root separation; route/technical debt 0.
- Functional-guild proposals only; detailed trophic canon remains UNKNOWN.

### `PEL/MKT/DAMAGE-X100-005`
- Reversible Mercado architecture damage/recovery state-swap foundation.
- Final structurally verified rev. **38**.
- 8 damage families × 4 co-located states × 3 severity variants = 96 direct combinations.
- Exactly one state visible per family; base architecture not destructively edited; route/UV/material/scale/technical gates passed.

### `PEL/CIV/PROP-X100-006`
- Mercado cultural/everyday prop expansion II.
- Final structurally verified scene checkpoint: **rev. 41**.
- 12 systemic families × 3 variants × 4 causal states = **144 direct configurations**.
- 48 authored state roots; exactly one visible/current state per family; 12 hidden LOD1 roots.
- Families: wet work station, tethered tool caddy, dry lockbox, mess vessel set, medical wetkit, trade measure, refuge lamp, textile repair frame, waste sorter, storm stowage, portable acoustic navigation marker, modular goods bin.
- Monolithic 12-family build timed out cleanly at rev38; bounded WEST/EAST mutations produced rev39/rev40, followed by transform-only grounding correction rev41. This staged replay is canonical.
- Final QA: grounding violations 0; platform overflow 0; CommandShell hits 0; physical family overlaps 0; visible technical leakage 0; UV/material/scale debt 0. Minimum previously measured route clearance ~6.815 m.
- Source contract: `scripts/build_market_culture_props_x100_v2.py`; receipt: `receipts/PEL_CIV_PROP_X100_006.md`.
- Runtime pickup/use, inventory, physics, dynamic state swaps, audio, production HLOD and GPU qualification remain engine gates.

## Active claim — `/EXOVANT-X100`
- Claim ID: `PEL/CIV/PROP-X100-007`
- Scope: Mercado cultural/everyday prop expansion III — final floor-closing wave.
- Why now: PROP-X100-001 (9 families) + PROP-X100-006 (12 families) yields **21 normalized cultural prop families**. The X100 planning floor is 30, leaving exactly **9 families** to close this Blender-addressable breadth gap.
- Target post-wave breadth: **30 normalized cultural prop families** total.
- Planned families, deliberately lore-light and function-first:
  1. rest sling / berth roll (`REST`)
  2. rinse / wash basin (`RINSE`)
  3. line-splicing jig (`SPLICE`)
  4. sealant / repair-consumables caddy (`SEAL`)
  5. salvage sorting tray (`SALVAGE`)
  6. maintenance kneeler / low step (`KNEEL`)
  7. fragile wet-goods transport cradle (`CRADLE`)
  8. waterproof temporary work/route slate (`SLATE`)
  9. personal tether/harness rack (`HARNESS`)
- These are not faction ranks, currencies or irreversible lore. They represent generic daily-life, repair, safety and work functions compatible with existing Mercado culture DNA.
- Culture DNA constraints remain: repair-first marine construction; wet/gloved ergonomics; tethering; drainage; corrosion resistance; low/heavy mass; replaceable parts; storm stowage; causal wear; no unsupported iconography/social hierarchy.
- Grammar target: 9 families × 3 variants (`compact|standard|communal`) × 4 states (`pristine|used|damaged_repaired|abandoned`) = **108 direct configurations** before placement/orientation grammar.
- Production rule: use a second staggered east/west side-belt row with measured route and existing-prop clearance; split mutation into bounded batches if needed to stay under the 300 s 3D-worker deadline.
- DoD: stable IDs; one visible/current state per family; UV0/materials/clean transforms; deck grounding; no CommandShell/platform/route obstruction; hidden LOD1 roots; deterministic source + receipt; final normalized coverage proof ≥30 families.
- Engine gate: runtime pickup/use, inventory, animation, audio, physics, state persistence, HLOD thresholds and target-GPU qualification remain `BLOCKED/PENDING`.

## Current status
`X100_PRODUCTION_ACTIVE`: PROP-X100-006 is structurally closed at rev41. The active production cell is PROP-X100-007, designed to close the 30-family cultural planning floor exactly.
