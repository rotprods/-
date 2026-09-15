# KHEPRI X100 — Material Surface Library Contract

Claim: `CLM-KHEPRI-MATERIALS-001`  
Owner: `AGENT-KHEPRI-MATERIALS-001`  
Branch: `art/khepri-materials-001`  
Protocol: `/EXOVANT-X100`

## North Star

Maximize credible KHEPRI material depth per authored source through physically/semantically motivated variation. The library must communicate manufacture, use, heat, maintenance and repair without random grunge, generic edge wear or unmotivated emission.

## Canon material families

1. `KHP_MAT_GLASS_SOLAR_001` — solar glass / vitrified substrate.
2. `KHP_MAT_MIRROR_OPTICAL_001` — mirror / reflector surfaces.
3. `KHP_MAT_BRONZE_SYNOD_001` — bronze structural/mechanical elements.
4. `KHP_MAT_CERAMIC_SCORCHED_001` — scorched ceramic thermal shielding.
5. `KHP_MAT_FABRIC_SHADE_001` — fabrics / shade systems.
6. `KHP_MAT_MINERAL_DESERT_001` — dark mineral / high-contrast thermal mass.

Reference environment: `71 °C` authored-area temperature. Atmospheric composition, humidity, precipitation and oxidation chemistry are unknown; do not invent atmosphere-driven corrosion chemistry.

## Material causality grammar

Base states need no damage mask: `calibrated`, `intact`, `taut_service`, `cut_clean`.

Causal state classes:

- `contact_use`: service wear, micro-abrasion, contact polishing, handled fabric, foot-traffic wear;
- `maintenance`: cleaning/service states;
- `thermal`: heat cycling, local heat effects, solar aging, thermal fissure proxy;
- `repair`: laminate/recoat/field patch/replacement/stitch/mechanical patch;
- `mechanical_stress`: stress chipping.

Every non-base state must map to at least one cause. Causal masks describe *where* the cause acts; no all-over noise pass is allowed.

## PBR channel contract

- BaseColor: sRGB, substrate/pigment only; no baked lighting or AO.
- Normal: Non-Color / linear; OpenGL +Y convention.
- MR/ORM source: Non-Color / linear. G = Roughness, B = Metallic. R may carry AO source data but AO export is not claimed until verified.
- StateMask: Non-Color / linear. Calibration implementation may encode use/thermal/repair/stress channels; metadata is authoritative when one RGBA texture cannot encode every semantic class.
- Height: optional source-authoring channel; no glTF runtime claim.
- Emission: forbidden by default in these six base families. Functional routing signals belong to a separate explicitly functional material family.

## Application scales — provisional authoring density

These are authoring targets, not target-hardware memory budgets:

- hero insert: `1024 px/m`;
- prop / machine: `512 px/m`;
- architectural: `256 px/m`.

## Combinatorial contract

Axes: family × state × finish × application scale. Five physically/semantically contradictory combinations are filtered instead of counted as variation.

Current compiler target: **139 valid combinations**, with at least 20 valid combinations per family.

## Calibration scene

A standalone Material Lab must contain:

- all 6 families;
- 4 representative causal states per family = 24 material cells;
- flat/grazing-response geometry plus curved/beveled response geometry;
- deterministic portable textures;
- motivated neutral key/fill lighting;
- stable IDs and metadata;
- renderable overview for material-legibility QA.

Calibration texture resolution is deliberately low; it proves material behavior, packing and causality, not final authored resolution.

## Definition of Done — family/system stage

A family is not promoted until it has:

- stable asset ID and variant/state IDs;
- declared semantic role;
- explicit physical/manufacturing interpretation;
- deterministic source generation or authored source provenance;
- UV0/test geometry validation;
- BaseColor + MR + Normal channels;
- state/cause metadata and mask evidence where applicable;
- packed/embedded or otherwise self-contained export evidence;
- no missing/external texture dependency in the accepted package;
- Blender visual calibration;
- GLB parse/readback;
- Godot native material/readback;
- deterministic cold rebuild fingerprint;
- receipt and handoff;
- human art gate before `FINAL`/AAAA promotion.

## Forbidden drift

- random grunge;
- uniform scratches;
- global edge wear;
- decorative complexity without material cause;
- generic cyberpunk neon;
- Egyptian iconography shortcut;
- unmotivated emissive response;
- decorative mirror without optical role;
- baked lighting in BaseColor;
- atmosphere-driven oxidation/weathering without canon.

## Nonclaims

This contract does not establish final Glass Sea medium/physics, final architecture, geology, target-hardware texture budgets, atmospheric chemistry, human art approval or cross-world shared-material ownership.
