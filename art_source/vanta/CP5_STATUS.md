# VANTA CP5 — Material / Trim / Decal Foundation

**World:** VANTA  
**Latest validated revision:** 8  
**Truth level:** `LOCALLY_VALIDATED_MATERIAL_FOUNDATION` — not engine-material-qualified and not final-art approved.

## Revision 7 — packed PBR role materials

The initial CP5 packing path failed validation and committed nothing. The replacement pipeline writes backing PNGs, reloads them and packs them into the `.blend` before accepting the mutation.

`vanta-cp5-pbr-textures-002` produced nine packed 512×512 maps:

- `T_VAN_CP5_STEEL_{BC,ORM,N}`
- `T_VAN_CP5_RUST_{BC,ORM,N}`
- `T_VAN_CP5_YELLOW_{BC,ORM,N}`

Material roles upgraded in place:

- `M_VAN_CP4_STEEL`
- `M_VAN_CP4_RUST`
- `M_VAN_CP4_UNION_YELLOW`

Conventions:

- BC = sRGB base color;
- ORM = Non-Color, `R=AO`, `G=roughness`, `B=metallic`;
- N = Non-Color tangent normal.

Coverage:

- 147 CP4 render meshes use these three material roles;
- 147/147 have UVs;
- missing UV count = 0.

Revision 7 source:

- `.blend` 7,557,149 B · etag `593e9b598b8c83ab8aa9866456648f28`
- GLB 5,429,352 B · etag `3e86b6ae502410d6c629d2e82d3561ed`

## Revision 8 — first trim sheet + decal atlas

`vanta-cp5-trim-decal-001` added:

### Trim A

- `T_VAN_CP5_TRIM_A_BC`
- `T_VAN_CP5_TRIM_A_ORM`
- `T_VAN_CP5_TRIM_A_N`
- `M_VAN_CP5_TRIM_A`

Current proof bands:

- U 0.00–0.30: rolled steel;
- U 0.30–0.55: ferric rust;
- U 0.55–0.80: union-yellow paint;
- U 0.80–1.00: detail band.

### Decal Atlas A

- `T_VAN_CP5_DECAL_A`
- `M_VAN_CP5_DECAL_A`

2×2 proof quadrants:

1. industrial hazard stripe;
2. cyan polarity/field glyph;
3. worker ownership bands;
4. impact ring and radial cracks.

Representative cards are placed on the storm shelter, magnetic anchor, crane and drydock rib.

### Calibration scene

- 12 CP5 calibration objects;
- neutral board and Vanta-light board;
- cameras `CAM_CP5_NEUTRAL_BOARD` and `CAM_CP5_VANTA_BOARD`;
- neutral and warm/cyan motivated-light pairs.

Revision 8 source:

- `.blend` 8,168,427 B · etag `251f6d510f8ae6c5250bae10c8ee5a61`
- GLB 5,990,788 B · etag `a3cfe2daf6a1005e35db478e3f4ec51d`

## Revision-8 QA

`vanta-rev8-final-audit-001` passes:

- scene: 832 objects / 711 meshes / 20 materials / 25 collections / 12 cameras / 15 lights;
- **13/13 CP5 images packed**;
- every CP5 image is 512×512;
- BC/decal images use sRGB;
- ORM/normal images use Non-Color;
- 147 textured CP4 meshes;
- zero UV misses;
- no regression of the CP4 parent-transform fix;
- no regression of the CP4 zero-gap test yard.

Neutral-board render execution proof:

- `vanta_cp5_neutral_board.png`
- artifact `a2438a37035038ca58e40a4ff27176d7`
- 640×480
- 244,743 B

This is render evidence, **not** visual/aesthetic approval.

## Known export blockers / warnings

GLB generation succeeds but is not yet an engine-material PASS:

- Blender glTF reports that multiple image texture nodes participate in some PBR/trim materials and sampler behavior may follow the first image node;
- Blender glTF reports unsupported AREA lights from the test yard.

Therefore:

- GLB existence = `implemented`;
- correct target-engine PBR binding = `unqualified`;
- target-engine light equivalence = `unqualified`.

## CP5 disposition

**Implemented + locally validated:**

- packed deterministic PBR foundation for steel/rust/yellow;
- packed first trim family;
- packed first decal atlas;
- UV coverage on the representative CP4 slice;
- neutral/Vanta calibration geometry and cameras;
- isolated render execution.

**Open:**

- direct visual/art-direction approval;
- production texel-density normalization;
- weld/frost/grease families beyond current proof atlas;
- mip/compression policy on target engine;
- target-engine PBR import/binding verification;
- close/mid/far material review in engine;
- target-hardware memory/GPU cost;
- propagation to the wider 327-target registry.

**Next gate:** qualify material import semantics in the target engine and run close/mid/far + collision/performance review on the CP4 vertical slice before mass propagation.

Evidence: `art_source/vanta/evidence/remote_blender_rev8.json`.
