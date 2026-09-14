# ELYSIUM NULL — Godot 4.7.2 runtime bridge

Claim: `CLM-ELYSIUM-RUNTIME-GODOT-001`  
World owner: `ART-ELYSIUM-001` / `art/world-elysium-null-001` / PR #15  
Contribution branch: `runtime/elysium-godot-adapter-001`  
Remote World Master: `00152eea-2da0-40ec-8666-78d6764c718f`  
Runtime export contract: Blender/Higgsfield revision **47**

## Purpose

This directory is the narrow integration boundary from the ELYSIUM World Master to the currently executable EXOVANT prototype in Godot 4.7.2. It does **not** replace the world owner, global gameplay systems, or the later production-engine decision.

The bridge is intentionally offline and deterministic. It consumes a checked-in runtime manifest derived from the World Master and never calls external providers at game runtime.

## Files

- `runtime_manifest.json` — compact engine-facing projection of the R47 Blender contract.
- `elysium_runtime_adapter.gd` — validates the contract, imports the owned GLB when present, routes global world-state events and exposes streaming-cell activation/deactivation requests.
- `elysium_runtime.tscn` — minimal integration scene with a dedicated `AssetRoot`.
- `elysium_runtime_smoke.gd` — headless contract/native gate.
- `assets/README.md` — exact local asset requirement; binary is not falsely claimed present.
- `evidence/CLM-ELYSIUM-RUNTIME-GODOT-001.json` — claim and truth-state receipt.

## Gates

Contract-only gate:

```sh
Godot_v4.7.2-stable_linux.x86_64 --headless --path . \
  --script res://art_source/worlds/elysium_null/runtime/elysium_runtime_smoke.gd \
  -- --contract-only
```

This validates/parses the adapter and scene and asserts:

- schema + claim identity;
- 17 unique deterministic streaming cells;
- 3 world states / 5 transitions / 11 events / 19 adapters;
- 19 population routes / 118 sockets;
- EDEN 48 m arena invariant;
- EDEN damage/population radii ≤24 m;
- canonical 1.5 s relocation warning.

Native import gate:

```sh
Godot_v4.7.2-stable_linux.x86_64 --headless --path . \
  --script res://art_source/worlds/elysium_null/runtime/elysium_runtime_smoke.gd
```

Native mode additionally requires `assets/elysium_world.glb`, Godot import as `PackedScene`, and successful instantiation. A contract-only PASS is **not** a native import PASS.

## Coordinate / streaming safety

The World Master has separate `MACRO_REFERENCE_SPACE` and `LOCAL_PRODUCTION_SPACE`. The 17 256 m macro cells are therefore registered as deterministic metadata only. The adapter deliberately does **not** turn `macro_location_m` into Godot transforms until the project explicitly qualifies:

1. origin-rebasing policy;
2. macro→local mapping;
3. target-engine precision budget;
4. native HLOD/occlusion/streaming measurements.

This prevents double-offset and silent axis/origin errors already encountered and corrected during Blender production.

## World State Bus

Initial state: `CONTROLLED`.

Priority:

- CONTROLLED = 100
- ANOMALY = 200
- EMERGENCY = 300

`push_event()` consumes only manifest-declared events, respects state dwell/cooldown requirements, resolves eligible transitions by priority, and emits adapter-state requests for all 19 ELYSIUM subsystem targets. It does not mutate story/history authority or invent native AI behavior.

## Current truth

`implemented`:

- R47 engine-facing manifest boundary;
- Godot adapter source;
- deterministic state transition interface;
- register-only streaming interface;
- binary import gate;
- contract/native smoke entrypoint.

`not yet qualified`:

- local R47 GLB copied into `assets/`;
- native Godot import/instantiation result;
- player/camera/dodge traversal against this full world master;
- navmesh rebuild/update cost;
- native HLOD/occlusion/streaming behavior;
- production GPU profile;
- human GATE-ART.

## Next executable action

Recover the exact World Master GLB for revision 47 into `runtime/assets/elysium_world.glb`, run the native smoke gate, then integrate a bounded player-scale traversal scene without editing shared `scripts/world.gd` from this atomic subclaim.
