# AURORA VEIL — STATUS PACK

**AGENT:** AGENT-02-AURORA  
**SESSION:** AURORA-20260912T192957Z-001  
**CLAIM:** CLM-AURORA-WORLD-001  
**BRANCH:** `art/world-aurora-veil-001`  
**REMOTE 3D PROJECT:** `d6488148-8547-4ffe-b63d-e5fbec3a339c`  
**REMOTE REVISION:** `7`  
**STATUS:** `IN_PROGRESS — WAVE 1 MACRO + ORBITAL BLOCKOUT QUALIFIED, NOT FINAL ART`  

## Current coverage

| Area | State | Receipt |
|---|---|---|
| Claim / ownership | DONE | `096745b1305ead0e9b5d04ffdd74b1633bdba300`; fleet ACK issue #7 epoch 1 |
| World Bible / Art contract | DONE | `WORLD_BIBLE.md` |
| Planet scale contract | PROPOSED / documented | `ADR/ADR-AUR-001-planet-scale.md` |
| Master Asset List | DONE for initial families | `MASTER_ASSET_LIST.yaml` |
| L1 orbital shell/atmosphere | REVIEW | remote rev 7; `QA/orbital_r7.json` |
| 3-region macro terrain | REVIEW | remote rev 7 preserves r5 surface baseline |
| Region anchors | REVIEW | remote rev 7 |
| Campamento blockout | IN_PROGRESS | remote rev 7 |
| Repetition Plain temporal grammar | IN_PROGRESS | remote rev 7 |
| AEON Orchard / arena | REVIEW blockout | remote rev 7 |
| Ecology proxies | IN_PROGRESS blockout | remote rev 7 |
| NPC/enemy proxies | IN_PROGRESS blockout | remote rev 7 |
| Peregrino variant | REVIEW blockout | remote rev 7 |
| Collision proxies | REVIEW | 4 hidden render proxies |
| Streaming planning cells | REVIEW / engine-neutral | 27 × 256 m planning cells |
| GLB export | PASS at remote rev 7 | etag `210ef84a071fb40a3b62c81d73b7b656` |
| Editable Blend | PASS at remote rev 7 | etag `7418b326a1a0745688903f0b3fc42b3e` |
| Engine import | BLOCKED | EXO-012 / production-engine decision |
| Target-hardware performance | BLOCKED | no qualified production GPU target |
| Human GATE-ART | PENDING | renders generated; no human art sign-off in this run |

## Verified surface-scene facts

- Blender worker: 5.2.
- Units: metric, 1 BU = 1 m in authored local frame.
- Macro local frame: 5,200 × 3,000 m; terrain vertical span 14.036 m in current blockout.
- Canon gravity: 0.94 g.
- Canon reference temperature: 11 °C.
- Planet radius: 5,900 km **PROPOSAL**, never promoted to canon.
- Surface checkpoint objects before orbital insertion: 329; semantic materials: 11.
- Observatory primary ring: 48.0 × 48.0 m proposal, corrected after QA mismatch.
- Observatory mast: 72.0 m proposal.
- AEON arena: 50.0 m diameter **CANON**.
- Peregrino blockout: 5.8 × 2.7 × 2.4 m proposal, corrected after QA mismatch.
- Bounded temporal anchors: 12 across three prototype fields.
- AEON echo sectors: exactly 3.
- Orchard machine-tree blockouts: 10.
- Streaming planning cells: 27.
- Separate collision proxies: 4, all hidden from render.

## Verified L1 orbital facts — r7

- `AUR-PLN-001`: shell 1,180 m display diameter, 2,562 vertices / 5,120 polygons.
- `AUR-ATM-001`: separate atmosphere shell ~1,205.96 m display diameter, 4,514 vertices / 4,608 polygons.
- 4 independent aurora ribbons; no shader-only dependency required for their silhouette.
- 2 observation-station proxies, matching canon; precise orbit altitude remains proposal.
- Physical radius metadata: 5,900,000 m **PROPOSAL**; display scale `1e-4`.
- Global continental geography: `UNKNOWN_NOT_AUTHORED`.
- Lighting: one scene-global `SUN_VELAR_LOW`; no AREA lights.
- Orbital render `aurora_r7_orbital_l1.png`: artifact `46c6e0a6451b54fcef6cd1b5c3d2346e`, 480×270, mean 0.1114, no black/white clipping.
- Surface regression after orbital insertion: world-overview mean 0.1793 vs r5 baseline 0.1793, delta `0.0000`.

## QA outcomes

### PASS
- claim ID preserved in scene;
- metre scale preserved for local gameplay frame;
- physical-vs-display orbital scale explicit;
- global geography not fabricated;
- separate planet/atmosphere/aurora layers;
- two canonical observation-station proxies;
- 48 m observatory ring matched after correction;
- 50 m AEON arena matched;
- Peregrino dimensions matched after correction;
- exactly three AEON echo sectors;
- collision proxies excluded from beauty render;
- streaming debug cells excluded from beauty render;
- portable light types only;
- macro overview camera far clip corrected to 12,000 m;
- L1 orbital package causes zero measured surface-overview exposure regression.

### FAILURE / FIX HISTORY
1. Monolithic first build timed out at 300 s → pipeline split into staged mutations; successful foundation and population/orchard stages then completed in ~10–12 s each.
2. Initial observatory ring exported 50.6 m instead of proposed 48 m → corrected to 48.0 m.
3. Initial Peregrino body exported 6.0 × 2.9 × 2.5 m vs manifest 5.8 × 2.7 × 2.4 m → corrected.
4. Overview camera rendered effectively sky-only because default far clip was ~1 km while the camera was ~4.9 km from target → far clip corrected to 12 km.
5. First pixel-audit script used an empty `Render Result` buffer and failed with division-by-zero → replaced with explicit temporary PNG load.
6. Orbital r6 initially added a second `SUN`; because SUN lights are scene-global this risked surface regression → removed in r7 and validated against r5 baseline.

### Exposure receipts
Surface revision-5 baseline and revision-7 regression:

| Camera | Mean | P01 | P50 | P99 | Black clip | White clip |
|---|---:|---:|---:|---:|---:|---:|
| World overview | 0.1793 | 0.0410 | 0.1822 | 0.8541 | 0 | 0 |
| Camp | 0.1724 | 0.0410 | 0.1909 | 0.4925 | 0 | 0 |
| AEON | 0.1988 | 0.0185 | 0.1912 | 0.8583 | 0.0047 | 0 |
| Orbital L1 r7 | 0.1114 | 0.0410 | 0.1056 | 0.2457 | 0 | 0 |

These statistics prove non-empty exposure/framing, **not artistic approval**.

## Progress metrics

Metrics describe this claim checkpoint, not the whole finished world.

- Asset coverage: initial families inventoried; macro and L1 orbital families now have actual scene representation, but most final assets remain TODO.
- Modeling: macro + orbital blockout established; hero production topology not started.
- Materials: semantic blockout/material-role layer only; calibrated final PBR/texture work not started.
- Optimization: planning cells + separate collision established; real LOD/HLOD/perf not qualified.
- Integration: GLB exchange succeeds through rev 7; production-engine import blocked.
- QA: dimensional/export/photometric/regression checks active; human art gate pending.

Open critical path after AUR/WORLD/003:
- P0: production-grade terrain qualification; bounded temporal state productionization; LOD/HLOD contract; engine/perf gates.
- P1: calibrated material foundations; modular architecture; ecology/characters/enemies/vehicle production; AEON hero production.

## NEXT

1. AUR/ARCH/021–023 / AUR/ARCH/006 — build a true modular Campamento foundation kit: structural frames, refuge shell, ring segments, utilities, pivots/grid and proof assembly.
2. AUR/MAT/020 — create calibrated material-role library aligned with construction process, not generic sci-fi surfaces.
3. AUR/TEMPORAL/007 — convert echo blockout into explicit state-variant/collision/anticipation contracts without changing global gameplay code.
