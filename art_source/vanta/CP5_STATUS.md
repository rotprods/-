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

## Revision 9 defect discovery — packed did not mean valid

A deeper pixel audit invalidated the earlier assumption that “13/13 packed” implied usable texture content. All thirteen revision-9 CP5 image datablocks — BC, ORM, normal and decal — read back as black payloads. Godot was transporting that bad source faithfully. This negative receipt is preserved; it is not rewritten as an importer failure.

The sampler warning was separately audited and was **not** evidence of conflicting sampler policies: every CP5 image used the same Blender sampler settings and the exported glTF contained one sampler (`LINEAR` / trilinear mip filtering, default repeat wrapping). Material topology remained conventional: BC→Base Color, ORM G→Roughness, ORM B→Metallic, tangent normal→Normal.

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

Godot generated 4,783,432 B of VANTA-specific import-cache files in this environment (including a 2,932,946 B `.scn`). This is a disk-cache observation, **not VRAM or GPU memory**.

**CP5 truth after rev10:** `EMPIRICALLY_QUALIFIED_GODOT_TEXTURE_PAYLOAD_AND_GROSS_MATERIAL_ROLE_TRANSPORT`. Source→embedded GLB payload→Godot texture readback and gross role separation are qualified. Human visual/art-direction approval, exact photometric equivalence, mip quality under production settings and target-GPU cost remain open.

Evidence authority: `art_source/vanta/evidence/rev10_texture_engine_qualification.json`.
