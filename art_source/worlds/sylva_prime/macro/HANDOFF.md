# HANDOFF — SYLVA PRIME MACRO FOUNDATION R11

AGENT: `AGENT-SYLVA-MACRO-01`  
SESSION: `20260912-SYLVA-MACRO-001`  
CLAIM: `CLM-SYLVA-MACRO-001`  
BRANCH: `art/world-sylva-prime-macro-001`  
LINEAR: `ROT-117`  
DRAFT PR: `#3`  
PRIMARY BLENDER: `05dce898-753d-4ff6-a4b0-31757dc868d8` @ **revision 11**  
NORTH STAR: reproducible metre-scale macro/regional foundation for SYLVA PRIME with explicit ownership, physical causality and recoverable integration contracts.

## CURRENT TRUTH

- checkpoint: `WAVE1I_CONTRACT_METADATA_R11`;
- primary scene source + portable GLB exist remotely;
- source technical QA: PASS at blockout/interface level;
- r9 route collision is historical failed checkpoint; r10 fixes it;
- r11 only normalizes metadata, no geometry delta from r10;
- human `GATE-ART`: PENDING;
- native engine import/traversal: NOT_RUN / environment-blocked here;
- provider root kit: NOT_READY due pivot + manifest gate;
- planetary Option C: proposal only;
- claim remains `KEEP / CHECKPOINT`.

## OWNERSHIP BOUNDARY

### This claim owns
- causal macro terrain and local metric world foundation;
- canonical region placement/spatial composition;
- diagnostic macro root topology;
- terrain-aware navigation centerlines;
- macro collision/streaming interfaces;
- VESPER macro encounter layout;
- root-kit **consumer sockets/support map**;
- reversible planet-scale decision artifacts.

### PR #6 owns
`CLM-SYLVA-PROC-NROOT-001`:
- reusable A1/A2/A3/B1/B2/C1/C2/C3 meso root module geometry;
- provider generator, callus surfaces, module collisions/material interfaces.

This branch contains **zero provider module meshes**.

## BUILD LINEAGE

1. `generate_sylva_macro.py`
2. `add_sylva_macro_interfaces.py`
3. `add_vesper_three_terraces.py`
4. `refine_macro_terrain_r6.py`
5. `apply_socket_consumer_contract_r7.py`
6. `apply_socket_support_map_r8.py`
7. `build_terrain_aware_routes_r10.py`
8. r11 metadata-only normalization (`SYLVA_NAV_R10`, `SYLVA_SOCKET_CONSUMER_V1`).

## WHAT CHANGED AFTER R6

### R7 — provider pivot blocker
Read-only audit of provider Blender project `43cf2b06-c47f-4ccd-ac34-76e9a585225a` r4 found object origins unsuitable for deterministic instancing: sampled origin→geometry-center offsets mostly 9–17.55 m. Only sampled C2 terrace callus was centered.

Persistent provider request: PR #6 comment `5648741376`.

Consumer contract locked:
- `+X` forward;
- `+Z` up;
- metres;
- scale 1;
- provider instances = 0;
- provider geometry copy = forbidden;
- transforms frozen until provider pivot normalization.

### R8 — semantic support map
All eight sockets now declare intended support object/role, but **zero transforms were snapped**. This prevents implicit placement guesses while preserving integration intent.

Support map: `SYLVA_SOCKET_SUPPORT_MAP_V1`.

### R9 — failed route-collision attempt
Terrain-aware centerlines were introduced, but the first collision ribbons had invalid side/end-cap topology and glTF emitted `mesh not valid` warnings.

R9 is **not deliverable** and is retained as failure evidence.

### R10 — valid terrain-aware navigation
Four stable route IDs are preserved and conform to r6 terrain using A* slope-weighted routing.

Total: **8,898.294 m**.

- leg00: 1,963.093 m / max 18.490°;
- leg01: 2,382.483 m / max 15.131°;
- leg02: 2,188.103 m / max 7.285°;
- leg03: 2,364.615 m / max 20.530°.

Collision ribbons are now closed manifold:
- 00: 28 verts / 26 faces;
- 01: 36 / 34;
- 02: 32 / 30;
- 03: 36 / 34;
- all: 0 nonmanifold edges, 0 degenerate faces.

### R11 — metadata consistency
No geometry changed.

Scene now declares:
- navigation `SYLVA_NAV_R10`;
- route profile `BALANCED_FOOT_TERRAIN_AWARE_R10`;
- collision `MANIFOLD_RIBBON_R10`;
- consumer contract `SYLVA_SOCKET_CONSUMER_V1`;
- support map `SYLVA_SOCKET_SUPPORT_MAP_V1`.

## R11 RECEIPTS

Scene:
- objects 151;
- meshes 91;
- curves 12;
- ~19,928 triangles;
- collision nodes 12;
- streaming cells/envelopes 16/3;
- sockets 8;
- VESPER terraces/connectors 3/2;
- provider meshes 0;
- final-scope violations 0;
- namespace/unit-scale violations 0.

Remote artifacts:
- `.blend`: 2,382,689 B / etag `095b96cc5dfca24bb086ac8b7b315d17`;
- GLB: 1,325,280 B / etag `5da3def12f2919b530bf6b4fc738a0e9`.

Master render smoke:
- 320×180;
- 90,993 B;
- mean RGB ~0.32439;
- variance ~0.06411;
- nonblank true.

This is not human art approval.

## GLB CONTRACT

Use `validate_glb_contract_r10.py` for recovered current GLB bytes.

The validator checks node/scope contracts and decodes the route-collision accessors to require closed-manifold, non-degenerate triangles.

Equivalent-logic synthetic gauntlet: **10/10 PASS**. `qa/GLB_CONTRACT_SELFTEST_R10.json` records truth boundaries.

Actual r11 GLB SHA/topology validation remains `ENV_BLOCKED_BINARY_RECOVERY` in this sandbox.

## BLOCKERS

### BLOCK-SYLVA-001 — planetary scale
Option C (1.20 R⊕) remains proposal. Orbital project `c796230b-0463-4e17-9446-2e746c5c4933` stays EMPTY r0 until fleet registry includes it.

### BLOCK-SYLVA-002 — target engine/hardware
No final LOD/HLOD/performance claim until engine + hardware/preset are qualified.

### BLOCK-SYLVA-003 — binary/native execution
Current sandbox cannot recover signed provider binaries or install pinned Godot through its network. Classify `ENV_BLOCKED`, not asset FAIL.

### BLOCK-SYLVA-004 — root-kit provider readiness
PR #6 must supply:
- valid manifest;
- normalized per-asset pivots/anchors;
- documented basis;
- render/collision anchor parity.

Do not instantiate provider modules until then.

## FLEET STATE

- published main at latest checked checkpoint: `f78bfdc8bd7b2f6ab52b45d39babcc1589ab3918`;
- producer ACK: issue #7 `5648367024`;
- orbital project registration request: `5648418266`;
- latest registry read before r7 still `reserved / ack:null`;
- producer does not edit `ops/fleet/registry.json`.

## NEXT 3 ACTIONS

1. RESYNC `main`, fleet registry and PR #6. If provider fixes pivots/manifest, read-only audit first, then consume modules through sockets; never copy ad hoc.
2. On an artifact-enabled runtime, recover exact r11 `.blend`/GLB, bind SHA-256, run `validate_glb_contract_r10.py`, import into pinned Godot and traverse all four legs + VESPER terraces with normal controls.
3. Human-review r11 composition/readability before adding microterrain/material/foliage density. Convert feedback into atomic claims.

CLAIM STATUS: `KEEP / CHECKPOINT`
