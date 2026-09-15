# NACRE AAA LOOKDEV / HERO — cold handoff

AGENT: AGENT-NACRE-LOOKDEV-01  
CLAIM: CLM-NACRE-LOOKDEV-HERO-001  
BRANCH: art/nacre-lookdev-hero-001  
BASE MAIN AT CLAIM: 8c01136aa14f89e177ff1216d1993d62ea963ad3  
FLEET ACTIVE MAIN: 2db9e3baf6ea5daa0440a11bdb26728a8a5f9d20  
X100 OPPORTUNITY: NACRE-AAA-LOOKDEV-TO-MESH / Wave 001 rank #1  
STATUS: ACTIVE / MANUAL_REFERENCE_BUILD_R2_TECHNICALLY_QUALIFIED / HUMAN_GATE_ART_OPEN  
FLEET ISSUE: #7 comment 5662212641  
FLEET INTEGRATION: PR #43 merged

## North Star

Prove one AAA-quality Nacre hero-family pipeline from approved visual truth to cleaned game-ready geometry, starting with `NACRE-LOOK-ARCHIVE-CHAMBER-001`. Visual beauty alone is insufficient: identity, material causality, construction/growth logic, topology, engine transport and same-camera visual regression all have explicit gates.

## DONE

### Governance / ownership
- X100 V2 + Global Density Director is canonical on main.
- Wave 001 selected `NACRE-AAA-LOOKDEV-TO-MESH` as portfolio rank #1.
- Sibling preflight found only Nacre macro/foundation owner; lookdev-hero remained disjoint.
- Fleet reserve→ACK CAS was first validated offline, then published by separate integrator PR #43 with `fleet_control validate`, Graphify rebuild and `project_control refresh/check` PASS.
- Claim is now canonical `ACTIVE`, epoch 1. Existing `CLM-NACRE-WORLD-MACRO-001` remains untouched.

### Look-lock candidate pack
- Canon/negative contract persisted in `LOOKDEV_TO_MESH_CONTRACT.md` and `TARGET_PACK_SPEC.json`.
- TARGET_A job: `165810de-cdb8-40ee-8340-c13cd3eddcf0`; requested Nano Banana Pro, effective metadata `nano_banana_2`.
- Reusable identity element: `fa973079-15b8-4648-a602-e1adb4e96655` / `nacre-archive-chamber-a`.
- TARGET_B/C/D generated from that exact identity element:
  - B `3b988b0b-89c0-411c-bb12-294a8ab09b09`;
  - C `3db84e38-bcb6-4ed4-bf2b-59fe0de706e6`;
  - D `7d6e08d7-c9d0-4c25-bc07-0e10f05c28b0`.
- B/C/D requested `nano_banana_2`; effective job metadata reports `nano_banana_flash`. Provider fallback is retained in evidence.
- `TARGET_PACK_RECEIPT.json` persists job IDs, URLs, effective models and gates.
- `HUMAN_GATE_ART` remains OPEN. A-D are multiview candidates, not approved visual truth.
- E/F remain intentionally deferred until the identity is accepted.

### Image-to-polygon truth
- Live catalog verifies Tripo H3.1 multiview, Meshy multi-image and Hunyuan3D v3 image-to-3D model availability.
- The connected tool surface still exposes no verified generic submit action for those models.
- Therefore status is `ENV_BLOCKED_3D_SUBMIT_SURFACE`; no Tripo/Meshy/Hunyuan output is fabricated.

### Manual reference fallback — R2
- Isolated primary 3D Jutsu project: `732aba1b-8490-4ee5-94f3-3caa69590f82`.
- Build class: **MANUAL_REFERENCE_BUILD**; never relabel as image-to-3D output.
- Primary revision 2:
  - 76 objects / 46 meshes / 23 curves;
  - hollow 48 m proposal chamber, nominal 1.6 m wall;
  - 3/3 real bored dock openings;
  - 3 load rings + 3 inner lips + 12 load-transfer ribs;
  - exactly 2 service hatches;
  - 11 causal mineral-growth strata;
  - 6 repair patches;
  - 5 bounded biological traces;
  - exact 1.800 m scale witness;
  - 0.000 m shell-floor gap;
  - zero non-unit mesh scales and zero degenerate meshes;
  - technical QA PASS.
- Primary `.blend`: 3,108,359 B / etag `2d526ee062985291a79ef85b83728a0c`.
- Primary GLB: 2,206,408 B / etag `afabe1487071bf4bc9777917a29054d0`.
- Primary semantic SHA256: `704ab6cff6fff63aff966db7f959260f9e312dedf7d56b5c50e24aa319144036` over 69 productive objects.
- Four 640×640 review renders A/B/C/D are file-backed; artifact IDs are in `MANUAL_REFERENCE_BUILD_R2.json`.

### Cold replay / negative evidence
- Independent project: `39d31b99-3975-4f3e-9281-6f8a3e60415f`.
- Initial replay reproduced 68/69 object fingerprints but shell fingerprint differed because Blender 5.2 booleans appended one unused trailing `NULL` material slot.
- Generator was corrected with `normalize_shell_material_slots` instead of hiding the mismatch.
- Qualified cold revision 2 `.blend`: 3,108,359 B / etag `51b74dc24b41627d49f245d532aae565`.
- Qualified cold GLB: 2,206,408 B / etag `bf3654dfeda333b72b46b8cdc387343f`.
- Cold semantic SHA256 now matches primary exactly: `704ab6cff6fff63aff966db7f959260f9e312dedf7d56b5c50e24aa319144036`.
- Byte identity is not claimed; semantic scene identity is the blockout/reference criterion.
- Source generator: `build_manual_reference_r2.py`.
- Full receipt: `MANUAL_REFERENCE_BUILD_R2.json`.

## OPEN GATES
- `HUMAN_GATE_ART`: inspect A-D look targets and R2 renders for identity, silhouette, material causality, construction logic and anti-slop.
- TARGET_E material macro + TARGET_F docking/manufacturing close-up: intentionally deferred until look-lock acceptance.
- Real Tripo/Meshy/Hunyuan multiview bake-off: blocked by submit surface, not by model availability.
- Reference build still requires final cleanup/retopology, UV0/UV2, calibrated authored PBR, shipping collision/LOD, target-engine import and same-camera visual regression.
- Target-hardware performance remains unqualified.
- Provider-independent recovered `.blend` + GLB SHA256 delivery receipt remains open.
- Do not call this final AAA art or a shipping asset.

## NEXT 5 ACTIONS
1. Human/creative-director compare the A-D look target pack and R2 renders; reject identity before producing extra detail if needed.
2. If look-lock passes, generate E/F without changing geometry identity; otherwise iterate TARGET_A and regenerate its multiview family.
3. Re-discover the generic image-to-3D submit surface. When available, run identical immutable A-D inputs through at least two candidates, geometry-first; raw outputs remain `BASE_CANDIDATE`.
4. Use the winning visual/reconstruction evidence to replace/refine the R2 manual reference into production topology + UV/PBR/collision/LOD; then target-engine import and visual regression.
5. Emit X100 evidence cells for material causality / meso architecture / reusability / QA only at the maturity actually proven, recompute portfolio gradient, then select the next highest-value gap.

## Claim status

KEEP / ACTIVE / TECHNICALLY_QUALIFIED_REFERENCE / HUMAN_GATE_ART_OPEN.
