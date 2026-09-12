# STATUS — CLM-SYLVA-MACRO-001

**Agent:** `AGENT-SYLVA-MACRO-01`  
**Session:** `20260912-SYLVA-MACRO-001`  
**Branch:** `art/world-sylva-prime-macro-001`  
**Remote Blender:** `05dce898-753d-4ff6-a4b0-31757dc868d8` @ revision `4`  
**State:** `IN_PROGRESS / VERIFIED R4 CHECKPOINT`

## Scope boundary

Owned here:
- km-scale local terrain foundation;
- canonical region anchors and spatial relationships;
- macro diagnostic root topology placement;
- macro traversal corridors;
- streaming metadata/envelopes;
- macro collision proxies;
- typed sockets that consume the neural-root kit owned by `CLM-SYLVA-PROC-NROOT-001`.

Explicitly not owned:
- reusable meso neural-root modules;
- final VESPER;
- NPCs;
- fauna/vegetation species assets;
- final architecture/interiors;
- gameplay/quest/runtime code.

## Coverage

| Task | Priority | State | Receipt |
|---|---|---|---|
| SYLVA/MACRO/001 Evidence pack | P0 | DONE | claim + draft PR #3 |
| SYLVA/MACRO/002 Coordinate/scale contract | P0 | DONE | Blender metadata + World Bible |
| SYLVA/MACRO/003 World-bible delta | P0 | DONE | `WORLD_BIBLE_MACRO.md` |
| SYLVA/MACRO/004 Macro terrain | P0 | DONE (BLOCKOUT) | Blender r4 + generator |
| SYLVA/MACRO/005 Structural root topology | P0 | REVIEW | 6 primary + 8 secondary diagnostic roots; reusable kit delegated to PR #6 |
| SYLVA/MACRO/006 Puerto del Injerto | P1 | REVIEW | regional foundation + collision + two typed kit sockets |
| SYLVA/MACRO/007 Bosque de las Frases | P1 | REVIEW | 3 route families + collision + three typed kit sockets |
| SYLVA/MACRO/008 Cámara de VESPER envelope | P1 | REVIEW | boss-space envelope + collision + three typed kit sockets; no final boss |
| SYLVA/MACRO/009 Streaming / traversal / collision interfaces | P0 | DONE (INTERFACE) | r4: 16 cells + 3 region envelopes + 8 collision proxies |
| SYLVA/MACRO/010 Export + handoff | P0 | IN_PROGRESS | `.blend` + GLB r4 + manifests/receipt; engine/human gates pending |

## R4 scene receipts

- **136 objects** total.
- **84 mesh objects**.
- **8 curve objects**.
- **~15,840 blockout triangles**.
- Local terrain bounds remain **12,000 × 12,000 m**, classified `PROPOSAL`.
- 6 primary + 8 secondary **diagnostic** macro roots.
- 4 diagnostic traversal route guides.
- 16 L3 streaming cells, each **3,000 m** square (`PROPOSAL`, backend `ENGINE_TBD`).
- 3 L4 hero-zone envelopes: Puerto 1,200 m, Bosque 1,700 m, VESPER 1,200 m (`PROPOSAL`).
- 8 typed sockets consuming provider IDs from `CLM-SYLVA-PROC-NROOT-001`.
- 8 macro collision objects including a 289-vertex / 256-face low-res terrain collision mesh.
- Provider meshes copied into this claim: **0**.
- Invalid provider sockets: **0**.
- Non-unit-scale mesh/curve objects: **0**.
- Non-`SYLVA_` objects: **0**.
- Final-scope violations: **0**.

## Remote artifacts

- `.blend` r4: **2,097,180 bytes**, etag `4470d8530489f327fb2d3c33c31e983d`.
- GLB r4: **1,074,844 bytes**, etag `f793339fd893d9829a84a43d21141054`.
- Export completed without the prior unsupported `AREA`-light warning.

## Visual-signal QA

The original direct `Render Result` pixel validator produced a false zero and is rejected as a validator.

Independent file-backed smoke on `SYLVA_CAM_Puerto`:
- resolution: 320×180;
- PNG bytes: 72,450;
- mean RGB: ~0.07998;
- variance: ~0.00392;
- max RGB: ~0.9882;
- result: `PASS_NONBLANK`.

This proves image signal exists. It **does not** approve composition or final art.

## Progress metrics

These are maturity estimates for this **atomic macro claim only**, not global EXOVANT progress.

- Macro/blockout family coverage: **100%** of declared macro families represented.
- Modeling maturity: **45%** — foundation/blockout; no final terrain sculpt/surface pass.
- Materials maturity: **10%** — diagnostic/lookdev only.
- Optimization maturity: **25%** — streaming/collision interfaces exist; LOD/HLOD and target profiling pending.
- Integration maturity: **35%** — portable GLB + provider sockets; engine import not run.
- QA maturity: **60%** — technical r4 QA passes; human art, engine traversal/collision and GPU performance remain open.

## Gates

| Gate | State |
|---|---|
| CANON | PASS with planetary radius/diameter `UNKNOWN_BLOCKED` |
| OWNERSHIP | PASS — PR #6 boundary explicit; no provider meshes copied |
| GEOMETRY / NAMESPACE / SCALE | PASS blockout |
| STREAMING INTERFACE | PASS_PROPOSAL |
| ROOT-KIT SOCKET CONTRACT | PASS |
| COLLISION PROXY PRESENCE | PASS_BLOCKOUT |
| EXPORT | PASS_REMOTE_GLB |
| EDITABLE SOURCE | PASS_REMOTE_BLEND |
| ART | PENDING_HUMAN_REVIEW |
| ENGINE IMPORT | NOT_RUN |
| GAMEPLAY TRAVERSAL / COLLISION | NOT_RUN |
| LOD/HLOD | NOT_IMPLEMENTED |
| PERFORMANCE | BLOCKED_TARGET_HARDWARE |

## Open P0

1. Import r4 GLB into the current executable engine path.
2. Instantiate/split render vs `SYLVA_COL_*` collision geometry and validate naming contract.
3. Traverse Puerto → Bosque → VESPER with the real controller; log clearance/camera failures.
4. Human art-direction review of macro silhouettes and route readability.
5. Keep planetary radius/diameter blocked until an explicit ADR/canon decision.

## Open P1

1. Consume actual PR #6 root modules at typed sockets after provider branch is ready for integration; do not recreate them here.
2. Revise regional envelopes from measured gameplay/streaming results rather than intuition.
3. Establish HLOD/vista strategy after engine + target hardware are qualified.

## Persistent outputs

- `art_source/worlds/sylva_prime/macro/generate_sylva_macro.py`
- `art_source/worlds/sylva_prime/macro/add_sylva_macro_interfaces.py`
- `production/manifests/sylva/macro/SYL_MACRO_FOUNDATION_001.yaml`
- `production/receipts/sylva/CLM-SYLVA-MACRO-001-R4.yaml`
- `art_source/worlds/sylva_prime/macro/WORLD_BIBLE_MACRO.md`
- `art_source/worlds/sylva_prime/macro/validation.json` (r3 historical validation)
- `art_source/worlds/sylva_prime/macro/HANDOFF.md`

## Claim

`KEEP / CHECKPOINT` — technical macro foundation is materially advanced, but P0 engine/human gates remain open. Do not mark DONE or merge as final world art.
