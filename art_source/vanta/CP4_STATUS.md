# VANTA CP4 — Modular Construction Kit Status

**World:** VANTA  
**Branch:** `art/world-vanta-001`  
**Remote Blender project:** `c82188b1-afdc-43f2-828a-5f0e98291f83`  
**Latest validated revision:** 9  
**Truth level:** `EMPIRICALLY_QUALIFIED_GODOT_4_7_2_STATIC_IMPORT_COLLISION` — final art, full gameplay traversal and target-hardware performance remain open.

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

## Godot 4.7.2 empirical qualification

GitHub Actions run `34720473947`, job `103625283508`, on a real `ubuntu-24.04` hosted runner completed successfully after the harness typing defect from the preceding run was corrected without changing the Blender asset.

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

The 711→691 visual-mesh reduction is expected: the 20 former collision render meshes are now converted to collision-only bodies by the Godot importer.

## Current CP4 disposition

**Empirically qualified in Godot 4.7.2 validation runtime:**

- exact GLB transport/hash recovery;
- native PackedScene import;
- critical visual-name preservation;
- source-authored `_colonly` collision conversion;
- 20 static bodies / 20 collision shapes;
- one real physics raycast against the floor module;
- 4 m Blender snap assembly with seven zero-gap seam checks.

**Still open before global static-asset DoD:**

- full player-controller traversal and interaction playtest;
- production-engine decision (Godot validation is not an engine-selection claim);
- direct visual/art-direction approval;
- close/mid/far review in production renderer;
- measured tris/draws/texture residency/memory/GPU cost on declared target hardware;
- HLOD/instancing runtime qualification.

Evidence authority: `art_source/vanta/evidence/godot_rev9_native_qualification.json`.

## Revision 10 — bounded CharacterBody traversal

Revision 10 is a texture-payload repair; geometry and the revision-9 `_colonly` collision contract were intentionally left unchanged. The collision slice was nevertheless regression-tested in pinned Godot 4.7.2 with a real `CharacterBody3D` rather than only a ray query.

Two independent executions (GitHub Actions run `34722670811`, job `103631274506`, plus the Higgsfield Linux sandbox) reached the same bounded result on the CP4 test-yard floor:

- `COL_VAN_CP4_TEST_YARD_FLOOR` present with a non-null imported collision shape;
- capsule `CharacterBody3D` settled on the authored floor;
- target reached;
- 323 physics frames recorded on-floor;
- travel ratio `0.969267592149354` across the 12 m floor collider;
- no claim is made for the full VANTA route, interactions, combat, HLOD or target-hardware performance.

**CP4 truth after rev10:** `EMPIRICALLY_QUALIFIED_BOUNDED_CHARACTERBODY_TRAVERSAL_GODOT_4_7_2`. Static import/collision and the representative floor traversal are qualified; full gameplay traversal and performance remain open.

Evidence authority: `art_source/vanta/evidence/rev10_texture_engine_qualification.json`.
