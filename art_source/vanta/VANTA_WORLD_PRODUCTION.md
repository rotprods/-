# VANTA — World Production Cell

**Project:** EXOVANT 2950  
**World:** VANTA  
**Owner branch:** `art/world-vanta-001`  
**Tracking:** Linear `ROT-114` (child of `ROT-109`)  
**Remote Blender:** `EXOVANT 2950 — VANTA — Full World Production Cell`  
**3D Jutsu project:** `c82188b1-afdc-43f2-828a-5f0e98291f83`  
**Authority:** latest user instruction → `AGENTS.md` → `_project_intelligence/STATE.json` → `HANDOFF.md` → `design/EXOVANT_BIBLIA.md` / `design/EXOVANT_DATA.json`  
**Claim level:** production design + editable blockout. This file does **not** claim that EXO-017, Vanta gameplay, final AAA art, performance or engine integration are complete.

---

## 0. Ownership / anti-overlap lock

This cell owns only VANTA art production.

Detected concurrent claims at reservation time:

- `art/terra-reliquary-kit-001` → Terra: **do not touch**.
- `art/ares-ix-world-001` and `art/ares-ix-world-agent-02` → Ares IX: **do not touch**.
- `art/world-pelagos-thalassa-001` → Pelagos: **do not touch**.
- `art/world-vanta-001` → Vanta: **this cell**.

Rules:

1. Never write into another art branch.
2. Never force-push.
3. Do not mutate global gameplay/state merely to make an art deliverable look integrated.
4. Cross-world reusable assets require an explicit shared-kit handoff; until then keep them namespaced `VAN_*`.
5. Before each wave, re-read remote branches/PRs and Linear. If another Vanta owner appears, reconcile instead of forking the same world silently.
6. A Vanta art checkpoint cannot close EXO-017. Chapter completion remains governed by its required gameplay/native/play gates.

---

# 1. North Star

> Build VANTA as an original, physically coherent, readable and engine-ready industrial world whose identity is visible in silhouette before texture: a high-gravity worker shipyard surviving beneath metal rain, where magnetism is infrastructure, weather, navigation language and combat affordance rather than decorative VFX.

A successful Vanta shot must communicate, without exposition:

- **1.86 g:** compressed architecture, heavy bracing, low centres of mass, short spans, thick handrails, powered lifting everywhere.
- **Labour history:** repairs, ownership marks, strike layers, personal modifications and repeated maintenance—not anonymous sci-fi greeble.
- **Metal rain:** overhead protection, storm channels, sacrificial plates, magnetic catchers, warning beacons and impact scars.
- **Magnetism:** field coils, polarity colours/shapes, anchor points, ferrous dust alignment and routes designed around field geometry.
- **Scarcity + reuse:** ships become houses, hull ribs become streets, containers become clinics, wreckage becomes tools.
- **FERRUM:** not a random robot. It is a shipyard process made body: hull segments, worker-memory cabin, induction coils, tug hardware and scrap-built limbs.

North Star acceptance is visual + technical: silhouette, material causality, navigation legibility, collision, LOD/HLOD, importability and measured runtime cost must all survive together.

---

# 2. Canon lock: facts that may not drift

From `design/EXOVANT_BIBLIA.md` / `EXOVANT_DATA.json`:

- Galaxy: **Andromeda**.
- System: **Drav**.
- Drav: fictional K5 V star.
- Faction: **Trabajadores del Anillo**.
- Gravity reference: **1.86 g**.
- Temperature reference: **−12 °C**.
- Premise: an orbital megafactory is broken; metallic precipitation threatens settlements that survive by recycling it.
- World rule: magnetism redistributes scrap and opens routes; storms are telegraphed; equipment can be anchored or a corridor changed.
- Regions:
  - **Puerto de las Manos** — union, workshops, bars/canteens, docks.
  - **Lluvia de Hierro** — scrap channels and magnetic rails.
  - **Anillo Caído** — FERRUM shipyard.
- NPC targets: **Mika Drav**, **Ciro Fenn**, **Bel Orta**.
- Enemies: **Cobrador de astillero**, **Enjambre de remaches**, **Remolcador automatizado**.
- Biota: **Litófago magnético**, **Raya de limaduras**, **Cuervo de remache**, **Bacteria de escoria**.
- Vehicle: **Remolcador Drav**.
- Custodian: **FERRUM, coloso de chatarra**.
- Boss arena canonical diameter: **72 m**.
- Art cue: cranes, segmented hulls, chains, magnets and shelters; granular rain and distant metal impacts.
- Specific production risk: do not simulate unlimited scrap. Use hero simulated pieces + instanced environment with controlled state transitions.

Anything beyond this section is a **production proposal** until promoted to design authority.

---

# 3. Planet scale proposal

The canon fixes gravity, not physical radius. To answer production scale without inventing a hidden canon fact, this cell uses the following explicit proposal:

| Parameter | Production proposal | Status |
|---|---:|---|
| Planet radius | 7,600 km | PROPOSED |
| Planet diameter | 15,200 km | PROPOSED |
| Surface gravity | 1.86 g | CANON |
| Implied mass | ~2.65 Earth masses | DERIVED FROM PROPOSAL |
| Implied mean density | ~8.6 g/cm³ | DERIVED; iron-rich world hypothesis |
| Authored chapter district | 24 × 24 km | PRODUCTION TARGET |
| Authored district area | 576 km² | DERIVED |
| Streaming macro cell | 4 × 4 km | PRODUCTION TARGET |
| Macro cell count | 36 | CURRENT BLOCKOUT |
| Hero route corridor | ~12 km | PRODUCTION TARGET |
| Boss arena | 72 m diameter | CANON |

### Why planet-scale != one Blender scene at literal planetary coordinates

The world is represented at physical planet scale in metadata/planetary navigation, while authored chapter geometry uses local metre-space cells. A literal 7,600 km-radius render mesh inside the same local scene would make precision, authoring, occlusion and physics worse without adding player-visible quality.

Production hierarchy:

1. **L0 Planet context** — low-frequency planet proxy / orbital presentation.
2. **L1 Planet districts** — geospatial/streaming index; procedural macro terrain outside authored chapter space.
3. **L2 Vanta chapter district** — 24×24 km, 36 × 4 km macro cells.
4. **L3 authored route cells** — close geometry around Puerto → Lluvia → Anillo.
5. **L4 hero interiors/arenas** — local high-density sublevels.
6. **L5 interactive props/characters** — independent origins/pivots, collision and LOD.

Origin rebasing or equivalent world-partition strategy is required at engine integration. Engine-specific technology (Nanite, World Partition, Godot equivalents) remains optional until the engine decision is empirically qualified.

---

# 4. Direction of art — VANTA visual bible

## 4.1 Primary visual thesis

**“Astillero obrero bajo una meteorología hecha de la propia industria.”**

Avoid generic cyberpunk, clean NASA modules, neon city language and random kitbash density. Every visible layer should answer at least one functional question: what holds it, moves it, heats it, shields it, grounds it, repairs it, identifies ownership or keeps people alive in 1.86 g?

## 4.2 Shape language

- Grounded, compressed masses; width over height.
- Repeated triangular bracing under high loads.
- Thick segmented ribs rather than delicate exposed trusses.
- Low-profile roofs with replaceable sacrificial top plates.
- Cylinders reserved for actuators, coils, pressure/drive components.
- Rectangular ship hull modules for inhabited/industrial spaces.
- Polarity hardware reads as paired/quartered geometry, not decorative rings everywhere.
- Hero silhouettes: asymmetry from repair history; readable massing from 200 m, 50 m, 10 m and 1 m.
- FERRUM: worker shipyard anatomy—pelvis as carriage, torso as hull, shoulders as gantry, hammer as keel tooling, claw as magnetic handler.

## 4.3 Material language

Master families:

1. rolled gunmetal steel;
2. ferric rust / pitted oxidised steel;
3. black slag / mill scale;
4. union-yellow safety paint, layered and repaired;
5. magnet/coil dark ceramic-metal composite;
6. cyan-blue field emission, narrow use only;
7. red warning emission for imminent hazard;
8. smoked reinforced glazing;
9. worker textiles / insulated softgoods;
10. medical ceramic/polymer;
11. cable rubber;
12. lubricant/wet steel;
13. frost/ice deposits;
14. ferrous dust;
15. slag biofilm.

Microstructure requirements for final materials:

- rolled direction and mill scale;
- weld beads and heat tint where fabrication logic requires them;
- edge abrasion based on traffic/contact, not global edge masks;
- paint thickness and layered repaint history;
- impact pitting on storm-facing surfaces;
- streaking aligned with drainage and magnetic fields;
- frost around pressure/temperature transitions;
- grease around bearings, pivots, cable drums and service hatches;
- galvanic variation at mixed-metal joints;
- no uniform procedural grunge.

## 4.4 Palette hierarchy

- 55–65% near-black steel / slag.
- 15–20% oxidised ferric red/brown.
- 8–12% worker/union ochre-yellow.
- 3–6% cold field cyan.
- <3% warning red.
- frost/white only where temperature or exposed pressure justifies it.

These are composition targets, not shader constants.

## 4.5 Lighting

- Drav star: warm/orange directional source, hard enough to reveal industrial relief.
- Heavy ambient attenuation beneath docks/hulls.
- Cold cyan practicals only around magnetic infrastructure.
- Warm sodium-like worker lights inside shelters/workshops.
- Warning red only during polarity/storm/boss telegraphs.
- Wet/greasy highlights restricted to actual lubricant/exposed service surfaces.
- Metal rain must be legible as weather and route pressure without becoming full-screen particle noise.

## 4.6 Sound-to-form linkage

Even though this cell owns 3D, geometry must leave acoustic space for:

- distant impacts on sacrificial roofs;
- tensioned cables;
- crane motors;
- chain slap;
- rail induction hum;
- worker chorus motifs converted into machine signalling.

Large cavities, plates and cable runs should have believable sources for those sounds.

---

# 5. Region architecture

## 5.1 Puerto de las Manos

**Purpose:** social/industrial readability, labour politics, safe-ish onboarding to Vanta systems.

Macro composition:

- low union hall as visual anchor;
- worker workshops arranged around repair yards, not a city grid;
- drydock as central longitudinal void;
- three crane silhouettes define skyline;
- refuges/canteen/infirmary inhabit converted hull modules;
- containers and medicine cargo establish supply conflict;
- strike/belonging layers appear through reversible decals and dressing, not baked into every mesh.

Required hero assets:

- Union Hall;
- primary crane;
- drydock rib system;
- Remolcador Drav;
- magnetic anchor station;
- medicine/supply transfer node;
- Mika/Ciro/Bel character targets.

## 5.2 Lluvia de Hierro

**Purpose:** magnetism becomes traversal language and environmental threat.

Macro composition:

- four major rail corridors;
- field arches crossing the route, each with visible power source;
- scrap channels forming valleys rather than random piles;
- storm beacons at decision points;
- shelters/anchor pads at readable intervals;
- ferrous dust aligns toward active fields to preview state before gameplay UI.

Rule for scrap:

- decorative field = static/instanced;
- stateful scrap cluster = authored alternate transforms;
- hero physics = small bounded pool only;
- no unlimited rigid-body field.

## 5.3 Anillo Caído

**Purpose:** industrial cathedral built from failed orbital infrastructure, but still worker-made and serviceable.

Macro composition:

- drydock spine as primary axis;
- repeated hull ribs create nave-like scale without copying religious architecture literally;
- induction towers pull wreckage into repair positions;
- tug cemetery documents failed logistics;
- FERRUM arena is downstream of the work process, not an isolated boss bowl;
- worker-memory casks are integrated into control infrastructure and become visible narrative evidence.

---

# 6. FERRUM production brief

**Target height:** ~30 m in current silhouette pass.  
**Arena:** 72 m canonical diameter.  
**Readability target:** silhouette recognizable as shipyard machinery at 100 m; attack component recognizable before animation at 35 m; weak/interaction components readable at combat distance.

Functional anatomy:

- root carriage / pelvis;
- four magnetic support legs;
- segmented hull torso;
- induction/polarity core;
- exposed worker-memory cabin;
- sensor head;
- left keel hammer;
- right magnetic handling claw;
- shoulder gantry;
- cable/hydraulic bundles;
- replaceable scrap armour;
- arena anchor sockets.

Required boss production states:

1. rest/maintenance;
2. phase-1 intact;
3. phase-2 polarity damage / partial armour loss;
4. phase-3 memory cabin exposed;
5. disengaged/pacified if narrative path allows;
6. wreck/dead;
7. LOD/HLOD display proxy.

Rig contract:

- explicit root and centre-of-mass control;
- legs/feet with contact controls;
- shoulder/upper arm/forearm/tool chains;
- hammer head and claw tines separately addressable;
- torso armour sockets;
- memory cabin socket;
- cable/hose secondary rig only where silhouette needs it;
- hitbox sockets separated from render geometry.

No simulation-heavy cable solution is accepted without deterministic fallback.

---

# 7. Character / enemy / ecology targets

## NPCs

### Mika Drav
Pilot / worker-ownership advocate. Silhouette must communicate mobility hardware, pilot protection and worker repair culture rather than luxury flight suit.

### Ciro Fenn
Foreman / continuity-of-supply concern. Heavier load-bearing clothing, manifest/coordination tools, visual signs of maintenance responsibility.

### Bel Orta
Scrapper / provenance expert. Tool harness, material sample storage and identifiable ship-part tags; avoid “post-apocalypse scavenger” cliché.

NPC final DoD includes deformation topology, rig, skin/hair/cloth strategy, sockets, LODs, facial/dialogue requirements, collision capsule and engine import.

## Enemies

- **Cobrador de astillero:** shield + mace geometry must telegraph block/commit/recovery.
- **Enjambre de remaches:** shared-mesh instanced agents driven by bounded swarm controller; central field source readable.
- **Remolcador automatizado:** vehicle-like scene enemy with trajectory, anchor points and obvious dangerous mass.

## Biota

- **Litófago magnético:** grounded crawler that metabolises contaminated alloys.
- **Raya de limaduras:** broad gliding silhouette; ferrous particulate relationship visible.
- **Cuervo de remache:** compact tool-using/nest-building bird analogue.
- **Bacteria de escoria:** shader/patch ecology, mostly instanced, no unnecessary skeletal cost.

Every creature must have ecological function, locomotion constraints, habitat placement and LOD/instancing strategy before beauty detail.

---

# 8. Vehicle — Remolcador Drav

Current blockout target: 22 m length, ~8.5 m beam.

Design requirements:

- heavy manoeuvring tug, not fighter silhouette;
- low centre of mass;
- visible magnetic skids/anchors;
- oversized lateral manoeuvring thrusters;
- replaceable armour and tug interfaces;
- pilot visibility compatible with industrial docking;
- docking/maintenance hardpoints readable from exterior;
- optional narrative damage states;
- independent collision primitive set;
- rig for thrusters, docking gear, clamp and doors where needed.

---

# 9. Modelling engineering standard

## 9.1 Units / transforms

- Blender metric, 1 unit = 1 metre.
- Apply scale before export unless a rig/export contract explicitly requires otherwise.
- Forward/up conversion documented at export.
- Pivots at functional hinge, contact or assembly points—not arbitrary bounding-box centres.
- World structures use cell-local coordinates; hero assets use asset-local origin.

## 9.2 Topology

- Silhouette and deformation drive topology.
- Mechanical topology follows manufacturing logic.
- Avoid subdivision on flat industrial surfaces unless the curvature is visible.
- Weighted normals/bevel strategy is acceptable in source, but export behaviour must be tested.
- Bolts/rivets become geometry only when their projected size and parallax justify it; otherwise normal/decal/trim.
- Welds: hero weld geometry only in close interaction; otherwise material/decal.
- Interior unseen geometry removed only after collision/shadow/animation needs are known.

## 9.3 UV / texturing

Three texture strategies:

1. **Trim/tiling** for architecture and high-repeat industrial kit.
2. **Atlas** for props/signage/decals.
3. **Unique** for FERRUM, key vehicle/NPC/enemy hero surfaces.

Texel-density proposal, pending target-hardware calibration:

- environment baseline: 256–512 px/m effective;
- hero environment: 512–1024 px/m;
- hero characters/boss/vehicle close zones: targeted unique density by camera distance, not one global number.

Texture sets must be packed for the selected engine later; do not create engine-specific irreversible source assets now.

## 9.4 PBR calibration

Every material receives:

- albedo range check;
- metallic/roughness semantic check;
- normal scale check at real-world object size;
- close/mid/far review;
- exposure review in neutral light + Vanta production light;
- compression/mip review after engine import.

---

# 10. LOD / HLOD / instancing

No universal triangle budget is claimed before target hardware/engine qualification. We still require deterministic reduction strategy.

Asset tiers:

- **S**: FERRUM, Remolcador Drav, principal region hero setpiece.
- **A**: interaction/high-importance assets.
- **B**: standard gameplay assets.
- **C**: repeated set dressing / distant assets.

Generic ratio targets, subject to visual validation:

- LOD0 = source game mesh.
- LOD1 ≈ retain 55–70% silhouette-relevant complexity.
- LOD2 ≈ retain 20–40%.
- LOD3 / proxy ≈ silhouette + material identity only.
- HLOD = combine static architecture by cell/visibility cluster; never merge interactive parts into an unaddressable blob.

Instancing priorities:

- rails/sleepers;
- hull ribs;
- cable/pipe modules;
- containers;
- scrap-decoration clusters;
- bolts/rivets where geometry is justified;
- biofilm patches;
- storm dressing.

---

# 11. Collision / physics

- Separate gameplay collision from render geometry.
- Hero collision naming follows target-engine import adapter, but source collection remains `11_COLLISION_GUIDES` / per-asset collision group.
- Architecture: simple convex/primitives where possible.
- Traversal surfaces: collision checked from actual player controller after integration.
- FERRUM: hitboxes by attackable/interactive body part, not one giant mesh collider.
- Remolcador: chassis collision + interaction zones; visual pipes/antennae do not become blocking collision.
- Scrap: only designated hero pieces use dynamic rigid bodies. Background scrap is static/instanced or switches authored states.

Mandatory collision gate: visible render success does not qualify traversability.

---

# 12. Magnetic storm state system

Geometry is authored for four visual states:

- **S0 CALM:** mostly static ferrous dust; route fully readable.
- **S1 CHARGE:** beacon/coil activation, dust alignment, cables tension.
- **S2 METAL RAIN:** bounded near debris + dense far/mid representation; anchor affordances highlighted physically.
- **S3 AFTERMATH:** moved hero scrap state, fresh impacts, route consequence.

Implementation must prefer authored state deltas and instancing over thousands of persistent rigid bodies.

---

# 13. Naming / collection contract

Current Blender collections:

```text
00_CONTROL
01_PLANETARY_CONTEXT
02_TERRAIN_MACRO
03_PORT_OF_HANDS
04_IRON_RAIN
05_FALLEN_RING
06_FERRUM_ARENA
07_HERO_BLOCKOUT
08_NPC_TARGETS
09_ENEMY_TARGETS
10_BIOTA_TARGETS
11_COLLISION_GUIDES
12_LIGHTS
13_CAMERAS
14_ROUTE_GUIDES
```

Asset IDs use `VAN_<DOMAIN>_<NAME>[_VARIANT]`.

Object naming prioritises semantic role, not auto-generated Blender names. Every final asset manifest must record:

- asset ID;
- source collection/file;
- canonical/proposed status;
- dimensions;
- pivot contract;
- materials;
- UV strategy;
- LOD/HLOD;
- collision;
- rig/animation when applicable;
- expected instances;
- measured triangles/draws/material slots/textures after production;
- engine import path;
- QA evidence refs.

---

# 14. Complete asset-registry architecture

The Vanta registry generator is maintained in `pipeline/generate_asset_registry.py`. Its current target expands to **327 production rows** covering:

- 36 streaming terrain cells;
- Puerto architecture + social/industrial facilities;
- Lluvia de Hierro traversal/magnetic/storm kit;
- Anillo Caído shipyard and arena infrastructure;
- ~60-piece modular industrial construction kit;
- ~60 props/set-dressing/signage/decal targets;
- 3 NPCs;
- 3 enemy families;
- FERRUM + detailed boss-part breakdown;
- 4 ecology families;
- Remolcador Drav;
- VFX families for weather, magnetism, combat and industry;
- material master families.

Rows are **targets**, not produced-asset claims. A row only becomes DONE after its own DoD passes.

---

# 15. Production state machine

Allowed task/asset states:

```text
BACKLOG
SPEC_LOCKED
BLOCKOUT
SILHOUETTE_APPROVED
HP_MODEL
GAME_MODEL
UV
BAKE
MATERIAL
RIG
ANIMATION
COLLISION
LOD_HLOD
ENGINE_IMPORT
QA_CLOSE
QA_MID
QA_FAR
PERF_MEASURED
DONE
BLOCKED
SUPERSEDED
```

No percentage-complete fields. Track exact state, open gates and receipts.

---

# 16. Definition of Done — every static 3D asset

An asset is DONE only when all applicable checks pass:

- [ ] stable asset ID + purpose;
- [ ] canonical/proposed origin recorded;
- [ ] metre scale verified against human reference;
- [ ] pivot/origin intentional;
- [ ] editable source preserved;
- [ ] mesh naming clean;
- [ ] normals/tangents validated;
- [ ] topology fit for silhouette/deformation/manufacturing logic;
- [ ] UVs validated for overlap policy and texel strategy;
- [ ] PBR material calibrated;
- [ ] texture source/provenance recorded;
- [ ] no accidental extreme material-slot count;
- [ ] collision separate and traversability/interaction tested where applicable;
- [ ] LOD/HLOD or explicit equivalent strategy exists;
- [ ] triangle/material/texture/memory/draw metrics recorded after target import;
- [ ] export reproducible;
- [ ] close/mid/far views reviewed in production lighting;
- [ ] engine import receipt exists;
- [ ] no P0/P1 visual or collision defects remain;
- [ ] branch/manifest/progress updated.

Character/creature additional DoD:

- [ ] deformation topology;
- [ ] skeleton/rig naming;
- [ ] skin weights;
- [ ] sockets;
- [ ] collision capsule/hitboxes;
- [ ] locomotion set;
- [ ] required combat/action clips;
- [ ] root-motion policy;
- [ ] facial/dialogue requirements if applicable;
- [ ] cloth/hair secondary motion fallback;
- [ ] LOD rig strategy.

Boss additional DoD:

- [ ] each telegraphing component readable;
- [ ] phase damage states authored;
- [ ] memory cabin narrative state;
- [ ] attack hitboxes separated;
- [ ] arena collision verified;
- [ ] dynamic scrap budget bounded;
- [ ] rig can reproduce all authored combat windows without impossible intersections;
- [ ] death/pacification/outcome states supported by geometry.

---

# 17. Checkpoints / waves

## CP0 — Ownership lock

**DoD:** branch + Linear ownership + exclusions visible.  
**Status:** DONE.

## CP1 — Canon + scale lock

Tasks:

- VAN-CP1-01 canon extraction;
- VAN-CP1-02 planet-size proposal;
- VAN-CP1-03 24×24 km district partition;
- VAN-CP1-04 4 km streaming cell convention;
- VAN-CP1-05 high-gravity architecture rules;
- VAN-CP1-06 art/material/lighting language.

**DoD:** all values labelled CANON/PROPOSED; no hidden lore mutation.  
**Status:** LOCALLY DOCUMENTED; external art-direction approval unmeasured.

## CP2 — Macro world blockout

Tasks:

- VAN-CP2-01 36 macro terrain cells;
- VAN-CP2-02 Puerto massing;
- VAN-CP2-03 Iron Rain corridor;
- VAN-CP2-04 Fallen Ring massing;
- VAN-CP2-05 72 m arena;
- VAN-CP2-06 route/camera references;
- VAN-CP2-07 scale audit.

**Current receipt:** remote Blender revision 1 produced 255 objects / 245 meshes / 36 terrain cells; arena measured 72 m.

**Status:** BLOCKOUT produced; visual and engine acceptance still open.

## CP3 — Silhouette targets

Tasks:

- VAN-CP3-01 FERRUM functional silhouette;
- VAN-CP3-02 Remolcador Drav;
- VAN-CP3-03 3 enemy families;
- VAN-CP3-04 4 biota families;
- VAN-CP3-05 magnetic anchor hero prop;
- VAN-CP3-06 close/mid/far camera review.

**Current receipt:** Blender revision 2: 388 scene objects; FERRUM composed from 43 named parts; vehicle/enemy/biota proxy families present.

**Status:** SILHOUETTE BLOCKOUT; final art not claimed.

## CP4 — Modular construction kit

- [ ] beams / braces;
- [ ] hull ribs;
- [ ] catwalks / stairs / ladders / railings;
- [ ] floors / grates / walls / doors / hatches;
- [ ] pipe families;
- [ ] cable families;
- [ ] chain/winch/pulley kit;
- [ ] magnet/coil kit;
- [ ] service boxes / vents / fans;
- [ ] deformation/damage variants;
- [ ] snap-grid/pivot validator.

**DoD:** one test yard proves modular assembly, no visible seam pathology, pivots and dimensions deterministic.

## CP5 — Material/trim/decal system

- [ ] final PBR material masters;
- [ ] trim sheets;
- [ ] decal atlases;
- [ ] weld/edge/impact/frost/grease causality review;
- [ ] storm-facing directional weathering;
- [ ] neutral-light calibration board;
- [ ] production-light board;
- [ ] mip/compression test after engine import.

## CP6 — Puerto de las Manos production

- [ ] Union Hall hero pass;
- [ ] drydock hero pass;
- [ ] crane family;
- [ ] workshop/refuge/canteen/infirmary kit;
- [ ] supply/medicine dressing;
- [ ] worker signage/ownership states;
- [ ] traversal collision;
- [ ] LOD/HLOD;
- [ ] close/mid/far composition review.

## CP7 — Lluvia de Hierro production

- [ ] rail corridors;
- [ ] magnetic arches;
- [ ] storm beacons;
- [ ] scrap channel kit;
- [ ] anchor/shelter system;
- [ ] storm visual states S0–S3;
- [ ] bounded dynamic scrap test;
- [ ] readability/accessibility check.

## CP8 — Anillo Caído production

- [ ] drydock spine;
- [ ] hull rib cathedral scale;
- [ ] induction towers;
- [ ] tug cemetery;
- [ ] worker-memory casks;
- [ ] FERRUM approach route;
- [ ] 72 m arena final geometry;
- [ ] phase-state geometry;
- [ ] collision/cover audit.

## CP9 — Characters / enemies / ecology / vehicle

Each target progresses independently through modelling → UV → material → rig if applicable → animation → collision → LOD → engine import → QA.

## CP10 — FERRUM hero production

- [ ] mechanical design lock;
- [ ] high-detail source;
- [ ] game mesh;
- [ ] UV/texture;
- [ ] rig;
- [ ] attack component articulation;
- [ ] hitbox sockets;
- [ ] damage states;
- [ ] memory cabin;
- [ ] bounded secondary simulation;
- [ ] engine integration;
- [ ] arena combat-camera readability.

## CP11 — Lighting / weather / VFX integration

- [ ] Drav directional key;
- [ ] shelter/workshop practicals;
- [ ] magnetic cyan hierarchy;
- [ ] warning red telegraphs;
- [ ] metal rain LOD tiers;
- [ ] ferrous dust preview;
- [ ] impact/spark budget;
- [ ] exposure/fog review.

## CP12 — Optimisation + qualification

- [ ] triangle/draw/material/texture metrics;
- [ ] cell visibility/HLOD;
- [ ] occlusion;
- [ ] instance batching;
- [ ] collision complexity;
- [ ] shader complexity;
- [ ] memory residency;
- [ ] p95/p99 frame-time measurement on declared hardware;
- [ ] navigation/playthrough after integration;
- [ ] visual regression cameras;
- [ ] final creative review.

Only then can this branch describe Vanta art as engine-qualified.

---

# 18. Multi-week execution order

This is sequencing, not a promise of background work.

| Wave | Focus | Exit gate |
|---|---|---|
| W1 | ownership, canon, scale, macroblockout | CP0–CP2 |
| W2 | silhouette targets + modular kit | CP3–CP4 |
| W3 | PBR materials / trims / decals | CP5 |
| W4 | Puerto final art | CP6 |
| W5 | Lluvia final art + storm system | CP7 |
| W6 | Anillo final art | CP8 |
| W7 | characters/enemies/biota/vehicle | CP9 |
| W8 | FERRUM hero + arena | CP10 |
| W9 | lighting/weather/VFX | CP11 |
| W10 | optimisation, import, regressions, art review | CP12 |

Parallelism inside this world is allowed only by asset partition, e.g. `VAN_FERRUM_*`, `VAN_PORT_*`, `VAN_RAIN_*`; two agents must not own the same asset ID simultaneously.

---

# 19. QA cameras

Current source scene defines:

- `CAM_VANTA_MASTER_WIDE` — macro composition;
- `CAM_PORT_QA` — Puerto;
- `CAM_RAIN_QA` — Lluvia;
- `CAM_RING_QA` — Anillo;
- `CAM_ARENA_QA` — FERRUM arena.

Final camera suite must add deterministic close/mid/far captures per hero asset and gameplay-height cameras for navigation/telegraph review.

---

# 20. Current evidence / truth state

As of the first Vanta execution session:

- remote Blender is Blender **5.2.0 LTS**;
- project ID `c82188b1-afdc-43f2-828a-5f0e98291f83`;
- editable `.blend` and portable GLB exist at remote revision 2;
- revision 1 audit: 255 objects, 245 meshes, 8 materials, 15 collections, 36 terrain cells;
- macro visible bounds (excluding hidden planetary proxy): approximately `[-12000,-12000,-32]` → `[12000,12000,667]` metres;
- arena deck dimensions measured `72×72×24 m` including deck depth; canonical playable plan diameter remains 72 m;
- revision 2 adds FERRUM, Remolcador Drav, enemy and biota silhouettes;
- PBR final textures, final topology, rigs, animations, engine integration and performance qualification are **not** complete.

Truth labels:

- World identity / named content: DOCUMENTED CANON.
- Planet radius/diameter: PROPOSED.
- Macro scene: IMPLEMENTED / remote-Blender editable.
- Scale measurements: LOCALLY VALIDATED in Blender.
- Visual quality: BLOCKOUT, not AAA qualified.
- Engine/gameplay/performance: UNQUALIFIED for this branch.

---

# 21. Immediate NEXT queue

1. Persist exact blockout generator under `art_source/vanta/pipeline/`.
2. Generate the 327-row asset registry reproducibly.
3. Persist remote Blender evidence manifest + project URL/revision.
4. Review macro and arena renders; fix camera/lighting if geometry reads poorly.
5. Build CP4 modular kit with shared mesh data and snap/pivot validator.
6. Create neutral PBR calibration board for CP5.
7. Begin one vertical-quality microset: **Puerto crane + anchor + drydock rib + shelter**, not the entire world at final fidelity simultaneously.
8. After microset quality/perf is proven, propagate the validated system to remaining assets.

This protects the project from the failure mode “hundreds of detailed assets before one representative kit passes engine and performance gates.”
