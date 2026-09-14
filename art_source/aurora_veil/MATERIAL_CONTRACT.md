# AURORA VEIL — MANUFACTURED MATERIAL CONTRACT r15

**Task:** `AUR/MAT/020`  
**Owner:** `AGENT-02-AURORA` / `CLM-AURORA-WORLD-001`  
**Remote proof:** Blender rev 15  
**Status:** `REVIEW_MANUFACTURED`; textures, authored normal/roughness detail and human GATE-ART remain open.

## Scope boundary

This contract calibrates **manufactured Campamento materials only**. It does not define planetary lithology or biome substrate. `AUR_MAT_MINERAL_FOUNDATION` represents manufactured foundation/grout and MUST NOT be reused as a claim about Aurora's natural rock.

All base colors are authored from sRGB targets converted to scene-linear values before entering Principled BSDF. No random procedural roughness/noise is used as a realism shortcut.

## Families

| Material | sRGB target | Metallic | Roughness nominal / range | IOR | Other |
|---|---:|---:|---:|---:|---|
| `AUR_MAT_STRUCTURAL_GALV_STEEL` | 118/128/132 | 1.00 | 0.34 / 0.28–0.60 | 1.5 | structural frames/ring boxes |
| `AUR_MAT_CERAMIC_COMPOSITE_PANEL` | 150/154/152 | 0.02 | 0.56 / 0.48–0.74 | 1.50 | coat 0.08, coat rough 0.32 |
| `AUR_MAT_EPDM_GASKET` | 20/23/25 | 0 | 0.90 / 0.82–0.96 | 1.52 | weather/pressure seals |
| `AUR_MAT_DARK_TEMPERED_GLASS` | 24/42/48 | 0 | 0.12 / 0.05–0.28 | 1.52 | transmission 0.62, coat 0.03 |
| `AUR_MAT_CLOCK_BRONZE_CAL` | 112/64/24 | 1.00 | 0.40 / 0.28–0.68 | 1.5 | clock/instrument hardware |
| `AUR_MAT_MINERAL_FOUNDATION` | 92/88/82 | 0 | 0.84 / 0.72–0.95 | 1.50 | manufactured pad/grout only |
| `AUR_MAT_SERVICE_TRAY` | 96/101/104 | 0.90 | 0.47 / 0.38–0.66 | 1.5 | folded zinc-coated service metal |

## Manufacturing + wear causality

### Galvanized structural steel
- fabricated/rolled steel, welded assemblies, field-bolted splice plates;
- tool/contact abrasion belongs near ladders, bolts, service edges and repeated handling;
- zinc oxidation/chalking raises roughness gradually;
- ferrous rust is allowed only where zinc/coating is actually breached;
- forbidden: orange rust blanket, uniform edge wear, random scratches.

### Ceramic composite cassette
- ceramic/mineral face bonded to insulated cassette on secondary rails;
- impact chips are localized to service edges/collision points;
- dust collects below seams and on lower horizontal traps;
- water streaks require a joint/drainage path;
- forbidden: plastic sheen, identical edge damage, arbitrary grime.

### EPDM gasket
- extruded seal under compression;
- exposed lips can chalk under UV; compressed faces can polish;
- dust accumulates on tacky/contact edges;
- forbidden: metallic response, bright rubber, random crack maps without age/UV cause.

### Dark tempered glass
- laminated/tempered observation/instrument glazing in replaceable frames;
- dust/condensation films and service handling are permitted;
- chips require impact evidence;
- forbidden: opaque black plastic, globally high roughness, uniform scratches.

### Bronze instrument hardware
- machined/cast copper alloy;
- handling polish localized to controls and service surfaces;
- oxidation/patina depends on moisture/exposure, not a global green mask;
- bearing grease belongs at mechanisms only.

### Manufactured mineral foundation
- precast/grouted foundation material;
- ground splash, dust and plausible water streaking;
- edge spall needs impact/freeze/service cause;
- explicitly NOT the natural terrain/lithology material.

### Service tray
- perforated/folded zinc-coated sheet metal;
- abrasion belongs at removable covers, brackets and fasteners;
- horizontal internal surfaces may trap dust;
- forbidden: uniform corrosion and scratches on inaccessible faces.

## Texture / channel contract

Current state: `PENDING_AUTHORED_PBR`.

Future production may add only channels consumed by the selected runtime. Candidate channels: base color, normal, roughness, metallic, AO where justified, emissive where justified, opacity/transmission where supported, masks for causal wear.

No final texel density, UDIM, trim/decal or texture resolution is canonized until engine/memory/camera budgets are qualified.

## QA evidence

Neutral temporary lookdev:
- `aurora_r15_material_lookdev.png` / artifact `042b49d7e35dbf07d46c2da32ee779d6`;
- 480×270; mean 0.2503; white clip 0.

Camp context regression:
- `aurora_r15_camp_material_context.png` / artifact `679c139409f72031592e96d90431add0`;
- mean 0.1741 vs r8 0.1714; delta +0.0027;
- p01 0.0410; p50 0.1912; p99 0.5003;
- black clip 0.0004; white clip 0.

These are technical exposure/lookdev receipts, not human art approval.
