# PELAGOS — PEL/MKT/MACH-X100-003 receipt

Status: **STRUCTURAL_PASS / NOT ENGINE-QUALIFIED**  
Branch: `art/world-pelagos-thalassa-001`  
3D Jutsu project: `39930c08-62bb-4034-b35d-70d0ce51c9d9`

## Why this claim existed

`/EXOVANT-X100` rerank at Blender rev. 34 found settlement machinery at literal zero after L3 interior had been established. The objective was therefore not decorative machinery; it was to close a multiplicative civilisation/infrastructure gap with equipment whose geometry and wear have marine causes.

## Delivered systemic families

1. `PEL-MACH-DRAIN-PUMP-001` — drainage / bilge pumping.
2. `PEL-MACH-FILTER-SKID-001` — service filtration.
3. `PEL-MACH-BALLAST-TRANSFER-001` — ballast / buoyancy transfer.
4. `PEL-MACH-MOORING-WINCH-001` — mooring tension control.
5. `PEL-MACH-STORM-RELEASE-001` — overload / storm release.
6. `PEL-MACH-EQUALIZATION-MANIFOLD-001` — pressure / fluid equalization.
7. `PEL-MACH-ACOUSTIC-RELAY-001` — acoustic relay / conditioning.
8. `PEL-MACH-HEAT-EXCHANGER-001` — fluid heat exchange.
9. `PEL-MACH-SERVICE-HOIST-001` — maintenance hoist.

Engineering semantics are **PROPOSAL**, constrained by canonical Pelagos wet/dry cycling, corrosion, drainage, buoyancy, mooring, maintainability and acoustic systems. Exact energy source, control stack and runtime simulation are intentionally not invented.

## Combinatorial contract

- 9 semantic families.
- 3 capacity variants: compact / standard / heavy.
- 4 causal service states: pristine / used / damaged-repaired / abandoned.
- **108 direct configurations**.
- **432 configurations** with cardinal-yaw placement before broader layout grammar.

Variation is causal: contact wear at service surfaces, localized repair at load/access zones, wet-zone fouling on abandoned equipment. No uniform grunge/random greeble contract.

## Scene execution history

### Build

- Initial build attempt failed before commit because a helper did not accept a `rot=` argument. No partial revision was created.
- Corrected build committed as **rev. 35**.
- Build output: 9 physical machine roots, 173 new objects, 124 new meshes plus hidden LOD/collision foundations.

### QA defect and correction

Focused structural QA found no physical machine overlap, floating geometry, UV/material debt or bay overflow. It did find a real maintenance-clearance defect: `PEL_MACH_HOIST` and `PEL_MACH_MANIF` left only ~1.06–1.08 m to `PEL_MKT_V1_UtilityRiser`, below the 1.20 m production clearance contract.

Both physical roots and their LOD/collision roots were moved **0.25 m west** with topology/material/state unchanged. Final correction committed as **rev. 36**.

### Final rev. 36 structural evidence

- physical machine roots: **9**;
- grounded at service floor z≈14.02 m: **PASS**;
- outside machinery bay: **0**;
- physical machine-to-machine 3D overlaps: **0**;
- minimum UtilityRiser clearance: **1.316 m** (`PEL_MACH_HOIST`) — PASS ≥1.20 m;
- next UtilityRiser clearance: **1.326 m** (`PEL_MACH_MANIF`);
- minimum clearance to existing interior service cell: **3.625 m**;
- visible technical geometry: **0**;
- missing visible UV0: **0**;
- missing visible material slots: **0**;
- non-unit visible mesh scales: **0**;
- current-state mix: 5 used / 2 damaged-repaired / 1 abandoned / 1 pristine;
- current variant mix: 1 compact / 6 standard / 2 heavy.

LOD/collision helpers use non-rendering geometry children. Their Empty roots themselves need not be hidden to remain non-renderable; all technical mesh children are excluded from render.

## Three-time history

- `ERA_0`: platform/service-channel/drainage trunk foundation.
- `ERA_1`: machinery occupation and service network.
- `ERA_2`: localized repairs, decommission/fouling and maintenance-state evidence.

## Persisted source

- `art_source/worlds/pelagos/scripts/build_market_machinery_x100.py`

The script is the deterministic semantic rebuild authority for this X100 machinery foundation. It encodes family IDs, production assembly placement, state causality, service sockets, basic functional signatures and hidden technical proxies.

## Explicit non-claims / blockers

This receipt does **not** claim:

- engine import qualification;
- runtime fluid/pressure simulation;
- interactive machine controls;
- exact power source/control electronics;
- final audio implementation;
- production HLOD switch distances;
- target-GPU performance qualification;
- semantic/cinematic GATE-ART.

Those remain `BLOCKED/PENDING` on engine/gameplay/performance authority. The Blender-side systemic machinery foundation is structurally qualified.
