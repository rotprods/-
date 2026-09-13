# UMBRA X100 ARCHITECTURAL INTERFACE KIT RECEIPT

Scope: `W04-X100-ARCH-INTERFACE-KIT`  
Status: `KIT_FOUNDATION / QA-FIXED / NOT FAMILY_COMPLETE`

## Purpose

UMBRA previously had macro architecture and machine systems, but insufficient reusable L3 language for how a 1.75 m person enters, climbs, crosses, accesses, seals and services structures. This pass fills that systemic gap rather than adding decorative mass.

## Families

Ten modular architectural-interface families were authored:

1. `ACCESS_DOOR`
2. `SERVICE_HATCH`
3. `LADDER`
4. `PLATFORM`
5. `HANDRAIL`
6. `GANTRY_FRAME`
7. `BRIDGE_DECK`
8. `CABLE_GLAND`
9. `CONDUIT_JUNCTION`
10. `ACCESS_CANOPY`

Each family currently has:
- `S / M / L` size variants;
- `STANDARD / WIND_SHIELDED / FIELD_MODIFIED` fabrication variants;
- 0.2 m modular snap-grid metadata;
- stable IDs;
- explicit semantic purpose;
- interface/socket metadata;
- LOD/collision declarations with runtime gates still explicit.

Authored roots: `90` (`10 × 3 × 3`).

The cross-family kit exceeds the X100 `100+ credible configurations` target through size × fabrication × compatible socket combinations. This is combinatorial capacity, not a claim of 100 handcrafted unique meshes.

## Player-scale contract

Reference human: `1.75 m`.

Measured/declared minimum clearances:
- access door: `1.20 m` wide × `2.20 m` high;
- gantry clear height: `~2.90 m` minimum;
- bridge clear width: `2.20 m`;
- access canopy clear height: `~2.20 m` minimum.

`SERVICE_HATCH` is explicitly a service/crawl aperture, not a standing-player doorway.

## Structural checkpoint

Primary project revision 10 initially produced:
- objects: `2,870`;
- mesh objects: `2,571`;
- evaluated triangles: `89,832`;
- active mesh datablocks: `494`;
- multi-user mesh datablocks: `323`;
- maximum users on one mesh: `117`;
- bad residual scales: `0`;
- zero-dimension meshes: `0`.

## Defect found and corrected

Objective terrain QA found exactly one systemic defect family: all nine `CONDUIT_JUNCTION` variants placed their downward service stub about `0.45 m` below terrain, implicitly inventing underground infrastructure.

That was not accepted as an undocumented feature.

Revision 11 moves the nine downward stubs to a surface-accessible position and tags them as surface-mounted continuation points; underground routing remains unauthored.

Post-fix gate:
- roots: `90`;
- terrain clearance global min: `-0.034 m`;
- roots below `-0.12 m` tolerance: `0`;
- roots with minimum clearance above `+0.20 m`: `0`;
- bad residual scales: `0`;
- zero-dimension meshes: `0`;
- player-clearance contract: PASS / unchanged.

## Hardness / causality

- `WIND_SHIELDED` adds a motivated exposure shield derived from constant lateral wind.
- `FIELD_MODIFIED` adds ivory replacement/reinforcement plates and braces.
- `STANDARD` keeps standardized fabrication.

No random decals, ornamental neon or unmotivated greeble were introduced.

## Remaining family-complete gates

Final UV0/texel density, calibrated PBR, collision, runtime traversal, LOD0/1/2 validation, engine import, direct visual review and durable provider-independent custody remain open.
