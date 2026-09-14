# AURORA VEIL — REMOTE BLENDER RECEIPT

## Identity

- Project: `EXOVANT 2950 — AURORA VEIL World Master — CLM-AURORA-WORLD-001`
- 3D Jutsu project ID: `d6488148-8547-4ffe-b63d-e5fbec3a339c`
- Project URL: https://higgsfield.ai/3d-jutsu/d6488148-8547-4ffe-b63d-e5fbec3a339c
- Final inspected revision for this checkpoint: `7`
- Blender worker: `5.2`
- Claim: `CLM-AURORA-WORLD-001`
- Owner: `AGENT-02-AURORA`

## Final committed remote artifacts

At revision 7:

- editable `.blend`: 5,859,342 bytes; etag `7418b326a1a0745688903f0b3fc42b3e`;
- portable `.glb`: 4,503,316 bytes; etag `210ef84a071fb40a3b62c81d73b7b656`.

The remote `.blend` is the editable scene receipt. This Git branch stores world specification, manifests, QA and reconstruction logic; it does not pretend a chat-local binary path is persistent.

## Surface scene checkpoint

The revision-5 surface checkpoint remains valid after the orbital insertion. A revision-7 surface-regression render reproduced the validated overview mean luminance exactly (`0.1793`, delta `0.0000`), with zero black/white clipping.

Surface facts preserved:

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

## L1 orbital checkpoint — revision 7

`AUR/WORLD/003` now has a separate display representation inside collection `14_ORBITAL_PROXY`:

- `AUR_PLN_001_ORBITAL_SHELL` / asset family `AUR-PLN-001`;
- `AUR_ATM_001_ATMOSPHERE_SHELL` / asset family `AUR-ATM-001`;
- four independent aurora ribbon curves;
- two observation-station proxies matching the canon statement that two stations carry divergent clocks;
- dedicated `CAM_AURORA_ORBITAL_L1`;
- explicit metadata anchor linking physical proposal to display scale.

Scale contract:

- physical radius `5,900,000 m` = **PROPOSAL** from ADR-AUR-001, not canon;
- display radius `590 m`;
- display scale `1e-4`;
- shell measures 1,180 m diameter in Blender display space;
- global continental geography remains `UNKNOWN_NOT_AUTHORED` rather than being invented.

Technical audit:

- planet shell: 2,562 vertices / 5,120 polygons;
- atmosphere shell: 4,514 vertices / 4,608 polygons;
- atmosphere is a separate dithered alpha material layer;
- one scene-global stellar sun only: `SUN_VELAR_LOW`;
- no AREA lights in portable scene;
- a first r6 implementation briefly introduced a second SUN, detected as cross-scene contamination risk and removed in r7 before promotion.

Orbital render QA:

- `aurora_r7_orbital_l1.png` / artifact `46c6e0a6451b54fcef6cd1b5c3d2346e` / 480×270;
- mean luminance 0.1114;
- p01 0.0410, p50 0.1056, p99 0.2457;
- black clipping 0, white clipping 0;
- this is photometric/blockout evidence, **not** human GATE-ART approval.

Detailed receipt: `QA/orbital_r7.json`. Reproducible package: `blender/aurora_orbital_l1.py`.

## Surface render evidence — revision 5 baseline

| Artifact | ID | Resolution |
|---|---|---|
| `aurora_r5_overview.png` | `f84c1785da5a26f4948cfe6b98da76e5` | 640×360 |
| `aurora_r5_camp.png` | `25ceae28f42f7b80791faae4f003543e` | 640×360 |
| `aurora_r5_aeon.png` | `22027b240626f24169a90e85619f9e7b` | 640×360 |

These are evidence artifacts, not a human GATE-ART approval.

## Important run history

The first monolithic build (`aurora-world-master-r1`) exceeded the Blender worker 300 s limit and committed nothing. Production was split into staged mutations:

1. `aurora-wave1-foundation-r1` → rev 1;
2. `aurora-wave1-orchard-proxies-r2` → rev 2;
3. `aurora-r3-scale-corrections` → rev 3;
4. `aurora-r4-camera-clip-fix` → rev 4;
5. rev 5 → validated surface-lighting checkpoint;
6. `aurora-wave1-orbital-l1-r6` → rev 6, then cross-scene second-SUN issue detected;
7. `aurora-orbital-r7-single-star-fix` → rev 7; technical/render/surface-regression QA passed.

This preserves two production learnings: large world builds must be checkpointed by semantic wave, and lighting objects with scene-global influence must be regression-tested against already-qualified cameras.

## What this scene is

A **semantic production blockout + L1 orbital proxy** that proves:

- the three canonical Aurora regions coexist in a metre-scale local frame;
- bounded temporal fields can be expressed without duplicating the whole world;
- the canonical 50 m AEON arena and three-sector contract can be represented physically;
- world-specific architecture/ecology/population/vehicle silhouettes have stable families;
- collision and streaming metadata stay separate from render geometry;
- an orbital layer can coexist without changing the surface-camera baseline;
- GLB export remains portable after orbital additions.

## What this scene is not

It is NOT:

- finished AAA/AAAA artwork;
- final topology;
- UV/bake/PBR completion;
- final characters/creatures;
- production engine integration;
- performance qualification;
- human art-direction approval;
- proof that the proposed 5,900 km planetary radius is canon;
- a canonical global continent/biome map.
