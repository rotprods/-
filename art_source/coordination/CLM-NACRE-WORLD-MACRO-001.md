# CLM-NACRE-WORLD-MACRO-001 — ownership + production contract

Status: IN_PROGRESS
Agent: AGENT-3D-NACRE-01
Branch: art/world-nacre-001
Scope: `NACRE / WORLD_MACRO / PLANETARY_FOUNDATION`
Fleet: active / epoch 1
ACK: https://github.com/rotprods/-/issues/7#issuecomment-5648339684
R5 follow-up: https://github.com/rotprods/-/issues/7#issuecomment-5652875105
Draft PR: https://github.com/rotprods/-/pull/17
Primary Blender: a49fc6f3-fedb-40a5-913f-10a08debb0e1 @ revision 5
Clean replay: 4750e054-b063-4ab8-afc9-214462f36128 @ revision 2
Main resynced: 26ae20f5d1b47d1efa0d54b20124ed93cbc0b43e
Resync merge: 32e3488dc4c5715217c571effeeac88c3dd0698e

## Included
- Nacre canon/evidence extraction for this macro cell.
- Physical-planet / playable-area / rendered-representation separation without inventing planetary radius.
- Kilometre-class mineral shell-city blockout.
- Seven archive chambers, surface-connected bridge/docking/load-path network, growth strata and bounded translucent accents.
- Foundational materials and explicit scale references.
- Reproducible Blender macro generator and static traversal collision generator.
- Isolated Godot native-import probe that emits a hash-bound native receipt once exact R5 GLB bytes are available locally.
- Nacre-only manifests, QA and handoff.

## Excluded
- Gameplay/runtime source edits.
- Other worlds.
- Final MNEMOS, final settlements/interiors/hero architecture, NPC/fauna/vehicles/equipment.
- Planet radius/diameter or other unapproved physical canon.
- Global engine decision / Unreal migration / GPU claims.
- Shared STATE/PLAN/global MANIFEST/graph ownership.

## Evidence classes
DOCUMENTED:
- NACRE / Andromeda / Mneme / Casas de Nácar / MNEMOS target.
- 0.26 g / 16 °C reference environment.
- Cities grow inside kilometre-scale mineral shells; biographies are stored/traded in pearls.
- Archivo de MNEMOS uses spherical archive rooms connected by bridges.
- Verified exchange route is Blender `.blend` → GLB → Godot 4.7.2 prototype.

UNKNOWN remains UNKNOWN:
- planetary radius/diameter;
- atmosphere, hydrology, tectonics;
- final playable area;
- final triangle/texture budgets;
- final LOD/HLOD/streaming distances and topology.

PROPOSAL only:
- ~1400 m shell target;
- 184 m archive core diameter;
- exact archive placement, bridge widths and ~3 m surface clearance.

Exact “Flu In / Flow In” repo method remains `PIPELINE_METHOD_NOT_FOUND`.

## Fleet / Git truth
Registry generation 8 marks this claim `active`, epoch 1, owner `AGENT-3D-NACRE-01`, with five stable IDs:
- `NACRE-MACRO-SHELL-001`
- `NACRE-MACRO-LINING-001`
- `NACRE-ARCHIVE-NET-001`
- `NACRE-BRIDGE-NET-001`
- `NACRE-SCALE-REF-001`

The branch was rebuilt non-force on `main@26ae20f5d1b47d1efa0d54b20124ed93cbc0b43e` using a tree based on current main plus only Nacre blobs. Verification immediately after resync: `behind_by=0`, merge-base=current main, no producer-side `MANIFEST.json` modification in diff. Global MANIFEST remains integrator-owned and must be regenerated in the final delivery checkout after branch files are present.

## North Star
Deliver a recoverable, causally constructed and reproducible Nacre macro-foundation legible without logos: mineral shell, pearl lining, archive spheres, surface bridges, docking/maintenance/load paths, growth history, bounded transparency, explicit scale and minimal gameplay collision. Human art approval and exact native runtime qualification remain separate gates.

## Task state
| ID | P | Output | Status |
|---|---|---|---|
| NACRE/MACRO/001 | P0 | Canon/evidence | DONE |
| NACRE/MACRO/002 | P0 | Fleet ownership | DONE — ACTIVE |
| NACRE/MACRO/003 | P0 | Planet/playable/render interface | DONE |
| NACRE/MACRO/004 | P0 | Coverage/interface IDs | DONE |
| NACRE/MACRO/005 | P1 | Reproducible macro blockout | DONE |
| NACRE/MACRO/006 | P1 | Portable material roles | DONE |
| NACRE/MACRO/007 | P1 | Structural causality | DONE_AT_BLOCKOUT |
| NACRE/MACRO/008 | P1 | Visual QA + human review | REVIEW — HUMAN OPEN |
| NACRE/MACRO/009 | P1 | Source/export/collision/native delivery | COLLISION PASS / NATIVE ENV_BLOCKED |
| NACRE/MACRO/010 | P1 | Handoff/release | IN_PROGRESS |

## R4 macro reproducibility
Primary and independent clean replay share exact macro semantic SHA256:
`48742ba2dc253a626fb807799a55e2c83f2e87f437cf761b66522bac7ba88787`

R4 QA: 130 objects; 97 meshes; 30 curves; 10/10 bridge links; 2.9999–3.0 m endpoint clearance; 0 penetrations; 0 non-unit scales; 0 degenerate dimensions; SUN_MNEME_A/B only.

## R5 collision reproducibility
Primary revision 5 adds 12 simple static traversal meshes named with Godot `-colonly`:
- ten archive bridge decks;
- entry bridge;
- entry service platform.

Primary + replay collision digest:
`af7b2d53c2700fb841205b776906150b3429a809107902d56799e6b92309adf1`

Checks: 12/12 proxy names present in export log; 0 containment violations; replay reproduces names/transforms/dimensions.

Waivers: chamber hulls require interior-aware shell collision; global shell must be tiled by gameplay cells; service rings are not yet declared traversable.

## LOD policy
Use Godot editor-import automatic mesh LOD for the imported glTF blockout. Do not author duplicate manual LOD/HLOD chains without profiling evidence.

## Native probe contract
`run_native_probe.py` consumes only a caller-supplied exact GLB and qualified Godot binary. It does not download or substitute assets. It performs editor import, rejects logged ERROR/SCRIPT ERROR, loads the imported PackedScene, requires zero visible `NACRE_COLL_*` proxy meshes, >=12 StaticBody3D, >=12 CollisionShape3D, plausible macro scale and surviving material roles, then writes `native-receipt.json` tied to exact artifact SHA256 plus logs.

## Native blocker
The probe cannot yet be executed because the exact R5 GLB cannot be co-located with the executable environment. Reproduced transport evidence:
- no general DNS egress from isolated execution container;
- provider-signed browser request returned storage `InvalidArgument` credential-date mismatch;
- independent fetch returned `target_unreachable`;
- container downloader refuses the signed storage URL because it cannot pass the safe web-open boundary.

Classification: `ENV_BLOCKED_ARTIFACT_TRANSPORT`, not asset FAIL and not Godot PASS.

## Open gates
- Human/direct `GATE-ART`.
- Exact R5 GLB Godot import/material/scale.
- Runtime collision/traversal.
- Current-tree MANIFEST refresh + fleet native delivery.
- HLOD/streaming profile.
- Target-hardware performance.

## Stop condition
Claim remains `KEEP / IN_PROGRESS`. Geometry, structural causality, portability and collision design/replay are qualified at blockout level. Native runtime, human art and performance are not. Never mark this world/claim DONE from R5.
