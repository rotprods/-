# SYLVA PRIME Macro — Engine Import Contract

Claim: `CLM-SYLVA-MACRO-001`  
Remote project: `05dce898-753d-4ff6-a4b0-31757dc868d8`  
Current validated Blender revision: **6**  
Node/import contract generation: **R5** (still valid in r6; r6 modifies terrain mesh data, not required IDs)  
Status: `BLOCKOUT / INTEGRATION CONTRACT`, not final art.

## 1. Coordinate / scale

- `1 Blender Unit = 1 metre`.
- Current local authored envelope: `12,000 × 12,000 m`, classification `PROPOSAL`.
- Physical Sylva radius/diameter are not approved canon; never infer them from the local patch.
- Blender source is Z-up; use normal glTF engine conversion rather than applying a second manual axis rotation.
- Mesh/curve transforms have unit scale in r6 QA.

## 2. Current terrain contract

Visible macro terrain:
- `SYLVA_TERRAIN_Macro12km_PROPOSAL`
- terrain model: `R6_BIOGEO_CAUSAL_MACRO_V1`
- render grid: 49×49 / 2,401 vertices.

Collision terrain:
- `SYLVA_COL_TERRAIN_Macro12km_LowRes_PROPOSAL`
- grid: 33×33 / 1,089 vertices.

Both use the same deterministic height function. R6 QA compared 289 shared coordinates: max/mean render↔collision height delta = **0 m**.

The terrain model contains six proposed root-bearing ridges and two proposed catchment depressions. These are production shaping hypotheses, not canonical tectonics/waterways.

## 3. Render / macro namespaces

Owned visible families:
- `SYLVA_TERRAIN_*`
- `SYLVA_ROOT_PRIMARY_*` / `SYLVA_ROOT_SECONDARY_*` — diagnostic macro topology only
- `SYLVA_PUERTO_*`
- `SYLVA_BOSQUE_*`
- `SYLVA_VESPER_*` — macro encounter/environment proxies only, no final VESPER
- `SYLVA_TRAV_*` — diagnostic traversal guides

All owned nodes must remain in the `SYLVA_` namespace.

## 4. Cámara de VESPER r5/r6 required layout

Required visible nodes:
- `SYLVA_VESPER_Terrace_00_ENTRY`
- `SYLVA_VESPER_Terrace_01_MIDDLE`
- `SYLVA_VESPER_Terrace_02_UPPER`
- `SYLVA_VESPER_TerraceConnector_00`
- `SYLVA_VESPER_TerraceConnector_01`
- `SYLVA_META_VESPER_ThreeTerraceLayout`

Measured connectors:
- 00: 142.215 m, 12.178°, 18 m visible / 16 m collision width
- 01: 145.685 m, 12.689°, 18 m visible / 16 m collision width
- both: `precision_jump_required=false`

Forbidden legacy arena nodes:
- `SYLVA_VESPER_ProxyArenaFloor`
- `SYLVA_COL_VESPER_ArenaFloor`

A GLB containing the legacy single-floor arena is not an r6-valid delivery.

## 5. Collision contract — 12 nodes

Prefix: `SYLVA_COL_`.

Required:
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

Policy:
1. never display collision proxies as final art;
2. instantiate/separate them using engine collision policy;
3. never substitute visible high-detail geometry as collision merely because it exists;
4. real CharacterBody traversal is required before collision PASS.

## 6. Neural-root provider sockets

Prefix: `SYLVA_SOCKET_`.

Provider claim: `CLM-SYLVA-PROC-NROOT-001` / PR #6. This branch owns placement sockets, **not** provider meshes.

- `SYLVA_SOCKET_PUERTO_EXIT_A1` → `SYL_ROOT_A1_STRAIGHT_08M`
- `SYLVA_SOCKET_PUERTO_MEMBRANE_C3` → `SYL_ROOT_C3_MEMBRANE_ANCHOR`
- `SYLVA_SOCKET_BOSQUE_APPROACH_A2` → `SYL_ROOT_A2_CURVE_12M`
- `SYLVA_SOCKET_BOSQUE_FORK_B1` → `SYL_ROOT_B1_FORK`
- `SYLVA_SOCKET_BOSQUE_RISE_A3` → `SYL_ROOT_A3_RISE_10M`
- `SYLVA_SOCKET_VESPER_APPROACH_A2` → `SYL_ROOT_A2_CURVE_12M`
- `SYLVA_SOCKET_VESPER_BUTTRESS_C1` → `SYL_ROOT_C1_BUTTRESS_07M`
- `SYLVA_SOCKET_VESPER_MEMBRANE_C3` → `SYL_ROOT_C3_MEMBRANE_ANCHOR`

Provider manifest: `production/manifests/sylva/procedural/SYL_NEURAL_ROOT_KIT_001.yaml`.

## 7. Streaming metadata

- 16 `SYLVA_STREAM_L3_X*Y*` local cells, currently 3 km proposals.
- `SYLVA_STREAM_REGION_PUERTO_INJERTO`
- `SYLVA_STREAM_REGION_BOSQUE_FRASES`
- `SYLVA_STREAM_REGION_CAMARA_VESPER`

These are portable metadata interfaces, not a decision to use a specific Godot/Unreal streaming backend.

## 8. Pre-import validator

Run:

```bash
python3 art_source/worlds/sylva_prime/macro/validate_glb_contract.py <recovered-r6.glb> --expected-sha256 <exact-sha>
```

The validator contract is `CLM-SYLVA-MACRO-001/R5`; its node requirements remain the current r6 requirements. Synthetic adversarial self-test passes 7/7, including rejection of an r4 single-floor export. The exact r6 GLB still needs recovery and execution against its real SHA-256.

## 9. Native acceptance sequence

1. Recover exact r6 `.blend` + GLB into an integrator/delivery checkout.
2. Bind SHA-256 to the recovered GLB.
3. Run the GLB contract validator.
4. Import through the engine's standard glTF path with no manual global scale multiplier.
5. Verify required node IDs survived import.
6. Split `SYLVA_COL_*` from visible geometry.
7. Preserve/read `SYLVA_SOCKET_*` and `SYLVA_STREAM_*` metadata or document an explicit conversion.
8. Spawn the real project controller at Puerto.
9. Traverse Puerto → Bosque → Cámara de VESPER with normal controls, no teleport/debug progression.
10. Attack Route 03 specifically: measured guide grade **15.079°**.
11. Traverse all three VESPER terraces and both connectors.
12. Record snagging, falls, camera obstruction, collision, z-fighting, scale/material defects.
13. Profile only on declared target hardware/preset.

## 10. Current remote r6 identity

Provider metadata, **not recovered delivery proof**:
- `.blend`: 2,348,647 bytes; etag `f82350b275ed699a790d7977be3a1ee1`.
- GLB: 1,299,444 bytes; etag `896ae5e1b86cc5874f008872c05235a7`.

## 11. Open gates

- binary recovery: `ENV_BLOCKED` in current sandbox;
- human `GATE-ART`: pending;
- engine import: not run;
- runtime traversal/collision: not run;
- LOD/HLOD: not implemented;
- target-hardware performance: blocked;
- planetary scale: proposal pending decision.

Remote export success, render signal or a provider URL does not close these gates.
