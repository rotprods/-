# STATUS — CLM-SYLVA-MACRO-001

**Agent:** `AGENT-SYLVA-MACRO-01`  
**Session:** `20260912-SYLVA-MACRO-001`  
**Branch:** `art/world-sylva-prime-macro-001`  
**Primary remote Blender:** `05dce898-753d-4ff6-a4b0-31757dc868d8` @ revision `5`  
**State:** `IN_PROGRESS / VERIFIED R5 CHECKPOINT`

## Scope boundary

Owned here:
- km-scale local terrain foundation;
- canonical region anchors and spatial relationships;
- diagnostic macro-root topology placement;
- macro traversal corridors;
- streaming metadata/envelopes;
- macro collision proxies;
- typed sockets consuming `CLM-SYLVA-PROC-NROOT-001`;
- Cámara de VESPER macro encounter-layout envelope;
- L0/L1 planetary-scale decision package, but **not canon promotion**.

Explicitly not owned:
- reusable meso neural-root modules (PR #6);
- final VESPER;
- NPC/fauna/vegetation production assets;
- final architecture/interiors;
- gameplay/quest/runtime code;
- final engine/performance decision.

## Current coverage

| Task | Priority | State | Evidence |
|---|---|---|---|
| Evidence / authority / claim | P0 | DONE | claim + PR #3 + issue #7 + ROT-117 |
| Metric coordinate contract | P0 | DONE | Blender metadata / World Bible |
| Macro terrain | P0 | DONE_BLOCKOUT | r5 source lineage |
| Structural macro-root topology | P0 | REVIEW | 6 primary + 8 secondary diagnostic roots; meso kit delegated |
| Puerto del Injerto foundation | P1 | REVIEW | blockout + collision + provider sockets |
| Bosque de las Frases foundation | P1 | REVIEW | 3 route languages + collision + provider sockets |
| Cámara de VESPER macro layout | P0 | **PASS_BLOCKOUT_R5** | three terraces + two wide connectors + separate collision |
| Streaming interface | P0 | DONE_PROPOSAL | 16 × 3 km L3 cells + 3 regional envelopes |
| Root-kit interface | P0 | PASS | 8 typed sockets / 0 provider meshes copied |
| GLB pre-import contract | P0 | PASS_SELFTEST | r5 validator 7/7 synthetic adversarial cases |
| Binary recovery / engine import | P0 | ENV_BLOCKED | `qa/ENGINE_IMPORT_ENV_BLOCKER.json` |
| Human art review | P0 | PENDING | interactive r5 scene available |
| LOD/HLOD / target performance | P1 | BLOCKED | engine + hardware unresolved |

## R5 scene receipts

Remote project `05dce898-753d-4ff6-a4b0-31757dc868d8`, revision 5:

- **148 objects**;
- **95 mesh objects**;
- **8 curves**;
- **~18,240 blockout triangles**;
- local authored terrain **12,000 × 12,000 m** (`PROPOSAL`, never planet size);
- 6 primary + 8 secondary diagnostic macro roots;
- 4 macro traversal guides, total guide length **7,927.391 m**;
- 16 proposed L3 streaming cells at 3 km;
- 3 proposed L4 regional envelopes;
- 8 typed root-kit sockets;
- **12** macro collision nodes total;
- non-unit scales: **0**;
- non-`SYLVA_` objects: **0**;
- provider root-kit meshes copied: **0**;
- final VESPER meshes: **0**.

### Cámara de VESPER r5 canon correction

The previous single circular proxy arena was removed. Required macro layout now exists:

- `SYLVA_VESPER_Terrace_00_ENTRY`: 116 m diameter, z −246 m;
- `SYLVA_VESPER_Terrace_01_MIDDLE`: 124 m diameter, z −216 m;
- `SYLVA_VESPER_Terrace_02_UPPER`: 112 m diameter, z −184 m;
- Connector 00: 142.215 m, 12.178°, 18 m visual / 16 m collision width;
- Connector 01: 145.685 m, 12.689°, 18 m visual / 16 m collision width;
- both connectors: `precision_jump_required=false`.

Receipt: `qa/R5_VESPER_CANON_LAYOUT.json`.

## Remote artifacts r5

- `.blend`: **2,290,409 bytes**, etag `2ccbc1ec2ffd854ae83b5cee197d16de`.
- GLB: **1,215,672 bytes**, etag `9c288dd826d7cbc3331b849dda1590e5`.
- VESPER r5 review PNG artifact: `33a52a26511ad4a5e38646eb55cb23a9`.
- GLB export completed without unsupported-light warnings.

## Visual signal QA

File-backed VESPER r5 smoke, 320×180:
- PNG: 81,344 bytes;
- mean RGB: ~0.21138;
- variance: ~0.02917;
- max RGB: ~0.59216;
- result: `PASS_NONBLANK`.

This proves image signal only. `GATE-ART` remains pending human review.

## GLB contract r5

`validate_glb_contract.py` now requires:
- 3 VESPER terrace nodes;
- 2 VESPER connector nodes;
- 5 VESPER collision nodes;
- 12 `SYLVA_COL_*` nodes total;
- no legacy `SYLVA_VESPER_ProxyArenaFloor` / `SYLVA_COL_VESPER_ArenaFloor`.

Adversarial synthetic gauntlet: **7/7 PASS**, including rejection of a simulated r4 single-floor arena export. The actual r5 GLB still requires byte recovery and execution of the validator against its exact SHA-256.

## Traversal scale finding

The four diagnostic route guides total **7.927 km**. Current prototype movement is 6 m/s on foot, 3 m/s guarding and 20 m/s in its generic vehicle state. Canon also specifies Sylva's `Vela de Ceniza con agarres de canopy`.

Interpretation: do **not** automatically compress the macro world. Future pacing should distinguish local pedestrian loops from macro vehicle/transit corridors and be validated in engine.

## Planetary-scale decision package

Physical radius/diameter remain unapproved canon. A reversible ADR now exists:
- `ADR-001_PLANETARY_SCALE_PROPOSAL.md`
- `planetary_scale_options.json`

Recommended proposal only: `SYL_SCALE_C_BROAD_BIOGENIC`, 1.20 R⊕, preserving the documented 1.12 g target under a spherical bulk approximation. `canonicalized=false`.

A separate orbital Blender project was created **empty only**:
`c796230b-0463-4e17-9446-2e746c5c4933` @ revision 0.

It must remain unmodified until the fleet integrator adds that project ID to the active reservation. Generator exists but has not been executed: `generate_orbital_scale_proposal_c.py`.

## Fleet governance

- Branch incorporated `main@f78bfdc8bd7b2f6ab52b45d39babcc1589ab3918` via one-way sync PR #19.
- Producer ACK epoch 1 posted to issue #7: comment `5648367024`.
- Additional empty orbital project registration request: comment `5648418266`.
- Latest readback still showed the producer claim as `reserved` / `ack:null`; producer must not mutate `ops/fleet/registry.json`.
- Requested registry path expansion for macro manifest/r5 delivery receipts is still awaiting integrator publication.

## Open P0

1. Integrator readback: claim active ACK + path expansion + orbital project ID.
2. Recover exact r5 `.blend` + GLB into a delivery checkout.
3. Run r5 GLB validator on exact recovered bytes and bind SHA-256.
4. Import into pinned Godot 4.7.2/current executable runtime.
5. Traverse Puerto → Bosque → all three VESPER terraces with normal controls/collision.
6. Human art-direction review.
7. Explicit creative decision before promoting any planetary radius.

## Gates

| Gate | State |
|---|---|
| CANON regional layout | PASS_BLOCKOUT |
| PLANETARY SIZE | PROPOSAL_PENDING_DECISION |
| OWNERSHIP / SHARD | PASS_LOCAL; FLEET ACK READBACK PENDING |
| GEOMETRY / NAMESPACE / SCALE | PASS_BLOCKOUT_R5 |
| VESPER THREE-TERRACE LAYOUT | PASS_BLOCKOUT_R5 |
| STREAMING INTERFACE | PASS_PROPOSAL |
| ROOT-KIT SOCKET CONTRACT | PASS |
| COLLISION PROXY PRESENCE | PASS_BLOCKOUT |
| GLB CONTRACT LOGIC | PASS_SELFTEST_7_OF_7 |
| EXPORT | PASS_REMOTE_GLB |
| EDITABLE SOURCE | PASS_REMOTE_BLEND |
| BINARY RECOVERY | ENV_BLOCKED |
| ART | PENDING_HUMAN_REVIEW |
| ENGINE IMPORT | NOT_RUN |
| GAMEPLAY TRAVERSAL / COLLISION | NOT_RUN |
| LOD/HLOD | NOT_IMPLEMENTED |
| PERFORMANCE | BLOCKED_TARGET_HARDWARE |

## Claim

`KEEP / CHECKPOINT` — materially advanced and technically coherent, but not DONE and not merge-ready as final world art.
