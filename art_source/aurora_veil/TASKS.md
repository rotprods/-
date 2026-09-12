# AURORA VEIL — TASK SYSTEM

**Agent:** AGENT-02-AURORA  
**Session:** AURORA-20260912T192957Z-001  
**Claim:** CLM-AURORA-WORLD-001  
**Branch:** art/world-aurora-veil-001  
**Remote checkpoint:** 3D Jutsu `d6488148-8547-4ffe-b63d-e5fbec3a339c` revision 8  

## North Star

Deliver AURORA VEIL as a complete, physically plausible, unmistakable EXOVANT world package, with planet-scale metadata, three canonical regions, temporal visual grammar, ecology/population, AEON, world-specific asset library, streaming/collision/export strategy, receipts and cold-resume documentation.

## First 10 tasks — current state

| ID | Priority | Status | Current evidence / remaining DoD |
|---|---|---|---|
| AUR/WORLD/001 Atomic ownership claim | P0 | DONE | Claim persisted before Blender. Commit `096745b1305ead0e9b5d04ffdd74b1633bdba300`; Fleet ACK issue #7 epoch 1. |
| AUR/WORLD/002 World Bible + scale ADR | P0 | DONE | `WORLD_BIBLE.md`, `ADR-AUR-001-planet-scale.md`; canon/proposal boundary explicit. |
| AUR/WORLD/003 L1 orbital representation | P0 | REVIEW | Remote rev 7+: separate `AUR-PLN-001` + `AUR-ATM-001`, 4 aurora ribbons, 2 station proxies, no invented global geography, surface regression PASS. Human visual review remains open. |
| AUR/WORLD/004 Macro map + regional anchors | P0 | REVIEW | 3 anchors + 5.2×3.0 km local macro frame exist; global continent geography remains UNKNOWN by design. |
| AUR/TERRAIN/005 Three-region terrain macro | P0 | REVIEW | Low-frequency terrain exists; geology/erosion/traversal refinement and final region tiling pending. |
| AUR/ARCH/006 Camp observatory/refuge kit | P1 | REVIEW_TECHNICAL | Rev 8: 4 m grid, 12 source modules, 16×12 m refuge proof, 24-segment 48 m observatory ring, manufacturing/material-role contract, instancing and render regression PASS. Final art/UV/PBR/human review pending. |
| AUR/TEMPORAL/007 Bounded echo grammar | P0 | IN_PROGRESS | 3 fields + 12 anchors exist. Next: explicit local state machine, per-state collision proxies and non-color-only pre-cue proof; no global rewind. |
| AUR/AEON/008 Huerto + 50 m arena | P1 | REVIEW_BLOCKOUT | Canon 50 m arena + 3 sectors + 10 machine trees + AEON blockout exist; final hero design/rig/readability pending. |
| AUR/ECO/009 Ecology/population lineup | P1 | IN_PROGRESS | Semantic proxies exist for NPC/enemies/fauna/Peregrino; final anatomy/silhouette/art approval pending. |
| AUR/TECH/010 Export/collision/streaming/QA | P0 | IN_PROGRESS | Blend/GLB export PASS through rev 8, 4 world collision proxies, 27 planning cells, dimensional/photometric/regression QA active; engine import/perf/human art gate pending. |

## Stable DoD references

### AUR/WORLD/003
- editable Blender orbital shell + portable exchange artifact;
- radius only referenced as `PROPOSAL` until accepted;
- atmosphere/aurora separate;
- no hero geometry on orbital mesh;
- coordinate link to local region anchors documented;
- no global geography invented where canon is silent;
- surface-region visual regression unchanged after orbital insertion.

### AUR/ARCH/006
- plausible foundations/load paths;
- maintenance access, utilities and cable/service routing represented;
- 4 m grid, pivots, variants and transitions documented;
- modular source objects use shared mesh datablocks for repeated assembly;
- 16×12 m refuge proof scene and 48 m segmented observatory ring prove the kit;
- manufacturing process recorded for structure/envelope/floor/roof/foundation/services/ring;
- human-scale and final art review still required before DONE.

### AUR/TEMPORAL/007
- one temporal rule per initial encounter sector;
- local state variants only; global world/save rewind prohibited;
- non-color-only anticipation cue;
- explicit per-state collision and persistence;
- readable delay contract and deterministic state IDs;
- visual source/repeat geometry must be inspectable independently.

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
- AUR/MAP/011 — global height/biome mask concept — DEFERRED_UNTIL_GLOBAL_GEOGRAPHY_DECISION
- AUR/MAP/012 — Campamento regional terrain pass — IN_PROGRESS
- AUR/MAP/013 — Llanura regional terrain pass — IN_PROGRESS
- AUR/MAP/014 — Huerto regional terrain pass — IN_PROGRESS
- AUR/VISTA/015 — inter-region skyline / landmarks — IN_PROGRESS

### WAVE 2 — KIT FOUNDATIONS
- AUR/MAT/020 — calibrated world material board — IN_PROGRESS_ROLE_LIBRARY_R8
- AUR/ARCH/021 — refuge modules — REVIEW_TECHNICAL_R8
- AUR/ARCH/022 — observatory ring modules — REVIEW_TECHNICAL_R8
- AUR/ARCH/023 — service / utility modules — REVIEW_TECHNICAL_R8
- AUR/INFRA/024 — route-recorder beacons — REVIEW_BLOCKOUT_R8
- AUR/INFRA/025 — clock-sync stations — REVIEW_BLOCKOUT_R8
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
