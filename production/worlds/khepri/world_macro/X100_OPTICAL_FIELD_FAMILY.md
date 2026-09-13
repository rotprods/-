# KHEPRI X100 — Optical Field System Family

Status: **SYSTEMIC_MACRO_COMPLETE**  
Family asset: `KHP_WM_HELIOSTAT_FOOTPRINTS`  
Owner: `AGENT-KHEPRI-WMACRO-001`  
Claim: `CLM-KHEPRI-WMACRO-001`  
Contracts: `KHP_OPTICAL_FIELD_X100_V1` + `KHP_OPTICAL_LOD_X100_V1`

## Purpose
Replace the original single fixed 8×4 macro proxy field with a deterministic systemic family that can generate many credible optical-field configurations while preserving route clearance, maintenance access, terrain contact, instancing and explicit epistemic boundaries.

This family is **macro infrastructure support**, not final Glass Sea architecture and not close-range final heliostat production art.

## Combinatorial grammar
Implemented axes:

- Layout: staggered bands / aligned lattice / diagonal bands / radial fan.
- Density: sparse / production / dense.
- Maintenance corridors: dual north-south / single north-south / cross.
- State profiles: operational / maintenance cycle / damage proxy / abandonment proxy.
- Scale mix: balanced / compact bias / standard bias.

`4 × 3 × 3 × 4 × 3 = 432` implemented configurations.

A cold pure-Python contract audit iterated the full configuration space. All configurations are non-empty and generate between `44` and `185` accepted placements after physical filters.

## Placement causality
Every candidate placement is filtered by:

- terrain model `KHP_TERRAIN_V1`;
- route clearance ≥ 140 m;
- route-anchor clearance ≥ 220 m;
- tile margin 350 m;
- slope ≤ 14°;
- deterministic maintenance corridor exclusion;
- deterministic spatial ordering for stable IDs.

Default representative configuration:

- layout: `staggered_bands`;
- density: `production`;
- corridor: `dual_ns`;
- state profile: `maintenance_cycle`;
- scale mix: `balanced`;
- accepted instances: `107`.

Measured default gates:

- min route clearance ≈ 144.714 m;
- min anchor clearance ≈ 269.916 m;
- min pair spacing ≈ 438.462 m;
- max terrain slope ≈ 10.794°;
- mast/terrain contact error ≈ −7.13…+8.61 μm.

## Structural scale family
Three LOD0 structural variants:

### Compact
- mast height 28 m;
- panel 28 × 17 × 1.6 m.

### Standard
- mast height 36 m;
- panel 36 × 22 × 2.0 m.

### Wide
- mast height 44 m;
- panel 46 × 26 × 2.2 m.

Each panel assembly includes a macro back-spine and hub, preventing the footprint from reading purely as a floating slab.

## State causality
No random scratches, random grunge or arbitrary noise is used to express state.

- `operational`: panel at normal tracking-proxy attitude.
- `maintenance`: panel stowed near vertical at 72°.
- `damaged_proxy`: panel lowered 3 m and rotated off-axis.
- `abandoned_proxy`: mast remains; panel is absent.

Damage and abandonment modes are production/system QA proposals, not canonical historical events.

Machine-readable state QA is authoritative and passes. AI image review is only supplementary legibility evidence.

## LOD source set
For compact / standard / wide × mast / panel:

| Level | Vertices | Polygons | Purpose |
|---|---:|---:|---|
| LOD0 | 24 | 18 | Representative macro authored mesh |
| LOD1 | 16 | 12 | Reduced structural silhouette |
| LOD2 | 8 | 6 | Far silhouette proxy |

12 LOD1/LOD2 source meshes live as unused Blender mesh datablocks with `fake_user=true` and zero object users. This keeps editable LOD source truth in the `.blend` while avoiding geometric payload in the representative GLB.

Master/cold LOD fingerprint:
`1c67430d580cae109fa50dfab73e6747304e87b5b3c9bba99e65fa6fe4e80101`

Runtime distance thresholds and HLOD are deliberately downstream technical-art work; this claim does not invent target-hardware thresholds.

## Reproducibility
Master and independent cold project produce identical X100 semantic fingerprint:
`01420ed366a7f8443a084332036604c47324d50900ae2033ea4d42059440d1fa`

Current artifact sizes also match master/cold:

- BLEND: 2,198,165 B;
- GLB: 577,744 B.

## Runtime verification
Exact R8 GLB imported in `Godot 4.7.2.stable.official.ed1daf0bf`:

- 229 total nodes;
- 219 MeshInstance3D;
- 107 mast nodes;
- 107 panel nodes;
- 3 unique mast Mesh resources;
- 3 unique panel Mesh resources;
- 224 authored stable asset IDs;
- 0 duplicate asset IDs;
- terrain remains 4,941 vertices / 4,941 normals / 9,600 tris;
- X100 LOD contract metadata survives;
- configuration count `432` survives;
- LOD manifest metadata survives.

This proves resource sharing and metadata fidelity, not draw-call/GPU qualification.

## Density QA
AI visual density review of exact R8 overview, supplemental only:

- infrastructure read: YES;
- route legible: YES;
- controlled variation: YES;
- clutter fail: NO;
- obvious floating: NO;
- repetition risk: LOW;
- density gate: PASS.

Minor future recommendations: use occasional wider maintenance corridors in denser downstream districts and stronger route emphasis where gameplay routes cross high-density fields.

## Exact R8 delivery
- GLB SHA256: `c9c698734061e481b94347c88d7c076b19c60261c8402548fb8ca1079d7d3579`
- BLEND SHA256: `b2f3e2f8ff90f28a5485dc019efcfa5913def0dbbcfb5e39d883d3c469a25337`
- persistent GLB media ID: `1bed7b1f-0e0a-4cd3-b61b-a62f950b4ff5`
- persistent BLEND media ID: `0988f832-71ab-4c21-9c1e-ecbe3cd08bcb`
- `fleet_control.py delivery`: PASS, `candidate_recovered_with_native_receipt`.

Git `.gitattributes` marks `.blend`/`.glb` binary/LFS. Do not inject these exact binaries as ordinary Git blobs; corporate Git LFS archival remains a non-blocking storage-policy follow-up.

## Hardness / nonclaims
This family does **not** claim:

- final close-range heliostat architecture;
- final Glass Sea infrastructure;
- final PBR/UV/material history;
- production collision;
- optical physics solution;
- runtime LOD thresholds / HLOD;
- target-hardware performance;
- human art approval;
- complete KHEPRI or AAAA completion.

The family is complete only at the declared systemic macro-support layer.
