# ORIGIN X100 Wave 02 — native-integration checkpoint

This file intentionally exists as a stable marker for the next P0 gate.

Gate: `REAL_GLB_IMPORT_GODOT_4_7_2`

Inputs:
- Atrio project `6e64cd59-f1f6-461f-850c-737d098f1723` revision 6.
- Archivo project `9bff5b6c-35a5-4db9-92de-4008a0fc3f4e` revision 6.

Required evidence before PASS:
1. Godot 4.7.2 imports both exact GLBs.
2. Imported PackedScenes instantiate headlessly.
3. Stable ORIGIN naming survives import sufficiently for runtime selection/QA.
4. Mesh/material/scale readback is recorded.
5. Imported collision geometry is used for a real physics/traversal gate or the missing importer contract is recorded as a blocker.
6. LOD switching / packing remains separate from mere presence of LOD meshes.

No PASS is implied by this marker itself.
