# LEVIATHAN — UV / PBR / LOD Production Contract

Claim: `CLM-W10-WORLD-LEVIATHAN-001`  
Owner: `AGENT-LEVIATHAN-10`  
Measured scene basis: working master revision 8, before structural instancing optimization.  
Status: **READINESS CONTRACT / NOT FINAL UV-PBR-LOD**.

## 1. Truth boundary

This contract separates four facts that must not be conflated:

1. **UV layer present** does not mean production unwrap approved.
2. **Principled material present** does not mean calibrated/textured PBR complete.
3. **Geometry measured** does not mean a hard performance budget exists.
4. **Repeated geometry instanced** does not mean an engine/runtime performance PASS exists.

Hard texture sizes, texel-density targets, LOD screen thresholds and GPU budgets remain blocked until production engine, target hardware, camera distances and streaming policy are qualified.

## 2. Measured UV state — revision 8

All 260 mesh objects have at least one UV layer.

QA across mesh triangles found:
- zero zero-area UV triangles;
- zero UV loops outside the 0–1 range;
- UVs are therefore structurally usable as blockout UV coordinates;
- relative density is not normalized and varies substantially by scale/family.

Relative UV-units-per-metre medians (not texels/metre):
- Puerto hero: `0.147932` (p10 `0.073244`, p90 `0.763282`);
- Jardines hero: `0.404062` (p10 `0.148804`, p90 `1.051500`);
- SOMA hero: `0.152930` (p10 `0.078742`, p90 `0.495711`);
- macro/other: `0.016025` median, reflecting very large blockout surfaces.

These values prove that an explicit unwrap/density pass is required before baked texture work. They are **measurements**, not target density values.

## 3. Curve state

Revision 8 contains 92 curve objects. Current curve tessellation settings are uniformly:
- `resolution_u = 4`;
- `bevel_resolution = 3`.

Curves are useful editable source for tendons, vascular lines, service lines, cilia and conduits, but they do not constitute final baked UV assets. Keep editable curves in source. Create deterministic evaluated/bake meshes only when texture baking or runtime-specific LOD requires them.

## 4. Material truth

18 portable material roles exist, all currently based on Principled BSDF constants.

**Image textures present: 0.**

Therefore current materials are look-development roles only. No final base-color, roughness, normal, metallic, AO, emissive or height texture set is claimed.

Measured role families include:
- living host: warm/dark tissue, vascular, membrane, cartilage, mucosa, necrotic, fibrous tendon, pressure lumen, pulse algae;
- human graft: ivory ceramic, dark technical, brushed metal, elastomer seal;
- signals: amber refuge, cyan diagnostic/memory, vermilion hazard;
- debug collision.

## 5. Engine-neutral texture intent

Until the target renderer is fixed, texture production should retain a portable metallic/roughness interpretation and explicit channel metadata. Candidate portable maps:
- Base Color — sRGB;
- Tangent-space Normal — linear;
- Roughness — linear;
- Metallic — linear where applicable;
- AO — linear when justified;
- Emissive — sRGB/renderer-appropriate conversion;
- Height/displacement — optional source data, not assumed to survive portable GLB as displacement.

Packing policy and final resolutions are **BLOCKED**, not invented here.

## 6. Family-specific art/material requirements

### Puerto de la Herida
- ceramic graft panels: repaired, non-plastic ceramic/polymer read;
- brushed structural metal: controlled directional roughness, not chrome;
- elastomer seals: compression/contact read at tissue interface;
- sutures/valves: dirt/wear follows maintenance and load paths;
- repeated modules may intentionally share UV/layout/texture sets when production approval allows.

### Jardines Inmunes
- mucosa: wetness must be scale-aware and avoid toy/plastic gloss;
- cartilage: layered/fibrous hard-organic read;
- necrotic material: local desaturation/roughness/thermal logic, not generic black damage;
- pulse algae: state variation must remain readable without relying only on hue;
- gardener: final anatomy/rig determines whether unique UDIM-style source or shared modular maps are appropriate; no choice is made yet.

### Cámara de SOMA
- membrane/tendon/pressure-lumen roles must preserve encounter telegraph readability;
- amber refuge and vermilion hazard signals remain semantically distinct under lighting changes;
- final SOMA material set remains blocked with final SOMA anatomy.

## 7. Repeated geometry / instancing

Revision-8 audit found 36 strict safe repetition groups covering 174 objects, with 138 redundant mesh datablocks removable under exact geometry/topology/UV/material/attribute equality.

Working-master revision 9 applies this structural optimization:
- mesh objects remain `260`;
- mesh datablocks: `260 -> 122`;
- objects relinked: `138`;
- object-level render-equivalent fingerprint is unchanged exactly at the audited precision.

This is a source/export optimization, **not a runtime performance PASS**.

Independent cold reconstruction exposed legacy primitive-tessellation differences outside Puerto. The cold project therefore reaches a slightly different strict sharing count (`260 -> 127` datablocks) despite the same higher-level scene contract. Do not misreport this as bit-exact raw-mesh reproducibility; it is tracked as provider/operator primitive realization drift.

## 8. LOD truth and policy

Current scene has:
- named LOD objects: `0`;
- Decimate modifiers: `0`;
- hard LOD budgets: **UNSET**.

Do not author arbitrary LOD triangle percentages just to fill the matrix. Before final LOD work, qualify:
1. target engine/import behavior;
2. target hardware/preset;
3. camera/FOV and representative encounter distances;
4. streaming/culling policy;
5. whether shared repeated meshes remain instanced after import.

Then derive LODs from measured silhouette/error thresholds rather than generic ratios.

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
