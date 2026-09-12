# UMBRA COLD HANDOFF — ART-UMBRA-001

## Identity

- Project: EXOVANT 2950
- World: `W04 UMBRA`
- Owner: `AGENT-UMBRA-04`
- Claim: `CLM-W04-WORLD-UMBRA-001`
- Role: `WORLD_OWNER`
- Branch: `art/world-umbra-001`
- PR: `#16` — DRAFT / KEEP
- Linear: `ROT-119` — In Progress
- Primary Blender: `7ab99682-8777-4143-8ae0-1fbb178ccafb`
- Replay Blender: `7f33ae14-540c-4af5-8131-1490465fe6cc`

## Resume truth

Current state is **Wave 1 production foundation, reproducible, not final AAAA**.

Do not restart UMBRA from scratch. Do not take over other worlds. Do not edit shared `STATE/PLAN/HANDOFF/PROGRESS` from this producer branch. Do not invent planet radius or final NOCTIL anatomy.

## Canon that is safe to rely on

- World 04 UMBRA, Sere system, Flotilla de los Sin Sol, NOCTIL.
- Sere: fictional M4 V red dwarf.
- synchronous rotation / habitable twilight band;
- reflector-station swarm;
- reference gravity `0.81 g`;
- reference-area temperature `−87 °C`;
- light/shadow are navigation permission + thermal state;
- reflector activation can reveal routes while exposing caravans;
- art seed: mobile twilight, caravans, reflectors, dark ice, tensioned fabric, constant lateral wind;
- combat anticipation must remain readable in darkness.

Unknown/blocked: physical radius/diameter, atmospheric contract, global hydrology/continents, final NOCTIL morphology/rig/attacks.

## Coordination state

Original reservation predates the fleet harness and that chronology is preserved.

Owner ACK is already published at issue #7 comment `5648349781`. Current registry readback still has UMBRA as `reserved / ack=null`; that transition is integrator-owned. Do not rewrite `main:ops/fleet/registry.json` from this branch.

The branch was first reconciled with `main@ca224a78c72512770cb599e82977623c4b8aa76d` through merge `58e54c25965a21e6a39b2bd3e309281be01b1166`, then with `main@758a9b6326a7d061f1e304abe9b1593b6b2d1a66` through merge `bfff105fb5e46d31e064a22f33053e43b132df19`. After the migration-readiness / asset-custody contract landed, UMBRA was reconciled again with `main@b74bd7072a7b2c68c4453402fbffe9d20bfb4de0` through two-parent merge `4678d0ddf6d74cce663ceb39ddbd205a30aa91da`. No force update was used. Global/runtime paths always come from current main and only UMBRA-owned semantic paths are overlaid.

The current fleet contract additionally requires durable provider-independent custody for final artistic delivery. Higgsfield project URLs and signed artifact links are production evidence, **not an independent backup**. UMBRA therefore cannot pass final 3D delivery until its `.blend`, GLB and dependencies are recovered into Git when transport permits or a persistent EXOVANT Drive bundle with stable ID, exact SHA256/bytes and a versioned receipt.

## Wave 0 checkpoint

Primary revision 1:

- 96 objects / 85 meshes / 9 materials;
- 12,204 evaluated triangles;
- 1200 × 700 m authored L2 testbed, explicitly PROPOSAL not planet size;
- 4 reflector proxies / 5 caravan proxies / refuge / NOCTIL environmental destination / scale refs;
- `.blend` 1,584,746 B;
- GLB 819,168 B;
- clean replay revision 1 matched semantic counts/dimensions and GLB size.

CI continuity P0 was closed on branch head `498f5de4ef991be7d768b613f2cd09a7df4be7c9`: Gauntlet `34720234976` passed `82/82` Python tests, `project_control.py check`, pinned Godot `4.7.2`, and native gates `import/state/world/input/smoke`. Evidence artifact `10306275373` exists.

## Wave 0 defects discovered by objective Gauntlet

Do not regress these:

- ten caravan tracks floated about `2.43–5.80 m`;
- several foundations were embedded/floating up to about `3.62 m`;
- delivery framing excluded reflector 03, caravan 00 and NOCTIL ring.

These were fixed in Wave 1.

## Wave 1 checkpoint

Primary project revision `2`, sceneSequence `0`.

Scene receipt:

- objects `407`;
- meshes `395`;
- materials `9`;
- evaluated triangles `35,028`;
- Wave-1 named objects `310`;
- bad residual object scales `0`;
- zero-dimension meshes `0`;
- `.blend` `4,134,586 B`, etag `5581ef232d24e37ea589dffe4514eb78`;
- GLB `2,474,196 B`, etag `0d351e8a81781acb64cf69db0134e39f`.

Implemented:

- terrain-aware contact correction for reflectors, caravans and refuge;
- reflector foundations, anchors, guying, thermal/power cabinet, cable trunk, service platform/rail, upper access ladder, gimbal/yoke, mirror backing ribs, twin actuators and sensor mast;
- caravan torsion rails, bogies, suspension links, wind cowl, service bays, cargo pods, heat fins, canopy structure and protected beacon;
- refuge six-foot support contact (full refuge kit remains open);
- delivery camera reframed to contain all required macro anchors;
- QA player-height camera added, explicitly non-runtime.

Contact gate: all checked gaps satisfy `|gap| <= 0.25 m`; reflector masts sit at `+0.060 m`, refuge `+0.080 m`, caravan tracks range `-0.045…+0.245 m`.

## Wave 1 reproducibility

Independent replay project revision `2` matches primary exactly on:

- 407 objects;
- 395 meshes;
- 9 materials;
- 35,028 evaluated tris;
- 310 Wave-1 objects;
- all 15 checked terrain-contact gaps;
- delivery camera transform/lens;
- GLB size `2,474,196 B`;
- zero bad scales / zero degenerate meshes.

Replay `.blend` also equals 4,134,586 B; etags differ and are not a semantic gate.

Persisted upgrader: `art_source/worlds/umbra/upgrade_wave1.py`. Detailed receipt: `art_source/worlds/umbra/WAVE1_RECEIPT.md`.

## Visual epistemic state

Wave-0 delivery/scale/aerial renders were successfully published, but this session's client download path did not expose image bytes to the agent for direct pixel inspection. Therefore **direct visual-art PASS is still REVIEW / not claimed**. Objective projection/contact checks are PASS; human/direct rendered-image review remains required before final art acceptance.

## Current blockers / open gates

1. `BLOCK-W04-001`: planet physical radius/orbital representation.
2. `BLOCK-W04-002`: production engine / target GPU and UMBRA runtime art budgets.
3. `BLOCK-W04-003`: final NOCTIL design/rig/attack contract.
4. `BLOCK-W04-004`: human/direct visual review.
5. `BLOCK-W04-005`: durable provider-independent binary custody (`.blend` + GLB + dependencies + stable receipt) under MR-EXO-001.
6. Final UVs/PBR/texel density/material budget.
7. Refuge production modular kit.
8. Quest-linked terrain/environment cells M01–M04.
9. Low-light/color-vision/combat-readability acceptance.
10. Shared-mesh/instancing optimization measurement.
11. Collision, LOD/HLOD, UMBRA-specific runtime import/traversal/profile receipt.
12. Integrator registry ACK readback.

## Next three actions

1. Close the branch continuity loop against current main, then build `W04/ARCH/014` refuge modular production kit and `W04/TERRAIN/011` quest-linked terrain cell archetypes; keep physical planet-scale values abstract.
2. Recover a durable binary checkpoint for Wave 1 under MR-EXO-001, then run `W04/OPT/021` and `W04/VIS/022`: measured instancing optimization plus post-Wave-1 image/readability defect loop.
3. Coordinate `W04/EXPORT/020` with integration owner for bounded GLB import, collision and traversal/profile receipt before locking LOD/GPU budgets.

## Critical operating rule on resume

Always RESYNC issue #7, `ops/fleet/registry.json`, branches/PRs, current `main`, Linear `ROT-119`, current fleet custody contract and both Blender project revisions before any new mutation. If `main` advanced, reconcile normally; never force. After any repo-owned source/doc change, regenerate exact root `MANIFEST.json` as the final content change and let the Gauntlet prove continuity rather than rerunning blindly.
