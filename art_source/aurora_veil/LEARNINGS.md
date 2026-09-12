# AURORA VEIL — LEARNINGS / REGRESSION LOG

This file records Aurora-specific observations. It does not replace `learning/hub`; promote only after the project learning runtime/integrator applies the canonical event workflow.

## L-AUR-001 — Split remote Blender world builds by semantic wave

**Symptom:** `aurora-world-master-r1` exceeded the 300 s worker deadline and committed no revision.  
**Mechanism:** one operation combined macro construction, region population and multiple renders/export work.  
**Correction:** foundation, population/orchard, scale QA, camera/lighting and render validation became separate operations.  
**Evidence:** revisions 1–5 completed after the split.  
**Boundary:** applies to this 3D Jutsu/Blender workload; not a universal threshold for every Blender host.  
**Status:** observed / candidate for LearningEvent promotion.

## L-AUR-002 — Query measured dimensions; do not trust intended primitive dimensions

**Symptom:** observatory ring measured 50.6 m vs proposed 48 m; Peregrino measured 6.0×2.9×2.5 m vs proposed 5.8×2.7×2.4 m.  
**Mechanism:** authored primitive parameters/torus thickness and blockout dimensions were not validated against final object bounds.  
**Correction:** direct scene query before checkpoint; corrected dimensions in revision 3.  
**Control:** hero/architectural blockouts need explicit bounding-box QA against manifest.  
**Status:** observed / candidate for LearningEvent promotion.

## L-AUR-003 — Render evidence requires camera clipping QA

**Symptom:** first world-overview evidence appeared almost empty/dark.  
**Mechanism:** overview camera was ~4.9 km from the target while the camera far clip remained near the default ~1 km.  
**Correction:** far clip explicitly set to 12 km; camp 5 km; AEON 2.5 km.  
**Control:** compare camera-target distance to clip range in camera QA.  
**Status:** observed / candidate for LearningEvent promotion.

## L-AUR-004 — Blender Render Result can be empty inside this query context

**Symptom:** first luminance validator divided by zero because `Render Result` exposed no pixels.  
**Mechanism:** query context did not provide a usable in-memory pixel buffer in that path.  
**Correction:** render to an explicit temporary PNG, reload with `bpy.data.images.load`, then measure pixels.  
**Boundary:** verified on the current Blender 5.2 3D Jutsu worker.  
**Status:** observed / candidate for LearningEvent promotion.

## L-AUR-005 — Photometric PASS is not GATE-ART

**Observation:** revision-5 overview/camp/AEON renders pass non-empty exposure checks and have zero white clipping.  
**Boundary:** this does not establish visual quality, composition, material realism or director approval.  
**Control:** keep `ART=PENDING_HUMAN_VISUAL_REVIEW`; never infer artistic approval from pixel statistics.  
**Status:** enforced in `QA/validation.json`.

## L-AUR-006 — Scene-global lights require cross-camera regression testing

**Symptom:** orbital L1 revision 6 introduced a second `SUN` intended only for the orbital proxy.  
**Mechanism:** a Blender SUN is scene-global; the extra source would also change the already-qualified surface lighting.  
**Correction:** remove `SUN_VELAR_ORBITAL`; reuse `SUN_VELAR_LOW` and validate the world-overview camera after the orbital package is present.  
**Evidence:** revision 7 surface regression reproduced the revision-5 overview mean luminance exactly (`0.1793`, delta `0.0000`) with zero clipping.  
**Control:** any light with scene-global influence must pass regression against previously qualified delivery cameras before promotion.  
**Status:** observed / candidate for LearningEvent promotion.

## L-AUR-007 — Orbital representation must not silently invent planetary geography

**Observation:** Aurora canon specifies local regions, sky/celestial motifs and two observation stations, but does not define global continents/biome topology.  
**Correction:** L1 orbital shell remains smooth/neutral, with physical radius tagged `PROPOSAL`, global geography `UNKNOWN_NOT_AUTHORED`, and atmosphere/aurora/stations as separate layers.  
**Control:** global continent or biome authoring requires a future explicit decision/ADR rather than decorative invention.  
**Status:** enforced by `QA/orbital_r7.json` and `blender/aurora_orbital_l1.py`.
