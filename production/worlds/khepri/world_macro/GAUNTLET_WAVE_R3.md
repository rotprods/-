# KHEPRI World Macro — Gauntlet Wave R3

**Claim:** `CLM-KHEPRI-WMACRO-001`  
**Master project:** `040f0c45-83a7-483c-9ee7-1e31c640a587`  
**Master revision:** `3`  
**Cold project:** `4c01fdbb-7093-4229-9a49-8237583280bc` rev `2` after generator+optimizer  
**Main observed:** `f78bfdc8bd7b2f6ab52b45d39babcc1589ab3918`

## RETROSPECT / ATTACK
Machine visual audit of rev2 found two real defects:
1. overview/gameplay cameras used Blender default `clip_end=1000 m` while route evidence spans 2–8 km;
2. the 1.85 m human scale guide was outside gameplay camera frame.

## IMPLEMENT
- overview: 32 mm, clip end 12,000 m;
- gameplay: 38 mm, clip end 8,000 m;
- QA human guide: 30 m forward on gameplay view axis;
- generator and validator updated so these values are contractual, not manual scene patches;
- scene metadata rebound to fleet-qualified main SHA.

## VERIFY
`khepri.validator.r3` => `structural_and_machine_visual_pass=true`.

- 77 objects / 6 meshes / 5 materials / 1 curve;
- 5,697 unique mesh vertices / 11,092 triangles;
- terrain `6400 × 4800 × 228.805 m`;
- all four route anchors in overview frame and clip range;
- farthest anchor: 8,095.8 m, overview clip end 12,000 m;
- human guide: 1.85 m, gameplay NDC bbox `[0.4896, 0.6030, 0.5105, 0.7206]`, projected height 84.7 px at 720p;
- zero duplicate names/asset IDs, invalid transforms, negative scales or non-unit mesh scales.

## COLD REBUILD
A new private Blender project rebuilt the updated scene and optimizer from clean state.

Master r3 and cold optimized rev2 both produce:
- `.blend`: 1,357,838 B;
- GLB: 703,040 B;
- semantic scene fingerprint: `7d80db30181cde1bded58d357384095c07cce0d2ca65e1b728b841aa93b252ca`.

Binary etags differ and binary identity is not claimed. The fingerprint canonicalizes irrelevant UV-sphere vertex index ordering while retaining actual geometry, face geometry, transforms, materials, metadata, camera lens and clipping ranges.

## CURRENT GATES
PASS:
- CANON boundary for this claim;
- structural geometry/scale;
- instancing optimization;
- machine-readable visual framing/clip gate;
- clean-project semantic reproducibility;
- portable provider GLB export.

OPEN:
- human GATE-ART;
- local/repo binary recovery + fleet delivery receipt;
- producer branch reconciliation against current main + exact MANIFEST + PR CI;
- engine import/collision/streaming;
- target-GPU performance.

**Stop condition:** no further content density until the producer reconciliation P0 is closed or explicitly delegated by the fleet integrator.
