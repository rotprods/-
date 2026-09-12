# SYLVA PRIME Macro — Engine Import Contract R11

Claim: `CLM-SYLVA-MACRO-001`  
Primary Blender: `05dce898-753d-4ff6-a4b0-31757dc868d8` @ **revision 11**  
State: `VERIFIED TECHNICAL CHECKPOINT / NOT FINAL ART`

## 1. Coordinate contract

- `1 Blender Unit = 1 metre`.
- Local authored envelope: `12,000 × 12,000 m`, `PROPOSAL`; never infer planet size from it.
- Blender source is Z-up; use the engine's normal glTF axis conversion once.
- Owned render/collision geometry is unit scale at the r10/r11 QA checkpoint.

## 2. Terrain contract

Visible terrain: `SYLVA_TERRAIN_Macro12km_PROPOSAL`  
Collision terrain: `SYLVA_COL_TERRAIN_Macro12km_LowRes_PROPOSAL`

Model: `R6_BIOGEO_CAUSAL_MACRO_V1`.

- render: 49×49 / 2,401 vertices / 2,304 faces;
- collision: 33×33 / 1,089 vertices / 1,024 faces;
- 289 common coordinates compared: max/mean height delta = **0 m**;
- macro terrain shaping is a production proposal, not canonical tectonics/waterways.

## 3. Navigation contract R10

Metadata node: `SYLVA_META_NavigationRouteContract`  
Version: `SYLVA_NAV_R10`  
Profile: `BALANCED_FOOT_TERRAIN_AWARE_R10`  
Solver: `A*_8_NEIGHBOR_SLOPE_WEIGHTED_R10`  
Hard solver grade ceiling: 22°.

Stable centerline IDs:
- `SYLVA_TRAV_PathGuide_00`
- `SYLVA_TRAV_PathGuide_01`
- `SYLVA_TRAV_PathGuide_02`
- `SYLVA_TRAV_PathGuide_03`

Measured current route chain:

| Leg | Length | Max grade |
|---|---:|---:|
| 00 | 1,963.093 m | 18.490° |
| 01 | 2,382.483 m | 15.131° |
| 02 | 2,188.103 m | 7.285° |
| 03 | 2,364.615 m | 20.530° |

Total: **8,898.294 m**.

These are navigation interfaces, not final road/root art. `movement_mode=UNASSIGNED_BASELINE`; runtime and vehicle teams still decide gameplay traversal.

### Route collision R10

Stable IDs:
- `SYLVA_COL_ROUTE_00`
- `SYLVA_COL_ROUTE_01`
- `SYLVA_COL_ROUTE_02`
- `SYLVA_COL_ROUTE_03`

Policy: `TERRAIN_AWARE_RIBBON_PROXY_MANIFOLD_R10`.

Source Blender QA:
- 00: 28 verts / 26 faces / 0 nonmanifold edges / 0 degenerate faces;
- 01: 36 / 34 / 0 / 0;
- 02: 32 / 30 / 0 / 0;
- 03: 36 / 34 / 0 / 0.

Historical r9 generated invalid ribbons and glTF warnings. **Never deliver r9.** R10 replaced side/cap topology and exports cleanly.

## 4. Cámara de VESPER contract

Required macro layout:
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

Forbidden legacy r4 nodes:
- `SYLVA_VESPER_ProxyArenaFloor`
- `SYLVA_COL_VESPER_ArenaFloor`

Final VESPER asset remains outside this claim.

## 5. Root-kit consumer contract

Metadata: `SYLVA_META_RootKitSocketConsumerContract`  
Consumer version: `SYLVA_SOCKET_CONSUMER_V1`  
Support map: `SYLVA_SOCKET_SUPPORT_MAP_V1`.

Consumer basis:
- local `+X` = forward;
- local `+Z` = up;
- metres;
- scale 1:1.

Provider: `CLM-SYLVA-PROC-NROOT-001` / PR #6.

Eight socket→provider IDs remain stable, but **provider instantiation is NOT_READY**.

Read-only provider r4 audit found seven sampled module objects with geometry 9–17.55 m away from object origin; only sampled `C2_TERRACE_CALLOUS` was centered. PR #6 blocker receipt: `5648741376`.

Therefore:
- no provider geometry is copied into this claim;
- socket transforms remain frozen;
- semantic support objects are assigned but **not snapped**;
- provider must publish normalized per-asset anchors/pivots, basis and collision parity before consumption;
- provider manifest must also parse/validate before integration.

## 6. Streaming contract

- 16 `SYLVA_STREAM_L3_*` local 3 km proposal cells;
- 3 `SYLVA_STREAM_REGION_*` regional envelopes.

These are portable metadata interfaces. They do not choose Godot/Unreal streaming implementation.

## 7. Collision contract

Exactly 12 `SYLVA_COL_*` macro collision nodes are expected:
- terrain: 1;
- Puerto: 1;
- Bosque: 1;
- routes: 4;
- VESPER terraces/connectors: 5.

Importer must not render collision proxies as final art and must not silently use high-detail render meshes as collision.

## 8. GLB pre-import validation

Current validator:

```bash
python3 art_source/worlds/sylva_prime/macro/validate_glb_contract_r10.py recovered.glb --expected-sha256 <SHA256>
```

Contract: `CLM-SYLVA-MACRO-001/R10`.

It validates GLB transport/names/counts/scope and decodes the route collision accessors to require closed-manifold, non-degenerate triangle topology.

Synthetic equivalent-logic gauntlet: **10/10 PASS**, including rejection of an open route collision mesh. Receipt: `qa/GLB_CONTRACT_SELFTEST_R10.json`.

The real r11 GLB has **not** passed this byte-level check because signed artifact recovery is network-blocked in the current sandbox. Do not convert the synthetic PASS into a real-artifact PASS.

## 9. Native acceptance sequence

1. Recover exact r11 `.blend` and GLB into an authorized delivery checkout.
2. Compute and record SHA-256.
3. Run `validate_glb_contract_r10.py` against the exact GLB.
4. Import via pinned Godot 4.7.2/current qualified engine path with no manual global scale multiplier.
5. Verify required node IDs and metadata survive or are deliberately converted.
6. Split all `SYLVA_COL_*` from visible geometry.
7. Do **not** instantiate PR #6 root modules until pivot/manifest gates pass.
8. Spawn the real project controller at Puerto.
9. Traverse all four terrain-aware legs and all three VESPER terraces using normal controls.
10. Record snagging/falls/camera obstruction/scale/material/collision failures.
11. Repeat with the future Sylva vehicle only after its movement envelope is separately qualified.
12. Profile only on declared target hardware/preset.

## 10. Current r11 remote identity

Remote-provider metadata, not recovered delivery proof:
- `.blend`: **2,382,689 B**, etag `095b96cc5dfca24bb086ac8b7b315d17`;
- GLB: **1,325,280 B**, etag `5da3def12f2919b530bf6b4fc738a0e9`.

Master render smoke: 320×180, 90,993 B, nonblank. Signal existence is not `GATE-ART`.

## 11. Open gates

- fleet ACK/path/project-ID publication: pending;
- exact binary recovery + SHA: `ENV_BLOCKED`;
- root-kit provider pivot/manifest: `BLOCKED`;
- engine import/traversal: not run;
- human art review: pending;
- LOD/HLOD/target performance: pending;
- planetary scale: proposal pending decision.
