# ORIGIN — X100 Coverage Ledger

Status date: 2026-09-14
Owner: `AGENT-ORIGIN-WORLD-01`
Branch: `art/world-origin-001`
World claim: `CLM-ORIGIN-WORLD-001`
Protocol: `/EXOVANT-X100`

## North Star

ORIGIN must read as a pre-existing, internally coherent place whose infrastructure, memory culture, structural history and material ageing explain themselves through geometry. Density is semantic and causal, never random greeble. Prefer reuse multipliers, native evidence, collision truth and systemic families over one-off prop count.

## Hard boundaries

- Other worlds: OUT OF SCOPE.
- `Corazón de EXOVANT`, final boss and final narrative state remain excluded.
- Archive dimensions and assembly spacing are `PROPOSAL_UNTIL_GODOT`.
- Real Atrio GLB import and real CharacterBody traversal are now PASS; do not repeat surrogate work.
- LOD geometry exists and imports, but engine runtime LOD switching/HLOD packing is not yet proven.
- Final causal textures, target-hardware performance and human `GATE-ART` remain incomplete.

## Coverage matrix

| Domain | Claim / family | Stable assets | Native evidence | State |
|---|---|---:|---|---|
| Atrio macrostructure | `CLM-ORIGIN-MEGA-ATRIO-001` | 10 locked IDs + 19 collision proxies | **REAL GLB import + Atrio CharacterBody traversal PASS** | empirically qualified system candidate |
| Atrio service infrastructure | `CLM-ORIGIN-INFRA-ATRIO-SERVICE-001` | 19 | survives rev8 import; placement remains outside traversal band | locally validated family candidate |
| El Organismo cultural-memory kit | `CLM-ORIGIN-CULT-ORGANISM-001` | 17 | survives rev8 import | locally validated family candidate |
| Archivo structural architecture | `CLM-ORIGIN-ARCH-ARCHIVE-001` | 21 + 21 proxies | rev6 PackedScene import PASS; assembly traversal pending | locally validated structural kit |
| LOD system | `CLM-ORIGIN-TECH-LOD-WAVE01-001` | 57 source assets | LOD nodes survive native import | geometry qualified; runtime switching pending |
| Archivo assembly grammar | `CLM-ORIGIN-ARCH-ARCHIVE-GRAMMAR-001` | 4 assemblies | 4/4 IDs survive native import | native traversal pending |
| Material response | Atrio + Archivo Principled roles | 14+ roles | material slots survive native import | response-v1 |
| Final texture maps | all | 0 final sets | not integrated | incomplete |
| Origin phenomena/ecology | future shard | 0 | pending | unbuilt |
| Corazón / boss | excluded | 0 | pending | deferred |

## Wave 01 — authored family base

### Atrio
Project: `6e64cd59-f1f6-461f-850c-737d098f1723`
- 36 stable X100 asset parents: 19 service + 17 cultural-memory.
- 148 source meshes.
- service clearance beyond A70 edge: +0.4312527094 m.
- culture clearance beyond B52 edge: +0.5812839777 m.
- rev4 exposed a 148-child double-parent transform defect; rev5 corrected it.

### Archivo
Project: `9bff5b6c-35a5-4db9-92de-4008a0fc3f4e`
- 21 stable assets / 8 structural families / 94 source meshes / 21 proxies.
- rev1 exposed nonportable AREA lights; rev2 replaced them with portable SPOT/POINT.

## Wave 02 — LOD + assembly grammar

### Real LOD geometry
Claim: `CLM-ORIGIN-TECH-LOD-WAVE01-001`

Atrio:
- LOD0 evaluated: 29,328 tris.
- LOD1: 14,544 = 49.59%.
- LOD2: 7,966 = 27.16%.
- 36/36 coverage; 148 LOD1 + 148 LOD2; UV/material/transform/silhouette QA PASS.

Archivo:
- LOD0 evaluated: 16,880 tris.
- LOD1: 8,688 = 51.47%.
- LOD2: 4,610 = 27.31%.
- 21/21 coverage; 94 LOD1 + 94 LOD2.
- one 7.9 cm LOD2 shell shrink was rejected and selectively reverted; final >6 cm drift failures = 0.

Important: triangle reduction is proven in authored geometry. Runtime switching/HLOD/frame-time/file-size savings are not yet claimed.

### Archivo assembly grammar
Claim: `CLM-ORIGIN-ARCH-ARCHIVE-GRAMMAR-001`
Stable assemblies:
- `ORG_ARC_ASM_WITNESS_GALLERY_A`
- `ORG_ARC_ASM_VAULT_JUNCTION_A`
- `ORG_ARC_ASM_MEMORY_NAVE_A`
- `ORG_ARC_ASM_SCAR_THRESHOLD_A`

Measured:
- 67 module instances.
- 367 linked mesh instances.
- 19 unique source assets consumed.
- source mesh-data duplication: 0.
- invalid refs: 0.
- recipe/seed signatures: 4/4.
- collision inheritance failures: 0.
- player lateral clearance margins: 2.64–4.24 m.
- all assembly geometry fits the rev6 delivery camera.

## Wave 03 — REAL_GLB_IMPORT + collision qualification

### Exact native inputs
Atrio rev8:
- project `6e64cd59-f1f6-461f-850c-737d098f1723`
- GLB 6,866,000 B
- etag `de3984397e1c5c4b768aa62deb95f648`
- SHA256 `13ce97f29928befa6efdd70a3f428ffd053883ca3eb9159c2d9366bd74966f8d`

Archivo rev6:
- project `9bff5b6c-35a5-4db9-92de-4008a0fc3f4e`
- GLB 5,171,380 B
- etag `e25633728494203865bd76b858723960`
- SHA256 `7d1ca1c5b04207f490a0ccfdae3fccec32c3b0d06d880d8ad364096cdeb57493`

### Native Godot 4.7.2 readback
Receipt: `production/receipts/origin/ORIGIN-REAL-GLB-GODOT-001.yaml`
Run `34831105389` / job `103934408512` = **SUCCESS**.

Atrio imported:
- PackedScene load: PASS
- 613 nodes / 570 meshes / 570 material slots
- 19 imported collision meshes
- 148 LOD1 + 148 LOD2 nodes
- service/cultural stable naming survives import

Archivo imported:
- PackedScene load: PASS
- 804 nodes / 703 meshes / 703 material slots
- 94 LOD1 + 94 LOD2 nodes
- 4/4 stable assembly IDs survive import

### Real CharacterBody3D physics
- 19 imported Atrio `COL_*` meshes converted to real trimesh `StaticBody3D` collision.
- inner landing r=11 m: PASS.
- outer landing r=37 m: PASS.
- real radial traversal: start r=11 → target r=37 → final r=38.028427 m.
- floor frames during traverse: 400.
- min Y remained 5.0342946 m.
- `physics_pass=true`, failures `[]`.

### Causal collision repair
Rev6 import itself already passed, but the CharacterBody stopped at r≈19.0647 m. Blender ray audit found the exact internal wall at x=19.220577 m in `COL_ORG_ATR_RING_A70_SEG_00`. The nine ring proxies were closed solids.

- rev7: converted all nine ring proxies to walkable top-only surfaces.
- adversarial QA rejected rev7 because normals faced downward.
- rev8: flipped winding upward.
- final Blender QA: 9/9 top-only proxies, 18 polys each, zero vertical hits at capsule-foot height, normals +Z.
- same native canary on rev8: **PASS**.

Deterministic cold rebuild path:
1. `origin_atrio.py`
2. `origin_atrio_collision_rev8.py`
3. Wave-01 family generators
4. Wave-02 LOD generator

## Highest-value remaining gaps

1. **Native Archive assembly CharacterBody traversal** and promote/reject proposal dimensions from measured results.
2. **Engine LOD switching + runtime packing/HLOD**; do not claim performance until measured.
3. Local/variable-gravity gameplay qualification on the real imported Atrio.
4. Final causal texture maps: black-mineral fracture, living-bronze ageing/patina, memory residue, repair states.
5. Origin phenomena/ecology and environmental effects on assets.
6. Distant-vista / macro connection language between Atrio, Archivo and later Corazón boundary.
7. Human `GATE-ART`.
8. Target-hardware performance.

## Continuous selection rule

After every family or gate, re-sync ownership and choose the highest-value uncovered cell. Do not repeat surrogate/import checks already empirically qualified unless an asset revision invalidates the receipt.
