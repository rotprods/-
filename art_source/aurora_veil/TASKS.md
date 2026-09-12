# AURORA VEIL — TASK SYSTEM

**Agent:** AGENT-02-AURORA  
**Session:** AURORA-20260912T192957Z-001  
**Claim:** CLM-AURORA-WORLD-001  
**Branch:** art/world-aurora-veil-001  
**Remote checkpoint:** 3D Jutsu `d6488148-8547-4ffe-b63d-e5fbec3a339c` revision 12  

## North Star

Deliver AURORA VEIL as a complete, physically plausible, unmistakable EXOVANT world package, with planet-scale metadata, three canonical regions, temporal visual grammar, ecology/population, AEON, world-specific asset library, streaming/collision/export strategy, receipts and cold-resume documentation.

## First 10 tasks — current state

| ID | Priority | Status | Current evidence / remaining DoD |
|---|---|---|---|
| AUR/WORLD/001 Atomic ownership claim | P0 | DONE | Claim persisted before Blender; Fleet ACK issue #7 epoch 1. |
| AUR/WORLD/002 World Bible + scale ADR | P0 | DONE | Canon/proposal/unknown boundary documented. |
| AUR/WORLD/003 L1 orbital representation | P0 | REVIEW | Orbital/atmosphere layers, station proxies, export and surface regression PASS; human visual review open. |
| AUR/WORLD/004 Macro map + regional anchors | P0 | REVIEW | 3 stable region anchors + 5.2×3.0 km local frame; global continents intentionally UNKNOWN. |
| AUR/TERRAIN/005 Three-region terrain macro | P0 | IN_PROGRESS | Low-frequency terrain exists; next gate is quantified geology/erosion/traversal qualification without invalidating current anchors. |
| AUR/ARCH/006 Camp observatory/refuge kit | P1 | REVIEW_TECHNICAL | Rev 8+: 4 m grid, manufacturing-aware modular source library, 16×12 m proof refuge, 24-segment 48 m ring, export/regression PASS. Final art/UV/PBR/human review open. |
| AUR/TEMPORAL/007 Bounded echo grammar | P0 | REVIEW_TECHNICAL | Rev 12: deterministic 5-state local contract, 3 fields, 6 hidden collision proxies, 3 AEON sectors, legacy hidden, global rewind/save mutation forbidden. Runtime/sound/human comprehension open. |
| AUR/AEON/008 Huerto + 50 m arena | P1 | REVIEW_BLOCKOUT | Canon 50 m arena + exactly 3 sectors + orchard/AEON blockout. Final hero design/rig/readability pending. |
| AUR/ECO/009 Ecology/population lineup | P1 | IN_PROGRESS | Semantic proxies exist; final anatomy/silhouette/LOD/art approval pending. |
| AUR/TECH/010 Export/collision/streaming/QA | P0 | IN_PROGRESS | Blend/GLB exchange PASS through rev 12; collision/streaming contracts and multiple QA baselines active; engine/perf/human gates remain. |

## Key DoD references

### AUR/TERRAIN/005
- macro elevation and geological logic before microdetail;
- measurable region slopes and traversal corridors;
- Campamento/Llanura/Huerto terrain intent differentiated by shape, not material noise alone;
- current placed hero anchors remain grounded after terrain refinement;
- hero-zone edges and future tiling documented;
- no global geography fabricated where canon is silent.

### AUR/ARCH/006
- plausible foundations/load paths;
- 4 m grid/pivots/variants;
- instanced source meshes;
- manufacturing causality and service access;
- real proof structure;
- human art review before DONE.

### AUR/TEMPORAL/007
- state order `IDLE → PRE_CUE → REPEAT_ARMED → REPEAT_ACTIVE → COOLDOWN`;
- one bounded rule/delay per local field/sector;
- non-color-only anticipation cue;
- collision enabled only for local `REPEAT_ACTIVE` proxy when required;
- encounter/arena-local persistence only;
- global rewind and save-state mutation forbidden;
- runtime/sound/comprehension qualification before DONE.

### AUR/TECH/010
- editable source + portable export;
- dimensions/material/object inventory;
- separate collision;
- LOD/HLOD and streaming strategy;
- visual baselines;
- native engine import and target-hardware performance before DONE.

---

## Production backlog

### WAVE 1 — MACRO WORLD
- AUR/MAP/011 global height/biome map — DEFERRED_UNTIL_GLOBAL_GEOGRAPHY_DECISION
- AUR/MAP/012 Campamento regional terrain — IN_PROGRESS
- AUR/MAP/013 Llanura regional terrain — IN_PROGRESS
- AUR/MAP/014 Huerto regional terrain — IN_PROGRESS
- AUR/VISTA/015 inter-region skyline — IN_PROGRESS

### WAVE 2 — KIT FOUNDATIONS
- AUR/MAT/020 calibrated world material board — IN_PROGRESS_ROLE_LIBRARY_R8
- AUR/ARCH/021 refuge modules — REVIEW_TECHNICAL_R8
- AUR/ARCH/022 observatory ring modules — REVIEW_TECHNICAL_R8
- AUR/ARCH/023 service/utility modules — REVIEW_TECHNICAL_R8
- AUR/INFRA/024 route-recorder beacons — REVIEW_BLOCKOUT_R8
- AUR/INFRA/025 clock-sync stations — REVIEW_BLOCKOUT_R8
- AUR/PROC/026 prairie scatter/variation — TODO
- AUR/PROC/027 cable/instrument routing — TODO

### WAVE 3 — WORLD POPULATION
- AUR/PROP/030 camp functional props — TODO
- AUR/PROP/031 market-clock props — TODO
- AUR/ECO/032 two-shadow grass — IN_PROGRESS_BLOCKOUT
- AUR/ECO/033 chronobutterfly — IN_PROGRESS_BLOCKOUT
- AUR/ECO/034 aurora antelope — IN_PROGRESS_BLOCKOUT
- AUR/ECO/035 interval wasp/nest — IN_PROGRESS_BLOCKOUT
- AUR/NPC/036 Ada Nox — IN_PROGRESS_PROXY
- AUR/NPC/037 Julián Ré — IN_PROGRESS_PROXY
- AUR/NPC/038 Cea Hora — IN_PROGRESS_PROXY
- AUR/ENEMY/039 delayed custodian — IN_PROGRESS_PROXY
- AUR/ENEMY/040 future looter — IN_PROGRESS_PROXY
- AUR/ENEMY/041 broken antelope — IN_PROGRESS_PROXY
- AUR/VEH/042 Peregrino route-recorder — REVIEW_BLOCKOUT

### WAVE 4 — HERO CONTENT
- AUR/AEON/050 AEON forms — IN_PROGRESS_BLOCKOUT
- AUR/AEON/051 AEON construction — TODO
- AUR/AEON/052 AEON rig/attack interfaces — TODO
- AUR/LANDMARK/053 observatory hero landmark — IN_PROGRESS_BLOCKOUT
- AUR/LANDMARK/054 orchard machine tree — IN_PROGRESS_BLOCKOUT

### WAVE 5 — DETAIL & STORYTELLING
- AUR/STORY/060 accident echo — TODO
- AUR/STORY/061 trapped-explorer rescue site — TODO
- AUR/STORY/062 temporal archive consequence states — IN_PROGRESS_BLOCKOUT
- AUR/DECAL/063 maintenance/index markings — TODO
- AUR/WEAR/064 causal wear — TODO
- AUR/DEST/065 authored damage states — TODO

### WAVE 6 — OPTIMIZATION
- AUR/LOD/070 hero LOD policy — TODO
- AUR/LOD/071 architecture HLOD proxies — TODO
- AUR/LOD/072 vegetation/fauna distance strategy — TODO
- AUR/COLL/073 collision simplification — IN_PROGRESS_BLOCKOUT
- AUR/STREAM/074 streaming/HLOD hierarchy — IN_PROGRESS_PLANNING
- AUR/PERF/075 measured target-hardware budget — BLOCKED_TARGET_HARDWARE

### WAVE 7 — INTEGRATION
- AUR/INT/080 engine import — BLOCKED_EXO_012
- AUR/INT/081 engine scale/material/collision — BLOCKED_EXO_012
- AUR/INT/082 temporal-state runtime — BLOCKED_ENGINE_INTERFACE
- AUR/INT/083 mission-route instantiation — BLOCKED_ENGINE_INTERFACE
- AUR/INT/084 profiling — BLOCKED_TARGET_RUNTIME

### WAVE 8 — AAAA POLISH
- AUR/ART/090 silhouette/readability — TODO
- AUR/ART/091 material calibration — TODO
- AUR/ART/092 art-drift gauntlet — TODO
- AUR/QA/093 near/mid/far human camera review — TODO_HUMAN
- AUR/QA/094 full World DoD — TODO
- AUR/HANDOFF/095 final cold-resume — TODO_FINAL

## Stop condition

Claim remains KEEP / IN_PROGRESS. No world DONE while P0/P1 remain, GATE-ART/runtime/perf are unresolved, or production assets lack their applicable topology/material/LOD/integration gates.
