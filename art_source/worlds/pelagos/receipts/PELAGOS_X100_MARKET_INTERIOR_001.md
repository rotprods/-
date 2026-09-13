# PELAGOS X100 — Mercado Interior / Service Listening Cell 001

Claim: `PEL/MKT/ARCH-X100-002`
Protocol: `/EXOVANT-X100`
3D scene project: `39930c08-62bb-4034-b35d-70d0ce51c9d9`
Final structurally verified Blender revision: **34**
Status: **INTERIOR_SYSTEMIC_FOUNDATION_V1 / STRUCTURAL_PASS / VISUAL_ARTIFACT_GENERATED / GATE-ART_PENDING**

## Why this wave existed
After the civilization-prop wave, X100 reranking at rev. 32 found `interior_like_objects = 0` and settlement machinery = 0. L3 interior architecture was therefore the largest near-zero multiplicative dimension. The response was not another exterior hero object: it was a modular interior grammar installed inside the existing Mercado CommandShell.

## Placement
- Root asset: `PEL-MKT-INTERIOR-SVC-001`
- Center: `(-504, -90, 14.02)` m
- Visible envelope: ~`7.95 × 5.82 × 3.37 m`
- CommandShell envelope: `[-542,-96,14] → [-498,-64,32]`
- Final QA: interior is fully inside CommandShell within 5 cm tolerance.
- Existing bridge corridor clearance beyond each 3 m bridge bevel: **9.279–10.981 m**.
- Interface proximity: west service wall is ~1.23 m from `ServiceChannel_05` and ~0.50 m from `UtilityRiser` in the rev. 33 audit.

## Combinatorial grammar
Four wall slots × five panel types (`solid | service | acoustic | custody | open`) under functional constraints produce **280 valid wall layouts**. With three floor patterns × two ceiling patterns × four temporal states, the cell grammar can produce up to **6,720 credible configurations** before district placement variation.

This is a systemic kit, not 6,720 manually authored rooms.

## Current canonical assembly
- West: maintenance/service wall with quick-disconnect manifold ports and removable panel.
- North: acoustic/listening baffles with hydrophone receiver sockets.
- South: four memory-custody niches with wet-glove handles and custody-state seals.
- East: open threshold, parked sliding hatch and physical consent/timetable state carrier; no invented glyph language.
- Floor: removable/drained plates, longitudinal service grate and west drainage trench.
- Structure: bronze load-bearing posts/beams with lightweight replaceable overhead membrane.
- Integrated support: workbench/tool rail, wet-storage lockers and motivated amber task lights.

## History as geometry
Three physical eras are simultaneously present:
- `ERA_0_ORIGINAL`: frame, floor, drain and primary ceiling logic.
- `ERA_1_OCCUPATION`: service, acoustic, custody, threshold and work modules.
- `ERA_2_CURRENT`: localized replacement floor plate over repeated service access, visible fasteners, mismatched service-wall patch, drainage-edge biological fouling and repaired membrane strip.

No global/random grunge was used as a history substitute.

## Technical delivery foundation
Hidden technical shards exist for:
- `PEL-MKT-INTERIOR-SVC-001-COL`
- `PEL-MKT-INTERIOR-SVC-001-LOD1`
- `PEL-MKT-INTERIOR-SVC-001-HLOD`
- visibility/portal-culling candidate metadata.

These are Blender-side proposals. Runtime door animation, audio behavior, portal/room culling, HLOD thresholds, collision semantics and target-GPU qualification remain blocked by the unresolved production-engine gate.

## QA history
### Rev. 33 structural audit
`PELAGOS-X100-MARKET-INTERIOR-QA-STRUCT-R33` proved:
- fully inside CommandShell;
- >9.2 m bridge-corridor clearance beyond bridge thickness;
- UV/material/scale debt = 0;
- three eras present.

It also exposed a real layout defect: the workbench/tool rail crossed ~0.10 m into the reserved 0.9 m central corridor. That prevented PASS.

The same audit initially appeared to report a zero east-threshold collision gap because hidden technical objects returned stale `matrix_world` values at the origin.

### Hidden-transform control
`PELAGOS-X100-MKT-INT-HIDDEN-TRANSFORM-CONTROL-R33` demonstrated this was **not** a parenting defect:
- hidden `matrix_world` could remain stale at zero while `hide_viewport=True`;
- composed transform `parent.matrix_world @ matrix_parent_inverse @ matrix_basis` matched the correct world placement;
- temporarily unhiding + `view_layer.update()` produced the same correct matrices;
- actual east collision intervals were `[-92.775,-91.325]` and `[-88.675,-87.225]` m;
- actual collision-clear threshold gap = **2.65 m**.

Audit rule learned: do not classify hidden technical geometry as origin-drift from stale `matrix_world`; compose matrices manually or force depsgraph evaluation.

### Rev. 34 correction
`pelagos.x100.market-interior.corridor-fix.v1` shifted the workbench cluster, tool rail and corresponding task light **0.30 m west** without altering the architecture envelope, threshold or service interfaces.

Final `PELAGOS-X100-MARKET-INTERIOR-QA-STRUCT-R34`:
- inside CommandShell: PASS;
- bridge clearance: PASS;
- east collision threshold gap: **2.65 m**;
- reserved central corridor width: **0.90 m**, blockers: **0**;
- missing UV: 0;
- missing materials: 0;
- non-unit mesh scales: 0;
- visible technical shards: 0;
- era counts: 13 original / 53 occupation / 12 current visible objects;
- result: **STRUCTURAL PASS**.

## Visual evidence
Workbench artifacts generated at rev. 34:
- `qa_x100_market_interior_r34_cutaway.png` — 768×512
- `qa_x100_market_interior_r34_player.png` — 768×512
- includes a temporary 1.75 m human-scale proxy.

The artifact service returned valid files, but the current execution environment could not DNS-resolve the signed storage host for pixel inspection. Therefore this receipt records **VISUAL_ARTIFACT_GENERATED**, not a semantic GATE-ART PASS.

## DoD state
Pass now:
- semantic purpose / stable IDs;
- player-scale envelope and clearances;
- modular snap/configuration grammar;
- explicit 3-era history geometry;
- UV/materials/clean transforms;
- collision/LOD/HLOD Blender foundations;
- bridge/service-interface spatial validation;
- deterministic source generator;
- structural QA + receipt.

Still open before FAMILY_COMPLETE:
- semantic visual GATE-ART;
- production-engine import;
- runtime door/audio/interaction bindings;
- portal/HLOD qualification;
- target-GPU profiling;
- district-wide propagation of the cell grammar.

## Source
`art_source/worlds/pelagos/scripts/build_market_interior_x100_v1.py`
