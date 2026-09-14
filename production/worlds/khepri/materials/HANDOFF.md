# KHEPRI X100 Materials — R4 Recoverable Handoff

AGENT: `AGENT-KHEPRI-MATERIALS-001`  
CLAIM: `CLM-KHEPRI-MATERIALS-001`  
BRANCH: `art/khepri-materials-001`  
PROTOCOL: `/EXOVANT-X100`  
FOUNDATION STATUS: **SYSTEMIC_MATERIAL_FOUNDATION_COMPLETE**  
REGISTRY STATUS: **PROVISIONAL_USER_AUTHORIZED_PENDING_MAIN_REGISTRY**

## NORTH STAR
Create a KHEPRI-specific material system whose depth comes from manufacturing, optical function, heat, use, maintenance and repair—not random grunge—while remaining deterministic, portable and reusable across many downstream assets.

## CURRENT TRUTH
This branch now owns a technically qualified **material-system foundation**, not final AAAA texture art. The current 128×128 maps are deterministic calibration/evidence maps used to prove causality, channel contracts, reproducibility and engine portability. They are explicitly **not** final runtime resolution, texture-memory budget or hero-surface art.

## SOURCE AUTHORITY
There is one material-identity authority:

- `art_source/khepri/materials/compile_material_library.py` — identity compiler: 24 materials, 96 packed maps, 48 calibration meshes.
- `art_source/khepri/materials/present_material_lab.py` — presentation-only camera/labels/backdrop/lights; must not alter material identity.
- `art_source/khepri/materials/build_material_lab.py` — orchestration wrapper; no material-generation math.
- `art_source/khepri/materials/compile_application_matrix.py` — pure-Python family × state × finish × application-scale compiler.

Do not reintroduce parallel material generators.

## MATERIAL FAMILIES
Canonical foundation IDs:

1. `KHP_MAT_GLASS_SOLAR_001`
2. `KHP_MAT_MIRROR_OPTICAL_001`
3. `KHP_MAT_BRONZE_SYNOD_001`
4. `KHP_MAT_CERAMIC_SCORCHED_001`
5. `KHP_MAT_FABRIC_SHADE_001`
6. `KHP_MAT_MINERAL_DESERT_001`

Each family has four causal calibration states. Causes are restricted to:
`base`, `contact_use`, `maintenance`, `thermal`, `repair`, `mechanical_stress`.

No random-grunge or global edge-wear layer exists.

## X100 APPLICATION MATRIX
Contract: `KHP_MATERIAL_APPLICATION_MATRIX_X100_V1`.

The pure compiler produces **139 valid applications** and filters five semantically contradictory combinations. It spans:

- manufacturing finish;
- causal state;
- application scale `hero_insert / prop_machine / architectural`;
- provisional authoring density `1024 / 512 / 256 px per metre` respectively.

These densities are **authoring proposals only** until target hardware and streaming/memory policy are qualified.

Matrix SHA256:
`18ce236b8983a08d5128364382a13d320caa2ac477307f612e8c1f4f5dd740fa`

## REPRODUCIBILITY
Master project: `d2bdc087-55ff-481e-93c5-e66bdfd57d8d` rev `4`.  
Cold project: `67d5c61f-29f2-426b-b6ba-77549f15b452` rev `2`.

Independent rebuild gates:

- 96 packed map bytes: **EXACT MATCH** — `e7aa1d9652a163819077920ed4fb1cf03d234b586333340c26c369e437d00a93`
- 24 material graphs/metadata: **EXACT MATCH** — `77c3fa2bbf1afb678784690123ec5545b2ab14de0788153b1910b159258c814e`
- 48 calibration sample semantics: **EXACT MATCH** — `34f1e9a37c079c5db0104ae0ec226d76d2c6741be6f4b030a9f3304e819bbb29`

Raw Blender vertex/loop ordering is not treated as identity because independent operator execution may reorder equivalent internals. The semantic geometry contract is dimensions, transforms, vertex/poly/loop/UV counts, material assignment, stable names and asset/state/cause metadata.

## FINAL R4 ARTIFACTS
GLB:
- bytes: `5,286,408`
- SHA256: `c855b873c3ef7627b48d60cf0db365b9fd192f4c6f6a59b6b79860dca993ab08`
- persistent media ID: `973ce04a-2268-41e0-bedc-34ee3c5e8aac`

BLEND:
- bytes: `3,304,936`
- SHA256: `e9d5f1fef3d8a9f4ef5f0c35e9605e81b3a0bec865379818d086defb7c8d797a`
- persistent media ID: `7a3c278a-0721-4293-b83b-07c720d64cae`

Visual evidence artifact: `5cbcb5204163c441748eb43d70f8affc`.

## MAP / GLTF BOUNDARY
BLEND contains **96** contract maps:
- 24 BaseColor;
- 24 metallic-roughness;
- 24 Normal;
- 24 causal StateMask.

GLB contains **72** connected textures:
- BaseColor 24;
- MetallicRoughness 24;
- Normal 24;
- Emissive 0.

All 72 are embedded; external URI count = 0; sampler count = 1.

The 24 StateMasks remain deliberately source-only because glTF has no standard generic state-mask texture role. Do not mislabel them as emissive/AO merely to force export.

## GODOT R4
Exact GLB imported with `Godot 4.7.2.stable.official.ed1daf0bf`:

- 24/24 contract materials found;
- 24 albedo textures;
- 24 metallic textures;
- 24 roughness textures;
- 24 normal textures;
- 48 sample meshes;
- zero bad/missing contract materials.

This proves material portability, not target-GPU memory/performance.

## VISUAL QA
Supplemental AI material-calibration review on normalized R3 presentation:

- family separation: PASS;
- state variation: PASS;
- Bronze states: PASS;
- Fabric states: PASS;
- Mirror calibrated: PASS;
- Ceramic patch: PASS;
- Mineral states: PASS;
- random grunge: NO;
- plastic-CGI failure: NO;
- exaggerated damage: NO;
- specular clipping: NO;
- labels/framing: PASS.

This is **not human final-art approval**.

## CANON / NONCLAIMS
Do not infer or author without a later decision:

- exact Glass Sea physical medium;
- atmospheric oxidation/weather chemistry;
- final surface geology;
- cross-world shared material library;
- final architecture;
- runtime texture memory budget;
- final texture resolution;
- target hardware performance.

## REGISTRY / PROMOTION BLOCKER
The branch exists under explicit user authorization because normal fleet reservation was not published after waiting overnight. `CLM-KHEPRI-MATERIALS-001` therefore remains branch-local/provisional until the serialized integrator writes it into `main:ops/fleet/registry.json`, the owner ACKs epoch 1 and the registry reads back `active`.

This is the only blocker to formal producer promotion. It is **not** a blocker to preserving the completed isolated authoring evidence.

## NEXT 3 ACTIONS
1. Publish/serialize `CLM-KHEPRI-MATERIALS-001` into main registry; owner ACK epoch 1; read back `active`.
2. Qualify production-resolution texture tiers, mip/streaming policy and memory budgets against target hardware before generating final-resolution sources.
3. With explicit downstream handoff, apply one material-family set to a real KHEPRI consumer. Preferred first pilot: `KHP_WM_HELIOSTAT_FOOTPRINTS` support geometry, without taking geometry ownership.

CLAIM STATUS: **KEEP / REVIEW / REGISTRY RECONCILIATION REQUIRED**
