# AURORA VEIL — REMOTE BLENDER RECEIPT

## Identity

- Project: `EXOVANT 2950 — AURORA VEIL World Master — CLM-AURORA-WORLD-001`
- 3D Jutsu project ID: `d6488148-8547-4ffe-b63d-e5fbec3a339c`
- Project URL: https://higgsfield.ai/3d-jutsu/d6488148-8547-4ffe-b63d-e5fbec3a339c
- Final inspected revision for this checkpoint: `5`
- Blender worker: `5.2`
- Claim: `CLM-AURORA-WORLD-001`
- Owner: `AGENT-02-AURORA`

## Final committed remote artifacts

At revision 5:

- editable `.blend`: 4,779,773 bytes; etag `828f4cbd201f87fcb232cfed66471131`;
- portable `.glb`: 3,086,552 bytes; etag `d9f25ec99d93aa9b693f933eeafe9119`.

The remote `.blend` is the editable scene receipt. This Git branch stores world specification, manifests, QA and reconstruction logic; it does not pretend a chat-local binary path is persistent.

## Scene checkpoint

Final-state audit observed:

- `scene_status = WAVE1_MACRO_BLOCKOUT_R4_LIGHTING_QA`;
- `claim_id = CLM-AURORA-WORLD-001`;
- `agent_id = AGENT-02-AURORA`;
- `world_id = aurora`;
- 329 objects;
- 11 materials;
- local macro terrain 5,200 × 3,000 × 14.036 m;
- observatory ring 48 × 48 × 2.466 m;
- observatory mast 72 m tall;
- AEON arena 50 × 50 × 1 m;
- Peregrino body 5.8 × 2.7 × 2.4 m;
- 12 local temporal anchors;
- 3 AEON echo-sector pylons;
- 10 machine-orchard tree blockouts;
- 27 planning streaming cells;
- 4 separate collision proxies.

## Render evidence

Final evidence set was generated after camera clipping correction:

| Artifact | ID | Resolution |
|---|---|---|
| `aurora_r4_overview.png` | `aab200eb7f217f218838fe39e05397be` | 640×360 |
| `aurora_r4_camp.png` | `32ccaeb22a99ae13f548d78c99cc54a0` | 640×360 |
| `aurora_r4_aeon.png` | `b2f96497e475c07ed70547e702a2896d` | 640×360 |

These are evidence artifacts, not a human GATE-ART approval.

## Important run history

The first monolithic build (`aurora-world-master-r1`) exceeded the Blender worker 300 s limit and committed nothing. The production strategy was changed to staged mutations:

1. `aurora-wave1-foundation-r1` → rev 1;
2. `aurora-wave1-orchard-proxies-r2` → rev 2;
3. `aurora-r3-scale-corrections` → rev 3;
4. `aurora-r4-camera-clip-fix` → rev 4;
5. revision 5 is the final observed lighting/QA-balanced remote checkpoint and preserves claim/dimensions/gates.

This is a pipeline learning: large world builds must be split into semantic checkpoints rather than coupling model creation and multiple renders into one worker operation.

## What this scene is

A **semantic production blockout** that proves:

- the three canonical Aurora regions can coexist in a metre-scale local frame;
- bounded temporal fields can be expressed without duplicating the whole world;
- the canonical 50 m AEON arena and three-sector contract can be physically represented;
- world-specific architecture/ecology/population/vehicle silhouettes have stable families;
- collision and streaming metadata can stay separate from render geometry;
- GLB export is currently portable enough for the repository's exchange workflow.

## What this scene is not

It is NOT:

- finished AAA/AAAA artwork;
- final topology;
- UV/bake/PBR completion;
- final characters/creatures;
- production engine integration;
- performance qualification;
- human art-direction approval;
- proof that the proposed 5,900 km planetary radius is canon.
