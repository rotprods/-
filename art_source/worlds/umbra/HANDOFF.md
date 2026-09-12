# UMBRA — Recoverable Handoff

AGENT: `AGENT-UMBRA-04`  
SESSION: `ART-UMBRA-001-20260912T2123+0200`  
CLAIM: `CLM-W04-WORLD-UMBRA-001`  
ROLE: `WORLD_OWNER`  
BRANCH: `art/world-umbra-001`  
BRANCH BASE AT CLAIM: `main@4c2fa044080004609ea6df45f34b2a784536507a`  
MAIN RECONCILED: `f78bfdc8bd7b2f6ab52b45d39babcc1589ab3918`  
RECONCILIATION MERGE: `455bf6419815a718641636cbb37723047863cdef`  
PR: `#16` draft  
LINEAR: `ROT-119`  
NORTH STAR: establish a collision-free, reproducible UMBRA world-production stream whose editable 3D source, canon separation, art language, asset coverage and validation can survive cold resume and later runtime integration.

## DONE
- Repository authority, executable-engine status, art protocol and later-promoted fleet harness recovered.
- Active branches/PRs audited before reservation; no UMBRA owner was observed at claim time.
- Atomic UMBRA reservation persisted before Blender production. Shared STATE/PLAN/HANDOFF were intentionally not mutated.
- Exact repository searches for `Flu In` and `Flow In` returned no verified method; no tool identity was invented.
- Qualified editable Blender route revalidated through 3D Jutsu / `bpy`.
- Primary project created: `7ab99682-8777-4143-8ae0-1fbb178ccafb`.
- Blender observed: `5.2.0 LTS`; metric scale `1 BU = 1 m`; empty initial scene.
- UMBRA World Bible written with CANON / UNKNOWN / PROPOSAL separation.
- Wave-0 master blockout committed as source-project revision `1`.
- Built: 1200×700 m authored terrain proposal, 7 ice-ridge proxies, 5 route segments, 4 reflector tower assemblies, 9 windbreak pylons, 5 caravan proxies, refuge hub, NOCTIL eclipse-ring destination proxy, 8 arena anchors, human/rover scale refs, 2 cameras, 7 lights.
- Editable `.blend`, portable `.glb` and 960×540 preview generated.
- Structural QA passed: 85 mesh objects, 12,204 evaluated triangles, 85 material slots, zero residual object-scale anomalies, zero zero-dimension meshes.
- Asset coverage manifest and deterministic repository generator source persisted.
- Initial Blender bootstrap defect recorded rather than hidden: blank project had no World datablock; corrected without producing a committed bad revision.
- Independent clean-project replay executed from repository generator blob `8456a891ebb14590794d3730e329a7d4bbd05c65` in project `7f33ae14-540c-4af5-8131-1490465fe6cc`, revision 1.
- Clean replay semantic QA matched source revision exactly on 96 objects, 85 meshes, 9 materials, 12,204 evaluated triangles, 85 material slots, terrain `[1200,700,11.795] m`, human `[0.44,0.44,1.75] m`, rover `[4.6,2.1,2.0] m`, 4 reflector masts and 5 caravan chassis. GLB byte size matched exactly at 819,168 B; binary etag equality is intentionally not required.
- Draft PR `#16` opened as the integration surface.
- Fleet harness promotion on main was detected during the session rather than ignored. Current `AGENTS.md`, `docs/FLEET_COORDINATION.md`, issue #7 and `ops/fleet/registry.json` were read.
- Current registry imports `CLM-W04-WORLD-UMBRA-001` as `reserved`, owner `AGENT-UMBRA-04`, epoch 1, with exact owned paths and primary project mapping.
- Owner ACK was published to issue #7 as comment `5648349781`; the producer did not mutate the main registry ACK transition.
- Linear projection `ROT-119` was created during reconciliation and explicitly preserves chronology: Linear did not precede the original reservation/geometry.
- Branch was reconciled with `main@f78bfdc8...` using a normal two-parent merge commit `455bf641...`; branch ref moved by fast-forward with `force=false`.
- Post-reconciliation compare showed branch `ahead`, `behind_by=0`, with exactly seven UMBRA-owned changed paths and no cross-scope diff.
- PR #16 became mergeable after reconciliation but remains draft because acceptance gates are still open.
- GitHub Actions run `34716069512` executed on a real ubuntu-24.04 runner. All **75/75 unit tests passed**. The only failure was `project_control.py check` reporting root `MANIFEST.json` drift for the seven newly-added UMBRA paths. Godot native gates were skipped after that continuity failure. This is a real CI failure, not ENV_BLOCKED.

## IN PROGRESS
- Refresh the generated root `MANIFEST.json` only, using exact SHA-256 hashes of the final seven UMBRA paths; this is an allowed generated projection update under fleet policy, not shared-state ownership.
- Re-run normal PR CI after manifest refresh and verify continuity + native gates.
- Direct visual/art QA remains pending; interactive source and replay scenes exist but no pixel-level agent PASS is claimed.
- Upgrade reflector/caravan/refuge proxies from C-blockout toward production topology after shape/proportion language review.

## BLOCKED
- `BLOCK-W04-001`: physical planet radius / orbital scale is not canonized.
- `BLOCK-W04-002`: production runtime + target GPU budgets are not empirically qualified; Godot is the current executable prototype while Unreal remains principal production candidate.
- `BLOCK-W04-003`: final NOCTIL morphology/function/anatomy/rig/attack contract is absent.
- Engine import, collision, LOD/HLOD, texture-memory and production GPU-performance PASS cannot be claimed yet.
- Fleet registry ACK readback remains pending the integrator applying comment `5648349781` as evidence.

## FILES MODIFIED / CREATED
Owned source paths:
- `art_source/coordination/ART-UMBRA-001-OWNERSHIP.md`
- `art_source/worlds/umbra/WORLD_BIBLE.md`
- `art_source/worlds/umbra/TASKS.md`
- `art_source/worlds/umbra/ASSET_MANIFEST.json`
- `art_source/worlds/umbra/generate_wave0.py`
- `art_source/worlds/umbra/VALIDATION.json`
- `art_source/worlds/umbra/HANDOFF.md`

Generated projection pending refresh:
- `MANIFEST.json` — may be updated only to the exact output equivalent of `python3 tools/project_control.py refresh`; it is not claimed as semantic shared-state ownership.

## ASSETS CREATED
Source remote project `7ab99682-8777-4143-8ae0-1fbb178ccafb`, revision `1`:
- Blend: 1,584,746 bytes, etag `f0b1ad2f8fb5baae1e8cc3f3b60b7b7a`.
- GLB: 819,168 bytes, etag `7a975a092cf47ce2369a30b17124e0e6`.
- Preview: artifact `def7a42f2a255d3c7b80bda39dae2015`, 398,298 bytes, 960×540, etag `16a925648f5a3df28235bfcbe4cf290f`.

Independent replay project `7f33ae14-540c-4af5-8131-1490465fe6cc`, revision `1`:
- Blend: 1,581,834 bytes, etag `88ca5db662ea398e6dd0ae3ce9e6aab7`.
- GLB: 819,168 bytes, etag `a536afcefeff280e93bd0aeb8f2dd405`.
- Semantic geometry/scale equivalence: PASS.

## TESTS / RECEIPTS
- `umbra-bootstrap-inspect-001`: PASS.
- `umbra-wave0-blockout-001`: FAIL before commit due absent World datablock; mechanism recorded.
- `umbra-wave0-blockout-002`: PASS → source revision 1.
- `umbra-wave0-qa-001`: PASS structural blockout QA.
- `umbra-repo-generator-replay-001`: PASS → clean replay revision 1 from repository generator blob.
- `umbra-repo-generator-replay-qa-001`: PASS semantic equivalence.
- GitHub Actions `34716069512`: 75 unit tests PASS; continuity FAIL only because generated `MANIFEST.json` does not yet include the seven final UMBRA files; Godot native steps skipped.
- `VALIDATION.json`: durable operation/gate state.

## DECISIONS
- Physical planet radius remains UNKNOWN rather than silently invented.
- Local authored testbed `1200×700 m` is a reversible PROPOSAL, not total world size.
- Shape language: low wind-shedding settlement masses + vertical reflector infrastructure + tension/anchor geometry; eclipse rings remain concentrated on the NOCTIL route.
- Portable Principled materials only in Wave 0; final texture/LOD/shader budgets wait for runtime qualification.
- NOCTIL final creature asset is not fabricated from insufficient canon; only environment/destination interface exists.
- Reproducibility is validated semantically rather than by demanding identical Blender container etags.
- Main drift was reconciled without force and without replacing shared project state.
- CI is classified from executed steps: unit suite PASS, generated-manifest continuity FAIL. No blind rerun.

## DEPENDENCIES
- Canon/ADR for physical planetary scale when L0/L1 work becomes critical.
- Runtime integrator for GLB import, collision, camera and performance gates.
- Boss/creature design contract for NOCTIL.
- Population/ecology canon or explicit proposals before mass production.
- Integrator readback/application of fleet registry ACK.
- Exact root manifest refresh, then normal CI readback.

## RISKS
- Low-light art may hide combat anticipation; accessibility test remains P1.
- Reflective materials can become generic/expensive; optical function must remain explicit.
- Over-authoring global geography before planet-scale decisions would create rework.
- Remote `.blend`/GLB receipts are valid provider artifacts but do not yet satisfy the fleet harness's final local delivery-binary gate without recovered local binary receipts/import validation.

## PROGRESS
- Ownership/canon bootstrap: `100%` for current checkpoint.
- Fleet ownership reconciliation: `owner ACK published`; registry ACK readback pending integrator.
- Wave-0 modeling/blockout target: `100%`.
- Structural QA: `100%` for executed blockout gates.
- Reproducibility gate: `100%` semantic clean replay PASS.
- Unit tests in PR CI: `75/75 PASS`.
- Continuity CI: `FAIL — generated MANIFEST refresh required`.
- Native Godot CI: `NOT EXECUTED` after continuity fail.
- Material finalization: `blockout only`; production percentage not claimed.
- Optimization: `0% production-qualified`; metrics recorded but budgets unresolved.
- Engine integration: `0%` / BLOCKED.
- Human/art final QA: pending.
- Full-world completion percentage: deliberately **NOT CLAIMED** because the denominator is not production-locked.

P0 OPEN: manifest/CI continuity, engine import, three blocking contracts (`planet scale`, `runtime/GPU`, `NOCTIL final spec`) and registry-ACK readback.  
P1 OPEN: visual QA, reflector/caravan/refuge production kits, low-light accessibility scene.  
P2/P3: ecology breadth, set dressing and polish remain downstream.

## NEXT 3 ACTIONS
1. Refresh exact generated `MANIFEST.json` for the final UMBRA files and verify CI reaches/passes native gates; do not hand-author arbitrary manifest values.
2. Run art/readability Gauntlet on the revision-1 scene, convert framing/contact/silhouette/readability defects into tasks, then produce Wave-1 reflector and caravan kits.
3. Coordinate a bounded GLB runtime import smoke test with the integration owner and record scale/material/collision/profile evidence.

CLAIM STATUS: `KEEP` — scope has substantial P0/P1 work and no observed UMBRA ownership collision.
