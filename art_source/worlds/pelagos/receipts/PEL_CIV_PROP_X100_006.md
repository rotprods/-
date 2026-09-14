# PEL/CIV/PROP-X100-006 — receipt

## Authority
- World: PELAGOS
- 3D Jutsu project: `39930c08-62bb-4034-b35d-70d0ce51c9d9`
- Collection: `16_MERCADO_CULTURE_X100_V2`
- Final verified scene revision: **41**
- Final QA: `PELAGOS-X100-CULTURE-PROPS-II-QA-FINAL-R41`
- Source contract: `art_source/worlds/pelagos/scripts/build_market_culture_props_x100_v2.py`

## Production history
A single 12-family mutation exceeded the Blender worker's 300 s deadline and timed out cleanly while the project remained at rev38. No partial commit was applied. Production was then bounded into two coherent mutations:

- WEST batch `pelagos.x100.props2.west.v2` → rev39
- EAST batch `pelagos.x100.props2.east.v2` → rev40
- transform-only grounding correction `pelagos.x100.props2.grounding-fix.v1` → rev41

This staged replay contract is now canonical for this claim.

## Authored families
1. wet work station
2. tethered tool caddy
3. dry lockbox
4. mess vessel set
5. medical wetkit
6. trade measure
7. refuge lamp
8. textile repair frame
9. waste sorter
10. storm stowage
11. portable acoustic navigation marker
12. modular goods bin

Stable IDs are declared in the source contract.

## System grammar
- 12 families
- 3 morphology/capacity variants: `compact | standard | communal`
- 4 causal states: `pristine | used | damaged_repaired | abandoned`
- **144 direct family/variant/state configurations** before placement/orientation grammar
- 48 authored state roots in the World Master
- exactly one visible/current state per family
- 12 hidden LOD1 semantic roots

## Structural QA — rev41
- family count: **12**
- state roots: **48**
- visibility/current-state errors: **0**
- visible meshes: **87**
- missing UV0: **0**
- missing materials: **0**
- non-unit visible mesh scale debt: **0**
- visible technical/LOD geometry leakage: **0**
- LOD1 roots: **12**, all hidden from viewport/render
- platform overflow: **0**
- CommandShell intersections: **0**
- physical inter-family overlaps: **0**
- grounding violations after correction: **0**
- collision policy: `query_only_until_gameplay_binding`

Final visible minimum Z values are at the 13.5 m deck datum within ±0.031 m tolerance. WORK/WASTE/NAV were already within tolerance; nine other families received transform-only datum corrections at rev41.

A preceding route-clearance audit at rev40 measured all families comfortably outside the bridge/dock corridor threshold. Minimum approximate clearance was the refuge lamp at ~6.815 m; other families ranged roughly 10–30 m.

## Cultural / art-direction contract
These assets increase evidence of daily life without inventing unsupported faction hierarchy or iconography. They encode:
- wet/gloved ergonomics,
- tethering,
- drainage,
- corrosion-resistant construction,
- low/heavy mass distribution,
- storm stowage,
- repair-first serviceability,
- replaceable parts and causal wear.

## Epistemic boundary
STRUCTURAL_PASS proves editable Blender authoring only. This claim does **not** prove runtime pickup/use, inventory, buoyancy physics, navmesh behavior, interaction audio, save-state, production HLOD thresholds or target-GPU qualification. Those remain engine/runtime gates.
