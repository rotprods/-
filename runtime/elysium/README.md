# ELYSIUM NULL — Godot 4.7.2 runtime bridge

Claim: `CLM-ELYSIUM-RUNTIME-GODOT-001`  
World owner: `ART-ELYSIUM-001` / `art/world-elysium-null-001` / PR #15  
Contribution branch: `runtime/elysium-godot-adapter-001`  
World Master: `00152eea-2da0-40ec-8666-78d6764c718f`  
Engine-facing export contract: revision **47**

## Purpose

This directory is the executable, non-ignored boundary from the ELYSIUM World Master into the current EXOVANT Godot 4.7.2 prototype. It intentionally lives outside `art_source/`, because `art_source/.gdignore` makes descendant resources unavailable to Godot's resource loader and project export.

The bridge is offline and deterministic. It consumes a checked-in manifest derived from the World Master and never depends on remote providers at game runtime.

## Files

- `runtime_manifest.json` — compact engine-facing projection of the R47 World Master contract.
- `elysium_runtime_adapter.gd` — validates the contract, imports the owned GLB when present, applies deterministic world-state timing semantics and exposes streaming requests.
- `elysium_runtime.tscn` — minimal integration scene with isolated `AssetRoot`.
- `elysium_runtime_smoke.gd` — headless contract/native qualification gate.
- `assets/README.md` — exact binary requirement and transport truth.

Authoring/ownership evidence remains under `art_source/worlds/elysium_null/evidence/` and is not runtime-loaded.

## Contract-only gate

```sh
Godot_v4.7.2-stable_linux.x86_64 --headless --path . \
  --script res://runtime/elysium/elysium_runtime_smoke.gd \
  -- --contract-only
```

It validates and executes:

- schema, claim identity, engine pin and R47 source revision;
- 17 unique deterministic 256 m streaming cells;
- register-only macro placement policy;
- 3 world states / 5 transitions / 11 events / 19 subsystem adapters;
- 19 population routes / 118 sockets;
- EDEN 48 m arena, damage/population radii ≤24 m and 1.5 s relocation warning;
- adapter/scene parse and instantiation;
- actual debounce + minimum-dwell behavior for CONTROLLED→ANOMALY→EMERGENCY;
- macro-cell metadata exposure without inventing a macro→local transform.

A contract-only PASS is never a native GLB import PASS.

## Native import gate

```sh
Godot_v4.7.2-stable_linux.x86_64 --headless --path . \
  --script res://runtime/elysium/elysium_runtime_smoke.gd
```

Native mode additionally requires `assets/elysium_world.glb`, Godot import as `PackedScene` and successful instantiation.

## Streaming/origin safety

The World Master deliberately distinguishes:

- `MACRO_REFERENCE_SPACE`
- `LOCAL_PRODUCTION_SPACE`

The 17 macro cells are therefore registered as deterministic metadata only. No Godot transform is generated until these are qualified:

1. origin-rebasing policy;
2. macro→local mapping;
3. target-engine precision budget;
4. native HLOD/occlusion/streaming measurements.

This is a hard anti-regression rule after earlier double-offset transform defects were caught and corrected in Blender.

## World State Bus

Initial state: `CONTROLLED`.

Priority:

- CONTROLLED = 100
- ANOMALY = 200
- EMERGENCY = 300

The adapter latches only declared events, evaluates state minimum dwell, event debounce and transition cooldown, implements `ANY`/`ALL`, resolves eligible transitions by priority, clears old-state latches after transition, and emits state requests to all 19 subsystem targets. It does not overwrite story/history authority or claim native AI implementation.

## Current truth

Implemented source boundary:

- R47 engine-facing manifest;
- executable Godot adapter and scene;
- deterministic timed state machine interface;
- register-only streaming-cell interface;
- GLB binary import/instantiation gate;
- contract-only/native smoke executable.

Still unqualified:

- exact R47 GLB copied into `runtime/elysium/assets/`;
- ELYSIUM-specific native smoke result;
- player/camera/dodge traversal against the full World Master;
- navmesh rebuild/update cost;
- native HLOD/occlusion/streaming behavior;
- origin rebasing/macro→local decision;
- production GPU profile;
- human GATE-ART.

## Next executable action

Recover the exact revision-47 GLB into `runtime/elysium/assets/elysium_world.glb`, run native smoke, then create a bounded traversal/profiling harness inside this ELYSIUM runtime namespace rather than editing shared `scripts/world.gd`.
