# SYLVA PRIME Macro — Engine Import Contract R13

Claim: `CLM-SYLVA-MACRO-001`  
Primary Blender: `05dce898-753d-4ff6-a4b0-31757dc868d8` @ **revision 13**  
State: `VERIFIED TECHNICAL CHECKPOINT / NOT FINAL ART`

## 1. Coordinate / world contract

- `1 Blender Unit = 1 metre`.
- Local authored patch: `12,000 × 12,000 m`, `PROPOSAL`; never infer planet radius from this patch.
- Blender source: Z-up. Use the engine's standard glTF conversion once.
- L3 terrain tile origins are cell-local in XY; world Z remains unchanged.
- Mesh/curve scale is 1:1 at r13 source QA.

## 2. Terrain morphology and partition

Morphology remains `R6_BIOGEO_CAUSAL_MACRO_V1`.

Current runtime-facing partition: `SYLVA_TERRAIN_STREAM_R12`.

### Render terrain
Required nodes:
- `SYLVA_TERRAIN_L3_X0Y0` … `SYLVA_TERRAIN_L3_X3Y3` = **16** tiles.

Per tile:
- 3,000 × 3,000 m footprint;
- 13×13 vertices @ 250 m;
- authoritative owner: matching `SYLVA_STREAM_L3_X#Y#` cell.

Total:
- 2,704 vertices;
- 2,304 faces;
- 285 shared seam coordinates verified;
- max/mean seam height delta = **0 m**.

### Collision terrain
Required nodes:
- `SYLVA_COL_TERRAIN_L3_X0Y0` … `SYLVA_COL_TERRAIN_L3_X3Y3` = **16** tiles.

Per tile:
- 9×9 vertices @ 375 m;
- policy `CUSTOM_LOWRES_HEIGHTFIELD_TILE`.

Total:
- 1,296 vertices;
- 1,024 faces;
- 189 shared seam coordinates verified;
- max/mean seam height delta = **0 m**.

### Forbidden legacy terrain after r12
- `SYLVA_TERRAIN_Macro12km_PROPOSAL`
- `SYLVA_COL_TERRAIN_Macro12km_LowRes_PROPOSAL`

A delivery containing either monolithic node is not an r13-valid current export.

Metadata node: `SYLVA_META_TerrainStreamingR12`.

## 3. Stream membership R13

Metadata node: `SYLVA_META_StreamMembershipR13`.  
Contract: `SYLVA_STREAM_MEMBERSHIP_R13`.

- 16 `SYLVA_STREAM_L3_X#Y#` 3 km cells;
- 147 owned spatial objects have explicit `stream_cells` metadata;
- 34 macro objects cross more than one cell;
- no owned spatial object lies outside the 12 km local patch;
- terrain render/collision tiles have exactly one authoritative owner cell;
- roots/routes/props/interfaces can declare multi-cell membership from world-bounds overlap.

This is backend-neutral. It does **not** assert a Godot/Unreal world-partition implementation.

## 4. Navigation R10

Metadata: `SYLVA_META_NavigationRouteContract`.  
Version: `SYLVA_NAV_R10`.  
Profile: `BALANCED_FOOT_TERRAIN_AWARE_R10`.

Stable centerlines:
- `SYLVA_TRAV_PathGuide_00` — 1,963.093 m / max 18.490°
- `SYLVA_TRAV_PathGuide_01` — 2,382.483 m / max 15.131°
- `SYLVA_TRAV_PathGuide_02` — 2,188.103 m / max 7.285°
- `SYLVA_TRAV_PathGuide_03` — 2,364.615 m / max 20.530°

Total: **8,898.294 m**.

Stable collision nodes:
- `SYLVA_COL_ROUTE_00..03`

Policy: `TERRAIN_AWARE_RIBBON_PROXY_MANIFOLD_R10`.

All four source meshes: 0 nonmanifold edges / 0 degenerate faces. Historical r9 is forbidden.

## 5. VESPER macro encounter contract

Required visible nodes:
- `SYLVA_VESPER_Terrace_00_ENTRY`
- `SYLVA_VESPER_Terrace_01_MIDDLE`
- `SYLVA_VESPER_Terrace_02_UPPER`
- `SYLVA_VESPER_TerraceConnector_00`
- `SYLVA_VESPER_TerraceConnector_01`
- `SYLVA_META_VESPER_ThreeTerraceLayout`

Required collision nodes:
- `SYLVA_COL_VESPER_Terrace_00_ENTRY`
- `SYLVA_COL_VESPER_Terrace_01_MIDDLE`
- `SYLVA_COL_VESPER_Terrace_02_UPPER`
- `SYLVA_COL_VESPER_Connector_00`
- `SYLVA_COL_VESPER_Connector_01`

Forbidden legacy:
- `SYLVA_VESPER_ProxyArenaFloor`
- `SYLVA_COL_VESPER_ArenaFloor`

Final VESPER remains outside this claim.

## 6. Root-kit consumer contract

Metadata: `SYLVA_META_RootKitSocketConsumerContract`.  
Consumer: `SYLVA_SOCKET_CONSUMER_V1`.  
Support map: `SYLVA_SOCKET_SUPPORT_MAP_V1`.

Basis:
- +X forward;
- +Z up;
- metres;
- scale 1.

Provider: `CLM-SYLVA-PROC-NROOT-001` / PR #6.

Provider instantiation remains `NOT_READY` because provider r4 audit found most sampled geometry 9–17.55 m away from object origin and provider manifest/pivot normalization is unresolved.

Rules:
- copy **zero** provider meshes into this claim;
- keep socket transforms frozen until provider publishes normalized pivots/anchors and render/collision anchor parity;
- re-audit provider read-only before consuming a new provider checkpoint.

## 7. Collision namespace

Current expected `SYLVA_COL_*` total: **27**.

Breakdown:
- terrain tiles: 16;
- Puerto deck: 1;
- Bosque pad: 1;
- route ribbons: 4;
- VESPER terraces/connectors: 5.

Importer must separate collision from visible art and must not silently substitute render meshes as collision.

## 8. GLB transport / semantic validation

Shared main delivery hardening from `ca224a78...` requires:
- SHA-bound recovered artifacts;
- every GLB chunk walked;
- 4-byte chunk alignment;
- chunk-bound validation;
- unique JSON/BIN chunks;
- no external resources;
- explicit native evidence paths.

Claim-local current validator:

```bash
python3 art_source/worlds/sylva_prime/macro/validate_glb_contract_r13.py recovered.glb --expected-sha256 <SHA256>
```

It additionally requires:
- 16 render + 16 collision terrain tiles;
- r12/r13 metadata nodes;
- no monolithic terrain nodes;
- stable VESPER/root-kit/navigation contracts;
- route-collision closed-manifold topology.

Exact r13 GLB byte/SHA validation remains `ENV_BLOCKED_BINARY_RECOVERY` in this sandbox. Remote provider size/etag is not a substitute for a recovered SHA.

## 9. Native acceptance sequence

1. Recover exact r13 `.blend` and GLB into an authorized checkout.
2. Compute SHA-256 for both artifacts.
3. Run shared `fleet_control.py delivery` with explicit evidence paths.
4. Run `validate_glb_contract_r13.py` against the same GLB SHA.
5. Import exact artifact through pinned/current qualified engine path with no manual global-scale multiplier.
6. Confirm all 16 L3 cell nodes and their terrain/collision children survive import or are deliberately converted.
7. Preserve/convert `stream_cells` membership metadata with an explicit importer map.
8. Test cell-boundary residency and unloading behavior; verify no cracks, double collision or missing collision.
9. Traverse all four terrain-aware route legs and all VESPER terraces using the real controller.
10. Do not instantiate PR #6 modules until provider pivot/manifest gates pass.
11. Profile only on declared target hardware/preset.

## 10. Current remote identity

r13 remote metadata, not recovered delivery proof:
- `.blend`: **2,777,367 B**, etag `dcb49cece03e111d066cad486ea77c1d`;
- GLB: **1,204,308 B**, etag `695fc7907b522dc42d8f09f697b3d99a`.

## 11. Open gates

- fleet ACK/path/orbital-project publication: pending;
- exact binary recovery + SHA: `ENV_BLOCKED`;
- root-kit provider pivot/manifest: `BLOCKED`;
- native stream residency/traversal: not run;
- HLOD/LOD implementation: not qualified;
- target-hardware performance: blocked;
- human art review: pending;
- planetary scale: proposal pending decision.
