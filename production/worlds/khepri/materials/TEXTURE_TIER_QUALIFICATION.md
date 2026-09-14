# KHEPRI Material Texture-Tier Qualification

Status: **NOT_READY_FOR_FINAL_RESOLUTION**  
Block: `BLOCK-KHP-MAT-001 / TARGET_HARDWARE_TEXTURE_BUDGET`  
Scope: `CLM-KHEPRI-MATERIALS-001`

## Evidence boundary

Repository authority currently proves:

- Godot `4.7.2` is the qualified native integration reference.
- The current execution VM is ~8 CPU / 20 GiB RAM with Mesa llvmpipe and no exposed `/dev/dri` or NVIDIA device.
- `docs/HARDWARE.md` explicitly requires a representative scene on a real GPU host before approving production visual/performance claims.
- Unreal production profiling remains a separate future qualification; therefore material source art must remain engine-neutral while runtime receipts may use Godot as the currently verified adapter.

Godot's 4.x image-import documentation states that 3D-detected textures normally enable mipmaps and VRAM compression, and that VRAM-compressed textures materially reduce memory/bandwidth. High-quality desktop/mobile compression paths depend on renderer/platform, so they must be measured on the actual target rather than inferred from this VM.

Primary documentation:
- https://docs.godotengine.org/en/4.x/tutorials/assets_pipeline/importing_images.html
- https://docs.godotengine.org/en/latest/tutorials/performance/gpu_optimization.html

## Why the final tier is blocked

A texture resolution is not a quality tier by itself. Final selection depends on:

1. intended player/camera distance;
2. UV/tiling strategy and real metres covered;
3. number of simultaneously resident material applications;
4. renderer and platform compression format;
5. target resolution/upscaling path;
6. available texture-memory budget and streaming behavior;
7. load-time/stutter behavior;
8. visual error after mip/compression at gameplay distance.

None of these may be silently replaced with “use 4K everywhere”.

## Candidate authoring tiers — PROPOSAL ONLY

The application matrix currently carries source-density proposals:

- `hero_insert`: 1024 px/m;
- `prop_machine`: 512 px/m;
- `architectural`: 256 px/m.

These are comparative authoring targets used to keep scale coherent. They do not prescribe square texture dimensions because a 0.5 m hero insert and a 12 m wall do not cover the same metres.

Candidate square test resolutions for qualification:
`512, 1024, 2048, 4096`.

Do not promote any candidate to production until the experiment below passes.

## Planning estimator

Run:

```bash
python3 art_source/khepri/materials/estimate_texture_residency.py --matrix
```

The estimator uses:

`RGBA8_base_bytes × full_mip_chain(≈4/3) ÷ effective_compression_ratio × resident_maps`

It intentionally accepts the effective compression ratio as an input. This is planning math, not measured GPU residency.

### Planning example — 3 connected maps × 24 resident material states

Approximate totals, not runtime evidence:

| Square tier | 4:1 effective compression | 6:1 effective compression |
|---|---:|---:|
| 512 | ~24 MiB | ~16 MiB |
| 1024 | ~96 MiB | ~64 MiB |
| 2048 | ~384 MiB | ~256 MiB |
| 4096 | ~1536 MiB | ~1024 MiB |

This deliberately demonstrates why “4K on every state” is not an acceptable default. Real residency will differ by channel format, alpha, platform compression, reuse, streaming and which states are concurrently resident.

## Qualification experiment

### A. Target-host evidence
Record:

- host/platform;
- GPU / unified-memory architecture;
- usable graphics memory or unified-memory policy;
- OS and driver;
- engine build + renderer (`Forward+`, `Mobile`, `Compatibility`, or future adapter);
- target output resolution;
- upscaling/dynamic-resolution settings;
- representative scene and commit/hash.

If these are missing: `NOT_READY`.

### B. Source variants
For the same material application generate controlled source tiers:

- 512;
- 1024;
- 2048;
- 4096 only when lower tiers visibly fail.

The underlying material causality/state must remain identical. Resolution cannot add new art-direction information.

### C. Import matrix
For every tier record:

- source bytes;
- imported texture bytes;
- mipmap state;
- actual engine compression/import mode;
- channel format;
- material count;
- resident texture count;
- load time;
- first-use stutter;
- measured graphics memory/residency if exposed by the platform.

Current Godot adapter should test its platform-supported VRAM-compression path; never label a BPTC/ASTC/S3TC/ETC2 result without readback from that target configuration.

### D. Visual matrix
Capture deterministic views at minimum:

- orthographic calibration;
- curved/grazing-light response;
- intended gameplay distance;
- close inspection distance;
- mip transition distance;
- in-context KHEPRI lighting.

Compare:

- silhouette-independent material identity;
- micro-normal retention;
- roughness breakup;
- optical/mirror response;
- repair/state readability;
- compression artifacts;
- shimmering/aliasing;
- mip instability.

### E. Performance matrix
On the target host record at least:

- frame CPU/GPU p50/p95/p99 for the representative route;
- graphics memory before/after material set residency;
- load time and first traversal stutter;
- texture upload/streaming spikes where tooling exposes them.

Do not infer target performance from llvmpipe.

## Selection rule

For each material application choose the **lowest-cost tier that preserves the approved perceptual result at its declared player distance** while fitting the scene's measured texture-memory/streaming envelope.

A higher tier is justified only by evidence such as:

- visible mip/normal/roughness failure at intended distance;
- hero inspection requirement;
- authored unique information that cannot be represented through tiling/trim/decal reuse.

A lower tier wins when the higher tier produces no visible gameplay benefit.

## DoD — KHP/MAT/013

`TARGET_HARDWARE_BOUND_TEXTURE_BUDGET_AND_RESOLUTION_TIERS` requires:

- [ ] target host identified and probed;
- [ ] renderer/platform recorded;
- [ ] representative KHEPRI consumer scene available;
- [ ] 512/1K/2K matrix measured; 4K only if justified;
- [ ] import/compression settings read back;
- [ ] mipmaps verified;
- [ ] visual comparison captured;
- [ ] memory/load/stutter measured;
- [ ] selected tier per application scale recorded;
- [ ] waivers for hero exceptions;
- [ ] receipt hash-bound to engine/build/scene/artifacts.

Until every applicable item passes, `KHP/MAT/013` remains `BLOCKED_TARGET_HARDWARE` and `KHP/MAT/015` final-resolution authoring remains NOT_READY.
