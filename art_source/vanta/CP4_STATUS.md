# VANTA CP4 — Modular Construction Kit Status

**World:** VANTA  
**Branch:** `art/world-vanta-001`  
**Remote Blender project:** `c82188b1-afdc-43f2-828a-5f0e98291f83`  
**Latest remote revision:** 11  
**Truth level:** `EMPIRICALLY_QUALIFIED_REV11_NATIVE_KILOMETRE_QA_TRAVERSAL_AND_MESH_SHARING` — the QA-only 10.2 km collider has passed native Godot 4.7.2 traversal/precision testing and source mesh sharing survives import. Final authored route, HLOD, gameplay interactions and target-GPU performance remain open.

## Scope

CP4 contains the representative Puerto de las Manos microset, 12 reusable 4 m modules, 48 snap sockets, collision proxies, LOD1 proxies, linked assembly yard, and the rev11 QA traversal spine used only for kilometre-scale collision/precision qualification.

## Preserved QA history

- **rev4:** structural checks later proved insufficient; 205 CP4 render children had doubled representative X/Y translations.
- **rev5:** `vanta-cp4-parent-fix-001` repaired those 205 parent/inverse defects.
- **rev6:** 19 assembly markers / 76 linked render meshes; seven seam checks; **0.000 m max floor gap**.
- **rev8:** exact GLB imported to Godot but produced **0 runtime collision objects**. This negative receipt remains preserved.
- **rev9:** 20 source collision meshes received `_colonly`; native Godot 4.7.2 produced **20 StaticBody3D + 20 CollisionShape3D** and a real floor raycast PASS.
- **rev10:** real capsule `CharacterBody3D` crossed the bounded yard floor; target reached, 323 on-floor physics frames, travel ratio `0.969267592149354`.

Rev10 evidence authority: `art_source/vanta/evidence/rev10_texture_engine_qualification.json`.

## Revision 11 exact checkpoint

Mutation: `vanta-rev11-dedup-qa-traversal-spine-003`.

Exact recovered binaries:

- `.blend`: **10,162,134 B** · SHA256 `3e60d536e7a38220935775fde9f2505f12adbf42451dcdbcaa87d9054645d899` · etag `12c55a03e326a0a3e4df352875d065dc`;
- GLB: **8,823,976 B** · SHA256 `a3ebb39f54d41e732c2ee343961cba43d85a2ced8a36c9d35306142443c36536` · etag `86720d1b76c01894746cbded53510bc6`.

### Guarded lossless source sharing

The relink guard requires identical local geometry, topology, smoothing, material slots, UV contents and supported semantic attributes. Editor-only selection attributes are ignored. FERRUM, DRAV, terrain cells, shape-key meshes, unsupported attributes and cross-semantic consumers are excluded.

Measured source result:

- used mesh datablocks: **635 → 412** after dedup;
- **414** after the two QA-route meshes are added;
- objects relinked: **255**;
- committed dedup groups: **33**;
- redundant mesh datablocks removed: **223**;
- representative sharing: sleepers 44×, crane braces 28×, modular stair steps 20×, ring hull ribs 18×, ladder rungs 14×, route pylons 11×.

### Native sharing survives import

Exact rev11 GLB instantiated in pinned **Godot 4.7.2-stable**:

- `MeshInstance3D`: **692**;
- mesh surfaces: **692**;
- unique mesh resources: **605**;
- unique material resources: **36**;
- `StaticBody3D`: **21**;
- non-null `CollisionShape3D`: **21**;
- `COL_VAN_QA_ROUTE_SPINE` found: **true**.

This proves bounded mesh-resource sharing survives the native import. It does **not** prove HLOD, draw-call reduction or target-GPU performance.

## QA traversal spine

The original 11 route pylons were guides, not a traversable route: their bases were all at `z=0` while the macro terrain beneath them stepped approximately through `+12 / -4 / +8 / +20 m`.

Rev11 adds explicitly diagnostic objects:

- `QA_VAN_ROUTE_SPINE`;
- `COL_VAN_QA_ROUTE_SPINE_colonly`;
- `CAM_QA_ROUTE_SPINE`;
- collection `24_QA_TRAVERSAL_SPINE`.

Geometry contract:

- authored length **10,200 m**;
- width **12 m**;
- 205 route samples at 50 m spacing;
- 410 vertices / 204 quads on both visual and collision meshes;
- maximum diagnostic slope **4.573921259900861°**;
- 200 m ramps bridge macro-height discontinuities;
- pylon base elevations now `[13, 5, -3, -3, -3, 3, 9, 9, 9, 15, 21] m`.

Precommit structural GLB validation: **626 meshes / 807 nodes / 20 materials / 13 images / 21 `_colonly` nodes**. This temporary export byte count is not the committed-provider GLB byte count.

**Truth boundary:** the spine remains `QA_ONLY_NOT_LEVEL_ART`; it is not the final Puerto→Anillo route.

## Native rev11 kilometre traversal — PASS

Because signed rev11 transport became available in the authorized Higgsfield Linux sandbox, the canary no longer required GitHub Actions and did not bypass the repository's CI cost quarantine.

Exact rev11 GLB SHA256 `a3ebb39f54d41e732c2ee343961cba43d85a2ced8a36c9d35306142443c36536` was imported into Godot 4.7.2 and traversed by a real capsule `CharacterBody3D` on the imported `ConcavePolygonShape3D` route collider.

Measured diagnostic run:

- collider bounds: position `[-5000,-3,-1556]`, size `[10200,24,12]` m;
- tested route distance: **10,198.001953125 m**;
- diagnostic speed: **180 m/s** — intentionally accelerated and not a gameplay-feel claim;
- target reached: **true**;
- travel ratio: **0.9999265272264227**;
- physics movement frames: **3,397**;
- total on-floor frames including settle: **3,519**;
- air frames: **4**;
- maximum vertical error against the authored QA profile: **0.0945854187011719 m**;
- maximum lateral Z drift: **0.0001220703125 m**;
- final position: `[5199.2509765625,21.9000072479248,-1549.99987792969]`;
- result: **PASS**.

This qualifies kilometre-scale collision continuity and coordinate precision for the diagnostic spine. It does **not** qualify gameplay-speed feel, combat, interaction traversal, final route art or GPU performance.

Evidence authority: `art_source/vanta/evidence/rev11_native_runtime_qualification.json`.

## Current CP4 disposition

**Empirically qualified:**

- 4 m modular snap assembly and zero-gap yard seams;
- native `_colonly` static collision conversion;
- rev10 bounded 12 m CharacterBody traversal;
- rev11 exact-binary recovery;
- rev11 guarded source mesh sharing and observable native mesh-resource sharing;
- rev11 10.198 km QA CharacterBody traversal / precision.

**Still open:**

- authored final VANTA traversal route and interaction/combat playtest;
- direct visual/art-direction approval;
- HLOD and runtime batching beyond basic shared mesh resources;
- measured frame time, draw calls, residency, memory and GPU cost on declared target hardware;
- final engine selection.

Do not treat the diagnostic QA spine as level art and do not mass-propagate the 327 planning targets solely because the kilometre physics gate passed.
