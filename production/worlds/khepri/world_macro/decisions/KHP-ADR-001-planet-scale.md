# KHP-ADR-001 — KHEPRI physical planet scale proposal

**Status:** PROPOSED / REVERSIBLE  
**Scope:** `CLM-KHEPRI-WMACRO-001`  
**Decision owner:** `AGENT-KHEPRI-WMACRO-001`  
**Affects:** KHEPRI world-macro only until explicitly promoted to canon.

## Context

Recovered canon fixes KHEPRI surface gravity at **0.63 g** but does not fix physical radius, mass or density. The user requires a defined planet scale, while project law forbids silently inventing canon. A physically plausible placeholder is therefore needed for L0/L1 engineering, clearly separated from canonical design data.

## Constraints

- Canon gravity: `g = 0.63 g_E`.
- Rocky world implied by solar-glass desert and two rocky moons, but bulk composition is not canonically specified.
- Planet must support a 1:1 logical scale while authored gameplay remains tiled/local.
- Changing radius later must not invalidate local gameplay meshes.

## Options considered

### A — Earth-radius low-density world
- Radius: `1.00 R_E = 6371 km`
- Required mass for 0.63 g: `0.63 M_E`
- Mean density: about `3.47 g/cm³`
- Advantage: intuitive scale.
- Risk: comparatively low density for a hot rocky world; larger world-space burden with no design benefit yet.

### B — Recommended balanced rocky world
- Radius: `0.82 R_E ≈ 5224 km`
- Diameter: `≈ 10,448 km`
- Required mass for 0.63 g: `0.63 × 0.82² ≈ 0.4235 M_E`
- Mean density relative to Earth: `0.4235 / 0.82³ ≈ 0.767`
- Mean density: `≈ 4.23 g/cm³` using Earth `≈ 5.51 g/cm³`
- Escape velocity: `≈ 8.0 km/s` (derived, planning only)
- Surface area: `≈ 343 million km²` (derived, planning only)
- Advantage: plausible rocky bulk density; planet remains enormous at 1:1 while reducing unnecessary global scale.
- Risk: still a design assumption; atmosphere/thermal model remains unknown.

### C — Small dense world
- Radius: `0.70 R_E ≈ 4460 km`
- Required mass: `≈ 0.309 M_E`
- Mean density: `≈ 4.97 g/cm³`
- Advantage: compact and physically plausible.
- Risk: stronger implication of metal-rich bulk composition not supported by canon.

## Decision

Use **Option B** only as a **production-scale proposal** for blockout metadata:

```text
KHEPRI_RADIUS_PROPOSAL_M = 5_224_000
KHEPRI_DIAMETER_PROPOSAL_M = 10_448_000
KHEPRI_SURFACE_GRAVITY_CANON_G = 0.63
KHEPRI_MASS_PROPOSAL_EARTH = 0.4235
KHEPRI_MEAN_DENSITY_PROPOSAL_G_CM3 = 4.23
```

The value MUST carry `epistemic=PROPOSAL`. It MUST NOT be written into `design/EXOVANT_DATA.json` or presented as canon without explicit creative/technical approval.

## Engineering consequence

All playable geometry is authored in **local tangent cells** at metre scale. Planet radius affects:

- orbital/L1 visualization;
- geodetic conversion;
- horizon curvature at long distance;
- eventual global travel calculations.

It does **not** affect local mesh coordinates. This makes the ADR reversible: replacing 5,224 km later changes metadata/conversion, not authored local geometry.

## Revalidation trigger

Re-open this ADR when any of the following occurs:

1. canonical planet radius/mass/atmosphere is defined;
2. orbital travel physics requires a different body model;
3. production-engine precision tests reject the local-cell strategy;
4. art direction requires visibly different horizon curvature in representative long-range vistas.

## Promotion gate

`PROPOSAL → CANON` requires an explicit project-level decision and synchronized update of canonical design data. A Blender blockout, render or successful export is not sufficient authority.
