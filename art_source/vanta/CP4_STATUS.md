# VANTA CP4 — Modular Construction Kit Status

**World:** VANTA  
**Branch:** `art/world-vanta-001`  
**Remote Blender project:** `c82188b1-afdc-43f2-828a-5f0e98291f83`  
**Latest validated revision:** 4  
**Truth level:** `LOCALLY_VALIDATED_GEOMETRY` — not engine-qualified, not final-art approved.

## Scope closed in this checkpoint

CP4 now has two complementary layers:

1. **Representative vertical microset** built in Puerto de las Manos coordinates:
   - `VAN_KIT_CRANE_A`
   - `VAN_KIT_MAG_ANCHOR_A`
   - `VAN_KIT_DRYDOCK_RIB_A`
   - `VAN_KIT_STORM_SHELTER_A`
2. **Metric 4 m snap-kit** with reusable source modules:
   - `VAN_MOD_FLOOR_4M_A`
   - `VAN_MOD_WALL_SOLID_4M_A`
   - `VAN_MOD_WALL_SERVICE_4M_A`
   - `VAN_MOD_RAIL_4M_A`
   - `VAN_MOD_PIPE_TRAY_4M_A`
   - `VAN_MOD_BRACE_4M_A`
   - `VAN_MOD_STAIR_4M_A`
   - `VAN_MOD_ROOF_4M_A`
   - `VAN_MOD_PILLAR_4M_A`
   - `VAN_MOD_DOOR_4M_A`
   - `VAN_MOD_MAG_RAIL_4M_A`
   - `VAN_MOD_BULKHEAD_8M_A`

Each snap module carries four explicit socket empties, a render hierarchy, separate collision and an LOD1 proxy. Asset IDs remain Vanta-namespaced.

## Revision receipts

### Revision 3 — representative microset

Operation: `vanta-cp4-microset-002`

- 173 CP4-tagged objects created in the first microset pass.
- 77 crane objects.
- 19 magnetic-anchor objects.
- 35 drydock-rib objects.
- 31 storm-shelter objects.
- 11 calibration-board objects.
- 7 separate collision objects.
- 4 LOD1 proxies.
- Editable `.blend`: 6,202,289 B, etag `98e19338c29fbf9f5d061735ba229c21`.
- GLB: 4,382,328 B, etag `8ceb5655ec26a9992b382344c4e3e2d6`.

The first three-camera QA batch timed out at 300 s. The scene revision remained valid. A smaller isolated crane proof then succeeded:

- artifact `vanta_cp4_crane_proof.png`
- artifact id `c09519f9702b54ce7595e7803f0a35a5`
- 640×480
- 248,546 B

This proves render execution, not aesthetic approval. Direct art review remains open.

### Revision 4 — snap kit

Operation: `vanta-cp4-snapkit-001`

- 12 reusable metric modules.
- 48 explicit snap sockets.
- 12 module collision proxies.
- 12 module LOD1 proxies.
- 4 m declared grid.
- 711 total scene objects after commit.
- Editable `.blend`: 7,046,134 B, etag `7617263dce0f383746d5411614908b17`.
- GLB: 4,842,424 B, etag `0ed964937085dafbcb717b35aacc5163`.

Structural QA operation `vanta-cp4-structural-qa-001` validated all 16 CP4 asset IDs. There were:

- zero failed assets;
- zero non-unit render-mesh scales;
- zero materialless render meshes;
- zero accidental `.001/.002/.003` suffix drift;
- exactly four sockets on every snap module;
- at least one independent collision and one LOD1 proxy for every validated asset.

Revision-4 audit:

- 711 objects;
- 618 meshes;
- 18 materials;
- 21 collections;
- 9 cameras;
- 9 lights;
- 315 CP4-tagged objects total;
- 206 CP4 render meshes;
- 19 CP4 collision objects;
- 16 CP4 LOD1 proxies;
- 16 CP4 roots;
- 48 snap sockets;
- 10 calibration objects.

## CP4 gate disposition

**CP4 is now `LOCALLY_VALIDATED_GEOMETRY`**, not fully DONE under the global static-asset DoD.

Passed locally:

- deterministic metre scale;
- functional pivots/root hierarchy;
- representative modular geometry;
- 4 m snap contract;
- explicit sockets;
- separate collision proxies;
- explicit LOD1 proxies;
- material-role assignment;
- editable `.blend` persistence;
- portable GLB export;
- structural naming/scale QA;
- isolated render execution.

Still open before final DoD:

- human/direct visual art approval;
- UV/trim-sheet production validation;
- final PBR texture authoring;
- seam review in assembled engine test yard;
- actual target-engine snap/import test;
- collision traversal/playtest;
- close/mid/far review in production engine;
- triangle/draw/material/texture/memory cost on declared target hardware;
- HLOD/instancing runtime qualification.

## CP5 handoff

The next gate is intentionally narrow:

1. turn the existing calibration precursor into neutral + Vanta-light material boards;
2. establish the first trim/decal family for steel/rust/yellow paint/impact/weld/frost/grease;
3. apply that system to the four representative CP4 assets;
4. verify the microset in close/mid/far views;
5. only then propagate the material system to the wider Vanta registry.

Evidence source: `art_source/vanta/evidence/remote_blender_rev4.json`.
