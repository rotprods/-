# EXOVANT — AAA ASSET FIDELITY GATE v1

Status: ENFORCED AFTER MERGE TO `main`  
Scope: all 3D world, environment, vehicle, creature, character, architecture, hero-prop and cinematic asset work.  
Extends: `/EXOVANT-X100`, Fleet, Graphify/COS and Gauntlet.

## 0. Correction that must persist

`BLOCKOUT != HERO ASSET`.

`MORE POLYGONS != MORE REALISM`.

A low-information source mesh does not become AAA because an agent adds more shaders, puddles, bevels, scatter, decals, noise, microgeometry or lights. Final-lookdev work is forbidden on a source asset that has not first passed the appropriate fidelity gate.

This protocol does **not** invalidate blockouts. It changes their truth state and downstream role:

- blockout/proxy geometry remains valuable for world layout, scale, traversal, collisions, camera, composition, streaming cells, gameplay topology and technical interfaces;
- it is not automatically eligible for final hero lookdev;
- hero surfaces are rebuilt, sourced or reconstructed at the correct information density before final lookdev.

## 1. Asset truth-state lattice

Every significant 3D asset/family must declare exactly one current fidelity state:

1. `BLOCKOUT` — spatial/layout witness only.
2. `PROXY` — technical/gameplay/collision/streaming witness; not visual authority.
3. `SUPPORT_CANDIDATE` — plausible supporting asset; final use depends on camera distance and runtime budget.
4. `HERO_CANDIDATE` — source appears capable of hero use but is not yet stress-qualified.
5. `HERO_QUALIFIED` — passes source-fidelity, close-up and material-domain gates for its intended use.
6. `RUNTIME_QUALIFIED` — derived game asset passes target-engine/runtime/profile gates.
7. `CINEMATIC_QUALIFIED` — derived cinematic asset passes final-frame/render/compositing gates.

No agent may promote an asset by label alone. Every promotion requires evidence.

## 2. Mandatory Source Fidelity Gate

Before expensive final lookdev, high-resolution texture authoring, long renders, final material polish or AAA/AAAA language, evaluate the source asset against its intended camera/player exposure.

### 2.1 Geometry / silhouette
Required where applicable:
- silhouette matches approved target from all critical views;
- scale and proportions are internally coherent;
- close camera angles do not reveal faceting, crude curvature or proxy construction;
- thickness/load-bearing/construction logic exists where visible;
- articulated parts have plausible pivots and separations;
- no hidden dependency on subdivision solely to mask wrong proportions;
- deformation-critical assets have topology compatible with the planned rig/deformation route.

### 2.2 Semantic part separation
Hero assets should expose meaningful controllable domains where needed:
- body/shell;
- glass/transmission;
- rubber/soft material;
- emissive/light elements;
- metal subtypes;
- moving/articulated parts;
- decals/logos/identity layers;
- collision or gameplay surfaces separately from visual geometry.

A single undifferentiated mesh/material blob is a warning for close-up hero use.

### 2.3 Surface/material authority
Before final material polish the asset must support the channels required by its target:
- Base Color;
- Roughness;
- Metallic when physically relevant;
- Normal;
- Displacement/microdisplacement where justified;
- transmission/IOR where relevant;
- coat/clearcoat for layered finishes;
- anisotropy where material physics requires it;
- masks for wear, wetness, dirt, state or damage when those effects are authored.

Material detail cannot compensate for a silhouette/proportion failure.

### 2.4 UV / texel / bake readiness
For runtime or texture-authored assets:
- UV strategy declared;
- no accidental destructive overlaps;
- texel-density policy recorded or explicitly deferred to target-hardware qualification;
- bake cage / normal-transfer route valid when deriving Runtime Master from a denser source;
- texture provenance and license retained.

### 2.5 Close-up stress test
A hero candidate must be reviewed at the closest plausible gameplay/cinematic distance under neutral and grazing light.

Fail examples:
- visible proxy facets;
- toy-like thickness;
- melted image-to-3D topology;
- broken symmetry where identity requires symmetry;
- impossible panel/part intersections;
- fake depth painted into texture where geometry is visible in parallax;
- glass represented as opaque plastic;
- materials collapsing into one roughness response.

## 3. Asset Factory Router

For Tier S/A, hero, boss, vehicle, landmark, identity architecture or any asset failing the fidelity gate, route through the best source-creation path instead of polishing the proxy.

### 3.1 Available route classes
Choose by evidence, not fashion:

- `MANUAL_MODEL` — Blender/manual hard-surface or sculpt when exact control is cheapest/cleanest.
- `PROCEDURAL_MODEL` — Geometry Nodes/scripted kits for systemic architecture/terrain/repetition.
- `CAD_SOURCE` — engineered assets where CAD/NURBS source exists or can be authored.
- `PHOTOGRAMMETRY_SCAN` — real-world surfaces/objects where capture is legal and available.
- `GAUSSIAN_SPLAT_STATIC` — static high-fidelity captured zones where runtime/render integration supports it; not a substitute for interactive mesh when collision/deformation is required.
- `MULTIVIEW_IMAGE_TO_3D` — reconstruct an approved same-subject multiview target pack.
- `SINGLE_IMAGE_TO_3D` — diagnostic/base candidate only unless independently corrected and qualified.
- `HYBRID_RECONSTRUCTION` — reconstructed base + manual structural correction + retopo + material rebuild.

### 3.2 Live multiview reconstruction candidates
On 2026-09-14 the connected Higgsfield catalog exposed current candidates including Tripo H3.1 multiview, Meshy multi-image and Hunyuan3D v3. Treat these as **provider capability examples, not immutable canon**. Re-query the live model catalog before spending credits or binding a production route.

Rules:
- prefer 3–4 mutually consistent views for identity-critical reconstruction;
- geometry-first bakeoff before optional expensive PBR generation when possible;
- at least two reconstruction candidates for Tier S/A unless one route has already been empirically qualified for that asset class;
- raw provider output state is always `BASE_CANDIDATE`;
- reconstruction provider identity/version, inputs and cost receipt must be persisted.

## 4. Look-lock → source-master → derivatives

Default Tier S/A path:

`CANON → VISUAL_DNA → LOOK_LOCK → SAME_SUBJECT_MULTIVIEW → RECONSTRUCTION/MANUAL_BAKEOFF → SOURCE_MASTER → HERO_FIDELITY_GATE → CINEMATIC_MASTER + RUNTIME_MASTER → ENGINE/RENDER QUALIFICATION → HUMAN GATE_ART`

### SOURCE_MASTER
Highest useful information-density editable source. It is not automatically a shipping asset.

### CINEMATIC_MASTER
May retain high geometry/material complexity for offline render, close-ups, render passes and beauty frames.

### RUNTIME_MASTER
Derived from the same approved identity using retopo/bakes/LODs/collision/streaming/material-budget rules. It must preserve the visual features that define identity under actual screen-space exposure.

Never put the cinematic source directly into gameplay merely because it looks better. Never damage the source master merely to hit runtime budget; derive a runtime asset.

## 5. Runtime derivative contract

For game use, derive and validate as applicable:
- LOD0/1/2+ or engine-native screen-space reduction policy;
- HLOD/cluster representation;
- collision proxy;
- impostor/billboard for distant representation when useful;
- baked normal/AO/curvature/masks from high source;
- texture streaming policy;
- mesh streaming policy;
- instancing/reuse policy;
- material/shader complexity budget;
- animation/skin budget;
- physics budget;
- target-device profiler receipt.

Polycount is an input, not the objective. The objective is frame-time + VRAM + visual identity preservation.

## 6. World representation pyramid

EXOVANT worlds must not use the same representation everywhere.

Recommended strategic hierarchy:

- `HERO_ZONE` — highest player visibility / narrative / combat importance; source-master derived AAA assets and dense authored causality.
- `SUPPORT_ZONE` — production-quality modular/systemic assets with bounded uniqueness.
- `SYSTEMIC_ZONE` — procedural/instanced kits and causal variation.
- `FAR_ZONE` — HLOD/impostor/procedural macro representation.
- `STATIC_CAPTURE_ZONE` — photogrammetry/splat representation only where interaction requirements permit.

This extends the existing 5/20/75 planning heuristic: detail follows player visibility, gameplay significance and reuse value rather than uniform density.

## 7. Material realism law

AAA realism is multi-scale information with causal surface history:

`MACRO SHAPE → MESO CONSTRUCTION → MATERIAL DOMAINS → MICRO RESPONSE → SURFACE HISTORY → LIGHT TRANSPORT`

Examples of causal surface history:
- contact polish where hands/boots/tools actually touch;
- water accumulation based on slope/drainage;
- erosion on exposed edges;
- thermal discoloration near heat sources;
- repair seams where failures occurred;
- dust deposition based on shelter/wind;
- biological growth based on moisture/light/ecology.

Random grunge is not history.

## 8. Render economics gate

No render-time or render-cost promise may be made from resolution alone.

Before a significant offline render:
1. choose representative `EASY`, `MEDIAN`, `WORST` frames;
2. render/benchmark them on the actual engine/device/settings;
3. record measured seconds/frame;
4. calculate frame count from duration × fps;
5. estimate GPU/device hours from measured timings;
6. apply current local/cloud/farm cost rate only after querying or supplying the real rate;
7. include storage, egress, denoise/compositing and artist iteration where material.

Recommended expected-seconds/frame estimator when only three probes exist:

`E[s/frame] = 0.20*easy + 0.60*median + 0.20*worst`

`device_hours = frames * E[s/frame] / 3600`

`wall_hours ≈ device_hours / (workers * measured_parallel_efficiency)`

Workers reduce wall time; they do not magically reduce ideal total compute-hours.

Do not canonize current vendor prices. Persist provider/date/rate snapshot with each estimate.

## 9. Gauntlet enforcement

### Fail closed before final lookdev when
- asset state is BLOCKOUT/PROXY but final-hero polish is requested;
- no approved look target exists for identity-critical asset;
- raw AI/reconstruction mesh is being treated as final;
- close-up stress gate fails;
- material domains required for the shot are inseparable;
- provider/version/provenance is missing;
- cinematic source is being inserted directly into runtime without derivative/profile plan.

### Fail closed before AAA/AAAA claim when
- source fidelity gate has no evidence;
- human GATE_ART remains open;
- target-engine import is absent where game-ready is claimed;
- target hardware profile is absent where performance is claimed;
- proxy/blockout metrics are presented as final art quality;
- generated textures/calibration swatches are presented as final production texture quality.

## 10. Retroactive adoption / salvage

Existing EXOVANT work is not deleted by this protocol.

At next owner resync:
1. inventory current assets/families;
2. label each with fidelity state;
3. preserve useful spatial/gameplay/procedural/blockout work;
4. identify `PROXY_POLISH_DEBT` — expensive final-lookdev effort applied to a source that is not hero-qualified;
5. select the highest-value hero gaps;
6. route those through Asset Factory;
7. derive runtime assets rather than replacing the whole world blindly;
8. keep verified collision/layout/gameplay work where identity changes do not invalidate it;
9. rerun affected visual/runtime gates.

A blockout can be a successful artifact and still fail the hero gate. Those statements are compatible.

## 11. Required receipt fields

For every Tier S/A or hero promotion:

```yaml
asset_id:
world:
claim:
fidelity_before:
fidelity_after:
intended_exposure:
look_target_refs: []
source_route:
provider_model_version: null
source_master_ref:
provenance:
geometry_gate:
semantic_parts_gate:
material_domain_gate:
uv_bake_gate:
closeup_stress_gate:
runtime_derivative_ref: null
cinematic_derivative_ref: null
render_benchmark_ref: null
engine_profile_ref: null
human_gate_art: pending
open_failures: []
```

## 12. Core invariant

**Do not spend final-quality effort on an information-poor source.**

First acquire or create enough correct 3D information. Then polish it. Then derive the runtime representation. Then profile it.
