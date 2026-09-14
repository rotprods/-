# SYLVA PRIME Macro — Engine Import Contract R18

Claim: `CLM-SYLVA-MACRO-001`  
Primary Blender: `05dce898-753d-4ff6-a4b0-31757dc868d8` @ **revision 22 / sceneSequence 0**  
State: `VERIFIED SOURCE TECHNICAL-ART CHECKPOINT / NOT FINAL ART`

## 1. Source identity

- 1 Blender Unit = 1 metre.
- Local authored patch = 12,000 × 12,000 m; this is not planetary diameter.
- Blender source is Z-up; apply the selected engine/glTF axis conversion once.
- R18 geometry fingerprint: `7b1a4c5c1f16c6b3c1319f3da26315c8d359ce97717272c91aa5910effe00939`.
- Remote revision22 identities:
  - `.blend` 3,312,722 B / etag `a1459ad6a5d5ae98f63b50e2613cf3b1`;
  - GLB 1,378,988 B / etag `62d30277f973bbd87bb8c2aa16152c58`.
- Remote size/etag is not SHA-bound delivery PASS.

## 2. Terrain / world partition

Morphology: `R6_BIOGEO_CAUSAL_MACRO_V1`.  
Partition: `SYLVA_TERRAIN_STREAM_R12`.

Required:
- 16 `SYLVA_TERRAIN_L3_X#Y#` render tiles, 3 km each;
- 16 `SYLVA_COL_TERRAIN_L3_X#Y#` collision tiles;
- 16 `SYLVA_STREAM_L3_X#Y#` cells;
- 4 `SYLVA_STREAM_L2_X#Y#` supercells.

R12 source QA: 285 render seam + 189 collision seam samples, max/mean Δz = 0 m. Legacy terrain monoliths are forbidden.

Hierarchy contract: `SYLVA_STREAM_HIERARCHY_R14`. Hero residency is L3-only; L2 coverage is grouping/HLOD metadata, never a command to load an entire supercell.

## 3. Membership / prefetch

Base membership: `SYLVA_STREAM_MEMBERSHIP_R13`; R01 conservative amendment: `SYLVA_STREAM_MEMBERSHIP_R16_AMENDMENT`.

R18 source bounds audit: missing memberships across R01..R06 = **0**. R01 retains conservative extra X0Y2/X1Y2 residency; do not shrink it merely because the final visible mesh no longer touches those cells.

Prefetch contract: `SYLVA_PREFETCH_POLICY_R15`.

State: `RUNTIME_EXPERIMENT_REQUIRED`, approved=false. Candidate policies remain current-only, +4, +8 and directional route-window + contextual hero overlay. Promote only from native measurements.

## 4. R18 primary-root representation

Contract: `SYLVA_MACRO_ROOT_XSEC_R18_ALL`.

Required asset IDs: `SYLVA_ROOT_PRIMARY_R01..R06`.

Every primary root is now a **self-contained Mesh**, not an exported Curve/helper-profile dependency:
- 1,040 vertices;
- 1,026 polygon faces;
- 0 nonmanifold edges / 0 degenerate faces at source QA;
- material `SYLVA_DIAG_RootFiber` retained;
- R16 load-correlated taper preserved;
- original R16 Bezier source serialized in `r17_source_curve_json` for rollback/reconstruction;
- no `SYLVA_PROFILE_R17_*` helper scene objects may exist in a valid R18 export.

Profiles:
- R01 1.10×0.70;
- R02 1.12×0.70;
- R03 1.18×0.66;
- R04 1.08×0.72;
- R05 1.06×0.74;
- R06 1.12×0.68.

Do not reconstruct these assets as circular tubes. R18 is still macro structural anatomy: it does not claim final bark/fiber/callus/reaction-tissue microstructure or gameplay root collision.

Historical invalid representations that must not be delivered:
- scene revision18 linked custom bevel helpers exported as standalone GLB primitives;
- scene revision19 unlinked helper objects were lost on `.blend` reopen;
- scene revision20 is the safe R16 rollback checkpoint, not the R18 result.

## 5. Navigation / route collision

Contract: `SYLVA_NAV_R10` / `MANIFOLD_RIBBON_R10`.

Four route legs total 8,898.294 m. `SYLVA_COL_ROUTE_00..03` must remain closed manifold and are gameplay-collision interfaces; HLOD never replaces them.

Repeatable transition probes:
- S-00 X0Y1→X1Y1 ≈ `(-3000,-2000,345.8)`;
- S-01 X1Y1→X1Y2 ≈ `(-500,0,356.1)`;
- S-02 X1Y2→X2Y2 ≈ `(0,250,352.2)`;
- S-03 X2Y2→X3Y2 ≈ `(3000,2000,-72.4)`.

## 6. VESPER macro arena

Required exact visible IDs:
- `SYLVA_VESPER_Terrace_00_ENTRY`;
- `SYLVA_VESPER_Terrace_01_MIDDLE`;
- `SYLVA_VESPER_Terrace_02_UPPER`;
- `SYLVA_VESPER_TerraceConnector_00`;
- `SYLVA_VESPER_TerraceConnector_01`.

Three similarly-prefixed `*_SignalRing` assets exist; do not count them as terraces.

Expected VESPER collision proxies: 5. Final VESPER model remains outside this claim.

## 7. Root-kit provider boundary

Provider: PR #6 / `CLM-SYLVA-PROC-NROOT-001`.

Consumer basis: +X forward / +Z up / metres / scale1. Eight macro sockets remain frozen.

Last provider audit remains NOT_READY despite CI green because deterministic manifest/pivot/anchor/render-collision parity gates were not proven. R18 valid macro delivery must contain **zero provider module meshes** unless a later provider handoff explicitly supersedes this gate.

## 8. HLOD / vista

`HLOD_FEATURE_RETENTION_R18.json` is the current feature-retention contract. It protects R18 primary-root skyline/taper/section, hero-core composition, traversal support and terrain seams.

No HLOD geometry, switch distance, screen-space threshold, triangle budget or backend is approved. Uniform percentage decimation is rejected by the R14 geometric error study.

## 9. Delivery chain

When artifact bytes are available:
1. recover exact revision22 `.blend` + GLB;
2. compute SHA-256 for both;
3. run shared `fleet_control.py delivery` with source-bound evidence;
4. run claim semantic validation against the same GLB SHA;
5. verify no legacy monoliths, helper profile nodes or PR #6 modules;
6. verify 16+16 terrain, 4 L2/16 L3, R18 root IDs and R16/R18 memberships;
7. import into the currently qualified native runtime with no arbitrary global scale multiplier;
8. execute S-00…S-03 + full route/VESPER traversal;
9. compare P0/P1/P2/P3 residency using measured load-to-ready latency, resident memory/set, frame spikes, visual pop, reversal and collision readiness;
10. profile only on declared target hardware/preset;
11. perform human art review independently.

## 10. Current acceptance / blockers

Source QA receipt: `qa/R18_ALL_PRIMARY_ROOT_XSEC_ACCEPTANCE.json`.

PASS source-side:
- R18 six-root structural meshes;
- root bounds→membership zero missing;
- terrain/world partition retained;
- route collision regression retained;
- exact VESPER layout retained;
- zero provider meshes / zero profile helper scene nodes;
- three regional render signals nonblank.

Still open:
- exact SHA-bound delivery;
- native import/residency/traversal;
- human GATE-ART;
- provider PR #6 readiness;
- final root surface anatomy/material/collision;
- HLOD/target-hardware qualification;
- planetary scale decision.
