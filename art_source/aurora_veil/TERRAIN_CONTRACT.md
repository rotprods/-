# AURORA VEIL — MACRO TERRAIN RELIEF CONTRACT r14

**Task:** `AUR/TERRAIN/005`  
**Owner:** `AGENT-02-AURORA` / `CLM-AURORA-WORLD-001`  
**Remote proof:** Blender rev 14  
**Truth state:** `REVIEW_TECHNICAL`; morphology proposal only. Lithology, microdetail, erosion simulation and final gameplay traversal remain open.

## Why this pass exists

The initial 5.2 × 3.0 km macro mesh was a valid layout plane but was too flat to carry world identity: global slope P95 was ~1.09° and maximum ~1.56°. Rev14 introduces low-frequency relief while preserving canonical region anchors, temporal fields and the primary traversal corridor.

## Spatial contract

Local frame remains physical metre scale: `1 BU = 1 m`.

Terrain object:

- object: `AURORA_MACRO_TERRAIN`;
- source mesh: `AURORA_MACRO_TERRAIN_MESH`;
- grid: 81 × 49 vertices;
- spacing: ~65 m × 62.5 m;
- XY extent: 5,200 × 3,000 m;
- rev14 Z span: 53.610 m.

This is L2/L3 macro morphology, not hero sculpt density.

## Region morphology

### Campamento del Segundo Día

Purpose: give the observatory a credible elevated/readable landscape without turning the settlement into a mountain level.

Proposal:

- broad northern uplands;
- southern drainage depression;
- low longitudinal shelves;
- protected build/approach zone around the canonical Campamento anchor.

Measured rev14:

- Z span: 50.904 m;
- slope P50: 1.411°;
- slope P95: 4.052°;
- max: 5.627°.

### Llanura de las Repeticiones

Purpose: preserve visual timing comprehension and long sightlines while avoiding an artificial flat plane.

Proposal:

- low rolling prairie;
- no cliff grammar;
- temporal fields protected from relief displacement;
- major corridor remains low-slope.

Measured rev14:

- Z span: 45.877 m across the broad regional slice;
- slope P50: 0.972°;
- slope P95: 4.962°;
- max: 8.666° at transition zones, not hero anchors.

### Huerto de AEON

Purpose: form a subtle amphitheatre around the orchard while preserving the canonical 50 m arena and three-sector readability.

Proposal:

- broad amphitheatre approach around AEON;
- east ridge for skyline separation;
- protected bowl/arena center;
- no invented lithology.

Measured rev14:

- Z span: 38.436 m;
- slope P50: 0.901°;
- slope P95: 3.510°;
- max: 7.238°.

## Protected traversal contract

Primary protected polyline:

`Campamento (-1600,350) → Llanura (0,-50) → AEON (1650,250)`

Mask:

- 120 m core: no relief delta;
- transition to full relief over next 300 m;
- additional local protection around Campamento, AEON and each temporal field.

This protects layout continuity before a final nav/traversal system exists. It is not a claim that the eventual production road/path is exactly this width.

## Anchor/contact QA

Rev14 exact terrain raycasts:

- Campamento anchor offset: +0.0158 m;
- Llanura anchor offset: +0.0036 m;
- Huerto anchor offset: −0.1085 m;
- AEON arena floor: +0.5915 m above terrain;
- temporal field A/B/C idle rings: exactly +0.28 m above local terrain.

The temporal contact correction is part of rev14 because the r12 fields were authored with a fixed Z before exact ground-query QA.

## Rollback contract

Do **not** rely on an unused duplicate mesh datablock: Blender checkpointing can purge unreferenced data and such a backup would create false safety.

Rollback is deterministic:

- versioned relief function lives in `blender/aurora_terrain_relief_r14.py`;
- applying with sign `+1` adds the relief to the r12 base;
- applying with sign `-1` removes the same deterministic relief from a matching r14 terrain;
- contact correction for temporal fields is recomputed from the terrain surface after the operation.

No rollback claim is made if the relief formula/version or base mesh topology changes.

## Export cleanliness

The first r13 attempt created a visible curve as a QA corridor. glTF export logs showed that `hide_render=True` does not guarantee omission from portable export. Rev14 removes all geometric QA guides from `21_TERRAIN_QA`; only EMPTY metadata markers remain.

Rev14 glTF log contains no `AUR_TERRAIN_QA_PROTECTED_CORRIDOR` extraction.

## Epistemic limits

NOT claimed:

- lithology/mineral composition;
- tectonic truth;
- erosion chronology;
- final biome mask;
- final collision/navmesh;
- micro/mid-frequency sculpt;
- final material blend;
- gameplay-certified traversal;
- human art approval.

These remain future gates. The current pass is an engine-neutral, reversible macro morphology candidate.
