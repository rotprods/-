# PELAGOS — PEL/MKT/DAMAGE-X100-005 receipt

Status: **STRUCTURAL_PASS / REVERSIBLE STATE-SWAP FOUNDATION / NOT ENGINE-QUALIFIED**  
Branch: `art/world-pelagos-thalassa-001`  
3D Jutsu project: `39930c08-62bb-4034-b35d-70d0ce51c9d9`  
Final structural checkpoint: **Blender rev. 38**

## Why this claim existed

Coverage rerank at rev. 37 measured only two explicit architecture damage/recovery families against a user planning range of 5–15. With 63 architecture families already represented, temporal material history remained shallow relative to structural breadth. `/EXOVANT-X100` therefore prioritized damage/recovery because it multiplies physical storytelling, temporal state, gameplay readability and asset reuse simultaneously.

This system is intentionally **non-destructive**: base Mercado meshes are never fractured or edited by the generator. Damage is represented through causal overlay/replacement modules attached to measured target surfaces, allowing future runtime state swaps without destroying authored source geometry.

## Delivered families

1. `PEL-DMG-DECK-IMPACT-001` — deck impact / load-spreading repair.
2. `PEL-DMG-CANOPY-TEAR-001` — flexible membrane tear / tension patch.
3. `PEL-DMG-BRIDGE-HINGE-001` — articulated-bridge hinge stress / brace.
4. `PEL-DMG-HATCH-SEAL-001` — service-hatch seal corrosion / ingress repair.
5. `PEL-DMG-BUOY-LEAK-001` — buoyancy-pod shell impact / leak clamp.
6. `PEL-DMG-MOORING-OVERLOAD-001` — mooring load-path overload / tear-out reinforcement.
7. `PEL-DMG-UTILITY-INGRESS-001` — service-channel fluid ingress / cover repair.
8. `PEL-DMG-SHELL-STRESS-001` — CommandShell stress concentration / emergency brace.

## Causal state grammar

Every family authors four co-located state roots:

- `stressed`;
- `damaged`;
- `field_repaired`;
- `abandoned`.

Severity/morphology variants:

- minor;
- standard;
- severe.

Combinatorial foundation:

- 8 families × 4 states = **32 authored state roots**;
- 8 × 4 × 3 = **96 direct variant/state combinations** before broader placement/orientation grammar.

Only one state is visible per family in the current scene. Alternates remain fully authored but hidden for future runtime/state-authoring work.

## Current visible state set — rev. 38

- BRIDGE → `field_repaired`;
- BUOY → `field_repaired`;
- CANOPY → `damaged`;
- DECK → `field_repaired`;
- HATCH → `stressed`;
- MOORING → `damaged`;
- SHELL → `field_repaired`;
- UTILITY → `field_repaired`.

## Surface attachment authority

Anchors were measured from evaluated target geometry rather than guessed world coordinates. Representative attachments:

- deck `PEL_MKT_Platform_00` → `(-552,-90,13.5)`, +Z normal;
- canopy `PEL_MKT_V1_CanopyMembrane_3` → `(-510.56097,-89.43903,39.17073)`, normal `(0.56604,-0.56604,0.59933)`;
- bridge `PEL_MKT_Bridge_0_3` → `(-517,10,16)`, normal `(0.95106,0,-0.30901)`;
- hatch `PEL_MKT_V1_Hatch` → `(-520.00006,-80,14.425)`;
- buoy `PEL_MKT_V1_BuoyPod_06` → `(-555.20001,-80,4.5)`, normal `(-0.98769,-0.15645,0)`;
- mooring `PEL_MKT_V1_MooringCleat_04` → top face at `(-558,-80,14.675)`;
- utility `PEL_MKT_V1_ServiceChannel_04` → `(-531.1051,-99.78462,13.745)`, normal `(0.80018,-0.46197,0.38248)`;
- shell `PEL_MKT_CommandShell` → `(-507.2876,-92.90078,23)`, normal `(0.47215,-0.84607,0.24746)`.

## Build result

Operation: `pelagos.x100.damage-recovery.v1`

- base revision: 37;
- committed revision: **38**;
- collection: `15_MERCADO_DAMAGE_X100_V1`;
- families: **8**;
- state roots: **32**;
- new objects: **209**;
- direct variant/state combinations: **96**;
- base architecture modified: **no**;
- collision policy: `none_or_query_until_runtime_damage_binding`.

## Structural QA — rev. 38

### State exactness

- state roots: **32**;
- family counts: 8 families × exactly 4 roots each;
- state counts: 8 stressed / 8 damaged / 8 field-repaired / 8 abandoned;
- visible current roots: **8** exactly — one per family;
- hidden alternate-state child leakage: **0**.

### Attachment / orientation

- attachment errors >5 mm: **0**;
- surface-normal orientation errors >1°: **0**;
- absurd overlay-scale failures: **0**.

### Technical integrity

- visible geometry objects: 43;
- missing UV0: **0**;
- missing material slots: **0**;
- non-unit visible mesh scales: **0**;
- visible technical/LOD geometry: **0**;
- hidden LOD1 roots: **8**, all roots and children hidden render + viewport.

### Traversal safety

The bridge damage family was explicitly checked against the `PEL_MKT_Bridge_0_3` route centerline.

- bridge centerline x: approximately −520 m;
- nearest visible repair geometry x: **−517.272 m**;
- distance from centerline: **2.728 m**;
- reserved route half-width: **1.5 m**;
- result: **PASS**.

Thus the damage storytelling layer does not silently convert the authored bridge route into a blocker.

### Current overlay envelopes

- bridge: ~0.735 × 0.895 × 0.742 m;
- buoy: ~0.359 × 1.497 × 0.982 m;
- canopy: ~1.057 × 0.994 × 1.239 m;
- deck: ~1.323 × 0.952 × 0.110 m;
- hatch: ~1.164 × 1.164 × 0.050 m;
- mooring: ~0.782 × 0.527 × 0.296 m;
- shell: ~1.669 × 1.142 × 1.095 m;
- utility: ~1.024 × 1.376 × 0.813 m.

Result: **STRUCTURAL_PASS**.

## Causality / anti-slop contract

Damage is tied to physical causes:

- docking/dropped-load impact at deck load paths;
- storm tension and repeated flex in membrane systems;
- cyclic hinge loading on articulated bridges;
- salt corrosion and fluid ingress at service seals;
- pressure-shell impact on buoyancy pods;
- storm/tow overload at mooring load paths;
- service-cover ingress at utility channels;
- platform flex / stress concentration at shell structure.

No random crack decals, uniform edge wear, grunge-everywhere or decorative destruction is part of this foundation.

## Persisted source

- `art_source/worlds/pelagos/scripts/build_market_damage_x100.py`

The script is the deterministic rebuild authority for this reversible damage/state-swap foundation.

## Post-wave coverage consequence

Rerank at rev. 38 reports:

- scene: 2,638 objects / 1,684 renderables;
- damage/recovery families: **8**, now above the 5-family planning floor;
- traversal families: **5**, at the planning floor;
- prop/cultural families: **9** against a 30-family planning floor — the next dominant Blender-addressable X100 gap.

## Explicit non-claims / blockers

This receipt does **not** claim:

- runtime fracture;
- destructibility physics;
- debris simulation;
- navmesh mutation;
- network replication;
- save/persistence of damage state;
- gameplay state machine bindings;
- production HLOD thresholds;
- target-GPU qualification;
- final cinematic/material GATE-ART.

Those remain `BLOCKED/PENDING` on engine/gameplay/performance authority. The Blender-side reversible damage/recovery foundation is structurally qualified.
