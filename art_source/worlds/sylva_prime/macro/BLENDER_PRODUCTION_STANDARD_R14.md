# SYLVA PRIME — BLENDER PRODUCTION STANDARD R14

**Purpose:** production-engineering contract for Blender assets that enter SYLVA PRIME.  
**Blender baseline observed:** 5.2.0 LTS in remote 3D Jutsu.  
**Units:** metric, 1 BU = 1 metre for current pipeline.  
**Current accepted macro source:** primary remote r13.  
**Important:** this standard does not transfer ownership. PR #6 remains owner of reusable neural-root modules.

---

# 1. Core engineering principles

1. **Macro shape before meso detail before micro detail.**
2. **Physical cause before noise.**
3. **Editable source before destructive bake.**
4. **One source asset, many instances; never duplicate cross-cell geometry to fake streaming.**
5. **Render geometry and collision are distinct interfaces.**
6. **LOD preserves silhouette/function, not arbitrary triangle percentages.**
7. **Every generator has deterministic inputs, version and bake/export path.**
8. **Every hero asset can be reconstructed from source without chat context.**
9. **Do not use a world-scale mesh as a substitute for tile hierarchy.**
10. **Do not add final detail to an asset whose owner/dependency/gate is unresolved.**

---

# 2. Scene coordinate contract

## Units

- `scene.unit_settings.system = METRIC`
- `scene.unit_settings.scale_length = 1.0`
- 1 Blender unit = 1 m.

## Axis

- Blender source: Z-up.
- Export: normal glTF conversion; never add a second global axis rotation downstream.

## World/local split

Current local authored patch:
- 12 km × 12 km.

Current terrain partition:
- 4×4 L3 cells;
- 3 km × 3 km each.

Terrain tile mesh coordinates:
- XY centered around local cell origin;
- world placement comes from `SYLVA_STREAM_L3_X#Y#` parent;
- Z remains source-world elevation.

Rationale:
- smaller local coordinates;
- clean cell ownership;
- exact duplicated boundary samples;
- backend-neutral streaming interface.

---

# 3. Naming contract

Use stable semantic prefixes.

## World / terrain
- `SYLVA_TERRAIN_L3_X#Y#`
- `SYLVA_COL_TERRAIN_L3_X#Y#`
- `SYLVA_STREAM_L3_X#Y#`
- `SYLVA_STREAM_REGION_*`

## Macro biology
- `SYLVA_ROOT_PRIMARY_*`
- `SYLVA_ROOT_SECONDARY_*`

These are macro topology owned by current claim; **not reusable PR #6 production modules**.

## Region
- `SYLVA_PUERTO_*`
- `SYLVA_BOSQUE_*`
- `SYLVA_VESPER_*`

## Navigation
- `SYLVA_TRAV_*`
- `SYLVA_COL_ROUTE_*`

## Integration
- `SYLVA_SOCKET_*`
- `SYLVA_META_*`

## Collision
Every macro collision object begins `SYLVA_COL_` and is non-final visible art.

Never overload one object name for two semantic purposes.

---

# 4. Transform / origin policy

## General

Production static meshes should reach integration with:
- scale `(1,1,1)`;
- deterministic origin;
- documented forward/up basis if instanced;
- no accidental parent compensation transforms.

## Terrain
Origin = owning L3 stream-cell center.

## Modular architecture
Origin = snap interface:
- wall/floor module: lower logical grid corner or documented center snap;
- door/transition: centerline at floor datum;
- corner/cap: grid-aligned documented pivot.

## Vehicle
Origin = vehicle dynamics reference agreed with runtime owner; do not arbitrarily center geometry.

## Character/creature
Origin/skeleton root follows animation contract, not mesh bounding-box center.

## Reusable root modules
Provider must publish explicit anchor/pivot policy. Current PR #6 r4 does not satisfy this gate; do not compensate in the macro scene with arbitrary offsets.

---

# 5. Terrain production pipeline

## 5.1 L0/L1

Planet shape stays separate from local gameplay tiles. Do not generate a 15,000 km sphere inside the r13 gameplay `.blend`.

## 5.2 L2/L3

Current accepted R12 topology:
- 16 render tiles;
- 16 collision tiles;
- exact border samples.

## 5.3 Final terrain refinement rule

Future terrain sculpt/detail must preserve shared boundaries.

Allowed approaches:
1. refine a higher-resolution shared/global height representation then cut tiles;
2. edit tiles with border vertices locked to a shared boundary dataset;
3. use overlapped authoring regions and deterministic boundary reconciliation.

Forbidden:
- independently sculpting adjacent tile edges;
- per-tile noise seeds with no seam lock;
- applying destructive displacement after border split without seam verification.

## 5.4 Frequency layering

### Macro frequency
- basins;
- ridges;
- load-bearing root terrain response;
- hero-zone support planes;
- navigation shaping.

### Meso frequency
- erosion/runoff only when physically/canonically justified;
- root pressure deformation;
- compacted trails;
- local scar/deposition fields.

### Micro frequency
- material displacement/normal;
- never baked into kilometre terrain geometry indiscriminately.

## 5.5 Tile QA

Each terrain wave must test:
- border coordinate identity;
- border Z delta;
- normals/tangent discontinuity;
- collision border delta;
- material blend continuity;
- native engine seam traversal.

Source PASS requires exact border height agreement. Engine PASS additionally requires no visible crack/double collision.

---

# 6. Structural-root modeling

## 6.1 Ownership

- macro kilometer roots: current macro claim;
- reusable 8–14 m meso modules: PR #6 provider;
- final hero-specific biological structures: dedicated asset owner as claimed.

Do not create a second reusable root library here.

## 6.2 Root source representation

For large editable roots, preferred source representation:
- curve/path or explicit guide spline;
- profile parameters;
- longitudinal radius field;
- stress/load direction field;
- material zone attributes;
- deterministic mesh bake.

## 6.3 Cross-section realism

Blockout may use circular/elliptical curves.

Hero/production roots should support:
- ellipticity;
- centroid offset;
- compression flattening;
- reaction-growth thickening;
- longitudinal fiber/ridge orientation.

Do not use random radial jitter as the main organic signal.

## 6.4 Branch junctions

Final hero branch junctions need topology that communicates load transfer.

Preferred:
- smooth saddle/fusion surface;
- longitudinal edge flow into child branch;
- local mass addition at mechanically loaded crotch;
- enough loops for silhouette and deformation if animated.

Avoid:
- raw intersecting cylinders;
- unresolved boolean crease;
- perfectly symmetric Y fork when load is asymmetric.

## 6.5 Natural graft vs human graft

Natural graft:
- continuous/intergrown tissue;
- broad biological contact;
- residual fusion seam if desired.

Human graft:
- prepared interface;
- clamp/support hardware;
- wound/callus transition;
- maintenance access.

---

# 7. Root Geometry Nodes / procedural interface proposal

This section defines **requirements**, not ownership of PR #6's implementation.

A production procedural root system should be capable of accepting conceptual inputs for:
- guide curve;
- parent radius;
- radius profile;
- load vector;
- reaction-growth vector;
- ellipticity;
- centroid offset;
- mechanical/hydraulic role;
- branch/graft state;
- traffic contact mask;
- wound age/state;
- LOD target.

Outputs should include, where relevant:
- render mesh;
- walk/callus surface;
- collision proxy;
- socket/anchor metadata;
- material masks;
- deterministic asset ID/version.

All outputs sharing an asset must share the same normalized anchor basis.

---

# 8. Membrane modeling

Source should preserve:
- anchors;
- tension direction;
- boundary reinforcement;
- sag/load state.

Preferred construction:
- low-resolution controlled surface / curve boundary;
- tension-aware deformation;
- final subdivision only where tier requires;
- thickness/edge reinforcement represented physically or with controlled normal/displacement depending distance.

Avoid:
- cloth simulation noise frozen without anchor logic;
- zero-thickness membrane where close inspection exposes the edge;
- identical wrinkles across unrelated spans.

---

# 9. Hard-surface graft hardware

## Primary forms
Define:
- clamp body;
- load direction;
- fastener/locking mechanism;
- access/removal direction;
- flexible or insulating interface to living tissue.

## Bevels
Bevel width is physical and scale-dependent.

Do not use one universal bevel modifier value across:
- 20 cm clamp;
- 2 m beam;
- 50 m structure.

## Manufacturing
Use plausible process by part:
- machined contact surfaces;
- cast/forged structural body;
- bent sheet cover;
- extruded member;
- replaceable polymer/ceramic pad;
- weld only where maintenance policy allows permanent join.

## Normals
Use geometry + weighted/custom normals only if pipeline/export remains portable. Validate glTF shading after export; Blender viewport appearance is not sufficient.

---

# 10. Architecture modular-kit standard

Final Puerto architecture owner must publish:
- base grid;
- vertical datum;
- module dimensions;
- pivots;
- corner/cap/transition rules;
- door/window/access standard;
- structure vs cladding distinction;
- utility channels;
- drainage;
- host-tissue interface;
- damage/replacement variants;
- material compatibility.

A modular kit is not accepted until it builds at least:
1. one compact service structure;
2. one multi-level occupied structure;
3. one root-attached transition;
4. one maintenance route;
without custom mesh hacks at every junction.

---

# 11. Hero creature / character topology

## VESPER

Modeling sequence:
1. ecological/function contract;
2. skeleton/load/locomotion logic;
3. primary masses;
4. secondary anatomy;
5. tertiary forms;
6. deformation test sculpt;
7. retopology;
8. UV/material/bake;
9. rig;
10. LOD and hit/collision interfaces.

No amount of surface growth detail compensates for an anatomically incoherent silhouette.

## NPCs

Hero NPC production must support:
- face deformation;
- shoulder/hip/elbow/knee deformation;
- wardrobe fit;
- hair solution appropriate to runtime;
- LOD strategy;
- equipment attachment interfaces.

No clone system should be derived from the three named hero NPCs without a separate population claim.

---

# 12. Fauna modeling standard

For every creature:
- define skeleton before tertiary sculpt;
- document locomotion and ground contact;
- define feeding anatomy;
- define sensory anatomy where visible;
- define respiratory/thermal assumptions only if world biology requires them;
- validate silhouette at gameplay camera distance.

Andador de corteza specifically requires a true six-leg gait solution; not a four-leg base with two decorative appendages.

---

# 13. UV policy

Choose UV strategy by asset role, not fashion.

## Unique UV
Use for:
- hero creature/character;
- uniquely weathered hero prop;
- asset requiring baked directional damage/skin detail.

## Tileable
Use for:
- large repeating architecture surfaces;
- terrain material families;
- long root surfaces where repetition can be broken procedurally/decal/mask.

## Trim sheet
Use for:
- human graft hardware families;
- modular architecture edges/frames;
- repeated maintenance components.

## UDIM
Allowed only when:
- asset tier warrants it;
- target runtime/toolchain supports memory cost;
- texel density requirement cannot be met rationally otherwise.

No UDIM-by-default policy.

## QA
Validate:
- seam placement;
- distortion;
- padding;
- mirrored overlap intent;
- texel-density class;
- mip behavior in engine.

---

# 14. Material channel policy

Do not author channels the target runtime does not consume.

Potential PBR channels:
- Base Color;
- Normal;
- Roughness;
- Metallic;
- AO where justified by pipeline;
- Height/Displacement only where target tier/runtime supports it;
- Emissive for semantic signal states;
- Opacity/transmission for vegetation/membranes where required;
- packed masks for biological zone/state variation.

Signal emissive must remain separate from base material identity.

---

# 15. Biological material masks

Final living materials should support physical-role variation such as:
- `MASK_MECHANICAL_LOAD`
- `MASK_HYDRAULIC_ROLE`
- `MASK_REACTION_TISSUE`
- `MASK_CALLOUS`
- `MASK_WOUND_ACTIVE`
- `MASK_TRAFFIC_CONTACT`
- `MASK_GRAFT_INTERFACE`
- `MASK_LOCAL_MOISTURE`

Exact channel packing belongs to material/runtime owner.

Avoid using independent random noise for every mask.

---

# 16. Collision engineering

## Terrain
Use R12 per-cell collision tiles until runtime proves a different approach.

## Routes
Current R10 ribbons are source-QA manifold proxies.

## Architecture
Prefer:
- primitives/compound convex for simple forms;
- custom simplified shells for complex traversal surfaces;
- per-room/section collision where streaming requires it.

## Organic roots
Do not use visible high-detail hero root as collision.

Final root collision should preserve:
- walkable crown;
- major side volume;
- critical gaps/openings;
while removing micro-ridges.

## Creature/character
Collision/hit zones follow gameplay/rig contracts, not auto-convex whole body.

---

# 17. LOD engineering

Final numbers remain blocked by target engine/hardware.

Functional LOD rules:

## Root
Preserve:
- overall curve;
- junction silhouette;
- walkable crown;
- major graft/wound mass.

Reduce:
- fiber microgeometry;
- small scars;
- tertiary ridge density.

## Architecture
Preserve:
- openings;
- floor/roof outline;
- major frame;
- dominant graft interface.

## Creature
Preserve:
- limb count;
- head/sensory silhouette;
- gameplay telegraph appendages;
- contact points.

## Terrain
Use spatial hierarchy/HLOD rather than naive whole-world decimation.

---

# 18. HLOD production rule

Current R14 evidence explicitly rejects one uniform simplification ratio for all tiles.

Future HLOD generator must use feature-aware protection for:
- terrain extrema;
- VESPER basin/rim;
- root-bearing ridges;
- hero support surfaces;
- landmark silhouette.

HLOD acceptance requires:
- world-space error;
- screen-space error;
- transition popping test;
- material/shader parity check;
- target-hardware profile;
- human vista approval.

HLOD never supplies gameplay collision.

---

# 19. Streaming integration

Current source truth:
- R12 16 render + 16 collision tiles;
- R13 `stream_cells` metadata on 147 spatial objects;
- R14 hierarchy/prefetch design is fenced and not executed.

Cross-cell object rule:
- one authored source object;
- several residency references/memberships;
- no duplicated source meshes per cell unless engine backend specifically requires generated proxy instances and identity is preserved.

Bosque hero residency:
- four L3 cells;
- four L2 coverage groups;
- **not** four full-resolution L2 residency commands.

---

# 20. Export contract

## GLB
Current current-claim validator chain:
- R10 topology;
- R11 transport hardening;
- R13 streamed-terrain semantics.

Delivery must:
- be exact recovered bytes;
- bind SHA-256;
- have 4-byte aligned valid chunks;
- contain unique JSON/BIN chunks;
- use no external resources;
- preserve current required node set;
- exclude legacy monolithic terrain;
- exclude provider module meshes from macro claim.

## Blender source
A GLB alone is not editable-source delivery.

Keep `.blend` plus deterministic scripts/generators/receipts.

No absolute fragile texture paths.

---

# 21. Deterministic procedural standard

Every procedural generator records:
- generator ID/version;
- input asset/source revision;
- deterministic seed if randomness exists;
- unit contract;
- output object naming;
- material assignment;
- collision policy;
- LOD policy or unresolved status;
- export compatibility;
- QA receipt.

Randomness without persisted seed/state is not production reproducibility.

---

# 22. Tier-specific source expectations

## Tier S
- editable high detail;
- deformation/topology proof;
- UV/bake/PBR;
- rig where applicable;
- LOD/collision;
- neutral + context render;
- native engine/performance evidence.

## Tier A
Same core discipline with detail proportional to gameplay inspection.

## Tier B
Production-ready topology/material/LOD/collision but less unique close microdetail.

## Tier C
Silhouette/material identity/readable construction; optimize aggressively where invisible.

## Tier D
Macro/vista/proxy; do not spend close-detail geometry.

---

# 23. Blender QA gauntlet

Before source checkpoint:

### Geometry
- [ ] no unintended degenerate faces
- [ ] manifold where required
- [ ] normals valid
- [ ] no accidental duplicate objects/verts
- [ ] correct dimension/scale

### Transforms
- [ ] scale policy satisfied
- [ ] origin/pivot documented
- [ ] parent relation intentional

### Materials
- [ ] material slots intentional
- [ ] no missing dependencies
- [ ] portable shaders for GLB-delivered preview where required

### UV
- [ ] seams/density/padding checked where applicable

### Collision
- [ ] separate proxy where applicable
- [ ] collision ID/policy documented

### LOD
- [ ] required tier/interfaces exist or explicit BLOCKED waiver

### Streaming
- [ ] membership/owner cell valid
- [ ] no seam drift
- [ ] cross-cell source not duplicated

### Export
- [ ] Blender save succeeds
- [ ] GLB export succeeds without invalid-mesh warning
- [ ] claim-local GLB validator passes on recovered exact bytes when environment allows
- [ ] engine import/native test pending or passed explicitly

---

# 24. Visual QA gauntlet

For final art, Blender technical PASS is insufficient.

Review:
- silhouette in grayscale;
- human scale;
- construction/growth causality;
- material response under neutral light;
- close detail only for correct tier;
- in-context route readability;
- art drift with emissives disabled;
- camera obstruction;
- repeated procedural patterns;
- CGI-noise shortcuts.

---

# 25. Current blocked production actions

Do **not** currently:
- mutate primary r13 remote while writer fence is frozen;
- execute R14 hierarchy generator until fleet claim is active;
- mutate orbital r0;
- instantiate PR #6 root modules;
- generate HLOD production meshes;
- define final triangle/texture/draw budgets;
- claim final hyperreal art from current blockout.

Safe work while blocked:
- references;
- specs;
- source generators not executed;
- static validators;
- art/asset contracts;
- future atomic claim decomposition;
- native test plans.
