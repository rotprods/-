# SYLVA PRIME Macro — Engine Import Contract R16

Claim: `CLM-SYLVA-MACRO-001`  
Primary Blender: `05dce898-753d-4ff6-a4b0-31757dc868d8` @ **revision 17 / sceneSequence 0**  
Art wave: **R16**, with revision17 metadata reconciliation  
State: `VERIFIED TECHNICAL-ART CHECKPOINT / NOT FINAL ART`

## 1. Coordinate / source contract

- `1 Blender Unit = 1 metre`.
- Local authored patch = `12,000 × 12,000 m`, PROPOSAL; never infer planetary radius from it.
- Blender source is Z-up; perform the engine/glTF axis conversion once.
- Accepted R16 MESH/CURVE geometry fingerprint:
  `747a5b10c7344d5e4b0623354927e98faab8df6f44fced81c5f042350f079a89`.
- Revision16 and revision17 share the same fingerprint; revision17 changed stream metadata only.

## 2. R12 terrain partition

Morphology: `R6_BIOGEO_CAUSAL_MACRO_V1`.  
Contract: `SYLVA_TERRAIN_STREAM_R12`.

Required render terrain:
- 16 × `SYLVA_TERRAIN_L3_X#Y#`;
- each 3 km × 3 km;
- 13×13 vertices @250 m;
- aggregate 2,704 verts / 2,304 faces;
- 285 seam samples, max/mean Δz **0 m**.

Required collision terrain:
- 16 × `SYLVA_COL_TERRAIN_L3_X#Y#`;
- 9×9 @375 m;
- aggregate 1,296 verts / 1,024 faces;
- 189 seam samples, max/mean Δz **0 m**;
- policy `CUSTOM_LOWRES_HEIGHTFIELD_TILE`.

Forbidden legacy nodes:
- `SYLVA_TERRAIN_Macro12km_PROPOSAL`;
- `SYLVA_COL_TERRAIN_Macro12km_LowRes_PROPOSAL`.

## 3. Spatial membership — R13 base + R16 amendment

Base metadata: `SYLVA_META_StreamMembershipR13`.  
Base contract: `SYLVA_STREAM_MEMBERSHIP_R13`.

R13 checkpoint:
- 147 owned spatial objects assigned;
- 0 outside patch;
- 34 cross-cell objects;
- max 6 cells/object;
- terrain tiles use authoritative single-cell ownership;
- large roots/routes may carry multi-cell bounds membership.

R16 amendment contract: `SYLVA_STREAM_MEMBERSHIP_R16_AMENDMENT`.

R16 taper enlarged only R01 enough to cross an additional L3 boundary. Required R01 membership is now:
`X0Y0 | X0Y1 | X0Y2 | X1Y0 | X1Y1 | X1Y2`.

The old R01 set `X0Y0|X0Y1|X1Y0|X1Y1` is stale and must not be reconstructed by an importer/tool.

Final R16 bounds audit: **0 stale primary-root memberships**.

## 4. R14 L2/L3 hierarchy

Metadata: `SYLVA_META_StreamHierarchyR14`.  
Contract: `SYLVA_STREAM_HIERARCHY_R14`.

Required L2:
- `SYLVA_STREAM_L2_X0Y0`
- `SYLVA_STREAM_L2_X0Y1`
- `SYLVA_STREAM_L2_X1Y0`
- `SYLVA_STREAM_L2_X1Y1`

Each L2 covers four existing L3 cells. L2 is grouping/coverage/HLOD orchestration metadata; never duplicate source geometry per L2.

Hero residency remains L3-only:
- Puerto: X0Y1/X1Y1;
- Bosque: X1Y1/X1Y2/X2Y1/X2Y2;
- VESPER: X2Y2/X3Y2.

Bosque L2 coverage across all four supercells **does not imply full L2 residency**. Do not move Bosque to simplify streaming.

## 5. R15 prefetch experiment

Contract: `SYLVA_PREFETCH_POLICY_R15`.

State: `RUNTIME_EXPERIMENT_REQUIRED`; production approved=false.

Candidates:
- P0 current-only;
- P1 current + four cardinal neighbors;
- P2 current + eight neighbors;
- P3 directional previous/current/next route window plus one contextual approaching/current hero overlay.

R16 membership recalculation conservative upper bounds by current object-cardinality:
- current-only: 31.97%;
- +4: 62.59%;
- +8: **72.79%**;
- directional route-window: **59.18%**.

P3 remains runtime candidate only. Do not activate every overlapping hero group merely because their cell sets overlap; hero activation is contextual/route-phase driven.

Selection rule: promote the least-resident policy that passes measured loading latency, collision readiness, visual pop, reversal/re-entry and traversal gates.

## 6. R16 macro-root biomechanical silhouette

Contract: `SYLVA_MACRO_ROOT_TAPER_R16`.

Required primary roots: `SYLVA_ROOT_PRIMARY_R01..R06`.

**Centerline coordinates/endpoints are locked to R15.** R16 changes only Bezier point radius multipliers:

| Root | Radius multipliers | Effective radius range | Load anchor |
|---|---|---:|---|
| R01 | 0.75 / 0.95 / 1.32 / 1.05 / 0.82 | 36.00–63.36 m | Puerto p2 |
| R02 | 0.72 / 0.92 / 1.30 / 1.02 / 0.78 | 44.64–80.60 m | Bosque p2 |
| R03 | 0.70 / 0.90 / 1.34 / 1.04 / 0.80 | 50.40–96.48 m | VESPER p2 |
| R04 | 0.78 / 0.92 / 1.18 / 1.08 / 0.82 | 28.08–42.48 m | network midspan |
| R05 | 0.75 / 0.92 / 1.20 / 1.10 / 0.82 | 22.50–36.00 m | network midspan |
| R06 | 0.70 / 0.82 / 0.94 / 1.08 / 1.28 | 28.00–51.20 m | VESPER approach p4 |

Importer/art-tool invariants:
- do not reset root point radii to 1.0;
- do not move centerlines to “fit” the new taper;
- preserve current stream membership, including R01 amendment;
- R16 still uses circular curve cross sections and **does not claim final buttress/fiber anatomy**.

Future non-circular/buttress refinement requires human visual review or a controlled isolated experiment before production promotion.

## 7. Navigation R10

Contract: `SYLVA_NAV_R10`; profile `BALANCED_FOOT_TERRAIN_AWARE_R10`.

- 00: 1,963.093 m / max 18.490°;
- 01: 2,382.483 m / max 15.131°;
- 02: 2,188.103 m / max 7.285°;
- 03: 2,364.615 m / max 20.530°;
- total 8,898.294 m.

Collision nodes `SYLVA_COL_ROUTE_00..03` remain closed manifold with 0 degenerate faces at R16 acceptance. Historical r9 is forbidden.

## 8. Streaming seam probes

Approximate route-transition probes from authored centerlines:
- S-00 X0Y1→X1Y1: `(-3000,-2000,345.8)`;
- S-01 X1Y1→X1Y2: `(-500,0,356.1)`;
- S-02 X1Y2→X2Y2: `(0,250,352.2)`;
- S-03 X2Y2→X3Y2: `(3000,2000,-72.4)`.

Use as repeatable transition probes, not centimeter-exact gameplay markers.

## 9. VESPER macro arena

Required visible:
- `SYLVA_VESPER_Terrace_00_ENTRY`
- `SYLVA_VESPER_Terrace_01_MIDDLE`
- `SYLVA_VESPER_Terrace_02_UPPER`
- `SYLVA_VESPER_TerraceConnector_00`
- `SYLVA_VESPER_TerraceConnector_01`
- `SYLVA_META_VESPER_ThreeTerraceLayout`

Required collision: three terrace + two connector `SYLVA_COL_VESPER_*` proxies.

Layout dimensions remain 116/124/112 m terrace diameters and 142.215/145.685 m connectors. Final VESPER asset remains outside this claim.

## 10. Root-kit provider consumer boundary

Consumer metadata: `SYLVA_META_RootKitSocketConsumerContract`.  
Consumer: `SYLVA_SOCKET_CONSUMER_V1`; support map `SYLVA_SOCKET_SUPPORT_MAP_V1`.

Basis: +X forward, +Z up, metres, scale 1.

Provider PR #6 / `CLM-SYLVA-PROC-NROOT-001` remains **NOT_READY** despite CI Gauntlet success at HEAD `5ba1ea6758e4c08ed82d95deb96f1bbcae1581f5`:
- provider manifest YAML shape still invalid around `materials`/`note`;
- no normalized per-asset pivot/anchor transforms;
- render/collision anchor parity unproven;
- no pivot-policy version.

Importer rule: **instantiate zero provider modules** until these gates pass and provider is re-audited read-only. Current macro source has zero provider meshes.

## 11. Collision namespace

Expected macro `SYLVA_COL_*` count remains 27:
- terrain 16;
- Puerto 1;
- Bosque 1;
- routes 4;
- VESPER 5.

R16 adds no primary-root gameplay collision. HLOD never substitutes gameplay collision unless a future engine ADR explicitly says otherwise.

## 12. Delivery validation

Remote revision17 identity:
- `.blend` 2,856,650 B / etag `5fb0cc50f5e21cb8cc0effd556e35c83`;
- GLB 1,220,616 B / etag `c7d3b8775c0519470d3ccc34bb392f3e`.

Remote size/etag is not delivery PASS.

Required delivery chain when artifact bytes are available:
1. recover exact revision17 `.blend` + GLB;
2. bind SHA-256;
3. run shared `fleet_control.py delivery` with explicit evidence paths;
4. run claim-local GLB semantic validator against the same GLB SHA;
5. verify R12/R13/R16 membership, R14 hierarchy and R15 policy metadata preservation or explicit adapter conversion;
6. import exact artifact into qualified engine;
7. execute S-00..S-03 and full route/VESPER traversal;
8. compare P0/P1/P2/P3 with load-to-ready latency, resident set/memory, frame spikes, pop/reversal and collision readiness;
9. keep PR #6 instances disabled;
10. profile only on declared target hardware/preset;
11. require human art review independently.

Current `validate_glb_contract_r13.py` remains the last byte-level claim validator baseline for streamed terrain/route topology. A future R16 validator should add exported root-silhouette/bounds assertions after exact GLB recovery demonstrates how Blender curve taper is represented in exported meshes.

## 13. R16 visual evidence

Three regional file-backed Eevee renders @256×144 are nonblank. Receipt: `qa/R16_REGIONAL_VISUAL_SIGNAL_SMOKE.json`.

Signed provider images could not be downloaded into the visual-inspection runtime. Do not treat signal metrics as composition/material/GATE-ART approval.

## 14. Open gates

- exact revision17 binary recovery + SHA-bound delivery: open;
- native R16 import/residency/traversal: not run;
- provider PR #6 pivot/manifest/anchor parity: blocked;
- human visual review of R16 taper: pending;
- non-circular/final root anatomy: pending review;
- HLOD/LOD target hardware qualification: pending;
- planetary scale: proposal pending decision.
