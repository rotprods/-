# ELYSIUM NULL — ARCHITECTURE KIT SPEC v0.1

Cell: `ART-ELYSIUM-001`
Remote scene revision qualified structurally: `2`
Status: `PROPOSAL / W1 STRUCTURAL CANDIDATE`

This file defines a reversible architectural grammar. Nothing in this file overrides the project canon or runtime controller dimensions.

## 1. Design thesis

ELYSIUM architecture must express a system that has removed surprise from construction. Its buildings therefore use a legible, repeatable structural grammar, but the repetition is diegetic: standardization is part of the world's control system.

The kit must avoid two opposite failures:

1. **generic sci-fi panel soup** — arbitrary seams, vents and greeble with no construction logic;
2. **empty white boxes** — no readable scale, maintenance, access or service logic.

The solution is low-frequency massing + few high-information construction interfaces.

## 2. Proposed dimensional grammar

All values below are `PROPOSAL` until validated with the runtime player controller and target engine.

| Parameter | Candidate |
|---|---:|
| Planning grid | 1.0 m |
| Primary structural bay | 4.0 m |
| Standard clear door width | 2.4 m |
| Standard clear door height | 2.7 m |
| Column prototype | 0.4 × 0.4 × 4.0 m |
| Solid panel prototype | 4.0 × 4.0 × 0.24 m |
| Façade tile prototype | 3.8 × 3.6 × 0.24 m |
| Span family | 8 / 12 / 16 m |
| Service hatch | 1.2 m nominal |

The 4 m bay is intentionally large enough to avoid claustrophobic modular repetition and to allow a clean façade rhythm. The 3.8 m tile leaves a controlled reveal within that bay rather than forcing decorative seams onto every surface.

## 3. Module family

### Structural

- `ELYS-ARCH-MOD-COL-040-400`
- `ELYS-ARCH-MOD-BEAM-400`
- `ELYS-ARCH-MOD-SPAN-08M`
- `ELYS-ARCH-MOD-SPAN-12M`
- `ELYS-ARCH-MOD-SPAN-16M`

### Envelope

- `ELYS-ARCH-MOD-PANEL-SOLID-400`
- `ELYS-ARCH-MOD-PANEL-REVEAL-400`
- `ELYS-ARCH-MOD-FACADE-380x360`

### Access / service

- door shadow + jamb/header assembly, current proposal 2.4 × 2.7 m clear opening;
- 1.2 m service hatch family;
- continuous service-spine language;
- canopy/service-rib assembly.

## 4. Instancing contract

The representative arrival façades use a single shared façade mesh data-block.

Structural receipt at Blender revision 2:

- deployed arrival façade instances: 32;
- prototype + instances sharing the same mesh: 33 users;
- all 32 deployed façade objects verified to share the prototype mesh;
- no requirement to duplicate geometry merely to create object-level placement.

Future production should prefer:

1. linked mesh data for identical hard-surface modules;
2. Geometry Nodes / engine instancing for large repeated populations only after export compatibility is verified;
3. unique geometry only when silhouette, damage, interaction or causal human modification requires it.

## 5. Pivot / snapping proposal

For production modules:

- wall/panel pivot: lower-left grid corner when snapping is primary;
- structural columns: center at floor contact;
- beams/spans: centerline with a documented start/end socket convention;
- doors/hatches: floor-contact center for placement, with separate interaction/socket transforms in engine;
- canopies: structural attachment corner/centerline, not arbitrary object centroid.

The current W1 scene proves dimensions and mesh sharing but does **not** yet promote final pivots/snapping conventions. That remains part of `ELYS/W1/001` acceptance.

## 6. Construction realism

A white envelope is not a magical continuous surface. Production detail must eventually account for:

- panel substrate / casting or composite manufacturing hypothesis;
- attachment strategy to structural frame;
- expansion and tolerance gaps;
- water/condensation management where relevant;
- removable maintenance zones;
- door seals and threshold;
- service access;
- lighting/service integration;
- repair/replacement logic.

Seams should exist where construction requires them, not as texture decoration.

## 7. Material roles

Current blockout roles:

- `MAT_Elysium_WhiteCeramic_PROPOSAL` — dominant envelope;
- `MAT_Elysium_WhiteMineral_PROPOSAL` — ground/mass surfaces;
- `MAT_Elysium_SatinMetal_PROPOSAL` — structural/service members;
- `MAT_Elysium_Recess_PROPOSAL` — high-value depth/reveal;
- `MAT_Elysium_ServiceAmber_PROPOSAL` — rare service/anomaly cue.

These are lookdev placeholders, not calibrated PBR master materials.

## 8. Art-direction constraints

### Required

- broad clean planes;
- readable human access points;
- few purposeful shadow reveals;
- maintenance logic integrated into architecture;
- deliberate repetition;
- causal exceptions.

### Forbidden drift

- random vents;
- repeated tiny bevel panels;
- meaningless emissive strips;
- exposed pipe forests merely to create complexity;
- universal grunge;
- fake edge wear over actively maintained surfaces;
- dense signage used to compensate for weak form.

## 9. Runtime blockers before promotion

The following must be measured before W1 grid values become production standard:

- player capsule width/height;
- sprint/dodge clearance;
- combat weapon sweep envelopes;
- camera boom/near clipping;
- enemy pathing sizes;
- accessibility route minimums;
- collision margin behavior;
- engine unit/import scale.

Until then, the metadata root remains:

`player_clearance_validation = PENDING_RUNTIME_CONTROLLER`.

## 10. Next acceptance test

Build one small reception structure exclusively from candidate modules and prove:

1. no hidden bespoke filler is required;
2. door/corridor dimensions work with real player controller;
3. façade repetition reads as intentional ELYSIUM control rather than unfinished art;
4. shared mesh instances survive GLB and target-engine import;
5. close/mid/far silhouette remains legible;
6. material and draw-call cost is measured.

Only then promote the kit from `STRUCTURAL CANDIDATE` to `QUALIFIED MODULE KIT`.
