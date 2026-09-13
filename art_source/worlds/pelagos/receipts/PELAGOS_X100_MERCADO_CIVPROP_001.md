# PELAGOS X100 — Mercado Civilization Prop System 001

Claim: `PEL/CIV/PROP-X100-001`
Protocol: `/EXOVANT-X100`
Scene project: `39930c08-62bb-4034-b35d-70d0ce51c9d9`
Final verified Blender revision for this receipt: **32**
Status: **SYSTEMIC_FAMILY_FOUNDATION_V1 / STRUCTURAL_PASS / GATE-ART_PENDING**

## Why this wave existed
The X100 coverage audit at rev. 30 found PELAGOS materially ahead in ecology and hero engineering but critically weak in culture-material, daily-life props and temporal-state coverage. This wave therefore maximizes multiple multiplicative dimensions at once rather than adding another isolated hero asset.

## Authored systemic families
1. `PEL-PROP-MEMCUST-001` — memory custody container
2. `PEL-PROP-HYDROPHONE-001` — hydrophone/listening station
3. `PEL-PROP-FUNERAL-BUOY-001` — funeral buoy
4. `PEL-PROP-TRADE-SIGNAL-001` — trading-channel/navigation signal
5. `PEL-PROP-CONSENT-MARKER-001` — consent/timetable physical marker
6. `PEL-PROP-REEF-CLAMP-001` — reef-safe clamp
7. `PEL-PROP-MAINT-CRATE-001` — maintenance crate
8. `PEL-PROP-SERVICE-REEL-001` — service hose/cable reel
9. `PEL-PROP-WET-GEAR-RACK-001` — wet gear/equipment rack

These were selected from World Bible requirements and repair-first construction logic. No unsupported faction iconography or social hierarchy was invented.

## Multiplication grammar
- 9 semantic families
- 3 scale/manufacturing variants: compact / standard / heavy
- 4 causal states: pristine / used / damaged / abandoned
- 108 direct family×variant×state combinations
- 4 cardinal yaw placements => at least **432** credible configuration keys before district/location grammar

The committed scene stages 36 specimens (nine families × four states) rather than baking all 108 one-offs. The generator is deterministic and can materialize the wider grammar.

## Causal state contract
- `pristine`: no synthetic wear overlay.
- `used`: wear only at repeated hand/tool contact.
- `damaged`: visible mismatched field-repair patch + explicit fastener near service/load-access regions.
- `abandoned`: biological fouling concentrated at lower/wet contact zones.

No random scratches, global grunge, meaningless decals or decorative greeble were used as the variation mechanism.

## Culture/manufacturing DNA encoded
- repair-first construction;
- corrosion-resistant frames;
- ivory technical ceramic/composite skins;
- dark waterproof technical textiles;
- visible replaceable panels and standardized fasteners;
- wet/gloved handles and service access;
- buoyancy/drainage/low-heavy-mass logic;
- precursor/oxidized bronze used through clamps, adapters and load-bearing mechanisms;
- memory cyan and amber emissive accents only where semantically motivated.

## Scene evidence
Initial build operation: `pelagos.x100.market-civprops.v1` → rev. 31.

Initial result:
- 382 new objects;
- 309 new meshes;
- ~6,644 estimated tris including hidden technical proxy geometry;
- 36 staged family/state assemblies;
- no UV debt on non-collision meshes;
- no non-unit mesh transforms;
- shared per-family LOD1 and LOD2 proxy assets;
- shared per-family collision/query proxy assets;
- runtime LOD thresholds/collision semantics explicitly pending engine.

## QA and defect closure
`PELAGOS-X100-MERCADO-CIVPROP-QA-STRUCT-R31` found one concrete defect family: three staged reef-safe clamps floated 0.118–0.166 m above the deck. No other family floated; there were no XY assembly overlaps, missing materials, missing UVs, non-unit transforms or visible technical shards.

`pelagos.x100.clamp-contact-fix.v1` corrected only the clamp staging-root Z contact and committed rev. 32. The persisted generator now also performs deterministic physical-core grounding against the deck support plane.

Final structural verification `PELAGOS-X100-MERCADO-CIVPROP-QA-STRUCT-R32`:
- roots: 36/36;
- each family: 4 staged states;
- state distribution: 9 pristine / 9 used / 9 damaged / 9 abandoned;
- floating assemblies: 0;
- excessive deck intersections: 0;
- missing UVs: 0;
- missing materials: 0;
- non-unit mesh scales: 0;
- visible LOD/collision technical meshes: 0;
- result: **PASS**.

## Visual evidence
Workbench QA artifacts were generated at rev. 32:
- `qa_x100_market_civprops_r32_full.png`
- `qa_x100_market_civprops_r32_close.png`
- temporary 1.75 m human-scale proxy included in the visual QA query.

The current connector exposes the artifact metadata/download but did not expose image pixels to this agent for direct semantic visual inspection. Therefore this receipt deliberately records `VISUAL_ARTIFACT_GENERATED` and **does not claim GATE-ART PASS**. Human/vision-capable review of silhouette hierarchy, aesthetic coherence and state readability remains pending.

## LOD / collision truth
Real hidden LOD1/LOD2 family proxy objects and collision/query proxies exist. They are **Blender-side foundations**, not runtime-qualified systems.

Pending engine-gated work:
- final switch thresholds;
- runtime interaction bindings;
- exact blocking vs overlap semantics;
- HLOD / instancing strategy;
- target-GPU profiling;
- import validation after EXO-012 production engine decision.

## Definition of Done state
PASS now:
- semantic purpose;
- stable IDs;
- meter-scale dimensions;
- staged player-scale context;
- causal manufacturing/material logic;
- UV0/material slots;
- clean transforms;
- support-plane contact;
- variation/state grammar;
- preliminary LOD/collision strategy and geometry;
- deterministic placement metadata;
- >100 credible configuration grammar;
- technical receipt;
- reproducible source generator.

Still open before `FAMILY_COMPLETE`:
- semantic visual GATE-ART;
- broader district placement pass;
- engine import/runtime qualification;
- target-GPU optimization proof;
- interaction gameplay implementation;
- export/prefab persistence after engine target is selected.

## Source
`art_source/worlds/pelagos/scripts/build_market_civprops_x100_v1.py`
