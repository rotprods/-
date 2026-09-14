# UMBRA X100 — MATERIAL HISTORY / CAUSALITY RECEIPT

Claim: `CLM-W04-WORLD-UMBRA-001`  
Owner: `AGENT-UMBRA-04`  
Global opportunity: `UMBRA-X100-SYSTEMIC-DENSITY`  
Global Director dimension: `material_causality`  
Primary project: `7ab99682-8777-4143-8ae0-1fbb178ccafb`  
Checkpoint: `X100_MATERIAL_CAUSALITY_FOUNDATION_001`  
Primary revision: **16**

## Why this pass exists

The EXOVANT X100 Global Density Director ranks UMBRA among the highest-value current portfolio opportunities and identifies `material_causality` as the dominant gradient. This pass therefore expands material history on already site-integrated civilization assets instead of adding indiscriminate geometry or inventing blocked ecology.

This is a **portable material-causality foundation, not final PBR**.

Directional wear masks, authored UV0, texture sets, texel density, calibrated roughness/normal response and target-engine budgets remain blocked until runtime/target evidence exists.

## Base material roles

Six existing functional/civilization material roles are expanded:

1. `MAT_SINSOL_DARK_METAL` → `METAL`
2. `MAT_SINSOL_TENSION_FABRIC` → `FABRIC`
3. `MAT_COLONIAL_IVORY_REPAIR` → `IVORY_REPAIR`
4. `MAT_SINSOL_THERMAL_COPPER` → `THERMAL_COPPER`
5. `MAT_SINSOL_GASKET` → `GASKET`
6. `MAT_SINSOL_THERMAL_CERAMIC` → `THERMAL_CERAMIC`

## Causal state set

Every role receives four controlled whole-object response variants:

### `COLD_ABRADED`

Cause: windborne ice/dust exposure.

Foundation response:
- slightly lighter/polished whole-object response;
- modest roughness reduction.

This is a coarse portable proxy. Final directional abrasion belongs in a later UV/mask stage.

### `THERMAL_CYCLED`

Cause: repeated cold/heat service cycles.

Foundation response:
- darker response;
- increased roughness;
- slightly reduced metallic response where applicable.

### `SERVICE_RENEWED`

Cause: recent cleaning, replacement or service.

Foundation response:
- slightly tighter/cleaner response;
- reduced roughness without becoming plastic.

### `FIELD_REPAIRED`

Cause: scarcity-driven local replacement and mismatched repair.

Foundation response:
- slightly lighter mismatch;
- increased roughness.

No random scratch/grunge layer is introduced.

## Semantic assignment rules

Material states are not random. They are derived from already-authored root metadata:

- habitation `SERVICED` → `SERVICE_RENEWED`;
- habitation `LIVED_IN` → `THERMAL_CYCLED`;
- habitation `FIELD_REPAIRED` → `FIELD_REPAIRED`;
- site-history `ERA_0` → `COLD_ABRADED`;
- site-history `ERA_1` → `FIELD_REPAIRED`;
- site-history `ERA_2` → `SERVICE_RENEWED` when the root explicitly describes repair/renewal/patch, otherwise `THERMAL_CYCLED`.

Catalog/library assets remain neutral. The pass is bounded to site-integrated X100 collections so the source library remains a clean recombination surface.

Object-level material-slot overrides are used, preserving shared mesh datablocks.

## r16 technical receipt

Mutation result:

- material-history variants created: **24**;
- site-integrated material-slot assignments: **485**;
- total scene objects: **4,871**;
- mesh objects: **4,329**;
- mesh datablocks: **788**;
- total materials after pass: **37**;
- shared mesh datablocks: **608**;
- residual non-unit object scales: **0**;
- zero-dimension meshes: **0**.

Assignments by causal state:

- `COLD_ABRADED`: **61**;
- `THERMAL_CYCLED`: **84**;
- `SERVICE_RENEWED`: **58**;
- `FIELD_REPAIRED`: **282**.

Assignments by material role:

- `METAL`: **219**;
- `FABRIC`: **38**;
- `IVORY_REPAIR`: **191**;
- `THERMAL_COPPER`: **11**;
- `GASKET`: **18**;
- `THERMAL_CERAMIC`: **8**.

r16 artifacts:

- editable `.blend`: **16,468,932 B**, provider etag `95b4818e0a8858e2ac37c4794bdc177a`;
- portable GLB: **4,649,568 B**, provider etag `140b38ad798295ba71f2bfa75e61ad1c`.

## Hardness / anti-slop contract

This pass explicitly avoids:

- blanket grunge;
- random scratches;
- uniform edge wear;
- arbitrary color variation;
- decorative dirt detached from process/history.

The four states correspond to explicit environmental, service or scarcity causes. Final localized/directional material history must later be expressed through UV/masks or equivalent runtime-qualified systems.

## Reproduction source

`art_source/worlds/umbra/apply_x100_material_history.py`

## Open gates before MATERIAL FAMILY_COMPLETE

- authored UV0 and texel-density policy;
- directional/functional wear masks;
- calibrated final texture sets;
- engine import/material transport readback;
- target-GPU material budget;
- LOD/HLOD interaction where material simplification is relevant;
- direct pixel/human art acceptance;
- independent X100 batch replay;
- exact post-batch MANIFEST + bounded manual Gauntlet;
- provider-independent binary custody under MR-EXO-001.
