# ADR-PEL-002 · Isolated asset visual QA

**Status:** ACCEPTED_FOR_PELAGOS_PIPELINE

## Context

The PELAGOS World Master grew to include world foundation, Mercado kit, Nácar-2, coral systems, material library, THALASSA and ecology anatomy. A query that attempted four 768×768 Eevee creature validation renders while leaving the whole World Master renderable (`pelagos.ecology.visual.r17`) exceeded the 300 s Blender execution limit.

This is a pipeline-scaling defect, not evidence that the ecology assets are invalid.

## Decision

For asset-level QA in the World Master:

1. **Silhouette / anatomy / proportion gate:** temporarily hide every unrelated object inside a read-only/query operation and render only the target `asset_id` with Blender Workbench at a modest resolution (512² is the current qualified checkpoint).
2. **Material / lighting gate:** run separately in an isolated lookdev scene or with only the target asset and portable motivated lights visible. Workbench is never used to claim material or lighting quality.
3. **Engine gate:** remains separate; a Blender render never replaces import, collision, LOD or profiling evidence.
4. Visibility changes used for QA should be query-only whenever possible so production visibility state is not polluted.

## Evidence

- Failed whole-world query: `pelagos.ecology.visual.r17` → `EXECUTION_TIMEOUT` after 300000 ms.
- Qualified control: `pelagos.ecology.visual-isolated.r17` → four 512×512 isolated Workbench renders completed in ~14 s.
- Receipt: `art_source/worlds/pelagos/receipts/PELAGOS-ECOLOGY-ANATOMY-002.json`.

## Consequences

- Asset QA latency becomes approximately proportional to the asset instead of the complete World Master.
- Silhouette and material quality are no longer conflated into one expensive beauty-render gate.
- Final art approval still requires appropriate in-context engine/render evidence.
- This decision is scoped to Pelagos until adopted elsewhere; it does not claim global project enforcement.

## Affected scopes

PEL/ECO/009, PEL/CHAR/012–014, PEL/ENEMY/015–017, PEL/PROP/018, PEL/QA/026 and future Pelagos hero assets.
