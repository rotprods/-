# KHEPRI World Macro — recoverable handoff / X100 checkpoint

AGENT: `AGENT-KHEPRI-WMACRO-001`  
SESSION: `SESSION-20260912-KHEPRI-001`  
CLAIM: `CLM-KHEPRI-WMACRO-001`  
BRANCH: `art/world-khepri-001`  
PR: `#8` draft  
X100: **ACTIVE**  
MASTER 3D PROJECT: `040f0c45-83a7-483c-9ee7-1e31c640a587` rev `8`  
COLD PROJECT: `4c01fdbb-7093-4229-9a49-8237583280bc` rev `6`  
CLAIM STATUS: **KEEP / REVIEW**  
FAMILY STATUS: `KHP_WM_HELIOSTAT_FOOTPRINTS = SYSTEMIC_MACRO_COMPLETE`

## NORTH STAR
KHEPRI world-macro is a deterministic metre-scale foundation with stable cross-domain route/tile/export interfaces. `/EXOVANT-X100` now governs expansion: maximize credible world depth per hour through systemic families, causal state variation and procedural recombination, never random clutter or AI slop.

## CURRENT TRUTH
This claim is **not KHEPRI complete** and is not final AAAA art. It now contains a technically qualified macro foundation plus one production-grade systemic support family. Final Glass Sea architecture, PBR material library, production geology, collision, runtime LOD thresholds/HLOD, characters, props, vehicles and final hero landmarks remain separate ownership leaves.

## R8 HEAD — EXACT ARTIFACTS
- Objects: `228`
- Mesh datablocks: `22` (10 scene meshes + 12 source-only LOD meshes)
- Materials: `5`
- Route curve: `1`
- Whole-scene GLB: `577,744 B`
- GLB SHA256: `c9c698734061e481b94347c88d7c076b19c60261c8402548fb8ca1079d7d3579`
- Editable BLEND: `2,198,165 B`
- BLEND SHA256: `b2f3e2f8ff90f28a5485dc019efcfa5913def0dbbcfb5e39d883d3c469a25337`
- Persistent GLB media: `1bed7b1f-0e0a-4cd3-b61b-a62f950b4ff5`
- Persistent BLEND media: `0988f832-71ab-4c21-9c1e-ecbe3cd08bcb`
- `fleet_control.py delivery`: PASS `candidate_recovered_with_native_receipt`

## TERRAIN / ROUTE FOUNDATION
Terrain remains 6.4 km × 4.8 km local tangent authoring cell using `KHP_TERRAIN_V1`.

R6 shading/export optimization:
- flat export positions `19,200` → seam-safe custom-normal export `4,941`;
- terrain export `520,508 B` → `178,288 B`;
- whole-scene GLB `822,272 B` → `480,312 B` before X100 density;
- 9,600 terrain tris unchanged;
- custom global normal error max ~`0.0368°`;
- master/cold terrain-normal SHA `ab7b0b20e8f305b2d30504fdf44d6b233f870d960f4b9774ff87ef1504c1b856`.

Route remains deterministic terrain-conforming QA interface:
- 576 points / 575 segments;
- 7 m target clearance, audited `6.9963…7.0043 m`;
- zero below-terrain samples;
- anchor order SHADE → GLASS_SEA → CRUCIBLE → RAKHET passes containment/ordering gate.

## X100 OPTICAL FIELD FAMILY
Tool: `art_source/khepri/world_macro/expand_optical_field_x100.py`  
Contract: `KHP_OPTICAL_FIELD_X100_V1`

Implemented configuration axes:
- 4 layouts: staggered bands / aligned lattice / diagonal bands / radial fan;
- 3 densities: sparse / production / dense;
- 3 maintenance corridor patterns: dual NS / single NS / cross;
- 4 state profiles: operational / maintenance cycle / damage proxy / abandonment proxy;
- 3 scale mixes: balanced / compact bias / standard bias.

Actual configuration space: **432**. Cold pure-contract audit proves every configuration non-empty, with `44…185` placements. This is a real combinatorial system, not a declared multiplier.

Representative macrocell R7/R8:
- 107 masts + 107 panels;
- 93 operational + 14 maintenance-cycle assemblies;
- scale family: compact / standard / wide;
- 3 shared mast LOD0 meshes + 3 shared panel LOD0 meshes;
- route clearance min ~144.714 m;
- anchor clearance min ~269.916 m;
- pair spacing min ~438.462 m;
- max accepted terrain slope ~10.794°;
- mast/terrain contact error about `−7.13…+8.61 μm`;
- topology has zero degenerate faces/edges.

R7 master/cold semantic fingerprint:
`01420ed366a7f8443a084332036604c47324d50900ae2033ea4d42059440d1fa`

### State causality
Machine gate is authority:
- operational: normal tracking proxy;
- maintenance: panel stowed at 72°;
- damaged proxy: panel 3 m lower + off-axis rotation;
- abandoned proxy: mast remains, panel absent.

No random grunge is used. AI state-gallery review says all four states are visually distinct; where its abandoned interpretation conflicted with structure, machine truth overrides vision. Damage/abandonment modes are **proposal QA modes**, not canon events.

### Density QA
AI overview density gate PASS, supplemental only:
- infrastructure read: yes;
- route legible: yes;
- controlled variation: yes;
- clutter fail: no;
- floating: no;
- repetition risk: low.

Minor follow-up suggestions only: future dense districts may open wider corridor breaks and strengthen route emphasis at cluster crossings. No current blocking defect.

## X100 LOD SOURCE FAMILY
Tool: `art_source/khepri/world_macro/add_optical_lods_x100.py`  
Contract: `KHP_OPTICAL_LOD_X100_V1`

For compact/standard/wide × mast/panel:
- LOD0: 24 verts / 18 polys;
- LOD1: 16 verts / 12 polys;
- LOD2: 8 verts / 6 polys.

12 LOD1/LOD2 source meshes are retained through Blender `fake_user`, with **zero object users**. They remain editable source truth and are not instanced in the representative GLB. Script idempotence explicitly distinguishes `fake_user` from object instancing.

Master/cold LOD fingerprint:
`1c67430d580cae109fa50dfab73e6747304e87b5b3c9bba99e65fa6fe4e80101`

Runtime LOD distance thresholds and HLOD remain downstream technical-art ownership; collision remains downstream gameplay ownership.

## GODOT NATIVE R8
Engine: `Godot 4.7.2.stable.official.ed1daf0bf`

R8 exact GLB native import:
- 229 nodes;
- 219 MeshInstance3D;
- 107 masts / 107 panels;
- 3 unique mast Mesh resources / 3 unique panel Mesh resources;
- 224 stable authored asset IDs / 0 duplicates;
- terrain 4,941 verts / 4,941 normals / 9,600 tris;
- `KHP_OPTICAL_LOD_X100_V1` metadata survives;
- `configuration_count=432` survives;
- LOD manifest metadata survives.

This proves import/resource sharing and metadata integrity, **not target-hardware performance**.

## BINARY DELIVERY
Technical transport blocker is closed for the current head:
- exact R8 bytes recovered and SHA-bound;
- persistent project media exists;
- Godot native import passes;
- fleet delivery passes.

Remaining corporate Git LFS archival is a storage-policy follow-up, not an asset-loss or execution blocker. Do not push `.blend`/`.glb` as ordinary Git blobs; `.gitattributes` marks them binary/LFS.

## VISUAL / HUMAN GATE
Machine + AI density/scale evidence exists. `HUMAN_GATE_ART` remains the only blocking review gate in this claim. Do not promote blockout/support materials to final AAAA art without explicit human/pixel review.

## CI / FINOPS
Last exact auto-Gauntlet green before cost quarantine: head `8022197e…`, run `34722654514` SUCCESS. Current `main` changed GitHub Actions to `workflow_dispatch` only for cost control. Therefore new branch/document waves require local combined checkout + `project_control` + tests + `fleet guard-git`; do not spend Actions unless a meaningful promotion gate requires it.

## CANON BOUNDARY / RECOVERY
- KHEPRI: Sahra / Andrómeda / Sínodo de Bronce / 0.63 g / 71 °C reference authored area / solar-glass desert + heliostats / RA-KHET.
- Proposed radius 5,224 km remains reversible ADR, not canon.
- Canonical named surface regions recovered: **Ciudad de los Toldos**, **Mar de Cristal**, **Crisol de RAKHET**. Exact map/boundaries remain unknown.
- Canonical biota recovered: **Escarabajo heliostato**, **Zorro de vidrio**, **Serpiente de cable**, **Liquen de prisma**. These unblock future ecology ownership; the complete trophic web, distributions, rigs and gameplay remain unclaimed/proposal territory.
- Canonical local vehicle recovered: **Helioperegrino**. Broader transport hierarchy remains unknown/unclaimed.
- Named NPC/adversary anchors are documented in `WORLD_BIBLE.md`; final character production remains unclaimed.
- Canon recovery receipt: `production/worlds/khepri/world_macro/receipts/R8_X100_CANON_RECOVERY.json`.
- X100 damage/abandonment states are systemic proposal modes, not story canon.

## NEXT EXECUTION
1. RESYNC coverage/fleet and preserve generated MANIFEST through the serialized integrator transaction; no Actions dispatch for docs-only reconciliation.
2. Highest systemic multiplier remains `GLOBAL_KHEPRI/materials_surface_library`.
3. Reservation proposal `CLM-KHEPRI-MATERIALS-001` has passed offline fleet CAS/collision validation but is **not yet published in main**. Until `reserved → owner ACK → active` is observable, material work is limited to pre-claim scratch contracts; no repo/provider/material mutation.
4. Canon recovery also changes ecology/vehicle coverage from false `BLOCKED` to `TODO/UNCLAIMED`; future agents may claim those domains, but this macro agent does not own them.
5. Do **not** broaden `CLM-KHEPRI-WMACRO-001` into final materials/architecture/ecology/characters/collision ownership.

CLAIM STATUS: **KEEP / REVIEW**  
FAMILY STATUS: **SYSTEMIC_MACRO_COMPLETE**
