# CLM-NACRE-WORLD-MACRO-001 — ownership + production contract

Status: IN_PROGRESS
Agent: AGENT-3D-NACRE-01
Branch: art/world-nacre-001
Scope: `NACRE / WORLD_MACRO / PLANETARY_FOUNDATION`
Fleet epoch: 1
Fleet state: active
Producer ACK: https://github.com/rotprods/-/issues/7#issuecomment-5648339684
R4 follow-up: https://github.com/rotprods/-/issues/7#issuecomment-5648897202
Draft PR: https://github.com/rotprods/-/pull/17
Primary Blender: a49fc6f3-fedb-40a5-913f-10a08debb0e1 @ revision 5
Clean replay: 4750e054-b063-4ab8-afc9-214462f36128 @ revision 2
Latest main observed: 26ae20f5d1b47d1efa0d54b20124ed93cbc0b43e

## Included
- Nacre canon/evidence extraction for this macro cell.
- Physical-planet / playable-area / rendered-representation interface without inventing planetary radius.
- Kilometre-class mineral shell-city blockout.
- Seven spherical archive chambers, bridge/docking/load-path network and bounded translucent accents.
- Foundational materials, shell-growth history and scale gauges.
- Reproducible Blender macro generator + reproducible static traversal collision pass.
- Nacre-only manifests, QA receipts and cold handoff.

## Excluded
- Runtime/gameplay source edits.
- Other worlds.
- Final MNEMOS boss model/rig/animation.
- Final settlements/interiors/hero architecture outside this macro interface.
- Final NPC/fauna/vehicles/equipment.
- Planetary radius/diameter or other unapproved global physical canon.
- Global engine decision / Unreal migration / GPU claims.
- Shared STATE/PLAN/global MANIFEST/graph ownership.

## Canon / evidence
DOCUMENTED:
- NACRE / Andromeda / Mneme / Casas de Nácar / MNEMOS target.
- Reference environment 0.26 g / 16 °C.
- Cities grow inside kilometre-scale mineral shells; biographies are stored/traded in pearls.
- Archivo de MNEMOS uses spherical archive rooms connected by bridges.
- Current verified exchange path is Blender `.blend` → GLB → Godot 4.7.2 prototype.

UNKNOWN remains UNKNOWN:
- planetary radius/diameter;
- atmosphere, hydrology, tectonics;
- final playable area;
- final poly/texture budgets;
- final LOD distances / HLOD / streaming implementation.

PROPOSAL only:
- ~1400 m shell target;
- 184 m archive core diameter;
- exact archive placement, bridge widths and ~3 m bridge/chamber surface clearance.

Exact “Flu In / Flow In” repo method remains `PIPELINE_METHOD_NOT_FOUND`.

## Fleet / ownership truth
The fleet registry generation 8 promotes this claim to `active`, epoch 1, owner `AGENT-3D-NACRE-01`, and records the five stable interface IDs:
- `NACRE-MACRO-SHELL-001`
- `NACRE-MACRO-LINING-001`
- `NACRE-ARCHIVE-NET-001`
- `NACRE-BRIDGE-NET-001`
- `NACRE-SCALE-REF-001`

Producer does not own the global registry; later transitions remain integrator transactions.

## North Star
Deliver a recoverable, causally constructed and reproducible Nacre macro-foundation whose identity is legible without logos: mineral shell, pearl lining, archive spheres, surface-connected bridges, docking/maintenance/load paths, growth history, bounded transparency and explicit scale. Human art approval and native runtime qualification remain separate gates.

## Task state
| ID | P | Output | Status |
|---|---|---|---|
| NACRE/MACRO/001 | P0 | Canon/evidence matrix | DONE |
| NACRE/MACRO/002 | P0 | Fleet ownership/ACK | DONE — ACTIVE |
| NACRE/MACRO/003 | P0 | Planet/playable/render interface | DONE |
| NACRE/MACRO/004 | P0 | Coverage/interface IDs | DONE |
| NACRE/MACRO/005 | P1 | Reproducible Blender macro blockout | DONE |
| NACRE/MACRO/006 | P1 | Portable material-role foundation | DONE |
| NACRE/MACRO/007 | P1 | Manufacturing/structural causality | DONE_AT_BLOCKOUT |
| NACRE/MACRO/008 | P1 | Visual QA evidence + human review | REVIEW — HUMAN GATE OPEN |
| NACRE/MACRO/009 | P1 | Source/export + collision + native delivery | COLLISION DESIGN PASS / NATIVE ENV_BLOCKED |
| NACRE/MACRO/010 | P1 | Handoff/release decision | IN_PROGRESS |

## R4 reproducibility checkpoint
Primary revision 4 and independent clean replay share exact macro semantic SHA256:

`48742ba2dc253a626fb807799a55e2c83f2e87f437cf761b66522bac7ba88787`

R4 blockout QA:
- 130 objects; 97 meshes; 30 curves;
- 10/10 archive bridges checked;
- endpoint clearance 2.9999–3.0 m;
- 0 bridge penetrations;
- 0 non-unit scales;
- 0 zero-dimension mesh/curve objects;
- only portable SUN_MNEME_A/B lighting.

## R5 collision checkpoint
Godot importer contract used: collision proxy node names end in `-colonly`.

Primary revision 5 adds exactly 12 simple static traversal proxies:
- 10 archive bridge deck proxies;
- 1 entry bridge proxy;
- 1 entry platform proxy.

Primary and clean replay collision digest match exactly:

`af7b2d53c2700fb841205b776906150b3429a809107902d56799e6b92309adf1`

QA:
- 12/12 proxy names present in exported GLB log;
- 0 proxy containment violations;
- collision pass is independently reproducible.

Explicit collision waivers:
- archive chamber hulls must be interior-aware shells, not solid convex blockers;
- global shell collision must later be regional/tiled, never a monolithic collider;
- service rings are not yet declared traversable.

## LOD policy
For this imported glTF blockout tier, use Godot editor-import automatic mesh LOD by default. Manual artist LOD chains and HLOD are deferred until runtime camera-distance/streaming profiling demonstrates a concrete need.

## Native import blocker
Exact Godot import has not occurred. Artifact transport is independently reproduced as blocked:
- local executable container has no general DNS egress;
- fresh provider-signed R5 URL cannot pass the safe web/download boundary;
- live browser/direct fetch surfaces also fail signed storage retrieval (`InvalidArgument` / `target_unreachable`).

Classification: `ENV_BLOCKED_ARTIFACT_TRANSPORT`, not asset FAIL and not runtime PASS.

## Global continuity
Latest main observed is `26ae20f5d1b47d1efa0d54b20124ed93cbc0b43e`; branch resync is required before integration. The global `MANIFEST.json` is integrator-owned. The old branch projection is stale after R5 and must not be treated as a valid receipt; a clean delivery checkout must inherit current-main MANIFEST and run `python3 tools/project_control.py refresh` before fleet guard/delivery.

## Open gates
- Human/direct `GATE-ART`.
- Exact R5 GLB Godot import/material/scale.
- Runtime collision/traversal.
- HLOD/streaming profile.
- Target-hardware performance.
- Current-main resync + exact MANIFEST refresh + fleet native delivery receipt.

## Stop condition
Claim remains `KEEP / IN_PROGRESS`. Macro geometry, structural causality, portability and reproducible collision design are qualified at blockout level. Human art and exact native runtime/performance are not. Never mark world/claim DONE from this checkpoint.
