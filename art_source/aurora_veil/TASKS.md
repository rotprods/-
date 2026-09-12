# AURORA VEIL — TASK SYSTEM

**Agent:** AGENT-02-AURORA  
**Session:** AURORA-20260912T192957Z-001  
**Claim:** CLM-AURORA-WORLD-001  
**Branch:** art/world-aurora-veil-001  

## North Star

Deliver AURORA VEIL as a complete, physically plausible, unmistakable EXOVANT world package, with planet-scale metadata, three canonical regions, temporal visual grammar, ecology/population, AEON, world-specific asset library, streaming/collision/export strategy, receipts and cold-resume documentation.

## First 10 tasks

### AUR/WORLD/001 — Atomic ownership claim
- Priority: P0
- Owner: AGENT-02-AURORA
- Output: `production/claims/aurora/CLM-AURORA-WORLD-001.yaml`
- Dependencies: current branch/PR/claim audit
- DoD:
  - no observed Aurora branch/PR before claim;
  - includes/excludes explicit;
  - branch and base SHA recorded;
  - claim persisted before Blender build.
- Status: DONE
- Evidence: commit `096745b1305ead0e9b5d04ffdd74b1633bdba300`

### AUR/WORLD/002 — World Bible + scale ADR
- Priority: P0
- Output: `WORLD_BIBLE.md`, `ADR-AUR-001-planet-scale.md`
- Dependencies: AUR/WORLD/001
- DoD:
  - canon/proposal/unknown separated;
  - 0.94 g and 11 °C preserved;
  - local metre-scale coordinate contract defined;
  - proposed radius isolated and reversible;
  - art/realism/temporal contracts documented.
- Status: IN_PROGRESS

### AUR/WORLD/003 — L1 orbital representation blockout
- Priority: P0
- Output: editable Blender orbital shell + GLB + inspection render
- Dependencies: AUR/WORLD/002
- DoD:
  - shell references proposed radius only as metadata;
  - atmosphere and aurora are separate objects/layers;
  - low/mid-frequency topology only;
  - no hero geometry baked onto planet mesh;
  - export succeeds without absolute-path dependencies.
- Status: TODO

### AUR/WORLD/004 — Macro map + regional anchor contract
- Priority: P0
- Output: three regional anchors, macro terrain composition, coordinate metadata
- Dependencies: AUR/WORLD/002
- DoD:
  - Campamento/Llanura/Huerto have stable IDs;
  - region distances and silhouettes support traversal hierarchy;
  - landmarks readable from neighboring region vistas;
  - local tangent frames documented;
  - no engine-specific streaming feature falsely claimed.
- Status: TODO

### AUR/TERRAIN/005 — Three-region terrain macro blockout
- Priority: P0
- Output: metre-scale terrain blockout spanning all three canonical regions
- Dependencies: AUR/WORLD/004
- DoD:
  - macro topography before microdetail;
  - traversable slopes and route corridors identified;
  - prairie negative space preserved;
  - hero-zone boundaries represented;
  - material assignment semantic, not noise-driven.
- Status: TODO

### AUR/ARCH/006 — Campamento observatory/refuge foundation kit
- Priority: P1
- Output: modular observatory/refuge blockout kit and constructed proof scene
- Dependencies: AUR/WORLD/005
- DoD:
  - structural load path plausible;
  - foundations, access, maintenance and cable routing present;
  - modular grid/pivots documented;
  - one real assembled observatory building proves the kit;
  - human scale reference PASS.
- Status: TODO

### AUR/TEMPORAL/007 — Bounded echo visual grammar prototype
- Priority: P0
- Output: three bounded echo-sector examples with stable source/repeat state IDs
- Dependencies: AUR/WORLD/005
- DoD:
  - one delay rule per sector;
  - duplicated state never duplicates whole world;
  - pre-effect cue readable through shape/motion/sound contract, not color only;
  - collision policy specified for each state;
  - persistence explicitly local vs save-state.
- Status: TODO

### AUR/AEON/008 — Huerto + canonical 50 m AEON arena blockout
- Priority: P1
- Output: 50 m arena, three echo sectors, orchard-machine kit, AEON scale envelope
- Dependencies: AUR/TEMPORAL/007
- DoD:
  - 50 m diameter measured;
  - exactly three primary sector contracts in prototype;
  - combat floor and exits remain legible;
  - AEON can occupy all proposed phases without camera collision;
  - local timeline does not rewrite global save state.
- Status: TODO

### AUR/ECO/009 — Ecology + population scale lineup
- Priority: P1
- Output: scale/silhouette blockouts for 4 species, 3 NPCs, 3 adversaries and Peregrino variant
- Dependencies: AUR/WORLD/005
- DoD:
  - every organism has ecological/behavioral role metadata;
  - silhouettes differentiated without materials;
  - canonical function represented;
  - human/vehicle scale comparisons included;
  - final anatomy/detail not falsely claimed.
- Status: TODO

### AUR/TECH/010 — Export / collision / streaming / QA receipts
- Priority: P0
- Output: validation report, `.blend`, GLB, collision proxies, streaming-cell metadata, renders
- Dependencies: AUR/WORLD/003..009 as applicable
- DoD:
  - Blender scene query validates objects, dimensions and materials;
  - portable export succeeds;
  - no missing dependencies;
  - separate collision strategy demonstrated;
  - visual evidence generated from delivery camera;
  - target-engine import/perf remains BLOCKED until appropriate engine/hardware gate if unavailable.
- Status: TODO

---

## Multi-week production backlog

### WAVE 1 — MACRO WORLD
- AUR/MAP/011 global height/biome mask concept from canonical constraints
- AUR/MAP/012 Campamento regional terrain pass
- AUR/MAP/013 Llanura regional terrain pass
- AUR/MAP/014 Huerto regional terrain pass
- AUR/VISTA/015 inter-region skyline and landmark proxies

### WAVE 2 — KIT FOUNDATIONS
- AUR/MAT/020 world material calibration board
- AUR/ARCH/021 refuge modules
- AUR/ARCH/022 observatory ring modules
- AUR/ARCH/023 service/utility modules
- AUR/INFRA/024 route-recorder beacons
- AUR/INFRA/025 clock-sync stations
- AUR/PROC/026 prairie scatter/variation system
- AUR/PROC/027 cable and instrument routing generator

### WAVE 3 — WORLD POPULATION
- AUR/PROP/030 camp functional props
- AUR/PROP/031 market-clock props
- AUR/ECO/032 two-shadow grass family
- AUR/ECO/033 chronobutterfly family
- AUR/ECO/034 aurora antelope family
- AUR/ECO/035 interval wasp/nest family
- AUR/NPC/036 Ada Nox
- AUR/NPC/037 Julián Ré
- AUR/NPC/038 Cea Hora
- AUR/ENEMY/039 delayed custodian
- AUR/ENEMY/040 future looter
- AUR/ENEMY/041 broken antelope
- AUR/VEH/042 Peregrino route-recorder variant

### WAVE 4 — HERO CONTENT
- AUR/AEON/050 AEON primary/secondary forms
- AUR/AEON/051 AEON mechanical construction pass
- AUR/AEON/052 AEON rig interface and attack clearance
- AUR/LANDMARK/053 primary observatory hero landmark
- AUR/LANDMARK/054 orchard state-preservation tree

### WAVE 5 — DETAIL & STORYTELLING
- AUR/STORY/060 accident echo set
- AUR/STORY/061 trapped-explorer rescue site
- AUR/STORY/062 temporal archive consequence states
- AUR/DECAL/063 maintenance/index marking system
- AUR/WEAR/064 causal wear masks and authored grime
- AUR/DEST/065 authored damaged-state variants

### WAVE 6 — OPTIMIZATION
- AUR/LOD/070 hero LOD policy
- AUR/LOD/071 architecture HLOD proxies
- AUR/LOD/072 vegetation/fauna distance strategy
- AUR/COLL/073 collision simplification pass
- AUR/STREAM/074 streaming cell/HLOD hierarchy
- AUR/PERF/075 measured budget table on target hardware

### WAVE 7 — INTEGRATION
- AUR/INT/080 import into selected production engine
- AUR/INT/081 scale/material/collision validation
- AUR/INT/082 temporal-state integration contract
- AUR/INT/083 mission-route instantiation
- AUR/INT/084 profiling and regression captures

### WAVE 8 — AAAA POLISH
- AUR/ART/090 silhouette/readability review
- AUR/ART/091 material calibration review
- AUR/ART/092 art-drift gauntlet
- AUR/QA/093 near/mid/far camera review
- AUR/QA/094 full World DoD audit
- AUR/HANDOFF/095 cold-resume package and final handoff

## Stop condition

Do not mark world DONE while any P0/P1 is open, export/import is unverified where required, a hero asset lacks a manifest, QA fails, art drift remains, or a cross-scope dependency is undocumented.
