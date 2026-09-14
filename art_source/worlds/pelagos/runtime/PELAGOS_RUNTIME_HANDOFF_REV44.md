# PELAGOS Runtime Handoff — rev44

Status: **HANDOFF_READY / NOT RUNTIME_IMPLEMENTED**

## Source-bound delivery
- 3D Jutsu project: `39930c08-62bb-4034-b35d-70d0ce51c9d9`
- World Master revision: **44**
- Art branch: `art/world-pelagos-thalassa-001`
- Current executable runtime authority inspected: **Godot 4.7.2 / main**
- GLB remains the repository's current Blender→Godot exchange format.

## Handoff artifacts
- `pelagos_runtime_manifest.rev44.json` — normalized external semantic authority for runtime import.
- `PELAGOS_GODOT_ACTIVATION_CONTRACT.md` — integration, persistence, collision, state-swap and acceptance contract.
- `validate_pelagos_runtime_manifest.py` — stdlib-only cold-check validator for the manifest.

Creation commits in this handoff wave:
- manifest: `41b66ba0e00f11673a12cdd6e19a6961564d5715`
- activation contract: `b1471ba497cdda87ab080b09a9ec6d1a816fea81`
- manifest validator: `4437264e6dbe1ad0806464783af66c5918e1a003`

## Manifest coverage
- cultural/everyday systemic families: **30**
- machinery families: **9**
- machinery socket groups: **9**
- sessile ecological guild families: **9**
- reversible damage/recovery families: **8**
- semantic/stateful family groups excluding sockets: **56**

## Runtime facts that constrain implementation
- `scripts/world.gd` currently instantiates `assets/reliquary_gate.glb` directly and recursively removes imported cameras/lights/presentation floors.
- interaction registration currently uses `{id,label,position,radius}` and `world.interact()` dispatch.
- `Progress` is the persistent campaign domain.
- `Progress.VERSION == 1` and `Progress.validate()` has a closed Terra schema.
- `SaveStore` rejects any parsed payload that `Progress.validate()` rejects.

Therefore Pelagos state persistence cannot be added safely by silently appending fields to the existing v1 snapshot. The contract requires an explicit versioned migration path before persistent Pelagos state is enabled.

## Critical semantic rules
- External manifest is authority; do not depend on Blender custom properties surviving GLB import.
- Do not infer semantic type from ID prefix alone; machinery sockets are not machinery families.
- Purpose metadata does not automatically create gameplay interaction.
- Cultural/sessile/damage hidden state nodes must remain non-interactive and non-colliding.
- Damage overlays do not own blocking collision by default; host architecture remains collision authority.
- Machinery current roots/sockets exist, but runtime visual state-swapping is not yet fully authored as four per-family physical states.
- Hidden Blender LOD helpers are not production HLOD/performance qualification.

## Required next owner
A runtime integration owner must resync `main`, perform Fleet/claim preflight, and implement the activation contract in a runtime-owned scope. This art branch must not mutate Terra runtime or global STATE/PLAN/MANIFEST as a shortcut.

## Honest blockers / non-claims
Still pending:
- source-bound GLB admission into the Godot runtime branch;
- runtime manifest/node validation in Godot;
- Progress v2 migration + save round-trip;
- gameplay-approved interaction subset;
- collision/query/nav bindings;
- LOD/HLOD/streaming thresholds;
- target-GPU qualification;
- semantic GATE-ART visual qualification.

Do not reopen bulk Pelagos family modeling unless one of these gates identifies a concrete missing asset requirement.
