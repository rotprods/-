# ORIGIN — REAL_GLB_IMPORT_GODOT_4_7_2

Status: **PASS**
Qualified: 2026-09-14

Canonical receipt:
`production/receipts/origin/ORIGIN-REAL-GLB-GODOT-001.yaml`

Qualified exact inputs:
- Atrio project `6e64cd59-f1f6-461f-850c-737d098f1723` revision **8**.
- Archivo project `9bff5b6c-35a5-4db9-92de-4008a0fc3f4e` revision **6**.

Godot 4.7.2 official imported both GLBs as PackedScenes. Stable LOD and assembly structure survived import. Nineteen imported Atrio `COL_*` meshes were converted into real `StaticBody3D` trimesh collision and a real `CharacterBody3D` capsule passed inner/outer landing and radial traversal from r=11 m beyond the r=37 m support target.

Evidence: run `34831105389`, job `103934408512`, SUCCESS.

The prior rev6 canary imported successfully but failed physics at r≈19.06 m due to a closed ring proxy internal wall. Rev8 converts the nine ring proxies to upward-facing walkable top surfaces; the same acceptance harness then passes.

This PASS does **not** imply engine runtime LOD switching/HLOD, Archive assembly traversal, local-gravity gameplay, target-hardware performance or human `GATE-ART`.
