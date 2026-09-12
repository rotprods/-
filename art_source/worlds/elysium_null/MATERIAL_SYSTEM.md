# ELYSIUM NULL — WHITE MATERIAL SYSTEM v0.1

Cell: `ART-ELYSIUM-001`
Remote Blender structural checkpoint: revision `6`
Status: `LOOKDEV CANDIDATE / GATE-ART PENDING`

This document converts the canonical “white arcology” seed into a physically motivated material family. It does **not** promote any numeric shader value to immutable canon.

## 1. Problem

ELYSIUM must read as maintained, controlled and materially real without collapsing into:

- generic glossy white sci-fi;
- plastic toy surfaces;
- featureless unlit white boxes;
- procedural grime used to manufacture realism;
- excessive dark seams that turn the world into a black/white tech cliché.

The design response is a small family of white materials with distinct manufacturing roles rather than one universal shader.

## 2. Candidate family

### C01 — Sintered Ceramic Facing

Blender material: `MAT_Elysium_WHITE_C01_SinteredCeramic`

Current portable Principled proposal:

- Base Color RGB: `0.78 / 0.79 / 0.785`
- Metallic: `0`
- Roughness: `0.34`
- Coat Weight: `0.06`
- Coat Roughness: `0.12`

Manufacturing hypothesis: sintered aluminosilicate ceramic facing.

Role: dominant maintained exterior/interior facing where the player must read a clean surface without mirror-like service gloss.

Current recommendation: **primary candidate for the dominant visible envelope**, but still requires direct visual and engine review.

### C02 — Mineral Composite Body

Blender material: `MAT_Elysium_WHITE_C02_MineralComposite`

Current proposal:

- Base Color RGB: `0.66 / 0.675 / 0.68`
- Metallic: `0`
- Roughness: `0.52`
- Coat Weight: `0`

Manufacturing hypothesis: mineral-filled structural composite.

Role: load-bearing/recessed matte body; provides value/roughness separation without using arbitrary dark panels.

Current recommendation: **secondary structural family**.

### C03 — Service Glaze

Blender material: `MAT_Elysium_WHITE_C03_ServiceGlaze`

Current proposal:

- Base Color RGB: `0.83 / 0.835 / 0.825`
- Metallic: `0`
- Roughness: `0.22`
- Coat Weight: `0.14`
- Coat Roughness: `0.08`

Manufacturing hypothesis: maintained ceramic glaze / hygienic service surface.

Role: rare touched/cleanable surfaces, medical/service interfaces, sanitation zones. It is deliberately **not** the universal world envelope.

Current recommendation: **accent/service material only** to avoid plastic-white visual drift.

---

## 3. Construction-system hypothesis

The revision-6 cutaway represents a reversible 240 mm architecture panel system:

- ceramic facing: **12 mm**;
- mineral/composite core: **180 mm**;
- metallic backer: **4 mm**;
- remaining thickness reserved for interface/tolerance/service gap within the 240 mm module.

These are production-design hypotheses, not certified engineering dimensions. Their value is to make seams, edges, repairs, penetrations and replacement logic spatially consistent.

## 4. Joint language

Candidate controlled reveal: **16 mm**.

A joint must correspond to:

- panel boundary;
- tolerance/expansion requirement;
- removable service element;
- structural transition;
- deliberate state/anomaly.

Do not draw seams simply to make a clean wall appear detailed.

## 5. Realism at three scales

### Macro

- large white planes remain uninterrupted enough to carry ELYSIUM’s control language;
- C01/C02 value separation supports massing;
- C03 cannot dominate large façades.

### Meso

- seams, attachment logic, service backs, access hatches and repair interfaces must correspond to construction.

### Micro

Microdetail is deliberately deferred. When added, it should represent:

- ceramic micro-roughness;
- manufacturing texture;
- physically local hand/contact polish;
- tiny repair evidence;
- rare maintenance failures.

No uniform scratch masks or all-over dirt.

## 6. Maintenance / wear contract

ELYSIUM actively maintains itself. Therefore normal surfaces should remain unusually controlled.

Permitted visible wear is high-information and causal:

1. hidden occupation;
2. service failure;
3. inaccessible maintenance zone;
4. deliberate human repair;
5. anomaly introduced against EDEN’s normalization.

Revision 6 includes one localized metal contact plate and amber repair tab to test this contrast.

## 7. Evaluation rig

Remote revision 6 includes:

- three 2.4 × 3.0 m, 240 mm thick candidate panels;
- neutral highlight spheres;
- layered construction cutaway;
- 16 mm joint sample;
- localized human-contact/repair sample;
- portable point-light lab;
- `CAM_MAT_CLOSE` — 70 mm;
- `CAM_MAT_MID` — 55 mm;
- `CAM_MAT_FAR` — 48 mm.

Published artifacts:

- `elysium_r6_material_close.png`
- `elysium_r6_material_mid.png`
- `elysium_r6_material_far.png`

Artifact existence proves renderability, not creative approval.

## 8. QA truth

### Structurally verified

- all three materials exist with expected Principled values;
- all candidates are non-metallic;
- proof panels measure exactly 2.4 × 0.24 × 3.0 m;
- cutaway dimensions match 12 mm / 180 mm / 4 mm proposal;
- reveal is 16 mm;
- three cameras exist at intended lenses;
- no external texture/network dependency;
- editable `.blend` and portable GLB revision 6 exist.

### Inconclusive

A temporary low-resolution render-buffer validator attempted to compute exposure/clipping statistics through `Render Result`, but this worker returned no readable pixel buffer for all three cameras. No false PASS was assigned.

### Still required

- direct visual inspection close/mid/far;
- target-engine material translation;
- calibrated lighting/exposure test in gameplay scene;
- micro-normal/roughness design if visible benefit justifies cost;
- texture/mip/memory measurement;
- final GATE-ART.

## 9. Promotion rule

Do **not** replace every ELYSIUM material with C01/C02/C03 yet.

Promotion sequence:

`LAB CANDIDATE → DIRECT VISUAL REVIEW → REPRESENTATIVE BUILDING MICROSET → ENGINE IMPORT → CLOSE/MID/FAR REVIEW → COST MEASUREMENT → MATERIAL MASTER`

Only after that should the material family propagate across the world.

## 10. Related stable asset IDs

- `ELYS-MAT-001` — white ceramic/mineral envelope: now `LOOKDEV_CANDIDATE`.
- `ELYS-MAT-002` — satin structural metal: remains blockout/production hypothesis.
- `ELYS-MAT-003` — dark service recess: remains controlled support role.
- `ELYS-MAT-005` — human repair/anomaly family: foundation candidate; final wear system pending.

Source script: `scripts/add_white_material_proof.py`.
