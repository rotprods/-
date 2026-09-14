# UMBRA WAVE 1 RECEIPT — ART-UMBRA-001

Status: `WAVE1_PRODUCTION_FOUNDATION / REPRODUCIBLE / NOT FINAL AAAA`

Claim: `CLM-W04-WORLD-UMBRA-001`  
Owner: `AGENT-UMBRA-04`  
Primary project: `7ab99682-8777-4143-8ae0-1fbb178ccafb`  
Independent replay project: `7f33ae14-540c-4af5-8131-1490465fe6cc`

## Trigger

Wave 0 passed structural reproducibility but the post-CI objective art Gauntlet exposed two production defects:

1. Terrain contact was invalid: the ten caravan tracks floated roughly `2.43–5.80 m`; several reflector masts / windbreaks were embedded by as much as `3.62 m`; the refuge base was embedded about `2.59 m`.
2. The delivery camera excluded reflector 03, caravan 00 and the NOCTIL destination ring.

These were treated as modeling defects, not hidden as blockout tolerance.

## Wave 1 scope executed

### Reflector kit — `W04-INF-001`

All four Wave-0 reflectors were terrain-seated and extended with functional/manufacturing logic:

- load-spreading foundation plate;
- four terrain-aware anchor pads per tower;
- guy members from mast to anchor field;
- lower power/thermal service cabinet;
- cable trunk;
- upper maintenance platform and safety rail;
- exposed upper ladder segment with sealed-lower-mast access assumption;
- gimbal ring + yoke;
- mirror backing ribs;
- twin linear aiming actuators;
- weather/maintenance sensor stem and head.

The mirror remains a reversible production-foundation representation, not a final optical simulation.

### Caravan kit — `W04-CAR-001`

All five caravans were terrain-seated and extended with a modular cold-world vehicle language:

- torsion-box longitudinal frame rails;
- six load-transfer bogies per vehicle;
- suspension links;
- wind-shedding upper cowl;
- bilateral field-service bays;
- bilateral quick-release cargo pods;
- rear heat-exchanger fins;
- tension-canopy structural members;
- protected identity/refuge beacon mast.

This establishes manufacturing and maintenance causality but is not final vehicle topology, UV, rig, suspension simulation or destruction authoring.

### Refuge / framing

- Refuge hub Wave-0 massing was terrain-seated and given six contact feet. Full `W04/ARCH/014` production kit remains open.
- Delivery camera was reframed to contain all four reflector masts, the left/mid/right caravan anchors, refuge hub and NOCTIL destination interface.
- `CAM_QA_PLAYER_READABILITY` was added as a QA-only 2.2 m-height camera; it is explicitly not runtime camera authority.

## Primary revision 2 receipt

Committed revision: `2`  
Scene sequence: `0`

- objects: `407`
- mesh objects: `395`
- materials: `9`
- evaluated triangles: `35,028`
- Wave-1 named objects: `310`
- residual non-unit object scales: `0`
- zero-dimension meshes: `0`
- editable `.blend`: `4,134,586 B`, etag `5581ef232d24e37ea589dffe4514eb78`
- portable GLB: `2,474,196 B`, etag `0d351e8a81781acb64cf69db0134e39f`

### Contact receipt after correction

All checked contact gaps are within the current blockout production threshold of `|gap| <= 0.25 m`:

- refuge base: `+0.080 m`
- caravan 00 tracks: `+0.071 / +0.129 m`
- caravan 01 tracks: `+0.065 / +0.135 m`
- caravan 02 tracks: `+0.014 / +0.186 m`
- caravan 03 tracks: `-0.045 / +0.245 m`
- caravan 04 tracks: `-0.016 / +0.216 m`
- reflector mast 00: `+0.060 m`
- reflector mast 01: `+0.060 m`
- reflector mast 02: `+0.060 m`
- reflector mast 03: `+0.060 m`

No checked contact exceeds `0.25 m` absolute error.

### Delivery framing receipt

Every required anchor is fully inside the delivery-camera projection after Wave 1:

- reflector masts 00–03;
- caravan chassis 00 / 02 / 04;
- refuge hub base;
- NOCTIL eclipse-ring destination proxy.

Delivery camera: location `[80, -1150, 250] m`, lens `38 mm`.

## Independent clean replay

Wave 1 was applied independently to the clean Wave-0 replay project and produced revision `2`.

Replay metrics match the primary scene exactly:

- objects `407`;
- meshes `395`;
- materials `9`;
- evaluated triangles `35,028`;
- Wave-1 objects `310`;
- zero non-unit object scales;
- zero zero-dimension meshes;
- exact same 15 terrain-contact gaps;
- same delivery camera transform/lens;
- GLB byte size exactly `2,474,196 B`.

Replay `.blend` size also equals the primary at `4,134,586 B`, while etags differ as expected from Blender/container metadata (`0df978c83f34ff7fdd07463f11ca7ab0` replay vs primary etag above). Binary etag identity is not used as the semantic reproducibility gate.

## Visual evidence / epistemic limit

Three Wave-0 QA renders were successfully published (`delivery`, `scale`, `aerial`) before Wave 1. The current client path did not expose their image bytes to the agent for direct pixel inspection. Therefore **no direct visual-art PASS is claimed**. Objective geometric framing/contact checks were used to identify and close concrete defects; human/direct image review remains an open gate.

## Known debt after Wave 1

- final UVs / texel-density contract;
- calibrated PBR / authored texture sets;
- linked/shared mesh optimization and instancing policy;
- LOD/HLOD and collision authoring;
- UMBRA-specific runtime import/traversal/profile evidence;
- low-light/color-vision gameplay readability acceptance;
- full refuge modular production kit;
- quest-cell environmental implementation;
- physical planet radius/orbital representation contract;
- final NOCTIL morphology/rig/attack contract;
- direct human art approval.

Wave 1 is therefore a reproducible production foundation, not completion.
