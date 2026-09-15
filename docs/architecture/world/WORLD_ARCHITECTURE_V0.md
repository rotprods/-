# EXOVANT 2950 — WORLD ARCHITECTURE V0

Status: PROPOSED / implementation-driving architecture, not shipped-game claim
Date: 2026-09-15
Source: `docs/research/world-generation/EXOVANT_WORLD_SYSTEMS_MASTER_2026-09-14.md`

## 1. Mission

Build a deterministic, versioned World Compiler that turns authored laws, physical constraints, civilization state, art vocabularies and manual overrides into dense playable world packages. Optimize for meaningful local depth and authored identity, not planet count.

## 2. Non-negotiable invariants

1. Runtime game remains playable offline; provider AI is not a world-runtime dependency.
2. Same input manifest + same compiler/rules/art versions => same canonical output digest.
3. Generated base state and persistent player delta state are separate.
4. Stable entity IDs survive regeneration whenever their semantic identity survives.
5. Hero locks/patches outrank procedural output and cannot be silently overwritten.
6. Geometry is downstream of physical + semantic constraints, not unconstrained RNG.
7. Every generated region emits provenance, metrics and validation receipts.
8. A successful compile is not an accepted world; validation and art/play gates remain distinct.
9. Generator upgrades require explicit migration/requalification; seed alone is never world identity.
10. Planet-scale simulation is multi-resolution; full-fidelity agents exist only where relevance warrants it.

## 3. Compiler DAG

```text
UniverseManifest
  -> PhysicalMacro
     -> Geology -> Hydrology -> Climate -> Biomes -> Ecology
  -> HistoricalMacro
     -> Civilizations -> History -> Territory -> Economy
  -> Infrastructure
     -> transport/water/energy/food/industry/waste/comms/defense
  -> Settlements
     -> City -> District -> Block -> Parcel
  -> Architecture
     -> BuildingProgram -> Adjacency -> Structure -> Facade -> InteriorTopology
  -> Population/Factions
  -> Narrative/Encounters/Secrets
  -> DensityComposition
  -> ArtResolution
  -> Validation
  -> StreamingPackage
```

Each node consumes typed upstream artifacts and emits typed artifacts plus provenance. No compiler may reach sideways into mutable runtime state.

## 4. Spatial identity

Hierarchy:
`universe/system/planet/continent/region/territory/settlement/district/block/parcel/building/floor/room/entity`.

Stable ID form is semantic and path-derived, e.g. `exo:vanta:region-004:city-002:district-007:block-011:building-003`. Seeds are derived with a specified hash from parent seed + stable child ID + domain separator. Random iteration order must never determine identity.

## 5. World identity contract

A compiled unit is identified by:

```text
stable_id
root_seed
compiler_version
module_versions
ruleset_versions
dataset_versions
artkit_versions
manual_patchset_version
input_digest
output_digest
```

All values are recorded in a generation manifest. Reproducibility tests compare output digests for fixed fixtures.

## 6. Base + Delta persistence

`PlayableState = GeneratedBase(versioned) + AuthoredOverrides(versioned) + PersistentDelta(save)`.

Delta examples: destroyed structure, opened state, NPC death, faction control, route change, quest consequence. Saves never need to serialize untouched generated content. Migration must resolve delta targets against stable IDs and fail visibly when an identity cannot be reconciled.

## 7. Simulation LOD

- S0 universe: aggregates only.
- S1 civilization: population/economy/war/migration/technology.
- S2 planet/region: ecology/weather/trade/territory.
- S3 settlement: district activity/business/transport/faction events.
- S4 vicinity: concrete NPCs/vehicles/nav/combat.
- S5 immediate: expensive AI/physics/animation/dialogue/destruction.

Promotion/demotion uses distance plus narrative importance, recent interaction, persistence dependencies, scheduled events and visibility. State transitions must be deterministic/reconcilable.

## 8. Interior materialization

I0 statistical -> I1 structural topology -> I2 playable realization. Buildings can exist globally at I0/I1 while meshes, props, NPCs, physics and lighting are materialized only for relevant I2 interiors. I2 regeneration uses stable building/interior identity and persistent deltas.

## 9. Procedural Authored Density

HERO: manually directed signature content. SUPPORT: parameterized authored archetypes. SYSTEMIC: compiler-produced under grammar and constraints. 5/20/75 remains planning guidance, never a quota.

The Density Compiler works over spatial cells and evaluates discovery, semantic uniqueness, traversal, interior depth, narrative affordances, systemic interactions, verticality, secrets, NPC agency, combat variation and landmark composition. Uniform maximum density is forbidden; pacing curves are first-class.

## 10. Anti-repetition

Every generated POI/layout emits a semantic fingerprint. Similarity is evaluated over multiple radii and likely routes. Above-threshold repetition requires intentional causal justification or reject/mutate/regenerate. Failing seeds become regression fixtures.

## 11. Art boundary

Blender/Houdini/DCC produce semantic reusable vocabulary: hero assets, kits, connectors, trims, materials, rigs, props, vehicles, creatures and exceptions. Whole planets are not authored as monolithic DCC scenes. Each reusable asset requires machine-readable context, connector, semantic and performance metadata.

## 12. Override precedence

`LOCK > PATCH/OVERRIDE > compiler output`. EXCLUDE prevents generator occupancy. Overrides address stable IDs/regions and are versioned. Compiler upgrades must report conflicts rather than overwrite hero work.

## 13. Runtime boundary

Build/offline: expensive generation, historical simulation, semantic QA, agent-assisted ideation/tagging, baking and package generation.
Runtime: streaming, local materialization, bounded simulation, deterministic local generation where justified, and delta application. No network AI requirement.

## 14. Observability

Each compile emits: manifest, dependency graph, timing, counts, density heatmap data, similarity diagnostics, nav/reachability diagnostics, memory/disk estimates, validation findings and exact version provenance.

## 15. Acceptance ladder

T0 contracts/determinism -> T1 1 km² physical proof -> T2 settlement/building proof -> T3 interiors -> T4 civilization/state -> T5 density/narrative -> T6 art integration -> T7 16 km² vertical world slice -> T8 engine-equivalent benchmark -> T9 regional scale -> T10 planet prototype.

Scaling is forbidden when the previous tier fails its quality/performance/reproducibility gates.
