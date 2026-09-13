# LEVIATHAN · Cold-Recovery Handoff

AGENT: `AGENT-LEVIATHAN-10`  
SESSION: `ART-LEVIATHAN-001-20260912T2123+0200`  
CLAIM: `CLM-W10-WORLD-LEVIATHAN-001`  
BRANCH: `art/world-leviathan-001`  
MAIN LAST OBSERVED: `26ae20f5d1b47d1efa0d54b20124ed93cbc0b43e`  
CLAIM STATUS: **KEEP / IN_PROGRESS**

NORTH STAR: reproducible LEVIATHAN foundation with causal living-world art, stable gameplay collision beneath visual tissue, durable portable material evidence, and no invented planet/engine budgets.

## 0. Resume protocol

1. Read `AGENTS.md`, `docs/FLEET_COORDINATION.md`, `ops/fleet/registry.json`, issue #7 and this file.
2. Fetch live `main`, this branch and PR #10 before any mutation.
3. World master: `2577a7b6-ebd7-4d31-a645-620e4b73a95d` @ r11.
4. World cold replay: `37a931c7-f2e6-46bc-9be0-26077e5de1c1` @ r9.
5. PBR primary lab: `6c67e70a-d29b-4a9d-8387-68ba071d8c3f` @ r5.
6. PBR cold lab: `21dfcfc6-a181-4300-b6a9-0ee2e09695ee` @ r1.
7. Do not self-promote fleet registry or touch shared runtime/global state from this claim.

## 1. Fleet / CI truth

- Latest main: `26ae20f5...`.
- Fleet registry generation: `8`.
- LEVIATHAN remains `reserved`, `ack:null`; integrator owns transition to `active`.
- Producer ACK: issue #7 comment `5648464282`.
- Jardines delta: `5648515712`; SOMA delta: `5648567162`.
- Manifest/integration request: `5648779529`.
- PBR auxiliary-project/material delta: `5652950795`.
- Main quarantines automatic Gauntlet triggers to reduce CI spend. Do not spend a rerun until exact merge-tree MANIFEST reconciliation.
- Last deeply diagnosed PR #10 run `34718006302`: 75/75 Python tests PASS; only root `MANIFEST.json` drift failed continuity before Godot stage.

## 2. Canon boundaries

CANON: LEVIATHAN / Soma / EL UMBRAL / Comuna del Pulso / 1.15 g / 38 °C / Puerto de la Herida / Jardines Inmunes / Cámara de SOMA / exact 58 m SOMA chamber.

UNKNOWN/BLOCKED: physical planet radius/diameter, final production engine, target hardware/preset, final playable-region dimensions, final SOMA anatomy.

PROPOSAL only: 720×480 m authored cell, representative creature dimensions, 8 m traversal width, current authored density and any LOD ratios until separately validated.

## 3. World remote truth

Primary working master: r11.
- blend 4,869,637 B / etag `7ccfdd11e07d845b3e962a802bdefa32`
- GLB 5,639,948 B / etag `3ab7e46dc7e2102ca709600b83269ecb`

Cold world: r9.
- blend 4,869,637 B / etag `1df2bc94b4ef09c3bb0c21f0f81c0c3e`
- GLB 5,643,252 B / etag `1a8147165c232f098e5e01ede32d3cf0`

Binary equality is not the art reproducibility criterion; evaluated visual-surface/delta equivalence is.

## 4. Representative region checkpoints

### Puerto
IDs `LEV-ARCH-001`, `LEV-INF-002`, `LEV-INF-003`.
- representative graft module, suture clamp, living valve;
- service-door defect corrected from 4.35 m to `0.28×1.60×2.60 m`;
- 13,380 native mesh tris;
- receipt `evidence/puerto_microset_r5.json`.

### Jardines
IDs `LEV-INF-005`, `LEV-ECO-001`, `LEV-ECO-004`.
- pressure conduit + independent stable service walk;
- pulse-algae pressure states;
- functional gardener proposal;
- 2.6 m = core body; articulated envelope `5.35×5.50×3.37 m`;
- collision core-only provisional; 21,644 evaluated tris;
- receipt `evidence/jardines_microset_r7.json`.

### SOMA
IDs/interfaces `LEV-RGN-003`, `LEV-ENV-002`, `LEV-ENV-003`, local `LEV-INF-003` variants.
- bridges, three refuge valves, contraction telegraphs, regulator cradle;
- v1 rejected before execution for possible chamber-radius violation;
- v2 evaluated max radius `28.3 m`, 0.7 m inside canonical 29 m;
- `SOMA_PROXY_NOT_FINAL`: combat-scale/silhouette only, `final_anatomy=false`;
- 34,308 evaluated tris;
- receipt `evidence/soma_encounter_microset_r8.json`.

## 5. Structural optimization / reproducibility

`optimize_repeated_mesh_instances_v2.py` uses order-invariant editable-surface signatures.

r8 → r10:
- 260 mesh objects remain;
- mesh datablocks `260 -> 98`;
- 162 duplicates removed = 62.3077%;
- blend reduction ~36.7564%; GLB reduction ~33.858%.

Primary/cold converge to 98 datablocks and the same canonical evaluated visual surface:
`1b9d885f7fd612a30c4fd289bbc79da6b06472b710867e8f63bafa9c87827a5d`.

Receipts: `evidence/canonical_surface_repro_r9.json`, `evidence/instancing_optimization_r10_v2.json`.

## 6. Stable traversal continuity — r11/r9

Source: `tools/build_stable_traversal_ribbon_v1.py`.

Measured:
- centerline 541.256 m;
- width 8.0 m **proposal**;
- thickness 0.5 m;
- 212 verts / 420 tris / zero degenerates;
- top z 5→7 m;
- max segment slope 7.6923% **not runtime-approved**;
- min real side clearance inside 6 m visual tube 1.0513 m;
- SOMA ingress side margin 1.1962–1.2161 m;
- final point `[205,-47,7]`, inside SOMA footprint and exactly on arena top;
- visual ingress remains outside collision.

Cold replay new-surface SHAs match primary:
- ribbon `65326c41be09e967561907938cf994e389cd1c28ad33390815b5fdd85dde253a`;
- ingress `3f8b05130e849f7fec36b059d6f11c3fab16cd43b74c8a80dbec446d8fd0e432`.

Receipt: `evidence/traversal_ribbon_r11.json`.

## 7. UV / PBR / LOD truth

World master:
- 260/260 mesh objects have UV layers;
- zero zero-area UV triangles / zero UV loops outside 0–1;
- texel density not normalized;
- image textures intentionally remain **0**;
- 18 portable constant material roles;
- no approved production LOD chain.

Contract: `UV_PBR_LOD_CONTRACT.md`; audits: `evidence/uv_pbr_lod_audit_r8.json`, `evidence/lod_feasibility_r10.json`.

LOD feasibility says: reject one global ratio; macro/rings tolerate greater simplification than small rounded hero/status/ecology parts. Final screen-space thresholds require engine/camera/hardware qualification.

## 8. Portable PBR calibration lab — canonical r5

Purpose: prove deterministic durable image-textured PBR transport **without contaminating the world master**.

Existing IDs only:
- `LEV-MAT-001`: Tissue Warm / Mucosa Wet / Cartilage.
- `LEV-MAT-002`: Ivory Ceramic / Brushed Metal / Seal Rubber.

Primary lab: `6c67e70a-d29b-4a9d-8387-68ba071d8c3f` r5.  
Cold lab: `21dfcfc6-a181-4300-b6a9-0ee2e09695ee` r1.  
Canonical builder: `tools/build_pbr_calibration_lab_v5_canonical.py`.  
Receipt: `evidence/pbr_calibration_lab_r5.json`.

### Failures recovered, not hidden
- r1 rejected: GENERATED images did not survive checkpoint with durable pixels.
- r2 rejected: Blender `Image.save()` produced identical black PNG buffers in this worker.
- custom byte-level PNG encoder canary passed.
- r3: durable packed PNGs established; found 8-bit roughness overflow on ceramic.
- r4: quantization-safe MR bounds fixed.
- r5: all accepted lessons consolidated into one empty-scene canonical builder.

### Technical PASS
- 27 objects / 15 meshes / 6 font curves / 2 cameras / 3 portable lights / 8 materials / 18 calibration images / 5 collections;
- zero orphan datablocks;
- 6 calibration materials × BaseColor/MR/Normal = 18 packed PNGs;
- 18 unique actual packed SHA256 values;
- 0 external file paths after packing;
- one UVMap per calibration material feeding all three texture nodes;
- decoded MR ranges remain within physical contracts after 8-bit quantization;
- sampled normal-vector lengths ≈1;
- parsed GLB: 18 images, 18 textures, 1 sampler, 8 materials, 18/18 images embedded, zero external image URI;
- all six calibration materials expose BaseColor + MetallicRoughness + Normal texture roles.

Primary r5 == cold r1 canonical fingerprint:
`fb881b5d76c3c2fe8f35441b7f27cf4a0ad71db74f69a915eb1d48d966db9230`.

Blender glTF sampler warning is classified EXPECTED_NON_BLOCKING: Metallic and Roughness sockets share the same MR Image Texture; exporter source warns on multiple shader sockets but uses the first sampler. Scene uses identical Linear/REPEAT sampling and parsed GLB contains exactly one sampler.

Render receipts exist:
- overview artifact `d87fa26f81070380bfd98f4b75f48c38` (640×360, 276,379 B);
- grazing artifact `bdf5a487186de4f4e62bd5483b4a8906` (640×360, 238,821 B).

Direct pixel/human art review is still unavailable and **not PASS**. Calibration resolution 256² is QA-only, not shipping budget. World-master propagation is not approved.

## 9. Current task truth

DONE: `W10/WORLD/001`, `W10/WORLD/002`, `W10/BLEND/003`.

REVIEW: `W10/REGION/004`, `005`, `006`, `W10/TECH/007`, `W10/MAT/008`, `W10/ECO/009`, `W10/QA/010`.

No region or MAT task is DONE because direct art review, runtime integration and world-master propagation remain open.

## 10. Open blockers

- `LEV-BLK-001`: physical planet radius/diameter absent.
- `LEV-BLK-002`: production engine not qualified.
- `LEV-BLK-003`: target hardware/preset not qualified.
- `LEV-BLK-004`: final SOMA anatomy/art/rig decision.
- `LEV-BLK-005`: final playable-region dimensions.
- `LEV-BLK-007`: exact provider binary + qualified runtime cannot yet coexist in this producer surface; confirmed via shell, secure-download path and independent browser.

Direct pixel-level art review remains unavailable; do not claim `B_ART`/visual-regression PASS.

## 11. Explicit non-claims

- LEVIATHAN is not DONE/AAAA-complete.
- calibration lab is not final world material art;
- no approved shipping texture resolution/UDIM/VT policy;
- no final texel density;
- no world-master PBR propagation;
- no final LOD/HLOD chain;
- no target-hardware FPS/GPU pass;
- no final NPC/creature/SOMA rig/animation;
- no engine import/capsule/nav/material runtime PASS.

## 12. Recovery files

Core: `WORLD_BIBLE.md`, `MASTER_ASSET_LIST.yaml`, `TASKS.yaml`, `STATUS.yaml`, `UV_PBR_LOD_CONTRACT.md`, `validation.json`.

Key generators: `build_master_scene.py`, `build_puerto_microset.py`, `refine_puerto_microset_v2.py`, `build_jardines_microset.py`, `refine_jardines_truth_v2.py`, `build_soma_encounter_microset_v2.py`, `optimize_repeated_mesh_instances_v2.py`, `build_stable_traversal_ribbon_v1.py`, `build_pbr_calibration_lab_v5_canonical.py`.

Key receipts: `canonical_surface_repro_r9.json`, `instancing_optimization_r10_v2.json`, `lod_feasibility_r10.json`, `traversal_ribbon_r11.json`, `pbr_calibration_lab_r5.json`, `runtime_import_blocker_r5.json`.

## 13. Next executable actions

1. Convert measured LOD feasibility into a versioned per-family, engine-neutral LOD policy and candidate-generation contract; do not approve final thresholds.
2. Expand representative asset coverage only inside existing LEVIATHAN IDs after live preflight.
3. Keep PBR textures isolated until direct art + engine validation become available.
4. When exact export bytes and qualified engine coexist, execute import → instantiate → scale/material/collision/capsule/nav traversal and bind evidence to export.
5. Integrator must reconcile registry ACK/asset/project IDs and root MANIFEST on exact merge tree before manual Gauntlet spend.

CLAIM STATUS: **KEEP**. PR #10 remains draft. Do not merge as world-complete.
