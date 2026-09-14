# NACRE — AAA LOOKDEV → MULTIVIEW → POLYGON CONTRACT v1

Claim candidate: `CLM-NACRE-LOOKDEV-HERO-001`  
Owner: `AGENT-NACRE-LOOKDEV-01`  
X100 opportunity: `NACRE-AAA-LOOKDEV-TO-MESH`  
Status: `READY_FOR_FLEET_ADMISSION`; no provider generation/modeling until Fleet readback admits the claim.

## 1. North Star

Convert one identity-critical Nacre family from approved AAA visual truth into a physically plausible, editable, game-ready 3D hero family while proving a repeatable image→polygon pipeline that can later scale to other Nacre families.

Pilot family: **Archive Chamber Identity** (`NACRE-LOOK-ARCHIVE-CHAMBER-001`).

The result is not judged by “looks impressive in one render”. It must preserve identity across views, imply fabrication/growth causality, survive Blender cleanup, produce portable PBR/geometry, import into the target runtime and pass visual regression against the approved target pack.

## 2. Canon / documented constraints

DOCUMENTED:
- World: NACRE; Andromeda / Mneme / Casas de Nácar.
- Reference gravity: 0.26 g; reference temperature: 16 °C.
- Cities grow inside kilometre-scale shells.
- Inhabitants preserve whole lives in pearls and trade biographies.
- `Canteras de Concha`: libraries grow by mineral strata.
- `Archivo de MNEMOS`: spherical archive rooms connected by bridges.
- Canon biota includes Caracol de archivo, Polilla de nácar and Liquen palimpsesto; these establish mineral-layering / revealed-writing / preserved-trace motifs, not permission to paste literal creatures onto architecture.

UNKNOWN / must not be invented as canon:
- planetary radius/diameter;
- final global geography;
- final archive-chamber dimensions;
- final production engine/hardware budgets;
- final material texture resolution/texel density.

Existing macro proposal geometry in `CLM-NACRE-WORLD-MACRO-001` is a scale/interface reference only and is excluded from modification by this claim.

## 3. Visual DNA — proposed, reversible until GATE-ART

### Shape language
- Primary: mineral shell curvature + pressure-grown spherical vaults; no generic sci-fi boxes.
- Secondary: structural seams, laminar growth bands, docking collars, maintenance apertures and load-transfer interfaces.
- Tertiary: sparse biography/archive instrumentation where function is legible; never random greeble.
- Silhouette must remain recognizable with flat gray material.

### Material language
- Nacre is **layered mineral composite**, not uniform chrome/pearlescent plastic.
- Outer structural shell: matte/rough mineral, local fractures and compression history.
- Inner archive surfaces: bounded iridescence from thin layered mineral response; variation follows layer direction and curvature.
- Structural/docking parts: darker functional material with visible attachment logic and maintenance access.
- Translucency/emission only where the archive function justifies it; never blanket glow.

### History / wear
`ERA_0 grown/mineral construction → ERA_1 archive retrofit/maintenance → ERA_2 current polishing, repair, deposition and biological trace`.

Wear follows contact, moisture/deposition, repair access, stress and maintenance. No uniform edge wear, random scratches or grunge-everywhere.

## 4. LOOK_LOCK target pack

Stable pack ID: `NACRE-LOOK-TARGET-PACK-001`.

Required views of the **same pilot chamber module**:
1. `TARGET_A_3Q_FRONT` — hero 3/4 exterior/interior threshold read.
2. `TARGET_B_SIDE` — near-orthographic side; silhouette and wall-thickness read.
3. `TARGET_C_REAR` — docking/service side; functional access read.
4. `TARGET_D_TOP` — top/high orthographic; major opening and bridge socket placement.
5. `TARGET_E_MATERIAL_MACRO` — nacre/mineral layer close-up with scale witness.
6. `TARGET_F_DOCK_DETAIL` — bridge collar / load path / maintenance interface close-up.

All reconstruction views A–D must depict one geometry, one state, one scale and one material assignment. No camera trick may change apertures, socket count or major seam placement between views.

### Generation framing contract
- neutral or controlled studio/context lighting;
- enough shadow to read depth, not hide geometry;
- no fog obscuring silhouette;
- no text/logos;
- no depth-of-field on reconstruction views;
- no people touching/occluding the asset; a separate 1.8 m scale witness may stand clear of geometry;
- no cropped major interfaces;
- physically plausible wall thickness and access dimensions.

### Negative art contract
Reject targets showing: random greebles, generic Star-Wars-like panel soup, chrome pearl plastic, perfect manufactured symmetry without growth logic, blanket translucency, arbitrary emissives, floating structures, impossible unsupported spans, noisy decals, overgrown microdetail that destroys macro silhouette, scale ambiguity, nonfunctional doors or maintenance access.

## 5. Image → 3D reconstruction bake-off

The approved A–D views become immutable reconstruction inputs. Do not regenerate views separately after reconstruction begins.

### Candidate A — Tripo H3.1 Multiview
Model: `tripo_h3_1_multiview_to_3d`
- 2–4 ordered views;
- `geometry_quality=detailed`;
- `texture=true`, `pbr=true` only after geometry-only silhouette probe if cost warrants;
- quad candidate enabled for editability test;
- face budget is a reconstruction budget, **not** runtime budget.

### Candidate B — Meshy Multi-Image
Model: `multi_image_to_3d`
- same approved 2–4 views;
- remesh enabled;
- quad topology candidate;
- target polycount chosen for source cleanup, not final runtime;
- PBR/texturing only after geometry candidate survives structural review.

### Candidate C — Hunyuan3D v3
Model: `hunyuan3d_v3_image_to_3d`
- same approved views;
- geometry-first candidate;
- PBR only after silhouette/structure acceptance;
- high face count is allowed only as source capture and must later be reduced deliberately.

`SAM 3 3D Objects` remains a fast diagnostic single-image lift, not the preferred hero reconstruction route.

## 6. Candidate scoring

Score each raw reconstruction 0–100, but **raw score cannot mark final asset**:
- 30 silhouette / multiview shape agreement;
- 20 structural & manufacturing/growth causality;
- 15 correct openings, bridge sockets and maintenance interfaces;
- 10 topology/editability potential;
- 10 material-region alignment;
- 5 wall thickness / scale plausibility;
- 5 absence of hallucinated/floating geometry;
- 5 UV/texture/PBR transport potential.

Hard reject if major views contradict each other, primary silhouette is wrong, critical openings are hallucinated/closed, or topology contains unrecoverable fused/self-intersecting masses across functional interfaces.

## 7. Blender AAA conversion

Selected reconstruction is **BASE_CANDIDATE** only.

Required conversion:
1. import into isolated Blender project;
2. metric re-scale from documented witness/proposal dimensions;
3. delete reconstruction garbage / detached islands;
4. rebuild primary silhouette where target mismatch exists;
5. rebuild structural openings, collars and maintenance access parametrically where needed;
6. retopologize with controllable edge flow / deterministic triangulation at export;
7. create real thickness where close inspection exposes shell cross-section;
8. UV strategy by tier; hero source may use UDIM only if runtime budget justifies it;
9. PBR material families separated by physical role;
10. causal wear/deposition pass;
11. collision separated from visual mesh;
12. LOD/HLOD decision from screen-space/runtime evidence, not arbitrary percentages;
13. export GLB and target-engine import;
14. render same target cameras and run visual-regression comparison;
15. human GATE-ART.

## 8. Definition of Done — pilot family

Not DONE until:
- [ ] Fleet claim ACTIVE/read back;
- [ ] A–F target pack persisted with provenance;
- [ ] A–D multiview geometry agreement accepted;
- [ ] at least two reconstruction candidates compared on identical inputs;
- [ ] raw AI/reconstruction status explicitly removed after cleanup;
- [ ] silhouette and structural interfaces match target pack;
- [ ] scale/thickness/maintenance logic documented;
- [ ] clean source persisted;
- [ ] UV/PBR/collision/LOD strategy implemented as applicable;
- [ ] engine import receipt tied to exact export hash;
- [ ] visual regression against target cameras;
- [ ] human GATE-ART PASS;
- [ ] X100 evidence receipt updates only cells actually proven.

## 9. Expansion after pilot

Only after the pilot passes, expand the visual DNA into:
- `NACRE-LOOK-SHELL-SURFACE-001` — macro/meso shell-growth family;
- `NACRE-LOOK-BRIDGE-IDENTITY-001` — bridge/docking family;
- `NACRE-LOOK-MATERIAL-DNA-001` — reusable mineral/nacre/structure material families.

Then build controlled size/state/regional variants. Do not generate hundreds of one-off AI meshes.
