# AURORA VEIL — LOCAL LEARNINGS / PROMOTION QUEUE

These observations are scoped to `CLM-AURORA-WORLD-001`. They are not promoted into the shared `learning/hub/events.jsonl` from this isolated branch because that index is a multi-agent hotspot. Promotion should happen during reviewed integration after resync.

## AUR-LRN-001 — Split remote world mutations by semantic checkpoint

- Symptom: `aurora-world-master-r1` combined macro geometry, population, orchard and three renders and exceeded the 300 s remote Blender worker limit.
- Mechanism: model creation + GLB checkpoint/export + multiple Eevee renders accumulated inside one mutation deadline.
- Correction: separate foundation, orchard/population, scale fixes and rendering into independent operations.
- Evidence: first operation timed out with no committed revision; staged geometry operations then completed and committed revisions successfully.
- Boundary: applies to the currently observed 3D Jutsu worker/deadline; not a universal Blender performance law.
- Proposed promotion: remote-editable-art-pipeline runbook.

## AUR-LRN-002 — Camera far clip is a world-scale QA gate

- Symptom: overview exposure was nearly uniform dark sky even though the local world existed and close cameras rendered signal.
- Mechanism: overview camera was ~4.9 km from target while default Blender camera far clip was ~1 km.
- Correction: set delivery-camera far clip from actual scene extent; current overview = 12 km, camp = 5 km, AEON = 2.5 km.
- Evidence: overview exposure moved from mean 0.0207 / p99 0.0244 to final observed mean 0.1793 / p99 0.8541, without white clipping.
- Boundary: camera-frustum/clip issue, not a lighting rule; far clip should be chosen from scale and precision constraints.
- Proposed promotion: art/visual-validation runbook.

## AUR-LRN-003 — Dimensional manifest must be tested against Blender geometry

- Symptom: initial observatory torus reported 50.6 m actual extent although proposal said 48 m; Peregrino blockout also exceeded manifest dimensions.
- Mechanism: torus major radius described centerline rather than outer diameter, and primitive body half-extents were chosen approximately.
- Correction: query `Object.dimensions`, then apply exact target dimensions before treating blockout as scale-qualified.
- Evidence: final audit reports 48.0 m observatory ring, 50.0 m arena and 5.8×2.7×2.4 m Peregrino.
- Boundary: applies to production dimensions; artistic silhouettes may still change when proposal dimensions are deliberately revised through ADR/manifest update.
