# AURORA VEIL — TASK SYSTEM

**Agent:** AGENT-02-AURORA  
**Session:** AURORA-20260912T192957Z-001  
**Claim:** CLM-AURORA-WORLD-001  
**Branch:** art/world-aurora-veil-001  
**Remote checkpoint:** 3D Jutsu `d6488148-8547-4ffe-b63d-e5fbec3a339c` revision 14  

## North Star

Deliver AURORA VEIL as a complete, physically plausible, unmistakable EXOVANT world package, with planet-scale metadata, three canonical regions, temporal visual grammar, ecology/population, AEON, world-specific asset library, streaming/collision/export strategy, receipts and cold-resume documentation.

## First 10 tasks — current state

| ID | Priority | Status | Current evidence / remaining DoD |
|---|---|---|---|
| AUR/WORLD/001 Atomic ownership claim | P0 | DONE | Claim persisted before Blender; Fleet ACK issue #7 epoch 1. |
| AUR/WORLD/002 World Bible + scale ADR | P0 | DONE | Canon/proposal/unknown boundary documented. |
| AUR/WORLD/003 L1 orbital representation | P0 | REVIEW_TECHNICAL | Body/atmosphere/aurora layers, two station proxies, export and surface regression PASS; human visual review open. |
| AUR/WORLD/004 Macro map + regional anchors | P0 | REVIEW_TECHNICAL | 3 stable anchors + 5.2×3.0 km frame; no fabricated global continents. |
| AUR/TERRAIN/005 Three-region terrain macro | P0 | REVIEW_TECHNICAL | Rev14: 53.61 m relief span, P95 4.278°, protected corridor/anchors, temporal contact repair, clean GLB, deterministic rollback. Lithology/microdetail/material blend/traversal/art remain open. |
| AUR/ARCH/006 Camp observatory/refuge kit | P1 | REVIEW_TECHNICAL | 4 m grid, manufacturing-aware modular library, 16×12 m proof refuge, 24-segment 48 m ring, instancing/export/regression PASS. Final art/UV/PBR open. |
| AUR/TEMPORAL/007 Bounded echo grammar | P0 | REVIEW_TECHNICAL | Rev12+: deterministic five-state local contract, 3 fields, 6 hidden collision proxies, 3 AEON sectors; runtime/sound/human comprehension open. |
| AUR/AEON/008 Huerto + 50 m arena | P1 | REVIEW_BLOCKOUT | Canon 50 m arena + exactly 3 sectors + orchard/AEON blockout. Final hero design/rig/readability pending. |
| AUR/ECO/009 Ecology/population lineup | P1 | IN_PROGRESS | Semantic proxies exist; final anatomy/silhouette/LOD/art approval pending. |
| AUR/TECH/010 Export/collision/streaming/QA | P0 | IN_PROGRESS | Blend/GLB exchange PASS through rev14; QA baselines active; engine/perf/LOD/human gates remain. |

## Critical technical receipts

### Terrain r14
- `TERRAIN_CONTRACT.md`
- `QA/terrain_r14.json`
- `blender/aurora_terrain_relief_r14.py`
- physical frame: 5,200×3,000×53.610 m;
- global slopes: P50 1.061°, P95 4.278°, max 8.666°;
- protected route core 120 m + 300 m feather;
- Camp/Plain/Huerto anchors remain grounded within ~11 cm;
- AEON floor remains +0.5915 m over terrain;
- temporal idle rings exactly +0.28 m over local terrain;
- no geometric Terrain QA objects remain in portable export;
- rollback uses exact versioned inverse formula, not a purgable orphan mesh.

### Camp modular r8+
- 4 m grid / 12 source modules;
- 16×12 m refuge proof;
- 48 m ring / 24 segments / shared mesh instancing;
- manufacturing/material-role contract;
- Camp render delta −0.001 vs r5 mean.

### Temporal r12+
- `IDLE → PRE_CUE → REPEAT_ARMED → REPEAT_ACTIVE → COOLDOWN`;
- exactly 3 local fields and 3 AEON sectors;
- collision disabled by default and owned only by ACTIVE local proxies;
- global rewind/save mutation forbidden.

## Next critical path

1. `AUR/MAT/020` — calibrated material board: physically plausible base values/ranges, manufacture-specific roughness/metalness, environment/wear causality and neutral lookdev evidence.
2. `AUR/PROC/027` — cable/instrument routing generator consuming Camp module sockets.
3. `AUR/AEON/050` — begin hero primary/secondary-form production after materials/temporal/terrain interfaces are stable.

## Backlog truth

- Global continent/biome map remains DEFERRED until global geography is decided.
- Terrain morphology is REVIEW_TECHNICAL, not final terrain.
- Camp modules are REVIEW_TECHNICAL, not final PBR assets.
- Temporal state grammar is REVIEW_TECHNICAL, not runtime implementation.
- Engine integration remains blocked by EXO-012.
- Target hardware performance remains blocked.
- Human GATE-ART remains pending.

## Stop condition

Claim remains KEEP / IN_PROGRESS. No world DONE while P0/P1 remain, GATE-ART/runtime/performance are unresolved, or final hero/character/environment assets lack applicable topology/material/LOD/integration gates.
