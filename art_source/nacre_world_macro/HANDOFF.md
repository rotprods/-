# NACRE WORLD MACRO — cold handoff

AGENT: AGENT-3D-NACRE-01
SESSION: 20260912T2123+0200-NACRE-01
CLAIM: CLM-NACRE-WORLD-MACRO-001
BRANCH: art/world-nacre-001
BASE MAIN AT CLAIM: 4c2fa044080004609ea6df45f34b2a784536507a
LAST MAIN MERGED NON-FORCE: 70fda70cd2120d38fba94e6a66e554e564c6c471
FLEET EPOCH: 1
FLEET STATUS OBSERVED: reserved; producer ACK published; integrator transition pending
COORDINATION ACK: issue #7 comment 5648339684
DRAFT PR: #17
PRIMARY REMOTE PROJECT: a49fc6f3-fedb-40a5-913f-10a08debb0e1 @ revision 4
CLEAN REPLAY PROJECT: 4750e054-b063-4ab8-afc9-214462f36128 @ revision 1
NORTH STAR: deliver a recoverable, semantically reproducible Nacre planetary-foundation package without inventing planetary canon; do not claim DONE before human art + native runtime gates.

DONE:
- Repository/canon/pipeline/fleet authority recovered.
- Nacre atomic macro-foundation claim established; producer ACK published with exact paths/project/asset IDs.
- Branch resynced to `main@70fda70...` using a two-parent merge + non-force ref update; compare confirmed `behind_by=0` and isolated Nacre-only diff.
- Planetary physical scale remains separate from authored/rendered representation; radius/diameter intentionally UNKNOWN.
- Macro scene has shell envelope, inner pearl lining, 7 archive chambers, surface-to-surface bridges/spines, 21 docking sockets, 7 service rings, 7 shell load-path tendons, 5 growth strata, bounded translucent plates, human/100m gauges, camera and binary SUN lights.
- R3 corrected center-to-center bridge penetration defect; 10/10 archive links now terminate outside chambers.
- Versioned generator exists at `art_source/nacre_world_macro/build_macro.py`.
- Cold replay exposed Blender 5.2 collection-membership incompatibility; generator fixed in commit `6be51b785b53c38e071461212254a81e601c8518`.
- Clean Blender replay succeeded from revision 0: 97 meshes, 30 curves, `SUN_MNEME_A/B`.
- Historical R3 vs replay semantic drift detected rather than hidden; drift traced to implicit legacy shell resolutions/rib/belt geometry/plate naming.
- Primary project rebuilt as revision 4 from corrected generator, making the versioned generator explicit authority for reversible macro blockout geometry.
- Primary R4 and independent cold replay semantic SHA256 match exactly: `48742ba2dc253a626fb807799a55e2c83f2e87f437cf761b66522bac7ba88787`.
- R4 QA PASS: 130 objects; 97 meshes; 30 curves; 10/10 bridges checked; 2.9999–3.0m endpoint clearance; 0 penetrations; 0 non-unit scales; 0 degenerate dimensions.
- R4 `.blend` + GLB provider receipts resolved; QA receipt persisted at `qa-r4.yaml`.

IN PROGRESS:
- Human/direct visual review remains OPEN; generated renders are evidence, not approval.
- Producer claim remains fleet `reserved`; integrator must apply ACK against current registry digest to promote `active`.
- Native Godot delivery/import/collision/LOD/perf remain unresolved.

ENV_BLOCKED:
- Attempted native delivery on isolated execution container.
- `git clone` could not resolve `github.com` in that environment.
- Exact provider binary could not cross the safe-download boundary into the same container.
- No Godot import occurred and no `fleet_control.py delivery` receipt was fabricated.
- Treat this as environment/transit blocker, NOT asset FAIL and NOT Godot PASS.

FILES OWNED / MODIFIED:
- `art_source/coordination/CLM-NACRE-WORLD-MACRO-001.md`
- `art_source/nacre_world_macro/HANDOFF.md`
- `art_source/nacre_world_macro/build_macro.py`
- `art_source/nacre_world_macro/manifest.yaml`
- `art_source/nacre_world_macro/qa-r3.yaml`
- `art_source/nacre_world_macro/qa-r4.yaml`

PUBLISHED INTERFACE IDS:
- `NACRE-MACRO-SHELL-001`
- `NACRE-MACRO-LINING-001`
- `NACRE-ARCHIVE-NET-001`
- `NACRE-BRIDGE-NET-001`
- `NACRE-SCALE-REF-001`

PRIMARY R4 RECEIPTS:
- Blender project: `a49fc6f3-fedb-40a5-913f-10a08debb0e1`, revision 4.
- `.blend`: 3,500,059 bytes / etag `a365ae84492f4142d949c1033636b092`.
- GLB: 3,828,832 bytes / etag `0b6dee01664cb91aae1a4b332e8ae163`.
- Semantic digest: `48742ba2dc253a626fb807799a55e2c83f2e87f437cf761b66522bac7ba88787`.
- Preview: `nacre_r4_canonical_hero.png`, 640×360, artifact `24642ce8001df31f7c50875e79c07c9d`.

CLEAN REPLAY RECEIPTS:
- Project `4750e054-b063-4ab8-afc9-214462f36128`, revision 1.
- 97 meshes / 30 curves / two SUN lights.
- `.blend`: 3,497,824 bytes / etag `7f6a1db325b7cee3692051b289590791`.
- GLB: 3,828,216 bytes / etag `9eb39213129f2e5b8bf150765df4c693`.
- Semantic digest matches primary R4 exactly. Byte identity is intentionally not the reproducibility criterion.

IMPORTANT OPERATIONS:
- `nacre-macro-build-v1` — noncommitting fail: missing World datablock.
- `nacre-macro-build-v1b` — noncommitting fail: Blender collection API mismatch.
- `nacre-macro-build-v1c` — revision 1.
- `nacre-portability-fix-r2` — revision 2; removed unsupported AREA light.
- `nacre-structural-bridge-fix-r3` — revision 3; bridge/docking/load-path correction.
- `nacre-qa-r3-geometry-render` — R3 structural PASS.
- `nacre-r3-generator-api-probe` — exposed versioned-generator collection membership TypeError.
- `nacre-r3-clean-replay-fixed-generator` — clean replay PASS.
- `nacre-r3-semantic-digest-primary/replay` — exposed historical R3 drift.
- `nacre-r4-generator-canonicalization` — revision 4 generated from corrected source.
- `nacre-r4-canonical-qa` — semantic match + geometry QA PASS.

DECISIONS:
- `PIPELINE_METHOD_NOT_FOUND` for exact “Flu In / Flow In”; use verified Blender 5.2 / GLB route.
- Versioned generator is the explicit authority for reversible macro proposal geometry from R4 onward.
- Semantic scene equivalence, not serialized byte identity, is the reproducibility criterion at this blockout tier.
- No random greeble/noise; growth strata and structural supports require causal purpose.
- Producer does not self-edit global fleet registry/STATE/PLAN.

OPEN GATES:
- Human `GATE-ART`.
- Integrator fleet ACK transition.
- Exact GLB Godot import/material/scale (currently ENV_BLOCKED on available local surface).
- Collision/traversal.
- LOD/HLOD/streaming.
- Target-hardware performance.
- Fleet native delivery with source/export/native receipt co-located.

NEXT 3 ACTIONS:
1. Integrator reconciles ACK `5648339684` against current fleet digest and promotes/updates Nacre reservation paths + asset IDs without force.
2. On a host with repo + provider binary transport, recover exact R4 GLB/.blend, import GLB into Godot 4.7.2, create collision strategy/native receipt and run fleet delivery + asset/native gates.
3. Run human creative-director review on R4; convert every rejected silhouette/composition/material issue into atomic R5 tasks, otherwise proceed to LOD/HLOD/streaming/performance qualification.

CLAIM STATUS: KEEP / IN_PROGRESS

RECOVERY: read latest main fleet protocol/registry first; then claim + manifest + qa-r4; inspect primary revision 4 or rebuild from `build_macro.py`; compare semantic digest against `48742ba2dc253a626fb807799a55e2c83f2e87f437cf761b66522bac7ba88787`. Never infer planetary radius/diameter from this blockout.
