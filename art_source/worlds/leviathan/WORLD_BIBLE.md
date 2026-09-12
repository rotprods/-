# LEVIATHAN — World Production Bible · ART-LEVIATHAN-001

Status: `IN_PROGRESS / WAVE 0–1 FOUNDATION`
Claim: `CLM-W10-WORLD-LEVIATHAN-001`
Agent: `AGENT-LEVIATHAN-10`
Branch: `art/world-leviathan-001`
Base authority snapshot: `main@4c2fa044080004609ea6df45f34b2a784536507a`

> This file is a production derivative. Canon authority remains `design/EXOVANT_BIBLIA.md` and `design/EXOVANT_DATA.json`. Anything not established there is labelled below.

## 1. Epistemic contract

- `CANON`: explicitly present in current world/design authority.
- `OBSERVED`: directly measured from an executed tool/runtime.
- `DOCUMENTED`: established by current repository protocol/runbook.
- `PROPOSAL`: reversible production decision for this branch.
- `BLOCKED`: decision absent or not yet qualified; must not be silently invented.

## 2. Identity

| Field | Value | Status |
|---|---|---|
| world_id | `leviathan` | CANON |
| name | LEVIATHAN | CANON |
| custodian | SOMA, el sistema inmune | CANON |
| domain | EL UMBRAL | CANON |
| system | Soma | CANON |
| faction | Comuna del Pulso | CANON |
| world nature | living planetary body; fantastic anatomy, not an astrobiology claim | CANON |
| gravity | 1.15 g | CANON |
| reference temperature | 38 °C | CANON |
| physical planet radius / diameter | UNKNOWN | BLOCKED |
| production engine | Unreal is principal candidate; not qualified/integrated | DOCUMENTED |
| executable prototype engine | Godot 4.7.2 stable | DOCUMENTED |
| Blender route | Higgsfield 3D Jutsu / Blender bpy | OBSERVED + DOCUMENTED |
| Blender version on dedicated LEVIATHAN project | 5.2.0 LTS | OBSERVED |
| Blender units | metric, scale_length 1.0 (`1 BU = 1 m`) | OBSERVED |

## 3. Local North Star

Deliver a recoverable LEVIATHAN world-production foundation that makes its living-planet identity legible without relying on text, preserves stable gameplay collision under deforming visual tissue, and establishes the three canonical regions plus SOMA’s 58 m encounter interface at real metre scale.

### Foundation acceptance metrics

1. 3/3 canonical regions represented in the master blockout.
2. SOMA arena interface at canonical 58 m diameter.
3. 1.85 m human scale reference present in the master scene.
4. Stable collision layer physically separated from visual-only deforming tissue.
5. All WAVE-0/1 scene objects deterministic/recoverable from source generator.
6. Editable `.blend` and portable GLB produced from the dedicated project.
7. No final-SOMA-anatomy, planet-radius, engine-performance or AAAA-complete claim without their gates.

## 4. World rule and narrative causality

### CANON

**Conflict.** Mountain ranges contract every forty minutes, revealing that the continents are the shell of a sleeping animal.

**Gameplay rule.** Environmental damage activates immune response by region. Healing a route may close an industrial shortcut and open an organic path; that consequence must be communicated before confirmation.

**Narrative material thesis.** The colony is not merely sitting on terrain: it is an implant inside a living body. Human infrastructure must therefore read as graft, brace, suture, drainage, diagnosis, access and maintenance—not generic sci-fi kitbash.

**Hidden causal layer.** The colony alone did not cause the disease; the Network is attacking organs that Hélix disconnected.

## 5. Canonical geography / authored hierarchy

### L0 — Planetary canon

- Living planetary body: CANON.
- Gravity 1.15 g: CANON.
- Reference temperature 38 °C: CANON.
- Physical radius, diameter, axial/orbital physical parameters: BLOCKED/UNKNOWN.

No physical planet size is assigned by this branch.

### L1 — Orbital representation

CANON says organ-like orbital bodies exist and are connected through fictive transit. Their number, dimensions and orbital mechanics are not currently defined. `NOT_READY` pending L0/Art/World decision.

### L2 — Regional authored test cell

`720 m × 480 m` is implemented as a **PROPOSAL blockout cell only**, not LEVIATHAN’s planet size or final playable-area promise. It exists to validate scale, region relationships, streaming boundaries and visual language.

### L3 — Canonical gameplay regions

1. **Puerto de la Herida** — colonists occupying a scarred/healed zone.
2. **Jardines Inmunes** — symbiotic fauna and lymph channels.
3. **Cámara de SOMA** — regulatory organ under pressure.

### L4 — Hero zones

- wound-port graft cluster and scar ring;
- immune-garden circulation crossing;
- SOMA’s 58 m regulatory chamber.

### L5 — Hero asset interfaces

- SOMA silhouette/combat-scale proxy (final anatomy explicitly NOT approved);
- living valve/safe-valve family;
- colony soft module + suture clamp family;
- lymph-channel and tissue-transition family;
- key biota/adversary silhouette references.

## 6. Ecology

### CANON species / role

- **Parásito jardinero** — removes dead tissue; density can turn it into a threat.
- **Ballena de linfa** — nutrient transport through channels.
- **Polinizador de herida** — accelerates healing and changes routes.
- **Alga de pulso** — indicates local pressure and rhythm.

### Ecology production rule — PROPOSAL

Every species must expose its physical/ecological function in silhouette, locomotion or placement before tertiary surface detail. Random alien ornamentation is rejected.

## 7. Population / actors

### CANON NPCs

- Oru Tess — planetary medic; treats the colony as a potentially viable graft.
- Anja Piel — born on LEVIATHAN; argues her home is part of the organism.
- Faro-3 — immune interface learning to distinguish invasion from coexistence.

### CANON adversaries

- Fagocito guardián — short pursuit then return to defended tissue.
- Extractor de pulso — drains channels to maintain human equipment.
- Colonia parasitaria — threat responsive to density and nutrients.

Current master scene uses silhouette proxies only. Character topology, rigging, animation and final anatomy remain `TODO` under later asset/domain tasks.

## 8. Architecture / infrastructure language

### CANON seed language

Habitable anatomy: abstract tissue, soft modules, sutures and valves.

### PROPOSAL production grammar

**Human graft layer**
- repaired ivory ceramic shells;
- dark technical under-structure;
- externally readable maintenance clamps;
- soft/rounded pressure shells instead of conventional rigid walls where tissue contact occurs;
- amber refuge markers.

**Living host layer**
- load-bearing cartilage/rib masses;
- vascular trunks following pressure/flow logic;
- membranes at moving interfaces;
- scar tissue around colonized perforations;
- cyan diagnostic/memory conduits only where information/diagnosis is functionally justified.

**Forbidden drift**
- random greebles;
- generic biomechanical horror without functional anatomy;
- gore as a substitute for design;
- uniform wetness/noise;
- arbitrary tentacles;
- moving collision that can trap/crush players without a designed escape volume.

## 9. SOMA encounter contract

### CANON

- arena/chamber diameter: **58 m**;
- slow contractions;
- biological bridges;
- wall must not crush without escape space;
- phase 1: localized antibodies/barriers;
- phase 2: contractions move cover/open safe vessels;
- phase 3: autoimmune reaction; diagnosis can separate colony from infection.

Representative attacks:
- Pulso expulsor — membrane inflates 1.5 s; valve shelter response.
- Barrido de cilios — fibers rise 1.0 s; advance after sweep.
- Nódulo inmune — marked 1.4 s; break anchor or leave radius.

### Current implementation boundary

`SOMA_PROXY_NOT_FINAL` is a combat-scale/silhouette interface only. It is NOT final custodian anatomy, topology, rig, materials, animation or combat integration.

## 10. Material direction

Core portable PBR roles currently implemented as WAVE-1 blockout materials:

- `LEV_MAT_TISSUE_WARM`
- `LEV_MAT_TISSUE_DARK`
- `LEV_MAT_VASCULAR`
- `LEV_MAT_MEMBRANE`
- `LEV_MAT_CARTILAGE`
- `HUM_MAT_IVORY_CERAMIC`
- `HUM_MAT_DARK_TECH`
- `SIGNAL_AMBER_REFUGE`
- `SIGNAL_CYAN_MEMORY`
- `SIGNAL_VERMILION_HOSTILE`
- `DEBUG_COLLISION_STABLE`

These are lookdev/blockout roles, not final calibrated texture sets. No UDIM/texture-memory decision is made before target runtime/hardware qualification.

## 11. Collision / deformation contract

CANON risk explicitly requires stable collision below visually deforming ground in the first version.

Production rule:

- `40_COLLISION_PROXY` owns stable gameplay substrate and route pads.
- living tissue may visually contract/morph independently.
- any future deformation system must prove character traversal, escape volumes and camera stability before its collision is allowed to deform.
- render success alone cannot close collision QA.

## 12. Camera / readability contract

Third-person combat readability outranks biological spectacle. The scene contains dedicated gameplay cameras for Puerto, Jardines and SOMA plus a production overview camera. Hostile vermilion, refuge amber and memory/diagnostic cyan must remain redundant with form/sound, never color-only cues.

## 13. Sound direction — CANON

Filtered pulses, tense membranes, medical signals mixed with community song.

No audio asset is claimed produced by this branch.

## 14. Current blockers / decisions needed

| ID | Decision needed | Impact | Work that can continue |
|---|---|---|---|
| LEV-BLK-001 | physical radius/diameter and planetary parameters | L0/L1 planetary representation | L2–L5 authored regional production |
| LEV-BLK-002 | final production engine after comparison | final export, LOD/HLOD/streaming specifics | neutral Blender/GLB pipeline and Godot-side later smoke import |
| LEV-BLK-003 | target GPU/hardware/preset | triangle/material/texture/shader hard budgets | measure raw metrics and optimize relative deltas |
| LEV-BLK-004 | final SOMA anatomical design review | final boss sculpt/rig/material/animation | arena and combat interface proxy |
| LEV-BLK-005 | final playable-region dimensions | streaming cell topology and authored density | representative-cell hierarchy and coverage planning |

## 15. Art drift test

Without labels, LEVIATHAN should remain identifiable by the relationship between living load-bearing anatomy, circulation, pressure interfaces, scar/suture construction and human graft modules. If it reads merely as “red organic sci-fi,” the asset fails art direction.

## 16. Current evidence

- Dedicated 3D Jutsu project: `2577a7b6-ebd7-4d31-a645-620e4b73a95d`.
- Blender observed: 5.2.0 LTS; metric scale 1.0; Eevee; 24 fps.
- Master blockout committed at remote revision 1.
- Revision 1 reports 125 scene objects, 90 meshes, 25 curve/font objects, 11 materials, four cameras and four lights.
- Remote revision generated editable `.blend` and portable GLB.
- Visual QA, final material QA, engine import, performance, human art review and gameplay collision remain separate gates until receipts exist.
