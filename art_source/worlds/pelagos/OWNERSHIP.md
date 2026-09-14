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
- Mercado civilization/prop systemic kit — rev32.
- 9 families × 3 variants × 4 states = 108 direct configurations / ≥432 with cardinal yaw.
- STRUCTURAL_PASS; source + receipt persisted.

### `PEL/MKT/ARCH-X100-002`
- CommandShell service/listening/memory-custody interior — rev34.
- Up to 6,720 credible layout/state configurations; geometry/corridor/technical gates passed.
- Semantic GATE-ART remains pending.

### `PEL/MKT/MACH-X100-003`
- Settlement machinery / utility spine — rev36.
- 9 functional families × 3 variants × 4 service states = 108 direct / ≥432 cardinal-yaw configurations.
- Final UtilityRiser clearance 1.316 m; overlap/UV/material/scale debt 0.

### `PEL/ECO/SESSILE-X100-004`
- Coro producer/filter/decomposer sessile ecology — rev37.
- 9 guild families × 3 variants × 4 ecological states = 108 direct configurations.
- 36 physical state roots; exact bathymetry contact; normal alignment; 10 m minimum root separation; route/technical debt 0.
- Functional-guild proposals only; detailed trophic canon remains UNKNOWN.

### `PEL/MKT/DAMAGE-X100-005`
- Reversible Mercado architecture damage/recovery state swaps — rev38.
- 8 damage families × 4 states × 3 severity variants = 96 direct combinations.
- One visible state/family; base architecture untouched; route/UV/material/scale/technical gates passed.

### `PEL/CIV/PROP-X100-006`
- Mercado cultural/everyday prop expansion II — final rev41.
- 12 families × 3 variants × 4 states = 144 direct configurations.
- 48 authored state roots; one visible/current state/family; 12 hidden LOD1 roots.
- Families: wet work station, tethered tool caddy, dry lockbox, mess vessel set, medical wetkit, trade measure, refuge lamp, textile repair frame, waste sorter, storm stowage, portable acoustic navigation marker, modular goods bin.
- Monolithic build exceeded the 300 s worker deadline cleanly; canonical replay is bounded WEST/EAST batches + datum correction.
- Final QA: grounding/platform/CommandShell/overlap/technical/UV/material/scale violations 0.
- Source: `scripts/build_market_culture_props_x100_v2.py`; receipt: `receipts/PEL_CIV_PROP_X100_006.md`.

### `PEL/CIV/PROP-X100-007`
- Mercado cultural/everyday prop expansion III — **final rev44**.
- 9 families × 3 variants × 4 states = **108 direct configurations**.
- Families: rest sling, rinse basin, line-splicing jig, sealant caddy, salvage sorting tray, maintenance kneeler, fragile wet-goods cradle, waterproof work/route slate, personal tether/harness rack.
- 36 authored state roots; exactly one visible/current state/family; 9 hidden LOD1 roots.
- Placement was preflighted as a staggered second side-belt row. Final structural QA: grounding/platform/CommandShell/inter-family overlap/technical/UV/material/scale violations **0**; preceding authored-geometry QA retained >4.4 m approximate minimum route-envelope clearance.
- Final normalized cultural breadth proof: `PROP-X100-001` 9 + `PROP-X100-006` 12 + `PROP-X100-007` 9 = **30 distinct stable cultural family IDs**.
- X100 cultural planning floor: **30** → **CLOSED**.
- Rev44 scene state: **3,380 objects / 1,836 renderables / 55 collections / 53 materials**.
- Source: `scripts/build_market_culture_props_x100_v3.py`; receipt: `receipts/PEL_CIV_PROP_X100_007.md`.

## X100 breadth decision
`DO_NOT_ADD_FAMILIES_BY_DEFAULT`.

Blender family-count expansion is no longer the highest-value move. New families now require a specific gameplay, narrative, ecological or visual proof that existing grammar cannot satisfy. Do not optimize object count.

The completed large X100 sequence added at least **564 direct systemic configurations** after the earlier foundation:
- machinery 108
- sessile ecology 108
- damage/recovery 96
- cultural expansion II 144
- cultural expansion III 108

This excludes the prior architecture and first cultural-prop grammars.

## Runtime authority resolved
The runtime boundary was inspected against current `main` after rev44 rather than guessed.

Facts:
- current executable prototype engine: **Godot 4.7.2**;
- `scenes/main.tscn` loads `scripts/world.gd`;
- existing Blender→runtime exchange pattern is GLB (`assets/reliquary_gate.glb` is the current proven example);
- `world.gd` recursively removes imported cameras/lights/presentation floors and currently owns Terra interaction dispatch;
- `Progress` is persistent campaign authority;
- `SaveStore` only accepts payloads that `Progress.validate()` accepts;
- `Progress.VERSION == 1` has a closed Terra schema, so Pelagos persistent state requires an explicit versioned migration rather than silently appending fields;
- Unreal 5.8 remains a production candidate pending EXO-012 benchmark, not the current runtime authority.

## Runtime activation handoff — READY
Art-side runtime handoff has been persisted without mutating runtime-owned files or global project state:

- `runtime/pelagos_runtime_manifest.rev44.json`
  - external normalized semantic authority;
  - 30 cultural families;
  - 9 machinery families + 9 separate socket groups;
  - 9 sessile guild families;
  - 8 reversible damage families;
  - 56 semantic/stateful family groups excluding sockets.
- `runtime/PELAGOS_GODOT_ACTIVATION_CONTRACT.md`
  - import/node-resolution contract;
  - state-swap semantics;
  - collision/query mapping;
  - interaction non-assumption rule;
  - explicit Progress v1→v2 migration design;
  - streaming/LOD boundary;
  - runtime acceptance suite and DoD.
- `runtime/validate_pelagos_runtime_manifest.py`
  - stdlib-only cold-check validator for IDs/states/counts/socket integrity/schema.
- `runtime/PELAGOS_RUNTIME_HANDOFF_REV44.md`
  - cold-resume receipt and honest blockers.

Critical integration rule: GLB is geometry transport; the external manifest is semantic authority. Do not depend on Blender custom properties surviving Godot import, do not infer semantic type from prefixes alone, and do not auto-create interaction/collision from descriptive purpose fields.

## Next frontier — activation / integration
Highest-value work now crosses the Blender/runtime boundary:
1. runtime-owned claim/branch resynced from current `main`;
2. source-bound rev44 GLB admission into Godot;
3. manifest validation + exact node resolution;
4. generic world asset-state registry + Pelagos adapter rather than expanding `world.gd` monolithically;
5. explicit `Progress` v2 migration preserving valid v1 saves;
6. visible-state persistence across cold restart;
7. query/collision/navigation semantics for props, machinery and damage overlays;
8. gameplay-approved interaction subset only;
9. streaming + LOD/HLOD thresholds and deterministic cell ownership;
10. target-GPU qualification;
11. semantic GATE-ART evidence against visual references and anti-AI-slop criteria.

These are not claimed complete from Blender evidence alone.

## Current status
`X100_BREADTH_FLOOR_CLOSED_REV44__RUNTIME_HANDOFF_READY`.

World Master structural authoring is substantially broader and stateful. The art owner has now delivered a source-bound runtime activation contract. Do not start another bulk modeling wave until runtime integration or semantic GATE-ART identifies a concrete missing asset requirement.
