# UMBRA X100 SERVICE-YARD RECEIPT

Scope: `W04-X100-DISTRICT-SERVICE-YARDS`  
Status: `FOUNDATION / QA-FIXED / NOT FINAL ART`

Three authored systemic compositions were assembled from the X100 service ecosystem rather than modeled as one-off clutter:

- `REFLECTOR_MAINT` around the reflector-03 flank;
- `CARAVAN_REPAIR` between the caravan 02/03 operating region;
- `REFUGE_LOGISTICS` south of the refuge.

Each yard preserves a 5 m central service/traversal corridor and uses three time layers:
- ERA_0 — original installed/safety systems;
- ERA_1 — occupation and active service equipment;
- ERA_2 — field repair/adaptation.

Initial authored composition: 30 prefab instances total, with 9 ERA_0 / 14 ERA_1 / 7 ERA_2 roles.

## Defects found by objective QA

The first pass failed two hardness gates:

1. large flat service aprons floated or intersected terrain by as much as `0.555 m`;
2. wayfinding/lighting elements intruded into the intended 5 m corridor.

No exception was granted. The flat aprons and visible QA rails were removed.

## Corrected checkpoint

Blender checkpoint: `X100_SERVICE_YARDS_QA_FIXED_001`.

Corrections:
- each service apron is now a deterministic terrain-conforming hardpack mesh;
- each hardpack uses a 12×6 cell grid / 91 sampled vertices and sits at exactly `+0.04 m` over local terrain samples;
- prefab roots remain at `+0.03 m` contact datum;
- centerline QA rails are not visible world geometry;
- reflector and caravan wayfinding markers moved to perimeter;
- refuge secondary lamp moved out of the center corridor.

Post-fix objective gate:

| Yard | Root contact | Corridor intrusions | Hardpack terrain offset |
|---|---:|---:|---:|
| Reflector maintenance | +0.03 m | 0 | +0.04 m |
| Caravan repair | +0.03 m | 0 | +0.04 m |
| Refuge logistics | +0.03 m | 0 | +0.04 m |

Scene post-fix:
- objects: `1,577`;
- mesh objects: `1,428`;
- materials: `12`;
- bad residual scales: `0`;
- zero-dimension meshes: `0`.

Direct pixel/human art review remains open; this receipt is structural/systemic acceptance only.
