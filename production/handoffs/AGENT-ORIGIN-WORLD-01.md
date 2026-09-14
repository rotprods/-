# EXOVANT 2950 — ORIGIN world-owner handoff

AGENT: `AGENT-ORIGIN-WORLD-01`  
SESSION ROOT: `SES-20260912-ORIGIN-WORLD-001`  
WORLD CLAIM: `CLM-ORIGIN-WORLD-001`  
BRANCH: `art/world-origin-001`  
LINEAR: `ROT-115`  
GITHUB COORDINATION: issue `#14`  
PROTOCOL: `/EXOVANT-X100`

## NORTH STAR

Own ORIGIN art/modeling at world level while keeping every advancement recoverable through atomic claims, deterministic generators, stable asset IDs, receipts and adversarial QA. Prefer systemic reuse, native evidence, physically correct collision and causal world depth over raw prop count.

## CURRENT TRUTH STATE

`EMPIRICALLY_QUALIFIED_NATIVE_IMPORT_AND_ATRIO_TRAVERSAL / SYSTEM_CANDIDATE`

This is stronger than the prior surrogate state. Do not regress to surrogate-only validation unless a future revision invalidates the real native receipt.

## ACTIVE / KEEP CLAIMS

- `CLM-ORIGIN-MEGA-ATRIO-001` — Atrio 70 m three-ring structural grammar.
- `CLM-ORIGIN-INFRA-ATRIO-SERVICE-001` — 19 service-infrastructure assets.
- `CLM-ORIGIN-CULT-ORGANISM-001` — 17 El Organismo cultural-memory assets.
- `CLM-ORIGIN-ARCH-ARCHIVE-001` — 21 Archivo structural assets + 21 proxies.
- `CLM-ORIGIN-TECH-LOD-WAVE01-001` — LOD0/1/2 for all 57 Wave-01 assets.
- `CLM-ORIGIN-ARCH-ARCHIVE-GRAMMAR-001` — four deterministic Archive assemblies.

Boss/Corazón remains explicitly excluded.

## CURRENT REMOTE PROJECTS

### Atrio
Project: `6e64cd59-f1f6-461f-850c-737d098f1723`  
Current qualified revision: **8**

Wave inventory:
- canonical 70 m / three-ring Atrio structural grammar.
- 19 service + 17 cultural-memory X100 assets.
- 148 source meshes plus 148 LOD1 + 148 LOD2 meshes.
- 19 total collision proxies.

LOD evidence:
- LOD0 evaluated: 29,328 tris.
- LOD1: 14,544 = 49.59%.
- LOD2: 7,966 = 27.16%.
- UV/material/transform/silhouette QA PASS.

Rev8 collision correction:
- 9/9 ring proxies are now top-only walkable surfaces.
- 18 polygons / 38 verts per ring proxy.
- upward normals (`min normal_z >= 0.99999994`).
- zero horizontal ring hits at capsule-foot z=4.32 m.
- visual geometry, bridges, nodes and LOD geometry were not modified.
- collision semantics: `walkable_top_surface_only_upward_v3`.

Rev8 artifact:
- GLB 6,866,000 B
- etag `de3984397e1c5c4b768aa62deb95f648`
- SHA256 `13ce97f29928befa6efdd70a3f428ffd053883ca3eb9159c2d9366bd74966f8d`
- Blend 8,463,819 B / etag `9bb9acfeac51397a3d54c64b81f0c074`

Deterministic rebuild:
1. `art_source/worlds/origin/atrio/origin_atrio.py`
2. `art_source/worlds/origin/atrio/origin_atrio_collision_rev8.py`
3. `art_source/worlds/origin/atrio/origin_atrio_x100_wave1.py`
4. `art_source/worlds/origin/tech/origin_lod_x100_wave2.py`

### Archivo de la Primera Herida
Project: `9bff5b6c-35a5-4db9-92de-4008a0fc3f4e`  
Current qualified revision: `6`

- 21 stable structural assets / 8 families / 21 proxies.
- 94 source meshes + 94 LOD1 + 94 LOD2.
- LOD0 16,880 / LOD1 8,688 / LOD2 4,610 tris.
- one LOD2 7.9 cm silhouette regression was rejected and selectively reverted.
- four stable assemblies, 67 module instances, 367 linked mesh instances.
- source mesh-data duplication 0.
- player lateral clearance proposal margins 2.64–4.24 m.
- GLB 5,171,380 B / etag `e25633728494203865bd76b858723960`.
- SHA256 `7d1ca1c5b04207f490a0ccfdae3fccec32c3b0d06d880d8ad364096cdeb57493`.

## REAL GODOT QUALIFICATION — PASS

Canonical receipt:
`production/receipts/origin/ORIGIN-REAL-GLB-GODOT-001.yaml`

Evidence:
- scratch evidence PR #32, intentionally NO-MERGE.
- final canary commit `194ee4fe3c04318bf2fab4eb62de72b97eb1b322`.
- GitHub Actions run `34831105389` / run #377.
- job `103934408512`.
- Godot `4.7.2-stable (official)` / hash `ed1daf0bf001b61586d9930840f2f1394092c079`.
- conclusion: **SUCCESS**.

Native import readback:
- Atrio: 613 nodes / 570 meshes / 570 material slots / 19 collision meshes / 148 LOD1 / 148 LOD2.
- Archivo: 804 nodes / 703 meshes / 703 material slots / 94 LOD1 / 94 LOD2 / 4 assembly IDs.
- both GLBs load as PackedScene.

Real Atrio physics:
- 19 imported `COL_*` meshes converted into real `StaticBody3D` trimesh collision.
- CharacterBody capsule radius 0.38 m / height 1.85 m.
- inner landing r=11 m: PASS, 136 floor frames.
- outer landing r=37 m: PASS, 136 floor frames.
- radial traversal r=11 → r=37: PASS; final/max radius `38.028427 m`.
- traversal floor frames 400; minimum Y `5.0342946 m`.
- `physics_pass=true`; failures `[]`.

## CAUSAL DEFECT CHAIN — DO NOT LOSE THIS LEARNING

Rev6 already imported correctly, but real CharacterBody traversal failed at `r≈19.0647 m`.

Blender horizontal ray audit identified `COL_ORG_ATR_RING_A70_SEG_00` exposing an internal vertical wall at `x=19.220577 m` with horizontal normal. The ring proxies were closed solids, so visually open bridge/ring interfaces contained invisible collision walls.

- rev7 removed side/bottom walls → top-only ring collision.
- adversarial QA rejected rev7 because winding was downward.
- rev8 reversed winding upward and passed Blender QA.
- the **same native canary** then passed without weakening the physics acceptance criteria.

This establishes a strong defect→fix→native-readback chain.

## PROVEN NOW

- exact Atrio rev8 GLB imports natively in Godot 4.7.2.
- exact Archivo rev6 GLB imports natively in Godot 4.7.2.
- stable ORIGIN naming/material/LOD/assembly structure survives import.
- real imported Atrio collision can be converted to physics bodies.
- real CharacterBody Atrio traversal passes across ring/bridge interfaces.
- 57 stable Wave-01 assets have actual LOD1/LOD2 geometry.
- four Archivo assemblies reuse linked source mesh data.

## STILL NOT PROVEN

- merged gameplay/runtime integration of these GLBs.
- CharacterBody traversal through Archive assemblies.
- engine runtime LOD switching, HLOD or packed file-size/frame-time savings.
- local/variable-gravity gameplay on imported Atrio.
- final causal texture sets.
- target-hardware performance.
- human `GATE-ART`.

Do not claim final AAAA+, final game-ready performance or final Archive dimensions before those gates pass.

## NEXT P0

1. Native Archive assembly CharacterBody traversal using exact imported rev6 geometry; use measurements to promote/reject proposal dimensions.
2. Engine runtime LOD switching + packing/HLOD proof on real imports.
3. Then local-gravity gameplay qualification and causal-texture finishing.

WORLD CLAIM STATUS: **KEEP**  
ALL LISTED ATOMIC CLAIMS: **KEEP / IN_PROGRESS**
