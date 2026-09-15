# KHEPRI Materials → EXOVANT World Compiler Bridge

Status: **COMPILER PASS / PROVISIONAL CLAIM**  
Contract: `KHP_MATERIAL_WORLD_ARTKIT_X100_V1`  
ArtKit version: `KHP_MAT_ARTKIT_001`  
Material claim: `CLM-KHEPRI-MATERIALS-001`  
World: `khepri`  
Civilization: `sinodo_de_bronce`

## Purpose
Expose the KHEPRI X100 material system as machine-readable authored identity for the future EXOVANT World Compiler / Asset Grammar. Procedural systems may choose from this grammar; they do not invent material meaning from filenames or random noise.

This bridge follows the current World Systems Master thesis:

> Procedural systems provide scale; authored systems provide identity; simulation provides causality; constraints provide coherence; validation provides quality.

## Inputs

- `world_artkit_source.json` — authored family/context semantics.
- `compile_application_matrix.py` — 139 semantically valid applications.
- `compile_material_recipe.py` — source/runtime material recipe.
- `compile_world_artkit.py` — deterministic bridge compiler.
- KHEPRI World Bible / EXOVANT Bible — canon and art-direction authority.

## Compiler result

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

## Context examples

The same material family can be reused without becoming semantically generic because the recipe remains context constrained.

### Heliostat bronze
`KHP_MAT_BRONZE_SYNOD_001::service_clean::cast_structural::architectural`

- civilization: Sínodo de Bronce;
- semantic roles: structure / mechanical service part / repair-history carrier;
- allowed: heliostat structure, Sínodo machine, maintenance access, workshop, Crisol de RAKHET, architectural structure;
- forbidden: random ornament, unrelated worlds.

### Heliostat mirror
`KHP_MAT_MIRROR_OPTICAL_001::calibrated::broad_reflector::architectural`

- semantic roles: heliostat reflector / beam routing / access-rights interface;
- allowed: heliostat field, Mar de Cristal, beam node, optical machine, architectural panel;
- forbidden: decorative mirror, unrelated worlds.

## Current context coverage

Compiled application grammar currently exposes approximately:

- `heliostat_field`: 23 compatible applications;
- `mar_de_cristal`: 46;
- `ciudad_de_los_toldos`: 23;
- `crisol_de_rakhet`: 70.

These are grammar compatibilities, not a command to place all compatible materials in each location.

## Interface contract for future generators

A World Compiler consumer should request a semantic application rather than a material filename, e.g.:

```yaml
world_id: khepri
context: heliostat_structure
semantic_role: structure
state: service_clean
finish: cast_structural
scale: architectural
```

The ArtKit resolves the request to a stable `application_id`. A generator must reject a recipe when the requested context appears in `forbidden_contexts` or cannot be matched to `allowed_contexts`.

## Performance boundary

`authoring_px_per_m` values remain source-authoring proposals inherited from the material application matrix. They are **not** runtime memory budgets. Final resolution, compression, mip residency and streaming require representative hardware qualification (`BLOCK-KHP-MAT-001`).

## Nonclaims

This bridge does not establish:

- final engine architecture;
- final texture resolution;
- Xbox/target-hardware memory budget;
- atmospheric chemistry;
- final Glass Sea physical medium;
- cross-world shared material library;
- automatic placement logic;
- human final-art approval.

The bridge supplies authored semantic truth to a future procedural system; it does not replace art direction or validation.
