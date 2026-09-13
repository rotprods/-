# VANTA CP5 — Material / Trim / Decal Foundation

**World:** VANTA  
**Latest remote revision:** 11  
**Texture payload qualification revision:** 10  
**Truth level:** `TEXTURE_PAYLOAD_AND_CAMERA_GEOMETRY_QUALIFIED / SIMPLE_LIGHT_CALIBRATION_INSUFFICIENT / PHOTOMETRIC_EQUIVALENCE_OPEN`.

## Material foundation and preserved history

- **rev7:** first packed BC/ORM/N foundation for steel, ferric rust and union yellow.
- **rev8:** first packed trim family, decal atlas, neutral/Vanta calibration boards; 147 representative CP4 meshes with 0 missing UVs.
- **rev9:** AREA export blocker removed, but deeper pixel audit proved all **13/13 packed CP5 image payloads were black**. Godot was transporting the invalid source faithfully. This negative receipt remains preserved.
- sampler audit proved there was one exported glTF sampler and no competing sampler policy; the black payload was not caused by the sampler warning.
- **rev10:** all 13 images regenerated through `pixels.foreach_set → update → pack`, then round-tripped through embedded GLB PNGs and Godot texture readback.

Exact rev10 payload checkpoint:

- `.blend`: 11,414,294 B · SHA256 `128979e51a507d97792ef3c15aaf9de20369e21589b60a9d13fe4d0d262d1466`;
- GLB: 9,228,876 B · SHA256 `934450fab1d9eff9dff0dc62971682a692d5f04d4d72871b9f274e6240c7e171`;
- 701 meshes / 832 nodes / 20 materials / 13 embedded images / 0 external resources.

Pinned Godot 4.7.2 runtime readback confirms:

- steel ≈ `[0.1719,0.1831,0.1961]`;
- ferric rust ≈ `[0.4635,0.1423,0.0575]`;
- union yellow ≈ `[0.8015,0.4274,0.0286]`;
- trim ≈ `[0.4895,0.3661,0.2700]`;
- roughness uses channel G (`1`), metallic B (`2`), normals survive;
- required material IDs missing: 0.

**Payload truth:** `EMPIRICALLY_QUALIFIED_GODOT_TEXTURE_PAYLOAD_AND_GROSS_MATERIAL_ROLE_TRANSPORT`.

## Camera / geometry equivalence — PASS

Three exact CP5 neutral swatches were rendered as white unlit geometry over black in Blender and Godot with the same calibration camera.

- silhouette IoU: **0.98481187435**;
- exact mask agreement: **0.9950347222**;
- Blender bbox `[34,66,605,243]` px;
- Godot bbox `[35,66,604,242]` px;
- imported Godot camera preserves expected transform/FOV (`18.549795°`).

The remaining shaded mismatch is therefore not classified as geometry, transform or projection failure.

## Controlled shaded equivalence — FAIL

Baseline shaded board comparison:

- luminance correlation **0.66896**;
- gradient correlation **0.37206**;
- top-15% edge IoU **0.3644**;
- luma SSIM-like **0.37419**;
- raw RGB MAE **0.25074**;
- per-channel tone-matched RGB MAE **0.07029**.

Gross material roles survive, but exact photometric equivalence does not.

## Light-unit diagnosis

Authored neutral point lights:

| Light | Blender source power | glTF point intensity | Godot default imported energy |
|---|---:|---:|---:|
| `L_CP5_NEUTRAL_FILL` | 600 | ~47.74648 | ~47.74648 |
| `L_CP5_NEUTRAL_KEY` | 1200 | ~95.49297 | ~95.49297 |

Observed point export is approximately `source power / (4π)`. Simply enabling Godot physical-light units without converting the imported values made the board more overexposed, so the project flag alone is not a repair.

Reusable diagnostic contract: `art_source/vanta/pipeline/GODOT_LIGHT_TRANSPORT_CONTRACT.md`.

## Standards-aware 4π adapter A/B — TESTED, NOT QUALIFIED

The first physically coherent point-light hypothesis was executed against the isolated neutral board:

- set Godot physical-light units on;
- `OmniLight3D.light_energy = 1`;
- map imported glTF candela to lumens via `lumens = candela × 4π`;
- preserve light transforms, color, range, materials and camera.

Result:

- fill: `47.74648 cd → 600 lm`;
- key: `95.49297 cd → 1200 lm`;
- Godot mean RGB becomes `[0.13666,0.10704,0.10319]` versus Blender `[0.08870,0.04603,0.02844]`;
- luminance correlation **0.48725**;
- gradient correlation **0.41223**;
- edge IoU **0.35017**;
- luma SSIM-like **0.39362**;
- RGB MAE **0.08633**;
- result: **FAIL**.

Adding Godot `TONE_MAPPER_AGX` improves absolute brightness/error somewhat but not structural equivalence:

- mean RGB `[0.11252,0.08290,0.07747]`;
- luminance correlation **0.44629**;
- gradient correlation **0.41709**;
- edge IoU **0.35133**;
- luma SSIM-like **0.41176**;
- RGB MAE **0.07136**;
- result: **FAIL**.

An earlier 2π trial was identified as a harness mistake before persistence and is explicitly discarded.

## 49-combination physical key/fill sweep — NO SIMPLE SCALAR SOLUTION

To test whether the remaining error could be closed by key/fill intensity alone, a 7×7 physical+AgX grid was rendered using scales `[0.25,0.4,0.63,1.0,1.6,2.5,4.0]` for each light, while keeping camera, textures, transforms and material topology fixed.

Acceptance threshold was `luma_corr ≥ 0.75`, `gradient_corr ≥ 0.65`, `edge_iou ≥ 0.35`.

- combinations tested: **49**;
- combinations passing: **0**;
- minimum RGB MAE: **0.0588791** at key `1.0×`, fill `0.25×`, but luma corr only **0.50078**, gradient corr **0.40109**, edge IoU **0.34536**;
- maximum luma correlation: **0.56112** at key `4.0×`, fill `1.0×`, with gradient corr **0.36729**, edge IoU **0.32978**, RGB MAE **0.14399**.

**Conclusion:** simple light-intensity calibration is insufficient. The remaining gap must be investigated in renderer-specific attenuation/radius/softness, BRDF/shadowing, Blender AgX look/color-management, and broader engine shading behavior. Do **not** compensate by mutating the repaired CP5 texture payload.

## Revision 11 exact checkpoint

Rev11 does not intentionally modify the 13 CP5 image payloads; payload qualification remains anchored to rev10.

Exact rev11 recovered binaries:

- `.blend`: **10,162,134 B** · SHA256 `3e60d536e7a38220935775fde9f2505f12adbf42451dcdbcaa87d9054645d899`;
- GLB: **8,823,976 B** · SHA256 `a3ebb39f54d41e732c2ee343961cba43d85a2ced8a36c9d35306142443c36536`.

Evidence authority: `art_source/vanta/evidence/rev11_native_runtime_qualification.json`.

## Current CP5 disposition

**Qualified:**

- repaired 13-image source payload and packed GLB roundtrip;
- Godot texture readback and gross material roles;
- BC / roughness-G / metallic-B / normal channel semantics;
- calibration camera + three-swatch geometry alignment.

**Tested and rejected as sufficient:**

- physical-unit flag alone;
- standards-aware point-light 4π mapping alone;
- 4π + Godot AgX alone;
- 49-combination simple physical key/fill scalar search.

**Still open:**

- renderer-specific attenuation/radius/softness and shadow calibration;
- exact Blender AgX look/color-management matching;
- human visual/art-direction approval;
- production texel-density/mip/compression policy;
- weld/frost/grease production families;
- close/mid/far material review;
- target-hardware texture residency, draw, memory and GPU cost;
- propagation to the wider 327-target registry.

**Critical rule:** CP5 textures are no longer the variable to tune for this mismatch.
