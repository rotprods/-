# NEXT — KHEPRI Materials X100

## Immediate critical path

### 1. `MAIN_REGISTRY_ACTIVE_ACK`
Formal promotion remains gated on fleet state:

- serialize `CLM-KHEPRI-MATERIALS-001` into current published `main:ops/fleet/registry.json`;
- owner ACK epoch 1;
- read back `active`;
- preserve the current branch/project IDs and avoid semantic/path collisions.

Authoring evidence already exists under explicit user authorization, but **formal producer promotion is not claimed** until this gate passes.

### 2. `QUALIFIED_LOOKDEV_CONSUMER`
The first real consumer pilot is already technically complete.

R10 proved:
- UV0 handoff across LOD0/1/2;
- Bronze + Mirror binding on visible LOD0 meshes;
- exact GLB/BLEND persistence;
- Godot import;
- material texture roles;
- instancing/resource sharing;
- fleet delivery.

It did **not** prove final material art because the consumer is Tier-D macro proxy geometry and the world has no qualified KHEPRI sky/reflection environment.

Next final-art consumer validation requires one of:

1. a qualified KHEPRI atmosphere/sky/reflection lookdev context; or
2. close-range heliostat/support geometry owned by an appropriate architecture/hero-support claim.

Do not brighten Bronze, increase Mirror roughness or bake fake reflections merely to make the current proxy read as final art.

### 3. `PRODUCTION_TEXTURE_TIER_QUALIFICATION`
Still blocked by target-hardware evidence.

Required inputs:
- representative target GPU/memory platform;
- texture streaming/virtual-texture policy;
- compression format support;
- representative scene residency/profile capture.

Only then decide:
- final source/runtime resolution tiers;
- mip policy;
- compression target;
- material/texture memory envelope;
- close-range hero budget.

128² calibration maps MUST NOT be promoted as production-resolution texture art.

### 4. `WORLD_COMPILER_ARTKIT_CONSUMPTION`
`KHP_MAT_ARTKIT_001` is compiled and validated.

Next systems work should consume it through semantic requests such as:

```yaml
world_id: khepri
context: heliostat_structure
semantic_role: structure
state: service_clean
finish: cast_structural
scale: architectural
```

Required tests:
- allowed-context request resolves deterministically;
- forbidden-context request rejects deterministically;
- stable application IDs survive world-generation seeds;
- state changes are driven by authored story/gameplay/environment tags rather than random variation;
- generators never silently cross world/faction boundaries.

## Subsequent X100 expansion

After the four gates above:

- apply material recipes to a second real consumer with qualified geometry ownership;
- build trim/tile/decal policy from measured consumer needs, not by default;
- author higher-resolution family sources only after hardware tiers exist;
- feed Ciudad de los Toldos / Mar de Cristal / Crisol de RAKHET through their future domain claims;
- use material history to express ERA_0 / ERA_1 / ERA_2 without random grunge;
- extend ArtKit context rules as new canonical KHEPRI infrastructure appears.

## Completed since previous NEXT

- `BLOCK-KHP-MAT-002` UV0 handoff → RESOLVED.
- first real consumer `KHP_WM_HELIOSTAT_FOOTPRINTS` → TECHNICAL PASS.
- R10 exact GLB/BLEND → persistent + SHA-bound.
- R10 Godot import/resource sharing → PASS.
- R10 fleet delivery → PASS.
- KHEPRI World Compiler Material ArtKit → PASS (6 families / 139 applications).
- final visual consumer gate correctly converted into downstream lookdev blocker `BLOCK-KHP-MAT-003`.

## Stop / isolation conditions

Stop or isolate when a step requires:
- final Glass Sea physical-medium canon;
- atmospheric chemistry;
- target hardware budget not yet qualified;
- cross-scope geometry mutation without handoff;
- close-range architecture ownership not granted;
- human final-art approval.
