# SYLVA PRIME — Macro / Terrain / Regional Foundation

**Agent:** `AGENT-SYLVA-MACRO-01`  
**Session:** `20260912-SYLVA-MACRO-001`  
**Claim:** `CLM-SYLVA-MACRO-001`  
**Branch:** `art/world-sylva-prime-macro-001`  
**Base:** `4c2fa044080004609ea6df45f34b2a784536507a`  
**Status:** `IN_PROGRESS / WAVE 0→1`

## North Star
Deliver the metric-scale, reproducible spatial foundation for SYLVA PRIME: canonical regions, macro terrain/root structure, readable traversal corridors, landmark silhouettes and interfaces that allow later terrain, architecture, ecology and encounter teams to work without changing global scale or duplicating assets.

## Evidence classification

| Field | Value | Class |
|---|---|---|
| World | SYLVA PRIME | CANON |
| Galaxy | ANDROMEDA | CANON |
| System | Dendra | CANON |
| Faction | Coro Micelial | CANON |
| Gravity | 1.12 g, revised proposal | DOCUMENTED |
| Temperature reference | 34 C | DOCUMENTED |
| Region 1 | Puerto del Injerto | CANON |
| Region 2 | Bosque de las Frases | CANON |
| Region 3 | Camara de VESPER | CANON |
| Art kit | structural roots, membranes, graft scaffolds, layered foliage | CANON |
| Planet radius/diameter | UNKNOWN | BLOCKED |
| Global continental layout | UNKNOWN | BLOCKED |
| Blender remote workflow | Higgsfield 3D Jutsu / bpy, Blender 5.2 LTS observed in current service | OBSERVED |
| Local blockout envelope | 12 km × 12 km working patch | PROPOSAL |
| Local units | 1 Blender Unit = 1 metre | PROPOSAL compatible with repo metric art practice; verify engine import |

## Local art-direction contract

- **Shape:** load-bearing root arches and branching tension paths dominate; human intervention appears as graft clamps, narrow scaffolds and surgical interfaces rather than generic sci-fi panels.
- **Proportion:** living structures are oversized relative to humans; traversable routes remain legible through repeated clearances, guard edges and scale references.
- **Silhouette:** each region must read without materials: grafted port / branching sentence forest / descending VESPER knot.
- **Material causality:** bark/fiber compresses and splits along growth; membranes sag/tension; human graft hardware shows clamp pressure, repair history and moisture exposure.
- **Forbidden drift:** random greeble, purple-alien-fantasy shorthand, decorative roots with no load/growth logic, uniformly glowing vegetation, arbitrary scratches or noise.

## First 10 tasks

### SYLVA/MACRO/001 — Evidence pack
- Priority: P0
- Output: claim, authority list, canon/unknown/proposal split.
- Dependencies: none.
- DoD: branch + persistent claim + draft PR + source list all exist and no semantic ownership collision is found.
- Status: DONE.

### SYLVA/MACRO/002 — Coordinate and scale contract
- Priority: P0
- Output: metre-scale local origin, region anchors, scale references, planet/local separation.
- Dependencies: 001.
- DoD: Blender scene stores units, origin policy, proposed working envelope and UNKNOWN planet radius without silently assigning a value.
- Status: TODO.

### SYLVA/MACRO/003 — World-bible delta
- Priority: P0
- Output: macro-only world bible containing known geography, traversal logic, art pillars, material/process logic and blocking decisions.
- Dependencies: 001.
- DoD: every field is classified CANON/DOCUMENTED/INFERRED/PROPOSAL/BLOCKED; no unsupported planetary fact is promoted.
- Status: TODO.

### SYLVA/MACRO/004 — Macro terrain blockout
- Priority: P0
- Output: low-frequency authored terrain/forest-floor substrate for the proposed 12 km × 12 km local patch.
- Dependencies: 002.
- DoD: continuous scale-correct mesh, deterministic generator, no high-frequency sculpting, three region anchors fit without terrain intersections that invalidate traversal.
- Status: TODO.

### SYLVA/MACRO/005 — Structural root network
- Priority: P0
- Output: primary root arches, trunks and load/growth corridors connecting regions.
- Dependencies: 004.
- DoD: roots have hierarchical radii, plausible branching, no random spaghetti crossings on primary routes, and at least one uninterrupted macro path between each adjacent region.
- Status: TODO.

### SYLVA/MACRO/006 — Puerto del Injerto foundation
- Priority: P1
- Output: enclave massing embedded in living tissue, graft scaffold language and approach landmark.
- Dependencies: 004,005.
- DoD: region readable in silhouette, human scale demonstrable, entry/exit corridors distinct, no final architecture ownership consumed.
- Status: TODO.

### SYLVA/MACRO/007 — Bosque de las Frases foundation
- Priority: P1
- Output: branching route field whose spatial grammar can support learned warning/permission signals.
- Dependencies: 004,005.
- DoD: minimum three route choices with distinguishable root/membrane landmarks; navigation remains legible without relying only on color.
- Status: TODO.

### SYLVA/MACRO/008 — Camara de VESPER envelope
- Priority: P1
- Output: descent volume and boss-space envelope only; final VESPER excluded.
- Dependencies: 004,005.
- DoD: arena/descent scale is explicit, camera/nav clearances are measurable, and no boss final mesh/rig is created.
- Status: TODO.

### SYLVA/MACRO/009 — Traversal / scale / collision QA
- Priority: P0
- Output: diagnostic human-scale references, slopes/clearances report, proxy collision policy and orthographic/perspective evidence.
- Dependencies: 006,007,008.
- DoD: no primary path narrower than the declared proxy clearance; all three regions can be traced through local coordinates; render and geometry metrics recorded.
- Status: TODO.

### SYLVA/MACRO/010 — Portable export + handoff
- Priority: P0
- Output: committed `.blend`, deterministic bpy generator, GLB, validation JSON, preview render, status/handoff.
- Dependencies: 009.
- DoD: portable export resolves, artifact counts and dimensions recorded, files/receipts referenced from branch; engine import remains explicitly pending until runtime gate executes.
- Status: TODO.

## Blocking decisions

### BLOCK-SYLVA-001 — Planetary physical radius
- decision_needed: Canon radius/diameter for SYLVA PRIME if required by orbital representation.
- affected_scope: L0 planetary canon and later orbital LOD only.
- why_blocking: A 1:1 planet sphere cannot be physically specified without an approved radius.
- options: author canonical radius; derive from later astrophysical/world-design pass; keep regional work decoupled.
- recommended_option: keep regional work decoupled now; approve radius in a dedicated world-scale ADR before L1 orbital production.
- reversibility: high while no L1 sphere is committed.
- work_that_can_continue: all local L2–L4 macro/regional foundation work.

## Progress

- Asset coverage: 0% final / blockout pipeline started
- Modeling: 0% before Blender commit
- Materials: 0% final; diagnostic materials only in this claim
- Optimization: 0% final; proxy strategy defined
- Integration: 0% engine; branch integration isolated
- QA: claim collision audit PASS; Blender/geometry/export pending
- P0 open: 6
- P1 open: 3
- P2 open: 0
- P3 open: 0
