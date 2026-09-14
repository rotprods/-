# PELAGOS · World Production Bible v0.1

Scope: `CLM-PEL-WORLD-001`  
Agent: `AGENT-PELAGOS-01`  
Canonical source: `design/EXOVANT_BIBLIA.md` + `design/EXOVANT_DATA.json`  
Operational status: **IN PRODUCTION / NOT WORLD-DONE**

Epistemic labels used throughout:

- **CANON**: directly represented by current design authority.
- **OBSERVED**: measured from current repository/tool state.
- **DOCUMENTED**: stated by operational/project documentation.
- **INFERRED**: derived from canon without changing it.
- **PROPOSAL**: reversible production decision introduced by this branch.
- **UNKNOWN**: not fixed by current authority.
- **BLOCKED**: requires an external decision/capability before qualification.

---

## 1. Identity

- `world_id`: `pelagos` — **CANON**
- Name: **PELAGOS** — **CANON**
- System: **Talas** — **CANON**
- Star: **Talas, fictional K2 V** — **CANON**
- Galaxy: **Milky Way** — **CANON**
- Faction: **Liga de las Mareas** — **CANON**
- Moon: **Lágrima**, conductive fictional moon affecting tides — **CANON**
- World type: ocean world with reef platforms — **CANON**
- Reference gravity: **0.91 g** — **CANON**
- Reference temperature: **8 °C** — **CANON**
- Core conflict: floating cities migrate following songs no one composed; local life transmits memories through tides — **CANON**
- Core gameplay rule: the reef stores sound; replayed sequences can attract fauna, open membranes or expose the player; collected information belongs to living subjects — **CANON**

Narrative function — **INFERRED FROM CANON**: Pelagos is the Act-I world that makes memory ownership physical. Terra frames land/return, Ares frames energy, and Pelagos turns data extraction into bodily/ecological trespass.

Gameplay function — **INFERRED FROM CANON**: teach acoustic interpretation, controlled vertical traversal, water-adjacent combat, ecological consent and routes that respond to information rather than simple key locks.

---

## 2. Scale contract

### Planetary

- Radius: **6,000 km — PROPOSAL**, ADR-PEL-001.
- Diameter: **12,000 km — PROPOSAL**.
- Circumference: **~37,699 km — DERIVED PROPOSAL**.
- Surface area: **~452.39 million km² — DERIVED PROPOSAL**.
- Mass: **~0.807 Earth masses — DERIVED PROPOSAL** from 0.91 g + proposed radius.
- Axial tilt: **UNKNOWN**.
- Rotation period: **UNKNOWN**.
- Orbital period: **UNKNOWN**.
- Atmospheric pressure/composition: **UNKNOWN**.
- Global mean ocean depth: **UNKNOWN**.

### Authored production space

Current World Foundation rev. 1 uses:

- 1 Blender unit = 1 metre — **OBSERVED WORLD-LOCAL DECISION**.
- L3 master authored cell: **2.2 × 2.2 km — PROPOSAL**.
- Horizontal streaming guides: 500 m cadence — **PROPOSAL**.
- Mean-sea datum at z = 0 m — **PROPOSAL**.
- Authored bathymetry current range: approximately z −199 m to +100 m including structures — **OBSERVED**.
- THALASSA arena: **52 m diameter — CANON**.

Planet scale never authorizes full-surface L5 density.

---

## 3. Macrogeography

### Canon regions

1. **Mercado de Boyas** — mobile population and floating assemblies.
2. **Coro del Arrecife** — channels that retain memory.
3. **Fosa de las Mil Miradas** — sanctuary of THALASSA.

### Production macro layout — PROPOSAL

The three canonical regions form one readable traversal triangle:

- Mercado: western human/social anchor, approximately `(-520,-80)` m.
- Coro: central ecological/acoustic anchor, approximately `(0,40)` m.
- Fosa: eastern/deep sacred anchor, approximately `(520,230)` m.

The topography is organized as:

- shallow mobile-market shelf;
- reef uplift around the Coro;
- sharply descending trench/funnel at the Fosa;
- secondary submerged saddles and channels reserved for Nácar-2 traversal.

Global continents: **UNKNOWN / likely non-applicable as Earth-like continental framing**. Pelagos should be described primarily through basins, reef shelves, thermal/mineral ridges, current corridors and emergent platform archipelagos until global geology is approved.

Tectonics: **UNKNOWN**. Do not fake plate maps before a geological decision record.

---

## 4. Climate and environmental physics

Reference-area temperature 8 °C is **CANON**. The following are **PROPOSALS** designed to make the art physically causal without changing story canon:

- high ambient humidity and continuous salt aerosol near exposed platforms;
- frequent low cloud / marine haze rather than permanently clear skies;
- wind loading is a primary architecture driver;
- tide amplitude locally amplified by Lágrima and reef geometry;
- material weathering dominated by salt crystallization, wet/dry cycling, galvanic corrosion and biological fouling;
- underwater visibility varies by current and biological activity; not uniform cinematic blue fog.

Precipitation rate, prevailing wind, seasonality and storm statistics remain **UNKNOWN** and must not be encoded as global canon yet.

---

## 5. Biome system

### B01 · Floating settlement shelf

- substrate: water surface over reef/mineral shelf — **INFERRED**;
- dominant structures: buoy platforms, articulated bridges, flexible canopies, moorings — **PROPOSAL based on Mercado canon**;
- palette: ivory repaired ceramic/composite, dark technical textiles, oxidized bronze, amber refuge signals;
- physical wear: tide-line deposits, salt bloom, rope/cable abrasion, impact dents around docking edges, UV chalking on exposed membranes;
- fauna pressure: opportunistic reef grazers and memory carriers around quieter infrastructure;
- settlement logic: structures must move, flex, detach or be towed rather than pretending to be land foundations.

### B02 · Mnemonic reef / Coro

- substrate: living reef structures that respond to vibration — **CANON/INFERRED**;
- dominant shapes: branching load paths, acoustic arches, cavities and ring structures — **PROPOSAL**;
- palette: green-grey living tissue/mineral, pale calcified surfaces, pale cyan memory emission;
- wear/growth: accretion and repair rather than human scratches; interfaces show where human hardware clamps or wounds living surfaces;
- settlement logic: human circulation should avoid turning the reef into conventional corridors; paths read as negotiated interfaces.

### B03 · Trench sanctuary / Fosa

- substrate: steep bathymetric descent — **INFERRED**;
- dominant structures: anchors, pressure-rated access, observation/maintenance columns, dry refuge platforms — **PROPOSAL constrained by canonical arena**;
- palette: black mineral, old bronze, pale colonial inserts, cyan living sensors, bermellion only for hostile intent;
- weathering: pressure, mineral deposition, biological film, low-light adaptation;
- gameplay: legible descent with recoverable anchors; no mandatory precision free-swim combat before it is separately validated.

---

## 6. Ecology

Canonical ecology:

### Medusa mnémica

- ecological role: carrier/transmitter of luminous memory — **CANON**;
- design rule: not a free battery/resource; visual design must communicate agency/ownership — **CANON**;
- locomotion proposal: low-frequency bell contraction with long compliant tentacles;
- material proposal: translucent tissue with internal particulate channels; avoid generic hologram jellyfish.

### Anguila de vidrio

- ecological role: predator following repeated sound — **CANON**;
- adaptation proposal: lateral-line-like resonant organs and low-reflectance transparent/mineral tissue;
- combat/behavior silhouette: long directional body; readable pre-charge bend rather than random serpentine noise.

### Bóvido de arrecife

- ecological role: grazes to keep channels open — **CANON**;
- adaptation proposal: broad low centre of mass, distributed gripping limbs/feet, scraping mouth architecture;
- production rule: body plan must justify grazing and stability, not merely resemble an Earth cow with coral.

### Coral escriba

- ecological role: incorporates vibration into growth — **CANON**;
- art logic: growth history becomes geometry; repeated acoustic events leave causal branching/ridging patterns;
- production opportunity: deterministic Geometry Nodes system, bakeable to game meshes.

### Food-chain / interaction state

Detailed trophic chain, reproduction cycles and population densities are **UNKNOWN**. Until defined, assets should encode function and habitat without inventing a complete ecology as canon.

---

## 7. Civilisation and material history

Liga de las Mareas controls/mediates routes and aquatic memory — **CANON**.

### Human/settler manufacturing language — PROPOSAL aligned with global EXOVANT grammar

- repair-first objects; replacement panels are visible rather than hidden;
- ivory technical ceramic/composite shells over corrosion-resistant structural frames;
- dark flexible textiles/membranes where movement and spray demand compliance;
- standardized maintenance interfaces with non-decorative fasteners;
- bronze/old precursor material is not copied cosmetically onto human parts; contact zones reveal adapters, clamps and misfit tolerances.

### Economic/material logic

Pelagos cannot use “sci-fi metal everywhere.” Buoyancy mass, corrosion, maintainability and field repair drive material choice. Heavy components sit low; light occupancy/canopy components sit high. Cable runs, ballast, drainage and access routes must be modeled when relevant.

---

## 8. Architecture

### Mercado de Boyas

Structural system — **PROPOSAL**:

- polygonal/semi-circular floating decks on buoyancy keels;
- tension/compression canopy masts;
- articulated bridges with visible joints;
- mooring and storm-release points;
- modular service spines for water, power, data and acoustic routing.

Module families required:

- primary buoy platform 60–90 m class;
- secondary platform 30–60 m;
- docking finger;
- articulated bridge straight/hinged;
- mast and membrane canopy;
- ballast/keel;
- utility riser;
- refuge light/hydrophone mast;
- market shell/stall cluster;
- maintenance hatch/interior pressure vestibule.

Current rev. 1 geometry is a **massing blockout**, not a final modular kit.

### Coro del Arrecife

Architecture is mostly ecological interface, not conventional building. Required families:

- acoustic arch;
- resonance ring;
- living memory node;
- clamp/interface platform;
- non-destructive walkway;
- hydrophone/listening station;
- ritual/negotiation area for Téa;
- membrane gateway that reacts to sound.

### Fosa / THALASSA

Required families:

- trench rim and descent collar;
- anchor tower/cable socket;
- pressure transition chamber;
- maintenance column used for line-of-sight gameplay;
- dry platform system;
- drainage/ventilation manifold;
- boss-arena floor/ring;
- extraction-link hardware whose severance is physically legible.

### Interiors

Only interiors required by missions should be authored at first: market control/medical/service interiors, acoustic translation room, memory containment/extraction space, pressure transition and arena maintenance spaces. Generic full-city interiors are **DEFERRED** until player routes demand them.

---

## 9. Transportation

### Pedestrian

- flexible bridges and dry decks;
- ladders/ramps/pressure access where needed;
- submerged routes must not silently change core dodge timing; movement rules require gameplay ownership.

### Water vehicle: Nácar-2 — CANON NAME/FUNCTION, PROPOSED DIMENSIONS

Current blockout: roughly 15 m long × 6.4 m wide × 5.4 m hull/canopy envelope.

Functional design requirements before hero modeling:

- propulsion: twin independently serviceable water thrusters — **PROPOSAL**;
- steering: differential thrust + control surfaces — **PROPOSAL**;
- braking/hold: reversible thrust + anchor/hold system — **PROPOSAL**;
- energy storage: **UNKNOWN**;
- pressure rating: **UNKNOWN**;
- cockpit: two seats; solo operation must remain possible — **CANON FUNCTION**;
- access: top/side hatch must be modeled and animated;
- cargo: maintenance/memory-recovery payload space — **PROPOSAL**;
- sensors: acoustic navigation/hydrophone array — **INFERRED/PROPOSAL**;
- damage zones: canopy, thrusters, fins/control surfaces, pressure hull, sensor array — **PROPOSAL**.

---

## 10. Characters and population

Canonical principal NPCs:

- **Nara Océano** — amphibious biologist; wants contact without extraction.
- **Damián Vo** — buoy captain; needs a commercial channel.
- **Téa del Coro** — reef interpreter; shares memory partially.

Production rule: none may resolve as “same human body + different colored suit.” Final character work must define age, body type, adaptation/prosthetics if any, occupation-specific wear, pressure/water interfaces, wardrobe construction, hair/skin behavior in humid/wet contexts and distinct silhouettes.

Current rev. 1 uses scale/silhouette proxies only.

---

## 11. Enemies

Canonical:

- **Buzo de extracción** — harpoon with cuttable cable.
- **Guardia de pólipos** — guards acoustic zones and retreats before learned dissonance.
- **Anguila centinela** — charges between anchors with visible route.

Art/realism contract:

- Buzo equipment must look pressure- and corrosion-designed; cable spool, harpoon launch path and cuttable segment must exist mechanically.
- Guardia de pólipos must have an ecological/defensive anatomy and a readable acoustic response organ.
- Anguila centinela charge path needs pre-attack body compression/alignment visible at gameplay distance.

---

## 12. THALASSA

Name: **THALASSA, coral de los mil ojos** — **CANON**.

Arena: **52 m floodable chamber with maintenance platforms and anchors; precise free-swim combat must not be mandatory before validation** — **CANON**.

Phases:

1. 100–70%: exploratory eyes reveal the player between pillars.
2. 70–35%: alternates flooding in two sectors and closing tentacles.
3. 35–0%: the chorus responds to restored memory and can allow severing the extraction link.

Representative attacks:

- Convergent gaze: three eyes lock light for 1.2 s; break line with a column.
- Current whip: tentacle telegraphs from outside for 0.9 s; enter the interior pocket.
- Pressure song: membranes expand for 1.6 s; move to a ventilated platform.

Current rev. 1 implements only silhouette/readability blockout: central body, 18 eye proxies, 8 tentacle curves, 8 LOS columns, 4 dry platforms. It is **not rigged or encounter-qualified**.

Hero production requirements:

- organism/manufactured-interface anatomical map;
- internal support logic for coral mass;
- eye hierarchy: scanning, aiming and damaged states;
- tentacle root mechanics and deformation zones;
- flood/pressure membranes;
- extraction-link hardware as a separate destructible/interactive asset;
- rig with stable deformation under large sweeps;
- collision/hitbox separation by gameplay function;
- close/medium/far silhouette gates.

---

## 13. Missions and physical asset implications

Main chain — **CANON**:

- `Q_PELAGOS_M01` Ciudad a la deriva — stabilize a platform / learn suit breathing.
- `Q_PELAGOS_M02` La memoria de la sal — record reef calls, distinguish greeting/alarm.
- `Q_PELAGOS_M03` Traducir una marea — recover stolen memory without destroying containing coral.
- `Q_PELAGOS_M04` Los mil ojos de THALASSA — descend via anchors and confront THALASSA with dry zones.
- `Q_PELAGOS_M05` La voz del océano — negotiate channel use and memory restitution.

Side quests — **CANON**:

- El nombre prestado — borrowed childhood memory.
- La boya funeraria — audible funeral signal for humans and reef.

Required storytelling props therefore include, at minimum: hydrophones, memory recording/containment hardware, intact/damaged extraction apparatus, funeral buoy, trading-channel navigation signals, consent/timetable markers, reef-safe clamps and archive/memory custody containers.

---

## 14. Consequences and state variants

Canonical outcomes:

- **Canal comercial**: market prospers; reef loses privacy.
- **Tratado de consentimiento**: scheduled transit + data restitution; requires intact archives.
- **Reserva marina**: trade rerouted; fauna restored; one NPC abandons business.

World production implication: Mercado, Coro and navigation assets need state-ready variants or parameterized dressing. The choice cannot be represented by a dialogue flag only.

Secret: voices sold by the market as ambience are memories of living subjects — **CANON**.

Reward: **Lente de memoria**, reveals hidden resonances and modifies sonic tools — **CANON**.

---

## 15. Art direction contract

### Pillars

1. **Habitable ocean engineering, not generic underwater sci-fi.** Everything human must answer buoyancy, pressure, salt and maintenance.
2. **Memory is physical but not holographic shorthand.** Cyan light is a signal layered on tangible tissue/mineral/optical mechanisms.
3. **Living architecture has causal growth.** Coral branching and cavities should imply load, flow, feeding and accumulated vibration.
4. **Consent versus extraction is visible in interfaces.** Clamps, cuts, cables, scars and careful non-destructive attachments reveal ethics before dialogue.
5. **Verticality remains readable.** Water never becomes permission for camera chaos or scale ambiguity.

### Shape language

- human: segmented buoyant discs, ribs, masts, articulated hinges, pressure shells;
- precursor/network: oxidized bronze rings/load paths and black mineral anchors;
- living reef: branching/porous curved structures following growth and flow;
- hostile/extractive: taut lines, spears, clamps and constrained geometry rather than random spikes.

### Proportion language

- occupancy volumes remain human-readable through doors/hatches/handrails/maintenance clearances;
- large platforms show buoyancy depth and structural support, not infinitely thin slabs;
- reef hero forms use repeated scale reference from human/Nácar-2 assets;
- THALASSA must dominate a 52 m arena but leave readable player pockets and LOS columns.

### Palette / signal semantics

Global EXOVANT meanings remain:

- amber = refuge;
- pale cyan = memory;
- vermilion = hostile intent;
- cold white = colonial authority.

Pelagos material dominant: black wet mineral + muted living green/grey + repaired ivory human shells + aged bronze interfaces. Signal colors must be redundant with shape/sound, never sole mechanics.

### Forbidden drift

- tropical turquoise resort look;
- random neon cyberpunk;
- Bioshock-style retro underwater imitation;
- Earth coral copied one-to-one without functional adaptation;
- generic “alien tentacle” noise;
- floating buildings with no ballast/mooring/maintenance logic;
- perfect clean white sci-fi surfaces;
- every surface wet/glossy at the same roughness;
- decorative bubbles/bioluminescence used to hide weak geometry.

---

## 16. Material and wear contract

World material families:

- `PEL_Human_IvoryCeramicComposite`;
- `PEL_MarineStructuralMetal`;
- `PEL_AgedBronzeNetwork`;
- `PEL_BlackMineralSubstrate`;
- `PEL_TechnicalMembrane`;
- `PEL_LivingCoralTissueMineral`;
- `PEL_OpticalMemoryTissue`;
- `PEL_PressureGlass`;
- `PEL_RopeCablePolymer`;
- `PEL_SaltBiofouling`.

Wear causality:

- splash/tide lines form by water level and drainage;
- salt deposits accumulate at evaporation edges/recesses;
- galvanic corrosion follows dissimilar-metal interfaces;
- handling polish appears at hatches, rails, controls and service fasteners;
- impact wear concentrates at docks/anchors;
- biological growth favors low-maintenance/static wet surfaces;
- heat wear appears only around actual power/drive components.

No uniform procedural edge-wear pass qualifies as final surfacing.

---

## 17. Procedural systems

Recommended world-local systems:

- coral growth generator driven by branch hierarchy, flow direction, age and acoustic-history parameters;
- buoy settlement assembly from platform/bridge/mast/utility modules;
- cable/mooring generator with tension-aware sag constraints;
- biofouling/salt mask generation derived from orientation, waterline and exposure;
- bathymetry tile generator separating geological macroshape from gameplay sculpt;
- acoustic-node scatter constrained by reef surfaces and mission readability.

All procedural output must be bakeable/exportable and produce deterministic seeds stored with assets.

---

## 18. Streaming / LOD strategy

Final engine-specific technology remains **BLOCKED by production engine qualification**, so this Bible specifies interfaces, not Unreal/Godot-exclusive implementation.

- planet representation and authored geometry are separate;
- authored world is partitionable into stable metre-space cells;
- hero zones expose their own HLOD/proxy boundary;
- repeated coral/platform modules should use shared meshes/instances where engine supports them;
- distant reef mass becomes silhouette/HLOD, not millions of individual coral colonies;
- water rendering is treated as a rendering system, not duplicated high-density geometry.

LOD budgets remain measured-per-class after representative engine import; no universal triangle limits are invented here.

---

## 19. Current build receipts

3D project: `39930c08-62bb-4034-b35d-70d0ce51c9d9`  
Project name: `EXOVANT 2950 — PELAGOS World Master — ART-PELAGOS-001`  
Committed scene revision: **1**  
Checkpoint: `PELAGOS-WF-001`

Observed rev. 1:

- 268 Blender objects;
- 139 mesh objects;
- 121 curve objects;
- 11 material roles;
- 49,320 raw mesh triangles before curve export tessellation;
- no mesh missing an asset ID;
- no mesh with non-unit object scale;
- no mesh without a material;
- no negative/zero object dimensions;
- GLB and `.blend` exported by the remote scene builder.

These receipts qualify **world foundation blockout only**.

---

## 20. World DoD

PELAGOS remains **NOT DONE** until the project-wide world DoD is met: planet metadata decision, macro geography, terrain, biomes, materials, ecology, architecture, necessary interiors, infrastructure, landmarks, props, population, creatures, vehicle, storytelling state variants, decals/destruction where needed, vista assets, LOD/collision/streaming strategy, measured performance, runtime integration, art coherence, QA and documentation.

No beauty render or Blender-only export can override those missing gates.
