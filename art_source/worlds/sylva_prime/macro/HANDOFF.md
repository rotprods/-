# HANDOFF — SYLVA PRIME MACRO FOUNDATION

AGENT: `AGENT-SYLVA-MACRO-01`  
SESSION: `20260912-SYLVA-MACRO-001`  
CLAIM: `CLM-SYLVA-MACRO-001`  
BRANCH: `art/world-sylva-prime-macro-001`  
LINEAR: `ROT-117`  
DRAFT PR: `#3`  
PRIMARY BLENDER: `05dce898-753d-4ff6-a4b0-31757dc868d8` @ revision `5`  
NORTH STAR: metre-scale, reproducible macro/regional foundation for SYLVA PRIME with explicit ownership and no invented canon.

## CURRENT TRUTH

- Primary production checkpoint: `WAVE1C_VESPER_THREE_TERRACES_R5`.
- Remote `.blend` and GLB exist at revision 5.
- Blender technical QA r5: `PASS_BLOCKOUT`.
- Human `GATE-ART`: `PENDING`.
- Exact binary recovery/native engine import/traversal: `ENV_BLOCKED / NOT_RUN`.
- Target hardware/performance: unresolved.
- Planetary-scale Option C exists only as `PROPOSAL_PENDING_CREATIVE_DIRECTOR`; no canon promotion occurred.
- Claim status: `KEEP / CHECKPOINT`.

## OWNERSHIP

### This claim owns
- km-scale local terrain and canonical regional placement;
- macro diagnostic root topology;
- macro traversal corridors;
- streaming metadata/envelopes;
- macro collision proxies;
- typed root-kit integration sockets;
- Cámara de VESPER macro encounter layout;
- reversible L0/L1 planetary-scale decision artifacts.

### PR #6 / `CLM-SYLVA-PROC-NROOT-001` owns
- reusable A1/A2/A3/B1/B2/C1/C2/C3 neural-root modules;
- meso route/callus surfaces;
- module material interfaces;
- per-module collision proxies.

Hard boundary: this claim contains **0 provider root-kit meshes**.

## DONE / EVIDENCE

### r1–r4 foundation
- 12 km local terrain proposal;
- three canonical regional foundations;
- 6 primary + 8 secondary diagnostic macro roots;
- Puerto/Bosque/VESPER blockout language;
- four route guides;
- portable lights and review cameras;
- 16 proposed 3 km streaming cells;
- 3 regional hero-zone envelopes;
- 8 provider sockets;
- low-res terrain + route/region collision interfaces.

### r5 VESPER canon correction
The old single circular arena proxy was removed because canon requires three terraces connected by wide roots.

Created:
- `SYLVA_VESPER_Terrace_00_ENTRY` — 116 m diameter / z −246;
- `SYLVA_VESPER_Terrace_01_MIDDLE` — 124 m / z −216;
- `SYLVA_VESPER_Terrace_02_UPPER` — 112 m / z −184;
- `SYLVA_VESPER_TerraceConnector_00` — 142.215 m / 12.178° / 18 m visible / 16 m collision;
- `SYLVA_VESPER_TerraceConnector_01` — 145.685 m / 12.689° / 18 m visible / 16 m collision;
- five dedicated VESPER collision proxies;
- `precision_jump_required=false` on both connectors.

r5 QA:
- 148 objects;
- 95 meshes;
- 8 curves;
- ~18,240 triangles;
- 3 terraces / 2 connectors / 12 total macro collision nodes;
- 0 legacy arena-floor nodes;
- 0 non-unit scales;
- 0 namespace violations;
- 0 provider meshes;
- 0 final VESPER meshes;
- `pass=true`.

r5 remote artifacts:
- `.blend`: 2,290,409 bytes / etag `2ccbc1ec2ffd854ae83b5cee197d16de`;
- GLB: 1,215,672 bytes / etag `9c288dd826d7cbc3331b849dda1590e5`;
- review PNG artifact `33a52a26511ad4a5e38646eb55cb23a9`.

r5 file-backed VESPER smoke:
- 320×180;
- 81,344 bytes;
- mean RGB ~0.21138;
- variance ~0.02917;
- nonblank `true`.

Signal PASS is not human art approval.

## REPRODUCIBLE SOURCE ORDER

1. `generate_sylva_macro.py`
2. `add_sylva_macro_interfaces.py`
3. `add_vesper_three_terraces.py`

Integration tools:
- `IMPORT_CONTRACT.md` — current r5 naming/import contract;
- `validate_glb_contract.py` — current r5 pure-stdlib pre-import validator.

R5 validator adversarial receipt:
- `qa/GLB_CONTRACT_SELFTEST_R5.json`;
- 7/7 synthetic contract cases pass;
- explicitly rejects a simulated r4 single-floor arena export.

## TRAVERSAL-SCALE FINDING

Four macro route guides total **7,927.391 m**.

Repository gameplay code currently uses:
- 6 m/s normal on foot;
- 3 m/s guarding;
- 20 m/s generic vehicle state.

Sylva canon includes `Vela de Ceniza con agarres de canopy`. Do not shrink the world automatically. Future pacing should separate local pedestrian loops from macro transit/vehicle corridors and be tested in engine.

## PLANETARY SCALE DECISION PACKAGE

Files:
- `ADR-001_PLANETARY_SCALE_PROPOSAL.md`
- `planetary_scale_options.json`

Recommended proposal only: Option C / `1.20 R⊕`, constrained to preserve documented `1.12 g` under the stated bulk approximation. `canonicalized=false`.

Separate orbital remote created **empty only**:
- project `c796230b-0463-4e17-9446-2e746c5c4933`;
- revision `0`;
- generator `generate_orbital_scale_proposal_c.py` exists but has **not been executed**;
- do not mutate until fleet registry explicitly includes this project ID.

## FLEET STATE

Current branch incorporated fleet harness from `main@f78bfdc8bd7b2f6ab52b45d39babcc1589ab3918` using one-way PR #19.

Producer communications:
- epoch-1 ACK: issue #7 comment `5648367024`;
- empty orbital-project registration request: `5648418266`.

Last registry readback still showed this claim `reserved` with `ack:null`. Producer must not edit `ops/fleet/registry.json`; wait for integrator publication.

Requested path expansion still pending for macro production manifest/receipt paths. Therefore current r5 receipt is kept under the already-reserved `art_source/worlds/sylva_prime/macro/qa/` path.

## BLOCKED

### BLOCK-SYLVA-001 — planetary canon promotion
- Option C is a proposal, not authority.
- Needs explicit creative/integrator decision.
- Local L2–L4 work remains independent.

### BLOCK-SYLVA-002 — target performance envelope
- Needs engine + target hardware/preset.
- No final triangle/material/draw/LOD/HLOD budget claim.

### BLOCK-SYLVA-003 — binary recovery / runtime
- Higgsfield resolves exact remote artifacts.
- Current sandbox cannot recover signed bytes due network/DNS/safe-download restrictions.
- Pinned Godot 4.7.2 is not locally present.
- Classification: `ENV_BLOCKED`, not asset/engine FAIL.

## NEXT 3 ACTIONS

1. Re-read `main` fleet registry. If producer ACK/path expansion/orbital project ID are published, update local claim metadata and only then mutate the orbital proposal remote.
2. On a host with artifact access, recover exact r5 `.blend` + GLB, run `validate_glb_contract.py` against the exact SHA-256, import with pinned Godot 4.7.2 and traverse Puerto → Bosque → all three VESPER terraces.
3. Run human art review of the r5 interactive scene. Convert every rejection into an atomic task; do not mark art DONE from render signal alone.

CLAIM STATUS: `KEEP / CHECKPOINT`
