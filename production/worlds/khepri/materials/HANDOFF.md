# KHEPRI X100 Materials — R10 consumer / ArtKit handoff

AGENT: `AGENT-KHEPRI-MATERIALS-001`  
CLAIM: `CLM-KHEPRI-MATERIALS-001`  
BRANCH: `art/khepri-materials-001`  
PROTOCOL: `/EXOVANT-X100`  
FOUNDATION: **SYSTEMIC_MATERIAL_FOUNDATION_COMPLETE**  
FIRST REAL CONSUMER: **TECHNICAL PASS**  
WORLD COMPILER BRIDGE: **PASS**  
REGISTRY: **PROVISIONAL_USER_AUTHORIZED_PENDING_MAIN_REGISTRY**

## North Star
Create KHEPRI material depth from manufacturing, optical function, heat, use, maintenance and repair—not random grunge—and expose it as deterministic reusable authored identity for both direct asset consumers and the future EXOVANT World Compiler.

## Source authority
Do not create parallel material generators.

- `compile_material_library.py` — 24 identity materials / 96 packed maps / 48 calibration meshes.
- `present_material_lab.py` — presentation only.
- `build_material_lab.py` — orchestration only.
- `compile_application_matrix.py` — 139 semantically valid applications.
- `compile_material_recipe.py` — layered source/runtime recipe.
- `world_artkit_source.json` — authored World-Compiler semantics.
- `compile_world_artkit.py` — deterministic ArtKit bridge.

## Material foundation R4
Master: `d2bdc087-55ff-481e-93c5-e66bdfd57d8d` rev 4.  
Cold: `67d5c61f-29f2-426b-b6ba-77549f15b452` rev 2.

Foundation:
- 6 families;
- 24 causal-state materials;
- 96 packed source maps;
- 72 GLB-connected BC/MR/N maps;
- 24 source-only StateMasks;
- 48 calibration meshes;
- 139 valid family × state × finish × scale applications;
- 5 contradictory combinations filtered.

Exact reproducibility:
- image manifest `e7aa1d9652a163819077920ed4fb1cf03d234b586333340c26c369e437d00a93`;
- material graph `77c3fa2bbf1afb678784690123ec5545b2ab14de0788153b1910b159258c814e`;
- sample semantics `34f1e9a37c079c5db0104ae0ec226d76d2c6741be6f4b030a9f3304e819bbb29`.

R4 persistent artifacts:
- GLB `5,286,408 B`, SHA `c855b873c3ef7627b48d60cf0db365b9fd192f4c6f6a59b6b79860dca993ab08`, media `973ce04a-2268-41e0-bedc-34ee3c5e8aac`;
- BLEND `3,304,936 B`, SHA `e9d5f1fef3d8a9f4ef5f0c35e9605e81b3a0bec865379818d086defb7c8d797a`, media `7a3c278a-0721-4293-b83b-07c720d64cae`.

Godot 4.7.2 readback and normalized material-calibration AI QA pass. This remains calibration evidence, not final-resolution texture art.

## UV handoff — blocker closed
`BLOCK-KHP-MAT-002` is **RESOLVED** by geometry owner `CLM-KHEPRI-WMACRO-001`.

Contract: `KHP_OPTICAL_UV0_HANDOFF_V1`

- 18 meshes covered across LOD0/1/2;
- `UVMap` uses dominant-axis local-object mapping;
- 4 metres per repeat;
- intentional tiling overlap;
- geometry SHA before/after unchanged: `41cb03864b03a907c8691de33843f874f1796ba67b0dc02980ad5af9fc60cf86`;
- master/cold UV SHA exact match: `13532b5bb722e7293e5248e061d6e30192a8cf21c21c355abd89095ea26a9c8e`.

Unique per-instance hero/story masks require a separate non-overlapping UV interface later.

## First real consumer — KHEPRI R10
Consumer: `KHP_WM_HELIOSTAT_FOOTPRINTS`  
World project: `040f0c45-83a7-483c-9ee7-1e31c640a587` rev 10.  
Contract: `KHP_HELIOSTAT_MATERIAL_PILOT_V1`

Bindings:
- Bronze structural: `KHP_MAT_BRONZE_SYNOD_001::service_clean::cast_structural::architectural`;
- Mirror optical: `KHP_MAT_MIRROR_OPTICAL_001::calibrated::broad_reflector::architectural`.

The R4 deterministic material compiler regenerated the exact source maps inside the consumer project; every source SHA was checked before slot mutation. Nine visible LOD0 material slots were changed. Geometry + UV SHA stayed identical:
`32274b915360ebcc3a9c1f9fb0f9ee79e2847986b48e6566d81c176b17e35824`.

Exact R10:
- GLB `590,844 B`, SHA `240154331d5514cbcc9d4d454ed944032f5f24458c522348b9105caa52fc01c4`, persistent media `f6f51455-0742-4233-97c2-9306fe7b7127`;
- BLEND `2,350,870 B`, SHA `95622989e554ffd843c67a06efa502934dda91ce8602045a2405ffcf7314baba`, persistent media `40d8e353-e509-43bd-9a36-2132cd427ac8`.

Godot exact import PASS:
- 229 runtime nodes;
- 219 MeshInstance3D;
- 107 masts / 107 panels;
- 3 unique mast meshes / 3 unique panel meshes;
- Bronze + Mirror retain albedo/metallic/roughness/normal textures;
- instancing preserved;
- `fleet_control.py delivery` PASS.

Receipt: `receipts/HELIOSTAT_R10_CONSUMER_PILOT.json`.

## Consumer visual truth
Technical consumer gate = **PASS**. Final material-art gate = **NOT PASS**.

Machine values are correct:
- Bronze metallic ≈0.82, roughness ≈0.25–0.34;
- Mirror metallic ≈0.94, roughness ≈0.075;
- BC/MR/N connections present;
- UV catastrophe absent.

But R10 consumer is Tier-D proxy geometry and KHEPRI world master currently has a single Sun plus near-black, unqualified sky/reflection context. AI close-up cannot read production-grade Bronze/Mirror and reports CGI/blockout character. Do **not** distort calibrated materials merely to compensate for missing close-range geometry or sky/lookdev.

New blocker: `BLOCK-KHP-MAT-003.yaml`.

## World Compiler ArtKit
Contract: `KHP_MATERIAL_WORLD_ARTKIT_X100_V1`  
Version: `KHP_MAT_ARTKIT_001`

Cold compiler PASS:
- 6 families;
- 139 applications;
- stable semantic/application IDs;
- style tags, semantic roles, allowed/forbidden contexts, causal state, manufacturing finish and application scale;
- material recipes remain non-emissive unless a separate functional signal family is defined;
- target-hardware budget remains explicitly blocked.

Hashes:
- matrix `18ce236b8983a08d5128364382a13d320caa2ac477307f612e8c1f4f5dd740fa`;
- application IDs `96d7e9406116e0556b68fc1199ec77c255d19d6ea36a151f5be284bd20176165`;
- ArtKit `c39e634c584ac01befeca61d74f3f1d87ab311f864f15a42098bdc837fe7584f`.

This bridge allows a future World Compiler to request semantic material applications instead of selecting filenames or generating random texture variation.

Docs/receipt:
- `WORLD_COMPILER_BRIDGE.md`
- `receipts/WORLD_COMPILER_ARTKIT_V1.json`

## Open blockers
Promotion blockers:
1. main registry must publish `CLM-KHEPRI-MATERIALS-001`, owner ACK epoch 1, readback active;
2. `HUMAN_ART_GATE`;
3. qualified KHEPRI sky/reflection or close-range heliostat consumer for final reflective-material judgement.

Hardware blocker:
- final texture resolution, compression, mips and residency need representative target hardware; no Xbox/target GPU authority is currently recovered in repo. Do not invent it.

Canon blockers:
- atmospheric chemistry;
- exact Glass Sea physical medium.

## Next actions
1. Serialize/admit the materials claim into the current main fleet registry; ACK epoch 1.
2. Keep R10 as technical consumer proof and require better consumer/lookdev context before final visual promotion.
3. Feed `KHP_MAT_ARTKIT_001` to future World Compiler/Asset Grammar work; validate context rejection as strongly as allowed-context selection.
4. Select the next real consumer only where geometry ownership and lookdev context are qualified.
5. Do not generate final-resolution textures until target-hardware budgets are measured.

CLAIM STATUS: **KEEP / REVIEW / REGISTRY RECONCILIATION REQUIRED**  
FOUNDATION: **COMPLETE**  
FIRST REAL CONSUMER: **TECHNICAL PASS**  
WORLD COMPILER ARTKIT: **PASS**  
FINAL ART: **PENDING / BLOCKED BY DOWNSTREAM LOOKDEV + HUMAN REVIEW**
