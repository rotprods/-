# VANTA CP5 — Material / Trim / Decal Foundation

**World:** VANTA  
**Latest validated revision:** 9  
**Truth level:** `NATIVE_MATERIAL_BINDING_PRESENT_VISUAL_EQUIVALENCE_OPEN` — Godot imports the material-bound surfaces, but PBR appearance equivalence and target-hardware cost are not yet qualified.

## Material foundation

Revision 7 established nine packed 512×512 maps for steel, ferric rust and union-yellow (`BC`, `ORM`, `N`). Revision 8 added packed `TRIM_A` (`BC/ORM/N`), packed `DECAL_A`, four representative decal cards and neutral/Vanta-light calibration boards.

Revision-8 local QA remains valid:

- 13/13 CP5 images packed;
- BC/decal use sRGB; ORM/normal use Non-Color;
- 147 representative CP4 meshes use the upgraded material roles;
- 0 missing UVs;
- CP4 transform and zero-gap assembly regressions: 0.

## Revision 9 portability change

The two CP4 test-yard AREA lights that Blender's glTF exporter reported as unsupported were converted to POINT lights. Revision-9 export no longer reports the AREA-light warning.

The exporter **still reports** that multiple image-texture nodes participate in some PBR/trim materials and that glTF sampler behavior may follow the first image node. This remains a real visual-portability blocker and is not treated as cosmetic log noise.

## Godot 4.7.2 native material-binding receipt

Revision-9 GLB SHA256: `d4cb8154802e7713b9887328431bd27dfdbc6ba6bec07e790fd0b99befef3258`.

GitHub Actions run `34720473947` imported the exact GLB into pinned Godot 4.7.2 and instantiated it as a PackedScene. After `_colonly` collision conversion, the visual scene contained:

- 691 `MeshInstance3D`;
- 691 mesh surfaces;
- **691 surfaces with an active material**;
- seven critical visual names preserved;
- 13 GLB images embedded at transport level.

This is strong evidence that material resources bind natively in Godot. It does **not** prove that Blender and Godot produce equivalent color, roughness, metallic, normal intensity, mip behavior or decal appearance.

## Current CP5 disposition

**Implemented / native binding validated:**

- packed deterministic PBR foundation for steel/rust/yellow;
- packed first trim family;
- packed first decal atlas;
- UV coverage on the representative slice;
- material resources bound to all 691 imported visual surfaces in Godot 4.7.2;
- AREA-light export blocker removed from the QA yard.

**Open:**

- direct visual/art-direction approval;
- Blender↔Godot visual-equivalence captures under controlled exposure;
- resolution/texel-density normalization beyond the 512² proof system;
- mip/compression policy;
- explicit verification of ORM/sampler semantics implicated by the current glTF warning;
- weld/frost/grease families beyond the proof atlas;
- close/mid/far material review;
- target-hardware texture residency, draw, memory and GPU cost;
- propagation to the wider 327-target registry.

Evidence authority: `art_source/vanta/evidence/godot_rev9_native_qualification.json`.
