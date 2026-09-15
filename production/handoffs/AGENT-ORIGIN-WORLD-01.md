# EXOVANT 2950 — ORIGIN world-owner handoff

AGENT: `AGENT-ORIGIN-WORLD-01`  
SESSION ROOT: `SES-20260912-ORIGIN-WORLD-001`  
WORLD CLAIM: `CLM-ORIGIN-WORLD-001`  
BRANCH: `art/world-origin-001`  
LINEAR: `ROT-115`  
GITHUB COORDINATION: issue `#14`  
PROTOCOL: `/EXOVANT-X100`

## NORTH STAR

Own ORIGIN art/modeling at world level while keeping every advancement recoverable through atomic claims, deterministic generators, stable IDs, receipts and adversarial QA. Prefer systemic reuse, native evidence, physically correct collision and causal world depth over raw asset count.

## CURRENT TRUTH STATE

`ATRIO_NATIVE_QUALIFIED / ARCHIVE_REV7_TRAVERSABLE_BLENDER_CANDIDATE / ARCHIVE_NATIVE_PENDING_PRIVATE_TRANSPORT`

Do not regress Atrio to surrogate evidence. Do not promote Archive rev7 to native PASS until the prepared Godot gate consumes the exact rev7 GLB through a private transport.

## ACTIVE / KEEP CLAIMS

- `CLM-ORIGIN-MEGA-ATRIO-001` — real imported Atrio traversal PASS.
- `CLM-ORIGIN-INFRA-ATRIO-SERVICE-001` — 19 service assets.
- `CLM-ORIGIN-CULT-ORGANISM-001` — 17 cultural-memory assets.
- `CLM-ORIGIN-ARCH-ARCHIVE-001` — 21 Archivo source assets + source proxies.
- `CLM-ORIGIN-TECH-LOD-WAVE01-001` — authored LOD0/1/2 for all 57 Wave01 assets.
- `CLM-ORIGIN-ARCH-ARCHIVE-GRAMMAR-001` — four stable Archivo assemblies.
- `CLM-ORIGIN-ARCH-ARCHIVE-NATIVE-001` — Wave04 exact native assembly traversal, in progress.
- `CLM-ORIGIN-TECH-RUNTIME-LOD-001` — Wave04 runtime LOD selection, in progress.

Boss/Corazón and all other worlds remain excluded.

## ATRIO — QUALIFIED BASELINE

Project `6e64cd59-f1f6-461f-850c-737d098f1723`, qualified revision **8**.

- 70 m canonical three-ring envelope.
- 19 service + 17 cultural-memory assets.
- 148 source + 148 LOD1 + 148 LOD2 meshes.
- 19 collision proxies.
- exact rev8 GLB SHA256 `13ce97f29928befa6efdd70a3f428ffd053883ca3eb9159c2d9366bd74966f8d`.
- Godot 4.7.2 run `34831105389` / job `103934408512` SUCCESS.
- real imported `COL_*` → real `StaticBody3D` trimesh.
- CharacterBody r=.38/h=1.85: r=11 landing PASS, r=37 landing PASS, radial traversal final/max r=`38.028427 m`, 400 floor frames, failures `[]`.

Learning retained: closed ring collision created an invisible wall at x=19.220577 m and stopped rev6 traversal at r≈19.0647. Top-only rev7 was rejected for reversed winding; rev8 +Z top-only passed the unchanged native test.

## ARCHIVO — WAVE04 CURRENT BASELINE

Project `9bff5b6c-35a5-4db9-92de-4008a0fc3f4e`.  
Current corrective revision: **7**.

Source system remains:
- 21 stable assets / 8 families.
- 94 source meshes + 94 LOD1 + 94 LOD2.
- authored triangle evidence LOD0 16,880 / LOD1 8,688 / LOD2 4,610.

### Why rev6 was rejected for traversal

Fresh 2026-09-15 inspection found:
- Witness floor gaps 7.075 m and max nearest walkable gap 19.581 m.
- Memory Nave gap 7.766 m.
- Scar Threshold gaps 5.701–7.959 m.
- Vault only had an overlapping center floor pair, not a meaningful through-route.
- child instances repeated module translation inside child-local transforms; rotated modules shifted diagonally.
- floor/threshold collision was closed-box, producing invisible side walls.
- rib/vault collision was a solid box although visible frames were open.
- persisted Wave02 grammar source was not equivalent to the remote rev6 assembly state.

These were treated as production defects, not as reasons to lower the native gate.

### Rev7 corrective build

Mutation `origin-archive-wave4-traversable-grammar-rebuild-009`.

Collision semantic repairs:
- Floor Spine A/B + Threshold A/B → one upward top-only collision quad.
- Rib Wall A/B/C → open-frame collider from visual two piers + lintel.
- Vault Frame A/B/C → open-frame collider from visual two jambs + header.
- no source visual or LOD visual geometry changed.

Instancing repair:
`child.matrix_local = source_parent.matrix_world.inverted_safe() @ source_child.matrix_world`.
This removes repeated module placement from child-local transforms.

Stable assemblies rebuilt as continuous 4.3 m main-deck systems:
- `ORG_ARC_ASM_WITNESS_GALLERY_A`
- `ORG_ARC_ASM_VAULT_JUNCTION_A`
- `ORG_ARC_ASM_MEMORY_NAVE_A`
- `ORG_ARC_ASM_SCAR_THRESHOLD_A`

Blocking core shells were moved into side alcoves where needed. All layout remains `PROPOSAL_UNTIL_GODOT`.

### Rev7 QA

Operation `origin-archive-wave4-qa-20260915-010` = **PASS**.

- Witness: 45 modules / 260 meshes / 45 colliders / 29 walkable / max nearest gap 0 m.
- Vault: 51 / 295 / 51 / 39 / gap 0 m.
- Memory Nave: 55 / 314 / 55 / 32 / gap 0 m.
- Scar Threshold: 28 / 163 / 28 / 22 / gap 0 m.
- transform errors 0.
- source meshes 94; LOD1 94; LOD2 94.
- floor/threshold normals +Z.
- main deck clear width metadata 4.3 m.
- narrow passage metadata Witness 2.0 m; others 2.75 m.

Rev7 artifacts:
- Blend 10,459,681 B / etag `7bbc8e9a10b2781933716fcef0eb7c8a`.
- GLB 3,752,376 B / etag `42851e33885cf79a6167b0891e3ecd39`.
- smaller GLB is observed but is **not** a runtime-performance claim.

Canonical Wave04 rebuild source:
`art_source/worlds/origin/archive/origin_archive_traversable_x100_wave4.py`.

Blender receipt:
`production/receipts/origin/ORIGIN-ARCHIVE-WAVE04-BLENDER-QA.yaml`.

## PREPARED NATIVE + RUNTIME LOD GATE

Reusable Godot 4.7.2 harness:
`art_source/worlds/origin/runtime/origin_archive_native_lod_validate.gd`.

Archive gate requires all 4 assemblies to:
- use exact imported `__COL_` meshes as trimesh `StaticBody3D` collision;
- discover valid floor nodes via support normal + capsule clearance;
- build a connected route graph with midpoint support checks;
- span >=70% of the walkable dominant axis;
- traverse with a real CharacterBody capsule r=.38/h=1.85 without falls/stalls.

Runtime LOD gate requires:
- exactly 94 deterministic source↔LOD1↔LOD2 groups;
- exactly one visible tier per group;
- near/mid/far switches exercised;
- triangle counts read from imported Godot mesh surfaces;
- LOD1 <65% and LOD2 <40% of LOD0;
- source collision mesh count unchanged across visual switches.

This would prove visual tier switching and geometry reduction only. It would **not** prove residency, packed memory, HLOD, streaming, FPS or target-GPU gains.

## CURRENT BLOCKER — SECURITY/TRANSPORT, NOT ASSET

Higgsfield returns the exact rev7 GLB through a short-lived signed R2 bearer URL. This GitHub connection exposes no workflow-dispatch payload or secret mutation surface, and Google Drive upload accepts only a connector `file_uri` rather than a URL. The GLB connector response does not expose a `file_uri`.

Therefore the bearer has **not** been persisted into GitHub history. The native Wave04 test is prepared but has not been executed against rev7. Do not claim native Archive PASS from Blender QA.

Scratch evidence branch:
`integration/origin-archive-native-lod-002`.
Harness blob SHA:
`48cf97b4eab094e364761a928c6bc13df8edc164`.

## NEXT P0

1. Establish a private binary bridge for the exact rev7 GLB and run the prepared Archive native + runtime LOD canary unchanged.
2. If PASS, implement runtime packing/HLOD/residency rather than merely hidden resident tiers.
3. Then qualify local/variable gravity on real Atrio import.
4. Causal texture finishing, phenomena/ecology, human `GATE-ART`, target hardware.

WORLD CLAIM STATUS: **KEEP**  
ALL LISTED ATOMIC CLAIMS: **KEEP / IN_PROGRESS**
