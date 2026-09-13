# AURORA VEIL — /EXOVANT-X100 Density Audit

Date: 2026-09-13
Owner: AGENT-02-AURORA
Parent claim: CLM-AURORA-WORLD-001 (ACTIVE, epoch 1)
Remote scene observed: revision 20, `WAVE3_AEON_HERO_FORMS_R20`

## Current truth

The remote scene contains 672 Blender objects and 34 materials, but only 13 objects/families carry top-level stable `asset_id` values. Therefore object count is not accepted as world density. Current state remains PLAYABLE FOUNDATION / early production world, not DENSE AAA and not AAAA candidate.

## Observed family coverage

| Domain | Observed top-level families | X100 planning range | Gap severity | Notes |
|---|---:|---:|---|---|
| Architecture | 3–4 | 20–40 | CRITICAL | Camp has ring/mast/refuge kit but limited semantic breadth and no systematic state/LOD matrix. |
| Infrastructure | 3 | 10–25 | CRITICAL | Clock sync, route beacon, service routing exist; junctions, power/data distribution, access/repair modules sparse. |
| Props | ~2 planned | 30–80 | CRITICAL | Large visual/storytelling gap. |
| Vegetation | 1 proxy family | 10–30 | CRITICAL | Two-shadow grass only as proxy. |
| Fauna | 3 proxy families | 5–20 | HIGH | Species roles exist but not production families. |
| Machinery | ~1–2 | 10–30 | CRITICAL | Orchard machine-tree + AEON-related forms do not cover civilization machinery. |
| Cultural objects | ~1 clock language | 5–20 | CRITICAL | Culture not yet readable from everyday objects alone. |
| Vehicles | 1 | 5–15 | HIGH | Peregrino only. |
| Destruction/damage | 1 planned family | 5–15 | CRITICAL | State breadth nearly zero. |
| Hero landmarks | 2–3 | 5–15 | MEDIUM | Better covered than systemic layers. |
| LOD/HLOD | strategy open | required across repeated families | CRITICAL P0 | Engine-neutral LOD contracts can proceed; engine import remains blocked by EXO-012. |

## Scale pyramid audit

- L0 Planetary: PRESENT as proposal/display shell; global geography intentionally unknown.
- L1 Regional: PRESENT for three canonical regions.
- L2 District/Settlement: THIN — Campamento has a proof assembly, not a dense district system.
- L3 Architectural: PARTIAL — modular base exists but family breadth/variants/states are insufficient.
- L4 Prop/Ecology: THIN — mostly semantic proxies.
- L5 Microdetail: NOT PRODUCTION-QUALIFIED — causal materials exist but authored detail/UV/texture passes remain open.

WORLD_DENSITY_GATE: FAIL by L2–L5 incompleteness.

## Highest-value gap selected

`AUR-X100-CAMP-SYSTEMIC-001` — Campamento systemic settlement kit.

Why this wins the next-work score:

1. multiplies architecture + infrastructure + props + states + LOD/collision simultaneously;
2. reuses already-validated 4 m grid, material roles and service-routing sockets;
3. unlocks 100+ credible settlement configurations without manual one-off modeling;
4. improves player-scale density in the first civilized region;
5. avoids collision with concurrent AEON r20 work;
6. creates reusable manufacturing/cultural language for later Campamento props/interiors.

## X100 configuration target

3 footprint patterns × 4 facade patterns × 3 roof/service patterns × 4 history states = **144 controlled configuration combinations** before local prop/ecology variation.

Only 12 representative configurations need to be instantiated as proof. The generator and module/state grammar are the multiplier.

## Gates

- No random greeble/grunge.
- Every state must have a physical cause.
- All repeated modules use shared mesh data where possible.
- Collision remains separate.
- LOD preserves silhouette/openings.
- Library/source modules remain deterministic and versioned.
- Human GATE-ART remains distinct from technical QA.
- No engine-import PASS until EXO-012 is resolved.
