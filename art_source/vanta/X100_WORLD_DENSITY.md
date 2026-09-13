# EXOVANT 2950 — VANTA WORLD DENSITY ×100

**Protocol:** `WORLD_DENSITY_X100_v1`  
**World:** VANTA / FERRUM  
**Producer:** `AGENT-VANTA-WORLD-01`  
**Branch:** `art/world-vanta-001`  
**Atomic claim:** `CLM-VANTA-X100-CULTURE-001`

X100 is a production algorithm, not a quality label. VANTA remains `BLOCKOUT` under the multiplicative completeness model.

## North Star

VANTA must read as a high-gravity worker shipyard whose labor culture, repair economy, magnetic industry, scarcity, cold climate and political history can be inferred from geometry before text is read. Density comes from **function × history × state × recombination**, never random clutter, uniform grunge or meaningless greeble.

## Multiplicative completeness

Fourteen normalized production dimensions are combined by geometric mean. Scores are evidence-linked planning heuristics, not canon or marketing claims. Current rev13 heuristic: **13.63% → BLOCKOUT**.

| Dimension | Score | Current evidence / blocker |
|---|---:|---|
| Macro world | 0.28 | 24×24 km district proxy, three regions; final topology open |
| Meso architecture | 0.18 | Puerto/Lluvia/Anillo blockout + CP4 kit; final interiors sparse |
| Micro assets | 0.08 | first X100 culture family; broad prop coverage sparse |
| Ecology | 0.03 | canonical species mostly targets/proxies; causal ecosystem absent |
| Civilization | 0.12 | Worker Life/Maintenance family begins closing this layer |
| Gameplay | 0.10 | CP4 traversal + diagnostic 10.2 km spine; final route/interactions open |
| Material causality | 0.18 | CP5 payload + causal state deltas; photometric portability open |
| Variation | 0.16 | 36 culture variants + CP4 modularity; many categories flat |
| Temporal states | 0.18 | five-state source system for 36 variants; not world-wide |
| Storytelling | 0.12 | ownership/repair/strike + three-era contract; tableaux sparse |
| Audio/visual language | 0.12 | strong canon/art language; runtime audio hooks sparse |
| Optimization | 0.16 | guarded dedup + clean selected delivery; HLOD/GPU open |
| Reusability | 0.22 | CP4 snap kit + X100 state contract; placement grammar open |
| QA | 0.20 | native Godot import/collision/UV/route evidence; human art/GPU open |

The lowest multiplicative dimension is currently **ECOLOGY**, but the active Worker Life family still has higher-priority quality gates and therefore remains the current claim.

## Worker Life / Maintenance Culture family

`CLM-VANTA-X100-CULTURE-001` reserves prefix `VAN_X100_CULT_*` and twelve causal families:

- LOCKER — worker ownership and personal storage;
- BENCH — low-COM work/rest surfaces for 1.86g;
- TOOLBOARD — maintenance access and missing-tool history;
- PARTSBIN — salvage sorting / fastener economy;
- MEDKIT — industrial trauma / thermal first aid;
- WELDCART — repair trolley / cable / gas service;
- BATTERY — magnetic-tool batteries and charging;
- RATION — worker food/water logistics;
- STRIKE — barricade / placard / ownership language;
- LIGHT — task/emergency lighting;
- SERVICE — patch boxes / conduit endpoints;
- TEXTILE — cold-weather worker softgoods.

Every family has `S/M/L` source variants and five causal states: `pristine / used / damaged / repaired / abandoned`. Rev13 therefore contains **36 source variants × 5 states = 180 source configurations** before placement context. The four non-pristine states are real source delta geometry, not metadata-only claims.

### Culture DNA

- thick welded/bolted fabrication with low center of mass;
- repairable modules and exposed service access;
- low handles, braced storage and maintenance clearance;
- mismatched salvage patches and visible fasteners;
- reuse-first resource logic and sorted salvage;
- black/steel/rust mass, yellow ownership/safety, cyan only for active magnetic/energy function;
- collective workshop logic, personal ownership marks and strike history;
- rugged magnetic shipyard technology, not decorative futurism.

## Source vs runtime contract

The rev13 `.blend` deliberately contains every state and LOD source. In the observed Blender 5.2 glTF path, `hide_render`, `hide_viewport`, `hide_set`, collection hiding and layer exclusion did **not** reliably filter delivery. Provider `preview.glb` is therefore source/preview evidence, not the X100 runtime authority.

Qualified runtime export uses `bpy.ops.export_scene.gltf(..., use_selection=True)` and explicitly selects:

1. family root;
2. base render children;
3. exactly the active state delta (none for pristine);
4. matching `_colonly` collider;
5. no `LOD1_*` source;
6. no inactive state layers;
7. no QA cameras/lights/decks.

Reusable implementation: `pipeline/export_x100_delivery.py`.

## Current family gates

### Technically qualified

- 36 roots / 12 families / S-M-L coverage;
- 144 non-pristine state delta sources + pristine base state;
- UV0 on every material-bearing delivery primitive;
- 36 collision proxies and 36 LOD1 source proxies;
- selected runtime GLB: 36 roots, 36 colliders, 28 active-state nodes, **0 inactive states, 0 LOD source**;
- Godot 4.7.2: 36 `StaticBody3D`, 36 non-null `CollisionShape3D`, 256 mesh instances/material surfaces, UV failures 0, locker collision ray PASS;
- selected QA-route GLB: 205/205 physical ray samples across the 10.2 km diagnostic spine;
- rev11 continuous CharacterBody kilometre canary remains the stronger route-traversal receipt.

### Open — `FAMILY_COMPLETE = false`

- manufacturing hardness: bevels, thickness, fasteners, welds and access clearances by family;
- true reduced LOD geometry rather than envelope proxies;
- richer causal material-state differentiation;
- 3–5 procedural Puerto tableaux proving placement grammar and story readability;
- player reach/access/clearance review per family;
- human visual/art-direction approval;
- target-GPU frame-time/draw/VRAM/residency;
- final Puerto placement instead of QA staging.

## Permanent loop

`technical delivery → manufacturing hardness → causal states/materials → placement grammar → engine QA → visual QA → coverage update → next lowest multiplicative dimension`.

Do not mass-propagate the legacy 327 planning targets merely because the first X100 family has a valid runtime bundle.