# ORIGIN / Archivo production authority

Current cold-rebuild sequence for the Archivo source/assembly system:

1. `origin_archive_x100_wave1.py` — 21 stable structural assets and source collision proxies.
2. `../tech/origin_lod_x100_wave2.py` — authored LOD1/LOD2 geometry.
3. `origin_archive_traversable_x100_wave4.py` — **current authoritative assembly grammar and collision semantics**.

`origin_archive_grammar_x100_wave2.py` is retained only as historical Wave02 evidence. Do not use it to rebuild the current assemblies: 2026-09-15 QA proved that its persisted state was not equivalent to the remote rev6 state and that the rev6 grammar was not traversal-ready.

Wave04 preserves the four stable assembly IDs but changes proposal layout, instancing math and collision topology. Final dimensions remain `PROPOSAL_UNTIL_GODOT` until `CLM-ORIGIN-ARCH-ARCHIVE-NATIVE-001` passes against the exact GLB.
