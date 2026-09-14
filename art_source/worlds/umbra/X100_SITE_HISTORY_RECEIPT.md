# UMBRA X100 — SITE HISTORY INTEGRATION RECEIPT

Checkpoint: `X100_SITE_HISTORY_INTEGRATION_001`  
Claim: `CLM-W04-WORLD-UMBRA-001`  
Owner: `AGENT-UMBRA-04`  
Status: `PRODUCTION_FOUNDATION / SITE-INTEGRATED / NOT FINAL AAAA`

## Why this exists

X100 is not satisfied by a catalog of variants. Reusable service, damage, architecture and microdetail families must appear inside real UMBRA spaces with causal placement and readable history.

This pass converts the X100 libraries into **world history as geometry** while preserving their shared mesh data.

## Source checkpoint

Primary Blender project: `7ab99682-8777-4143-8ae0-1fbb178ccafb`.

The project had already advanced to `X100_MICRODETAIL_LIBRARY_FOUNDATION_001` with:

- 3 service yards;
- 10 service/cultural utility families;
- 60 DAMAGED/ABANDONED state roots;
- 10 modular architectural interface families;
- 10 causal L5 microdetail families;
- rule-driven placement metadata and no random grunge/greeble contract.

## Site integration delivered

Five site clusters were authored using linked mesh data from the libraries:

1. `REFUGE_SERVICE`
2. `REFLECTOR02`
3. `REFLECTOR03`
4. `M03_ARCHIVE`
5. `CARAVAN_REPAIR`

Total integrated prefabs: **31**.

### REFUGE_SERVICE

ERA_0:
- wind-shielded service platform;
- wind-shielded handrail.

ERA_1:
- field-modified maintenance ladder;
- field-modified service hatch.

ERA_2:
- damaged power/thermal cabinet;
- renewed structural repair plate;
- wind-protected cable clamp.

### REFLECTOR02

ERA_0:
- large wind-shielded service platform;
- large mast-maintenance ladder;
- large wind-shielded handrail.

ERA_1:
- field-modified cable gland;
- field-modified conduit junction.

ERA_2:
- damaged tension-service winch;
- renewed load-transfer weld;
- wind/vibration cable clamp.

### REFLECTOR03

This site intentionally has a different maintenance history from Reflector 02.

ERA_1:
- field-modified gantry frame;
- wind-shielded access canopy;
- field-modified platform;
- older structural repair plate.

ERA_2:
- abandoned cable reel after reroute;
- windborne-abrasion guard.

### M03_ARCHIVE

ERA_0:
- wind-shielded human access door;
- original latch language.

ERA_1:
- later crawl-service hatch;
- field-added handrail.

ERA_2:
- renewed gasket/flange;
- renewed hinge hardware.

Narrative record text/content remains externally owned and was not invented.

### CARAVAN_REPAIR

ERA_1:
- field-modified maintenance gantry.

ERA_2:
- damaged service stand;
- abandoned cable reel;
- fresh repair plates near active maintenance route.

## Technical receipt

Primary committed scene revision after integration: **r13**.

Observed result:

- total objects: **3,776**;
- mesh objects: **3,356**;
- materials: **12**;
- residual non-unit scales: **0**;
- zero-dimension meshes: **0**;
- site clusters: **5**;
- integrated prefab roots: **31**;
- root terrain-contact range: **+0.04 m to +0.04 m**;
- all integrated roots pass `abs(contact_gap) <= 0.06 m`.

Site collection object counts after integration:

- refuge service: `70`;
- reflector 02: `80`;
- reflector 03: `49`;
- M03 archive: `44`;
- caravan repair history: `36`.

The integration preserves linked source mesh data instead of copying unique geometry for every placement.

## QA correction

An earlier broad contact audit incorrectly flagged elevated functional parts such as axles, cooling fins and service plates as if they were ground interfaces. The QA contract was corrected to inspect actual support/base/foot/pad/deck interfaces.

Corrected ground-interface audit on the pre-integration X100 scene:

- checked interfaces: `45`;
- failures beyond ±0.35 m: `0`.

No healthy geometry was modified to satisfy the faulty metric.

## Hardness contract

This pass does **not** use random scatter, arbitrary scratches, blanket grunge or meaningless greebles.

Every placement is tied to one of:

- access;
- maintenance;
- power/thermal routing;
- wind protection;
- load transfer;
- service history;
- damage/failure;
- repair/replacement.

The three-time rule is physically encoded:

`ERA_0 ORIGINAL → ERA_1 MODIFICATION → ERA_2 CURRENT DAMAGE/REPAIR`.

## What is still not DONE

This receipt does not claim:

- final pixel-level/human art approval;
- UV0/PBR/texel-density lock;
- final LOD/HLOD;
- engine collision acceptance;
- runtime interaction logic;
- target-GPU profile;
- provider-independent `.blend`/GLB custody;
- planet-scale L0 completion;
- ecology canon;
- final NOCTIL design.

## Reproduction source

`art_source/worlds/umbra/integrate_x100_site_history.py`

The source script consumes the existing X100 library roots and performs deterministic, terrain-seated, linked-data site integration.
