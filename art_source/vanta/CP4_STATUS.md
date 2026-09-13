# VANTA CP4 — Modular Construction Kit Status

**World:** VANTA  
**Branch:** `art/world-vanta-001`  
**Remote Blender project:** `c82188b1-afdc-43f2-828a-5f0e98291f83`  
**Latest remote revision:** 11  
**Truth level:** `SOURCE_VALIDATED_REV11_DEDUP_AND_QA_ROUTE / GODOT_BOUNDED_CHARACTERBODY_REV10_QUALIFIED` — the rev11 10.2 km QA route is structurally validated in Blender/GLB, but native kilometre traversal is still pending manual CI promotion; final art and target-hardware performance remain open.

## Scope

CP4 contains a representative Puerto de las Manos vertical microset (`VAN_KIT_CRANE_A`, `VAN_KIT_MAG_ANCHOR_A`, `VAN_KIT_DRYDOCK_RIB_A`, `VAN_KIT_STORM_SHELTER_A`), 12 reusable 4 m modules, 48 snap sockets, separate collision proxies, LOD1 proxies and a linked Blender assembly yard.

## QA history that must remain visible

### Revision 4 — insufficient structural QA

Revision 4 passed roots/scales/materials/sockets/collision/LOD checks, but a later world-coordinate audit found a **P1 parent-inverse defect**: 205 CP4 render children had doubled representative X/Y translations. Revision-4 CP4 approval is superseded.

### Revision 5 — parent transform repair

`vanta-cp4-parent-fix-001` repaired all 205 affected render children. Exact guards pass for crane, anchor, rib, shelter and representative snap modules.

### Revision 6 — metric assembly test yard

The first instancer failed its own seam assertion before commit and was discarded. `vanta-cp4-test-yard-002` then passed 19 instance markers, 76 linked render meshes, 7 seam checks and **0.000 m maximum floor gap**.

### Revision 8 — native import exposed the collision contract gap

A real GitHub-hosted Ubuntu runner recovered the exact revision-8 GLB and imported it in pinned **Godot 4.7.2 stable**. Geometry/name/material-surface import passed, but the runtime contained **0 `CollisionObject3D`**. The Blender collision guides existed but their `COL_VAN_*` names had no Godot import semantics. This negative receipt is why CP4 was not declared DONE at revision 8.

Rev8 native import receipt scope:

- GLB SHA256 `18318e0fdae3757b07054e0b376c8222b0adfd281f24d0ba57582010bd039792`;
- 711 mesh instances / 711 mesh surfaces;
- all seven critical visual names present;
- **0 runtime collision objects**.

### Revision 9 — source-level Godot collision contract

`vanta-rev9-godot-collision-contract-001` renamed the 20 simple collision meshes to the `_colonly` convention while preserving their original semantic names in Blender metadata. The two QA-only AREA lights were converted to POINT lights for portable glTF export.

Revision-9 source:

- `.blend`: 8,178,521 B · etag `9cc8c4c8c79e887ce9ef7364710dcbf4` · SHA256 `11b60150409718182cac44d190444f912064e7ff4431f444cca76effbdd0c66b`;
- GLB: 5,993,560 B · etag `0e82911eefab809ede430a231ae9953b` · SHA256 `d4cb8154802e7713b9887328431bd27dfdbc6ba6bec07e790fd0b99befef3258`;
- GLB: 701 meshes / 832 nodes / 20 materials / 13 images;
- exactly 20 `_colonly` nodes before import.

## Godot 4.7.2 empirical qualification through revision 10

GitHub Actions run `34720473947`, job `103625283508`, on a real `ubuntu-24.04` hosted runner qualified the rev9 native collision contract.

Native Godot receipt:

- engine: `4.7.2-stable (official)`;
- required visual names missing: **0**;
- visual `MeshInstance3D`: **691**;
- visual mesh surfaces: **691**;
- `StaticBody3D`: **20**;
- non-null `CollisionShape3D`: **20**;
- floor physics raycast: **PASS**;
- raycast collider: `COL_VAN_MOD_FLOOR_4M_A`;
- all 20 semantic collision-body names recovered by the importer.

The 711→691 visual-mesh reduction is expected: the 20 former collision render meshes are converted to collision-only bodies by the Godot importer.

### Revision 10 — bounded CharacterBody traversal

Revision 10 retained the revision-9 geometry/collision contract and regression-tested it in pinned Godot 4.7.2 with a real `CharacterBody3D` rather than only a ray query.

Two independent executions (GitHub Actions run `34722670811`, job `103631274506`, plus the Higgsfield Linux sandbox) reached the same bounded result on the CP4 test-yard floor:

- `COL_VAN_CP4_TEST_YARD_FLOOR` present with a non-null imported collision shape;
- capsule `CharacterBody3D` settled on the authored floor;
- target reached;
- 323 physics frames recorded on-floor;
- travel ratio `0.969267592149354` across the 12 m floor collider.

**CP4 truth through rev10:** `EMPIRICALLY_QUALIFIED_BOUNDED_CHARACTERBODY_TRAVERSAL_GODOT_4_7_2`.

Evidence authority: `art_source/vanta/evidence/rev10_texture_engine_qualification.json`.

## Revision 11 — lossless source dedup + kilometre-scale QA traversal spine

Mutation `vanta-rev11-dedup-qa-traversal-spine-003` advanced the remote source from rev10 to rev11 after two prior attempts correctly failed before commit on guard defects. Those failed operations are negative execution history, not revisions.

Exact remote rev11 provider checkpoint currently available:

- `.blend`: **10,162,134 B** · etag `12c55a03e326a0a3e4df352875d065dc`;
- GLB: **8,823,976 B** · etag `86720d1b76c01894746cbded53510bc6`;
- binary SHA256 recovery for rev11 remains pending a permitted manual native canary; do not infer it from etag.

### Source datablock dedup

The dedup is deliberately narrower than the complete duplicate-geometry inventory. It only relinks repetitive/procedural families when local geometry, topology, smoothing, material slots, UV contents and semantic mesh attributes match exactly. Editor-only selection attributes are ignored. FERRUM, DRAV, terrain cells, shape-key meshes and unsupported/cross-semantic users are excluded.

Measured result:

- used mesh datablocks before: **635**;
- after dedup: **412**;
- after adding the two QA-spine meshes: **414**;
- objects relinked to shared geometry: **255**;
- dedup groups committed: **33**;
- redundant mesh datablocks removed: **223**.

Representative linked families after commit:

- iron sleepers: **44×** one mesh;
- crane braces: **28×**;
- modular stair steps: **20×**;
- ring hull ribs: **18×**;
- crane ladder rungs: **14×**;
- modular rail posts: **12×**;
- route pylons: **11×**.

This is a source-structure optimization. It does **not** by itself claim lower Godot draw calls, HLOD qualification or target-GPU performance.

### QA traversal spine

The old macro route consisted of 11 visual pylons whose bases were all at `z=0`, while the proxy terrain beneath them stepped through top elevations of approximately `+12`, `-4`, `+8` and `+20 m`. It was therefore not a valid traversable surface.

Rev11 adds an explicitly diagnostic route:

- visible `QA_VAN_ROUTE_SPINE`;
- collision-only `COL_VAN_QA_ROUTE_SPINE_colonly`;
- collection `24_QA_TRAVERSAL_SPINE`;
- `CAM_QA_ROUTE_SPINE`;
- length **10,200 m**;
- width **12 m**;
- sampling step **50 m**;
- 410 vertices / 204 quads on both visual and collision meshes;
- maximum authored diagnostic slope **4.573921259900861°**;
- 200 m ramps bridge the macro proxy terrain discontinuities;
- the 11 route pylons now rest on the QA profile with base elevations `[13, 5, -3, -3, -3, 3, 9, 9, 9, 15, 21] m`.

Precommit temporary GLB structural validation found **626 meshes / 807 nodes / 20 materials / 13 images / 21 `_colonly` nodes**, including both QA route objects. The committed provider GLB has its own byte size above and must not be conflated with the temporary export bytes.

**Important truth boundary:** this spine is `QA_ONLY_NOT_LEVEL_ART`. It tests kilometre-scale collision/traversal and coordinate behavior; it is not the final Puerto→Anillo authored route.

### Native rev11 traversal status

`main` commit `26ae20f5d1b47d1efa0d54b20124ed93cbc0b43e` quarantines automatic gauntlet triggers to `workflow_dispatch` for cost control. The connected GitHub surface in this session can inspect and rerun existing jobs but cannot create a new manual dispatch. Therefore the 10.2 km CharacterBody canary is **not executed yet** and is classified:

`ENV_BLOCKED_BY_MANUAL_CI_PROMOTION_POLICY`

Do not substitute the rev10 12 m traversal receipt for rev11.

## Current CP4 disposition

**Empirically qualified:**

- 4 m modular snap assembly and zero-gap yard seams;
- native rev9 static collision conversion;
- rev10 bounded 12 m CharacterBody traversal.

**Source/GLB validated in rev11:**

- guarded lossless datablock sharing for repetitive families;
- 10.2 km diagnostic visual/collision spine;
- 21st `_colonly` route collider in structural GLB validation;
- macro pylon contact correction against the QA profile.

**Still open:**

- manual Godot 4.7.2 canary on the exact committed rev11 GLB for the 10.2 km spine;
- authored final VANTA route and interaction/combat traversal;
- direct visual/art-direction approval;
- HLOD/runtime-instancing qualification;
- measured frame time, draw calls, residency, memory and GPU cost on declared target hardware;
- final engine selection.

Evidence authority: `art_source/vanta/evidence/rev11_dedup_route_visual_portability.json`.
