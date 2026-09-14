# LEVIATHAN — LOD Feasibility Envelope

Claim: `CLM-W10-WORLD-LEVIATHAN-001`  
Basis: primary Blender revision 10 / 98 shared mesh datablocks.  
Status: **MEASURED FEASIBILITY / NO FINAL LOD CHAIN**.

## Why this exists

The project previously had no LOD objects, no Decimate modifiers and no qualified engine/hardware budget. Rather than inventing generic `LOD1=50% / LOD2=25%` rules, this checkpoint measures how current geometry responds to simplification.

It does **not** choose production LOD thresholds. Final thresholds still require camera/screen-space validation, direct art review, engine import behavior and target-hardware evidence.

## Measurement method

Temporary query-only duplicates were simplified with Blender `Decimate(COLLAPSE)`. Every modifier was evaluated using a fresh depsgraph. The original and simplified surfaces were compared bidirectionally using BVH nearest-surface distances sampled at vertices plus triangle centroids.

Reported error is:
- absolute world-space metres;
- max/RMS error as a percentage of the original object's world-space bounding-box diagonal.

The first probe was rejected because its depsgraph was stale and all ratios falsely reported zero reduction. A canary then proved the corrected method by simplifying `SOMA_PROXY_NOT_FINAL` from 2,208 to exactly 1,104 triangles at ratio 0.5.

Evidence: `evidence/lod_feasibility_r10.json`.

## Representative ratio curves

Nine representative high-cost forms were tested at 75%, 50% and 25% of original triangles.

Observed maximum-error ranges:

| Triangle ratio | Triangle reduction | Max error / bbox diagonal |
|---|---:|---:|
| 0.75 | 25% | ~0.046–0.160% |
| 0.50 | 50% | ~0.093–0.319% |
| 0.25 | 75% | ~0.253–0.741% |

This demonstrates meaningful simplification headroom, especially in large smooth rings/shells. It does not establish what is visually acceptable in gameplay.

Examples at ratio 0.50:
- macro rib: ~0.094% max normalized error;
- Puerto scar ring: ~0.093%;
- SOMA proxy: ~0.134%;
- Puerto hero valve frame: ~0.101%;
- SOMA regulator ring: ~0.137%;
- lymph whale proxy: ~0.137%;
- gardener digestive sac: ~0.218%;
- SOMA contraction membrane: ~0.238%;
- lymph-channel cartilage rib: ~0.319%.

## Full 50% sweep

A broader sweep tested one representative per shared visual mesh datablock for render-visible, non-collision meshes with at least 100 original triangles.

- unique visual meshes tested: **52**;
- represented draw triangles before: **91,132**;
- represented draw triangles after 50% simplification: **45,566**;
- median max normalized error: **0.319%**;
- p90 max normalized error: **0.722%**;
- worst max normalized error: **0.820%**.

The worst normalized errors are dominated by small rounded detail, not large macroforms:
- pulse-algae root collars;
- Puerto valve status nodes;
- gardener contact pads;
- pulse-algae bulbs;
- SOMA regulator pressure bulbs.

Their absolute errors are still millimetric-to-centimetric, but their small object size makes the normalized error larger.

## Outlier refinement

Five small rounded outlier classes were tested at ratios 0.9, 0.8, 0.7, 0.6 and 0.5.

At **0.8 ratio**, their max normalized error is approximately **0.151–0.269%**. At **0.7**, it rises to approximately **0.277–0.481%**. At **0.5**, it reaches approximately **0.621–0.820%**.

Therefore a single global ratio would be technically weak. A future screen-space LOD pass should start from different probe envelopes:

### Bucket A — macro / large smooth structural forms
Examples: world ribs, scar rings, large arena rings, large membranes, large vehicle/creature proxies.

Measured evidence supports testing approximately 50% triangles as an **evaluation candidate** before art/screen-space approval.

### Bucket B — small rounded hero/detail forms
Examples: root collars, indicator/status nodes, contact pads, small bulbs.

Measured evidence supports a more conservative starting probe around 80% triangles. This is **not** an approved LOD ratio.

### Bucket C — final animated anatomy / authored silhouette-critical forms
Do not auto-decimate merely because a geometric metric passes. Final SOMA, final creatures, hands/faces/articulated contact anatomy and other silhouette-critical assets require topology/rig-aware LOD authoring.

## What remains before real LOD production

1. Qualify production engine/import path.
2. Confirm whether shared mesh instancing survives import as intended.
3. Define representative camera distances/FOV/resolution and screen-space error measurement.
4. Add direct silhouette/material/normal-map art review.
5. Qualify target hardware/preset and actual performance bottleneck.
6. Author LODs by error/importance class rather than one global triangle ratio.
7. Re-run export/import and runtime regression gates.

Until those conditions exist, `LOD_FEASIBILITY` is PASS as evidence, while final LOD completion remains BLOCKED/NOT RUN.
