# NACRE WORLD MACRO — cold handoff

AGENT: AGENT-3D-NACRE-01
CLAIM: CLM-NACRE-WORLD-MACRO-001
BRANCH: art/world-nacre-001
FLEET EPOCH: 1
FLEET STATUS: active
COORDINATION ACK: issue #7 comment 5648339684
R4 FOLLOW-UP: issue #7 comment 5648897202
DRAFT PR: #17
PRIMARY PROJECT: a49fc6f3-fedb-40a5-913f-10a08debb0e1 @ revision 5
CLEAN REPLAY: 4750e054-b063-4ab8-afc9-214462f36128 @ revision 2
LATEST MAIN OBSERVED: 26ae20f5d1b47d1efa0d54b20124ed93cbc0b43e
LAST MAIN ACTUALLY MERGED: 758a9b6326a7d061f1e304abe9b1593b6b2d1a66
NORTH STAR: deliver a recoverable, reproducible Nacre macro-foundation without inventing planetary canon; release only after human art + exact native runtime gates.

## DONE
- Repo/canon/pipeline/fleet authority recovered.
- Atomic claim is now `active` in `main:ops/fleet/registry.json`, epoch 1, with five stable asset IDs.
- Planet physical scale remains separated from authored/rendered blockout; radius/diameter intentionally UNKNOWN.
- R4 macro foundation canonicalized from versioned Blender generator; independent clean replay matches exact semantic SHA256 `48742ba2dc253a626fb807799a55e2c83f2e87f437cf761b66522bac7ba88787`.
- R4 structural QA: 130 objects, 97 meshes, 30 curves, 10/10 bridge links, 2.9999–3.0 m endpoint clearance, 0 bridge penetrations, 0 non-unit scales, 0 degenerate dimensions.
- R5 collision pass added 12 deterministic static traversal proxies using Godot `-colonly`: 10 archive bridges + entry bridge + entry platform.
- R5 proxy containment PASS and GLB export log confirms all 12 collision mesh names were exported.
- Primary + clean replay R5 collision digest match exactly: `af7b2d53c2700fb841205b776906150b3429a809107902d56799e6b92309adf1`.
- Collision generator persisted as `art_source/nacre_world_macro/collision_r5.py` and receipt as `qa-r5.yaml`.
- LOD policy resolved for this tier: use Godot imported-scene automatic mesh LOD by default; do not author duplicate manual LOD chains without profiling evidence.

## PRIMARY R5 RECEIPTS
- Project `a49fc6f3-fedb-40a5-913f-10a08debb0e1`, revision 5.
- `.blend`: 3,587,945 bytes / etag `c338414fba3fa23d2d229264068bfad5`.
- GLB: 3,850,332 bytes / etag `bbc4e71f186a1ae408e293393a434da8`.
- Collision proxy count: 12.
- Collision digest: `af7b2d53c2700fb841205b776906150b3429a809107902d56799e6b92309adf1`.

## CLEAN REPLAY R5
- Project `4750e054-b063-4ab8-afc9-214462f36128`, revision 2.
- Same 12 proxy names, transforms/dimensions contract and exact collision digest.
- 0 containment violations.

## COLLISION POLICY
Included now:
- `NACRE_COLL_BRIDGE_00-colonly` … `NACRE_COLL_BRIDGE_09-colonly`
- `NACRE_COLL_ENTRY_BRIDGE-colonly`
- `NACRE_COLL_ENTRY_PLATFORM-colonly`

Explicit waivers:
- archive chamber hulls: must remain interior-aware shells; do not create solid convex chambers that would block future interiors;
- global shell: collision must be regional/tiled with gameplay cells, never one monolithic planet-shell collider;
- service rings: not currently declared player-traversable.

## NATIVE DELIVERY / ENV_BLOCKED
Exact Godot import is still unexecuted. The blocker is artifact transport, not an observed asset/runtime failure:
- isolated executable container has no general DNS egress;
- fresh provider-signed GLB URL returned storage `InvalidArgument` through browser automation (credential-date mismatch against X-Amz-Date);
- a second direct fetch surface returned `target_unreachable`;
- container direct-download safety requires a web-opened safe URL, but the signed R2 storage URL is rejected by that allowlist.

Therefore: no Godot PASS, no asset FAIL, no fabricated fleet-native receipt.

The repo already contains a qualified Godot 4.7.2 CPU visual runbook (`evidence/visual-display-runbook.md`). Once exact R5 GLB bytes coexist with that runtime, the next native gate is import → inspect node/material/scale → confirm 12 `-colonly` proxies become collision-only static bodies → traversal smoke test → native receipt.

## FILES OWNED
- `art_source/coordination/CLM-NACRE-WORLD-MACRO-001.md`
- `art_source/nacre_world_macro/HANDOFF.md`
- `art_source/nacre_world_macro/build_macro.py`
- `art_source/nacre_world_macro/collision_r5.py`
- `art_source/nacre_world_macro/manifest.yaml`
- `art_source/nacre_world_macro/qa-r3.yaml`
- `art_source/nacre_world_macro/qa-r4.yaml`
- `art_source/nacre_world_macro/qa-r5.yaml`

Global `MANIFEST.json` is not producer-owned. The branch’s old generated projection is stale after R5 and must not be treated as a valid receipt. Delivery checkout must inherit current-main MANIFEST then run `python3 tools/project_control.py refresh`; fleet guard allows that projection only if exact.

## OPEN GATES
- Human `GATE-ART`.
- Exact R5 GLB Godot import/material/scale.
- Collision runtime traversal.
- HLOD/streaming profile.
- Target-hardware performance.
- Global MANIFEST refresh + fleet native delivery receipt.
- Branch resync with latest main before integration.

## NEXT 3
1. Co-locate exact R5 GLB/.blend with a checkout containing qualified Godot 4.7.2; run editor import and verify the 12 `-colonly` conversions.
2. Run collision traversal + scale/material smoke test; write native receipt tied to exact R5 GLB hash and run fleet `delivery`.
3. Run human creative-director review; only then decide between art R6 fixes or optimization/HLOD/performance work.

CLAIM STATUS: KEEP / IN_PROGRESS

RECOVERY: read latest `main` fleet protocol/registry, this handoff, `manifest.yaml`, `qa-r5.yaml`; inspect primary revision 5 or rebuild R4 with `build_macro.py` then apply `collision_r5.py`. Never infer planetary radius/diameter from this blockout.
