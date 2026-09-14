# EXOVANT 2950 — WORLD SYSTEMS MASTER

**Status:** R&D master / pre-canon architecture input  
**Date:** 2026-09-14  
**Purpose:** consolidate the current world-generation thesis, research direction, architectural decisions under consideration, production implications, experiments, gates and execution order into one death-safe artifact.  
**Authority:** this document does **not** silently override `AGENTS.md`, `_project_intelligence/STATE.json`, `_project_intelligence/PLAN.json`, `design/EXOVANT_BIBLIA.md` or `design/EXOVANT_DATA.json`. Accepted conclusions must be promoted through explicit ADR/plan/canon updates.

---

# 1. NORTH STAR

EXOVANT must prove that a very large interplanetary universe can be produced from a deliberately limited number of extraordinarily large, dense and systemic worlds, with local areas capable of sustaining hours of meaningful exploration, while preserving authored identity and AAA-target visual quality.

The production thesis is not `model enormous worlds manually`. It is:

> **Design laws, cultures, histories, art vocabularies and constraints; compile worlds from them; validate them automatically; hand-author the highest-value exceptions.**

The critical metric is not number of planets. It is **meaningful depth per unit area and per human production hour**.

The existing twelve worlds remain valuable as major authored civilization/world anchors. The new architecture should make them deeper rather than discard their IP.

---

# 2. CORE CHANGE OF DOCTRINE

## Old implicit model

`design world -> model world in Blender -> import scene -> populate -> gameplay`

This does not scale to planet-sized worlds with dense interiors, infrastructure, NPCs, history, ecology and systemic change.

## Target model

`design physical laws + culture + history + art vocabulary + grammars + constraints -> World Compiler -> deterministic base world -> authored hero overrides -> validation -> streaming/runtime materialization -> persistent player deltas`

Blender remains important, but becomes an **Asset Authoring Environment**, not the database or authoring surface for entire planets.

Blender/Houdini/DCC work should primarily produce:
- hero assets and landmarks;
- modular architectural kits;
- structural modules/connectors;
- props and mechanical kits;
- trims, decals and material vocabularies;
- creatures, vehicles and rigs;
- collision/LOD/reference geometry;
- clean reusable source assets.

A world owner should increasingly own **world identity, art direction, kits, constraints, hero locations and acceptance**, not attempt to manually mesh every square kilometre.

---

# 3. RESEARCH THESIS: WHAT TO LEARN FROM NO MAN'S SKY

The useful lesson from No Man's Sky is not its planet count. The useful principle is that deterministic procedural systems can represent a world far larger than stored authored geometry by reconstructing content from seeds, algorithms and reusable authored components.

Research must distinguish:
- documented fact;
- technical inference;
- EXOVANT proposal.

Primary investigation lanes:
1. deterministic seeds and hierarchical generation;
2. terrain/noise/planet generation;
3. authored asset vocabularies and procedural recombination;
4. runtime vs offline generation;
5. streaming and reconstruction;
6. flora/fauna/ecosystem variation;
7. repetition and local-depth failure modes;
8. how modern PCG can exceed the structural limitations of broad but shallow generation.

EXOVANT must explicitly optimize for the inverse trade-off: **fewer worlds, dramatically greater local semantic density and causal depth**.

---

# 4. PROCEDURAL AUTHORED DENSITY

Canonical candidate principle:

> Procedural systems provide scale; authored systems provide identity; simulation provides causality; constraints provide coherence; validation provides quality.

Use three broad production classes:

## HERO (~5%)
Hand-directed/high-touch:
- major city centres;
- boss arenas;
- signature monuments;
- critical story locations;
- civilization-defining architecture;
- iconic vistas/landmarks.

## SUPPORT (~20%)
Parametric/semi-authored:
- temples;
- factories;
- stations;
- farms;
- military facilities;
- settlement archetypes;
- major infrastructure.

## SYSTEMIC (~75%)
Compiler-produced under strong rules:
- housing;
- streets;
- utilities;
- minor interiors;
- vegetation distribution;
- caves;
- industrial support structures;
- minor POIs;
- environmental detail.

The percentages are planning guidance, not a quota. Variation must be causal, not noise.

---

# 5. WORLD COMPILER — TARGET ARCHITECTURE

Create a first-class subsystem, provisionally:

`tools/world-compiler/`

Conceptual modules:

```text
UniverseCompiler
StarSystemCompiler
PlanetCompiler
GeologyCompiler
ClimateCompiler
HydrologyCompiler
BiomeCompiler
EcologyCompiler
CivilizationCompiler
HistoryCompiler
TerritoryCompiler
EconomyCompiler
InfrastructureCompiler
SettlementCompiler
RoadCompiler
CityCompiler
DistrictCompiler
BuildingCompiler
InteriorCompiler
PopulationCompiler
FactionCompiler
NarrativeCompiler
EncounterCompiler
SecretCompiler
DensityCompiler
ValidationCompiler
StreamingPackageCompiler
```

Generation dependency chain:

```text
SEED
 -> MACRO CONSTRAINTS
 -> PHYSICAL WORLD
 -> CLIMATE/HYDROLOGY/ECOLOGY
 -> HISTORY SIMULATION
 -> CIVILIZATIONS
 -> TERRITORIES
 -> INFRASTRUCTURE
 -> SETTLEMENTS
 -> ARCHITECTURE
 -> INTERIORS
 -> POPULATION
 -> FACTIONS/ECONOMY
 -> NARRATIVE/EVENTS
 -> DENSITY PASS
 -> ART COMPOSITION PASS
 -> VALIDATION
 -> STREAMING PACKAGE
```

A city must not exist because RNG selected `CITY`. Its location, morphology and function should emerge from terrain, water, resources, transport, history, population, economy, defense and culture constraints.

---

# 6. HIERARCHICAL WORLD MODEL

Spatial hierarchy candidate:

```text
Universe
 -> Galactic Region
 -> Star System
 -> Planetary Body
 -> Continent
 -> Region
 -> Biome
 -> Territory
 -> Settlement
 -> District
 -> Block
 -> Parcel
 -> Building
 -> Floor
 -> Room
 -> Prop/Interactable
```

Semantic hierarchy intersects it:

```text
Civilization
 -> Species/Population
 -> Culture
 -> Language/Naming
 -> Belief/Philosophy
 -> Political System
 -> Economy
 -> Technology
 -> Infrastructure
 -> Factions
 -> Historical Timeline
 -> Territorial Influence
```

World geometry should be downstream of both physical and semantic state.

---

# 7. HIERARCHICAL SEEDS + VERSIONING

Never define a world only by one seed.

Child seeds derive deterministically from stable IDs and parent seeds:

```text
GalaxySeed    = H(UniverseSeed, galaxyID)
SystemSeed    = H(GalaxySeed, systemID)
PlanetSeed    = H(SystemSeed, planetID)
RegionSeed    = H(PlanetSeed, regionID)
CitySeed      = H(RegionSeed, cityID)
DistrictSeed  = H(CitySeed, districtID)
BuildingSeed  = H(DistrictSeed, buildingID)
InteriorSeed  = H(BuildingSeed, interiorID)
```

Every generated entity needs at minimum:

```text
entity_id
parent_id
seed
generator_version
ruleset_version
artkit_version
manual_patchset_version
```

World identity is:

`seed + generator versions + rules + datasets + art-kit versions + authored overrides`

This is required for reproducibility, migration, regression testing and partial regeneration.

---

# 8. BASE WORLD + DELTA STATE

Do not persist every generated stone/object as save data.

```text
Base World = deterministic compiler output
Player World = Base World + persistent delta state
```

Persist meaningful mutations:
- destroyed/repaired structures;
- opened/locked states;
- deaths;
- faction control;
- bridges/routes changed;
- inventory/economy state;
- quest/world consequences;
- authored permanent modifications.

This separates world scale from save size.

---

# 9. SIMULATION LOD

A planet cannot run full AI for every resident.

Candidate relevance hierarchy:

```text
S0 Galactic statistical simulation
S1 Civilization simulation
S2 Planet/regional simulation
S3 Settlement/district simulation
S4 Player-vicinity entity simulation
S5 Immediate full-fidelity simulation
```

S0/S1 may track aggregates such as population, production, war, migration and technology.
S2 adds ecology, regional trade, weather and territory.
S3 adds district activity, businesses, transport and faction events.
S4 materializes actual NPCs/vehicles/navigation/combat.
S5 enables expensive AI, physics, animation, inventory, dialogue and destruction.

Relevance is a function of more than distance:
- player proximity;
- narrative importance;
- recent interaction;
- persistent dependency;
- scheduled events;
- visibility/audibility;
- gameplay criticality.

---

# 10. PLANET TECH RESEARCH TARGET

Required investigation/prototyping:
- spherical/planet-scale coordinate model;
- large-world coordinates/origin rebasing;
- space-to-surface transition;
- planetary terrain representation;
- multi-resolution terrain/clipmaps/virtualization;
- erosion and geological plausibility;
- tectonic/structural macroforms where useful;
- hydrology and drainage;
- oceans;
- caves/subsurface layers;
- atmosphere;
- weather/climate;
- biome transitions;
- ecology distribution;
- streaming across multiple orders of magnitude.

Do not commit to physically perfect simulation where perceptual plausibility plus deterministic constraints gives better production economics.

---

# 11. CIVILIZATION COMPILER

Civilizations should derive from causal variables rather than arbitrary visual themes.

Candidate dependency chain:

`environment -> resources -> biology -> technology -> social structure -> beliefs -> politics -> economy -> architecture -> language -> warfare -> urbanism`

Run abstract historical simulation to produce consequences:
- ruins;
- old roads;
- borders;
- abandoned settlements;
- religious sites;
- fortifications;
- mines;
- trade routes;
- migration/diaspora;
- scars from conflict;
- architectural strata.

History becomes a generator input for geography rather than lore pasted after level design.

---

# 12. INFRASTRUCTURE-FIRST SETTLEMENTS

Settlements require functional networks:
- water;
- energy;
- food;
- transport;
- industry;
- waste;
- communication;
- defense.

These networks condition land value, density, districts, road topology, industrial placement and population distribution.

Not every system must be individually simulated. Use statistical representation until local materialization matters.

---

# 13. BUILDING + INTERIOR GRAMMARS

Never generate buildings as arbitrary boxes.

Pipeline:

`building purpose -> required functions -> spatial program -> adjacency graph -> circulation -> structure -> facade grammar -> services -> interior kit -> props`

Example: a hospital semantically requires entrance/triage/emergency/diagnostics/wards/surgery/staff/storage/waste/maintenance/energy relationships. A factory, temple or residence has different grammar.

Interior LOD candidate:

```text
I0 statistical: function/capacity/population only
I1 structural: floors/rooms/doors/navigation topology
I2 playable: meshes/props/NPCs/loot/lighting/physics
```

Materialize I2 near/for the player deterministically rather than keeping every room instantiated globally.

---

# 14. ASSET GRAMMAR

Every reusable asset should acquire machine-readable semantics, not only filenames.

Candidate fields:

```yaml
asset_id: VAN_ARCH_WALL_A12
category: wall
civilization: vanta
style_tags: [industrial, brutalist]
dimensions: {width: 4, height: 3}
connectors: {left: WALL_A, right: WALL_A}
allowed_contexts: [industrial, port]
forbidden_contexts: [luxury_residential]
weathering: [salt, corrosion]
semantic_roles: [factory, infrastructure]
performance_class: support
```

World generation operates over semantic compatibility + geometric connectors + performance constraints.

---

# 15. DENSITY COMPILER

Create a `DensityCompiler` / validator that evaluates spatial cells rather than relying on subjective claims.

Candidate base cell: 250m x 250m, aggregated to km² and larger regions.

Track at least:
- traversal interest;
- visual interest;
- interaction density;
- verticality;
- narrative density;
- secret density;
- combat affordances;
- social density;
- enterable/interior density;
- landmark visibility;
- semantic uniqueness;
- route diversity;
- environmental storytelling;
- systemic events.

Candidate EXOVANT Density Index (EDI):

```text
0.15 Discovery
0.15 Semantic uniqueness
0.12 Traversal complexity
0.12 Interior depth
0.10 Narrative affordances
0.10 Systemic interactions
0.08 Verticality
0.06 Secret density
0.05 NPC agency
0.04 Combat variation
0.03 Landmark composition
```

Weights are hypotheses until calibrated against authored benchmark areas and playtests.

Do not maximize density uniformly. Measure pacing/interest curves: quiet -> tension -> discovery -> reward -> quiet -> foreshadow -> challenge -> reveal.

Target concept: dense urban/hero areas may sustain several hours/km²; wilderness can be substantially lower while retaining route, landmark and discovery quality. Exact thresholds require empirical calibration.

---

# 16. ANTI-REPETITION / SEMANTIC FINGERPRINTS

Every generated POI/layout can emit a semantic fingerprint:

```json
{
  "biome": "...",
  "terrain_form": "...",
  "architecture_family": "...",
  "poi_role": "...",
  "encounter_shape": "...",
  "narrative_function": "...",
  "material_palette": "...",
  "layout_signature": "...",
  "reward_class": "..."
}
```

Nearby content above a similarity threshold is rejected, mutated or regenerated unless repetition is intentionally causal.

Measure repetition across multiple radii and play routes, not only globally.

---

# 17. NARRATIVE SYSTEM

Do not use runtime LLM improvisation as the foundation of world coherence.

Narrative generation should operate from structured facts:
- world history;
- faction goals;
- character goals;
- resources;
- conflicts;
- locations;
- relationships;
- prior consequences.

Candidate graph primitives:

`CAUSE -> CONFLICT -> OPPORTUNITY -> AGENT -> LOCATION -> CONSEQUENCE`

Quests/events should emerge from world state or authored narrative graphs, not generic filler templates.

LLMs/agents are useful primarily offline/build-time for:
- research;
- ideation;
- variant generation;
- lore/dialogue proposals;
- semantic tagging;
- QA;
- consistency checking;
- layout critique;
- test generation.

The shipped game remains capable of functioning offline without provider APIs.

---

# 18. MANUAL OVERRIDES

Procedural generation must support authored control:

```text
LOCK
PATCH
EXCLUDE
OVERRIDE
```

Hero regions can be locked against regeneration. Generator upgrades must not silently destroy authored locations.

Overrides must be versioned and address stable entity/region IDs.

---

# 19. WORLD VALIDATION

Create a first-class validator, provisionally `tools/world-validator/`.

Automated checks should include:
- terrain holes/seams;
- impossible required slopes;
- floating/interpenetrating assets;
- blocked doors;
- unreachable rooms;
- roads to nowhere;
- invalid building grammars;
- nav islands;
- quest deadlocks;
- missing infrastructure dependencies;
- duplicate layouts;
- POI semantic repetition;
- density deserts;
- pathological over-density;
- streaming spikes;
- memory spikes;
- spawn traps;
- invalid persistence references;
- seed/version reproducibility failures.

A generated world is not accepted merely because compilation succeeds.

---

# 20. AUTOMATED EXPLORERS

Build headless/low-fidelity traversal agents to inspect generated worlds at scale.

Measure:
- distance/time before discovery;
- time between meaningful POIs;
- route diversity;
- dead ends;
- unreachable content;
- combat frequency;
- reward cadence;
- traversal entropy;
- semantic repetition;
- navigation failures;
- generation/runtime costs.

Use many seeds and preserve failing seeds as regression fixtures.

---

# 21. WORLD OBSERVABILITY

Every compiler build should be capable of emitting:
- world/planet manifest;
- generation timing;
- population/civilization summaries;
- POI counts;
- unique layout counts;
- density heatmaps;
- semantic similarity maps;
- route/navigation failures;
- streaming weight;
- memory/disk estimates;
- generator/rules/art-kit versions;
- validation receipts.

A 2D/3D inspection surface should allow designers