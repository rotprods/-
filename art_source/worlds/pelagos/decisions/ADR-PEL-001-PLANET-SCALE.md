# ADR-PEL-001 · Planet scale and authored-area separation

Status: **PROPOSED FOR REVIEW**  
Scope: `CLM-PEL-WORLD-001` only.  
Decision owner: `AGENT-PELAGOS-01`.  
Date: 2026-09-12.

## Context

Pelagos canon fixes an ocean world, design gravity `0.91 g`, an 8 °C reference area, Talas as its K2 V star, and Lágrima as a tide-driving moon. The repository does **not** currently provide a canonical Pelagos radius, diameter, mass, axial parameters, continental mask, full bathymetry or atmosphere model.

The production request requires defining a planet scale without turning the entire planet into one mesh. The master production contract explicitly separates physical planet scale, orbital representation, region tiles, gameplay cells and hero zones.

## Options

1. **Leave radius UNKNOWN.** Safest epistemically, but blocks consistent orbital/world-scale layout and distance conventions.
2. **Use Earth radius.** Convenient but arbitrary and visually weak because it silently imports Earth scale.
3. **Adopt a reversible Pelagos-specific production radius.** Gives measurable scale while keeping the value explicitly non-canonical until reviewed.

## Decision

Adopt the following **world-local production proposal**, not canon:

- radius: **6,000 km**;
- diameter: **12,000 km**;
- circumference: **~37,699 km**;
- surface area: **~452.39 million km²**;
- canonical surface gravity input: **0.91 g**;
- implied mass if the 6,000 km proposal and 0.91 g are both retained: **~0.807 Earth masses** (derived, not independent canon).

The current playable master cell is a separate authored-space proposal:

- master authored extent: **2.2 × 2.2 km**;
- coordinate origin: **Coro del Arrecife datum at mean sea level**;
- principal blockout centers: Mercado de Boyas `(-520,-80)`, Coro `(0,40)`, Fosa `(520,230)` metres;
- THALASSA arena center: `(520,230,-92)` metres;
- arena diameter: **52 m canonical**.

## LOD/scale contract

- **L0 Planetary Canon:** metadata and global topology; no dense mesh requirement.
- **L1 Orbital:** low/mid-frequency sphere/bathymetry representation, future task.
- **L2 Macro Regions:** tiled oceanic/bathymetric regions, future task.
- **L3 Gameplay Cells:** authored cells such as current 2.2 km master region.
- **L4 Hero Zones:** Mercado, Coro, Fosa/THALASSA.
- **L5 Hero Assets:** characters, creatures, hero architecture, vehicle and boss.

No L3/L4 density is extrapolated across the full planetary surface.

## Consequences

Positive:
- permits measurable world composition and orbital planning;
- prevents monolithic planet meshes;
- keeps detailed geometry focused on player-visible zones;
- proposal is reversible before global travel/orbital representation locks it in.

Negative / risk:
- radius is not current canon and can change;
- a radius change affects orbital visuals, horizon curvature, streaming math and global maps but **must not** require rescaling authored metre-space assets.

## Affected scopes

Pelagos world macro, future orbital representation, travel framework, vistas and streaming. No other planet inherits this radius.

## Review gate

This ADR cannot become `ACCEPTED` until a creative/technical owner explicitly approves the radius or replaces it. The current Blender scene stores radius and mass with `PROPOSAL` metadata labels.
