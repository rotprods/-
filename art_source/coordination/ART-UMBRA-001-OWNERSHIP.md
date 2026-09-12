# ART-UMBRA-001 · UMBRA world production ownership

Date: 2026-09-12.
Base at reservation: `4c2fa044080004609ea6df45f34b2a784536507a` (`main` observed before branch creation).
Branch: `art/world-umbra-001`.
Agent: `AGENT-UMBRA-04`.
Session: `ART-UMBRA-001-20260912T2123+0200`.
Claim: `CLM-W04-WORLD-UMBRA-001`.
World: `umbra` / **UMBRA — NOCTIL, el eclipse viviente**.
Role: `WORLD_OWNER`.

## Authority and observed canon

- Repository authority: `rotprods/-`.
- Protocol authority: `AGENTS.md`, `_project_intelligence/STATE.json`, `HANDOFF.md`, `MEMORY.md`, `_project_intelligence/PLAN.json`, `GOALS.md`, `ROADMAP.md`.
- Fleet coordination authority after its later promotion to `main`: `docs/FLEET_COORDINATION.md`, `ops/fleet/registry.json`, GitHub issue `#7`.
- World/art authority: `design/EXOVANT_BIBLIA.md`, `design/EXOVANT_DATA.json`, `docs/ART_PRODUCTION.md`.
- Engine currently executable: Godot `4.7.2.stable.official.ed1daf0bf`; Unreal remains the principal production candidate and is not qualified as integrated.
- Qualified editable-art route: remote 3D Jutsu / Blender `bpy`, with source `.blend`, generator/source Python, portable GLB and evidence required by `LRN-EXO-20260912-BLENDER`.
- UMBRA canon: Milky Way / Sere system / Flotilla de los Sin Sol; tidally locked world with settlements in the twilight band; small reflector-station swarm; mobile-twilight art kit of caravans, reflectors, dark ice and tensioned fabric; constant crosswind; darkness must never hide combat anticipation.

## Owned paths

- `art_source/worlds/umbra/`
- `art_source/coordination/ART-UMBRA-001-OWNERSHIP.md`

These are exact fleet paths; no wildcard ownership is asserted by the current coordination harness.

## Included

- UMBRA planetary/world-production specification and scale layers.
- Twilight-band macro layout and authored gameplay-region blockouts.
- UMBRA environment, architecture, infrastructure, caravan, reflector, dark-ice, prop, material, vegetation/ecology proxy, NPC/enemy/creature/vehicle proxy families needed for coverage planning.
- NOCTIL arena/environment proxy and silhouette interfaces only; final character/creature rigging may be split into later domain claims if parallelism requires it.
- Deterministic Blender master-scene generator, editable scene hierarchy, materials, cameras/lights, validation scripts, portable export and visual evidence for this branch.
- Per-asset manifests, task/coverage/status/handoff files under the owned UMBRA path.

## Excluded

- Runtime Godot scenes/scripts and gameplay logic.
- Terra, Ares IX, Pelagos, Khepri, Vanta or any other world-owned paths.
- Shared `STATE/PLAN/HANDOFF/PROGRESS` mutation; integration authority reconciles shared state after review.
- Shared libraries without a separate non-overlapping claim.
- Unreal/DLSS/GPU performance claims without qualification.
- Final NOCTIL anatomy/rig/attack implementation until the corresponding design contract exists.
- Final production completion of the entire world until engine import, performance and human/art review gates pass.

## Collision audit at reservation time

Observed branches before claim: `art/ares-ix-world-001`, `art/ares-ix-world-agent-02`, `art/terra-reliquary-kit-001`, `art/world-khepri-001`, `art/world-pelagos-thalassa-001`, `art/world-vanta-001`, `main`. Open draft PRs visibly owned ARES IX and Terra. No UMBRA branch/PR was present when this claim was persisted.

## Fleet-harness reconciliation

The fleet ownership harness was promoted to `main` after this reservation and after the first UMBRA geometry checkpoint. Chronology is preserved rather than backdated.

Latest reconciliation evidence in this session:
- `main@f78bfdc8bd7b2f6ab52b45d39babcc1589ab3918` was read after the harness promotion.
- `ops/fleet/registry.json` imports `CLM-W04-WORLD-UMBRA-001` as `reserved`, owner `AGENT-UMBRA-04`, branch `art/world-umbra-001`, epoch `1`, with the exact owned paths above and primary project `7ab99682-8777-4143-8ae0-1fbb178ccafb`.
- Owner acknowledgement was published to issue #7 as comment `5648349781`, including scopes, primary + clean-replay project IDs and current asset IDs. The producer does not mutate the `main` registry ACK on its own; the integrator must apply/read back that transition.
- Linear projection `ROT-119` was created after the harness appeared. It explicitly records that Linear did not precede the original geometry and therefore is not used as retroactive proof.
- Draft PR `#16` is the integration surface and remains draft until current-main reconciliation and open technical/art gates are handled.

Primary project: `7ab99682-8777-4143-8ae0-1fbb178ccafb` @ revision `1`.
Auxiliary reproducibility project: `7f33ae14-540c-4af5-8131-1490465fe6cc` @ revision `1`; QA-only, not a competing world scene.

## Current claim state

`RESERVED / OWNER ACK PUBLISHED / WAVE 0 LOCALLY VALIDATED / KEEP`.

This is not `released` and not `done`. No stale heartbeat or blocked gate releases the scope automatically. Significant new production waves must repeat the live ownership preflight before remote mutation.
