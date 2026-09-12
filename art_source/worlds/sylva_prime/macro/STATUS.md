# STATUS — CLM-SYLVA-MACRO-001

**Agent:** `AGENT-SYLVA-MACRO-01`  
**Branch:** `art/world-sylva-prime-macro-001`  
**Primary Blender:** `05dce898-753d-4ff6-a4b0-31757dc868d8` @ **revision 13**  
**State:** `IN_PROGRESS / VERIFIED R13 TECHNICAL CHECKPOINT`  
**Claim:** `KEEP / CHECKPOINT`

## Current truth

This claim owns the SYLVA PRIME macro/regional foundation: causal terrain, canonical region placement, terrain-aware navigation, backend-agnostic streaming/collision interfaces, VESPER macro encounter layout and consumer sockets toward PR #6. It is **not final world art**.

PR #6 exclusively owns reusable meso neural-root modules. Final VESPER/NPC/fauna/vegetation/architecture/gameplay/material polish remain outside this claim.

## Wave progression

- r1 — 12 km local terrain blockout + canonical region foundations.
- r2 — portable lighting/review cameras.
- r3 — camera-range correction + render signal QA.
- r4 — 16 L3 cells, regional envelopes, root-kit sockets, collision interfaces.
- r5 — canon correction: 3 VESPER terraces + 2 wide connectors.
- r6 — causal biogeomorphic terrain shared by render/collision.
- r7 — root-kit consumer basis + provider-pivot blocker.
- r8 — semantic socket support map; 0 transforms snapped.
- r9 — failed terrain-aware collision-ribbon attempt; **not deliverable**.
- r10 — terrain-aware navigation + manifold route collisions.
- r11 — navigation/socket metadata normalized; delivery hardening adopted from main.
- r12 — monolithic terrain retired; 16 render + 16 collision terrain tiles created.
- r13 — stream-cell membership assigned to every owned spatial object.

## R13 scene truth

Remote artifacts:
- `.blend`: **2,777,367 B**, etag `dcb49cece03e111d066cad486ea77c1d`;
- GLB: **1,204,308 B**, etag `695fc7907b522dc42d8f09f697b3d99a`.

Scene QA:
- objects: **182**;
- mesh objects: **121**;
- curve objects: **12**;
- L3 stream cells: **16**;
- regional envelopes: **3**;
- VESPER terraces/connectors: **3 / 2**;
- root-kit sockets: **8**;
- provider meshes copied: **0**;
- final-scope violations: **0**;
- non-`SYLVA_` objects: **0**;
- non-unit mesh/curve scales: **0**.

## Terrain R6 → streamed R12

Terrain morphology remains `R6_BIOGEO_CAUSAL_MACRO_V1`; r12 changes partition/origin structure, not heights.

### Render
- 16 `SYLVA_TERRAIN_L3_X#Y#` tiles;
- each tile: 3,000 × 3,000 m;
- each tile grid: 13×13 @ 250 m;
- total render vertices: **2,704** (boundary duplication only);
- total render faces: **2,304** — identical face count to pre-split terrain;
- shared seam points checked: **285**;
- max/mean seam height delta: **0 m**.

### Collision
- 16 `SYLVA_COL_TERRAIN_L3_X#Y#` tiles;
- each tile grid: 9×9 @ 375 m;
- total collision vertices: **1,296**;
- total collision faces: **1,024** — identical face count to pre-split collision terrain;
- shared seam points checked: **189**;
- max/mean seam height delta: **0 m**.

The monolithic nodes are retired and now legacy:
- `SYLVA_TERRAIN_Macro12km_PROPOSAL`;
- `SYLVA_COL_TERRAIN_Macro12km_LowRes_PROPOSAL`.

Contract: `SYLVA_TERRAIN_STREAM_R12`.

## R13 stream membership

Contract: `SYLVA_STREAM_MEMBERSHIP_R13`.

- spatial objects assigned: **147**;
- objects outside local patch: **0**;
- cross-cell objects: **34**;
- maximum cells touched by one object: **6**;
- terrain tiles use one authoritative owner cell even though boundary vertices are duplicated;
- other macro objects use world-bounds overlap and may carry multi-cell membership.

Largest cross-cell structures:
- `SYLVA_ROOT_PRIMARY_R04`: 6 cells;
- `SYLVA_ROOT_PRIMARY_R05`: 6 cells;
- `SYLVA_ROOT_PRIMARY_R01/R02/R03/R06`: up to 4 cells;
- route/collision objects retain multi-cell membership where required.

This is portable metadata, not a Godot/Unreal streaming-backend decision.

## Navigation R10 retained

`SYLVA_NAV_R10` / `BALANCED_FOOT_TERRAIN_AWARE_R10`:
- leg00: 1,963.093 m / max 18.490°;
- leg01: 2,382.483 m / max 15.131°;
- leg02: 2,188.103 m / max 7.285°;
- leg03: 2,364.615 m / max 20.530°;
- total: **8,898.294 m**.

All four route-collision ribbons remain closed manifold with 0 nonmanifold edges and 0 degenerate faces. Historical r9 remains forbidden.

## Root-kit dependency

Consumer contracts:
- `SYLVA_SOCKET_CONSUMER_V1`;
- `SYLVA_SOCKET_SUPPORT_MAP_V1`;
- +X forward / +Z up / metres / scale 1.

PR #6 provider remains `NOT_READY`: read-only audit showed sampled module geometry offset ~9–17.55 m from object origin; provider manifest/pivot normalization must pass before instancing. Provider instances: **0**. Provider geometry copied: **0**.

## VESPER retained

- 3 terraces: 116 / 124 / 112 m diameter;
- connectors: 142.215 m @ 12.178° and 145.685 m @ 12.689°;
- 18 m visual / 16 m collision width;
- no precision jumps;
- obsolete single-floor arena absent;
- final VESPER absent.

## Validation / delivery

Current claim-local validator: `validate_glb_contract_r13.py`.

It requires:
- shared-main R11 transport envelope hardening;
- 16 streamed render terrain nodes;
- 16 streamed collision terrain nodes;
- R12/R13 metadata nodes;
- no legacy monolithic terrain;
- stable VESPER/navigation/root-kit scope rules;
- closed-manifold route collisions.

Exact r13 GLB SHA-bound validation still requires binary recovery. Current environment remains `ENV_BLOCKED_BINARY_RECOVERY`; remote export metadata is not promoted to delivery PASS.

Reproducible build chain:
1. `generate_sylva_macro.py`
2. `add_sylva_macro_interfaces.py`
3. `add_vesper_three_terraces.py`
4. `refine_macro_terrain_r6.py`
5. `apply_socket_consumer_contract_r7.py`
6. `apply_socket_support_map_r8.py`
7. `build_terrain_aware_routes_r10.py`
8. r11 metadata normalization
9. `split_streaming_terrain_r12.py`
10. `assign_stream_membership_r13.py`

Key QA:
- `qa/R11_NAVIGATION_AND_ROOTKIT_INTEGRATION.json`
- `qa/R13_STREAMING_WORLD_PARTITION.json`
- `qa/GLB_CONTRACT_SELFTEST_R10.json`
- `qa/ENGINE_IMPORT_ENV_BLOCKER.json`

## Fleet / planetary boundary

- branch synchronized with `main@97fb47472a654112779655d4d537851e709f269a` before r12/r13 production;
- owner-admission learning applied and documented;
- accidental default-branch publication was repaired through PR #21 without force;
- orbital project `c796230b-0463-4e17-9446-2e746c5c4933` remains EMPTY r0 because fleet registry still exposes only the primary project and `ack:null`;
- Option C / 1.20 R⊕ remains proposal only.

## Open P0

1. Fleet integrator ACK/path/orbital-project publication.
2. PR #6 valid manifest + normalized per-asset pivot/anchor contract.
3. Recover exact r13 `.blend`/GLB, bind SHA-256 and run shared delivery + `validate_glb_contract_r13.py`.
4. Native engine import and real-controller traversal/residency test across L3 boundaries and VESPER terraces.
5. Human art-direction review.
6. Target-hardware HLOD/LOD/performance qualification.
7. Explicit decision before planetary-scale promotion.

## Gates

| Gate | State |
|---|---|
| Canon regions / VESPER layout | PASS_BLOCKOUT |
| Terrain causality | PASS_R6 |
| Terrain streaming partition | PASS_R12_SOURCE |
| Stream membership | PASS_R13_SOURCE |
| Terrain seams | PASS_ZERO_DELTA |
| Navigation topology | PASS_R10 |
| Namespace / unit transforms | PASS_R13 |
| Root-kit consumer basis/support | PASS |
| Root-kit provider pivot/manifest | BLOCKED |
| Remote export/editable source | PASS_R13 |
| Exact GLB SHA/delivery | ENV_BLOCKED |
| Engine residency/traversal | NOT_RUN |
| Human art review | PENDING |
| HLOD/target performance | BLOCKED_TARGET_HARDWARE |
| Planet radius canon | PROPOSAL_PENDING_DECISION |
