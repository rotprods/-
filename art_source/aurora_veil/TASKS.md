# AURORA VEIL — TASK SYSTEM

**Agent:** AGENT-02-AURORA  
**Session:** AURORA-20260912T192957Z-001  
**Claim:** CLM-AURORA-WORLD-001  
**Branch:** art/world-aurora-veil-001  
**Remote checkpoint:** 3D Jutsu `d6488148-8547-4ffe-b63d-e5fbec3a339c` revision 19  

## North Star

Deliver AURORA VEIL as a complete, physically plausible, unmistakable EXOVANT world package, with planet-scale metadata, three canonical regions, temporal visual grammar, ecology/population, AEON, world-specific asset library, streaming/collision/export strategy, receipts and cold-resume documentation.

## First 10 tasks — current state

| ID | Priority | Status | Current evidence / remaining DoD |
|---|---|---|---|
| AUR/WORLD/001 Atomic ownership claim | P0 | DONE | Fleet ACK issue #7 epoch 1; draft PR #20. |
| AUR/WORLD/002 World Bible + scale ADR | P0 | DONE | Canon/proposal/unknown boundary documented. |
| AUR/WORLD/003 L1 orbital representation | P0 | REVIEW_TECHNICAL | Separate body/atmosphere/aurora + stations, export and surface regression PASS; human art review open. |
| AUR/WORLD/004 Macro map + regional anchors | P0 | REVIEW_TECHNICAL | Stable 5.2×3.0 km local frame / 3 anchors; no invented continents. |
| AUR/TERRAIN/005 Three-region terrain macro | P0 | REVIEW_TECHNICAL | Rev14 53.61 m relief, slope/anchor/export/rollback gates pass. Lithology/microdetail/nav/art open. |
| AUR/ARCH/006 Camp observatory/refuge kit | P1 | REVIEW_TECHNICAL | 4 m modular kit + 48 m ring + level proof platform; r19 fixes terrain hierarchy and adds 19 variable piers. UV/PBR/art open. |
| AUR/TEMPORAL/007 Bounded echo grammar | P0 | REVIEW_TECHNICAL | Rev12 deterministic five-state local contract, 3 fields, 6 disabled-by-default collision proxies, 3 AEON sectors. Runtime/audio/comprehension open. |
| AUR/AEON/008 Huerto + 50 m arena | P1 | REVIEW_BLOCKOUT | Canon 50 m arena / 3 sectors. Hero AEON production is next high-visibility content. |
| AUR/ECO/009 Ecology/population lineup | P1 | IN_PROGRESS | Semantic proxies exist; final anatomy/silhouette/LOD/art open. |
| AUR/TECH/010 Export/collision/streaming/QA | P0 | IN_PROGRESS | Blender/GLB PASS through rev19; technical QA active; native engine/perf/LOD/human gates open. |

## Additional production tasks

| ID | Priority | Status | Receipt |
|---|---|---|---|
| AUR/MAT/020 Manufactured material calibration | P1 | REVIEW_MANUFACTURED | `MATERIAL_CONTRACT.md`, `QA/material_r15.json`, Camp regression +0.0027 mean; natural lithology explicitly excluded. |
| AUR/PROC/027 Camp service/cable routing | P1 | REVIEW_TECHNICAL | `SERVICE_ROUTING_CONTRACT.md`, `QA/service_r19.json`; live sockets, 19 piers, power/data clearances, no accidental routing objects. |

## Current critical receipts

- `QA/orbital_r7.json`
- `QA/camp_r8.json`
- `QA/temporal_r12.json`
- `QA/terrain_r14.json`
- `QA/material_r15.json`
- `QA/service_r19.json`
- `TEMPORAL_CONTRACT.md`
- `TERRAIN_CONTRACT.md`
- `MATERIAL_CONTRACT.md`
- `SERVICE_ROUTING_CONTRACT.md`
- reconstructors under `art_source/aurora_veil/blender/`.

## Rev19 architecture/routing facts

- proof root pad-plane Z: 9.632 m;
- terrain under proof pads: 8.426–9.438 m;
- 20 pads; 19 adjustable piers 0.109–0.982 m;
- floor bottom examples: +0.710 to +1.427 m over terrain;
- clock base embeds 0.08 m; beacons 0.05 m;
- power route: 14.155 m, 0.65–2.951 m terrain clearance;
- data A/B: 77.621 / 77.549 m, exactly +0.45 m at 14 control points;
- 4 shared-mesh cable stakes; no source object in routing collection;
- final electrical class and bend-elbow production geometry remain pending.

## Next critical path

1. **AUR/AEON/050** — hero primary/secondary forms derived from canon, arena clearances and temporal mechanics.
2. AUR/AEON/051 — manufacturing/construction articulation after form gate.
3. AUR/AEON/052 — rig/attack-clearance interfaces after construction gate.
4. Then return to ecology/population depth and optimization.

## Stop condition

Claim remains KEEP / IN_PROGRESS. Do not mark world DONE while P0/P1 remain, HUMAN GATE-ART/runtime/performance are unresolved, or production assets lack applicable topology/material/LOD/integration gates.
