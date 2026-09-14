# KHEPRI X100 — Systemic Material Layering

Contract: `KHP_MATERIAL_RECIPE_X100_V1`  
Compiler: `art_source/khepri/materials/compile_material_recipe.py`

## Objective

Generate hundreds of credible material applications without authoring hundreds of independent full texture sets.

The unit of production is a **recipe**, not a random variant texture folder.

## Source decomposition

Every application is compiled from five explicit dimensions:

1. **Family base** — physical substrate and core response.
2. **Manufacturing finish** — cast, machined, polished, woven, cut, etc.
3. **Causal state** — use, maintenance, thermal history, repair or mechanical stress.
4. **Causal mask** — where that history acts spatially.
5. **Application scale** — hero insert / prop-machine / architectural.

The current matrix compiles these dimensions into 139 valid application IDs while rejecting five contradictions.

## Authoring rule

Do not create a unique BC/MR/N set for every application by default.

Prefer shared source primitives:

- six family-base source sets;
- two manufacturing-finish profiles per family;
- reusable causal-mask generators/painted masks;
- explicit repair inserts/decals only where geometry/history requires them;
- scale-aware tiling density;
- application recipes that compile the above.

This makes variation causal and keeps iteration centralized.

## Portable baseline

The currently verified engine interchange is standard glTF PBR. For a concrete consumer the safe portable baseline is:

`shared source recipe → bake consumer BaseColor + MetallicRoughness + Normal → GLB`

The causal StateMask stays in source unless a runtime shader/interface explicitly consumes it.

This avoids pretending that glTF exposes arbitrary source-mask semantics.

## Future engine-native optimization

Only after engine + hardware qualification may a runtime adapter replace portable baked outputs with mechanisms such as:

- shared tile sets;
- trim sheets;
- decal masks;
- material instances;
- texture arrays;
- virtual texturing / streaming equivalents;
- shader-driven state blending.

None of these are currently canonized as the production runtime path.

## Cache key

A compiled application is addressed by:

`<family_asset_id>::<state>::<finish>::<scale>`

Example:

`KHP_MAT_MIRROR_OPTICAL_001::calibrated::broad_reflector::architectural`

The recipe compiler rejects unknown/filtered keys instead of silently falling back to a generic material.

## Anti-slop constraints

Shared layering must never become a license for:

- random roughness noise;
- one universal grunge mask;
- uniform edge wear;
- arbitrary color variants;
- unrelated decals;
- surface damage disconnected from use/load/heat/repair;
- higher texture resolution as a substitute for material anatomy.

## Production consequence

X100 depth comes from recombination of a small physically coherent source vocabulary. The target is high perceived history and diversity per source hour, with every visible state traceable to a cause and every runtime specialization traceable to a recipe.
