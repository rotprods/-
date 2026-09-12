# AURORA VEIL — TASK SYSTEM

**Agent:** AGENT-02-AURORA  
**Session:** AURORA-20260912T192957Z-001  
**Claim:** CLM-AURORA-WORLD-001  
**Branch:** art/world-aurora-veil-001  
**Remote checkpoint:** 3D Jutsu `d6488148-8547-4ffe-b63d-e5fbec3a339c` revision 7  

## North Star

Deliver AURORA VEIL as a complete, physically plausible, unmistakable EXOVANT world package, with planet-scale metadata, three canonical regions, temporal visual grammar, ecology/population, AEON, world-specific asset library, streaming/collision/export strategy, receipts and cold-resume documentation.

## First 10 tasks — current state

| ID | Priority | Status | Current evidence / remaining DoD |
|---|---|---|---|
| AUR/WORLD/001 Atomic ownership claim | P0 | DONE | Claim persisted before Blender. Commit `096745b1305ead0e9b5d04ffdd74b1633bdba300`. |
| AUR/WORLD/002 World Bible + scale ADR | P0 | DONE | `WORLD_BIBLE.md`, `ADR-AUR-001-planet-scale.md`; canon/proposal boundary explicit. |
| AUR/WORLD/003 L1 orbital representation | P0 | REVIEW | Remote rev 7: separate `AUR-PLN-001` shell + `AUR-ATM-001` atmosphere/4 ribbons, 2 canonical station proxies, GLB PASS, no global geography invented, surface camera regression delta 0. Human visual review remains open. |
| AUR/WORLD/004 Macro map + regional anchors | P0 | REVIEW | 3 anchors + 5.2×3.0 km local macro frame exist; global macro/continent geography intentionally remains UNKNOWN rather than invented. |
| AUR/TERRAIN/005 Three-region terrain macro | P0 | REVIEW | Low-frequency terrain exists; geology/erosion/traversal refinement and final region tiling pending. |
| AUR/ARCH/006 Camp observatory/refuge kit | P1 | IN_PROGRESS | 48 m ring, 72 m mast, habitats and sync stations exist as blockout; manufacturing-complete modular kit and assembled proof need production pass. |
| AUR/TEMPORAL/007 Bounded echo grammar | P0 | IN_PROGRESS | 3 fields, 12 anchors, delayed source/state geometry exist; runtime collision/audio/state schema pending. |
| AUR/AEON/008 Huerto + 50 m arena | P1 | REVIEW_BLOCKOUT | Canon 50 m arena + 3 sectors + 10 machine trees + AEON blockout exist; final hero design/rig/readability pending. |
| AUR/ECO/009 Ecology/population lineup | P1 | IN_PROGRESS | Semantic proxies exist for NPC/enemies/fauna/Peregrino; final anatomy/silhouette/art approval pending. |
| AUR/TECH/010 Export/collision/streaming/QA | P0 | IN_PROGRESS | Blend/GLB export PASS through rev 7, 4 collision proxies, 27 planning cells, scale + photometric + surface-regression QA PASS; engine import/perf/human art gate pending. |

## Stable DoD references

### AUR/WORLD/003
- editable Blender orbital shell + portable exchange artifact;
- radius only referenced as `PROPOSAL` until accepted;
- atmosphere/aurora separate;
- no hero geometry on orbital mesh;
- coordinate link to local region anchors documented;
- no global geography invented where canon is silent;
- surface-region visual regression remains unchanged after orbital insertion.

### AUR/WORLD/004
- Campamento/Llanura/Huerto stable IDs;
- macro distances and vista hierarchy defined;
- local tangent frames preserved;
- no false engine-specific streaming claim.

### AUR/TERRAIN/005
- macro elevation and geological logic before microdetail;
- route corridors/slopes reviewed;
- material distribution semantic;
- hero-zone edges and region tiling documented.

### AUR/ARCH/006
- plausible foundations/load paths;
- maintenance access, utilities, drainage/cabling;
- grid, pivots, variants and transitions documented;
- one assembled production structure proves kit;
- human-scale QA.

### AUR/TEMPORAL/007
- one temporal rule per initial encounter sector;
- local state variants only;
- non-color-only anticipation cue;
- explicit per-state collision and persistence;
- readable delay contract.

### AUR/AEON/008
- 50 m arena exact;
- three primary echo sectors;
- combat floor/exits/camera readability;
- AEON phase-clearance and attack telegraph review;
- local arena timeline cannot mutate global save state.

### AUR/ECO/009
- each organism has ecology/behavior metadata;
- silhouettes differentiated without materials;
- canonical roles represented;
- scale lineups and LOD/crowd policies;
- final anatomy not claimed from proxies.

### AUR/TECH/010
- source/editable artifact;
- portable export;
- dimensions/material/object inventory;
- separate collision;
- LOD/HLOD strategy;
- renders/visual regression baseline;
- engine import and target-hardware performance before DONE.

---

## Multi-week production backlog

### WAVE 1 — MACRO WORLD
- AUR/MAP/011 — global height/biome mask concept from canonical constraints — DEFERRED_UNTIL_GLOBAL_GEOGRAPHY_DECISION
- AUR/MAP/012 — Campamento regional terrain pass — IN_PROGRESS
- AUR/MAP/013 — Llanura regional terrain pass — IN_PROGRESS
- AUR/MAP/014 — Huerto regional terrain pass — IN_PROGRESS
- AUR/VISTA/015 — inter-region skyline / landmarks — IN_PROGRESS

### WAVE 2 — KIT FOUNDATIONS
- AUR/MAT/020 — calibrated world material board — TODO
- AUR/ARCH/021 — refuge modules — TODO
- AUR/ARCH/022 — observatory ring modules — IN_PROGRESS
- AUR/ARCH/023 — service / utility modules — TODO
- AUR/INFRA/024 — route-recorder beacons — TODO
- AUR/INFRA/025 — clock-sync stations — IN_PROGRESS_BLOCKOUT
- AUR/PROC/026 — prairie scatter / variation system — TODO
- AUR/PROC/027 — cable / instrument routing generator — TODO

### WAVE 3 — WORLD POPULATION
- AUR/PROP/030 — camp functional props — TODO
- AUR/PROP/031 — market-clock props — TODO
- AUR/ECO/032 — two-shadow grass family — IN_PROGRESS_BLOCKOUT
- AUR/ECO/033 — chronobutterfly — IN_PROGRESS_BLOCKOUT
- AUR/ECO/034 — aurora antelope — IN_PROGRESS_BLOCKOUT
- AUR/ECO/035 — interval wasp / nest — IN_PROGRESS_BLOCKOUT
- AUR/NPC/036 — Ada Nox — IN_PROGRESS_PROXY
- AUR/NPC/037 — Julián Ré — IN_PROGRESS_PROXY
- AUR/NPC/038 — Cea Hora — IN_PROGRESS_PROXY
- AUR/ENEMY/039 — delayed custodian — IN_PROGRESS_PROXY
- AUR/ENEMY/040 — future looter — IN_PROGRESS_PROXY
- AUR/ENEMY/041 — broken antelope — IN_PROGRESS_PROXY
- AUR/VEH/042 — Peregrino route-recorder — REVIEW_BLOCKOUT

### WAVE 4 — HERO CONTENT
- AUR/AEON/050 — AEON primary/secondary forms — IN_PROGRESS_BLOCKOUT
- AUR/AEON/051 — AEON mechanical construction — TODO
- AUR/AEON/052 — AEON rig/attack-clearance interfaces — TODO
- AUR/LANDMARK/053 — primary observatory hero landmark — IN_PROGRESS_BLOCKOUT
- AUR/LANDMARK/054 — orchard state-preservation machine tree — IN_PROGRESS_BLOCKOUT

### WAVE 5 — DETAIL & STORYTELLING
- AUR/STORY/060 — accident echo set — TODO
- AUR/STORY/061 — trapped-explorer rescue site — TODO
- AUR/STORY/062 — temporal archive consequence states — IN_PROGRESS_BLOCKOUT
- AUR/DECAL/063 — maintenance/index markings — TODO
- AUR/WEAR/064 — causal wear masks — TODO
- AUR/DEST/065 — authored damaged-state variants — TODO

### WAVE 6 — OPTIMIZATION
- AUR/LOD/070 — hero LOD policy — TODO
- AUR/LOD/071 — architecture HLOD proxies — TODO
- AUR/LOD/072 — vegetation/fauna distance strategy — TODO
- AUR/COLL/073 — collision simplification — IN_PROGRESS_BLOCKOUT
- AUR/STREAM/074 — streaming/HLOD hierarchy — IN_PROGRESS_PLANNING
- AUR/PERF/075 — measured target-hardware budget table — BLOCKED_TARGET_HARDWARE

### WAVE 7 — INTEGRATION
- AUR/INT/080 — production engine import — BLOCKED_EXO_012
- AUR/INT/081 — engine scale/material/collision validation — BLOCKED_EXO_012
- AUR/INT/082 — temporal-state integration — BLOCKED_ENGINE_INTERFACE
- AUR/INT/083 — mission-route instantiation — BLOCKED_ENGINE_INTERFACE
- AUR/INT/084 — profiling/regression captures — BLOCKED_TARGET_RUNTIME

### WAVE 8 — AAAA POLISH
- AUR/ART/090 — silhouette/readability review — TODO
- AUR/ART/091 — material calibration review — TODO
- AUR/ART/092 — art-drift gauntlet — TODO
- AUR/QA/093 — near/mid/far camera review — TODO_HUMAN
- AUR/QA/094 — full World DoD audit — TODO
- AUR/HANDOFF/095 — final cold-resume package — TODO_FINAL

## Stop condition

The claim remains KEEP / IN_PROGRESS. Do not mark AURORA DONE while any P0/P1 remains open, GATE-ART is pending, production-engine import is blocked, performance is unmeasured, final hero assets lack production topology/materials/LOD, or the radius proposal has not been resolved explicitly.
