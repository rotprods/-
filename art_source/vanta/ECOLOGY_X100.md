# VANTA — ECOLOGY ×100

**Claim:** `CLM-VANTA-X100-ECOLOGY-001`  
**Owner:** `AGENT-VANTA-WORLD-01`  
**Prefix:** `VAN_X100_ECO_`  
**Latest source:** Blender rev26  
**Truth level:** representative ecology slice empirically qualified for native collision + all-scale motion; final art/gameplay/GPU remain open.

## North Star

VANTA ecology must look like a system that evolved around heat, slag, ferrous dust, magnetic infrastructure and worker salvage—not four creatures placed on an industrial map. Organisms must leave readable physical consequences on scrap, routes and maintenance economy.

## Causal graph

```text
slag heat / oxidized waste
    ↓
BACTERIA_SLAG — decomposer / biofilm resource
    ↓ feeds / marks
LITHOPHAGE — primary consumer / ferrous grazer
    ↓ sheds + channels magnetic material
FILINGS_RAY — secondary consumer / field-following redistribution
    ↓ wakes align filings and expose field corridors

scrap carrion / loose fasteners
    ↓
RIVET_CROW — scavenger / nest builder
    ↓
fastener nests / local maintenance-material loss

metal rain + magnetic storms
    ↘ modify all four species and their traces
```

This is a production graph, not a complete scientific simulation.

## Species families

| Species | Role | Motion profile | In-world consequence |
|---|---|---|---|
| Bacteria de escoria | decomposer/resource biofilm | `sessile_respiration_and_vent_pulse` | slag oxidation, heat-affinity patches, biofilm density |
| Litófago magnético | primary consumer | `six_contact_magnetic_tripod_gait` | scrap grazing, route erosion, magnetic nodule seeding |
| Raya de limaduras | secondary consumer / redistributor | `field_locked_ground_skim` | filings wakes, visible field lines, corridor redistribution |
| Cuervo de remache | scavenger | `high_gravity_perch_short_hop` | fastener theft/nests, repair-material clues |

Each species has `S/M/L` source variants: **12 source variants total**. The current slice also carries **36 causal state-delta sources** and four trace families.

## Representative habitats in Lluvia de Hierro

### Slag Nursery
Anchored into an existing scrap bank. Chain:

`slag_heat → bacteria_growth → lithophage_grazing → magnetic_nodule_deposition`

### Filings Corridor
Integrated with the existing magnetic rail corridor. Chain:

`field_alignment → ray_filings_wake → lithophage_graze_channel → route_surface_change`

### Rivet Roost
Integrated with existing scrap. Chain:

`scrap_carrion → rivet_scavenging → fastener_nest → maintenance_material_loss`

The three tableaux contain **10 organism placements**. Every placement is bound to source asset, active state, collision source, LOD1/LOD2 source, motion profile, motion source, distance bands, ecology tags and influence radius.

## Motion contract

- source frame range: 1–97 @ 24 fps (~4 seconds);
- M source actions: 24, of which 22 produce transform change;
- S/L retarget: 36 sampled actions, 32 dynamic;
- retarget: `sampled_delta_scale_v1`;
- position delta scales with size ratio;
- rotation delta is preserved;
- scale response is proportional;
- frame 1 == frame 97 is enforced for every retarget loop.

Godot 4.7.2 empirical provider canary at rev25:

- 10 `StaticBody3D`;
- 10 non-null `CollisionShape3D`;
- 10/10 physical ray hits;
- 54 dynamic ecology animations;
- 4,266 animation tracks;
- 10/10 placements targeted by imported animation;
- 10/10 placements demonstrate runtime transform change.

This qualifies motion transport, not final creature AI.

## LOD / optimization

Current representative source totals:

- LOD0/source: **4,076 tris**;
- LOD1: **444 tris** (~10.89%);
- LOD2: **168 tris** (~4.12%).

Worker-Life HLOD/LOD work remains a separate culture subsystem. Ecology has LOD source and per-placement bands, but ecology-specific runtime LOD pop assessment remains open.

## Runtime-delivery contract

The provider preview GLB is **not** runtime authority because the rich `.blend` contains source families, LOD authoring, QA hooks and additional evidence.

`pipeline/export_x100_ecology_delivery.py` emits only:

1. `ECO_TBL_SLAG_NURSERY`;
2. `ECO_TBL_FILINGS_CORRIDOR`;
3. `ECO_TBL_RIVET_ROOST`;
4. their active in-world geometry;
5. the ten transformed `_colonly` colliders;
6. the imported/retargeted animation actions.

It excludes `VAN_X100_ECO_*` source families, LOD source, cameras, audio hooks, affordance helpers and influence QA helpers.

Latest structural clean-export proof from rev26:

- 554,804 B;
- SHA256 `ffbaf45b158001dcc2e376b5b3f2606d8d4739dcc39bfb39a88009627d9926a7`;
- 223 nodes / 144 meshes / 9 materials;
- 60 animations / 133 channels;
- 10 `_colonly` nodes;
- 0 authoring source nodes;
- 0 LOD source nodes;
- 0 editor-hook nodes.

The sandbox recycled before the clean GLB could be re-imported into Godot. Therefore **clean selected native reimport remains OPEN** even though the larger exact provider artifact already passed native collision and all-scale motion.

## Audio and gameplay hooks

Rev26 contains ten source-only audio hooks. Representative event IDs:

- `vanta.eco.bacteria.slag_hiss_pulse`
- `vanta.eco.lithophage.magnetic_grind_gait`
- `vanta.eco.filings_ray.field_skim`
- `vanta.eco.rivet_crow.fastener_call`

Three source-only affordance hooks exist:

- biofilm density → salvage quality / litófago presence;
- magnetic alignment → ray wake reveals safe field line;
- fastener-nest density → repair-material availability signal.

`implemented_gameplay=false` is deliberate. These hooks define integration contracts and must not be misreported as functioning gameplay.

## Visual QA

Rev26 contains persistent CLOSE/MID/FAR cameras for each habitat. Eevee MID renders executed successfully for all three habitats. Their existence proves render execution, **not human art approval**.

## Open gates

- native Godot reimport of the clean selected ecology GLB;
- human close/mid/far art-direction review;
- richer causal material-state differentiation;
- final AI / gameplay implementation of the affordance contracts;
- target-GPU frame time, draw calls, texture residency and VRAM;
- authored propagation into more of Lluvia de Hierro only after the representative slice remains green.

## Next multiplicative move

Once these quality gates are closed, do **not** add random extra fauna. Recompute the 14-dimensional geometric mean. At rev26, the next low dimensions are meso architecture and gameplay, so the next X100 claim should connect ecology to authored traversal/industrial spaces rather than inflate species count.
