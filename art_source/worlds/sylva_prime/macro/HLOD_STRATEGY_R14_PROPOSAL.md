# SYLVA PRIME — HLOD Strategy R14 Proposal

Claim: `CLM-SYLVA-MACRO-001`  
Source scene: accepted R13  
Status: `PROPOSAL / READ_ONLY / NOT EXECUTED`  
Writer fence: `FROZEN_PENDING_FLEET_ACTIVE`

## Decision

Do **not** generate one uniformly decimated terrain/HLOD recipe for all 16 L3 tiles.

R13 proves that terrain complexity is strongly non-uniform. The correct architecture is:

1. **L3 base terrain tiles** — authoritative streamed terrain partition (`SYLVA_TERRAIN_STREAM_R12`).
2. **L4 hero-core overlays** — small, measured regions around Puerto, Bosque and VESPER; they do not turn an entire 3 km L3 cell into hero density.
3. **L4 corridor overlays** — preserve traversal silhouettes / root-route relationships independent of base terrain simplification.
4. **L2 supercell metadata** — 4 × 6 km groups for residency/prefetch/HLOD orchestration, not duplicated source geometry.
5. **Feature-aware HLOD generation** — preserve critical extrema/ridges/corridors; never rely on a global percentage-decimate rule.

No switching distance, screen-space error threshold, triangle budget or renderer backend is approved until target engine/hardware qualification.

## Why uniform decimation is rejected

Read-only R13 study: `qa/R14_HLOD_GEOMETRIC_ERROR_MATRIX.json`.

Source per L3 tile:
- 13×13 vertices;
- 250 m grid;
- 144 quads / 288 rendered triangles equivalent per tile before export triangulation.

A hypothetical 500 m uniform grid reduces each tile to 7×7 / 72 triangles, but error varies radically:

| Tile | Relief | 500 m p95 error | 500 m max error | Interpretation |
|---|---:|---:|---:|---|
| X1Y0 | 324.8 m | 7.5 m | 38.6 m | comparatively stable |
| X2Y3 | 173.5 m | 6.9 m | 41.2 m | comparatively stable |
| X0Y1 | 426.8 m | 33.1 m | 178.4 m | local feature loss risk |
| X1Y1 | 508.8 m | **122.1 m** | **310.8 m** | feature-critical |
| X2Y2 | 741.9 m | **100.5 m** | **270.7 m** | feature-critical |
| X3Y2 | 590.0 m | 46.6 m | 195.6 m | feature-sensitive |

At 750–1500 m spacing the error becomes worse in many of the same tiles. A global reduction ratio would therefore allocate quality by convenience rather than perceptual/geometric need.

## Measured hero-core overlays

Hero core is distinct from regional prefetch envelope.

Measured visible macro-geometry XY extent + 50 m safety, rounded to 25 m:

- **Puerto**: 550 m proposal.
- **Bosque**: 200 m proposal, explicitly excluding its long route geometry.
- **VESPER**: 400 m proposal.

Existing regional envelopes (Puerto 1200 m, Bosque 1700 m, VESPER 1200 m) remain useful as broad residency/prefetch envelopes; they must not be interpreted as “maximum geometry density everywhere in this radius.”

R14 hero overlay mapping is verified read-only in `qa/R14_STREAM_HIERARCHY_READONLY_QA.json`.

## Bosque special case

Bosque is intentionally located close to the L2 four-way boundary.

Its 200 m hero core overlaps four L3 cells and all four proposed L2 supercells. This is not a reason to move the world landmark.

Rule:

> Preserve Bosque geography. Solve the streaming architecture with an explicit hero residency group / prefetch overlay.

Moving Bosque to simplify world partition would optimize the implementation at the expense of world composition.

## L2 proposal

`STREAM_HIERARCHY_R14_PROPOSAL.json` defines four 6 km supercells:

- `L2_X0Y0` → X0Y0/X0Y1/X1Y0/X1Y1
- `L2_X0Y1` → X0Y2/X0Y3/X1Y2/X1Y3
- `L2_X1Y0` → X2Y0/X2Y1/X3Y0/X3Y1
- `L2_X1Y1` → X2Y2/X2Y3/X3Y2/X3Y3

Read-only QA passes:
- all 16 L3 cells covered exactly once;
- 4-neighbor and 8-neighbor graphs symmetric;
- L2 object/membership-slot counts match the proposal;
- 19 objects cross L2 boundaries;
- six expected objects cross all four L2 groups.

Do not duplicate those large roots/routes per L2. Residency references the same authored asset.

## Proposed HLOD asset IDs

Contract-only IDs, no meshes generated yet:

- `SYLVA_HLOD_L2_X0Y0`
- `SYLVA_HLOD_L2_X0Y1`
- `SYLVA_HLOD_L2_X1Y0`
- `SYLVA_HLOD_L2_X1Y1`

Generation remains `BLOCKED_TARGET_BACKEND_PENDING`.

## Feature retention contract for future HLOD builder

Any future HLOD candidate must preserve, before art approval:

### Terrain
- L3 external tile boundary positions exactly or through compatible crack-free stitching/skirt policy;
- dominant horizon/silhouette extrema;
- VESPER depression silhouette;
- major root-bearing ridge lines;
- Puerto/Bosque/VESPER hero-core terrain support;
- corridor support surfaces where visible in the distance.

### Macro structures
- primary root skyline and load-bearing silhouette;
- VESPER city-root tower cluster / terrace silhouette when visible;
- Puerto living-arch silhouette;
- Bosque Phrase landmark silhouette;
- no duplication of PR #6 provider-module geometry.

### Streaming
- one authoritative source asset, not copies per L2;
- preserve R13 membership provenance;
- HLOD is a representation, not a second gameplay/collision source.

### Collision
HLOD carries **no gameplay collision** unless a future engine-specific ADR explicitly requires it. Current `SYLVA_COL_*` remains the gameplay collision interface.

## Qualification gauntlet before HLOD promotion

A generated HLOD is not accepted until:

1. exact source revision/asset set recorded;
2. crack/seam test across neighboring L2/L3 representations;
3. world-space geometric deviation measured;
4. screen-space silhouette deviation measured at declared cameras/distances;
5. hero/corridor overlays tested independently from base HLOD;
6. transition popping / dither / crossfade evaluated in the target renderer;
7. draw calls, triangles, VRAM and shader cost measured on declared hardware/preset;
8. occlusion/residency behavior measured during real controller traversal;
9. collision remains authoritative and unaffected;
10. human art review approves vista/landmark readability.

## Current stop condition

Do not execute `build_stream_hierarchy_r14.py` or create HLOD meshes while:
- fleet claim is `reserved / ack:null`;
- `REMOTE_WRITER_FENCE.json` is frozen;
- target renderer/hardware remains unresolved.

The next valid execution state is: fleet `active` + one nominated writer + fresh R13/R14 readback.
