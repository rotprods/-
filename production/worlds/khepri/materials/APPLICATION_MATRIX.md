# KHEPRI Material Application Matrix — X100

Authority: `art_source/khepri/materials/compile_application_matrix.py`  
Contract: `KHP_MATERIAL_APPLICATION_MATRIX_X100_V1`

The matrix is generated, not hand-maintained. Current audit:

- valid applications: **139**;
- contradictions filtered: **5**;
- families: **6**;
- scales: **3**;
- matrix SHA256: `18ce236b8983a08d5128364382a13d320caa2ac477307f612e8c1f4f5dd740fa`.

## Application scales

- `hero_insert` — provisional authoring target 1024 px/m; close inspection / hero inset.
- `prop_machine` — provisional authoring target 512 px/m; interactive props and machinery.
- `architectural` — provisional authoring target 256 px/m; modular architecture and broad surfaces.

These are **not runtime budgets**. They exist to keep source authoring density coherent until target hardware, virtual-texture/streaming strategy and texture-memory budgets are qualified.

## Valid applications per family

- solar glass: 23;
- optical mirror: 23;
- Sínodo bronze: 23;
- scorched ceramic: 24;
- shade fabric: 23;
- dark mineral: 23.

## Filtered contradictions

The compiler rejects these semantic mismatches rather than counting them as fake variation:

1. solar glass / thermal cycled / precision polished / architectural;
2. optical mirror / service microabrasion / precision optic / prop machine;
3. Sínodo bronze / contact polished / machined service / architectural;
4. shade fabric / handled worn / laminated cloth / architectural;
5. dark mineral / foot-traffic worn / rough mass / architectural.

## Consumer rule

A downstream asset requests a material application by stable key:

`<asset_id>::<state>::<finish>::<scale>`

The material team owns the material definition. The consuming geometry owner keeps geometry, UV-layout and gameplay ownership. Cross-scope geometry edits require an explicit handoff.

## Failure contract

Never expand the matrix through:

- random grunge variants;
- arbitrary palette swaps;
- global scratches;
- emission variants without functional routing purpose;
- atmospheric corrosion chemistry while atmosphere remains unresolved;
- higher texture resolution treated as material depth by itself.
