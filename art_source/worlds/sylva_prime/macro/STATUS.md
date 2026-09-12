# STATUS — CLM-SYLVA-MACRO-001

**Agent:** `AGENT-SYLVA-MACRO-01`  
**Branch:** `art/world-sylva-prime-macro-001`  
**Primary Blender:** `05dce898-753d-4ff6-a4b0-31757dc868d8` @ **revision 11**  
**State:** `IN_PROGRESS / VERIFIED R11 TECHNICAL CHECKPOINT`  
**Claim:** `KEEP / CHECKPOINT`

## Current truth

This branch owns SYLVA PRIME macro/regional terrain, region placement, navigation centerlines, streaming/collision interfaces, VESPER macro layout and root-kit consumer sockets. It is **not final world art**.

PR #6 exclusively owns reusable meso neural-root modules. Final VESPER/NPC/fauna/vegetation/architecture/gameplay/material polish remain outside this claim.

## Wave progression

- r1 — local 12 km terrain blockout + canonical region foundations.
- r2 — portable lighting/review cameras.
- r3 — camera clip correction + file-backed render smoke.
- r4 — streaming cells/envelopes, sockets, macro collision interfaces.
- r5 — canon fix: three VESPER terraces + two wide connectors.
- r6 — causal biogeomorphic macro terrain shared by render/collision.
- r7 — root-kit consumer basis and provider-pivot blocker.
- r8 — explicit semantic support map for all eight sockets; zero transforms snapped.
- r9 — terrain-aware navigation prototype; **collision topology invalid / historical failed checkpoint**.
- r10 — collision ribbons rebuilt manifold; invalid-mesh export warnings eliminated.
- r11 — metadata normalized so scene/generators agree on R10 navigation and socket contracts.

## R11 scene metrics

- objects: **151**;
- mesh objects: **91**;
- curve objects: **12**;
- approximate triangles: **19,928**;
- streaming L3 cells: **16**;
- streaming region envelopes: **3**;
- macro collision nodes: **12**;
- VESPER terraces/connectors: **3 / 2**;
- root-kit sockets: **8**;
- provider meshes copied: **0**;
- final-scope violations: **0**;
- non-`SYLVA_` objects: **0**;
- non-unit mesh/curve scales: **0**.

Remote artifacts:
- `.blend`: **2,382,689 B**, etag `095b96cc5dfca24bb086ac8b7b315d17`;
- GLB: **1,325,280 B**, etag `5da3def12f2919b530bf6b4fc738a0e9`.

## Terrain R6 retained

`R6_BIOGEO_CAUSAL_MACRO_V1`:
- visible terrain 2,401 verts / 2,304 faces;
- collision terrain 1,089 verts / 1,024 faces;
- 289 render↔collision common samples: max/mean Δz **0 m**;
- six proposed structural-root ridges;
- two proposed catchment/depression shapes;
- no microdetail or canonical tectonics/waterways claimed.

Terrain face slopes: median 4.939°, p95 20.297°, max 51.231°.

## Navigation R10

Contract: `SYLVA_NAV_R10` / `BALANCED_FOOT_TERRAIN_AWARE_R10`.

| Route | Length | Max grade | Collision |
|---|---:|---:|---|
| 00 | 1,963.093 m | 18.490° | manifold, 0 degenerate |
| 01 | 2,382.483 m | 15.131° | manifold, 0 degenerate |
| 02 | 2,188.103 m | 7.285° | manifold, 0 degenerate |
| 03 | 2,364.615 m | 20.530° | manifold, 0 degenerate |

Total centerline chain: **8,898.294 m**.

Route geometry remains a navigation proposal, not final grown-root/road art. `movement_mode=UNASSIGNED_BASELINE` until runtime qualification.

### Historical failure retained

r9 collision ribbons produced glTF `mesh not valid` warnings. r10 rebuilt them with closed side/cap topology:
- route00 28 verts / 26 faces;
- route01 36 / 34;
- route02 32 / 30;
- route03 36 / 34;
- nonmanifold edges = 0 for all;
- degenerate faces = 0 for all.

Never deliver r9.

## Root-kit integration

Consumer metadata:
- `SYLVA_SOCKET_CONSUMER_V1`;
- `SYLVA_SOCKET_SUPPORT_MAP_V1`;
- `+X` forward / `+Z` up / metre units / scale 1.

Read-only audit of PR #6 Blender r4 found most sampled provider module geometry offset **9–17.55 m** from object origin. PR #6 receipt: comment `5648741376`.

Therefore:
- provider pivot status: `BLOCKED_PROVIDER_NORMALIZATION_REQUIRED`;
- provider instances created: **0**;
- provider meshes copied: **0**;
- all eight support roles are explicit but transforms remain unsnapped/frozen;
- provider manifest validity/pivot policy must pass before consumption.

## VESPER retained

- three terraces: 116 / 124 / 112 m diameter;
- connectors: 142.215 m @ 12.178° and 145.685 m @ 12.689°;
- 18 m visible / 16 m collision width;
- no precision jumps;
- obsolete single-floor arena absent;
- final VESPER absent.

## GLB validation

Current validator: `validate_glb_contract_r10.py`.

It validates required namespaces/counts/scope and decodes route collision accessors to require closed-manifold, non-degenerate triangle topology.

Synthetic equivalent-logic gauntlet: **10/10 PASS**. Receipt: `qa/GLB_CONTRACT_SELFTEST_R10.json`.

Exact r11 GLB byte/SHA validation remains `ENV_BLOCKED_BINARY_RECOVERY`; synthetic PASS is not promoted to real-artifact PASS.

## Render signal

r11 master smoke:
- 320×180;
- PNG 90,993 B;
- mean RGB 0.32439;
- variance 0.06411;
- max 0.78431;
- `PASS_NONBLANK`.

This is signal validation only. Human visual/art review is pending.

## Reproducible build chain

1. `generate_sylva_macro.py`
2. `add_sylva_macro_interfaces.py`
3. `add_vesper_three_terraces.py`
4. `refine_macro_terrain_r6.py`
5. `apply_socket_consumer_contract_r7.py`
6. `apply_socket_support_map_r8.py`
7. `build_terrain_aware_routes_r10.py`
8. r11 metadata normalization is trivial/non-geometric and documented by scene metadata + QA receipt.

Key QA:
- `qa/R5_VESPER_CANON_LAYOUT.json`
- `qa/R6_TERRAIN_CAUSALITY.json`
- `qa/R7_ROOTKIT_SOCKET_INTEGRATION.json`
- `qa/R11_NAVIGATION_AND_ROOTKIT_INTEGRATION.json`
- `qa/GLB_CONTRACT_SELFTEST_R10.json`
- `qa/ENGINE_IMPORT_ENV_BLOCKER.json`

## Planetary scale

Option C / 1.20 R⊕ remains a reversible proposal only. Separate orbital project `c796230b-0463-4e17-9446-2e746c5c4933` remains EMPTY r0 until fleet registry explicitly includes it.

## Open P0

1. Fleet integrator ACK/path/project-ID publication.
2. PR #6 valid manifest + normalized module pivot/anchor contract.
3. Recover exact r11 `.blend`/GLB and bind SHA-256.
4. Run R10 validator against recovered GLB bytes.
5. Import into pinned Godot 4.7.2/current runtime and traverse all four route legs + VESPER terraces.
6. Human art-direction review.
7. Decide/defer planetary scale before any L0/L1 production promotion.

## Gates

| Gate | State |
|---|---|
| Canon regions / VESPER layout | PASS_BLOCKOUT |
| Terrain causality + render↔collision | PASS_R6 |
| Navigation source topology | PASS_R10 |
| Namespace / unit transforms | PASS_R11 |
| Streaming/collision interfaces | PASS_PROPOSAL |
| Root-kit consumer basis/support map | PASS |
| Root-kit provider pivot/manifest | BLOCKED |
| GLB validator logic | PASS_SELFTEST_10_OF_10 |
| Exact GLB byte/SHA validation | ENV_BLOCKED |
| Remote export/editable source | PASS_R11 |
| Engine import/traversal | NOT_RUN |
| Human art review | PENDING |
| LOD/HLOD/performance | BLOCKED_TARGET_HARDWARE |
| Planet radius canon | PROPOSAL_PENDING_DECISION |
