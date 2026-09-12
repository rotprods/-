# CLM-NACRE-WORLD-MACRO-001 — ownership + production contract

Status: IN_PROGRESS
Agent: AGENT-3D-NACRE-01
Session: 20260912T2123+0200-NACRE-01
Branch: art/world-nacre-001
Base main SHA at claim: 4c2fa044080004609ea6df45f34b2a784536507a
Current main observed: f78bfdc8bd7b2f6ab52b45d39babcc1589ab3918
Heartbeat receipt: 2026-09-12T21:28:30Z
Fleet epoch: 1
Fleet state observed: reserved
Producer ACK: https://github.com/rotprods/-/issues/7#issuecomment-5648339684
Draft PR: https://github.com/rotprods/-/pull/17
Remote Blender project: a49fc6f3-fedb-40a5-913f-10a08debb0e1
Remote Blender revision: 3
Manifest: art_source/nacre_world_macro/manifest.yaml
Generator: art_source/nacre_world_macro/build_macro.py
QA receipt: art_source/nacre_world_macro/qa-r3.yaml

## Scope key

`NACRE / WORLD_MACRO / PLANETARY_FOUNDATION`

### Included
- Canon extraction for Nacre only.
- Planet/world-scale representation contract and measurable scale-reference scene.
- Macro shell-city/environment language derived from mineral shells + cultivated archives.
- Foundational material and macro construction/load-path logic for downstream Nacre cells.
- One independent remote Blender 5.2 scene plus deterministic generator proving scale, silhouette hierarchy, material separation, structural interfaces and camera readability at blockout level.
- Nacre-only manifests, task graph, QA receipts and handoff.

### Excluded
- Runtime/gameplay scripts and scenes.
- Existing Terra portal/reliquary source.
- Every other world branch/scope.
- Final MNEMOS model/rig/animation.
- Final settlements/interiors/hero architecture beyond macro interfaces.
- Final humanoid/NPC/fauna/vehicle/equipment production.
- Final collision/LOD/HLOD/streaming implementation.
- Production-engine decision, Unreal migration or GPU performance claims.
- Shared PLAN/STATE/global MANIFEST/graph ownership.

## Collision + fleet audit

The claim was created only after a live branch audit. Umbra appeared during discovery and was abandoned without writes, proving the need for resync-before-claim. During the first Nacre wave, `main` advanced and introduced the fleet harness. Current fleet authority is `docs/FLEET_COORDINATION.md`, `ops/fleet/registry.json` and issue #7.

The fleet registry recognizes this claim as `reserved`, epoch 1, owner `AGENT-3D-NACRE-01`, branch `art/world-nacre-001`, and project `a49fc6f3-fedb-40a5-913f-10a08debb0e1`. Producer ACK `5648339684` publishes the exact owned path directory and five interface IDs. This producer does not self-promote registry status; the integrator owns the `reserved -> active` transition against the current digest.

## Authority / evidence

DOCUMENTED:
- World NACRE; Andromeda; system Mneme; faction Casas de Nácar.
- Boss target: MNEMOS, el archivo encarnado.
- Fictive stable Mneme A/B binary; mineral shells and cultivated archives; three fictive archive moons.
- Reference environment: gravity 0.26 g; area temperature 16 °C.
- Cities grow inside kilometre-scale shells; inhabitants preserve lives in pearls and trade biographies.
- Archivo de MNEMOS uses spherical archive rooms connected by bridges.
- Art language: mineral archive vaults, bounded translucent plates, thin bridges, shell friction and spatially displaced voices.
- Design risk: duplicated scenarios and uncontrolled translucent materials.
- Current verified art pipeline: `.blend` source -> GLB interchange -> Godot prototype. Godot 4.7.2 is executable prototype; Unreal 5.8 remains an unqualified candidate.

`Flu In` / `Flow In` exact method name was searched and not found. Status: `PIPELINE_METHOD_NOT_FOUND`. The executable route used is Higgsfield 3D Jutsu `bpy` / Blender 5.2, preserving `.blend`, GLB, generator and QA receipts.

UNKNOWN: planetary radius/diameter, atmosphere, hydrology, tectonics, world coordinate origin, final playable area, final triangle/texture budgets, final LOD distances and final streaming implementation.

PROPOSAL only: 1400 m shell target, 184 m archive-core diameter, archive placement, bridge dimensions and 3 m deck-to-chamber clearance. These are reversible blockout interfaces, not canon.

## Planet-scale interface

- PHYSICAL PLANET SCALE: UNKNOWN.
- PLAYABLE AUTHORED AREA: UNKNOWN.
- RENDERED REPRESENTATION: kilometre-class shell-city macro blockout.
- HERO ASSET SCALE: outside this claim; 1.8 m humans and 100 m pylons exist only as QA gauges.

## Local North Star

Deliver a recoverable Nacre planetary-foundation package recognizable without logos: kilometre-scale mineral-shell architecture containing spherical archival chambers, physically readable bridge/docking/load-path systems and shell growth history, with human scale references, bounded transparency, deterministic naming and portable GLB-compatible materials. No final-quality claim until human art and runtime gates pass.

## First 10 tasks

| ID | P | Output | Dependency | Definition of Done | Status |
|---|---|---|---|---|---|
| NACRE/MACRO/001 | P0 | Canon/evidence matrix | repo authority | Production-driving statements classified | DONE |
| NACRE/MACRO/002 | P0 | Collision-safe ownership | 001 | Claim persisted with scope/base/ownership | DONE |
| NACRE/MACRO/003 | P0 | Planet/playable/render interface | 001 | Unknown planet values not promoted to canon | DONE |
| NACRE/MACRO/004 | P0 | Coverage matrix | 001,003 | Stable IDs/tier/QA fields exist | DONE |
| NACRE/MACRO/005 | P1 | Blender macro blockout | 003 | Shell, archives, bridges, camera/lights, scale refs | DONE |
| NACRE/MACRO/006 | P1 | Material-role pass | 005 | Portable bounded material roles | DONE |
| NACRE/MACRO/007 | P1 | Manufacturing/structural pass | 005 | Bridge attachment, load paths and maintenance access mechanically legible | DONE_AT_MACRO_BLOCKOUT |
| NACRE/MACRO/008 | P1 | Visual QA pack | 005-007 | Perspective + orthographic evidence generated; human/direct art judgement recorded | REVIEW |
| NACRE/MACRO/009 | P1 | GLB + editable source delivery | 005-008 | Revision, GLB/.blend receipts + clean native delivery receipt | IN_PROGRESS |
| NACRE/MACRO/010 | P1 | Handoff/release decision | 009 | Receipts, blockers, next actions and claim status cold-recoverable | IN_PROGRESS |

## Structural Gauntlet R3

Revision 2 had a real construction defect: archive bridges were generated center-to-center and therefore penetrated archive volumes. Revision 3 replaces the bridge network with surface-to-surface geometry.

Operation `nacre-structural-bridge-fix-r3`:
- removed 22 v2 bridge/spine objects;
- rebuilt 10 archive links surface-to-surface plus main entry link;
- added 21 docking sockets;
- added 7 service rings;
- added 7 suspension/load-path tendons to the inner shell;
- added 5 shell growth strata as causal growth-history signals rather than random detail.

Operation `nacre-qa-r3-geometry-render` verified:
- 97 mesh objects + 30 curve objects / 130 total scene objects;
- 10/10 archive bridge links checked;
- exactly +3.0 m deck clearance at both chamber endpoints;
- 0 bridge penetrations;
- 0 non-unit scales;
- 0 zero-dimension mesh/curve objects;
- portable lights remain `SUN_MNEME_A` + `SUN_MNEME_B` only;
- low-resolution revision-3 preview artifact `a5c7c5699ab993db11fb4d5903fb5504`.

Revision-3 provider receipts:
- `.blend`: 2,913,059 bytes; etag `2b5398f1c4bd906874e827daad64428b`.
- GLB: 3,090,440 bytes; etag `6ccb564c4ada071aeca2270db804ba87`.

Deterministic cold-rebuild source is now versioned at `art_source/nacre_world_macro/build_macro.py`; QA is versioned at `qa-r3.yaml`.

## Open gates / blockers

- `GATE-ART`: OPEN for human/direct visual approval. Multi-view evidence exists, but render generation does not itself constitute creative-director approval.
- Godot import/instantiate/scale/material test: OPEN.
- Collision authoring/runtime traversal: OPEN.
- LOD/HLOD/streaming: OPEN pending runtime strategy/budgets.
- Performance: OPEN pending target hardware and final budget.
- Fleet native binary delivery receipt: OPEN; local recovered `.blend` + GLB must be bound to a native Godot receipt.
- Planet radius/diameter remains intentionally UNKNOWN.

## Stop condition

Claim remains `KEEP / IN_PROGRESS`. Macro structural causality is materially improved and geometry QA passes, but the claim is not DONE while human art approval, native delivery/import, collision, LOD/streaming or performance qualification remain open.
