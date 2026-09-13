# NACRE WORLD MACRO — cold handoff

AGENT: AGENT-3D-NACRE-01
CLAIM: CLM-NACRE-WORLD-MACRO-001
BRANCH: art/world-nacre-001
FLEET: active / epoch 1
ACK: issue #7 comment 5648339684
R5 FOLLOW-UP: issue #7 comment 5652875105
DRAFT PR: #17
PRIMARY BLENDER: a49fc6f3-fedb-40a5-913f-10a08debb0e1 @ revision 5
CLEAN REPLAY: 4750e054-b063-4ab8-afc9-214462f36128 @ revision 2
MAIN RESYNCED: 26ae20f5d1b47d1efa0d54b20124ed93cbc0b43e
RESYNC MERGE: 32e3488dc4c5715217c571effeeac88c3dd0698e
NORTH STAR: deliver a recoverable, reproducible Nacre macro-foundation without inventing planetary canon; release only after human art and exact native runtime gates.

## DONE
- Repository/canon/pipeline/fleet authority recovered.
- Claim is ACTIVE in fleet registry generation 8 with five stable interface IDs.
- Branch rebuilt non-force on `main@26ae20f5...`; final compare at resync: behind_by=0, exact main merge base, only Nacre-owned files in diff. Stale producer-side global MANIFEST projection was eliminated from the tree.
- Planet physical scale separated from blockout; radius/diameter intentionally UNKNOWN.
- R4 macro geometry is reproducible from `build_macro.py`; primary and clean replay macro semantic SHA256 match exactly: `48742ba2dc253a626fb807799a55e2c83f2e87f437cf761b66522bac7ba88787`.
- R4 structural QA: 130 objects, 97 meshes, 30 curves, 10/10 bridge links, ~3 m surface clearance, 0 penetrations, 0 non-unit scales, 0 degenerate dimensions.
- R5 adds 12 reproducible Godot `-colonly` traversal proxies through `collision_r5.py`: 10 archive bridges, entry bridge and entry platform.
- Primary + clean replay R5 collision digest match exactly: `af7b2d53c2700fb841205b776906150b3429a809107902d56799e6b92309adf1`.
- Export logs contain all 12 collision proxy meshes; 0 containment violations.
- Explicit collision waivers prevent unsafe shortcuts: no solid archive chamber hulls, no monolithic global-shell collider, no service-ring collision before traversability is declared.
- LOD decision for this tier: use Godot imported-scene automatic mesh LOD by default; manual LOD/HLOD waits for profiling evidence.
- Isolated native validation harness is versioned under `art_source/nacre_world_macro/native_probe/` plus `run_native_probe.py`.

## R5 PROVIDER RECEIPTS
- Primary revision 5 `.blend`: 3,587,945 bytes / etag `c338414fba3fa23d2d229264068bfad5`.
- Primary revision 5 GLB: 3,850,332 bytes / etag `bbc4e71f186a1ae408e293393a434da8`.
- Clean replay revision 2 reproduces the collision contract.
- Collision digest: `af7b2d53c2700fb841205b776906150b3429a809107902d56799e6b92309adf1`.

## NATIVE PROBE — READY, NOT YET EXECUTED
Runner:
`python3 art_source/nacre_world_macro/run_native_probe.py --godot <qualified-godot-4.7.2> --glb <exact-r5.glb> --out <evidence-dir>`

The wrapper:
1. validates GLB magic and hashes the exact artifact;
2. creates a temporary standalone Godot project from `native_probe/project.godot` + `probe.gd`;
3. runs headless editor import and rejects logged ERROR/SCRIPT ERROR even if process exit is zero;
4. loads the imported PackedScene;
5. requires zero visible `NACRE_COLL_*` MeshInstance3D proxies;
6. requires at least 12 StaticBody3D and 12 CollisionShape3D nodes;
7. checks macro max span remains 1200–1600 m and at least five material roles survive;
8. writes fleet-compatible `native-receipt.json` tied to artifact SHA256 plus import/probe logs.

## ENV_BLOCKED — EXACT ASSET TRANSPORT
No Godot import has occurred. The same blocker has been reproduced across independent surfaces:
- executable container has no general DNS egress;
- provider-signed GLB request through live browser returned storage `InvalidArgument` credential-date mismatch;
- independent direct fetch returned `target_unreachable`;
- container downloader requires the signed storage URL to first pass a safe web-open boundary, which rejects it.

Classification: `ENV_BLOCKED_ARTIFACT_TRANSPORT`, not asset FAIL and not Godot PASS. Do not fabricate native evidence.

The repo already has qualified Godot 4.7.2 CPU visual infrastructure in `evidence/visual-display-runbook.md`; the missing condition is co-location of the exact R5 GLB bytes with that runtime.

## FILES OWNED
- `art_source/coordination/CLM-NACRE-WORLD-MACRO-001.md`
- `art_source/nacre_world_macro/HANDOFF.md`
- `art_source/nacre_world_macro/build_macro.py`
- `art_source/nacre_world_macro/collision_r5.py`
- `art_source/nacre_world_macro/manifest.yaml`
- `art_source/nacre_world_macro/qa-r3.yaml`
- `art_source/nacre_world_macro/qa-r4.yaml`
- `art_source/nacre_world_macro/qa-r5.yaml`
- `art_source/nacre_world_macro/run_native_probe.py`
- `art_source/nacre_world_macro/native_probe/project.godot`
- `art_source/nacre_world_macro/native_probe/probe.gd`

Global `MANIFEST.json` is not producer-owned. At the resync it is inherited from current main, not the stale R4 producer projection. Because R5/native-probe files are branch additions, a clean delivery checkout must run `python3 tools/project_control.py refresh` and then fleet guard/delivery before merge.

## OPEN GATES
- Human `GATE-ART`.
- Exact R5 GLB native Godot import/material/scale.
- Runtime collision/traversal.
- Current-tree MANIFEST refresh + fleet native delivery.
- HLOD/streaming profiling.
- Target-hardware performance.

## NEXT 3
1. Obtain a transferable exact R5 GLB/.blend file reference (or repair provider signed-download generation) and co-locate it with the qualified Godot 4.7.2 runtime.
2. Execute `run_native_probe.py`; if PASS, add normal traversal smoke test and fleet `delivery` receipt against exact GLB SHA.
3. Run human creative-director review; rejected art findings become atomic next-revision tasks, otherwise proceed to HLOD/streaming/performance profiling.

CLAIM STATUS: KEEP / IN_PROGRESS

RECOVERY: read latest main fleet registry/protocol, this handoff, `manifest.yaml` and `qa-r5.yaml`; inspect primary revision 5 or rebuild macro with `build_macro.py` then apply `collision_r5.py`. Never derive planet radius/diameter from this blockout.
