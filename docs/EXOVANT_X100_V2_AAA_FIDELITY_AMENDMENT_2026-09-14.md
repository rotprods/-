# EXOVANT-X100 V2 — AAA Fidelity Amendment

Date: 2026-09-14  
Status after merge: binding amendment to `docs/EXOVANT_X100_V2.md`.

## Why this amendment exists

The existing X100 system correctly established look-lock, image-to-3D as a base candidate, cleanup/retopo, causal materials, LOD/collision and visual regression. Production evidence across active world branches nevertheless shows a recurring risk: technically excellent blockouts/proxies can accumulate enormous engineering effort while still lacking the source information required for final AAA visual fidelity.

This amendment makes the missing gate explicit and machine-testable.

## Superseding Tier S/A path

Where the older shorthand says:

`LOOK_LOCK → IMAGE_TARGET → IMAGE_TO_3D_BASE → CLEANUP/RETOPO → MATERIAL → LOD/COLLISION → ENGINE → VISUAL_REGRESSION`

read it as:

`LOOK_LOCK → SAME_SUBJECT_MULTIVIEW → SOURCE_ASSET_BAKEOFF → SOURCE_MASTER → HERO_FIDELITY_GATE → MATERIAL/LOOKDEV → RUNTIME_DERIVATION → ENGINE/RENDER QUALIFICATION → VISUAL_REGRESSION → HUMAN_GATE_ART`

The original sequence remains useful history; this amendment governs promotion after adoption.

## Asset Factory bakeoff

For identity-critical assets, compare candidate routes rather than defaulting to the current Blender proxy:

- manual Blender model/sculpt;
- procedural/Geometry Nodes;
- CAD source;
- photogrammetry/scan;
- multiview reconstruction;
- hybrid reconstruction + manual correction.

Connected-model examples observed 2026-09-14 include Tripo H3.1 multiview, Meshy multi-image and Hunyuan3D v3. These are not hard-coded production dependencies. Re-query live availability, capability and cost before use.

## Retroactive EXOVANT world rule

Every currently active art/world owner performs this at next normal resync:

1. inventory current Blender/GLB families;
2. label each `BLOCKOUT`, `PROXY`, `SUPPORT_CANDIDATE`, `HERO_CANDIDATE`, `HERO_QUALIFIED`, `RUNTIME_QUALIFIED` or `CINEMATIC_QUALIFIED`;
3. preserve validated layout, gameplay topology, collision, streaming and procedural work;
4. identify hero-visible assets whose source fails close-up fidelity;
5. mark prior cosmetic effort on those weak sources as `PROXY_POLISH_DEBT` rather than continuing it;
6. route only highest-value identity gaps through Asset Factory first;
7. derive runtime masters from approved source masters;
8. rerun gates invalidated by geometry/identity changes.

This is a salvage protocol, not a reset.

## Portfolio priority consequence

X100 value scoring should penalize `proxy_polish_without_source_fidelity` heavily. A new material/microdetail pass on a non-qualifying hero proxy has lower expected value than replacing/reconstructing its source geometry.

Conversely, systemic geometry may remain intentionally simple when it passes its actual screen-space/gameplay role. Not every object needs hero density.

## Gauntlet command

Each hero promotion receipt should be checked with:

```bash
python3 tools/aaa_asset_gate.py path/to/asset-fidelity.json
```

This validator checks evidence contracts; it does not infer beauty from triangle count.

## Immutable laws

- `BLOCKOUT != HERO_ASSET`.
- `MORE_POLYGONS != MORE_REALISM`.
- `SOURCE_MASTER != SHIPPING_RUNTIME_ASSET`.
- `RAW_RECONSTRUCTION != FINAL_ASSET`.
- `TECHNICAL_PASS != HUMAN_GATE_ART`.
- `RENDER_RESOLUTION != RENDER_TIME_ESTIMATE`.
