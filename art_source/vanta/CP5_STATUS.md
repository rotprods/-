# VANTA CP5 — Material / Trim / Decal Foundation

**World:** VANTA  
**Latest remote revision:** 11  
**Texture payload qualification revision:** 10  
**Truth level:** `GODOT_TEXTURE_PAYLOAD_AND_GROSS_ROLE_TRANSPORT_QUALIFIED / PHOTOMETRIC_EQUIVALENCE_BLOCKED_BY_LIGHT_TRANSPORT` — CP5 payload transport is qualified, camera/geometry alignment is qualified, but Blender↔Godot shaded equivalence is not.

## Material foundation

Revision 7 established nine packed 512×512 maps for steel, ferric rust and union-yellow (`BC`, `ORM`, `N`). Revision 8 added packed `TRIM_A` (`BC/ORM/N`), packed `DECAL_A`, four representative decal cards and neutral/Vanta-light calibration boards.

Revision-8 local QA remains valid:

- 13/13 CP5 images packed;
- BC/decal use sRGB; ORM/normal use Non-Color;
- 147 representative CP4 meshes use the upgraded material roles;
- 0 missing UVs;
- CP4 transform and zero-gap assembly regressions: 0.

## Revision 9 portability history

The two CP4 test-yard AREA lights that Blender's glTF exporter reported as unsupported were converted to POINT lights. The exporter continued reporting that multiple image-texture nodes participate in some PBR/trim materials and that glTF sampler behavior may follow the first image node.

A deeper audit proved two distinct facts that must not be conflated:

1. all 13 rev9 CP5 image payloads were actually black — a real source defect;
2. the sampler warning did **not** correspond to competing sampler policies: CP5 image nodes use the same sampler settings and the exported GLB contains one sampler.

Godot rev9 was transporting the bad black payload correctly. This negative evidence is preserved rather than rewritten as an importer failure.

## Revision 10 — texture payload repair and native role transport

Operation `vanta-rev10-texture-payload-repair-001` regenerated all 13 CP5 512×512 images in place using the validated `pixels.foreach_set → update → pack` path. Before commit, every image was round-tripped through a temporary GLB, its embedded PNG was extracted/reloaded, and the payload was remeasured. External resources remained zero and the GLB still contained one sampler.

Exact revision-10 checkpoint:

- `.blend`: 11,414,294 B · SHA256 `128979e51a507d97792ef3c15aaf9de20369e21589b60a9d13fe4d0d262d1466`;
- GLB: 9,228,876 B · SHA256 `934450fab1d9eff9dff0dc62971682a692d5f04d4d72871b9f274e6240c7e171`;
- 701 meshes / 832 nodes / 20 materials / 13 embedded images / 0 external resources;
- 20 `_colonly` collision nodes retained.

Pinned Godot 4.7.2 qualification (Actions run `34722670811`, job `103631274506`) read the imported textures back from `StandardMaterial3D` and confirmed the intended gross roles:

- steel albedo ≈ `[0.1719, 0.1831, 0.1961]`;
- ferric rust ≈ `[0.4635, 0.1423, 0.0575]`;
- union yellow ≈ `[0.8015, 0.4274, 0.0286]`;
- trim ≈ `[0.4895, 0.3661, 0.2700]`;
- steel/rust/yellow/trim retain normal maps plus roughness channel G (`1`) and metallic channel B (`2`);
- required material IDs missing: 0;
- CPU/Mesa neutral-board capture created successfully; near-black pixels ≈ 0.66%, with measurable steel/rust/yellow regions.

Godot generated 4,783,432 B of VANTA-specific import-cache files in that environment, including a 2,932,946 B imported scene. This is disk-cache evidence, **not VRAM or GPU-memory evidence**.

**CP5 payload truth after rev10:** `EMPIRICALLY_QUALIFIED_GODOT_TEXTURE_PAYLOAD_AND_GROSS_MATERIAL_ROLE_TRANSPORT`.

Evidence authority: `art_source/vanta/evidence/rev10_texture_engine_qualification.json`.

## Controlled Blender↔Godot visual-portability diagnosis

The next gate intentionally separated camera/geometry transport from shading/lighting.

### Camera and geometry alignment — PASS

The exact three neutral CP5 swatches (`VAN_CP5_NEUTRAL_STEEL`, `VAN_CP5_NEUTRAL_RUST`, `VAN_CP5_NEUTRAL_YELLOW`) were rendered in Blender and Godot as white unlit geometry over black using the same imported calibration camera.

Measured mask agreement:

- silhouette IoU: **0.98481187435**;
- exact mask pixel agreement: **0.9950347222**;
- Blender bbox: `[34, 66, 605, 243]` px;
- Godot bbox: `[35, 66, 604, 242]` px;
- centroids practically coincide.

The imported Godot camera also preserves the expected transform and FOV (`18.549795°`). Therefore the major shaded mismatch is **not** classified as a geometry, transform or camera-projection defect.

### Controlled shaded equivalence — FAIL

With the CP5 board shaded rather than unlit, the engines diverge materially:

- luminance correlation: **0.66896**;
- gradient correlation: **0.37206**;
- top-15% edge IoU: **0.3644**;
- global luminance SSIM-like score: **0.37419**;
- raw RGB MAE: **0.25074**;
- simple per-channel tone-matched MAE: **0.07029**.

Gross steel/rust/yellow roles are present in both images, but this is not close enough to claim photometric Blender↔Godot equivalence.

### Light-unit transport blocker

The isolated neutral-board experiment reduced the test to the two authored neutral point lights.

Observed source/export/import values:

| Light | Blender source power | glTF point intensity | Godot default imported energy |
|---|---:|---:|---:|
| `L_CP5_NEUTRAL_FILL` | 600 | ~47.74648 | ~47.74648 |
| `L_CP5_NEUTRAL_KEY` | 1200 | ~95.49297 | ~95.49297 |

The glTF point values are approximately `Blender power / (4π)`. Godot's default path exposes those values as `light_energy`, while the physical-intensity surface remains separate. Simply enabling Godot physical light units without an adapter made the board **more** overexposed, so the flag alone is not the repair.

The controlled isolated means also diverged strongly:

- Blender normalized mean ≈ `[0.0887, 0.0460, 0.0284]`;
- Godot legacy normalized mean ≈ `[0.2528, 0.2116, 0.1975]`;
- Godot physical-units mode without conversion ≈ `[0.7594, 0.7510, 0.7222]`.

This is consistent with an upstream glTF/Godot light-unit portability problem, not evidence that the repaired CP5 textures should be darkened or rebaked.

A reusable diagnostic/adaptation contract is now versioned at:

`art_source/vanta/pipeline/GODOT_LIGHT_TRANSPORT_CONTRACT.md`

Its physically coherent first A/B proposal for isotropic point/Omni lights is **not yet qualified**: map imported candela to Godot lumens with `lumens = candela × 4π`, set `light_energy = 1`, preserve transforms/color/range, and rerun the neutral-board comparison. Directional and spot lights require their own contracts; the point-light mapping must not be generalized blindly.

### Revision 11 interaction with CP5

Revision 11 changes source datablock sharing and adds a QA traversal spine; it does not intentionally modify the 13 CP5 payloads. The CP5 payload qualification therefore remains anchored to rev10 while the latest remote production source is rev11.

Rev11 remote provider checkpoint:

- `.blend`: 10,162,134 B · etag `12c55a03e326a0a3e4df352875d065dc`;
- GLB: 8,823,976 B · etag `86720d1b76c01894746cbded53510bc6`;
- rev11 SHA256 recovery is still pending a permitted manual native canary; no hash is inferred from provider etags.

## Current CP5 disposition

**Qualified:**

- repaired 13-image packed payload foundation;
- source→embedded GLB PNG roundtrip;
- Godot runtime texture readback and gross material roles;
- BC / roughness-G / metallic-B / normal channel semantics;
- calibration camera and three-swatch geometry alignment.

**Explicitly failed/open:**

- exact Blender↔Godot shaded/photometric equivalence;
- runtime light-unit adapter calibration;
- direct human visual/art-direction approval;
- production texel-density normalization beyond the 512² proof system;
- mip/compression quality under production target settings;
- weld/frost/grease families beyond the proof atlas;
- close/mid/far production-renderer review;
- target-hardware texture residency, draw, memory and GPU cost;
- propagation to the wider 327-target registry.

**Critical rule:** do not compensate for the light mismatch by mutating CP5 texture values. The current evidence isolates the blocker to renderer/import lighting behavior after camera/geometry and texture transport have passed their bounded tests.

Evidence authority: `art_source/vanta/evidence/rev11_dedup_route_visual_portability.json` and `art_source/vanta/pipeline/GODOT_LIGHT_TRANSPORT_CONTRACT.md`.
