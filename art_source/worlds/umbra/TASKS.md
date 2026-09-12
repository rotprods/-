# UMBRA — Task System

Claim: `CLM-W04-WORLD-UMBRA-001`  
Agent: `AGENT-UMBRA-04`  
Branch: `art/world-umbra-001`

## Local North Star

Deliver UMBRA's first production-grade world foundation as an isolated, reproducible 3D stream whose art language, scale, ownership, editable source and validation can be continued by another agent without chat context. Wave 0 succeeds when the blockout and pipeline receipts are real; it does **not** claim final AAA quality.

## First 10 tasks

| ID | Priority | Objective / Output | Dependency | Definition of Done | Status |
|---|---|---|---|---|---|
| W04/BOOT/001 | P0 | Recover repo authority, HEAD, protocols and world canon | repo access | `AGENTS`, STATE, art/world sources read; base SHA recorded; unknowns separated | DONE |
| W04/CLAIM/002 | P0 | Reserve collision-free UMBRA ownership | W04/BOOT/001 | branch + ownership file persisted; includes/excludes explicit; no UMBRA competing branch observed | DONE |
| W04/CANON/003 | P0 | Create World Bible with epistemic separation | W04/BOOT/001 | canon, unknowns, proposals, art/realism/manufacturing contracts and world DoD versioned | DONE |
| W04/PIPE/004 | P0 | Revalidate editable Blender route | W04/CLAIM/002 | dedicated 3D Jutsu project; Blender version, metric units, empty scene and guards observed | DONE |
| W04/BLK/005 | P1 | Build deterministic twilight-band regional blockout | W04/PIPE/004 | terrain + traversal + reflector + caravan + refuge + NOCTIL destination proxy committed in Blender revision | DONE |
| W04/QA/006 | P0 | Run structural/scale QA | W04/BLK/005 | object/mesh/material/tri counts measured; scale refs measured; no residual object-scale anomalies or zero-dimension meshes | DONE |
| W04/ASSET/007 | P1 | Persist master asset/coverage registry | W04/CANON/003 | every Wave-0 family has ID, tier, priority, owner, status, dependency, dimension state, LOD/collision/export state | DONE |
| W04/GEN/008 | P1 | Persist and independently replay Blender generator/source | W04/BLK/005 | versioned script rebuilt a clean project with the same 96 objects / 85 meshes / 9 materials / 12,204 tris and scale dimensions; no external absolute asset paths | DONE |
| W04/VIS/009 | P1 | Human/agent visual QA of delivery render | W04/BLK/005 | framing, contacts, silhouette, light hierarchy and art drift inspected; defects converted to tasks | REVIEW |
| W04/ENG/010 | P0 | Engine import / gameplay camera acceptance | W04/ASSET/007 + engine integration authority | GLB imported in active runtime; scale/material/collision/camera/profile receipt recorded | BLOCKED |

## Wave 1 queued tasks

- `W04/TERRAIN/011` — derive 3–4 gameplay terrain cell archetypes from the quest chain without inventing global geology.
- `W04/INFRA/012` — production reflector kit: foundation, mast, gimbal, mirror, actuator, service ladder/platform, cable/power interface.
- `W04/CAR/013` — caravan modular kit: chassis, shell, canopy, track/runner, service bay, refuge beacon, cargo interfaces.
- `W04/ARCH/014` — refuge hub kit with wind-load/manufacturing logic.
- `W04/MAT/015` — calibrated portable PBR material library and texel-density policy after runtime target validation.
- `W04/NOCTIL/016` — boss function/anatomy/telegraph interface brief before final creature modeling.
- `W04/QUEST/017` — environmental asset mapping for Q_UMBRA_M01..M04.
- `W04/ACCESS/018` — low-light and color-vision readability test scene.
- `W04/LOD/019` — LOD/collision strategy after engine target budget is empirically qualified.
- `W04/EXPORT/020` — deterministic export/import smoke test with runtime receipt.

## Blocking decisions

### BLOCK-W04-001 — planetary radius
- decision needed: physical radius/diameter or explicit authoring abstraction.
- affected scope: orbital representation, curvature, long-distance vistas, absolute world coordinates.
- why blocking: a fake value would contaminate L0/L1 scale.
- options: (A) canonize radius; (B) define radius as intentionally abstract until later; (C) adopt a scientifically motivated proposal through ADR.
- recommended: B for current art production; continue authored local regions in metres.
- reversible: yes before orbital/world-partition integration.
- work that can continue: L2–L5 regional production.

### BLOCK-W04-002 — final production engine / GPU budget
- decision needed: qualified production runtime and hardware targets.
- affected scope: triangle/material/texture budgets, LOD/HLOD, streaming, shaders, collision profile.
- current evidence: Godot 4.7.2 is executable prototype; Unreal remains principal production candidate but is not integrated/qualified.
- recommended: record metrics now, avoid universal hard caps until target qualification.
- work that can continue: topology discipline, measured counts, portable PBR, proxy collision planning.

### BLOCK-W04-003 — final NOCTIL morphology
- decision needed: ecological/function/anatomy/rig/attack contract.
- affected scope: hero boss mesh, rig, animation, hitboxes, arena proportions.
- current action: maintain destination/environment proxy only.
