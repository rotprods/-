# EXOVANT 2950 — ORIGIN world-owner handoff

AGENT: `AGENT-ORIGIN-WORLD-01`  
SESSION ROOT: `SES-20260912-ORIGIN-WORLD-001`  
WORLD CLAIM: `CLM-ORIGIN-WORLD-001`  
BRANCH: `art/world-origin-001`  
LINEAR: `ROT-115`  
GITHUB COORDINATION: issue `#14`  
PROTOCOL: `/EXOVANT-X100`

## NORTH STAR

Own ORIGIN art/modeling at world level while keeping work recoverable through atomic claims, deterministic generators, stable asset IDs, receipts and hard QA. Prefer systemic reuse, native evidence and causal world depth over raw one-off prop count.

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
Current qualified revision: `6`

Baseline structural checkpoint:
- canonical arena envelope: 70 m, three connected rings.
- original explicit collision proxies: 19.
- surrogate CharacterBody traversal: PASS.

X100 Wave 01:
- 36 stable asset parents / 13 families / 148 source meshes.
- service radial clearance beyond A70 edge: +0.4312527094 m.
- culture radial clearance beyond B52 edge: +0.5812839777 m.
- parenting defect found at rev4 and corrected at rev5.

X100 Wave 02 LOD:
- 148 LOD1 + 148 LOD2 meshes.
- LOD0 evaluated: 29,328 tris.
- LOD1: 14,544 tris (49.59%).
- LOD2: 7,966 tris (27.16%).
- 36/36 asset coverage; UV/material/transform/bounds QA PASS.
- LOD0 frozen.
- rev6 GLB: 7,039,992 B / etag `3cd3d91fc0d667c3c93145ba3efadc51`.

### Archivo de la Primera Herida
Project: `9bff5b6c-35a5-4db9-92de-4008a0fc3f4e`  
Current qualified revision: `6`

X100 Wave 01:
- 21 stable assets / 8 structural families / 94 source meshes / 21 proxies.
- source geometry QA PASS.
- nonportable AREA lights discovered at rev1; replaced with SPOT/POINT at rev2.

X100 Wave 02 LOD:
- 94 LOD1 + 94 LOD2 meshes.
- LOD0 evaluated: 16,880 tris.
- LOD1: 8,688 tris (51.47%).
- LOD2: 4,610 tris (27.31%).
- one 7.9 cm silhouette regression on `ORG_ARC_ARCHIVE_CORE_SHELL_A_CORE` rejected; only that LOD2 reverted to unbeveled base. Final >6 cm drift failures: 0.

X100 Wave 02 assembly grammar:
- `ORG_ARC_ASM_WITNESS_GALLERY_A`
- `ORG_ARC_ASM_VAULT_JUNCTION_A`
- `ORG_ARC_ASM_MEMORY_NAVE_A`
- `ORG_ARC_ASM_SCAR_THRESHOLD_A`
- 67 module instances / 367 linked mesh instances / 19 unique source assets consumed.
- source mesh data duplicated: 0.
- recipe and seed signatures valid: 4/4.
- collision inheritance failures: 0.
- player lateral clearance margins: 2.64–4.24 m beyond 0.76 m capsule diameter.
- delivery camera refit at rev6: all assembly geometry in frame.
- dimensions remain `PROPOSAL_UNTIL_GODOT`.
- rev6 GLB: 5,171,380 B / etag `e25633728494203865bd76b858723960`.

## DEFECTS FOUND AND CORRECTED

1. Atrio rev2: camera clipping, floating supports and oversize node collision proxies.
2. Atrio X100 rev4: 148-child double-parent transform defect; fixed at rev5.
3. Archivo rev1: AREA lights nonportable in GLB; fixed with SPOT/POINT in rev2.
4. Archivo LOD rev3: one LOD2 shell drifted 7.9 cm; rejected and selectively reverted in rev4.
5. Archivo assembly rev5: delivery camera missed the largest nave; camera-only refit at rev6, geometry unchanged.

## EPISTEMIC TRUTH

Current overall truth state: `LOCALLY_VALIDATED_SYSTEM_CANDIDATE`.

Proven:
- 57 stable Wave-01 asset IDs exist remotely with deterministic generators.
- 57/57 have actual LOD1 and LOD2 geometry, not metadata-only promises.
- all LOD QA passes current UV/material/transform/silhouette contracts.
- four stable Archive assemblies exist and reuse linked source mesh data.
- GLB exports succeed at the stated revisions.

Not proven:
- real Godot import readback of Atrio rev6 / Archivo rev6.
- imported GLB collision/traversal with real geometry.
- engine LOD switching, runtime packing/HLOD or frame-time savings.
- final causal texture sets.
- target-hardware performance.
- human `GATE-ART`.

Do not claim final AAAA+, final game-ready performance or final Archive scale until those gates pass.

## RECOVERABLE SOURCE / RECEIPTS

- `art_source/worlds/origin/X100_COVERAGE.md`
- `art_source/worlds/origin/atrio/origin_atrio.py`
- `art_source/worlds/origin/atrio/origin_atrio_x100_wave1.py`
- `art_source/worlds/origin/archive/origin_archive_x100_wave1.py`
- `art_source/worlds/origin/tech/origin_lod_x100_wave2.py`
- `art_source/worlds/origin/archive/origin_archive_grammar_x100_wave2.py`
- `production/claims/CLM-ORIGIN-MEGA-ATRIO-001.yaml`
- `production/claims/CLM-ORIGIN-INFRA-ATRIO-SERVICE-001.yaml`
- `production/claims/CLM-ORIGIN-CULT-ORGANISM-001.yaml`
- `production/claims/CLM-ORIGIN-ARCH-ARCHIVE-001.yaml`
- `production/claims/CLM-ORIGIN-TECH-LOD-WAVE01-001.yaml`
- `production/claims/CLM-ORIGIN-ARCH-ARCHIVE-GRAMMAR-001.yaml`
- `production/receipts/origin/ORIGIN-X100-WAVE-01-QA.yaml`
- `production/receipts/origin/ORIGIN-X100-WAVE-02-QA.yaml`

## NEXT ACTION — P0

`REAL_GLB_IMPORT_GODOT_4_7_2`.

Use the exact Atrio rev6 and Archivo rev6 GLBs, import them into an isolated Godot 4.7.2 validation project, verify PackedScene instantiation, stable naming/mesh/material/scale readback, then build real collision/traversal evidence from imported geometry. Only after that should Archive proposal dimensions be promoted/rejected and engine LOD switching be measured.

WORLD CLAIM STATUS: **KEEP**  
ALL LISTED ATOMIC CLAIMS: **KEEP / IN_PROGRESS**
