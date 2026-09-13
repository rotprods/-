# SYLVA PRIME Macro — Engine Import Contract R15

Claim: `CLM-SYLVA-MACRO-001`  
Primary Blender: `05dce898-753d-4ff6-a4b0-31757dc868d8` @ **revision 15**  
State: `VERIFIED TECHNICAL CHECKPOINT / NOT FINAL ART`

## 1. Coordinate / world contract

- `1 Blender Unit = 1 metre`.
- Local authored patch: `12,000 × 12,000 m`, PROPOSAL; never infer planet radius from it.
- Blender source is Z-up; use the engine's normal glTF axis conversion once.
- R12 terrain tile origins are cell-local in XY; world Z remains authored.
- Current MESH/CURVE geometry fingerprint is invariant from accepted r13 through r15:
  `003760384ade90b7b0b792de6850a2eae90322d22f2ca246f8211395cb3e6224`.

R14/R15 are metadata/hierarchy waves and must not alter this geometry fingerprint.

## 2. Terrain morphology / R12 partition

Morphology: `R6_BIOGEO_CAUSAL_MACRO_V1`.

Runtime-facing terrain contract: `SYLVA_TERRAIN_STREAM_R12`.

### Render terrain

Required: 16 nodes `SYLVA_TERRAIN_L3_X0Y0` … `SYLVA_TERRAIN_L3_X3Y3`.

Per tile:
- 3,000 × 3,000 m;
- 13×13 vertices @ 250 m;
- authoritative matching `SYLVA_STREAM_L3_X#Y#` owner cell.

Aggregate source QA:
- 2,704 vertices / 2,304 faces;
- 285 shared seam samples;
- max/mean seam Δz = **0 m**.

### Collision terrain

Required: 16 nodes `SYLVA_COL_TERRAIN_L3_X0Y0` … `SYLVA_COL_TERRAIN_L3_X3Y3`.

Per tile:
- 9×9 vertices @ 375 m;
- policy `CUSTOM_LOWRES_HEIGHTFIELD_TILE`.

Aggregate source QA:
- 1,296 vertices / 1,024 faces;
- 189 shared seam samples;
- max/mean seam Δz = **0 m**.

Forbidden legacy nodes:
- `SYLVA_TERRAIN_Macro12km_PROPOSAL`;
- `SYLVA_COL_TERRAIN_Macro12km_LowRes_PROPOSAL`.

Metadata: `SYLVA_META_TerrainStreamingR12`.

## 3. R13 spatial membership

Metadata: `SYLVA_META_StreamMembershipR13`.  
Contract: `SYLVA_STREAM_MEMBERSHIP_R13`.

- 16 L3 cells @ 3 km;
- R13 checkpoint assigned 147 owned spatial objects;
- 34 macro objects crossed more than one cell;
- 0 owned spatial objects were outside the local patch;
- terrain tiles use one authoritative cell;
- roots/routes/interfaces may have multi-cell bounds membership.

This is residency provenance, not a runtime backend implementation.

## 4. R14 L2/L3 hierarchy

Metadata: `SYLVA_META_StreamHierarchyR14`.  
Contract: `SYLVA_STREAM_HIERARCHY_R14`.

Required L2 nodes:
- `SYLVA_STREAM_L2_X0Y0`
- `SYLVA_STREAM_L2_X0Y1`
- `SYLVA_STREAM_L2_X1Y0`
- `SYLVA_STREAM_L2_X1Y1`

Each L2 is 6 km and references exactly four existing L3 cells. L3 and L2 4/8-neighbor graphs are symmetric. L2 is grouping/coverage/HLOD orchestration metadata; it is **not duplicated geometry**.

### Hero residency semantics

Residency is L3-only:
- Puerto: `X0Y1`, `X1Y1`;
- Bosque: `X1Y1`, `X1Y2`, `X2Y1`, `X2Y2`;
- VESPER: `X2Y2`, `X3Y2`.

Bosque overlaps all four L2 groups by coverage. This must never be translated into automatic full-residency of all four L2 groups. `hero_l2_full_residency_implied=false` is an invariant.

Do not move Bosque to simplify world partition.

## 5. R15 prefetch policy contract

Contract: `SYLVA_PREFETCH_POLICY_R15`.

Current state: `RUNTIME_EXPERIMENT_REQUIRED`.  
Production policy approved: **false**.

Required candidates retained for native comparison:
- `P0_CURRENT_ONLY`;
- `P1_CURRENT_PLUS_4`;
- `P2_CURRENT_PLUS_8`;
- `P3_DIRECTIONAL_ROUTE_WINDOW`.

`P3_DIRECTIONAL_ROUTE_WINDOW` is the primary runtime candidate only; it is not production-approved.

R14 pressure study found current+8 can conservatively touch up to **72.8%** of the current spatial-object set by membership cardinality. Therefore importers/runtimes must not treat an old `ADJACENT_8...` value as authority.

Selection rule:
> promote the least-resident policy that passes native visual, collision, traversal and measured load/residency-latency gates.

Source experiment: `PREFETCH_POLICY_R14_EXPERIMENT.json`.  
Native plan: `NATIVE_STREAM_RESIDENCY_TEST_PLAN.md`.

## 6. Navigation R10

Metadata: `SYLVA_META_NavigationRouteContract`.  
Contract: `SYLVA_NAV_R10`.  
Profile: `BALANCED_FOOT_TERRAIN_AWARE_R10`.

Stable centerlines:
- `SYLVA_TRAV_PathGuide_00` — 1,963.093 m / max 18.490°;
- `SYLVA_TRAV_PathGuide_01` — 2,382.483 m / max 15.131°;
- `SYLVA_TRAV_PathGuide_02` — 2,188.103 m / max 7.285°;
- `SYLVA_TRAV_PathGuide_03` — 2,364.615 m / max 20.530°.

Total: **8,898.294 m**.

Collision nodes `SYLVA_COL_ROUTE_00..03` use `TERRAIN_AWARE_RIBBON_PROXY_MANIFOLD_R10`; accepted r15 source QA still reports 0 nonmanifold edges and 0 degenerate faces for all four. Historical r9 is forbidden.

## 7. Native seam probes

Approximate route-transition probes from read-only 25 m centerline sampling:

| ID | From → To | Approx point (m) |
|---|---|---|
| S-00 | X0Y1 → X1Y1 | `(-3000, -2000, 345.8)` |
| S-01 | X1Y1 → X1Y2 | `(-500, 0, 356.1)` |
| S-02 | X1Y2 → X2Y2 | `(0, 250, 352.2)` |
| S-03 | X2Y2 → X3Y2 | `(3000, 2000, -72.4)` |

Use these as repeatable streaming/collision transition probes; they are not centimeter-exact gameplay markers.

## 8. VESPER macro encounter

Required visible nodes:
- `SYLVA_VESPER_Terrace_00_ENTRY`
- `SYLVA_VESPER_Terrace_01_MIDDLE`
- `SYLVA_VESPER_Terrace_02_UPPER`
- `SYLVA_VESPER_TerraceConnector_00`
- `SYLVA_VESPER_TerraceConnector_01`
- `SYLVA_META_VESPER_ThreeTerraceLayout`

Required collision:
- `SYLVA_COL_VESPER_Terrace_00_ENTRY`
- `SYLVA_COL_VESPER_Terrace_01_MIDDLE`
- `SYLVA_COL_VESPER_Terrace_02_UPPER`
- `SYLVA_COL_VESPER_Connector_00`
- `SYLVA_COL_VESPER_Connector_01`

Forbidden legacy single-floor arena nodes remain forbidden. Final VESPER model/rig/attacks remain outside this claim.

## 9. Root-kit consumer contract

Metadata: `SYLVA_META_RootKitSocketConsumerContract`.  
Consumer: `SYLVA_SOCKET_CONSUMER_V1`.  
Support map: `SYLVA_SOCKET_SUPPORT_MAP_V1`.

Consumer basis:
- +X forward;
- +Z up;
- metres;
- scale 1.

Provider: PR #6 / `CLM-SYLVA-PROC-NROOT-001`.

Latest provider re-audit at HEAD `5ba1ea6758e4c08ed82d95deb96f1bbcae1581f5` remains **NOT_READY** despite CI Gauntlet success:
- current manifest still contains invalid YAML structure around `materials`/`note`;
- generator still does not publish normalized per-asset pivots/anchors;
- render/collision anchor parity is not proven;
- no pivot-policy version is authoritative.

Importer rule: instantiate **zero** provider modules until all four gates above pass and provider is re-audited read-only. Current macro source contains zero provider meshes.

## 10. Collision namespace

Current expected `SYLVA_COL_*` macro nodes: **27**.

- terrain tiles: 16;
- Puerto deck: 1;
- Bosque pad: 1;
- route ribbons: 4;
- VESPER terraces/connectors: 5.

Collision must remain distinct from visible final art. HLOD must not become gameplay collision unless a future engine-specific ADR explicitly authorizes it.

## 11. GLB transport / semantic validation

Shared delivery hardening requires recovered SHA-bound `.blend` and GLB, complete GLB chunk walking, 4-byte alignment, bounds, unique JSON/BIN, no external resources and a native receipt with explicit evidence paths.

Current claim validator baseline remains `validate_glb_contract_r13.py`; it proves streamed terrain/current-node and inherited route topology semantics. R14/R15 add EMPTY/custom metadata contracts rather than new MESH/CURVE geometry, so a future validator revision must additionally assert the R14/R15 nodes/properties once exact GLB property preservation is confirmed.

Remote r15 size/etag is **not** delivery PASS.

## 12. Native acceptance sequence

1. Recover exact r15 `.blend` and GLB into an authorized checkout.
2. Compute SHA-256 for both.
3. Run shared `fleet_control.py delivery` with explicit evidence paths.
4. Run claim-local GLB validation against the same GLB SHA.
5. Import exact artifact through a qualified engine path without an ad-hoc global scale multiplier.
6. Map/preserve R12 terrain, R13 membership, R14 hierarchy and R15 policy metadata explicitly.
7. Verify render/collision readiness separately at S-00..S-03.
8. Compare P0/P1/P2/P3 policies with instrumented load-to-ready latency, resident objects/memory, frame spikes, pop-in and reversal behavior.
9. Traverse all four route legs and all three VESPER terraces with the real controller.
10. Keep root-kit provider instances disabled until provider gates pass.
11. Profile only on declared target hardware/preset.
12. Require human art review independently of runtime PASS.

## 13. Current remote identity

r15 remote metadata:
- `.blend`: **2,848,052 B**, etag `d95ef102d90bf84db182c8d8be85b1bd`;
- GLB: **1,218,436 B**, etag `d5de5a68ca567167b1f696ceefdba088`.

## 14. Open gates

- exact binary recovery + SHA-bound delivery: not yet qualified;
- native R15 metadata import/residency policy experiment: not run;
- PR #6 provider pivot/manifest/anchor parity: blocked;
- human art review: pending;
- HLOD/LOD target-hardware qualification: pending;
- planetary scale: proposal pending explicit decision.
