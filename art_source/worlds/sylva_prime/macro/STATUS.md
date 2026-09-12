# STATUS — CLM-SYLVA-MACRO-001

**Agent:** `AGENT-SYLVA-MACRO-01`  
**Branch:** `art/world-sylva-prime-macro-001`  
**Primary Blender:** `05dce898-753d-4ff6-a4b0-31757dc868d8` @ revision `6`  
**State:** `IN_PROGRESS / VERIFIED R6 CHECKPOINT`  
**Claim:** `KEEP / CHECKPOINT`

## Current production truth

R6 is a macro/regional **blockout + integration foundation**, not final world art.

Owned here:
- 12 km local authored terrain proposal and macro topography;
- canonical region anchors/spatial relationships;
- diagnostic structural-root topology;
- traversal corridors;
- streaming envelopes/metadata;
- macro collision proxies;
- typed sockets to `CLM-SYLVA-PROC-NROOT-001`;
- Cámara de VESPER macro encounter layout;
- reversible L0/L1 planetary-scale decision artifacts.

Excluded:
- reusable meso root kit (PR #6);
- final VESPER/NPC/fauna/vegetation/architecture;
- gameplay/quest code;
- final materials/LOD/HLOD/performance qualification;
- planetary canon promotion.

## Wave progression

- **r1:** local terrain + 3 region foundations + macro-root topology.
- **r2:** portable lighting + review cameras.
- **r3:** camera-range correction + validated nonblank file-backed render smoke.
- **r4:** 16 streaming cells + 3 region envelopes + 8 provider sockets + collision interfaces.
- **r5:** canon correction: replace single VESPER arena floor with 3 terraces + 2 wide connectors.
- **r6:** replace sine/cosine blockout terrain with deterministic causal macro model shared by render and collision.

## R6 scene metrics

- objects: **149** (r6 terrain metadata adds one scene node over r5);
- render terrain: **2,401 vertices / 2,304 faces / 4,608 tris**;
- collision terrain: **33×33 = 1,089 vertices / 1,024 faces / 2,048 tris**;
- terrain z: **−310.617 m → 519.258 m**;
- root-bearing macro ridges: **6**;
- drainage/catchment shaping hypotheses: **2**, explicitly `PROPOSAL_NOT_CANON_WATERWAYS`;
- 16 proposed L3 streaming cells;
- 3 regional L4 envelopes;
- 8 typed provider sockets;
- 12 macro collision nodes;
- 3 VESPER terraces + 2 connectors;
- final VESPER meshes: **0**;
- provider root-kit meshes copied: **0**.

### Terrain causality / consistency

Model: `R6_BIOGEO_CAUSAL_MACRO_V1`.

Render and collision are generated from the exact same deterministic height function:
- common comparison samples: **289**;
- max render↔collision height delta: **0 m**;
- mean delta: **0 m**.

Measured terrain face slopes:
- median: **4.939°**;
- p90: **14.186°**;
- p95: **20.297°**;
- max: **51.231°**.

Macro route grades:
- Route 00: 1,913.113 m @ **2.996°**;
- Route 01: 2,085.402 m @ **2.199°**;
- Route 02: 1,930.026 m @ **1.484°**;
- Route 03: 1,998.850 m @ **15.079°**.

Route 03 must be validated with the real controller/camera before gameplay approval.

## VESPER r5/r6 retained contract

- 3 terraces: 116 m / 124 m / 112 m diameter;
- connector 00: 142.215 m @ 12.178°;
- connector 01: 145.685 m @ 12.689°;
- 18 m visual / 16 m collision width;
- no precision jump required;
- obsolete single-floor arena nodes absent.

## Remote r6 artifacts

- `.blend`: **2,348,647 bytes**, etag `f82350b275ed699a790d7977be3a1ee1`.
- GLB: **1,299,444 bytes**, etag `896ae5e1b86cc5874f008872c05235a7`.
- master terrain review PNG artifact: `8f6c2c0d249577bd9d4e586b6b62145c`.

Master file-backed render smoke 320×180:
- PNG: 90,828 bytes;
- mean RGB ~0.32490;
- variance ~0.06411;
- max RGB ~0.78431;
- `PASS_NONBLANK`.

This proves render signal only; human art approval remains pending.

## Reproducible build chain

1. `generate_sylva_macro.py`
2. `add_sylva_macro_interfaces.py`
3. `add_vesper_three_terraces.py`
4. `refine_macro_terrain_r6.py`

Integration/QA:
- `IMPORT_CONTRACT.md`
- `validate_glb_contract.py` — r5 node contract, still applicable to r6 because r6 changes terrain data, not required node IDs.
- `qa/GLB_CONTRACT_SELFTEST_R5.json` — 7/7 synthetic adversarial cases.
- `qa/R5_VESPER_CANON_LAYOUT.json`
- `qa/R6_TERRAIN_CAUSALITY.json`
- `qa/ENGINE_IMPORT_ENV_BLOCKER.json`

## Planetary scale

`ADR-001_PLANETARY_SCALE_PROPOSAL.md` recommends Option C / 1.20 R⊕ as a reversible design proposal preserving the documented 1.12 g bulk target. It is **not canon**.

Orbital project `c796230b-0463-4e17-9446-2e746c5c4933` remains **empty revision 0** and must not be mutated until fleet registry readback includes that project ID.

## Fleet state

- branch synced with `main@f78bfdc8bd7b2f6ab52b45d39babcc1589ab3918`;
- latest compare before r6 work: 36 ahead / 0 behind;
- producer ACK issue #7 comment `5648367024`;
- orbital registration request `5648418266`;
- latest main registry still showed claim `reserved` / `ack:null`;
- producer does not edit `ops/fleet/registry.json`.

## Open P0

1. Fleet integrator ACK/path/project-ID readback.
2. Recover exact r6 `.blend` + GLB to a delivery checkout.
3. Run GLB validator against exact recovered r6 bytes and bind SHA-256.
4. Import into pinned Godot 4.7.2/current runtime.
5. Traverse Puerto → Bosque → all VESPER terraces; specifically attack the 15.079° final macro route and connector transitions.
6. Human art-direction review.
7. Explicit decision before planetary-scale promotion.

## Gates

| Gate | State |
|---|---|
| Regional canon / VESPER layout | PASS_BLOCKOUT_R6 |
| Terrain render↔collision consistency | PASS_R6 |
| Namespace / unit transforms | PASS_R6 |
| Root-kit ownership boundary | PASS |
| Streaming/collision interfaces | PASS_PROPOSAL |
| GLB contract logic | PASS_SELFTEST_7_OF_7 |
| Remote export/editable source | PASS |
| Binary recovery | ENV_BLOCKED |
| Engine import/traversal | NOT_RUN |
| Human art review | PENDING |
| LOD/HLOD/performance | BLOCKED |
| Planet radius canon | PROPOSAL_PENDING_DECISION |
