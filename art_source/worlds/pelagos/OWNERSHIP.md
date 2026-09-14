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

## Next frontier — activation / integration
Highest-value work now crosses the Blender/runtime boundary:
1. import/export manifest + stable-ID registry for Pelagos stateful families;
2. engine binding for visible-state swaps and save-state persistence;
3. query/collision/navigation semantics for props, machinery and damage overlays;
4. interaction contract for daily-life props and machinery without inventing unsupported mechanics;
5. streaming + LOD/HLOD thresholds and deterministic cell ownership;
6. target-GPU performance qualification;
7. semantic GATE-ART evidence against visual references and anti-AI-slop quality criteria.

These are not claimed complete from Blender evidence alone.

## Current status
`X100_BREADTH_FLOOR_CLOSED_REV44`.

World Master structural authoring is substantially broader and stateful. The next production cell must identify the repository's actual runtime/engine authority and integrate these stable IDs there, or close semantic GATE-ART. Do not start another bulk modeling wave until one of those gates produces a concrete missing asset requirement.
