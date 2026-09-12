# VANTA CP4 — Modular Construction Kit Status

**World:** VANTA  
**Branch:** `art/world-vanta-001`  
**Remote Blender project:** `c82188b1-afdc-43f2-828a-5f0e98291f83`  
**Latest validated revision:** 8  
**Truth level:** `LOCALLY_VALIDATED_GEOMETRY_AND_BLENDER_ASSEMBLY` — not engine-qualified, not final-art approved.

## Scope

CP4 contains:

- representative Puerto de las Manos vertical microset:
  - `VAN_KIT_CRANE_A`
  - `VAN_KIT_MAG_ANCHOR_A`
  - `VAN_KIT_DRYDOCK_RIB_A`
  - `VAN_KIT_STORM_SHELTER_A`
- 12 reusable metric modules on a declared 4 m grid;
- 48 explicit snap sockets;
- separate collision proxies;
- LOD1 proxies;
- linked Blender assembly/test yard.

## Important correction to revision-4 QA

Revision 4 initially passed structural checks for roots, scales, materials, sockets, collision and LOD. A later world-coordinate audit found that this was insufficient: **205 CP4 render children had been parented without preserving their intended world transform**, doubling representative X/Y translations.

Example before fix:

- `VAN_CRANE_BASE` local = `[-5600,-970,4]`
- world = `[-11200,-1940,4]`

This was classified as a **P1 geometry/pipeline defect**. Revision-4 CP4 approval is therefore superseded.

### Revision 5 — parent transform repair

Operation `vanta-cp4-parent-fix-001` repaired all 205 affected render children and added hard coordinate guards.

Representative guards now pass exactly:

- crane base `[-5600,-970,4]`
- magnetic anchor base `[-5200,1100,1.2]`
- drydock pillar `[-5480,-672,12]`
- shelter body `[-5550,430,3.2]`
- floor module deck `[-5480,520,0.22]`
- solid wall panel `[-5468,520,2]`
- stair first step `[-5481.8,544,0.2]`

Revision 5 source:

- `.blend` 7,032,696 B · etag `30a2b0a629c7b82513198049b65b4a31`
- GLB 4,822,424 B · etag `dc1ea5e5b1c5deadfe7237151ec826f5`

### Revision 6 — metric assembly test yard

The first test-yard attempt failed its own seam assertion before commit because its instancer introduced double pitch. It was discarded rather than accepted.

Corrected operation `vanta-cp4-test-yard-002` then passed:

- 19 module-instance markers;
- 76 linked render meshes;
- 6 assembled floor tiles;
- 7 deterministic seam checks;
- **maximum measured floor gap: 0.000 m**;
- no off-grid instance roots.

This validates the 4 m contract **inside Blender only**. It does not qualify target-engine snap/import or gameplay collision.

Revision 6 source:

- `.blend` 7,421,204 B · etag `538aed8fd6603a40cfc8a8f2b21b1621`
- GLB 5,375,388 B · etag `85b835bfbdd33cd862c0e03251ba4fdf`

### Revision 8 regression audit

`vanta-rev8-final-audit-001` confirms that later CP5 work did not regress CP4:

- all seven coordinate guards still exact;
- 205 corrected parented render children remain valid;
- all seven test-yard seam gaps remain 0 m;
- test-yard state remains `LOCALLY_ASSEMBLED`.

Render execution proof also passed at revision 8:

- `vanta_cp4_test_yard.png`
- artifact `f2ce32a87e098470ed00328fef4cbbb2`
- 640×480
- 248,872 B

This proves render execution for the assembled 76-mesh yard. Direct aesthetic approval remains open.

## Current CP4 disposition

**Passed locally:**

- metric scale and representative world-coordinate guards;
- root/pivot hierarchy after the rev5 repair;
- modular render geometry;
- 4 m grid contract;
- 48 explicit sockets;
- separate collision proxies;
- explicit LOD1 proxies;
- applied scale/material/UV structural checks;
- deterministic Blender assembly with zero measured floor seams;
- editable `.blend` persistence;
- GLB export existence;
- isolated render execution.

**Still open before global DoD:**

- direct/human visual art approval;
- target-engine snap/import test;
- engine collision traversal/playtest;
- close/mid/far review in production engine;
- engine material semantics;
- measured tris/draws/materials/textures/memory/GPU cost on declared target hardware;
- HLOD/instancing runtime qualification.

GLB export currently emits warnings for unsupported Blender AREA lights and, after CP5, sampler/material-node behavior. These warnings are tracked as engine-portability blockers, not ignored.

Current evidence: `art_source/vanta/evidence/remote_blender_rev8.json`.
