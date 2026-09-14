# STATUS — CLM-SYLVA-MACRO-001

**Agent:** `AGENT-SYLVA-MACRO-01`  
**Branch:** `art/world-sylva-prime-macro-001`  
**Primary Blender:** `05dce898-753d-4ff6-a4b0-31757dc868d8` @ **revision 22 / sceneSequence 0**  
**State:** `IN_PROGRESS / VERIFIED R18 TECHNICAL-ART CHECKPOINT`  
**Claim:** `ACTIVE / KEEP` · fleet epoch 1 / ACK published  
**Latest main synchronized:** `26ae20f5d1b47d1efa0d54b20124ed93cbc0b43e`

## Current truth

SYLVA PRIME macro foundation is a recoverable metre-scale world-production checkpoint, not final world art. It owns causal terrain, region placement, macro traversal, streaming/collision interfaces, VESPER macro layout and kilometre-scale primary-root topology/silhouette. PR #6 retains exclusive ownership of reusable meso neural-root modules.

Accepted art wave is **R18**, scene revision **22**.

## Material advance R16 → R18

R16 fixed the six primary roots' load-correlated taper while preserving centerlines. R18 completes the next macro-silhouette step: all six `SYLVA_ROOT_PRIMARY_R01..R06` are now **self-contained closed Mesh assets**, replacing the circular Curve-tube representation with a deterministic bilateral flattened structural section.

Contract: `SYLVA_MACRO_ROOT_XSEC_R18_ALL`.

Each primary root:
- 1,040 vertices / 1,026 faces;
- 0 nonmanifold edges;
- 0 degenerate faces;
- material `SYLVA_DIAG_RootFiber` retained;
- R16 taper preserved;
- original R16 Bezier controls/handles/radii serialized inside the asset for rollback/reconstruction;
- existing object ID/name, collections, transform, stream membership and owner metadata preserved;
- no helper profile scene objects required or exported.

Profiles:
- R01: width 1.10 / height 0.70 — Puerto;
- R02: 1.12 / 0.70 — Bosque;
- R03: 1.18 / 0.66 — VESPER;
- R04: 1.08 / 0.72 — network cross-root;
- R05: 1.06 / 0.74 — network cross-root;
- R06: 1.12 / 0.68 — VESPER approach.

R18 geometry fingerprint:
`7b1a4c5c1f16c6b3c1319f3da26315c8d359ce97717272c91aa5910effe00939`.

Receipt: `qa/R18_ALL_PRIMARY_ROOT_XSEC_ACCEPTANCE.json`.

### R17 experiment history retained

R17 was deliberately gated before all-root promotion:
- revision18: custom bevel helper profiles leaked into GLB → rejected;
- revision19: unlinked helper profiles were orphan-purged on `.blend` reopen → rejected;
- revision20: explicit rollback restored safe R16;
- revision21: self-contained mesh representation passed A/B on R01/R03;
- revision22: same method promoted to R02/R04/R05/R06 as R18.

Never reinterpret revision18/19 as accepted delivery states.

## R18 streaming / bounds QA

All six R18 root meshes are fully covered by their existing L3 membership. **Missing memberships: 0**.

R01 keeps the R16 conservative membership `X0Y0|X0Y1|X0Y2|X1Y0|X1Y1|X1Y2`; the final mesh physically touches only the four lower cells, so X0Y2/X1Y2 are intentional conservative extras rather than missing residency.

Retained contracts:
- terrain morphology `R6_BIOGEO_CAUSAL_MACRO_V1`;
- terrain partition `SYLVA_TERRAIN_STREAM_R12`;
- membership base `SYLVA_STREAM_MEMBERSHIP_R13` + `SYLVA_STREAM_MEMBERSHIP_R16_AMENDMENT`;
- hierarchy `SYLVA_STREAM_HIERARCHY_R14`;
- prefetch policy state `SYLVA_PREFETCH_POLICY_R15` / `RUNTIME_EXPERIMENT_REQUIRED`;
- navigation `SYLVA_NAV_R10`.

## Terrain / world partition retained

- 16 render terrain tiles @3 km;
- 16 collision terrain tiles @3 km;
- 4 L2 supercells / 16 L3 cells;
- R12 seam QA remains Δz = 0 m on 285 render + 189 collision shared samples;
- legacy terrain monoliths remain absent;
- Bosque hero residency remains four explicit L3 cells; L2 coverage never implies full-L2 residency.

No HLOD mesh is generated or approved. `HLOD_FEATURE_RETENTION_R18.json` now locks the features a future backend-specific HLOD/vista builder must preserve.

## Navigation / VESPER regression

R10 route chain remains 8,898.294 m. All four `SYLVA_COL_ROUTE_00..03` remain closed manifold with zero degenerate faces.

VESPER exact macro layout remains:
- three terraces: 116 / 124 / 112 m;
- two connectors: 142.215 m @12.178° and 145.685 m @12.689°;
- five VESPER collision proxies;
- final VESPER excluded.

A QA counter initially reported six terrace-prefix objects because three `SignalRing` objects share the prefix; exact canonical terrace-ID audit confirmed 3/3 terraces intact. No scene fix was needed.

## R18 visual signal

Three file-backed Eevee renders @256×144 PASS_NONBLANK:
- Puerto: 49,058 B · variance 0.00376456;
- Bosque: 48,652 B · variance 0.00473493;
- VESPER: 47,283 B · variance 0.00422835.

This is signal evidence only. Human `GATE-ART` remains **PENDING**.

## R18 remote identity

- `.blend`: **3,312,722 B**, etag `a1459ad6a5d5ae98f63b50e2613cf3b1`;
- GLB: **1,378,988 B**, etag `62d30277f973bbd87bb8c2aa16152c58`.

Remote identity is not a recovered SHA-bound delivery PASS.

## Root-kit provider dependency

PR #6 / `CLM-SYLVA-PROC-NROOT-001` remains **NOT_READY for deterministic consumption** despite CI green at last audit:
- current provider manifest YAML shape invalid around `materials` / `note`;
- normalized per-asset pivot/anchor contract absent;
- render/collision anchor parity unproven;
- pivot-policy version absent.

Macro contains 0 provider meshes/instances. Eight consumer sockets remain frozen.

## Production authority

Current package includes:
- `MASTER_ASSET_LIST_R15.json` + R16/R18 amendments;
- `WORLD_ASSET_COVERAGE_R14.json`;
- `SYLVA_PARALLEL_SHARDING_R14.json`;
- issue #27 non-reserving ready queue;
- `ART_DIRECTION_BIBLE_R14.md`;
- `BIOLOGICAL_REALISM_REFERENCE_PACK_R14.md`;
- `BLENDER_PRODUCTION_STANDARD_R14.md`;
- `HLOD_STRATEGY_R14_PROPOSAL.md` + `HLOD_FEATURE_RETENTION_R18.json`;
- `NATIVE_STREAM_RESIDENCY_TEST_PLAN.md`.

## Fleet / concurrency

Fleet claim ACTIVE, epoch1. Writer epoch 5 `SYLVA-MACRO-WRITER-EPOCH-5-R17-XSEC-20260914` is **CLOSED_ACCEPTED_R18**. A future primary-project mutation requires a fresh main/fleet/project readback and a new single-writer epoch.

Orbital project `c796230b-0463-4e17-9446-2e746c5c4933` remains EMPTY r0/unregistered; do not mutate.

## Open gates

P0:
1. recover exact revision22 `.blend` + GLB; bind SHA-256; run shared delivery + current claim validator;
2. native import and S-00…S-03 streaming/collision tests plus full route/VESPER traversal;
3. human art review of R18 root silhouette and intersections;
4. keep PR #6 blocked until manifest + anchors + parity pass.

P1:
5. final biological root meso/micro anatomy/material pass after human review — do not reintroduce generic noise;
6. target-renderer/hardware feature-aware HLOD qualification;
7. activate downstream independent material/prop/fauna/flora/character claims from issue #27 after live collision audit;
8. explicit planet-scale decision before orbital work.

## Gates

| Gate | State |
|---|---|
| Canon regions / VESPER layout | PASS_BLOCKOUT |
| Terrain causality / partition / seams | PASS_R6/R12 |
| Membership / L2-L3 hierarchy | PASS_R13/R14/R16_AMENDMENT |
| Prefetch semantics | PASS_R15_UNAPPROVED |
| Macro-root taper | PASS_R16_SOURCE |
| Macro-root non-circular structural meshes | **PASS_R18_SOURCE** |
| Root bounds→membership | **PASS_ZERO_MISSING** |
| Route collision topology | PASS_R10 |
| Provider root-kit | BLOCKED |
| Remote source/export | PASS_R18_REMOTE |
| Exact SHA-bound delivery | NOT_YET_QUALIFIED |
| Native residency/traversal | NOT_RUN |
| Human GATE-ART | PENDING |
| HLOD/target performance | BLOCKED_TARGET_HARDWARE |
| Planet radius canon | PROPOSAL_PENDING_DECISION |
