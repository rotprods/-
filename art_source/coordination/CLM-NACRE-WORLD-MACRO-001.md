# CLM-NACRE-WORLD-MACRO-001 — ownership + production contract

Status: IN_PROGRESS
Agent: AGENT-3D-NACRE-01
Session: 20260912T2123+0200-NACRE-01
Branch: art/world-nacre-001
Base main SHA: 4c2fa044080004609ea6df45f34b2a784536507a
Heartbeat: 2026-09-12T21:59:00+02:00
Remote Blender project: a49fc6f3-fedb-40a5-913f-10a08debb0e1
Remote Blender revision: 2
Manifest: art_source/nacre_world_macro/manifest.yaml

## Scope key

`NACRE / WORLD_MACRO / PLANETARY_FOUNDATION`

### Included
- Canon extraction for Nacre only.
- Planet/world-scale representation contract and measurable scale-reference scene.
- Macro shell-city/environment language derived from the canon of mineral shells + cultivated archives.
- Foundational material roles and construction logic for later Nacre kits.
- One independent remote Blender 5.2 scene that proves scale, silhouette, material separation and camera readability at blockout level.
- Nacre-only manifests, task graph, QA receipts and handoff.

### Excluded
- Runtime/gameplay scripts and scenes.
- Existing Terra portal/reliquary source.
- Ares IX, Terra, Khepri, Pelagos, Umbra and Vanta branches/scopes.
- Final MNEMOS boss model/rig/animation.
- Final humanoid/NPC production.
- Final vehicle production.
- Production-engine decision, Unreal migration or GPU performance claims.
- Silent edits to shared PLAN/STATE/HANDOFF on main.

## Collision audit

Observed active art branches before claim: `art/ares-ix-world-001`, `art/ares-ix-world-agent-02`, `art/terra-reliquary-kit-001`, `art/world-khepri-001`, `art/world-pelagos-thalassa-001`, `art/world-umbra-001`, `art/world-vanta-001`. No Nacre branch/PR/claim was observed immediately before `art/world-nacre-001` was created. This file is the persistent ownership signal for this branch.

A race was observed during discovery: Umbra appeared after the first branch audit and before claim creation. Umbra was therefore abandoned without writes. This is evidence that every subsequent wave must resync before claiming a new cell.

## Authority / evidence

CANON/DOCUMENTED from repository:
- World: NACRE.
- Galaxy: Andromeda.
- System: Mneme.
- Faction: Casas de Nácar.
- Boss target: MNEMOS, el archivo encarnado.
- Celestial premise: fictive stable Mneme A/B binary; world of mineral shells and cultivated archives; colonies on a larger moon; three fictive archive moons with designed orbital routes.
- Reference environment: gravity 0.26 g; area temperature 16 °C.
- Lore premise: cities grow inside kilometre-scale shells; inhabitants store whole lives in pearls and trade biographies.
- Named places include Casa de las Copias, Canteras de Concha and Archivo de MNEMOS; the latter is described as spherical rooms connected by bridges.
- Art language: mineral archive vaults, bounded translucent plates, thin bridges, shell friction and spatially displaced voices.
- Design risk: duplicated scenarios and translucent materials; active versions should be bounded and states prefabricated.
- Current art pipeline: editable `.blend` source -> GLB interchange -> Godot prototype; Godot 4.7.2 is executable prototype, Unreal 5.8 remains an unqualified production candidate.

`Flu In` / `Flow In` exact method name was searched and not found in the repository. Status: `PIPELINE_METHOD_NOT_FOUND`. The verified executable route used here is Higgsfield 3D Jutsu `bpy` on Blender 5.2, preserving `.blend` + GLB receipts.

UNKNOWN until explicitly approved or discovered: planetary radius/diameter, atmosphere, hydrology, tectonics, world coordinate origin, final playable-area dimensions, final poly/texture budgets, final LOD distances, final engine streaming implementation.

PROPOSAL parameters used in blockout remain isolated and reversible; they are not canon. Revision 2 currently uses a shell-city blockout span target of 1400 m and an archive-core diameter of 184 m solely to communicate scale.

## Planet-scale interface

- PHYSICAL PLANET SCALE: UNKNOWN; no radius/diameter invented.
- PLAYABLE AUTHORED AREA: UNKNOWN; no production acreage invented.
- RENDERED BLOCKOUT REPRESENTATION: revision-2 shell-city scene, measured bounds 1394.44 × 1050.02 × 845.57 m.
- HERO ASSET SCALE: not claimed by this scope; human 1.8 m proxies and 100 m pylons exist only as scale gauges.

## Local North Star

Deliver a recoverable Nacre planetary-foundation package that makes the world recognizable without logos: kilometre-scale mineral-shell architecture containing spherical archival chambers and bridge networks, with physically coherent massing, human scale references, bounded translucent-material intent, deterministic naming and a portable GLB-compatible material set. No final-quality claim until art review and runtime integration gates pass.

## First 10 tasks

| ID | P | Output | Dependency | Definition of Done | Status |
|---|---|---|---|---|---|
| NACRE/MACRO/001 | P0 | Canon/evidence matrix | repo authority | Every production-driving statement tagged CANON/DOCUMENTED/UNKNOWN/PROPOSAL | DONE |
| NACRE/MACRO/002 | P0 | Collision-safe ownership + branch contract | 001 | Claim persisted, scope/includes/excludes/base SHA recorded | DONE |
| NACRE/MACRO/003 | P0 | Nacre world-scale interface | 001 | Planet/playable/rendered scales separated; unknowns not invented as canon | DONE |
| NACRE/MACRO/004 | P0 | Master asset/coverage matrix for this claim | 001,003 | IDs, tier, dimensions, dependencies, paths, QA fields exist | DONE |
| NACRE/MACRO/005 | P1 | Remote Blender blockout v1 | 003 | Editable scene at metre scale with shell-city macroform, archive spheres, bridges, camera/lights and human references | DONE |
| NACRE/MACRO/006 | P1 | Material-role pass | 005 | Portable Principled roles separate nacre mineral, structural dark metal, archive pearl, bridge/service surfaces; no uncontrolled transparency | DONE |
| NACRE/MACRO/007 | P1 | Manufacturing/structural plausibility pass | 005 | Load paths, supports, access/maintenance logic and bridge attachment are visually legible | IN_PROGRESS |
| NACRE/MACRO/008 | P1 | Visual QA pack | 005-007 | Perspective + orthographic/scale views rendered and inspected; floating/intersection/framing defects logged/fixed | BLOCKED |
| NACRE/MACRO/009 | P1 | GLB + editable source receipts | 005-008 | Exact remote revision recorded; GLB and .blend resolvable; object/material counts documented | IN_PROGRESS |
| NACRE/MACRO/010 | P1 | Handoff + next cell proposal | 009 | DONE/IN_PROGRESS/BLOCKED/receipts/next 3 actions + claim status persisted | IN_PROGRESS |

## Execution receipts — checkpoint R2

- Blender project: `a49fc6f3-fedb-40a5-913f-10a08debb0e1`.
- Successful build: operation `nacre-macro-build-v1c`, revision 1.
- Portability fix: operation `nacre-portability-fix-r2`, revision 2.
- Final geometry query: operation `nacre-final-qa-r2` against revision 2.
- `.blend` revision 2: 2,343,988 bytes; etag `49df1eee4bf980b1da063676015d5835`.
- GLB revision 2: 2,253,168 bytes; etag `9ab4c7474e11d771957c94da79917795`.
- Revision-2 scene: 69 mesh objects, 18 curve objects, 12,830 raw vertices, ~25,092 raw pre-modifier triangles, eight material roles, two portable SUN lights.
- Bounds: 1394.44 × 1050.02 × 845.57 m.
- Transform QA: zero non-unit object scales observed; zero zero-dimension mesh/curve objects observed.
- Revision-1 QA render exists: `nacre_macro_r1_qa.png`, 960 × 540, artifact `1e28cb00be72db164a61b00ae4c1cdf9`.
- Export defect found and fixed: unsupported AREA light emitted a GLB warning in revision 1; removed in revision 2, leaving only portable SUN lights.
- Two failed build attempts committed no scene revision: missing World datablock, then Blender-5.2 collection API mismatch. Both were corrected before successful build.

## Open gates / blockers

- `GATE-ART`: OPEN. The render artifact was generated, but this client did not provide a visually inspectable artifact payload to the agent. No visual PASS is claimed.
- Godot import/instantiate/scale/material/collision test: OPEN.
- Collision authoring: OPEN.
- LOD/HLOD/streaming policy: OPEN pending runtime budgets/engine decision.
- Performance budget: OPEN; target hardware and final budgets are not canonically fixed.
- Planet radius/diameter: UNKNOWN and intentionally not invented.

## Stop conditions

Claim status remains `KEEP / IN_PROGRESS`. Do not mark this claim DONE while P1 structural plausibility, visual inspection, runtime import/collision/LOD/performance gates, or any other applicable stop condition remains open. Never promote proposal dimensions to planetary canon without an explicit decision.
