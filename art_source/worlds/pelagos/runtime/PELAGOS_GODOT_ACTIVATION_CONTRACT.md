# PELAGOS — Godot Runtime Activation Contract · rev44

Status: **HANDOFF_READY / NOT RUNTIME_IMPLEMENTED**  
World: `PELAGOS`  
World Master: 3D Jutsu project `39930c08-62bb-4034-b35d-70d0ce51c9d9`, revision **44**  
Art owner branch: `art/world-pelagos-thalassa-001`  
Runtime authority inspected: `main`  
Current executable engine: **Godot 4.7.2**  
Production candidate: Unreal 5.8, still blocked on EXO-012 representative-scene benchmark.

This document is a boundary contract. It deliberately does **not** modify `scripts/world.gd`, `scripts/progress.gd`, `scripts/save_store.gd`, global STATE/PLAN/MANIFEST or the active Terra gameplay unit from this world-art branch.

## 1. Why the frontier moved

Pelagos Blender breadth is no longer the dominant gap. By rev44 the world has a structurally verified stateful foundation across machinery, sessile ecology, reversible damage and a normalized **30-family cultural/everyday prop floor**. Continuing to add families without a gameplay/narrative requirement would optimize object count rather than product value.

The next useful work is activation:

`BLENDER SOURCE -> GLB DELIVERY -> MANIFEST VALIDATION -> GODOT NODE RESOLUTION -> STATE BINDING -> QUERY/COLLISION -> PERSISTENCE -> STREAMING/LOD -> PLAY/PERF/ART GATES`

## 2. Facts from the current Godot runtime

Current `main` establishes the following integration constraints:

- `scenes/main.tscn` loads `scripts/world.gd`.
- `world.gd` directly imports the existing `assets/reliquary_gate.glb`, calls `clean_presentation()`, then places it in the scene.
- `clean_presentation()` recursively removes imported `Camera3D`, `Light3D` and presentation-floor nodes.
- Current interactions are registered as dictionaries containing `id`, `label`, `position`, `radius`; player input calls `world.interact()` and the handler dispatches by `item.id`.
- `Progress` is the authoritative persistent campaign state.
- `SaveStore` verifies a SHA-256 envelope, parses the payload, and **rejects it unless `Progress.validate()` accepts it**.
- `Progress.VERSION == 1` and its validation schema is closed over the Terra fields. Arbitrarily adding `pelagos`, `worlds`, or per-asset state to the current snapshot would therefore make the save invalid.
- `world.gd` already carries a large amount of Terra presentation/gameplay. Repository architecture explicitly forbids solving twelve worlds by growing one giant script.

Consequence: Pelagos must integrate through a data-driven adapter/domain boundary, not hundreds of new `match` arms inside `world.gd`.

## 3. Delivery inputs

A runtime integration branch MUST consume these art-side authorities together:

1. World Master rev44 GLB export from Jutsu project `39930c08-62bb-4034-b35d-70d0ce51c9d9`.
2. `art_source/worlds/pelagos/runtime/pelagos_runtime_manifest.rev44.json`.
3. Claim receipts and deterministic source contracts under `art_source/worlds/pelagos/receipts/` and `scripts/`.
4. This activation contract.

The GLB is geometry/presentation transport. The JSON manifest is semantic authority. Blender custom properties MAY survive some import paths, but runtime correctness MUST NOT depend on that.

## 4. Proposed runtime boundary

The runtime implementation should create a small generic world-state layer plus a Pelagos adapter. Exact filenames may be reconciled by the runtime owner; responsibilities are normative.

### 4.1 Generic `WorldAssetStateRegistry`

Responsibilities:

- load a validated external manifest;
- index stable `asset_id` records;
- resolve required imported node names exactly once;
- apply one active visual state per state group;
- make hidden states non-interactive and non-colliding;
- expose safe query methods (`has_asset`, `allowed_states`, `get_state`, `set_state`);
- reject unknown asset IDs or invalid state transitions without mutating the last valid scene state;
- serialize only persistent state, never render-node references.

### 4.2 `PelagosRuntimeAdapter`

Responsibilities:

- instantiate the Pelagos GLB under a dedicated world root;
- reuse/centralize the existing presentation cleanup rule rather than duplicating cameras/lights/floors;
- validate `world_id == PELAGOS`, source revision and manifest schema;
- resolve every required state node/socket/target from the manifest;
- apply initial states from persisted world state, falling back to manifest current states only for first load;
- publish **approved** interaction descriptors to the existing interaction layer or its successor;
- own Pelagos-specific runtime wiring without putting 56 family groups into `world.gd`.

### 4.3 `world.gd`

`world.gd` should become a coordinator, not the Pelagos asset database. The expected integration is conceptually:

1. choose/load destination world;
2. instantiate its adapter;
3. provide shared services (player, interaction gateway, persistence gateway, UI/event bus as applicable);
4. let the adapter own world-local asset state.

Do not add one `match` branch for every Pelagos asset family.

## 5. Import / node-resolution contract

At load time:

1. Instantiate the GLB.
2. Remove imported presentation-only nodes using the existing cleanup behavior or a shared equivalent.
3. Load `pelagos_runtime_manifest.rev44.json`.
4. Resolve manifest nodes recursively by exact name.
5. Required node name appears zero times -> family enters `IMPORT_INVALID`; fail closed for that family and emit diagnostic.
6. Required node name appears more than once -> reject import contract; ambiguity is not repaired by “first match”.
7. Unknown extra GLB nodes do not gain semantics automatically.
8. State templates such as `PEL_CIV3_REST_{STATE}` substitute normalized uppercase state tokens only after the state has been validated against the family’s allowed state list.
9. Machine socket nodes are a separate type. `*-SOCKET` IDs MUST NOT be counted or instantiated as additional machinery families.
10. Damage family semantics come from manifest/source receipt, not scene-hierarchy discovery.

## 6. State-swap semantics

Stateful cultural, sessile and damage families already carry multiple authored visual states.

`set_state(asset_id, new_state)` must be atomic from the caller’s perspective:

- validate asset ID;
- validate `new_state` is allowed;
- resolve target node before changing visibility;
- enable target state;
- disable all sibling state nodes;
- disable query/collision on hidden siblings;
- update persistent domain state only after the visual transition succeeds;
- emit a deterministic state-changed event if/when an event bus exists.

Calling `set_state(id, current_state)` is idempotent.

### Machinery exception

The current World Master contains one physical current-state machinery root per family plus semantic configuration grammar, sockets, LOD/collision proxies. Runtime MUST NOT pretend four fully authored machinery visual states are already swappable from one imported GLB. Machinery state transitions stay read-only/semantic until explicit per-state runtime-ready geometry is delivered.

## 7. Interaction contract

`purpose` is descriptive metadata, **not permission to make the object interactive**.

The runtime owner must define an approved interaction subset backed by gameplay design. Until then:

- cultural families may be inspectable/queryable but do not automatically grant pickup/use/inventory mechanics;
- machinery sockets do not imply fluid simulation or power simulation;
- sessile ecology does not imply harvesting or ecological simulation;
- damage states do not imply repair gameplay;
- acoustic naming does not imply a finished audio mechanic.

For approved interactions, keep stable interaction IDs independent from translated labels. The current `{id,label,position,radius}` mechanism can be adapted initially, but Pelagos interaction definitions should live in data/adapter code rather than a giant central `match`.

## 8. Collision / navigation mapping

Never generate gameplay collision directly from high-detail visible meshes by default.

Manifest policies map as follows:

- `query_only_until_gameplay_binding` -> no `StaticBody3D` by default; optional `Area3D`/query shape only after interaction approval.
- `none_or_soft_query` -> non-blocking by default; optional soft query volume.
- `none_or_query_until_runtime_damage_binding` -> damage overlay never owns route-blocking collision; the host architecture remains collision authority unless a future gameplay change explicitly mutates navigation/collision.
- `unbound` -> no automatic collision until audited.

Machinery has authored collision proxies, but proxy-to-Godot shape mapping and production collision budgets remain a separate integration gate. Hidden alternate states and hidden LOD helpers must never contribute collision/navigation.

## 9. Persistence migration — REQUIRED before stateful Pelagos save

Current `Progress.VERSION = 1` cannot store Pelagos state without failing validation. The safe path is an explicit v2 migration.

### 9.1 Proposed v2 payload extension

Preserve all current Terra fields and add a bounded world-state dictionary:

```json
{
  "version": 2,
  "flags": {},
  "rewards": [],
  "memories": 0,
  "choice": "",
  "valves": [0,0,0],
  "checkpoint": [0.0,1.0,18.0],
  "echo": [],
  "echo_value": 0,
  "worlds": {
    "PELAGOS": {
      "schema": 1,
      "asset_states": {
        "PEL-PROP-REST-SLING-003": "used"
      },
      "flags": {}
    }
  }
}
```

The example is schema shape only; it does not authorize new Pelagos gameplay flags.

### 9.2 Migration algorithm

1. Verify the existing SaveStore envelope SHA exactly as today.
2. Parse payload.
3. If `version == 1`, validate it against the **old v1 rules** before migration.
4. Produce an in-memory v2 payload preserving every existing Terra field and adding `worlds = {}`.
5. Validate the migrated v2 payload.
6. Do not rewrite the user’s save merely because it was loaded; next explicit save can serialize v2 through the same temp/verification/backup pipeline.
7. If v1 data fails v1 validation, retain current failover-to-backup behavior. Migration must never “repair” a corrupt payload into validity.

### 9.3 Validation responsibilities

Persistence validation has two layers:

- structural save validation: bounds/types/size/version and safe world-state shape;
- semantic Pelagos validation: asset IDs and allowed states against the runtime manifest.

An invalid Pelagos state must not corrupt or discard otherwise valid Terra progress. Prefer rejecting the invalid world-state mutation before it enters the snapshot.

## 10. Streaming / LOD boundary

The authored hidden LOD1 helpers are semantic/authoring evidence, not production threshold qualification.

Runtime integration must later define:

- cell ownership and streaming granularity;
- distance/screen-size LOD thresholds;
- HLOD grouping for settlement/ecology;
- collision lifetime relative to render LOD;
- interaction/query lifetime relative to streamed cells;
- memory budgets;
- CPU/GPU frame budgets on the target device.

Do not claim a production LOD/HLOD system because hidden Blender LOD helpers exist.

## 11. Minimum acceptance suite for a runtime PR

A Pelagos activation PR is not admissible without automated evidence for at least:

### Manifest/import
- valid manifest loads;
- wrong `world_id`, wrong schema or missing required keys fail closed;
- every required node resolves exactly once in the imported representative GLB;
- machine sockets are classified as sockets, not duplicate families;
- imported Camera3D/Light3D/presentation-floor nodes are absent after cleanup.

### State swaps
- each stateful family accepts all declared states;
- invalid state is rejected without changing visible state;
- invalid asset ID is rejected;
- exactly one state node is visible after every swap;
- repeated same-state set is idempotent;
- hidden states have no active collision/query registration.

### Persistence
- existing valid v1 Terra save migrates in memory to valid v2 without losing any field;
- corrupt v1 remains rejected and backup fallback still works;
- v2 round-trip through SaveStore preserves Pelagos asset states and Terra progress;
- unknown asset/state cannot be committed into a valid snapshot;
- failed write still preserves healthy backup and prior main save.

### Interaction / collision
- no manifest family becomes interactable solely from `purpose`;
- approved interaction IDs remain stable across labels/localization;
- damage overlays do not block the bridge route by default;
- sessile `none_or_soft_query` families never create blocking StaticBody3D automatically.

### Regression
- existing Terra `tests/test_state.gd`, world/input tests and native Gauntlet remain green;
- cold-load representative Pelagos scene produces no duplicate stable IDs or missing-node diagnostics.

## 12. Performance qualification gate

A representative Pelagos cell must be profiled in the actual selected production runtime/hardware before any AAA/performance claim.

Capture at minimum:

- frame CPU and GPU time;
- draw calls;
- triangles/primitives after import and active LOD;
- material count;
- texture memory;
- resident scene memory;
- load/stream latency;
- collision/query object count;
- state-swap spike cost.

Godot 4.7.2 is the current executable authority. Unreal 5.8 remains a candidate until EXO-012 compares the same representative scene under equivalent controls/content and measured CPU/GPU/memory/load/export conditions.

## 13. Semantic GATE-ART

Structural QA is not final visual qualification. A future art gate must compare representative Pelagos frames against approved target imagery and explicitly reject:

- procedural repetition visible at gameplay distance;
- AI-slop silhouettes;
- arbitrary grunge;
- inconsistent material response;
- unsupported decorative sci-fi language;
- scale cues that contradict traversal/engineering;
- lighting that hides rather than validates geometry/material quality.

This gate should use stable camera IDs and source-revision-bound evidence.

## 14. Runtime-branch execution order

A future runtime owner should execute:

`RESYNC main -> read AGENTS/STATE/PLAN/HANDOFF -> Fleet/ownership preflight -> claim runtime integration scope -> import rev44 GLB -> add/copy runtime manifest -> implement manifest validator -> implement world asset-state registry -> implement Progress v2 migration -> bind Pelagos adapter -> tests -> native Gauntlet -> representative play/capture -> persist receipt/handoff`

Do **not** begin by adding dozens of `match` arms to `world.gd`.

## 15. Definition of Done for “Pelagos activated in Godot”

All of the following are required:

- representative Pelagos GLB imported from a source-bound rev44 export;
- manifest validated and all required nodes resolved;
- cultural/sessile/damage state swaps work deterministically;
- persistence v2 migrates v1 and survives cold restart;
- collision/query policy is explicit and route-safe;
- approved interaction subset works through stable IDs;
- no regression to Terra save/gameplay tests;
- LOD/streaming configuration exists with measured evidence;
- target-hardware profile exists;
- semantic GATE-ART representative views pass.

Until then the correct status is **HANDOFF_READY / NOT RUNTIME_IMPLEMENTED**.
