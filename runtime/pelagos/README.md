# Pelagos Godot runtime bridge — rev44

Claim: `CLM-PELAGOS-RUNTIME-GODOT-001`  
Owner world branch: `art/world-pelagos-thalassa-001`  
Source World Master: Higgsfield `39930c08-62bb-4034-b35d-70d0ce51c9d9`, revision **44**  
Target runtime: **Godot 4.7.2**

## What this implements

This namespace turns the Pelagos rev44 art handoff into an engine-facing contract without touching shared Terra gameplay:

- 56 stable family records: 30 cultural, 9 machinery, 9 sessile ecology, 8 reversible damage families;
- 47 stateful families with explicit state-node mappings/patterns;
- 9 machinery socket groups;
- 224 unique native node resolution keys;
- fail-closed GLB import/instantiation gate;
- duplicate/missing required-node rejection;
- deterministic visible-state switching by stable asset ID;
- versioned Pelagos world-state snapshot/restore (`EXOVANT.PELAGOS.STATE.v1`);
- namespaced `campaign_v2_world_patch()` projection for a future global `Progress` migration;
- deny-by-default interaction allowlist;
- non-blocking collision policy boundary; no automatic collision is derived from visible meshes;
- separate static manifest validation and Godot smoke modes.

## Truth boundary

Current truth is `IMPLEMENTED_EXECUTABLE_SOURCE_NOT_PELAGOS_NATIVE_QUALIFIED`.

A contract-only PASS proves schema, IDs, state grammar and in-memory state roundtrip. It does **not** prove that the rev44 GLB imports, that its node names survive Godot import, or that collision/navigation/performance/art gates pass.

Native qualification requires the exact rev44 GLB at:

`runtime/pelagos/assets/pelagos_world_rev44.glb`

Expected source artifact metadata:

- size: `19,524,308` bytes;
- etag: `4aa72fec83eca94619f1b0a761e28c1e`.

Do not substitute another Blender revision under this filename.

## Gates

Static manifest gate:

```bash
python3 runtime/pelagos/validate_manifest.py
```

Godot contract-only smoke:

```bash
Godot_v4.7.2-stable_linux.x86_64 --headless --path . \
  --script res://runtime/pelagos/pelagos_runtime_smoke.gd -- --contract-only
```

Native smoke after exact GLB recovery:

```bash
Godot_v4.7.2-stable_linux.x86_64 --headless --path . \
  --editor --quit-after 2
Godot_v4.7.2-stable_linux.x86_64 --headless --path . \
  --script res://runtime/pelagos/pelagos_runtime_smoke.gd
```

Native PASS requires `PackedScene` import/instantiation, all 224 required resolution keys exactly once, current-state application and a reversible state-swap witness.

## Save integration

The current global `scripts/progress.gd` is version 1 and rejects unknown payload shape through `Progress.validate()`. This branch therefore does not modify `Progress` or `SaveStore`.

`campaign_v2_world_patch()` emits only a proposal namespace:

```text
worlds.PELAGOS = EXOVANT.PELAGOS.STATE.v1
```

A runtime-owned integration against current `main` must implement and test the global v1→v2 migration before this data is persisted in campaign saves. Silently adding fields to v1 is forbidden.

## Explicit exclusions

- `scripts/world.gd`, `scripts/progress.gd`, `scripts/save_store.gd`;
- shared scenes and Terra gameplay;
- automatic pickup/inventory/quests for the cultural props;
- blocking collision generation from render geometry;
- runtime fracture/debris/navmesh mutation for damage overlays;
- streaming/HLOD thresholds;
- target-GPU qualification;
- Unreal migration decision;
- semantic GATE-ART / human art approval.

The next admissible step is exact rev44 GLB recovery + native smoke. After that, open a separate global-runtime integration claim for `Progress` v2 and shared world loading rather than expanding this namespace into another monolithic `world.gd`.
