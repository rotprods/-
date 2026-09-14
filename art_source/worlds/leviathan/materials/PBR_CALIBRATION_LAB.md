# LEVIATHAN · Portable PBR Calibration Lab v1

Status: `CALIBRATION_PROTOTYPE_NOT_FINAL`  
Claim: `CLM-W10-WORLD-LEVIATHAN-001`  
Task: `W10/MAT/008`  
Scope: isolated material QA project only; **do not propagate to the world master without art + engine review**.

## Purpose

Advance LEVIATHAN from constant-color Principled material roles toward a portable, image-textured PBR basis while keeping the world master reversible and uncontaminated.

This lab is deliberately **engine-neutral** and **provider-local**:

- no external textures, scans or licensed libraries;
- all textures are generated deterministically from versioned Python;
- packed image textures are embedded in the editable Blender source;
- GLB portability is part of the test;
- no 4K/UDIM/virtual-texturing policy is invented before runtime/hardware qualification;
- no material is promoted as final AAAA art from this lab alone.

## Existing asset interfaces only

### `LEV-MAT-001` — living host material family
1. `LEV_CAL_TISSUE_WARM`
2. `LEV_CAL_MUCOSA_WET`
3. `LEV_CAL_CARTILAGE`

### `LEV-MAT-002` — human graft material family
4. `HUM_CAL_IVORY_CERAMIC`
5. `HUM_CAL_BRUSHED_METAL`
6. `HUM_CAL_SEAL_RUBBER`

No new global material asset IDs are created by the lab.

## Texture contract

Calibration resolution: **256×256 per map**. This is a deterministic QA resolution, not a shipping texture budget.

Each swatch receives:

- BaseColor image (sRGB intent);
- Metallic/Roughness image (Non-Color; G=roughness, B=metallic; R reserved=1.0);
- tangent-space Normal image (Non-Color; neutral Z-up baseline with deterministic microstructure);
- one portable Principled BSDF material;
- explicit calibration metadata describing intended roughness/metallic ranges and physical role.

### Physical intent / failure contract

| Swatch | Role | Roughness intent | Metallic | Art failure to avoid |
|---|---|---:|---:|---|
| Tissue Warm | load-bearing living host tissue | 0.36–0.58 | 0 | plastic toy flesh, uniform pink |
| Mucosa Wet | moist pressure/lumen surface | 0.10–0.28 | 0 | mirror chrome wetness, flat candy red |
| Cartilage | fibrous structural biological frame | 0.38–0.62 | 0 | porcelain/bone confusion, perfectly smooth ivory |
| Ivory Ceramic | replaceable human graft shell | 0.20–0.34 | 0 | sterile CG white, zero micro-pitting |
| Brushed Metal | human technical load frame | 0.24–0.42 | 1 | uniform gray plastic, random isotropic noise |
| Seal Rubber | compression gasket / soft technical seal | 0.56–0.78 | 0 | velvet, glossy vinyl, pure black clipping |

## Scene QA contract

The calibration scene must contain:

- one 1 m-class UV sphere per swatch;
- one slanted planar coupon per swatch to reveal grazing-light roughness/normal response;
- 1.85 m human scale reference;
- neutral floor/backdrop;
- portable `SUN`/`POINT`/`SPOT` lighting only;
- overview camera plus one grazing-light close camera;
- semantic collections separating host/human/light/reference assets;
- metre units and 24 fps.

## Acceptance gates for the lab

A calibration revision may be called `LAB_PASS` only when:

1. all six swatches have BaseColor + MR + Normal image nodes;
2. image nodes are connected to Principled inputs through portable nodes;
3. generated images are packed into `.blend`;
4. GLB export exists with no missing-image error;
5. all sphere/coupon dimensions are metre-scale and transforms sane;
6. no material uses unsupported external texture paths;
7. independent cold replay reproduces the same generated texture digests and material parameters;
8. rendered artifact receipts exist;
9. **direct artistic approval and world-master propagation remain separate gates**.

## Non-claims

This lab does **not** establish:

- final material look;
- final texel density;
- final texture resolution;
- final SSS/transmission model;
- final shader cost;
- engine-specific channel packing;
- target-hardware performance;
- final art approval.

The lab exists to replace ambiguity with a deterministic, portable material baseline that can later be reviewed and promoted selectively.
