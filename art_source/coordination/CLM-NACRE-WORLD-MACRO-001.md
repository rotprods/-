# CLM-NACRE-WORLD-MACRO-001 — ownership + production contract

Status: CLAIMED
Agent: AGENT-3D-NACRE-01
Session: 20260912T2123+0200-NACRE-01
Branch: art/world-nacre-001
Base main SHA: 4c2fa044080004609ea6df45f34b2a784536507a
Heartbeat: 2026-09-12T21:31:00+02:00

## Scope key

`NACRE / WORLD_MACRO / PLANETARY_FOUNDATION`

### Included
- Canon extraction for Nacre only.
- Planet/world-scale representation contract and measurable scale-reference scene.
- Macro shell-city/environment language derived from the canon of mineral shells + cultivated archives.
- Foundational material roles and construction logic for later Nacre kits.
- One independent remote Blender 5.2 scene that proves scale, silhouette, material separation and camera readability.
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

Observed active art branches before claim: `art/ares-ix-world-001`, `art/ares-ix-world-agent-02`, `art/terra-reliquary-kit-001`, `art/world-khepri-001`, `art/world-pelagos-thalassa-001`, `art/world-umbra-001`, `art/world-vanta-001`. No Nacre branch/PR/claim was observed immediately before this branch was created. This file is the persistent ownership signal for this branch.

## Authority / evidence

CANON/DOCUMENTED from repository:
- World: NACRE.
- Galaxy: Andromeda.
- System: Mneme.
- Faction: Casas de Nácar.
- Boss target: MNEMOS, el archivo encarnado.
- Celestial premise: fictive stable Mneme A/B binary; world of mineral shells and cultivated archives; colonies on a larger moon; three fictive archive moons with designed orbital routes.
- Lore premise: cities grow inside kilometre-scale shells; inhabitants store whole lives in pearls and trade biographies.
- Named places include Canteras de Concha and Archivo de MNEMOS; the latter is described as spherical rooms connected by bridges.
- Design risk: duplicated scenarios and translucent materials; active versions should be bounded and states prefabricated.
- Current art pipeline: editable `.blend` source -> GLB interchange -> Godot prototype; Godot 4.7.2 is executable prototype, Unreal 5.8 remains an unqualified production candidate.

UNKNOWN until explicitly approved or discovered: planetary radius/diameter, exact gravity, atmosphere, hydrology, tectonics, world coordinate origin, final playable-area dimensions, final poly/texture budgets, final LOD distances, final engine streaming implementation.

PROPOSAL parameters used in blockout must remain isolated and reversible; they are not canon.

## Local North Star

Deliver a recoverable Nacre planetary-foundation package that makes the world recognizable without logos: kilometre-scale mineral-shell architecture containing spherical archival chambers and bridge networks, with physically coherent massing, human scale references, bounded translucent material use, deterministic naming and a portable GLB-compatible material set. No final-quality claim until art review and runtime integration gates pass.

## First 10 tasks

| ID | P | Output | Dependency | Definition of Done | Status |
|---|---|---|---|---|---|
| NACRE/MACRO/001 | P0 | Canon/evidence matrix | repo authority | Every production-driving statement tagged CANON/DOCUMENTED/UNKNOWN/PROPOSAL | IN_PROGRESS |
| NACRE/MACRO/002 | P0 | Collision-safe ownership + branch contract | 001 | Claim persisted, scope/includes/excludes/base SHA recorded | DONE |
| NACRE/MACRO/003 | P0 | Nacre world-scale interface | 001 | Planet/playable/rendered scales separated; unknowns not invented as canon | TODO |
| NACRE/MACRO/004 | P0 | Master asset/coverage matrix for this claim | 001,003 | IDs, tier, dimensions, dependencies, paths, QA fields exist | TODO |
| NACRE/MACRO/005 | P1 | Remote Blender blockout v1 | 003 | Editable scene at metre scale with shell-city macroform, archive spheres, bridges, camera/lights and human references | TODO |
| NACRE/MACRO/006 | P1 | Material-role pass | 005 | Portable Principled materials separate nacre mineral, structural dark metal, archive pearl, bridge/service surfaces; no uncontrolled transparency | TODO |
| NACRE/MACRO/007 | P1 | Manufacturing/structural plausibility pass | 005 | Load paths, supports, access/maintenance logic and bridge attachment are visually legible | TODO |
| NACRE/MACRO/008 | P1 | Visual QA pack | 005-007 | Perspective + orthographic/scale views rendered and inspected; floating/intersection/framing defects logged/fixed | TODO |
| NACRE/MACRO/009 | P1 | GLB + editable source receipts | 005-008 | Exact remote revision recorded; GLB and .blend resolvable; object/material counts documented | TODO |
| NACRE/MACRO/010 | P1 | Handoff + next cell proposal | 009 | DONE/IN_PROGRESS/BLOCKED/receipts/next 3 actions + claim status persisted | TODO |

## Stop conditions

Do not mark this claim DONE while P0/P1 items remain, Blender scene has no visual inspection, GLB/.blend receipts are missing, or any UNKNOWN has been promoted to canon without approval.
