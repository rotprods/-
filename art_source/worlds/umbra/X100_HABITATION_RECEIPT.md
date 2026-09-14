# UMBRA X100 — HABITATION / CULTURE / INTERIOR RECEIPT

Claim: `CLM-W04-WORLD-UMBRA-001`  
Owner: `AGENT-UMBRA-04`  
Primary project: `7ab99682-8777-4143-8ae0-1fbb178ccafb`  
Final checkpoint for this pass: `X100_HABITATION_ANNEX_QA_FIXED_001`  
Status: `SYSTEMIC FOUNDATION / NOT FAMILY_COMPLETE / NOT FINAL AAAA`

## Goal

Close one of UMBRA's largest non-blocked X100 holes: daily habitation and cultural identity at L3–L4.

This pass does **not** invent religion, social doctrine, narrative text, species, planet scale or runtime interaction logic. Cultural identity is expressed through survival fabrication and use:

- low-profile forms;
- glove-friendly latches and access;
- sealed/strapped storage;
- replaceable field repairs;
- tension fabric and dark metal;
- ivory repair hierarchy;
- amber refuge/service cues;
- thermal copper where heat transfer is functional;
- non-text physical bar/notch identity marks.

## Systemic library

Ten semantic families were authored:

1. `SLEEP_POD` — insulated low-profile rest module.
2. `RATION_LOCKER` — sealed ration/dry consumables storage.
3. `MESS_TRAY` — washable heated communal eating surface.
4. `HEATED_BENCH` — communal heated seat + under-seat storage.
5. `DRYING_RACK` — glove/boot/textile drying and warming frame.
6. `PERSONAL_LOCKER` — personal-effects storage with glove latch.
7. `MED_CABINET` — field medical storage; contents intentionally unspecified.
8. `PRIVACY_SCREEN` — tension-fabric privacy/thermal partition.
9. `CREW_ID_PLATE` — non-text caravan/crew identity plate.
10. `THERMAL_VESSEL_RACK` — secured insulated food/drink vessel rack.

Each family has:

- `S / M / L` capacity variants;
- `SERVICED / LIVED_IN / FIELD_REPAIRED` causal states;
- stable IDs;
- semantic purpose;
- culture DNA metadata;
- placement rules;
- gameplay/story tags;
- provisional LOD/collision strategy.

Library total: **90 prefab roots**.

Every library root was terrain-contact audited after construction:

- roots checked: `90`;
- contact range: `+0.03 m … +0.03 m`;
- failures beyond ±0.06 m: `0`.

State variation is causal rather than random:

- `SERVICED`: intact/service-tagged condition;
- `LIVED_IN`: repeated-handling/occupancy strap evidence;
- `FIELD_REPAIRED`: local repair plate + clamp.

## QA defect discovered at r14

The first site composition placed twelve habitation modules inside the footprint of `ARCH_REFUGE_HUB_BASE`.

A dedicated QA query proved that the hub base is still a **closed blockout solid**:

- vertices: `8`;
- edges: `12`;
- polygons: `6`;
- closed manifold by edge-use: `true`;
- dimensions: `44 × 30 × 12 m`.

Therefore the apparent interior layout would have been hidden inside a solid cube. This was treated as a real production defect, not accepted because the placement metrics happened to pass.

The invalid site composition was not promoted as final.

## QA correction — visible leeward habitation annex

`fix_x100_habitation_annex.py` relocates the twelve domestic roots to a visible leeward annex south of the refuge blockout and reuses the existing X100 architectural kit for its structure.

Domestic roots integrated: **12**.

Architectural roots integrated: **20**:

- six `GANTRY_FRAME / L / FIELD_MODIFIED` bays;
- six `ACCESS_CANOPY / L / WIND_SHIELDED` bays;
- six `HANDRAIL / L / WIND_SHIELDED` edge modules;
- two `PLATFORM / L / STANDARD` entry decks connecting toward the refuge edge.

The annex intentionally reserves a central access corridor (`x≈68…76`, `y≈5…20`) rather than filling all available space.

Final r15 objective receipt:

- total scene objects: **4,871**;
- mesh objects: **4,329**;
- materials: **13**;
- habitation library roots: **90**;
- visible habitation roots: **12**;
- annex structural roots: **20**;
- annex collection objects: **291**;
- residual non-unit object scales: **0**;
- zero-dimension meshes: **0**;
- annex root contact range: `+0.03 m … +0.03 m`;
- annex contact gate: **PASS**;
- refuge closed-base south edge: `y=20 m`;
- habitation roots occupy `y=7…16 m`, physically outside the closed base.

Artifact sizes at r15:

- editable `.blend`: `15,793,297 B`;
- portable GLB: `4,566,312 B`.

## Visual review status

A 960×540 Eevee review render was generated from a temporary camera as artifact `21c57b605bb5715b889c8394f4214cc9`.

The initial review camera was too tight to contain both extreme canopy bays; this is a **review-camera framing issue**, not a geometry/contact failure. The current session could retrieve the artifact metadata but could not independently inspect/download its pixels through the available binary transport, therefore:

`DIRECT_PIXEL_ART_REVIEW = REVIEW_NOT_CLAIMED`

No visual PASS is fabricated.

## Reproduction source

- `generate_x100_habitation_culture.py`
- `fix_x100_habitation_annex.py`

The two-step source preserves the defect chronology and correction instead of erasing evidence that the original refuge base is still blockout-solid.

## Still open before FAMILY_COMPLETE

- final UV0 / texel density / calibrated PBR;
- explicit collision proxies in runtime;
- LOD1/LOD2 and optional HLOD under target budgets;
- engine import and performance receipt;
- direct visual/human art approval;
- accessible low-light/readability review;
- additional habitation compositions in caravans / future valid interiors;
- provider-independent binary custody under MR-EXO-001.
