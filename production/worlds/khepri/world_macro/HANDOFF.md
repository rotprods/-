# KHEPRI World Macro — recoverable handoff

AGENT: `AGENT-KHEPRI-WMACRO-001`  
SESSION: `SESSION-20260912-KHEPRI-001`  
CLAIM: `CLM-KHEPRI-WMACRO-001`  
BRANCH: `art/world-khepri-001`  
PR: `#8` draft  
QUALIFIED MAIN: `be6162064ceb475d5f7a7aa1388a7873f25d3258`  
MANIFEST-LOCKED GREEN HEAD BEFORE DOC SYNC: `8022197ec42eae9764d3dab2fcda311d8acad5e2`  
EXACT PR GAUNTLET: `34722654514` SUCCESS  
MASTER 3D PROJECT: `040f0c45-83a7-483c-9ee7-1e31c640a587` rev `4`  
COLD 3D PROJECT: `4c01fdbb-7093-4229-9a49-8237583280bc` rev `3`  
CLAIM STATUS: **KEEP / REVIEW**

## NORTH STAR
Deliver KHEPRI `WORLD_MACRO / PLANETARY_FOUNDATION` as a reproducible metre-scale Blender foundation preserving canon, separating L0/L1/L2 scale, exposing stable cross-domain interfaces, and never promoting proposal/blockout values to canon/final art without their gates.

## CURRENT TRUTH
This is a deterministic, structurally qualified world-macro blockout/foundation. It is **not KHEPRI DONE**, not final AAAA art, not target-engine-integrated production terrain and not human-art-approved.

## MASTER R4
- 77 objects / 6 mesh datablocks / 5 materials / 1 route curve.
- 5,697 unique mesh vertices / 11,092 unique triangles.
- Terrain: `6400 × 4800 × 228.805 m`.
- 1.85 m human QA reference.
- 32 heliostat panels → one shared panel mesh.
- 32 heliostat masts → one shared mast mesh.
- Whole-scene `.blend`: `1,379,495 B`, etag `6d81d2c81e19a841056f018926e32944`.
- Whole-scene GLB: `822,272 B`, etag `40d610951c4f0d8d3d83c7d4e67519dc`.

## DEFECTS CORRECTED BY GAUNTLET
1. Empty 3D Jutsu project had no World datablock → generator bootstraps it.
2. 32 duplicated mast mesh datablocks → one shared mast mesh.
3. Camera default `clip_end=1000 m` clipped kilometre-scale proof → overview 12 km / gameplay 8 km clip contracts.
4. Human QA guide outside gameplay frame → positioned 30 m on view axis, ~84.7 px at 720p.
5. Four-point route ribbon crossed terrain → deterministic 576-point terrain-conforming route at ~7 m clearance.
6. Raw mesh fingerprint falsely failed from UV-sphere index ordering → geometry-semantic fingerprint separates index order from actual shape/topology-by-coordinate.
7. Split L1 export leaked authoring-only `Z=-1100 m` preview offset → export-time recenter + exact restoration.
8. GLB byte hashes differ across independent Blender serialization → normalized glTF JSON + Blender semantic fingerprint used for deterministic semantic gate.
9. Parallel-shard CI manifest drift → fleet/main reconciliation; exact PR Gauntlet now green.

## R4 ROUTE / CONTACT / PORTABILITY
Route receipt `R4_ROUTE_CLEARANCE.json`:
- 576 points / 575 segments;
- target clearance 7 m;
- audited clearance `6.9963…7.0043 m`;
- maximum error `4.3 mm`;
- zero below-terrain samples.

Heliostat receipt `R4_HELIOSTAT_CONTACT.json`:
- mast-ground contact error approximately `−4…+4 μm`;
- panel center 6 m above mast top;
- minimum macro spacing 490 m;
- shared mesh instancing preserved.

Portability receipt `R4_PORTABILITY.json`:
- no external image dependency;
- no absolute image paths;
- no unsupported light types;
- no unused mesh/curve/material/camera/light datablocks;
- blockout materials remain portable Principled roles.

## TOPOLOGY GAUNTLET
Operation `khepri.topology.audit.r4.20260913` PASS:
- 68 mesh objects / 6 unique mesh datablocks;
- zero zero-area faces;
- zero zero-length edges;
- zero invalid face normals;
- every non-terrain mesh closed/manifold;
- terrain has exactly 280 boundary/non-manifold edges, the expected perimeter of an open 81×61 tile; explicit waiver references terrain tiling contract;
- route curve has 575 non-degenerate ~10 m segments;
- one material slot per mesh object.

This is blockout topology QA only; final UV/retopo/collision/LOD are separate gates.

## SPLIT EXPORT / STREAMING INTERFACE
`export_stream_units.py` + `R4_STREAM_SPLIT.json` prove separable portable packages without changing the master.

L1 orbital:
- standalone centered export;
- authoring offset `(0,0,-1100)` removed only during export, then restored;
- 1 object / 1 mesh / 1 material;
- `132,916 B` master and cold;
- normalized glTF JSON master/cold hash matches (`5600ba9e…`);
- no cameras or external URIs.

L2 macrocell:
- terrain + optical footprints + four route anchors;
- excludes QA route guide, human QA guide, cameras and lights;
- `553,012 B` master and cold;
- 69 nodes / 65 mesh objects / only 3 glTF meshes because instancing is preserved;
- normalized glTF JSON master/cold hash matches (`7c99bfe2…`);
- no external URIs.

This proves portable packaging boundaries, **not production engine streaming**.

## TERRAIN TILING CONTRACT
`terrain_tile_contract.py` + `R5_TERRAIN_TILING.json`:
- tile-local storage, global tangent-grid height evaluation;
- 81×61 grid at exact 80 m spacing;
- E/W/N/S border coordinate error `0 m`;
- border height error `0 m`;
- global-gradient normal mismatch max ~`1.48e-6°`;
- master terrain's 4,941 vertices match `KHP_TERRAIN_V1` within max ~`7.6 μm` / mean ~`0.81 μm` float residual.

Using the **proposed/non-canon** 5,224 km radius, a flat 6.4×4.8 km cell has ~1.53 m corner sagitta. Therefore this gate proves authoring continuity only; final spherical curvature/world partition remains unresolved.

## CI / FLEET
Fleet claim is active in `ops/fleet/registry.json` and protects exact KHEPRI paths/project IDs.

- Integration head `a4cb4d0b…` → PR Gauntlet `34722486412` SUCCESS.
- An accidental post-green receipt was removed rather than forcing another stale manifest.
- Manifest-locked tree `8022197e…` → PR Gauntlet `34722654514` SUCCESS.

Do not treat CI success as art, GPU or engine-import approval.

## VISUAL EVIDENCE
Fresh Eevee query `khepri.visual.fresh.r4.20260913` at 960×540:
- overview artifact `57acd2b85cc986ccb1f9ec5502b96b0a`, 403,017 B;
- gameplay artifact `c6bd87b88141e4955efd33a53416ef8b`, 424,972 B.

Machine framing/scale gates PASS. A browser-agent traversed both images for independent review but returned an empty structured result; classify as **NO_EVIDENCE**, not PASS/FAIL. Human/pixel GATE-ART remains open.

## BINARY PERSISTENCE BLOCKER — NARROWED
Provider r4 `.blend` and GLB remain recoverable. A browser workflow successfully downloaded both exact provider files, so provider egress itself is confirmed. Upload then stopped safely because:
- browser GitHub session was unauthenticated;
- no credentials were configured;
- browser download filesystem did not expose a reusable `file_uri` to the authenticated GitHub connector.

No GitHub files or branches were modified by that automation. `fleet_control.py delivery` can validate binaries once local but does not transport them. Current blocker is therefore **cross-tool private file handoff**, not asset absence.

## CANON / DECISIONS
- KHEPRI canon: Sahra / Andrómeda / Sínodo de Bronce / 0.63 g / 71 °C reference area / solar-glass desert + heliostats / RA-KHET.
- KHP-ADR-001 radius 5,224 km remains reversible PROPOSAL, not canon.
- Local tangent metre-scale cells replace any monolithic gameplay-planet mesh.
- `SHADE`, `GLASS_SEA`, `CRUCIBLE`, `RAKHET` remain cross-domain route interfaces, not final art ownership.
- Final architecture/materials/characters/fauna/vehicles/RA-KHET belong to separate claims.

## OPEN GATES
### P0 — BINARY_PERSISTENCE_TRANSPORT
Need repository-controlled or equivalent private storage of exact R4 `.blend` + GLB, local SHA256, native/import receipt, then fleet delivery gate.

### P1 — HUMAN_GATE_ART
Need human/pixel review of overview/gameplay and explicit defects/approval. Machine visual QA cannot substitute.

### DOWNSTREAM / OUTSIDE CURRENT DONE CLAIMS
- target-engine import/instantiate/traversal;
- production collision/navmesh;
- final UV/PBR/material library;
- final terrain/geology;
- final LOD/HLOD/world partition;
- target-hardware GPU budget;
- final planet curvature/canon radius.

## NEXT 3 ACTIONS
1. Bridge R4 `.blend`/GLB into repository-controlled private storage and execute local SHA256 + fleet delivery/native import gates.
2. Obtain human/pixel art review of R4 overview/gameplay; mutate only if defects fall inside world-macro ownership.
3. When those gates are resolved, decide `RELEASE` vs a narrowly defined follow-up claim; do not keep expanding world density under this foundation claim.

CLAIM STATUS: **KEEP / REVIEW**
