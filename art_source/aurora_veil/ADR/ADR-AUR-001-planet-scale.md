# ADR-AUR-001 — Planet scale and coordinate contract

**Status:** PROPOSED / reversible  
**World:** AURORA VEIL  
**Owner:** AGENT-02-AURORA  
**Claim:** CLM-AURORA-WORLD-001  

## Context

Current canon establishes Aurora gravity at 0.94 g and area reference temperature at 11 °C, but does not define radius, diameter, mass, obliquity, day length or a planet coordinate implementation. The production request requires planet-scale design without creating a single giant mesh or forcing precision loss into Blender/engine scenes.

## Problem

We need a stable scale contract now so terrain, architecture, creature scale, orbital representation and later streaming work can share one coordinate model. Choosing an engine-specific World Partition/floating-origin implementation before EXO-012 would overcommit the project.

## Options

### A — Earth-radius placeholder
Use 6,371 km and infer mass from 0.94 g.

Pros: familiar.  
Cons: looks like an unexamined default; not necessary for the world identity.

### B — 5,900 km rocky world
Use 5,900 km radius; 11,800 km diameter. With 0.94 g this implies ~0.805 Earth masses and ~5.59 g/cm³ mean density.

Pros: physically plausible terrestrial body, slightly smaller than Earth, reversible, compatible with 0.94 g.  
Cons: not canon until approved.

### C — keep radius UNKNOWN
Do not commit even a planning radius.

Pros: zero lore invention.  
Cons: blocks orbital scale, surface-area estimates and stable planet metadata requested by production.

## Decision

Adopt **Option B as PROPOSAL only**:

- radius: 5,900,000 m;
- diameter: 11,800,000 m;
- surface area: ~437,435,361 km²;
- local Blender scale: 1 BU = 1 m;
- Blender/world-authoring scenes remain local tangent frames near origin;
- global planetary position is metadata;
- exact engine floating-origin/world-partition implementation remains BLOCKED by EXO-012.

## Consequences

- Orbital shell and map metadata can be built now.
- No asset is placed millions of metres from Blender origin.
- Region files carry stable global anchors plus local transforms.
- Any later canon radius change requires metadata/map reprojection but should not require remodelling metre-scale assets.

## Affected scopes

- Aurora orbital representation;
- terrain tiling;
- streaming/HLOD;
- regional origin anchors;
- world map;
- orbital cinematics;
- future engine integration.

## Reversibility

High. Radius is isolated as metadata until accepted into global canon.

## Acceptance

- no world asset depends on a hard-coded engine origin scheme;
- scene units remain physical metres;
- region anchor metadata is present before multi-region exports;
- documentation always labels the 5,900 km value PROPOSAL until canonized.
