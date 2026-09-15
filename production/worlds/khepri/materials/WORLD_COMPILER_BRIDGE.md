# KHEPRI Materials → EXOVANT World Compiler Bridge

Status: **ARTKIT + RESOLVER + FIRST CONSUMER BINDING PLAN PASS / PROVISIONAL CLAIM**  
ArtKit contract: `KHP_MATERIAL_WORLD_ARTKIT_X100_V1`  
Resolver contract: `KHP_MATERIAL_WORLD_ARTKIT_RESOLVER_V1`  
Consumer plan contract: `KHP_HELIOSTAT_MATERIAL_BINDING_PLAN_V1`  
ArtKit version: `KHP_MAT_ARTKIT_001`  
Material claim: `CLM-KHEPRI-MATERIALS-001`  
World: `khepri`  
Civilization: `sinodo_de_bronce`

## Purpose
Expose the KHEPRI X100 material system as machine-readable authored identity for the future EXOVANT World Compiler / Asset Grammar, **and enforce its semantic boundaries**. Procedural systems may request material applications from this grammar; they must not infer material meaning from filenames, nearest-neighbour similarity or random variation.

Current chain:

```text
KHEPRI canon / World Bible
    ↓
KHP_MAT_ARTKIT_001
    ↓
fail-closed semantic resolver
    ↓
consumer world metadata (role/state/variant/context)
    ↓
causal material binding plan
    ↓
portable/runtime representation selected only after engine qualification
```

This bridge follows the World Systems Master thesis:

> Procedural systems provide scale; authored systems provide identity; simulation provides causality; constraints provide coherence; validation provides quality.

## ArtKit inputs

- `world_artkit_source.json` — authored family/context semantics.
- `compile_application_matrix.py` — 139 semantically valid applications.
- `compile_material_recipe.py` — source/runtime material recipe.
- `compile_world_artkit.py` — deterministic ArtKit compiler.
- KHEPRI World Bible / EXOVANT Bible — canon and art-direction authority.

## ArtKit compiler result

Cold checkout audit:

- 6 material families;
- 139 applications;
- 5 invalid semantic combinations filtered before compilation;
- every application has stable ID, causal state, manufacturing finish, application scale, style tags, semantic roles, allowed contexts and forbidden contexts;
- all portable recipes remain non-emissive unless a separate functional signal family is defined;
- StateMask remains source-only;
- target-hardware texture budget remains explicitly blocked rather than invented.

Hashes:

- application matrix SHA256: `18ce236b8983a08d5128364382a13d320caa2ac477307f612e8c1f4f5dd740fa`
- application IDs SHA256: `96d7e9406116e0556b68fc1199ec77c255d19d6ea36a151f5be284bd20176165`
- compiled ArtKit SHA256: `c39e634c584ac01befeca61d74f3f1d87ab311f864f15a42098bdc837fe7584f`

## Fail-closed resolver

Tool: `art_source/khepri/materials/resolve_world_material_request.py`

The World Compiler must request semantics, not filenames:

```yaml
world_id: khepri
context: heliostat_structure
semantic_role: structure
state: service_clean
finish: cast_structural
scale: architectural
```

Resolver rules:

- wrong world → `REJECTED / WORLD_MISMATCH`;
- unknown semantic role → `REJECTED`;
- explicitly forbidden context → `REJECTED / FORBIDDEN_CONTEXT`;
- impossible combination → `REJECTED / NO_VALID_APPLICATION`;
- more than one authored candidate → `AMBIGUOUS / AUTHORED_SELECTOR_REQUIRED`;
- exactly one valid application → `RESOLVED` with stable `application_id`.

It never chooses “the closest material”.

### Resolver evidence

Basic adversarial audit PASS:

- exact heliostat Bronze resolves;
- exact heliostat Mirror resolves;
- decorative mirror is rejected;
- cross-world `vanta` request is rejected;
- underspecified Crisol structure is marked ambiguous rather than randomly selected.

Exhaustive cold audit:

- **139/139** applications can round-trip exactly through at least one authored semantic request;
- 0 wrong-family resolutions;
- 0 valid applications rejected;
- 0 valid applications left ambiguous after full authored selectors;
- 12/12 forbidden-context probes rejected.

Hashes:

- basic audit SHA256: `178c4db24cc9a76fd8dee65146b4e4a87fe74eb5e1040c43df775086d1005e7a`
- exhaustive audit SHA256: `92bd3b05c19204a167e150d6fa5edcd40dd56c45c4399c00db7d75de6559fbd0`

Receipt: `receipts/WORLD_COMPILER_RESOLVER_V1.json`.

## Context examples

### Heliostat Bronze
`KHP_MAT_BRONZE_SYNOD_001::service_clean::cast_structural::architectural`

- civilization: Sínodo de Bronce;
- semantic roles: structure / mechanical service part / repair-history carrier;
- allowed: heliostat structure, Sínodo machine, maintenance access, workshop, Crisol de RAKHET, architectural structure;
- forbidden: random ornament, unrelated worlds.

### Heliostat Mirror
`KHP_MAT_MIRROR_OPTICAL_001::calibrated::broad_reflector::architectural`

- semantic roles: heliostat reflector / beam routing / access-rights interface;
- allowed: heliostat field, Mar de Cristal, beam node, optical machine, architectural panel;
- forbidden: decorative mirror, unrelated worlds.

## Current context coverage

Compiled grammar currently exposes approximately:

- `heliostat_field`: 23 compatible applications;
- `mar_de_cristal`: 46;
- `ciudad_de_los_toldos`: 23;
- `crisol_de_rakhet`: 70.

These counts are compatibility, not placement commands.

## Consumer metadata bridge — real KHEPRI R10

The R10 world consumer already publishes per-instance authored metadata:

- `world_id`;
- `family_asset_id`;
- `role`;
- `state`;
- `variant_id`;
- stable `exovant_asset_id`;
- epistemic status.

Snapshot:
`art_source/khepri/materials/heliostat_consumer_state_matrix.json`

Metadata SHA256:
`10f8a55ecbada301c8c0b392f3731cd6283c328e4e5d98dde044fbd291f4600b`

Observed consumer:

- 214 optical objects;
- 107 masts + 107 panels;
- each role: 93 operational + 14 maintenance;
- compact / standard / wide variants.

## Causal binding-plan compiler

Tool: `art_source/khepri/materials/compile_heliostat_binding_plan.py`

It resolves the real consumer state into authored material applications through the resolver:

### Mast
Both operational and maintenance mast proxies use:

`KHP_MAT_BRONZE_SYNOD_001::service_clean::cast_structural::architectural`

The structural material is state-invariant at this macro-support level.

### Panel
Operational optical face:

`KHP_MAT_MIRROR_OPTICAL_001::calibrated::broad_reflector::architectural`

Maintenance optical face:

`KHP_MAT_MIRROR_OPTICAL_001::maintenance_cleaning::broad_reflector::architectural`

Panel structural slot remains Sínodo Bronze.

### Binding-plan evidence

- objects: 214;
- role/state/variant groups: 12;
- plan SHA256: `ca709806dbb4463a6088b49effdeffa4946638bd64e17091b4778c66fb7efeea`;
- combined resolver+binding audit SHA256: `7c2385b33868e789071b80f70086ec1df243427908362bd67a977da7d3a71591`;
- every group has an authored binding;
- operational panels resolve calibrated Mirror;
- maintenance panels resolve maintenance-cleaning Mirror;
- mast Bronze remains state-invariant.

Receipt: `receipts/HELIOSTAT_BINDING_PLAN_V1.json`.

## Runtime representation boundary

Material causality and runtime representation are separate decisions.

Current R10 has six shared optical Mesh resources:

- 3 mast variants;
- 3 panel variants.

A qualified engine-level per-instance/material override could preserve those six resources.

Portable glTF fallback without such a feature needs only:

- 3 mast resources (state-invariant material);
- 6 panel resources (3 variants × operational/maintenance material state);
- **9 total optical Mesh resources**.

Therefore state causality does **not** require 214 unique resources. Portable fallback is +3 resources / **1.5×** current optical mesh-resource count while keeping 214 scene objects.

The runtime strategy is deliberately deferred until engine/target-hardware qualification.

## Performance boundary

`authoring_px_per_m` values remain source-authoring proposals inherited from the application matrix. They are **not** runtime memory budgets. Final resolution, compression, mip residency and streaming require representative hardware qualification (`BLOCK-KHP-MAT-001`).

Likewise, the 6-vs-9 mesh-resource runtime choice requires engine profiling; the ArtKit does not silently choose it.

## Nonclaims

This bridge does not establish:

- final engine architecture;
- final runtime material-override capability;
- final texture resolution;
- Xbox/target-hardware memory budget;
- runtime LOD state switching;
- atmospheric chemistry;
- final Glass Sea physical medium;
- cross-world shared material library;
- automatic story-state assignment;
- human final-art approval.

The bridge supplies authored semantic truth and fail-closed constraints to procedural systems; it does not replace art direction, gameplay ownership or validation.
