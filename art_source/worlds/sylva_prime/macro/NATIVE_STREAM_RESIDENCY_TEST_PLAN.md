# SYLVA PRIME — Native Stream Residency Test Plan

Claim: `CLM-SYLVA-MACRO-001`  
Source checkpoint: Blender **r13**  
Hierarchy target: `SYLVA_STREAM_HIERARCHY_R14` (`READY_NOT_EXECUTED_WRITER_FENCED`)  
Current runtime result: `NOT_RUN`

This plan is backend-neutral. It defines evidence and failure conditions without choosing Godot/Unreal streaming APIs or inventing target-hardware budgets.

## Preconditions

1. Recover exact r13 `.blend` + GLB and bind SHA-256.
2. Pass shared `fleet_control.py delivery` transport gate.
3. Pass `validate_glb_contract_r13.py` on the exact same GLB SHA.
4. Import at 1:1 metric scale through the qualified engine's standard glTF path.
5. Preserve or deliberately translate:
   - 16 `SYLVA_STREAM_L3_X#Y#` cells;
   - 16 render terrain tiles;
   - 16 collision terrain tiles;
   - `SYLVA_STREAM_MEMBERSHIP_R13` object memberships.
6. Do not instantiate PR #6 root modules unless its pivot/manifest blocker is separately closed.
7. Human art approval and hardware performance remain separate gates.

## Geometry-residency rule

Use r13 `stream_cells` as the conservative geometry/collision residency set. It is based on world bounding-box overlap and may contain cells that the route centerline never enters.

Never replace object membership with route-centerline membership.

## Player-prefetch rule

Use route centerline progression to trigger travel prefetch. Current proposal after R14 activation:

`ADJACENT_8_PLUS_L3_HERO_RESIDENCY_GROUP`

Hero residency is **L3-only**. L2 is hierarchy/HLOD coverage metadata and must not imply loading an entire 6 km supercell at full resolution.

## Exact route seam probes

Centerline transitions were read-only sampled at 25 m granularity. The boundary coordinates themselves are authored grid boundaries.

### Probe S-00 — Puerto exit

- Route: `SYLVA_TRAV_PathGuide_00`
- Transition: `X0Y1 -> X1Y1`
- Approx route distance: **283.876 m**
- Boundary point: **(-3000, -2000, 345.8) m**
- L2: remains inside `L2_X0Y0`

Assertions:
- source + destination render tiles resident before crossing;
- source + destination collision tiles resident before crossing;
- no visible terrain crack at x = -3000;
- no double collision, snag, step-up, sink or airborne impulse;
- camera remains stable at normal traversal velocity.

### Probe S-01 — Bosque south boundary

- Route: `SYLVA_TRAV_PathGuide_01`
- Transition: `X1Y1 -> X1Y2`
- Approx route distance: **1678.729 m**
- Boundary point: **(-500, 0, 356.1) m**
- L2 transition: `L2_X0Y0 -> L2_X0Y1`

Assertions:
- target L3 is prefetched before y = 0 crossing;
- crossing does not force all four Bosque-covered L2 supercells into full-resolution residency;
- geometry membership for multi-cell macro roots remains stable.

### Probe S-02 — Bosque central junction

- Route: `SYLVA_TRAV_PathGuide_01`
- Transition: `X1Y2 -> X2Y2`
- Approx route distance: **2282.483 m**
- Boundary point: **(0, 250, 352.2) m**
- L2 transition: `L2_X0Y1 -> L2_X1Y1`

This probe enters the Bosque global L2-junction hotspot.

Required hero overlay while inside the Bosque core:
- `X1Y1`
- `X1Y2`
- `X2Y1`
- `X2Y2`

Assertions:
- exactly the explicit L3 hero-residency group is guaranteed by the hero overlay;
- L2 coverage is metadata only;
- no world-geometry relocation is allowed as a streaming fix;
- inspect macro roots that touch all four L2 groups for duplicate instances or premature unload.

### Probe S-03 — VESPER approach

- Route: `SYLVA_TRAV_PathGuide_03`
- Transition: `X2Y2 -> X3Y2`
- Approx route distance: **1605.120 m**
- Boundary point: **(3000, 2000, -72.4) m**
- L2: remains inside `L2_X1Y1`

Assertions:
- no crack or collision discontinuity at x = 3000;
- VESPER hero residency group keeps `X2Y2 + X3Y2` available;
- all three VESPER terraces and both wide connectors remain traversable after the transition.

## Route 02 boundary note

`SYLVA_TRAV_PathGuide_02` centerline remains entirely in `X2Y2` under the half-open / positive-axis tie policy, even though the route object's conservative geometry bounds are `X1Y2|X2Y2`.

This is expected and is a required regression check proving geometry residency and player prefetch are separate concepts.

## Hero residency overlays

### Puerto
- core radius proposal: 550 m
- L3 resident group: `X0Y1|X1Y1`
- L2 coverage: `L2_X0Y0`

### Bosque
- core radius proposal: 200 m
- L3 resident group: `X1Y1|X1Y2|X2Y1|X2Y2`
- L2 coverage spans all four L2 supercells
- **do not** interpret that coverage as four L2 full-residency commands.

### VESPER
- core radius proposal: 400 m
- L3 resident group: `X2Y2|X3Y2`
- L2 coverage: `L2_X1Y1`

## Unload / hysteresis tests

The exact hysteresis distance/time is backend- and movement-speed-dependent and is not fixed here.

For each transition:
1. cross forward;
2. continue far enough for the source cell to become an unload candidate;
3. confirm no source-owned cross-cell macro asset disappears while still required by target-cell membership;
4. reverse direction immediately after unload eligibility;
5. measure reload hitch/pop/collision delay;
6. record the resident-cell set on both sides of the boundary.

Failure examples:
- collision unloads before visible geometry or vice versa;
- multi-cell root disappears when one owner cell unloads;
- duplicate multi-cell geometry is instantiated;
- unloaded source collision remains active as an invisible wall;
- hero overlay causes whole-world full-resolution residency;
- cell transition blocks input or camera.

## Relative-complexity targets for observation

These are **not budgets**, only hotspot priorities from r13:

1. `X3Y2` — 5,996 visible tri-slots / 592 collision tri-slots
2. `X2Y2` — 5,956 / 416
3. `X0Y1` — 3,460 / 192
4. `X1Y2` — 1,944 / 348

L2 relative visible-slot priority:
1. `L2_X1Y1` — 12,828
2. `L2_X0Y0` — 5,788
3. `L2_X0Y1` — 2,936
4. `L2_X1Y0` — 2,648

If HLOD becomes qualified later, start evaluation with `L2_X1Y1`; do not create HLOD solely from this ranking.

## Evidence required per native run

Record:
- exact GLB SHA-256;
- exact source commit;
- engine/version/build;
- graphics backend and hardware/renderer;
- import path/resource ID;
- resident L3 cells before/after every seam;
- collision and render residency separately;
- player speed/movement mode;
- frame-time trace around transitions (informational unless target budget exists);
- screenshots/video/logs at S-00..S-03;
- duplicate/missing geometry findings;
- camera/input/traversal findings;
- explicit PASS/FAIL per seam.

A CPU/llvmpipe graphical capture may prove scene visibility/control flow where qualified by the shared visual runbook, but must **not** be used as target GPU performance qualification.
