# Gauntlet evidence and decisions

Canonical protocol: [GAUNTLET_LOOP_MASTER.md v1.0](https://github.com/rotprods/rot.knowledge/blob/e8be6757b80eeab243c3f7000e343be076bd8642/prompts/engineering/GAUNTLET_LOOP_MASTER.md), blob `7e3fa190e980936a51858059c014e6cc192e091e`.

Flow applied: reconstruct → actual changes → impact model → attack → severity → patch → native tests → evidence → restore → cold resume → update state → next frontier. Six recursive iterations on the same unresolved problem trigger reassessment; this is not a promise to loop indefinitely.

## Impact model

Inputs: player controls, UI buttons, local save bytes, GLB asset. Dependents: scene actors, quest UI, environment state, checkpoint and save. Trust boundary: save parsing; no runtime network or external secrets. Failure cases: skipped prerequisites, duplicate rewards, interrupted writes, broken checkpoints, geometry blocking traversal, repeated damage in an attack, attacks crossing cover. Recovery: prior valid save generation, deterministic quest ledger, reproducible source package. Single-player save store assumes one running game process; simultaneous instances writing the same save are not qualified.

## Iteration 1 — native foundation

Implemented the first Terra chain, controller, combat, AI, save, geometry import and tests. Godot parsed/imported the project after correcting an inferred Vector3 type in the world script. State/recovery suite: 26 checks passed. Scene integration initially passed 17/18.

**P1 EXO-F001:** the portal ramp ended below the landing at its front edge. A character walking into the portal stopped at z≈−80.87, y≈0.93. This was a physics failure despite the source GLB rendering correctly. Corrected the ramp position, length and angle. Regression: actual CharacterBody traversal past z−84 with height above 1.2 m.

**P3 EXO-F002:** intentionally corrupt save files emitted native parser errors even when recovery succeeded. Replaced convenience JSON parsing with an explicit parser/error return so expected corruption is handled without false engine-error noise. Tests still verify backup recovery; no error is silently converted into success.

## Iteration 2 — visual and traversal review

Scene integration passed 18/18, portal final position ≈[0,1.48,−85.56]. A real Godot render was produced under Xvfb with Mesa llvmpipe CPU rendering. Review found excessive light, primitive block silhouettes and low-contrast footer controls. Reduced key/ambient intensity, replaced block bodies with articulated capsule/sphere armor, added movement articulation, lowered the camera, added health/stamina bars and a dark control strip. These changes improve prototype readability; they do not achieve AAA art quality.

The local environment blocks Unix sockets and privileged package setup. Godot itself runs as a standalone binary. An authenticated virtual display and the game can communicate by TCP when launched in the same command process group; separate command sandboxes do not share that loopback namespace. No GPU was discovered or fabricated. No Mac bridge was opened. `tests/capture_visual.py` closes its virtual display on completion.

## Iteration 3 — hostile combat case and final checks

**P1 EXO-F003:** enemy area damage originally checked distance/height but did not verify intervening solid cover. Added a physics ray against the collision layer before applying damage. Added a regression with a solid wall between the player and an enemy strike. The test itself required an explicit MeshInstance3D type; that parse error was fixed before rerunning the suite.

The final native gate counts are recorded in JSON receipts, not inferred from this narrative. Each run deletes old receipts before execution, requires a fresh receipt, and fails on script errors, timeout, nonzero return or a failed assertion. `run_gauntlet.py` checks import, state/recovery, native integration and a runtime smoke test. No unexecuted test is a PASS.

## Iteration 4 — AAA source-fidelity regression (2026-09-14)

**P1 EXO-F004 — PROXY_POLISH_LOOP:** portfolio review of active world PRs showed a recurrent project-level risk: technically valid Blender scenes, deterministic geometry, collision/LOD receipts and material systems can consume multiple waves while hero-visible source meshes remain explicitly classified by their own owners as blockout, semantic proxy or non-final art. The failure is architectural, not a request for more noise/material layers.

### Root cause
The project had a strong `raw AI mesh != final asset` rule but no universal fail-closed promotion gate between `BLOCKOUT/PROXY` and expensive final lookdev. Consequently an agent could keep improving technical density and cosmetic response without first proving that the source carried enough silhouette/proportion/construction information for the intended close-up.

### Correction
Added `docs/AAA_ASSET_FIDELITY_GATE_V1.md`, X100 schema-v3 fidelity states, `tools/aaa_asset_gate.py`, render-economics estimator and unit tests. Global law:

`BLOCKOUT != HERO_ASSET`

`MORE_POLYGONS != MORE_REALISM`

Hero promotion now requires evidence for silhouette, proportion, construction logic, semantic part separation, material-domain readiness, UV/bake readiness and close-up stress. A `BLOCKOUT/PROXY` promotion also requires explicit source rebuild/structural-upgrade evidence. Raw reconstruction cannot self-certify final art.

### Salvage rule
No world is reset. Verified layout, traversal, collision, streaming, procedural placement, runtime import and other technical work remain valid unless the new identity geometry invalidates them. At next owner resync assets are relabeled and `PROXY_POLISH_DEBT` is identified; only high-value identity gaps are rebuilt first.

### Asset Factory
Tier S/A assets may route through manual/procedural/CAD/photogrammetry/multiview/hybrid reconstruction. Tripo H3.1 multiview, Meshy multi-image and Hunyuan3D v3 were observed as live connected candidates on 2026-09-14, but provider/version/cost must be revalidated before spend. Provider output remains `BASE_CANDIDATE` until the same hero gate passes.

### Render economics
Resolution alone no longer authorizes render-time/cost claims. Benchmark `EASY/MEDIAN/WORST` frames on the actual engine/device/settings, estimate measured seconds/frame, then apply current rate. Provider price is live data, not a canonical constant.

### Evidence status
`tools/aaa_asset_gate.py` has explicit unit coverage for valid hero qualification, blocked proxy→hero jump, raw reconstruction rejection, polycount insufficiency, human gate requirement for AAA claims and runtime qualification receipts. The estimator has independent arithmetic/fail-closed tests. Project-wide native Gauntlet remains manual/cost-quarantined; this protocol change does not fabricate a Godot/GPU/art PASS.

## Promotion boundary and open risks

Promotion applies only to this prototype's tested behavior. It does not imply that the full game, final art, platform packages, input accessibility or human usability are complete. No known unresolved P0/P1 in the covered regression cases; broader production acceptance remains open.

- P2: full manual run without controlled test setup has not been performed. Integration tests reposition actors to isolate mechanics.
- P2: no gamepad, remapping, adjustable FOV or mobile touch; the current target is keyboard/mouse desktop.
- P2: one enemy archetype plus ATLAS, two boss attack families and parameter phases, one functional melee family. Full plan has more.
- P2: characters are procedural stand-ins; terrain is a blockout; portal remains high-draw-call reference geometry. Textures, UV/LOD, skeletons, IK and authored locomotion remain.
- P2: no audio production, voice, full quest alternatives, native platform export or target-device performance qualification.
- P2: one writer per save file; no multi-process lock or parallel automated writer qualification. Future background activations must use version guards on shared project artifacts and stop on conflicts.
- P3: save schema v1 rejects unknown future versions; migrations must be introduced with their own fixtures before schema v2.

Simplification review: no network backend, room server, procedural galaxy simulation, agent dispatcher or payment system was added. Domain progress and save handling are separate; actor and world scripts remain direct. Future extraction of world construction from interaction code should follow measured editing friction, not speculative abstraction.

Final UI review: replaced theme-sized progress widgets with explicit 6 px bars after the render exposed unwanted minimum height. Re-rendered and smoke-tested. The fresh archive reconstruction passed all four native gates without a pre-existing import cache.
