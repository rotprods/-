# UMBRA — Recoverable Handoff

AGENT: `AGENT-UMBRA-04`  
SESSION: `ART-UMBRA-001-20260912T2123+0200`  
CLAIM: `CLM-W04-WORLD-UMBRA-001`  
BRANCH: `art/world-umbra-001`  
BRANCH BASE AT CLAIM: `main@4c2fa044080004609ea6df45f34b2a784536507a`  
LATEST MAIN OBSERVED AT FINAL RESYNC: `196ef814fdc845ec797979906d01dc25009217c7`  
PR: `#16` draft  
NORTH STAR: establish a collision-free, reproducible UMBRA world-production stream whose editable 3D source, canon separation, art language, asset coverage and validation can survive cold resume and later runtime integration.

## DONE
- Repository authority, executable-engine status and art protocol recovered.
- Active art branches/PRs audited; no UMBRA branch/PR owner was observed before claim.
- Atomic UMBRA ownership persisted; shared STATE/PLAN/HANDOFF intentionally untouched.
- `Flu In` and `Flow In` exact names searched in repository and not found; no tool identity invented.
- Persisted project learning revalidated: remote editable Blender route is 3D Jutsu / `bpy`.
- Dedicated source project created: `7ab99682-8777-4143-8ae0-1fbb178ccafb`.
- Blender observed: `5.2.0 LTS`; metric scale `1 BU = 1 m`; empty initial scene.
- UMBRA World Bible written with CANON / UNKNOWN / PROPOSAL separation.
- Wave-0 master blockout committed as source-project revision `1`.
- Built: 1200×700 m authored terrain proposal, 7 ice-ridge proxies, 5 route segments, 4 reflector tower assemblies, 9 windbreak pylons, 5 caravan proxies, refuge hub, NOCTIL eclipse-ring destination proxy, 8 arena anchors, human/rover scale refs, 2 cameras, 7 lights.
- Editable `.blend`, portable `.glb` and 960×540 preview generated.
- Structural QA passed: 85 mesh objects, 12,204 evaluated triangles, 85 material slots, zero residual object-scale anomalies, zero zero-dimension meshes.
- Asset coverage manifest and repository generator source persisted.
- First bootstrap defect recorded rather than hidden: blank project had no World datablock; corrected without producing a committed bad revision.
- Clean-project deterministic replay executed from repository generator blob `8456a891ebb14590794d3730e329a7d4bbd05c65` in independent project `7f33ae14-540c-4af5-8131-1490465fe6cc`, revision 1.
- Clean replay semantic QA matched source revision exactly on 96 objects, 85 meshes, 9 materials, 12,204 evaluated triangles, 85 material slots, terrain `[1200,700,11.795] m`, human `[0.44,0.44,1.75] m`, rover `[4.6,2.1,2.0] m`, 4 reflector masts and 5 caravan chassis. GLB byte size matched exactly at 819,168 B; binary etags were not treated as required equality.
- Draft PR `#16` opened against `main` with ownership, receipts, blockers and merge guard.
- Final RESYNC found `main` advanced to `196ef814fdc845ec797979906d01dc25009217c7` with a multi-agent ownership-preflight policy change. Branch is intentionally left unforced and must reconcile before merge.

## IN PROGRESS
- Visual/art QA: interactive source and replay scenes exist, but this agent has not claimed a direct pixel-level visual PASS from the artifact.
- Upgrade reflector/caravan/refuge proxies from C-blockout toward production topology after acceptance of shape/proportion language.
- Reconcile branch safely with current main before any merge-ready state.

## BLOCKED
- `BLOCK-W04-001`: physical planet radius / orbital scale not canonized.
- `BLOCK-W04-002`: production runtime + target GPU budgets not empirically qualified; Godot is current executable prototype, Unreal remains principal production candidate.
- `BLOCK-W04-003`: final NOCTIL morphology/function/anatomy/rig/attack contract absent.
- Engine import, collision, LOD/HLOD, texture-memory and GPU-performance PASS cannot be claimed yet.

## FILES MODIFIED / CREATED
- `art_source/coordination/ART-UMBRA-001-OWNERSHIP.md`
- `art_source/worlds/umbra/WORLD_BIBLE.md`
- `art_source/worlds/umbra/TASKS.md`
- `art_source/worlds/umbra/ASSET_MANIFEST.json`
- `art_source/worlds/umbra/generate_wave0.py`
- `art_source/worlds/umbra/VALIDATION.json`
- `art_source/worlds/umbra/HANDOFF.md`

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
- `VALIDATION.json`: durable receipt and gate states.

## DECISIONS
- Physical planet radius remains UNKNOWN rather than silently invented.
- Local authored testbed `1200×700 m` is a reversible PROPOSAL, not total world size.
- Shape language: low wind-shedding settlement masses + vertical reflector infrastructure + tension/anchor geometry; eclipse rings restricted mainly to NOCTIL route.
- Portable Principled materials only in Wave 0; final texture/LOD/shader budgets wait for runtime qualification.
- NOCTIL final creature asset is not fabricated from insufficient canon; only environment/destination interface exists.
- Reproducibility is validated semantically, not by demanding identical `.blend`/GLB etags across runs; scene metadata/container serialization may differ even when measured content matches.
- No force update/rebase is performed automatically after main drift; integration must reconcile the new ownership policy safely.

## DEPENDENCIES
- Canon/ADR for physical planetary scale when L0/L1 work becomes critical.
- Runtime integrator for GLB import, collision, camera and performance gates.
- Boss/creature design contract for NOCTIL.
- Population/ecology canon or explicit proposals before mass production.
- Current `main@196ef814...` reconciliation before merge readiness.

## RISKS
- Low-light art may hide combat anticipation; accessibility test remains P1.
- Reflective materials can become generic/expensive; optical function must remain explicit.
- Over-authoring global geography before planet-scale decisions would create rework.
- PR #16 is currently draft/non-mergeable while branch and current main diverge; do not force refs.

## PROGRESS
- Ownership/canon bootstrap: `100%` for current checkpoint.
- Wave-0 modeling/blockout target: `100%`.
- Structural QA: `100%` for blockout gates executed.
- Reproducibility gate: `100%` semantic clean replay PASS.
- Material finalization: `blockout only`; production percentage not claimed.
- Optimization: `0% production-qualified`; metrics recorded but budgets unresolved.
- Engine integration: `0%` / BLOCKED.
- Human/art final QA: pending.
- Full-world completion percentage: deliberately **NOT CLAIMED** because the denominator is not production-locked.

P0 OPEN: 3 blocking contracts (`planet scale`, `runtime/GPU`, `NOCTIL final spec`) plus engine import and branch reconciliation gates.  
P1 OPEN: visual QA, reflector/caravan/refuge production kits, low-light accessibility scene.  
P2/P3: ecology breadth, set dressing and polish remain downstream.

## NEXT 3 ACTIONS
1. Reconcile `art/world-umbra-001` with current `main@196ef814...` under the newly promoted ownership-preflight policy, rerun branch guards and keep PR #16 draft until clean.
2. Run art/visual Gauntlet on the revision-1 scene, convert framing/contact/silhouette/readability defects into tasks, then produce Wave-1 reflector and caravan kits.
3. Coordinate with integration authority for a bounded GLB runtime import smoke test without changing shared runtime ownership; record scale/material/collision/profile evidence.

CLAIM STATUS: `KEEP` — scope has substantial P0/P1 work and no observed UMBRA ownership collision.
