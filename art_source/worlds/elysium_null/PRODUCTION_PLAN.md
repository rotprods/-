# ELYSIUM NULL — PRODUCTION PLAN · ART-ELYSIUM-001

Status: `ACTIVE / FOUNDATION_WAVE_0`
Scope owner: `ART-ELYSIUM-001`
Branch: `art/world-elysium-null-001`

This plan is intentionally local to the ELYSIUM NULL art branch. It does not mutate shared `STATE.json`, `PLAN.json` or `HANDOFF.md`; the integrator reconciles shared project state after review.

---

## 1. LOCAL NORTH STAR

Deliver ELYSIUM NULL as a recoverable, modular, hyperrealistic game-world production package whose art direction communicates controlled perfection through function and spatial behavior—not generic white sci-fi decoration—and whose assets can be measured, exported, integrated, optimized and continued by another agent without chat context.

---

## 2. DEFINITION OF READY

A task may enter `IN_PROGRESS` only when it has:

- stable task ID;
- owner/scope;
- canon or proposal classification;
- inputs/references;
- dependencies;
- expected file/output;
- measurable DoD;
- collision check against other world agents.

If one is missing: `NOT_READY`.

---

## 3. STATUS MODEL

`TODO → CLAIMED → IN_PROGRESS → REVIEW → DONE`

Exceptional states:

- `BLOCKED`
- `DEFERRED`
- `SUPERSEDED`

No `DONE` without receipts.

---

## 4. WAVES

### W0 — Authority / foundation
Goal: remove ambiguity before expensive art.

Deliverables:
- ownership contract;
- world bible;
- exhaustive coverage manifest;
- scale hierarchy;
- Blender world master;
- deterministic foundation generator;
- first representative blockout;
- QA receipt.

Exit: repository and remote scene can be cold-resumed without this chat.

### W1 — Architectural grammar
Goal: turn blockout language into production modules.

Deliverables:
- structural core kit;
- envelope kit;
- canopy/bridge/gate kit;
- service spine/hatches;
- domestic kit skeleton;
- material calibration targets;
- grid/pivot/snapping spec.

Exit: at least one non-hero building and one domestic unit can be assembled entirely from qualified modules.

### W2 — Avenida del Recibimiento
Goal: make the first canonical region playable and visually diagnostic.

Deliverables:
- final route topology;
- reception architecture;
- tram infrastructure;
- repeated gardens;
- service props;
- anomaly storytelling set;
- collision/LOD first pass.

Exit: close/mid/far engine review package plus traversal test.

### W3 — Casas sin Desgaste
Goal: prove frozen-personalization grammar.

Deliverables:
- domestic kit;
- obsolete preference profiles;
- archived-resident props;
- hidden Noa route;
- wear anomaly trail;
- climate/window side-story assembly.

Exit: player can visually infer “personalized for someone absent” without exposition text.

### W4 — Synthetic ecology
Goal: build maintained-life system.

Deliverables:
- pollen automaton;
- porcelain bird;
- index butterfly;
- maintenance roots;
- flora family;
- nutrient/service interfaces;
- instancing/wind/LOD strategy.

Exit: ecology reads as active world infrastructure and remains within measured budgets.

### W5 — Population / adversaries
Goal: production-ready character families.

Deliverables:
- El Jardinero;
- Noa Cero;
- Elías Ret;
- Custodio de comodidad;
- Podador blanco;
- Doble doméstico;
- wardrobe/equipment language;
- rigs / sockets / deformation tests.

Exit: representative locomotion/combat/readability package passes close/mid/far review.

### W6 — EDEN encounter art
Goal: convert canonical boss logic into physical geometry.

Deliverables:
- EDEN hero model;
- pruning arm;
- service hands/manipulators;
- movable arena modules;
- three phase visual states;
- attack telegraph geometry;
- collision and camera clearance.

Exit: 48 m arena remains traversable across all authored states and representative telegraphs are readable.

### W7 — World macro / vistas
Goal: make Elysium feel world-scale without authoring every metre at hero density.

Deliverables:
- macro habitat topology;
- Alba Nula skyline grammar;
- maintenance mirrors;
- reserve-colony vistas;
- HLOD/impostor candidates;
- streaming-cell boundaries.

Exit: orbital/far/region/gameplay scales transition coherently with no false natural-planet assumptions.

### W8 — Optimization / integration
Goal: qualify rather than merely beautify.

Deliverables:
- final collision families;
- LOD/HLOD;
- material/draw-call consolidation;
- GLB/import profile;
- target-engine scene;
- performance measurements;
- GATE-ASSET package;
- GATE-ART package.

Exit: all required project gates pass or are explicitly blocked/waived by authority.

---

# 5. FIRST 10 EXECUTABLE TASKS

## ELYS/W0/001 — Establish ownership
Priority: P0
Status: `DONE`

Output:
`art_source/coordination/ART-ELYSIUM-001-OWNERSHIP.md`

DoD:
- branch exists from observed main SHA;
- active-world collision audit performed;
- owned/excluded paths explicit;
- no shared-state overwrite.

Receipt:
commit `3575ccd4bf6a488f56d3ddd64a4d496b14599cd1`.

---

## ELYS/W0/002 — Recover world canon
Priority: P0
Status: `DONE`

DoD:
- cosmology/world form recovered;
- gravity and temperature recovered;
- regions, NPCs, ecology, enemies, missions, EDEN and vehicle recovered;
- proposal vs canon separated.

Receipt:
`WORLD_BIBLE.md`.

---

## ELYS/W0/003 — Build coverage manifest
Priority: P0
Status: `DONE`

DoD:
- architecture, materials, ecology, NPC, enemies, boss, vehicle, props and technical assets represented;
- every row has stable ID, priority, status, epistemic type and DoD;
- P0/P1 gaps are visible.

Receipt:
`ASSET_MANIFEST.json`.

---

## ELYS/W0/004 — Create remote World Master
Priority: P0
Status: `DONE`

Remote project:
`00152eea-2da0-40ec-8666-78d6764c718f`

DoD:
- dedicated ELYSIUM project;
- Blender/version observed rather than assumed;
- metric units;
- clean base scene;
- independent from other world agents.

Observed:
Blender `5.2.0 LTS`, metric `1 BU = 1 m`.

---

## ELYS/W0/005 — Deterministic representative blockout
Priority: P0
Status: `DONE / STRUCTURAL_VERIFY`

Scene revision: `1`.

Contains:
- 1.85 m human scale proxy;
- Avenida arrival axis;
- repeated arcology masses;
- controlled gardens;
- custodian tram proxy;
- 48 m EDEN arena;
- movable arena modules;
- EDEN distant proxy;
- localized repaired human object;
- delivery camera and motivated artificial lighting.

DoD structural receipts:
- 153 objects;
- 149 meshes;
- 9 materials;
- 4,724 vertices;
- 5,618 polygons;
- zero meshes without material;
- zero duplicate object names;
- EDEN arena measured 48 × 48 m;
- local scene bounds measured 72 × 262 × 46.9 m.

Visual/engine approval remains separate.

---

## ELYS/W0/006 — Persist exact generator
Priority: P0
Status: `IN_PROGRESS`

DoD:
- Blender Python source checked into owned path;
- repeat execution from clean scene produces equivalent named hierarchy and metric anchors;
- generator contains no external network dependency;
- output preserves `.blend` source and GLB exchange path.

---

## ELYS/W0/007 — Foundation QA receipt
Priority: P0
Status: `IN_PROGRESS`

Required checks:
- canonical 48 m arena;
- human proxy scale;
- naming uniqueness;
- material assignment;
- collection ownership;
- deterministic script;
- editable blend available remotely;
- GLB available remotely;
- preview artifact exists;
- visual review explicitly separate from structural pass.

Output:
`evidence/foundation_validation.json`.

---

## ELYS/W1/001 — Arcology modular grid decision
Priority: P0
Status: `TODO`

Dependencies:
W0 complete.

DoD:
- 1 m planning grid tested;
- 4 m bay candidate tested;
- 8/12/16 m span family tested;
- player clearances measured against runtime controller before promotion;
- pivots/snapping specification committed.

---

## ELYS/W1/002 — White envelope production material
Priority: P0
Status: `TODO`

DoD:
- physically plausible substrate/manufacturing hypothesis;
- macro/meso/micro roughness structure;
- no plastic-white response;
- close/mid/far renders;
- engine material translation documented;
- measured texture/material cost.

---

## ELYS/W1/003 — EDEN arena state graph
Priority: P0
Status: `TODO`

DoD:
- at least three arena geometry states;
- each state keeps guaranteed corridors;
- every moving module has start/preview/target transforms;
- canonical 1.5 s Reubicación telegraph can be represented spatially;
- collision/nav/camera envelopes documented;
- no state relies on geometry teleport invisible to player.

---

# 6. BLOCKERS / NON-CLAIMS

Current branch does **not** claim:

- total physical diameter/radius of ELYSIUM habitat;
- Unreal integration;
- production GPU qualification;
- final PBR calibration;
- final collision;
- final LOD budgets;
- GATE-ASSET pass;
- GATE-ART pass;
- human playtest;
- world completion.

Container-local clone/tool execution was unavailable in the initiating session due network/DNS path. GitHub connector and qualified remote Blender path were used for real writes/execution. Project-native `studio.py`, `asset_audit.py` and Godot Gauntlet therefore remain to be run by a runtime that has the repository checkout and engine binary.

---

# 7. CONTINUOUS LOOP

For every session:

`RETROSPECT → RESYNC MAIN/BRANCH → AUDIT CLAIMS → PICK P0/P1 → BUILD → STRUCTURAL QA → VISUAL QA → EXPORT → INTEGRATION QA → DOCUMENT → RECEIPTS → HANDOFF`

At the sixth repetition of one failure mechanism: stop iteration, diagnose architecture/root cause, then change approach.

---

# 8. LOCAL DEFINITION OF DONE — ASSET

An ELYSIUM asset is not `DONE` until all applicable items pass:

- [ ] Stable asset ID and manifest entry.
- [ ] Canon/proposal provenance.
- [ ] Real scale.
- [ ] Correct pivot/origin.
- [ ] Editable source.
- [ ] Generator/source script where procedural.
- [ ] Clean names/collections.
- [ ] Topology/shading validated.
- [ ] UV/texel strategy.
- [ ] PBR materials.
- [ ] Causal wear only.
- [ ] Separate collision when applicable.
- [ ] LOD/equivalent strategy.
- [ ] Measured triangles/vertices/material slots/textures.
- [ ] GLB/export.
- [ ] Import test.
- [ ] Close/mid/far review.
- [ ] In-engine review.
- [ ] Performance receipt.
- [ ] Manifest/status updated.

Hero character/boss additionally requires rig/deformation/animation/socket/hit-interface validation.

---

# 9. WORLD STOP CONDITION

Never declare ELYSIUM NULL complete because a render is attractive.

Completion requires coverage matrix closure, engine integration, asset/performance gates, art approval and campaign/world dependencies or an explicit authority waiver for each omitted gate.
