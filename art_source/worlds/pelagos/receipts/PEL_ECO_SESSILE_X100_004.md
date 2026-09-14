# PELAGOS — PEL/ECO/SESSILE-X100-004 receipt

Status: **STRUCTURAL_PASS / VISUAL_ARTIFACT_GENERATED / NOT ENGINE-QUALIFIED**  
Branch: `art/world-pelagos-thalassa-001`  
3D Jutsu project: `39930c08-62bb-4034-b35d-70d0ce51c9d9`  
Final structural checkpoint: **Blender rev. 37**

## Why this claim existed

After the X100 prop, interior and settlement-machinery waves, coverage rerank still found producer/decomposer sessile ecology near zero. That left the ecology graph multiplicatively incomplete even though canonical hero ecology already existed.

The World Bible states that the detailed Pelagos trophic chain, reproduction cycles and population densities are UNKNOWN. Therefore this claim introduces **reversible functional guild proposals**, not irreversible new species canon. It does not replace or retcon canonical Medusa mnémica, Anguila de vidrio, Bóvido de arrecife or Coral escriba.

## Delivered functional families

1. `PEL-ECO-SESSILE-FILTER-FAN-001` — current-facing filter fan.
2. `PEL-ECO-SESSILE-PHOTIC-RIBBON-001` — photic primary-producer ribbon.
3. `PEL-ECO-SESSILE-DETRITUS-MAT-001` — detritus decomposer mat.
4. `PEL-ECO-SESSILE-MINERAL-TUBE-001` — mineral-tube chemo/decomposer colony.
5. `PEL-ECO-SESSILE-NURSERY-CRUST-001` — calcifying juvenile nursery crust.
6. `PEL-ECO-SESSILE-FOULING-FILTER-001` — persistent wet-interface/filter cluster.
7. `PEL-ECO-SESSILE-DECAY-BIOFILM-001` — organic-decay decomposer biofilm.
8. `PEL-ECO-SESSILE-CURRENT-BIOFILTER-001` — porous sponge-like current biofilter.
9. `PEL-ECO-SESSILE-LEE-DETRITUS-001` — lee-zone detritus aggregation.

## State and combinatorial contract

Physical states authored for every family:

- `colonizing`;
- `mature`;
- `disturbed_recovering`;
- `senescent`.

Morphology/exposure variants:

- compact;
- standard;
- spread.

Combinatorial foundation:

- 9 families × 3 variants × 4 ecological states = **108 direct configurations**;
- placement grammar further multiplies by substrate, slope, current, light and disturbance state.

The build physically materializes **36 state roots** (9 families × all 4 states), rather than merely documenting them.

## Causal morphology contract

This system is explicitly anti-random-scatter:

- filter laminas and porous biofilters encode current-facing morphology;
- photic ribbons encode light-access producer function;
- decomposer mats and biofilms encode detritus/organic-resource relationships;
- mineral tubes encode mineral-gradient association;
- nursery crusts encode calcifying juvenile settlement substrate;
- fouling/filter colonies encode persistent wet interfaces;
- lee-zone patches encode down-current deposition.

Ecological states change geometry rather than adding generic grunge:

- colonizing → juvenile growth front;
- mature → active core / maximum functional density;
- disturbed-recovering → localized recovery growth and wider irregular spread;
- senescent → detritus and reduced active density.

## Placement / physical execution

Build operation: `pelagos.x100.sessile-ecology.v1`

- base revision: 36;
- committed revision: **37**;
- collection: `14_CORO_SESSILE_ECO_X100_V1`;
- new objects: **399**;
- physical roots: **36**;
- visible ecology geometry objects: **344**;
- one hidden shared LOD1 exemplar per family;
- collision policy: `none_or_soft_query`.

All physical roots are projected to `PEL_ENV_Bathymetry_2200m` using BVH/raycast. Their local +Z is aligned to the measured bathymetry normal, avoiding guessed elevation or floating scatter.

Authored anchor Z range at rev. 37: **−10.321 m to +9.301 m**.

## Final structural QA — rev. 37

### Coverage exactness

- physical roots: **36**;
- semantic families: **9**;
- roots per family: **4** exactly;
- state counts: 9 colonizing / 9 mature / 9 disturbed-recovering / 9 senescent;
- variants: 9 compact / 18 standard / 9 spread.

### Contact / orientation / scale

- substrate-Z mismatches >5 mm: **0**;
- substrate-normal orientation failures >1°: **0**;
- representative normal error: ~0–0.02°;
- minimum root spacing: **10.0 m**;
- absurd colony scale failures (>3 m footprint or height): **0**;
- sampled colony envelopes generally remain ~0.3–1.7 m scale.

### Technical integrity

- visible geometry missing UV0: **0**;
- visible geometry missing materials: **0**;
- non-unit visible mesh scales: **0**;
- visible LOD/technical geometry: **0**;
- hidden family LOD1 roots: **9**;
- all LOD1 mesh children `hide_render=true` and `hide_viewport=true`.

### Integration / clearance

Existing coral/memory-node collision check excludes giant acoustic-arch/ring/beacon AABBs and considers local visible coral/node geometry only.

- new colonies within <1.0 m approximate clearance of existing coral/memory-node geometry: **0**;
- approximate minimum clearance to pre-existing local coral/node geometry: **19.504 m**;
- explicit walk/path/bridge/traversal overlap hits: **0**;
- collision policy remains soft/query-only, so the guilds do not silently create hard gameplay blockers.

Result: **STRUCTURAL_PASS**.

## Visual evidence

Workbench QA artifacts were generated at rev. 37:

- `qa_x100_sessile_r37_overview.png` — 768×512;
- `qa_x100_sessile_r37_grazing.png` — 768×512.

The signed artifact host could not be pixel-inspected by this execution environment. Therefore the truthful status is `VISUAL_ARTIFACT_GENERATED`; semantic/cinematic GATE-ART is **not** claimed.

## Persisted source

- `art_source/worlds/pelagos/scripts/build_coro_sessile_ecology_x100.py`

The script contains the deterministic family/state grammar, bathymetry BVH projection, normal alignment, functional geometry signatures, causal state evidence and hidden family LOD1 foundation.

## Explicit non-claims / blockers

This receipt does **not** claim:

- a complete Pelagos trophic chain;
- final species taxonomy/naming;
- reproduction cycles or population densities;
- runtime population spawning/simulation;
- acoustic behavior bindings;
- ecological persistence/save-state;
- gameplay harvesting/resources;
- production streaming/HLOD thresholds;
- target-GPU qualification;
- final material/lighting/cinematic GATE-ART.

Those remain `UNKNOWN`, `PROPOSAL`, or `BLOCKED/PENDING` by the appropriate design/engine authority. The Blender-side functional sessile ecology foundation itself is structurally qualified.
