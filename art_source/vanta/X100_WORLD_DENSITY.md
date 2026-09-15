# EXOVANT 2950 — VANTA WORLD DENSITY ×100

**Protocol:** `WORLD_DENSITY_X100_v1`  
**World:** VANTA / FERRUM  
**Producer:** `AGENT-VANTA-WORLD-01`  
**Branch:** `art/world-vanta-001`  
**Active claims:** `CLM-VANTA-X100-CULTURE-001` + `CLM-VANTA-X100-ECOLOGY-001`  
**Latest remote source:** Blender rev26

X100 is a production algorithm, not a quality label. The evidence-linked 14-dimensional geometric-mean heuristic is now **29.96% → PLAYABLE FOUNDATION**. This remains explicitly non-canon and is not an AAA/AAAA claim.

## North Star

VANTA must read as a high-gravity worker shipyard whose labor culture, repair economy, magnetic industry, scarcity and ecology can be inferred from geometry and systemic consequences before exposition. Density must come from **function × history × state × recombination × ecology × gameplay**, never random clutter.

## Coverage

| Dimension | Score | Rev26 evidence / blocker |
|---|---:|---|
| Macro world | 0.28 | 24×24 km district proxy and three regions; planetary/final topology open |
| Meso architecture | 0.20 | validated kits/tableaux inhabit Puerto and Lluvia; final authored interiors/routes sparse |
| Micro assets | 0.24 | culture family + ecology family + functional details/traces |
| Ecology | 0.32 | 4 causal species, 12 variants, 36 state deltas, 4 traces, 3 habitats, native motion/collision |
| Civilization | 0.32 | 5 Worker Life tableaux express labor/repair/medicine/strike/charging |
| Gameplay | 0.20 | traversal/collision receipts and ecology affordance contracts; final AI/interactions open |
| Material causality | 0.22 | causal culture states + ecology traces; photometric portability open |
| Variation | 0.34 | state/scale/tableau recombination across culture and ecology |
| Temporal states | 0.36 | five culture states + three eras + ecology state deltas |
| Storytelling | 0.34 | repair/strike history + ecology impacts on routes/salvage/maintenance |
| Audio/visual language | 0.24 | 10 ecology audio hooks; runtime audio still open |
| Optimization | 0.36 | culture LOD/HLOD runtime canary + ecology LOD reductions + clean exporter |
| Reusability | 0.45 | shared datablocks, systemic tableaux, source→placement bindings and deterministic exporter |
| QA | 0.48 | native Godot collision/motion/LOD receipts; human art and target GPU remain open |

Current lowest dimensions are **MESO_ARCHITECTURE and GAMEPLAY (0.20)**, but the active ecology claim still has quality gates and remains the immediate owner of its representative slice.

## Worker Life / Maintenance Culture

The culture system remains twelve families under `VAN_X100_CULT_*`, each with S/M/L variants and five causal states.

Key qualified evidence through rev19:

- 36 source variants × five states;
- 165 structurally beveled parts;
- 333 justified functional details;
- 36 maintenance clearances;
- five systemic tableaux;
- 40 placements / 675 linked instance parts;
- 1.8 m corridor: nine blockers discovered and repaired, zero remaining;
- 25 three-era story objects;
- real LOD1 + LOD2;
- five tableau HLOD sources.

### HLOD P1 found and repaired

Adversarial rev18 audit found all five HLOD proxies near global origin due a bad parent/inverse relationship. Rev19 repaired this by detaching HLOD proxies and applying explicit world transforms.

Rev19 additionally provides:

- one packed 1024² HLOD palette atlas;
- `M_VAN_X100_HLOD_ATLAS_A` with a single texture node;
- per-asset LOD distance-band metadata;
- persistent Maintenance Bay CLOSE/MID/FAR QA cameras.

Native Godot 4.7.2 tier canary:

- 5 m → LOD0, 141 meshes;
- 30 m → LOD1, 19 meshes;
- 70 m → LOD2, 8 meshes;
- 120 m → HLOD, 1 mesh;
- HLOD textured surfaces: 1/1.

This qualifies tier switching mechanics in the representative culture slice. Pop quality and target-GPU performance remain open.

## Ecology ×100

Canonical species are no longer only proxy targets. See `ECOLOGY_X100.md`.

Representative Lluvia de Hierro ecosystem:

- Bacteria de escoria — decomposer/resource biofilm;
- Litófago magnético — primary consumer / ferrous grazer;
- Raya de limaduras — field-following secondary consumer/redistributor;
- Cuervo de remache — scavenger/nest builder.

Current source:

- 4 species × S/M/L = 12 variants;
- 36 ecology state-delta sources;
- four trace families;
- three in-world habitats;
- ten organism placements;
- ten influence-volume source contracts;
- ten in-world runtime colliders;
- LOD0/source 4,076 tris → LOD1 444 → LOD2 168.

### In-world causal habitats

1. **Slag Nursery**  
   `slag_heat → bacteria_growth → lithophage_grazing → magnetic_nodule_deposition`

2. **Filings Corridor**  
   `field_alignment → ray_filings_wake → lithophage_graze_channel → route_surface_change`

3. **Rivet Roost**  
   `scrap_carrion → rivet_scavenging → fastener_nest → maintenance_material_loss`

### All-scale motion

The ecology source uses 1–97 @24 fps loops.

- M source: 24 actions / 22 dynamic;
- S/L sampled retarget: 36 actions / 32 dynamic;
- dynamic total: **54**;
- all ten in-world placements receive motion.

Exact rev25 provider-artifact Godot 4.7.2 canary:

- 10 `StaticBody3D`;
- 10 non-null `CollisionShape3D`;
- 10/10 physical ray hits;
- 54 ecology animations with runtime transform change;
- 4,266 animation tracks;
- 10/10 placements targeted;
- 10/10 placements visibly change transform in runtime state.

This is empirical motion/collision transport. It is **not** creature AI.

### Audio / affordance integration surfaces

Rev26 adds ten source-only audio hooks and three source-only ecology affordance hooks. `implemented_gameplay=false` remains deliberate.

Examples:

- biofilm density → salvage quality/lithophage presence;
- magnetic alignment → ray wake reveals safe field line;
- fastener-nest density → repair-material availability signal.

These are integration contracts, not completed gameplay.

## Source versus runtime

Rich Blender source is not a shipping bundle.

Versioned exporters:

- `pipeline/export_x100_delivery.py` — Worker Life;
- `pipeline/export_x100_ecology_delivery.py` — ecology.

Latest rev26 clean ecology structural proof:

- 554,804 B;
- SHA256 `ffbaf45b158001dcc2e376b5b3f2606d8d4739dcc39bfb39a88009627d9926a7`;
- 223 nodes / 144 meshes / 9 materials;
- 60 animation records / 133 channels;
- 10 `_colonly` nodes;
- 0 authoring source nodes;
- 0 LOD source nodes;
- 0 editor-hook nodes.

The sandbox recycled before this clean GLB could be re-imported into Godot. Therefore clean-bundle native reimport remains OPEN. The exact larger provider artifact is the current empirical native-runtime authority.

## Exact rev26 source checkpoint

- `.blend`: 22,120,321 B;
- `.blend` SHA256 `47b7a8feeba5874d5f08ac518dd430cfe9327bd6d49697c7a33fa43e7cd2f836`;
- provider GLB: 14,482,968 B;
- provider GLB SHA256 `0b3a320dfe6f105c07147a6030c8f4b92ca8b3c38a954004177e32b8d1c35ae2`.

Provider preview is source/evidence transport, not shipping authority.

## Visual QA

Persistent CLOSE/MID/FAR cameras exist for each ecology habitat. Rev26 Eevee MID renders executed for all three. This establishes render execution only; **human art-direction approval remains false**.

## Open gates

- clean selected ecology GLB native Godot reimport;
- human close/mid/far visual/art review;
- photometric Blender↔runtime light calibration;
- final ecology AI and gameplay interactions;
- target GPU frame time / draw calls / residency / VRAM;
- authored final Puerto/Lluvia placement beyond representative slices;
- global registry/integration reconciliation.

## Next multiplicative move

Do not increase species count merely to inflate inventory. Close the ecology clean-delivery/art/gameplay gates, then attack the new multiplicative bottleneck: **MESO_ARCHITECTURE × GAMEPLAY**. The next strong claim should integrate these validated culture/ecology systems into an authored industrial route/interior where magnetism, ecology and worker infrastructure jointly modify traversal.
