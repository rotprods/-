# ART-ELYSIUM-001 — COLD RESUME HANDOFF

Date: 2026-09-12
World: `elysium` / ELYSIUM NULL
Ownership: `WORLD_OWNER`
Branch: `art/world-elysium-null-001`
Draft integration PR: `#15`
Linear: `ROT-116` · In Progress
Claim: **KEEP / ACTIVE**
Owned path: `art_source/worlds/elysium_null/**`
Initial base main: `4c2fa044080004609ea6df45f34b2a784536507a`
Ownership-policy main observed during resync: `196ef814fdc845ec797979906d01dc25009217c7`
Remote Blender project: `00152eea-2da0-40ec-8666-78d6764c718f`
Current qualified Blender revision: **6**

---

## NORTH STAR

Build ELYSIUM NULL as a physically coherent, modular and recoverable world-scale artificial habitat whose controlled perfection is communicated by construction, circulation, maintained ecology, state changes and rare causal human anomalies rather than generic white sci-fi decoration.

---

# COORDINATION TRUTH

- Current `AGENTS.md` mandatory ownership preflight was re-read after `main` advanced.
- Coordination issue #7 was re-read.
- All live branches and relevant world-art PRs were re-fetched before continuing the significant production wave.
- ELYSIUM NULL remains represented by exactly one full-world owner branch: `art/world-elysium-null-001`.
- Draft PR #15 and Linear `ROT-116` point to this owner.
- Any future parallel work inside ELYSIUM requires an explicit `ATOMIC_SUBCLAIM` with asset IDs/collections/exclusions; do not create a second world branch.

---

# CANON BOUNDARY

Recovered canon retained:

- artificial world-scale habitat, **not a natural planet**;
- Alba Nula / EL UMBRAL;
- 1.00 g / 21 °C;
- Los Custodios Vacíos;
- Avenida del Recibimiento / Casas sin Desgaste / Jardín de EDEN;
- boss EDEN;
- EDEN arena exactly **48 m diameter**;
- `Reubicación` destination warning **1.5 s**.

Total habitat diameter/radius remains unresolved. Do not invent a natural-planet radius.

---

# IMPLEMENTED / VERIFIED CHECKPOINTS

## R1 — W0 foundation

- metric `1 BU = 1 m`;
- 1.85 m human scale witness;
- 260 × 72 m representative Avenida cell proposal;
- repeated white arcology massing and maintained gardens;
- Tranvía custodio proxy;
- exact 48 m EDEN arena;
- localized repaired-human-trace prop;
- 153 objects / 149 meshes / 9 material roles;
- 4,724 source vertices / 5,618 source polygons;
- editable `.blend`, GLB and preview.

Two bootstrap failures before R1 are preserved in `evidence/foundation_validation.json`; neither committed a scene revision.

## R2 — W1 architecture grammar candidate

- 1 m planning-grid proposal;
- 4 m primary-bay proposal;
- 8 / 12 / 16 m span family;
- 0.4 × 0.4 × 4 m column prototype;
- 4 × 4 × 0.24 m solid panel prototype;
- 3.8 × 3.6 × 0.24 m shared façade tile;
- 2.4 × 2.7 m clear-door proposal;
- 32 deployed arrival façades share one prototype mesh; 33 mesh users including prototype.

## R3 — EDEN spatial state graph

- explicit layouts A/B/C;
- 12 state target transforms;
- 16 visible State-B destination-footprint bars;
- four 8 × 8 m proposal modules all remain within canonical 24 m arena radius;
- candidate minimum axis corridor: 6 m;
- arena/state metadata embedded in Blender.

## Runtime-clearance static audit

Current executable prototype values recovered from `main@196ef814...`:

Player:
- capsule radius `0.38 m`;
- diameter `0.76 m`;
- height `1.85 m`.

Standard enemy:
- radius `0.40 m`;
- diameter `0.80 m`;
- height `1.80 m`.

Current prototype boss:
- radius `1.10 m`;
- diameter `2.20 m`;
- height `5.80 m`.

Architecture candidate door `2.4 × 2.7 m` against player:
- total horizontal slack `1.64 m`;
- centered per-side slack `0.82 m`;
- vertical headroom `0.85 m`.

Truth state: `PASS_STATIC_GEOMETRY_ONLY`. Native traversal/camera/dodge clearance remains pending. Current boss is intentionally not human-door traversable.

## R4/R5 — EDEN movement + collision contract

R4 introduced:
- four kinematic module roots;
- eight separate collision proxies;
- 16 physical mechanism objects;
- 2-axis linear actuator sled + orthogonal subfloor rails candidate;
- canonical 1.5 s warning represented as 36 frames at 24 fps;
- separate 1.0 s / 24-frame movement duration **PROPOSAL**.

One animation bootstrap attempt failed before commit because Blender 5.2 did not expose `Action.fcurves` as expected.

R4 structural QA then found a real committed hierarchy defect: visible garden meshes were double-transformed after parenting while collision roots moved correctly.

R5 fixed all moving children with explicit local coordinates. Verification at State A and State B showed all four visible bases and their base collision proxies at identical XYZ world positions with measured delta `[0,0,0]`.

Stable collision IDs:

- `ELYS-COL-EDN-00-BASE` / `TOP`
- `ELYS-COL-EDN-01-BASE` / `TOP`
- `ELYS-COL-EDN-02-BASE` / `TOP`
- `ELYS-COL-EDN-03-BASE` / `TOP`

R5 remote artifacts:
- `.blend` 2,867,208 B · etag `dc639fd78ed771da917a4d45b02f1c99`;
- GLB 2,692,504 B · etag `2d2e0aee2c06bec978685794af33665`;
- State A preview `951c10651bc747331a491786c1969111`;
- State B preview `316d7b8e9566b4103a8d1713f2e4fbcf`.

Important: Blender keyframes/collision are an editable production contract, **not target-engine gameplay implementation**.

## R6 — white-envelope material proof

Three portable Principled material candidates:

### C01 · Sintered Ceramic Facing
- RGB `0.78 / 0.79 / 0.785`;
- roughness `0.34`;
- coat `0.06`;
- intended dominant maintained facing.

### C02 · Mineral Composite
- RGB `0.66 / 0.675 / 0.68`;
- roughness `0.52`;
- intended structural/recessed matte body.

### C03 · Service Glaze
- RGB `0.83 / 0.835 / 0.825`;
- roughness `0.22`;
- coat `0.14`;
- intended rare hygienic/touched service surfaces, not universal envelope.

Construction-system hypothesis:
- total module thickness: `240 mm`;
- ceramic face: `12 mm`;
- mineral core: `180 mm`;
- metal backer: `4 mm`;
- controlled reveal candidate: `16 mm`.

R6 material lab:
- 17 proof objects;
- close 70 mm / mid 55 mm / far 48 mm evaluation cameras;
- dedicated portable point-light rig;
- localized contact plate + repair tab to test causal human anomaly rather than global grime;
- no external texture/network dependencies.

R6 artifacts:
- editable `.blend`: 3,424,296 B · etag `a20e80769a9a200abcfd8f27406a1cfe`;
- GLB: 3,355,212 B · etag `ff8895eebbfca8eb84998357d01cf58d`;
- close preview: `0334173f0a79b93ee93ccce06f620b97`;
- mid preview: `89e63ab2e721798392f9aeb5ba7840c7`;
- far preview: `e7a6c54641ea26ee4f4da24a1d24b46c`.

Structural shader/dimension QA passed. Direct pixel/art-direction review is **not claimed**. A temporary objective render-buffer validator returned `NO_PIXEL_BUFFER` on all three cameras; that attempt is preserved as inconclusive, not converted into a PASS.

Do not propagate C01/C02/C03 across the whole world until direct visual + engine microset qualification.

---

# PRIMARY FILES

- `WORLD_BIBLE.md`
- `ASSET_MANIFEST.json`
- `PRODUCTION_PLAN.md`
- `ARCHITECTURE_KIT_SPEC.md`
- `MATERIAL_SYSTEM.md`
- `EDEN_STATE_GRAPH.md`
- `scripts/generate_foundation.py`
- `scripts/add_w1_arch_kit.py`
- `scripts/add_eden_stategraph.py`
- `scripts/add_eden_collision_motion.py`
- `scripts/add_white_material_proof.py`
- `evidence/foundation_validation.json`
- `evidence/w1_arch_kit_validation.json`
- `evidence/eden_stategraph_validation.json`
- `evidence/eden_collision_motion_validation.json`
- `evidence/white_material_proof_validation.json`
- `../../coordination/ART-ELYSIUM-001-OWNERSHIP.md`

---

# CURRENT GATE TRUTH

Qualified at current Blender/source scope:

- canon/proposal separation;
- metre scale;
- 48 m EDEN arena;
- modular architecture structural candidate;
- static player/enemy clearance audit;
- EDEN moving-root timeline candidate;
- separate collision proxies;
- visible/collision transform alignment after R5 fix;
- physical actuator candidate;
- white-envelope material laboratory candidate;
- editable `.blend` + GLB + reproducible source scripts + receipts.

OPEN / UNQUALIFIED:

- direct GATE-ART approval;
- native player/dodge/camera traversal through architecture;
- target-engine EDEN state transition;
- nav-obstacle updates;
- target-engine collision traversal;
- final UV/texel density;
- final micro-normal/roughness textures;
- LOD/HLOD/streaming qualification;
- material memory/draw/shader cost;
- production GPU/performance;
- project-native `GATE-ASSET` in a qualified checkout;
- human gameplay review;
- total world completion.

---

# NEXT 3 ACTIONS

## 1. Representative reception microset

Build one reception structure entirely from the current module kit + C01/C02/C03 material roles. This becomes the architecture/material vertical slice rather than propagating hundreds of assets blindly.

Acceptance:
- no bespoke filler required to hide kit weaknesses;
- C01 dominant / C02 structural / C03 service hierarchy readable;
- local human anomaly remains sparse and causal;
- close/mid/far cameras;
- GLB export;
- engine import/traversal when runtime access is available.

## 2. EDEN target-runtime prototype

Translate R5 root/telegraph/collision contract to the executable runtime without touching another owner's gameplay scope unless coordinated through an explicit atomic integration claim.

Acceptance:
- 1.5 s destination warning retained;
- movement duration independently tunable;
- moving collision follows visible module;
- no unavoidable trap/choke;
- camera/dodge test;
- nav update cost measured.

## 3. Casas sin Desgaste foundation

After the reception microset proves the kit/material grammar, block out the second canonical region using obsolete preference profiles rather than cosmetic reskins.

---

# CLAIM STATUS

`KEEP / ACTIVE / WORLD_OWNER`.

Do not start a second ELYSIUM world branch. Any parallel ELYSIUM contribution must be an explicit non-overlapping `ATOMIC_SUBCLAIM` reconciled against issue #7, PR #15, Linear ROT-116 and the current branch.
