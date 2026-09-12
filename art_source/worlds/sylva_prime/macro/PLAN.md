# SYLVA PRIME — Macro / Terrain / Regional Foundation Plan

**Agent:** `AGENT-SYLVA-MACRO-01`  
**Claim:** `CLM-SYLVA-MACRO-001`  
**Branch:** `art/world-sylva-prime-macro-001`  
**Accepted Blender:** `05dce898-753d-4ff6-a4b0-31757dc868d8` @ **r13**  
**Current state:** `IN_PROGRESS / R13 ACCEPTED / R14 READY_NOT_EXECUTED_WRITER_FENCED`

## North Star

Deliver a reproducible metre-scale macro/regional foundation for SYLVA PRIME whose terrain, region composition, traversal, streaming and provider interfaces can be integrated into a real game without inventing planetary canon or duplicating other agents' assets.

This plan covers **only** the atomic macro claim. Full-world missing families are tracked separately in `WORLD_ASSET_COVERAGE_R14.json`.

## Evidence / truth split

| Field | Value | Class |
|---|---|---|
| World | SYLVA PRIME | CANON |
| Galaxy | ANDROMEDA | CANON |
| System | Dendra | CANON |
| Faction | Coro Micelial | CANON |
| Regions | Puerto del Injerto / Bosque de las Frases / Cámara de VESPER | CANON |
| VESPER arena rule | three terraces connected by wide roots | CANON |
| Gravity | 1.12 g | DOCUMENTED |
| Temperature ref | 34 C | DOCUMENTED |
| Local patch | 12 km × 12 km | PROPOSAL |
| Planet radius | UNKNOWN; Option C 1.20 R⊕ exists only as ADR proposal | BLOCKED/PROPOSAL |
| Blender workflow | 3D Jutsu + bpy, Blender 5.2 LTS | OBSERVED |
| Current primary remote | r13 | OBSERVED/RECEIPTED |
| Production engine streaming backend | UNKNOWN | BLOCKED |
| Target hardware/performance budget | UNKNOWN | BLOCKED |

## Production tasks

### SYLVA/MACRO/001 — Evidence + ownership bootstrap
- Priority: P0
- Status: **DONE**
- Output: repo authority, claim, branch, PR #3, Linear ROT-117, collision audit.
- DoD: persistent scope and exclusions exist; PR #6 boundary explicit.
- Evidence: claim file, PR #3, issue #7.

### SYLVA/MACRO/002 — Metric coordinate / planet-local separation
- Priority: P0
- Status: **DONE_FOUNDATION**
- Output: 1 BU = 1 m local scene, 12 km patch proposal, planet radius remains separate/unknown.
- DoD: no local dimension is silently promoted to planet scale.

### SYLVA/MACRO/003 — Macro World Bible
- Priority: P0
- Status: **DONE_FOUNDATION**
- Output: `WORLD_BIBLE_MACRO.md`.
- DoD: canon/documented/proposal/blocked fields separated; art drift contract explicit.

### SYLVA/MACRO/004 — Causal macro terrain
- Priority: P0
- Status: **DONE_SOURCE_FOUNDATION**
- Output: `R6_BIOGEO_CAUSAL_MACRO_V1`.
- DoD achieved: deterministic shape; render/collision shared height function; 289 shared samples Δz = 0 m; no fake high-frequency detail.
- Still open: final terrain sculpt/material ecology belongs to later production claim(s).

### SYLVA/MACRO/005 — Macro structural-root topology
- Priority: P0
- Status: **REVIEW_DIAGNOSTIC**
- Output: 6 primary + 8 secondary macro roots.
- DoD achieved: connectivity/hierarchical radii/macro silhouette exists.
- Open: human art review; production meso detail must consume PR #6 rather than duplicate it.

### SYLVA/MACRO/006 — Puerto del Injerto foundation
- Priority: P1
- Status: **REVIEW_BLOCKOUT**
- Output: two living arches, macro deck, graft scaffold/clamps, region/collision envelope.
- Measured visible bounds: ~647 × 542 × 400 m.
- Open: final architecture/infrastructure ownership, materials, interiors, native traversal/art review.

### SYLVA/MACRO/007 — Bosque de las Frases foundation
- Priority: P1
- Status: **REVIEW_BLOCKOUT**
- Output: three route families, six root rails, six signal arches, Phrase Node/Halo, region/collision envelope.
- Measured visible bounds: ~1744 × 2388 × 186 m.
- Open: final biome/foliage/signal interaction/detail claims and human review.

### SYLVA/MACRO/008 — Cámara de VESPER macro encounter
- Priority: P0 canon
- Status: **PASS_BLOCKOUT_CANON_LAYOUT**
- Output: three terraces + two wide connectors + context proxies + collision.
- Metrics: terraces 116/124/112 m; connectors 142.215 m @ 12.178° and 145.685 m @ 12.689°; 18 m visual / 16 m collision width.
- DoD achieved: old single-floor arena removed; no precision-jump requirement; final VESPER excluded.
- Open: native controller/camera encounter test and art review.

### SYLVA/MACRO/009 — Terrain-aware navigation + collision
- Priority: P0
- Status: **PASS_SOURCE_R10 / RUNTIME_PENDING**
- Output: four stable centerlines + four manifold collision ribbons.
- Total route: 8898.294 m.
- Max grades: 18.490° / 15.131° / 7.285° / 20.530°.
- Historical r9 invalid collision retained as failure evidence; never deliver r9.
- Open: real controller, movement-mode and camera test.

### SYLVA/MACRO/010 — Portable source/export + delivery contract
- Priority: P0
- Status: **PASS_REMOTE_SOURCE / EXACT_DELIVERY_ENV_BLOCKED**
- Output: editable remote `.blend`, GLB, generators, R13 validator and import contract.
- Current r13 remote: `.blend` 2,777,367 B; GLB 1,204,308 B.
- Open: recovered SHA-256, shared fleet delivery gate, exact GLB R13 validation, native import.

### SYLVA/MACRO/011 — Root-kit consumer interface
- Priority: P0 dependency
- Status: **CONSUMER_PASS / PROVIDER_BLOCKED**
- Output: 8 typed sockets, +X forward/+Z up/metres/scale1, semantic support map.
- Provider: `CLM-SYLVA-PROC-NROOT-001` / PR #6.
- Blocker: provider sampled geometry offset 9–17.55 m from object origin + manifest/pivot contract unresolved.
- DoD: provider publishes valid manifest, normalized anchors and render/collision anchor parity; macro then re-audits read-only and instances through sockets.

### SYLVA/MACRO/012 — Physical L3 terrain partition
- Priority: P0
- Status: **DONE_SOURCE_R12**
- Output: 16 render + 16 collision 3 km tiles; monolithic sources retired.
- QA: render 285 shared seam samples Δz = 0; collision 189 samples Δz = 0.
- Open: native cell residency/unload test.

### SYLVA/MACRO/013 — World-object L3 membership
- Priority: P0
- Status: **DONE_SOURCE_R13**
- Output: `SYLVA_STREAM_MEMBERSHIP_R13` on 147 spatial objects.
- QA: 0 outside patch; 34 cross-cell; max 6 cells/object.
- Open: importer must preserve/translate metadata and verify single-source cross-cell residency.

### SYLVA/MACRO/014 — L2 hierarchy + hero residency overlay
- Priority: P1
- Status: **READY_NOT_EXECUTED_WRITER_FENCED**
- Output prepared: proposal, generator, static validator, QA, execution gate.
- Design: 4 × 6 km L2 supercells over 16 L3 cells.
- Critical rule: hero residency is **L3-only**; L2 is coverage/HLOD metadata, not full-res residency.
- Bosque: 4 L3 hero cells and all 4 L2 coverage; do not move geography and do not load all four L2 by implication.
- Blocker: fleet registry remains `reserved / ack:null`; single-writer fence active.

### SYLVA/MACRO/015 — Prefetch policy qualification
- Priority: P1
- Status: **EXPERIMENT_DESIGNED / NOT_RUNTIME_APPROVED**
- Candidates:
  - current only;
  - current + cardinal 4;
  - current + all 8;
  - directional prev/current/next route window + contextual L3 hero overlay.
- Read-only cardinality shows current+8 can reach 72.8% of current spatial objects; therefore no default is promoted.
- Output: `PREFETCH_POLICY_R14_EXPERIMENT.json`, seam probes and native test plan.
- DoD: choose least-resident policy that passes measured IO latency, visual, collision and traversal gates at required movement speeds.

### SYLVA/MACRO/016 — HLOD strategy
- Priority: P2 after runtime qualification
- Status: **PROPOSAL_READ_ONLY / GENERATION_BLOCKED**
- Evidence: uniform terrain simplification error varies radically by tile; feature-aware strategy required.
- Relative future priority: L2_X1Y1 > X0Y0 > X0Y1 > X1Y0.
- DoD: backend/hardware known; world/screen-space error, transition popping, VRAM/draw/shader cost and human vista review all pass.

### SYLVA/MACRO/017 — Native engine residency/traversal
- Priority: P0 integration
- Status: **NOT_RUN / ARTIFACT_RECOVERY_ENV_BLOCKED**
- Exact seam probes S-00..S-03 are documented in `NATIVE_STREAM_RESIDENCY_TEST_PLAN.md`.
- DoD: exact SHA-bound GLB import; resident-cell instrumentation; all seams/traversal/VESPER pass; no duplicate/missing multi-cell assets; evidence attached.

### SYLVA/MACRO/018 — Human art-direction gate
- Priority: P0 before polish/final merge
- Status: **PENDING**
- DoD: macro silhouettes, region identity, scale/readability, causal terrain/root language and forbidden-drift test approved by human art direction.

### SYLVA/MACRO/019 — Planet scale decision / L0-L1 promotion
- Priority: P0 decision before orbital production
- Status: **PROPOSAL_PENDING_DECISION**
- Option C / 1.20 R⊕ exists but is not canon.
- Orbital project remains EMPTY r0 and unregistered in fleet.
- DoD: explicit decision + fleet registration before any orbital mutation.

## Progress — atomic claim only

These values describe maturity of this macro claim, **not global Sylva completeness**:

- Canon/ownership foundation: high maturity; current boundaries explicit.
- Macro geometry/source foundation: advanced blockout/interface state, not final production art.
- Terrain streaming source: implemented and source-QA'd.
- Navigation/collision source: implemented and source-QA'd.
- Provider integration: blocked by PR #6 readiness.
- Native engine integration: not run.
- HLOD/performance: not qualified.
- Human art: not approved.
- Planetary L0/L1: proposal only.

Full-world asset coverage, including VESPER/NPC/fauna/flora/architecture/vehicle/materials/props/population/destruction, is tracked in `WORLD_ASSET_COVERAGE_R14.json` and must not be inferred as complete from this claim.

## Stop conditions

Do not mark this claim DONE while any of these remain:
- fleet writer state unresolved;
- PR #6 required but not provider-ready;
- exact binary delivery/native import unavailable;
- engine residency/traversal untested;
- human art review pending;
- final HLOD/performance unresolved where applicable;
- planetary scale accidentally promoted without decision.
