# SYLVA PRIME Macro — Engine Import Contract

Claim: `CLM-SYLVA-MACRO-001`  
Remote source: Higgsfield 3D Jutsu project `05dce898-753d-4ff6-a4b0-31757dc868d8`, validated revision `4`  
Status: `BLOCKOUT / INTEGRATION CONTRACT`, not final art.

## Purpose

This contract removes importer ambiguity before the r4 GLB enters Godot/Unreal. It does **not** claim runtime import has passed. It defines deterministic naming and classification so render geometry, collision interfaces, streaming metadata and provider sockets can be separated without heuristics.

## Coordinate / scale contract

- Blender source uses metric units: `1 Blender Unit = 1 metre`.
- Current local authored envelope is `12,000 × 12,000 m` and classified `PROPOSAL`.
- Physical Sylva Prime radius/diameter remain `UNKNOWN_BLOCKED`.
- Do not infer planetary scale from the local patch.
- Blender is Z-up. glTF interchange is Y-up; importer must use the engine's standard glTF coordinate conversion rather than applying a second manual axis rotation.
- Mesh/curve transforms were validated at unit scale in Blender r4.

## Namespace classes

### Render / macro foundation

All owned scene objects use the `SYLVA_` namespace.

Important render families:
- `SYLVA_TERRAIN_*` — visible macro terrain proposal.
- `SYLVA_ROOT_PRIMARY_*` / `SYLVA_ROOT_SECONDARY_*` — diagnostic macro topology guides only.
- `SYLVA_PUERTO_*` — Puerto del Injerto blockout/proxy foundation.
- `SYLVA_BOSQUE_*` — Bosque de las Frases route-language blockout.
- `SYLVA_VESPER_*` — Cámara de VESPER envelope/proxies only; no final VESPER asset.
- `SYLVA_TRAV_*` — diagnostic traversal guides, not final road meshes.

### Collision interface

Prefix: `SYLVA_COL_`

Current r4 collision nodes:
- `SYLVA_COL_TERRAIN_Macro12km_LowRes_PROPOSAL`
- `SYLVA_COL_PUERTO_Deck`
- `SYLVA_COL_BOSQUE_CentralPad`
- `SYLVA_COL_VESPER_ArenaFloor`
- `SYLVA_COL_ROUTE_00`
- `SYLVA_COL_ROUTE_01`
- `SYLVA_COL_ROUTE_02`
- `SYLVA_COL_ROUTE_03`

Importer policy:
1. Never display `SYLVA_COL_*` as final visible art.
2. Instantiate them as collision/debug interfaces according to engine policy.
3. Do not use visible high-detail geometry as collision merely because it exists.
4. r4 proxies validate presence and naming only; actual CharacterBody traversal is still pending.

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

These are metadata interfaces, **not a commitment to a specific engine streaming backend**. Godot/Unreal implementation remains `ENGINE_TBD` until EXO-012 / runtime qualification.

## Import acceptance sequence

1. Verify exact GLB bytes against the delivery receipt/native receipt hash.
2. Run `validate_glb_contract.py <file.glb>` before engine import.
3. Import using the engine's normal glTF path with no manual global scale multiplier.
4. Confirm expected top-level/node names survived import.
5. Separate `SYLVA_COL_*` from visible render geometry.
6. Record `SYLVA_SOCKET_*` transforms for provider-module placement; do not bake provider meshes into this source.
7. Record `SYLVA_STREAM_*` metadata or equivalent importer map; do not silently discard without waiver.
8. Spawn the real project player/controller at Puerto.
9. Traverse Puerto → Bosque → VESPER with normal controls and collision; no teleports/debug progression.
10. Record clearance, camera, collision, z-fighting, material and navigation defects.
11. Profile only on a declared hardware/preset; CPU/software render is not GPU qualification.

## Native receipt minimum

A runtime receipt must contain:
- exact GLB SHA-256;
- import timestamp;
- engine/version;
- source branch/commit;
- imported scene/resource path;
- scale check result;
- named-node contract result;
- collision-node result;
- traversal result;
- screenshots/logs/evidence refs;
- `passed: true|false` with explicit failure reasons.

## Gates still open

- `GATE-ART`: human visual review.
- `GATE-ENGINE`: actual Godot/Unreal import.
- runtime collision/traversal.
- HLOD/LOD implementation.
- target-hardware performance.
- recovered binary `.blend` + GLB in an integrator checkout per `docs/FLEET_COORDINATION.md` delivery gate.

A remote 3D Jutsu URL, successful remote GLB export, or beauty render does **not** close those gates.
