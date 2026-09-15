# KHEPRI World Macro — recoverable handoff / R10 X100 checkpoint

AGENT: `AGENT-KHEPRI-WMACRO-001`  
CLAIM: `CLM-KHEPRI-WMACRO-001`  
BRANCH: `art/world-khepri-001`  
PR: `#8` draft  
CLAIM STATUS: **KEEP / REVIEW**  
MASTER 3D PROJECT: `040f0c45-83a7-483c-9ee7-1e31c640a587` rev **10**  
COLD PROJECT: `4c01fdbb-7093-4229-9a49-8237583280bc` UV rev **7**  
FAMILY: `KHP_WM_HELIOSTAT_FOOTPRINTS = SYSTEMIC_MACRO_COMPLETE`

## North Star
Maintain KHEPRI as a deterministic metre-scale world foundation with stable cross-domain interfaces. `/EXOVANT-X100` expands depth through systemic families, causal states and procedural recombination without random clutter, duplicated ownership or false AAAA claims.

## Current truth
The macro claim is technically mature but **not final art and not KHEPRI complete**. It owns macro terrain/interfaces and the systemic optical support family. Final close-range heliostat architecture, sky/atmosphere, PBR texture budgets, collision, characters, ecology, vehicles and hero landmarks remain separate domains.

## Foundation retained
- terrain: 6.4 × 4.8 km local tangent cell;
- terrain runtime mesh: 4,941 vertices / 9,600 tris;
- terrain custom-normal contract: `KHP_GLOBAL_GRADIENT_NORMAL_V1`;
- terrain route: 576 points, target clearance 7 m, zero below-terrain samples;
- optical field: 107 masts + 107 panels, 3 structural scale families;
- systemic configuration space: 432 valid layouts/state/density/corridor combinations;
- LOD source: LOD0/1/2, 12 source-only reduced meshes;
- Godot import/resource sharing previously qualified.

## R9 — material UV0 interface
Geometry owner explicitly closed the material UV blocker.

Contract: `KHP_OPTICAL_UV0_HANDOFF_V1`

- 18 optical meshes covered: LOD0 + LOD1 + LOD2, mast/panel × compact/standard/wide;
- UV layer: `UVMap`;
- deterministic dominant-axis object-space mapping;
- 4 metres per texture repeat;
- overlap intentionally allowed for tileable materials;
- unique hero/story masks require a separate future UV interface;
- geometry semantic SHA unchanged before/after:
  `41cb03864b03a907c8691de33843f874f1796ba67b0dc02980ad5af9fc60cf86`;
- UV SHA master/cold exact match:
  `13532b5bb722e7293e5248e061d6e30192a8cf21c21c355abd89095ea26a9c8e`.

Source: `art_source/khepri/world_macro/add_optical_uv0_handoff.py`  
Contract doc: `production/worlds/khepri/world_macro/MATERIAL_UV_HANDOFF.md`

## R10 — first real KHEPRI material consumer
The macro world now consumes the real KHEPRI material system at calibration resolution.

Contract: `KHP_HELIOSTAT_MATERIAL_PILOT_V1`

Bindings on visible LOD0 family meshes:

- mast + structural panel parts → `KHP_MAT_BRONZE_SYNOD_001::service_clean::cast_structural::architectural`;
- optical face → `KHP_MAT_MIRROR_OPTICAL_001::calibrated::broad_reflector::architectural`.

The exact texture bytes were regenerated with the material-library R4 deterministic compiler and hash-checked against R4 before any slot mutation.

Nine material slots were changed. Geometry + UV semantic SHA remained identical before/after binding:
`32274b915360ebcc3a9c1f9fb0f9ee79e2847986b48e6566d81c176b17e35824`.

LOD1/LOD2 have UV0 but remain source-only and retain their previous material slots until runtime LOD switching is qualified.

## Exact R10 artifacts

GLB:
- 590,844 B;
- SHA256 `240154331d5514cbcc9d4d454ed944032f5f24458c522348b9105caa52fc01c4`;
- persistent media `f6f51455-0742-4233-97c2-9306fe7b7127`.

BLEND:
- 2,350,870 B;
- SHA256 `95622989e554ffd843c67a06efa502934dda91ce8602045a2405ffcf7314baba`;
- persistent media `40d8e353-e509-43bd-9a36-2132cd427ac8`.

`fleet_control.py delivery` passes for these exact hashes with native receipt SHA:
`34df327c3b3df504f959cc175782a78af6600086f4af797ce8919694c07baf1d`.

## Godot R10
Godot `4.7.2.stable.official.ed1daf0bf` exact GLB import PASS:

- 229 runtime nodes;
- 219 MeshInstance3D;
- 107 masts / 107 panels;
- 3 unique mast Mesh resources / 3 unique panel Mesh resources;
- Bronze + Mirror keep BaseColor/Metallic/Roughness/Normal textures;
- 0 pilot material failures;
- instancing remains preserved.

## Visual truth
Do not confuse technical material integration with final art.

AI QA on R10:
- overview: infrastructure/route remain legible, but material identity is too distant to judge;
- close-up in current world: **final-art readability FAIL**;
- no UV catastrophe, no visible seam/stretching failure, no specular clipping;
- machine diagnosis: Bronze ≈0.82 metallic / roughness 0.25–0.34; Mirror ≈0.94 metallic / roughness 0.075, all texture roles connected;
- current world has one Sun and a near-black, unqualified sky/reflection context;
- consumer geometry is Tier-D macro support, not close-range production architecture.

Therefore the correct blocker is downstream lookdev/consumer quality, **not broken material transport**. Do not brighten materials arbitrarily or bake fake reflections into BaseColor to make this proxy look finished.

Receipt: `production/worlds/khepri/world_macro/receipts/R10_MATERIAL_CONSUMER_PILOT.json`.

## Canon / ownership boundary
- canonical named regions: Ciudad de los Toldos, Mar de Cristal, Crisol de RAKHET;
- documented biota: Escarabajo heliostato, Zorro de vidrio, Serpiente de cable, Liquen de prisma;
- documented vehicle: Helioperegrino;
- final ecology, characters, vehicle geometry and regional architecture remain unclaimed by this macro cell;
- proposed radius remains proposal, not canon.

## Open blockers
1. `HUMAN_GATE_ART` — no AI/machine gate can close it.
2. Qualified KHEPRI sky/reflection/lookdev context for final reflective-material judgement.
3. Close-range heliostat geometry if the optical family is ever promoted above Tier-D macro support.

## Downstream / non-blocking
- final texture resolution and target-hardware memory budgets;
- runtime LOD thresholds/HLOD;
- production collision/navmesh;
- corporate Git LFS archival policy.

## Next actions
1. Keep R10 as the exact technical material-consumer proof.
2. Let `CLM-KHEPRI-MATERIALS-001` own material grammar/library work; macro only supplies geometry interfaces.
3. Create/claim a dedicated KHEPRI atmosphere/sky or close-range heliostat lookdev leaf before final material-art promotion.
4. Continue `/EXOVANT-X100` on the next unclaimed world domain rather than increasing detail randomly in this claim.

CLAIM STATUS: **KEEP / REVIEW**  
FAMILY STATUS: **SYSTEMIC_MACRO_COMPLETE**  
MATERIAL CONSUMER TECHNICAL STATUS: **PASS**  
FINAL ART STATUS: **BLOCKED / HUMAN + DOWNSTREAM LOOKDEV**
