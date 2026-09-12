# UMBRA — World Bible · ART-UMBRA-001

Status: `WAVE 0 / CANON LOCK + BLOCKOUT`. World: `WORLD-04 / UMBRA`. Claim: `CLM-W04-WORLD-UMBRA-001`. Agent: `AGENT-UMBRA-04`.

This file deliberately separates repository canon from reversible production proposals. A proposal is not promoted to canon by being modeled.

## 1. Identity

### CANON
- Name: **UMBRA**.
- Boss/function figure: **NOCTIL, el eclipse viviente**.
- Galaxy: **VÍA LÁCTEA**.
- System: **Sere**.
- Primary: fictional **M4 V red dwarf**.
- Faction: **Flotilla de los Sin Sol**.
- Planetary condition: fictitious synchronous rotation; settlements concentrate in the twilight band.
- Orbital infrastructure: a small swarm of reflector stations.
- Reference gravity: **0.81 g**.
- Reference area temperature: **−87 °C**.
- Exosuits may compensate movement load where communicated; dodge timing must not silently change between worlds.
- Observer language: `Ojo Quieto` and `Esposas del Alba` are Flotilla drawings; Sere remains almost fixed in the sky.

### UNKNOWN / BLOCKED
- Physical planet radius and diameter.
- Total surface area.
- Exact orbital period, atmospheric chemistry/pressure and tidal-lock age.
- Global continental map and hydrology.
- Production-engine world-partition/streaming contract.

No numerical value is assigned to these until canon or an approved technical ADR defines it.

## 2. Narrative and gameplay function

### CANON
Core rule: **light and shadow are navigation permissions as well as temperature states**. Activating a reflector can reveal routes while exposing caravans to surveillance.

Known quest chain:
1. `Q_UMBRA_M01 — La frontera del día`: find the caravan by reading temperature and tracks.
2. `Q_UMBRA_M02 — Sombras que respiran`: adjust a reflector to save a convoy without revealing its entire route.
3. `Q_UMBRA_M03 — Geometría del eclipse`: recover records proving deliberate exclusion of returned people.
4. `Q_UMBRA_M04 — El refugio de NOCTIL`: ascend to the crown and fight NOCTIL's mechanism.

### PRODUCTION CONSEQUENCE
Every environment kit must support at least one of four readings: thermal safety, route readability, surveillance exposure, or wind adaptation. Decoration with no relation to those systems is low priority.

## 3. Art-direction contract

### CANON
- Environment kit: **mobile twilight — caravans, reflectors, dark ice and tensioned fabric**.
- Sound: constant lateral wind, tensioned tarps and caravan radio with meaningful silences.
- Visual risk: darkness must never hide combat anticipation; low-brightness and color-vision profiles require explicit validation.
- Global EXOVANT continuity: amber = refuge, pale cyan = memory, vermilion = hostile intent, cold white = colonial authority; color is never the only signal.

### PROPOSAL — shape language
- Primary massing: low horizontal wind-shedding bodies and long traversal lines.
- Secondary hierarchy: thin vertical reflector masts and anchored pylons.
- Tertiary accents: tension triangles, cable arcs, service collars and field-repair plates.
- NOCTIL environment motif: eclipse/concentric-ring silhouettes used sparingly around the boss route, not across all assets.
- Forbidden drift: generic neon cyberpunk, decorative random greebles, mirror panels without thermal/optical function, uniform edge wear, high-frequency sci-fi noise, ornamental spikes unrelated to wind/structure.

### PROPOSAL — proportion language
- Habitable mobile modules should read as compressed and sheltered rather than tall.
- Reflectors can exceed settlement height by an order of magnitude, making light-control infrastructure the skyline.
- Access points, ladders and service rails must preserve human scale even inside monumental infrastructure.

## 4. Material and manufacturing families

### CANON-DERIVED / PROPOSAL IMPLEMENTATION
1. `MAT_UMBRA_DARK_ICE`: low-albedo ice/mineral substrate; erosion and directional ablation follow the lateral wind.
2. `MAT_SINSOL_DARK_METAL`: welded/extruded structural metal, darkened for thermal/optical management; field repairs visible.
3. `MAT_REFLECTOR_MIRROR`: highly controlled reflective surface only on optical/thermal reflector elements.
4. `MAT_SINSOL_TENSION_FABRIC`: cold-rated tension membrane; anisotropic wear expected at anchors and fold lines.
5. `MAT_COLONIAL_IVORY_REPAIR`: inherited EXOVANT human ceramic/repair language used as a trace of colonial manufacturing, not as the dominant world color.
6. `MAT_REFUGE_AMBER`: refuge light/signalling material; geometry/sound must duplicate the semantic cue.
7. `MAT_HOSTILE_VERMILION`: hostile cue for boss-space validation; never the sole telegraph.

Manufacturing realism: masts require base plates/anchors, service collars and maintenance access; caravan shells attach to a load-bearing chassis; tensioned fabric requires defined anchor points; mirror assemblies require aiming/actuation interfaces.

## 5. Wear causality

- Constant lateral wind → directional abrasion, polished windward edges, deposition in leeward cavities.
- Ice/dust mixture → streaks and packed material at ground contact, not isotropic grime.
- Caravan use → track/runner wear, access-step wear, service-panel handling marks and localized grease.
- Reflector maintenance → clean optical zones contrasted with dirty mounts and actuator housings.
- Thermal cycling → seams, gaskets and repair compounds become visually important.

## 6. Planet-scale representation

### L0 — planetary canon
`RADIUS = UNKNOWN`. Logical world condition = synchronous/twilight band. Do not author a fake 1:1 radius.

### L1 — orbital representation
BLOCKED until radius/orbit/atmosphere are decided. Only reflector-swarm concept/interface may be specified.

### L2 — region
Current authored testbed is a **PROPOSAL**: `1200 m × 700 m`, designed to validate traversal, reflector hierarchy, caravan scale and a boss-destination silhouette. It is not the world's total playable area.

### L3 — gameplay cells
Planned cell families:
- thermal-track approach / Q_UMBRA_M01;
- convoy/reflector decision space / Q_UMBRA_M02;
- archive/exclusion evidence space / Q_UMBRA_M03;
- ascent/crown/NOCTIL space / Q_UMBRA_M04.

### L4 — hero zones
First candidate: reflector-refuge/caravan testbed plus NOCTIL destination proxy. Hero density is deferred until camera/navigation and art language survive blockout review.

### L5 — hero assets
Reflector control assembly, caravan command module, archive evidence unit, NOCTIL encounter infrastructure and selected hero props. Final NOCTIL creature/character design is not claimed by this blockout.

## 7. Macro geography and climate

### CANON
- Habitation logic is tied to a twilight band on a synchronously rotating world.
- Constant lateral wind is an art/sound constraint.
- Reference area temperature is −87 °C.

### PROPOSAL
- Terrain language for the first gameplay region uses shallow wind-carved ice/mineral relief with a leeward ridge line rather than tall chaotic mountains.
- Routes follow serviceable hardpack/compacted surfaces between reflector and caravan nodes.
- Global tectonics, oceans and continent count remain undefined.

## 8. Settlement and infrastructure logic

### PROPOSAL derived from canon mechanics
- Settlements are partly mobile because thermal/light availability and surveillance risk can move.
- Reflector towers are both infrastructure and tactical switches; they must be readable from long distance.
- Refuge hubs use lower silhouettes and wind-shedding shells.
- Windbreak pylons, fabric anchors, cable systems and maintenance collars are structural storytelling, not decoration.
- Roads are not assumed; early routes are hardpack/service tracks until transport canon expands.

## 9. Ecology

`BLOCKED / UNDEFINED IN CANON` for detailed native species. Do not populate generic alien flora/fauna. Allowed current work: abiotic ice/mineral substrate, human habitation traces and explicit proxy slots for later ecology claims.

## 10. Characters / population

Faction identity is CANON; final population design is not yet specified here. Population assets must eventually encode role, cold adaptation, mobility and social access to light/refuge. Crowd cloning with only clothing swaps is forbidden.

## 11. Vehicles

Current caravan vehicle geometry is a **PROXY**. Mechanical requirements for production vehicles: propulsion suitable for low-temperature terrain, steering/braking/cooling or heating rationale, energy storage, service access, cargo/refuge interfaces and damage zones. No drivetrain technology is canonized in Wave 0.

## 12. NOCTIL contract

CANON: NOCTIL is the world boss/function figure and Q_UMBRA_M04 leads to its refuge/crown encounter.

Current model: an **environmental eclipse-ring destination proxy only**. It intentionally does not invent NOCTIL anatomy, rig, attacks or final scale. Final boss design requires a separate anatomy/function/telegraph contract and collision/animation ownership.

## 13. Camera, lighting and readability

- Third-person readability outranks atmospheric darkness.
- Sere key light is low-angle, warm/red; cold horizon fill separates silhouettes.
- Refuge amber and hostile vermilion are local cues, always duplicated by geometry/position/animation/sound in final gameplay.
- Beauty render is not approval. Required views: game camera, scale view, orthographic/plan, wireframe, material breakdown, in-engine camera once import exists.

## 14. Wave-0 measurable target

A successful Wave 0 checkpoint contains:
- one isolated ownership branch/path;
- one dedicated editable Blender project;
- metric scene and deterministic hierarchy;
- one 1200×700 m authored regional blockout clearly marked PROPOSAL;
- at least 4 reflector tower proxies;
- at least 5 caravan proxies;
- one refuge hub;
- one NOCTIL arena/destination proxy;
- human and vehicle scale references;
- two validation cameras;
- structural QA with zero residual object scale anomalies and zero zero-dimension meshes;
- editable `.blend`, portable `.glb`, preview receipt and manifest;
- no claim of planet radius, AAA completion, Unreal integration or GPU performance without evidence.

## 15. DoD for world completion

UMBRA remains incomplete until planetary metadata, authored regions, terrain, materials, required ecology, architecture, infrastructure, landmarks, props, population, creatures, vehicles, story assets, decals/destruction, vistas, LOD/collision/streaming, performance, engine integration, art-coherence review, accessibility/readability review and documentation all pass or receive explicit waivers.
