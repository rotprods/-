# SYLVA PRIME Macro — Engine Import Contract

Claim: `CLM-SYLVA-MACRO-001`  
Remote source: Higgsfield 3D Jutsu project `05dce898-753d-4ff6-a4b0-31757dc868d8`, validated revision `5`  
Status: `BLOCKOUT / INTEGRATION CONTRACT`, not final art.

## Purpose

This contract removes importer ambiguity before the r5 GLB enters Godot/Unreal. It does **not** claim runtime import has passed. It defines deterministic naming and classification so render geometry, collision interfaces, streaming metadata and provider sockets can be separated without heuristics.

## Coordinate / scale contract

- Blender source uses metric units: `1 Blender Unit = 1 metre`.
- Current local authored envelope is `12,000 × 12,000 m` and classified `PROPOSAL`.
- Physical Sylva Prime radius/diameter remain unresolved canon; `ADR-SYLVA-001` contains a separate proposal and must not be mistaken for approved world data.
- Do not infer planetary scale from the local patch.
- Blender is Z-up. glTF interchange is Y-up; importer must use the engine's standard glTF coordinate conversion rather than applying a second manual axis rotation.
- Mesh/curve transforms were validated at unit scale in Blender r5.

## Namespace classes

### Render / macro foundation

All owned scene objects use the `SYLVA_` namespace.

Important render families:
- `SYLVA_TERRAIN_*` — visible macro terrain proposal.
- `SYLVA_ROOT_PRIMARY_*` / `SYLVA_ROOT_SECONDARY_*` — diagnostic macro topology guides only.
- `SYLVA_PUERTO_*` — Puerto del Injerto blockout/proxy foundation.
- `SYLVA_BOSQUE_*` — Bosque de las Frases route-language blockout.
- `SYLVA_VESPER_*` — Cámara de VESPER encounter envelope/proxies only; no final VESPER asset.
- `SYLVA_TRAV_*` — diagnostic traversal guides, not final road meshes.

### Cámara de VESPER — canonical macro layout

The r5 contract intentionally invalidates the older single circular arena proxy. Canon requires **three terraces connected by wide roots**, with vertical movement through routes/anchors rather than surprise precision jumps.

Required visible macro-layout nodes:
- `SYLVA_VESPER_Terrace_00_ENTRY`
- `SYLVA_VESPER_Terrace_01_MIDDLE`
- `SYLVA_VESPER_Terrace_02_UPPER`
- `SYLVA_VESPER_TerraceConnector_00`
- `SYLVA_VESPER_TerraceConnector_01`
- `SYLVA_META_VESPER_ThreeTerraceLayout`

Measured r5 connector interfaces:
- Connector 00: 142.215 m long, 12.178° slope, 18 m visible width, 16 m collision width.
- Connector 01: 145.685 m long, 12.689° slope, 18 m visible width, 16 m collision width.
- Both declare `precision_jump_required=false`.

The removed legacy nodes must not be treated as valid r5 content:
- `SYLVA_VESPER_ProxyArenaFloor`
- `SYLVA_COL_VESPER_ArenaFloor`

### Collision interface

Prefix: `SYLVA_COL_`

Current r5 collision nodes (**12 total**):
- `SYLVA_COL_TERRAIN_Macro12km_LowRes_PROPOSAL`
- `SYLVA_COL_PUERTO_Deck`
- `SYLVA_COL_BOSQUE_CentralPad`
- `SYLVA_COL_ROUTE_00`
- `SYLVA_COL_ROUTE_01`
- `SYLVA_COL_ROUTE_02`
- `SYLVA_COL_ROUTE_03`
- `SYLVA_COL_VESPER_Terrace_00_ENTRY`
- `SYLVA_COL_VESPER_Terrace_01_MIDDLE`
- `SYLVA_COL_VESPER_Terrace_02_UPPER`
- `SYLVA_COL_VESPER_Connector_00`
- `SYLVA_COL_VESPER_Connector_01`

Importer policy:
1. Never display `SYLVA_COL_*` as final visible art.
2. Instantiate them as collision/debug interfaces according to engine policy.
3. Do not use visible high-detail geometry as collision merely because it exists.
4. r5 proxies validate presence and naming only; actual CharacterBody traversal is still pending.
5. VESPER terrace/connector collision must be tested with the real controller before any gameplay-pass claim.

### Root-kit integration sockets

Prefix: `SYLVA_SOCKET_`

These are placement interfaces to provider claim `CLM-SYLVA-PROC-NROOT-001`; this macro claim does **not** own the provider meshes.

Current socket contract:
- `SYLVA_SOCKET_PUERTO_EXIT_A1` → `SYL_ROOT_A1_STRAIGHT_08M`
- `SYLVA_SOCKET_PUERTO_MEMBRANE_C3` → `SYL_ROOT_C3_MEMBRANE_ANCHOR`
- `SYLVA_SOCKET_BOSQUE_APPROACH_A2` → `SYL_ROOT_A2_CURVE_12M`
- `SYLVA_SOCKET_BOSQUE_FORK_B1` → `SYL_ROOT_B1_FORK`
- `SYLVA_SOCKET_BOSQUE_RISE_A3` → `SYL_ROOT_A3_RISE_10M`
- `SYLVA_SOCKET_VESPER_APPROACH_A2` → `SYL_ROOT_A2_CURVE_12M`
- `SYLVA_SOCKET_VESPER_BUTTRESS_C1` → `SYL_ROOT_C1_BUTTRESS_07M`
- `SYLVA_SOCKET_VESPER_MEMBRANE_C3` → `SYL_ROOT_C3_MEMBRANE_ANCHOR`

Provider manifest:
`production/manifests/sylva/procedural/SYL_NEURAL_ROOT_KIT_001.yaml`

Importer/integrator must not treat these sockets as permission to duplicate provider meshes into this branch. Provider assets should be instanced/linked after PR #6 integration.

### Streaming metadata

Prefix: `SYLVA_STREAM_`

Current proposal:
- `SYLVA_STREAM_L3_X0Y0` … `SYLVA_STREAM_L3_X3Y3`: 16 local 3 km L3 cells.
- `SYLVA_STREAM_REGION_PUERTO_INJERTO`
- `SYLVA_STREAM_REGION_BOSQUE_FRASES`
- `SYLVA_STREAM_REGION_CAMARA_VESPER`

These are metadata interfaces, **not a commitment to a specific engine streaming backend**. Godot/Unreal implementation remains `ENGINE_TBD` until engine/runtime qualification.

## Import acceptance sequence

1. Recover the exact revision-5 GLB and `.blend` into a delivery checkout.
2. Verify exact GLB SHA-256 against the delivery/native receipt.
3. Run `validate_glb_contract.py <file.glb>` before engine import; r4/legacy arena exports must fail the r5 contract.
4. Import using the engine's normal glTF path with no manual global scale multiplier.
5. Confirm expected top-level/node names survived import.
6. Separate `SYLVA_COL_*` from visible render geometry.
7. Record `SYLVA_SOCKET_*` transforms for provider-module placement; do not bake provider meshes into this source.
8. Record `SYLVA_STREAM_*` metadata or equivalent importer map; do not silently discard without waiver.
9. Spawn the real project player/controller at Puerto.
10. Traverse Puerto → Bosque → Cámara de VESPER with normal controls and collision; no teleports/debug progression.
11. Specifically traverse all three VESPER terraces and both wide connectors; record slope, snagging, camera, fall and recovery behavior.
12. Record clearance, camera, collision, z-fighting, material and navigation defects.
13. Profile only on a declared hardware/preset; CPU/software render is not GPU qualification.

## Native receipt minimum

A runtime receipt must contain:
- exact GLB SHA-256;
- import timestamp;
- engine/version;
- source branch/commit;
- imported scene/resource path;
- scale check result;
- r5 named-node contract result;
- collision-node result;
- VESPER three-terrace traversal result;
- full Puerto → Bosque → VESPER traversal result;
- screenshots/logs/evidence refs;
- `passed: true|false` with explicit failure reasons.

## Current remote r5 artifact identity

Remote provider metadata only; not a recovered delivery receipt:
- `.blend`: 2,290,409 bytes; etag `2ccbc1ec2ffd854ae83b5cee197d16de`.
- GLB: 1,215,672 bytes; etag `9c288dd826d7cbc3331b849dda1590e5`.

## Gates still open

- `GATE-ART`: human visual review.
- `GATE-ENGINE`: actual Godot/Unreal import.
- runtime collision/traversal.
- HLOD/LOD implementation.
- target-hardware performance.
- recovered binary `.blend` + GLB in an integrator checkout per `docs/FLEET_COORDINATION.md` delivery gate.

A remote 3D Jutsu URL, successful remote GLB export, or beauty render does **not** close those gates.
