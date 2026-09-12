# LEVIATHAN · Cold-Recovery Handoff

AGENT: `AGENT-LEVIATHAN-10`
SESSION: `ART-LEVIATHAN-001-20260912T2123+0200`
CLAIM: `CLM-W10-WORLD-LEVIATHAN-001`
BRANCH: `art/world-leviathan-001`
HEAD BEFORE HANDOFF COMMIT: `e6e06d4f70b80a10a530dccade4e26fc85718e30`
NORTH STAR: Deliver a recoverable LEVIATHAN world-production foundation whose living-planet identity is legible, whose visual deformation is decoupled from stable gameplay collision, and whose canonical Puerto/Jardines/SOMA interfaces survive technical QA without invented planet scale or engine budgets.

## DONE

- Repository/bootstrap/authority recovery from `rotprods/-` completed.
- Main authority snapshot used for claim: `4c2fa044080004609ea6df45f34b2a784536507a`.
- Multi-agent collision audit executed; Terra, Ares IX, Pelagos, Khepri, Nacre, Umbra and Vanta were observed as reserved/claimed and not touched.
- A concurrent UMBRA claim was detected after an attempted branch reservation; UMBRA was abandoned before build and no cross-scope file was modified.
- Atomic LEVIATHAN claim persisted at `production/claims/CLM-W10-WORLD-LEVIATHAN-001.yaml`.
- Evidence-bound World Bible created.
- Master asset/coverage registry created.
- First 10 tasks + DoD created and resynced.
- Dedicated remote Blender project created and qualified: `2577a7b6-ebd7-4d31-a645-620e4b73a95d`.
- Blender observed: 5.2.0 LTS, metric, `1 BU = 1 m`, Eevee, 24 fps.
- WAVE-1 master blockout committed to remote revision 2.
- Three canonical region interfaces exist: Puerto de la Herida, Jardines Inmunes, Cámara de SOMA.
- Stable collision layer is separate from visual contraction membranes.
- 1.85 m human scale reference measured.
- SOMA chamber corrected from an initial 64.4 m envelope to exact 58 m outer envelope.
- Non-portable AREA light replaced by portable POINT; revision-2 GLB export no longer reports the AREA-light warning.
- Geometry QA: no required-object miss, accidental scale, zero-poly mesh or degenerate polygon detected.
- Camera math: all three region centers are in the overview frame; SOMA center is in the gameplay camera frame.
- Revision-2 editable `.blend` and portable GLB exist.
- Revision-2 overview and SOMA gameplay renders exist as receipts.
- Versioned generator source created: `art_source/worlds/leviathan/tools/build_master_scene.py`.
- Validation/history of recovered failures persisted in `validation.json`.

## IN PROGRESS

- `W10/BLEND/003`: generator/source exists and revision-2 remote scene exists; independent clean-project cold rerun of the versioned script remains before DONE.
- `W10/REGION/004`: Puerto blockout awaits direct visual/art review.
- `W10/REGION/005`: Jardines blockout awaits direct visual/art review.
- `W10/REGION/006`: SOMA blockout awaits direct visual/art review.
- `W10/TECH/007`: structure-level collision separation passes; runtime traversal/collision test is not run.
- `W10/MAT/008`: 11 material roles exist; final calibrated PBR textures/UV/channel validation are not done.
- `W10/ECO/009`: silhouette proxies exist; final anatomy/rig/animation are not done.
- `W10/QA/010`: structure/export receipts exist; direct pixel-level visual review and engine import remain open.

## BLOCKED

- `LEV-BLK-001`: physical radius/diameter and planetary parameters are absent from current canon. Do not invent them.
- `LEV-BLK-002`: Unreal is a production candidate, not yet the qualified integrated production engine.
- `LEV-BLK-003`: target hardware/GPU/preset is unresolved; hard triangle/texture/shader budgets remain unqualified.
- `LEV-BLK-004`: final SOMA anatomical/art-direction decision required before final sculpt/rig.
- `LEV-BLK-005`: final playable-region dimensions required before final streaming topology/density.

## FILES MODIFIED / CREATED

- `art_source/coordination/ART-LEVIATHAN-001-OWNERSHIP.md`
- `production/claims/CLM-W10-WORLD-LEVIATHAN-001.yaml`
- `art_source/worlds/leviathan/WORLD_BIBLE.md`
- `art_source/worlds/leviathan/MASTER_ASSET_LIST.yaml`
- `art_source/worlds/leviathan/TASKS.yaml`
- `art_source/worlds/leviathan/STATUS.yaml`
- `art_source/worlds/leviathan/validation.json`
- `art_source/worlds/leviathan/tools/build_master_scene.py`
- `art_source/worlds/leviathan/HANDOFF.md`

## ASSETS CREATED / IMPLEMENTED AS BLOCKOUT OR PROXY

- L2 stable substrate + six large living-tissue masses.
- Major vascular trunks, diagnostic conduit and five rib/cartilage macrostructures.
- Puerto: stable deck, scar ring, eight suture clamps, six soft colony modules + technical bellies, refuge beacon and airlock valve.
- Jardines: stable path, three lymph channels, pulse-algae family, gardener proxies and lymph-whale silhouette proxy.
- Traversal: organic visual path + eight stable collision pads.
- SOMA: exact 58 m chamber envelope/floor, three biological bridges, three safe valves, three visual contraction membranes, non-final SOMA silhouette/halo/cilia interface.
- Adversary scale proxies: Fagocito guardián, Extractor de pulso, Colonia parasitaria.
- Four cameras, four portable lights, 100 m scale grid and 11 blockout material roles.

None of the above is claimed as final AAAA asset quality.

## TESTS / RECEIPTS

Remote project: `2577a7b6-ebd7-4d31-a645-620e4b73a95d`, final committed revision: `2`.

Revision 2:
- objects: 125;
- meshes: 90;
- curves/fonts: 25;
- materials: 11;
- cameras: 4;
- lights: 4 (`POINT`, `SUN` only);
- collision objects: 12;
- visual contraction objects in collision collection: 0;
- human reference: 0.55 × 0.40 × 1.85 m;
- SOMA ring: 58 × 58 × 6.4 m;
- SOMA stable floor: 58 × 58 × 6 m;
- editable blend: 4,034,313 bytes, etag `a2156686fbcad1ff1a36c0b5c7ea7831`;
- GLB: 4,397,196 bytes, etag `17a660fe9198015d9e2a01514efdbb10`;
- overview render: artifact `f467205d40557710bcd580d10393a1ec`;
- SOMA gameplay render: artifact `5a66cdc6560bdf42b7a62531d45513a1`;
- interactive revision-2 scene preview surfaced to the user.

Full gate matrix and recovered failures: `art_source/worlds/leviathan/validation.json`.

## DECISIONS

- No physical planet size invented.
- 720 × 480 m is explicitly a reversible authored test-cell proposal, not planet/playable-world canon.
- First-version traversal collision remains stable beneath independent visual tissue deformation.
- 58 m is treated as the external chamber envelope for the current SOMA blockout.
- SOMA current object is explicitly a combat-scale/silhouette interface, never final anatomy.
- Only portable `POINT`/`SUN` lighting remains after glTF warning reconciliation.
- No hard poly/texture/shader budget until engine/hardware qualification.

## DEPENDENCIES

- Current design authority: `design/EXOVANT_BIBLIA.md`, `design/EXOVANT_DATA.json`.
- Art runbook: `docs/ART_PRODUCTION.md`.
- Remote Blender learning event: `learning/.../LRN-EXO-20260912-BLENDER.json`.
- Integration authority must reconcile global shared state; this claim intentionally did not edit global STATE/PLAN/HANDOFF/PROGRESS.

## RISKS

- Direct agent pixel-level visual inspection was unavailable in this client despite rendered receipts and interactive scene preview; art PASS is therefore not claimed.
- Living tissue/materials are WAVE-1 roles, not hyperreal final anatomy/materials.
- No LEVIATHAN engine import has been run.
- No runtime performance profile exists.
- No final LOD/UV/texture/rig/animation pass exists.
- L0/L1 planet-scale work remains blocked by missing physical scale canon.

## NEXT 3 ACTIONS

1. Cold-rerun `tools/build_master_scene.py` in a clean dedicated Blender project and compare object/scale/material/camera receipts against revision 2; fix generator drift if any.
2. Perform direct visual/art review of revision-2 overview/SOMA preview, convert every framing/intersection/material/readability defect into W10 tasks, and iterate the blockout.
3. Qualify and execute a LEVIATHAN runtime import smoke test for scale/material/collision; keep engine-specific LOD/performance claims blocked until production-engine/hardware decisions are qualified.

CLAIM STATUS: **KEEP**

The branch must not be merged as “world complete.” A draft PR is appropriate for coordination/review only.
