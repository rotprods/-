# KHEPRI — World Bible shard

**World ID:** `khepri`  
**Authority inputs:** `design/EXOVANT_BIBLIA.md`, `design/EXOVANT_DATA.json`  
**Purpose:** recoverable world-context shard for parallel 3D production. This file does not replace canonical design data.  
**Epistemic rule:** every item is labeled CANON/DOCUMENTED, DOCUMENT_DERIVED, PROPOSAL or UNKNOWN.

## Identity

- **Name:** KHEPRI — DOCUMENTED.
- **Galaxy:** ANDRÓMEDA — DOCUMENTED.
- **System:** Sahra — DOCUMENTED.
- **Primary:** Sahra, fictional F8 V star — DOCUMENTED.
- **Faction:** Sínodo de Bronce — DOCUMENTED.
- **Boss:** RA-KHET, sol encadenado — DOCUMENTED.
- **Narrative act:** Act II / *El derecho a nombrar* — DOCUMENTED.
- **Conflict:** a robotic civilization treats irreplaceable parts as sacred while its artificial-star infrastructure ceases to obey reliably — DOCUMENTED.
- **Core world rule:** light stores both energy and rights of use; orienting mirrors changes temperature, doors and district supply — DOCUMENTED.

## Scale

- **Surface gravity:** `0.63 g` — DOCUMENTED.
- **Reference authored-area temperature:** `71 °C` — DOCUMENTED.
- **Physical radius / diameter / mass / mean density:** UNKNOWN in canon.
- **KHP-ADR-001 production proposal:** radius `5,224 km`, diameter `10,448 km`, mass `~0.4235 M_E`, density `~4.23 g/cm³` — PROPOSAL / REVERSIBLE.
- **Authoring unit:** `1 Blender Unit = 1 metre` for the current verified Blender pipeline — LOCAL TECHNICAL CONTRACT.
- **Current representative macro-cell extent:** `6.4 km × 4.8 km` — PROPOSAL for pipeline validation; not final playable acreage.

## Planetary / orbital context

- **Surface concept:** solar-glass desert with cities under heliostats — DOCUMENTED.
- **Orbital bodies/infrastructure:** Aguja reflector station and two fictional rocky moons — DOCUMENTED.
- **Atmospheric composition/pressure:** UNKNOWN.
- **Axial tilt / day length / orbital eccentricity:** UNKNOWN.
- **Global continental map:** UNKNOWN.
- **Ocean fraction:** UNKNOWN. **Mar de Cristal** is a DOCUMENTED named surface region, but whether its physical medium is literal liquid, vitrified terrain or another optical substrate remains UNKNOWN and BLOCKED FOR FINAL MATERIAL INTERPRETATION.

## Macrogeography

### Documented functional requirements

Mission design requires a spatial chain that can support:

1. communal shade / inhabited area where the player learns the price of light;
2. a “sea” crossing with reflector route and subterranean alternative;
3. a crucible/industrial debt site;
4. RA-KHET encounter space with beam redistribution nodes;
5. visible infrastructure whose ownership/maintenance can change in the aftermath.

These are **DOCUMENT_DERIVED functional regions**, not final region names or layouts.

### Canonical named surface regions

Recovered directly from `design/EXOVANT_BIBLIA.md`:

- **Ciudad de los Toldos** — talleres y deuda energética — DOCUMENTED.
- **Mar de Cristal** — campos de reflexión y rutas de sombra — DOCUMENTED.
- **Crisol de RAKHET** — máquina solar encadenada — DOCUMENTED.

These names/functions are canon-level design inputs. The current macro coordinates remain PROPOSAL interfaces and do not claim final architecture or regional boundaries.

### Current world-macro interfaces

The world-macro cell publishes only route interfaces:

- `KHP_WM_ROUTE_SHADE`
- `KHP_WM_ROUTE_GLASS_SEA`
- `KHP_WM_ROUTE_CRUCIBLE`
- `KHP_WM_ROUTE_RAKHET`

Their current positions are PROPOSAL blockout coordinates and may change during level-design/architecture ownership review.

### Unknown geology

Tectonics, crustal composition, dune/glass formation mechanism, mountain systems, valleys, caverns and erosion chronology are UNKNOWN. Detailed geological sculpt must not reverse-engineer lore from visual convenience without an ADR.

## Climate

- **Heat:** `71 °C` is the recovered reference for the authored area — DOCUMENTED.
- **Humidity:** UNKNOWN.
- **Precipitation:** UNKNOWN.
- **Wind regime:** UNKNOWN.
- **Seasonality:** UNKNOWN.
- **Erosion drivers:** solar/thermal stress is a plausible design direction but remains PROPOSAL until canonized.

## Biomes

Canonical biome taxonomy is not fixed in the recovered source. Current production may use functional macro placeholders only:

- solar-glass desert — DOCUMENTED surface identity;
- heliostat shadow zones — DOCUMENT_DERIVED from cities under heliostats;
- subterranean route environment — DOCUMENT_DERIVED from mission routing;
- crucible industrial thermal zone — DOCUMENT_DERIVED from mission routing.

Biome taxonomy, soil ecology, population distribution and the complete food-chain structure remain UNKNOWN; documented KHEPRI species are listed under Ecology below.

## Civilization — Sínodo de Bronce

### Documented cultural/material cues

- irreplaceable mechanical parts have sacred/social importance;
- light distribution is simultaneously infrastructure and property/right;
- debt and inherited access rights matter to quests;
- KHEPRI visual kit is “crystal and shadow”: fabrics, mirrors, scorched ceramic, prisms and walkways;
- glass bells, resonant cables and solar-tracking motors define the recovered sound language.

### Unknowns

Manufacturing standards, body morphology of the robotic civilization, exact settlement hierarchy, domestic life, governance structure beyond the faction label, iconographic grammar and maintenance rituals require domain-owner elaboration.

## Architecture

**Not owned by `CLM-KHEPRI-WMACRO-001`.** Architecture agents should consume the route/cell interfaces but own final geometry.

Required categories to resolve:

- residential — UNKNOWN / UNCLAIMED;
- civic/commercial — UNKNOWN / UNCLAIMED;
- industrial/crucible — function DOCUMENTED, final architecture UNCLAIMED;
- religious/ritual — cultural need inferred from Sínodo context, final form UNKNOWN;
- military/security — UNKNOWN;
- infrastructure — heliostats, mirrors/prisms, shade and energy routing are DOCUMENTED functions; final kits UNCLAIMED;
- ruins — UNKNOWN;
- interiors — UNKNOWN.

## Transportation

- **Helioperegrino** — moto de vela solar de superficie — DOCUMENTED local vehicle.
- Walkways are part of the documented KHEPRI asset-kit language.
- Broader pedestrian/road/rail/air/orbital transport hierarchy remains UNKNOWN/UNCLAIMED; the documented Helioperegrino does not authorize inventing a complete transport network.

## Ecology

Recovered canonical biota from `design/EXOVANT_BIBLIA.md`:

- **Escarabajo heliostato** — orients its shell to regulate heat — DOCUMENTED.
- **Zorro de vidrio** — refracts its outline without becoming invisible — DOCUMENTED.
- **Serpiente de cable** — lives among cooled collectors — DOCUMENTED.
- **Liquen de prisma** — fixes minerals in areas of dispersed light — DOCUMENTED.

These species unblock an ecology claim, but they do **not** yet define a complete trophic web, reproduction, population density, biome distribution, animation/rig or gameplay statistics. Future ecology production must preserve the documented functions and mark any predator/resource/decomposer relationships beyond them as PROPOSAL until separately canonized.

## Characters / population

Documented named NPC anchors:

- **Hermana Asha** — mecánica del Sínodo; busca abolir deuda heredada — DOCUMENTED.
- **Qadir Noé** — mercader; financia reparaciones que nadie quiere pagar — DOCUMENTED.
- **Yal de la Sombra** — cuidadora; conoce rutas fuera del culto — DOCUMENTED.

Documented adversary archetypes:

- **Penitente heliostático** — escudo espejo con ventana de giro — DOCUMENTED.
- **Saboteador de lente** — coloca haces con anclajes visibles — DOCUMENTED.
- **Escarabajo colosal** — territorial; vulnerable tras descargar calor — DOCUMENTED.

Final morphology, rigs, wardrobe/equipment, crowds and combat production remain outside the world-macro claim and UNCLAIMED.

## Gameplay / mission spatial contract

Documented main chain:

1. **La peregrinación de cobre** — repair communal shade; learn the price of light.
2. **Reliquias vivientes** — cross the sea using reflectors or underground routes.
3. **El salmo de las baterías** — free technicians held by debt in the crucible.
4. **Desencadenar a RA-KHET** — redistribute beams between arena nodes during the confrontation.
5. **El precio de otro amanecer** — decide ownership and maintenance of solar infrastructure.

Documented sidequests include inherited toll/debt review and converting a minor collector into a condenser at the cost of market energy. The prism-optics minigame redirects beams using thermal reading, with an assisted interaction mode.

## Art Direction Contract

### Pillars

1. **Optics are infrastructure, not decoration.** Mirrors/prisms exist to route energy/access.
2. **Heat has architectural consequences.** Shade, ceramic shielding and maintenance access must be legible.
3. **Sacred maintenance.** Bronze/mechanical elements should feel repaired, inherited and materially consequential rather than generically ornate.
4. **Crystal + shadow.** Strong directional light and useful shadow structure carry navigation.
5. **Rights are spatial.** Energy ownership must be readable through barriers, routing and access states, not only dialogue.

### Shape language

- large optical planes;
- radial/axial tracking structures;
- long shade geometries;
- restrained vertical markers;
- purposeful cable/tension lines;
- broad desert basins at macro scale.

### Material families

- solar glass / vitrified substrate;
- mirror/reflector surfaces;
- bronze structural/mechanical elements;
- scorched ceramic thermal shielding;
- fabrics/shade systems;
- dark mineral / high-contrast thermal mass;
- emissive routing signals only where function requires them.

### Forbidden drift

- generic cyberpunk neon;
- Egyptian/ancient iconography as a shortcut from the name “Khepri”;
- random greebles;
- decorative mirrors that do not have optical purpose;
- uniform scratches/wear;
- uncontrolled specular/emissive surfaces;
- geometry noise substituting for manufacturing logic.

## Technical world hierarchy

- **L0:** planetary metadata; gravity documented, radius proposal pending canon approval.
- **L1:** lightweight orbital representation; no gameplay collision.
- **L2:** tiled/local-tangent macro terrain.
- **L3:** gameplay cells — future claims.
- **L4:** hero zones — future claims.
- **L5:** hero assets — future claims.

KHEPRI uses local metre-scale authoring cells so a future engine adapter can implement streaming/origin management without requiring planet-scale meshes in Blender.

## Open blockers / decisions

- physical radius promotion or replacement;
- atmosphere and long-range sky model;
- literal meaning/material physics of the “glass sea”;
- global map and exact boundaries/relationships among the documented named regions;
- complete ecology graph beyond the four documented KHEPRI species;
- settlement/city kit ownership;
- RA-KHET final design/rig;
- target-engine GPU/streaming qualification.
