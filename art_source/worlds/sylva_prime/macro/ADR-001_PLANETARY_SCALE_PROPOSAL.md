# ADR-SYLVA-001 — Planetary Scale Proposal

**Status:** `PROPOSED / CREATIVE-DIRECTOR DECISION REQUIRED`  
**Claim:** `CLM-SYLVA-MACRO-001`  
**Affects:** Sylva Prime L0 planetary metadata and later L1 orbital representation.  
**Does not alter:** current 12 km local authored blockout, which remains a reversible L2–L4 production proposal.

## 1. Authority classification

### CANON / DOCUMENTED

- World: `SYLVA PRIME`.
- System: `Dendra`.
- Faction: `Coro Micelial`.
- Current world-data gravity: `1.12 g (propuesta revisada)`.
- Current temperature reference: `34 °C`.
- Canonical surface regions: Puerto del Injerto, Bosque de las Frases, Cámara de VESPER.
- Planetary radius and diameter are **not defined** in the current canon.

### EXTERNAL REFERENCE

NASA/JPL Solar System Dynamics lists Earth mean radius ≈ 6371.0084 km, mean density ≈ 5.5134 g/cm³, surface gravity ≈ 9.80 m/s² and escape speed ≈ 11.19 km/s.

Reference: https://ssd.jpl.nasa.gov/planets/phys_par.html

NASA also documents confirmed rocky exoplanets larger/more massive than Earth; e.g. HD 219134 b at ~1.6 Earth radii, ~4.5 Earth masses and ~6 g/cm³, so the 1.05–1.20 R⊕ design range below is not intrinsically outside observed rocky-planet scale.

Reference: https://www.nasa.gov/news-release/nasas-spitzer-confirms-closest-rocky-exoplanet/

### PROPOSAL

The options below are design solutions constrained to preserve the documented 1.12 g surface gravity. They are not astrophysical observations of Sylva Prime and must not be promoted to canon without an explicit decision.

## 2. Method

For a spherical bulk approximation:

- `g / g⊕ = (M / M⊕) / (R / R⊕)^2`
- therefore, for the fixed design target `g = 1.12 g⊕`:
  - `M/M⊕ = 1.12 × (R/R⊕)^2`
- mean-density ratio follows:
  - `ρ/ρ⊕ = (M/M⊕)/(R/R⊕)^3 = 1.12/(R/R⊕)`

This is a design-scale consistency check, not an interior-structure simulation. Real exoplanet composition/density depends on compression, iron fraction, volatiles and atmosphere.

## 3. Options

| Option | Radius | Diameter | Circumference | Mass | Mean density | Surface area | Escape speed | Reading |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| A — Compact dense | 1.05 R⊕ = 6,689.6 km | 13,379.1 km | 42,031.7 km | 1.2348 M⊕ | 5.881 g/cm³ | 562.35 M km² | 12.13 km/s | More compact, denser, less distinctive from Earth-scale worlds |
| B — Earth-density balance | 1.12 R⊕ = 7,135.5 km | 14,271.1 km | 44,833.9 km | 1.4049 M⊕ | 5.513 g/cm³ | 639.83 M km² | 12.53 km/s | Exact Earth-like mean density under the 1.12 g target |
| C — Broad biogenic super-Earth | **1.20 R⊕ = 7,645.2 km** | **15,290.4 km** | **48,036.3 km** | **1.6128 M⊕** | **5.146 g/cm³** | **734.49 M km²** | **12.97 km/s** | Largest recommended option while remaining comfortably in a rocky-world design regime |

`M km²` = million square kilometres.

## 4. Recommendation

**RECOMMENDED: Option C — 1.20 R⊕.**

Proposed L0 values if approved:

```yaml
world_id: sylva
planet_radius_m: 7645210.08
planet_diameter_m: 15290420.16
circumference_m: 48036271.64
surface_area_km2: 734494776.37
mass_earth: 1.6128
mean_density_g_cm3: 5.14584
surface_gravity_earth: 1.12
escape_velocity_km_s: 12.9727
classification: PROPOSAL_PENDING_APPROVAL
```

### Why C fits Sylva

1. **Scale identity.** A 20% larger radius gives ~44% more total surface area than Earth, supporting the feeling of an ecologically immense biosphere without resorting to an implausibly huge planet.
2. **Gravity consistency.** 1.6128 M⊕ at 1.20 R⊕ exactly preserves the documented 1.12 g bulk surface-gravity target under the simplified spherical model.
3. **Material/ecological reading.** Slightly lower Earth-relative mean density (0.933× Earth) leaves design room for a somewhat more volatile-rich mantle/crust or lower iron fraction while remaining fundamentally rocky; this is a worldbuilding direction, not yet canon.
4. **Production separation.** The number can live at L0 metadata while gameplay continues in local tangent-space cells. No existing terrain must be rescaled.
5. **Reversibility.** Choosing A/B/C later changes L0/L1 metadata/orbital representation, not the established 1 m local asset scale.

## 5. Planet-scale engineering contract if approved

Do **not** model the physical planet as one gameplay mesh.

- **L0 — physical/logical planet:** exact radius/mass/gravity metadata; logical 1:1 measurements.
- **L1 — orbital representation:** independent low/medium-frequency sphere/heightfield representation. It may use a normalized/render scale for Blender authoring, provided the physical radius metadata remains exact and conversion is explicit.
- **L2 — continent/region:** tiled terrain hierarchy, scale chosen from gameplay/streaming measurement.
- **L3 — gameplay cells:** current r4 proposal is 3 km cells over a 12 km authored patch; not yet final.
- **L4 — hero zones:** regional envelopes around Puerto/Bosque/VESPER, currently proposals.
- **L5 — hero assets:** independent close-range production assets.

Local gameplay geometry continues at `1 BU = 1 m` in tangent space. A future large-world/origin-rebasing strategy is an engine decision, not baked into Blender geometry now.

## 6. Decision consequences

### If Option C is approved

- update world canon/data through the project authority/integrator, not from this producer branch unilaterally;
- generate a separate L1 orbital proxy scene with explicit representation scale and metadata;
- derive continental/biome tiling only after climate/geography direction is approved;
- keep current 12 km Sylva patch coordinates unchanged.

### If Option A or B is selected

- same production architecture; only L0/L1 numerical metadata changes.

### If all options are rejected

- preserve `UNKNOWN_BLOCKED` and continue only local/regional work.

## 7. What this ADR does not decide

- orbital semi-major axis around Dendra;
- atmosphere composition/pressure;
- axial tilt/day length;
- ocean fraction;
- tectonic regime;
- final continents;
- production engine/floating-origin implementation;
- final climate simulation.

Those require independent evidence/creative decisions and must not be inferred from this radius proposal.
