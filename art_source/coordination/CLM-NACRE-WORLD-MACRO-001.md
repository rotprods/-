# CLM-NACRE-WORLD-MACRO-001 — ownership + production contract

Status: IN_PROGRESS
Agent: AGENT-3D-NACRE-01
Session: 20260912T2123+0200-NACRE-01
Branch: art/world-nacre-001
Base main SHA at claim: 4c2fa044080004609ea6df45f34b2a784536507a
Last main merged without force: 70fda70cd2120d38fba94e6a66e554e564c6c471
Fleet epoch: 1
Fleet state observed: reserved
Producer ACK: https://github.com/rotprods/-/issues/7#issuecomment-5648339684
Draft PR: https://github.com/rotprods/-/pull/17
Remote Blender project: a49fc6f3-fedb-40a5-913f-10a08debb0e1
Remote Blender revision: 4
Clean replay project: 4750e054-b063-4ab8-afc9-214462f36128 @ revision 1
Manifest: art_source/nacre_world_macro/manifest.yaml
Generator: art_source/nacre_world_macro/build_macro.py
Current QA: art_source/nacre_world_macro/qa-r4.yaml

## Scope key

`NACRE / WORLD_MACRO / PLANETARY_FOUNDATION`

### Included
- Nacre canon/evidence extraction for this macro cell.
- Physical-planet / playable-area / rendered-representation interface without inventing radius.
- Kilometre-class shell-city macro blockout.
- Spherical archive chamber network, bridge/docking interfaces and macro load paths.
- Foundational material roles, shell-growth history and human/100m scale gauges.
- Deterministic Blender 5.2 generator, remote source/export, QA receipts and cold handoff.

### Excluded
- Runtime/gameplay source edits.
- Other worlds.
- Final MNEMOS boss, final settlements/interiors/hero architecture, final NPC/fauna/vehicles/equipment.
- Final collision/LOD/HLOD/streaming implementation.
- Global engine decision / Unreal migration / GPU performance claims.
- Shared PLAN/STATE/global MANIFEST/graph ownership.

## Authority / evidence

DOCUMENTED from repo:
- NACRE; Andromeda; Mneme; Casas de Nácar; MNEMOS target.
- Mneme A/B fictive binary; mineral shells + cultivated archives; reference 0.26 g / 16 °C.
- Cities grow inside kilometre-scale shells; biographies are preserved/traded in pearls.
- Archivo de MNEMOS uses spherical archive rooms connected by bridges.
- Art risk: uncontrolled translucent material versions and duplicated scenarios.
- Verified art path: `.blend` source -> GLB -> Godot 4.7.2 prototype. Unreal 5.8 remains unqualified production candidate.

UNKNOWN remains UNKNOWN: planetary radius/diameter, atmosphere, hydrology, tectonics, global coordinate origin, final playable area, final triangle/texture budgets, LOD distances and final streaming implementation.

PROPOSAL only: shell target ~1400 m, archive core 184 m, archive placements, bridge widths and 3 m deck/chamber interface clearance.

`Flu In` / `Flow In` exact repo method was not found: `PIPELINE_METHOD_NOT_FOUND`.

## Fleet / collision state

The claim was created after a live branch audit; an Umbra race was detected and abandoned without writes. The fleet registry recognizes this Nacre claim as `reserved`, epoch 1. Producer ACK `5648339684` publishes owner, branch, project, exact Nacre directory and five stable interface IDs. No producer-side mutation of the global registry has been performed; `reserved -> active` remains an integrator transaction against the current registry digest.

This branch was resynced against `main@70fda70c...` via a normal two-parent merge commit and non-force ref update. Post-resync compare showed `behind_by: 0` and only owned Nacre files differed from main.

## Local North Star

Deliver a recoverable, semantically reproducible Nacre macro-foundation whose identity is readable without logos: kilometre-scale mineral shell, archive spheres, surface-connected bridges, docking/maintenance/load paths, shell growth history, bounded transparency and explicit scale gauges. Human art approval and native runtime gates remain separate.

## Task state

| ID | P | Output | Status |
|---|---|---|---|
| NACRE/MACRO/001 | P0 | Canon/evidence matrix | DONE |
| NACRE/MACRO/002 | P0 | Collision-safe ownership/fleet ACK | DONE_PRODUCER_SIDE |
| NACRE/MACRO/003 | P0 | Planet/playable/render interface | DONE |
| NACRE/MACRO/004 | P0 | Coverage/interface IDs | DONE |
| NACRE/MACRO/005 | P1 | Blender macro blockout | DONE |
| NACRE/MACRO/006 | P1 | Portable material-role foundation | DONE |
| NACRE/MACRO/007 | P1 | Macro manufacturing/structural causality | DONE_AT_BLOCKOUT |
| NACRE/MACRO/008 | P1 | Visual QA evidence + human review | REVIEW — human GATE-ART OPEN |
| NACRE/MACRO/009 | P1 | Reproducible source/export + native delivery | ENV_BLOCKED at native transport/import |
| NACRE/MACRO/010 | P1 | Final handoff / claim release decision | IN_PROGRESS |

## Gauntlet history

### R2 -> R3 structural correction
R2 bridge decks were center-to-center and intersected archive volumes. R3 replaced them with surface-to-surface decks/spines and added 21 docking sockets, 7 service rings, 7 suspension/load-path tendons and 5 growth strata. R3 QA checked 10/10 links: ~3 m endpoint clearance, 0 penetrations, 0 non-unit scales, 0 degenerate dimensions.

### Cold-replay attack and generator bug
A fresh Blender project exposed a real versioned-generator bug: Blender 5.2 rejects a `Collection` object in `bpy_prop_collection.__contains__`. Probe `nacre-r3-generator-api-probe` returned `TypeError`. `build_macro.py` was fixed to compare child collection names (`6be51b785b53c38e071461212254a81e601c8518`).

The fixed generator rebuilt a clean project to 97 meshes / 30 curves / 2 SUN lights. Initial semantic comparison against historical R3 still differed because R3 inherited older shell resolutions/ribs/belts/plate naming that the generator had never encoded explicitly.

### R4 reproducibility canonicalization
Rather than preserve implicit historical drift, the reversible macro blockout was rebuilt in the primary project from the corrected versioned generator. Primary revision 4 and independent clean replay now share exact semantic scene digest:

`48742ba2dc253a626fb807799a55e2c83f2e87f437cf761b66522bac7ba88787`

R4 QA:
- 130 total objects;
- 97 meshes + 30 curves;
- 10/10 bridge links checked;
- endpoint clearance 2.9999–3.0 m;
- 0 bridge penetrations;
- 0 non-unit scales;
- 0 zero-dimension mesh/curve objects;
- only `SUN_MNEME_A/B` portable lights;
- semantic cold-replay match = PASS.

R4 remote receipts:
- `.blend`: 3,500,059 bytes, etag `a365ae84492f4142d949c1033636b092`.
- GLB: 3,828,832 bytes, etag `0b6dee01664cb91aae1a4b332e8ae163`.
- hero preview: artifact `24642ce8001df31f7c50875e79c07c9d` (640×360).

## Native delivery attempt

Attempted the next required gate rather than assuming it:
- isolated execution container could not resolve `github.com`, so clean checkout could not be cloned there;
- the short-lived provider binary could not cross the available safe-download boundary into that container;
- therefore no Godot import or `fleet_control.py delivery` was executed.

Classification: `ENV_BLOCKED`, not asset FAIL and not runtime PASS.

## Open gates / blockers

- Human/direct `GATE-ART`: OPEN. Render evidence is not approval.
- Fleet integrator transition `reserved -> active`: OPEN outside producer ownership.
- Godot exact-GLB import/material/scale: ENV_BLOCKED in this execution surface.
- Collision/traversal: OPEN.
- LOD/HLOD/streaming: OPEN.
- Target-hardware performance: OPEN.
- Fleet native binary delivery: ENV_BLOCKED until exact binaries and repo checkout coexist on an executable host.
- Planet radius/diameter remains intentionally UNKNOWN.

## Stop condition

Claim remains `KEEP / IN_PROGRESS`. Geometry, portability and semantic reproducibility are qualified at blockout level; human art, native runtime, collision, LOD/streaming and performance are not. Do not merge/mark DONE as a completed world.
