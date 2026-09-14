# LEVIATHAN — UV / PBR / LOD Production Contract

Claim: `CLM-W10-WORLD-LEVIATHAN-001`  
Owner: `AGENT-LEVIATHAN-10`  
Measured art-surface basis: representative scene established at revision 8; structural optimizer v2 validated through primary revision 10 / cold revision 8.  
Status: **READINESS CONTRACT / NOT FINAL UV-PBR-LOD**.

## 1. Truth boundary

This contract separates facts that must not be conflated:

1. **UV layer present** does not mean production unwrap approved.
2. **Principled material present** does not mean calibrated/textured PBR complete.
3. **Geometry measured** does not mean a hard performance budget exists.
4. **Repeated geometry instanced** does not mean an engine/runtime performance PASS exists.
5. **A feasible simplification ratio** does not become a final LOD threshold without camera/engine/hardware qualification.

Hard texture sizes, texel-density targets, LOD screen thresholds and GPU budgets remain blocked until production engine, target hardware, camera distances and streaming policy are qualified.

## 2. Measured UV state — art surface established at revision 8

All 260 mesh objects have at least one UV layer.

QA across mesh triangles found:
- zero zero-area UV triangles;
- zero UV loops outside the 0–1 range;
- UVs are structurally usable as blockout coordinates;
- relative density is not normalized and varies substantially by scale/family.

Relative UV-units-per-metre medians (not texels/metre):
- Puerto hero: `0.147932` (p10 `0.073244`, p90 `0.763282`);
- Jardines hero: `0.404062` (p10 `0.148804`, p90 `1.051500`);
- SOMA hero: `0.152930` (p10 `0.078742`, p90 `0.495711`);
- macro/other: `0.016025` median.

These are measurements, not target density values. An explicit unwrap/density decision remains required before baked texture production.

Receipt: `evidence/uv_pbr_lod_audit_r8.json`.

## 3. Curve state

The representative scene contains 92 curve objects. Current curve tessellation settings are uniformly:
- `resolution_u = 4`;
- `bevel_resolution = 3`.

Curves remain editable source for tendons, vascular lines, service lines, cilia and conduits. They are not automatically final baked/LOD assets. Create deterministic evaluated meshes only when texture baking or runtime-specific LOD requires them.

## 4. Material truth

18 portable material roles exist, all currently based on Principled BSDF constants.

**Image textures present: 0.**

Therefore current materials are look-development roles only. No final Base Color, Roughness, Normal, Metallic, AO, Emissive or Height texture set is claimed.

Role families include:
- living host: warm/dark tissue, vascular, membrane, cartilage, mucosa, necrotic, fibrous tendon, pressure lumen, pulse algae;
- human graft: ivory ceramic, dark technical, brushed metal, elastomer seal;
- signals: amber refuge, cyan diagnostic/memory, vermilion hazard;
- debug collision.

## 5. Engine-neutral texture intent

Until the renderer is fixed, retain a portable metallic/roughness interpretation and explicit channel metadata:
- Base Color — sRGB;
- Tangent-space Normal — linear;
- Roughness — linear;
- Metallic — linear where applicable;
- AO — linear when justified;
- Emissive — renderer-appropriate sRGB/linear conversion;
- Height/displacement — optional source data, not assumed to survive portable GLB as displacement.

Packing policy and final resolutions are **BLOCKED**, not invented here.

## 6. Family-specific art/material requirements

### Puerto de la Herida
- repaired ceramic/polymer must avoid plastic-toy read;
- brushed structural metal needs directional roughness, not chrome;
- elastomer seals need visible compression/contact logic;
- sutures/valves wear should follow maintenance and load paths;
- repeated modules may intentionally share UV/layout/texture sets after approval.

### Jardines Inmunes
- mucosa wetness must be scale-aware, not generic gloss;
- cartilage should read layered/fibrous hard-organic;
- necrotic material should express tissue state through calibrated color/roughness, not generic black damage;
- pulse algae state must remain readable without relying only on hue;
- gardener final texture topology depends on final anatomy/rig, which is not yet approved.

### Cámara de SOMA
- membrane/tendon/pressure-lumen roles must preserve combat telegraphs;
- amber refuge and vermilion hazard must remain distinguishable under lighting changes;
- final SOMA material set remains blocked with final SOMA anatomy.

## 7. Repeated geometry / instancing — validated through revision 10

The initial revision-8 audit showed large repeated-geometry opportunity. Two optimization stages were used to validate and then canonicalize sharing safely.

### v1 diagnostic stage
- primary r8 → r9: 260 → 122 mesh datablocks;
- no mesh objects removed;
- working-master visual/object fingerprint unchanged;
- cold replay exposed different internal primitive index ordering, which made v1 unnecessarily conservative.

### Reproducibility correction
A complete order-invariant evaluated-surface comparison proved primary and cold have identical render-semantic geometry/UV/material output. The apparent raw drift was only internal Blender vertex/face numbering.

Canonical primary/cold evaluated-surface fingerprint:
`6c06329ff60fe34383394bece0c80f66bb9e4486793712854e462c3af8eea26a`.

Receipt: `evidence/canonical_surface_repro_r9.json`.

### v2 production structural optimization
`tools/optimize_repeated_mesh_instances_v2.py` canonicalizes local topology/surface, all UV layers, materials, smoothing, sharp-face and edge state independently of index order. It refuses sharing when shape keys, vertex groups, mesh animation, color attributes or unknown public mesh attributes are present.

Primary revision 10 and cold revision 8 both converge to:
- mesh objects: `260`;
- mesh datablocks: **`98`**;
- canonical visual-surface fingerprint: `1b9d885f7fd612a30c4fd289bbc79da6b06472b710867e8f63bafa9c87827a5d`.

Aggregate primary r8 → r10:
- datablocks `260 -> 98` (**62.3077% reduction**);
- `.blend` `7,657,188 -> 4,842,680 B` (**36.7564% reduction**);
- GLB `8,492,516 -> 5,617,124 B` (**33.858% reduction**).

No visual-surface change is detected. This remains a source/export structural optimization, **not a runtime FPS/GPU PASS**.

Receipt: `evidence/instancing_optimization_r10_v2.json`.

## 8. LOD truth and policy

Current committed scene has:
- named LOD objects: `0`;
- Decimate modifiers: `0`;
- hard LOD budgets: **UNSET**.

Do not create generic 50%/25% LODs merely to fill a matrix. Before final LOD authoring, qualify:
1. target engine/import behavior;
2. target hardware/preset;
3. camera/FOV and representative encounter distances;
4. streaming/culling policy;
5. whether shared mesh instances remain shared after import.

An engine-neutral feasibility study may measure simplification ratio versus geometric error on temporary duplicates. Such measurements are evidence for later decisions, not final thresholds.

Final LODs should be derived from measured silhouette/surface error and production viewing conditions, not arbitrary percentages.

## 9. UV/PBR/LOD Definition of Done

This contract reaches DONE only when applicable assets have receipts for:
- approved unwrap/seams and intentional overlap policy;
- normalized or explicitly exempted texel density;
- no accidental UV degeneracy/overlap;
- calibrated PBR textures/material parameters under approved lighting;
- portable export validation;
- engine import and visual comparison;
- LOD chain with measured screen-space/silhouette error;
- target-hardware performance evidence;
- direct art review.

Until those gates exist, `W10/MAT/008` and LOD/performance gates remain REVIEW/BLOCKED as appropriate.
