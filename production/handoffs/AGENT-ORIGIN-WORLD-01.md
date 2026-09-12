# EXOVANT 2950 — ORIGIN world-owner handoff

AGENT: `AGENT-ORIGIN-WORLD-01`  
SESSION: `SES-20260912-ORIGIN-WORLD-001`  
WORLD CLAIM: `CLM-ORIGIN-WORLD-001`  
ACTIVE ATOMIC CLAIM: `CLM-ORIGIN-MEGA-ATRIO-001`  
BRANCH: `art/world-origin-001`  
BASE MAIN: `196ef814fdc845ec797979906d01dc25009217c7`  
LINEAR: `ROT-115`  
GITHUB COORDINATION: issue `#14`  
REMOTE BLENDER PROJECT: `6e64cd59-f1f6-461f-850c-737d098f1723`  
REMOTE REVISION: `2`

## NORTH STAR

Own ORIGIN art/modeling at world level while keeping production sharded into recoverable atomic claims. Current cell delivers the Atrio de las Rutas structural grammar: canonical 70 m three-ring arena envelope, black-mineral load paths, living-bronze interfaces, radial bridges, route nodes, route aperture and explicit collision proxies.

## DONE

- Re-read updated `AGENTS.md` ownership preflight on main commit `196ef814...`.
- Read coordination registry issue #7; ORIGIN was explicitly `UNCLAIMED AT SNAPSHOT`.
- Fetched all current branches and verified no Origin branch existed.
- Reserved `art/world-origin-001` before geometry.
- Created Linear `ROT-115` before geometry and linked branch/registry.
- Re-fetched Origin branches immediately after reservation; only this branch was present.
- Created world-owner coordination issue #14 and updated registry #7.
- Persisted `CLM-ORIGIN-WORLD-001` and atomic `CLM-ORIGIN-MEGA-ATRIO-001` before Blender production.
- Built a new isolated Blender 5.2 LTS project for the Atrio; no existing world project was modified.
- Produced 3 ring families, 3 radial bridge families, support family, safe node, valve node and route aperture.
- Added black-mineral load bands and living-bronze joints based on functional load/connection roles rather than decorative greeble.
- Added bounded TERRA/NACRE/VANTA material-echo inserts without importing or taking ownership of prior-world geometry.
- Added current prototype player reference 1.85 m / radius 0.38 m.
- Produced explicit collision proxies and GLB export.
- Ran technical QA and then spatial QA; corrected all found defects before final gate.
- Persisted deterministic generator, manifest and QA receipt.

## CURRENT CHECKPOINT

Truth state: `LOCALLY_VALIDATED_BLOCKOUT` — not final art.

Remote revision 2 metrics:

- objects: `132`
- mesh objects: `126`
- materials: `13`
- explicit collision proxies: `19`
- visible approximate triangles: `11,436`
- Blender: `5.2.0 LTS`
- units: metric, `1 BU = 1 m`
- arena envelope: `70 m` canon
- ring radii: `35 / 24 / 13 m` proposal inside canon envelope
- ring width: `5.0 m` proposal
- bridge clear width: `4.5 m` proposal

Final scripted QA `origin-atrio-qa-release-005`: `PASS=true`.

## DEFECTS FOUND AND CORRECTED

### ORG-QA-F001 — camera clipped production geometry
Spatial query found outer-ring corners outside frame (`xmin=-0.187`, `ymin=-0.189`). Delivery camera was moved farther and set to 45 mm. Final production extents are `xmin=0.009`, `xmax=0.942`, `ymin=0.056`, `ymax=0.778`.

### ORG-QA-F002 — structural supports floated over datum
Primary and auxiliary support piers were 0.020–0.025 m above the preview datum. All 12 were lowered by 0.04 m. Final measured contact is a controlled overlap of 0.015–0.020 m.

### ORG-QA-F003 — node collision exceeded visible geometry
Safe/valve square proxy corners exceeded the 4 m visual disc by 1.233 m. Replaced with 12-sided cylindrical collision proxies of radius 3.72 m.

## FINAL QA RECEIPTS

PASS:

- required asset IDs
- collision coverage
- zero-area meshes = 0
- meshes without materials = 0
- non-unit scales = 0
- claim metadata mismatch = 0
- production corners inside delivery camera
- support contact
- node collision inside visible boundary
- GLB export

Artifacts revision 2:

- `.blend`: 2,369,786 bytes / etag `f17892c2acf59a2dc3fffda6379bf88a`
- `.glb`: 2,760,416 bytes / etag `85905d94d8409d2cfcba2a6ab67bed9b`
- PNG: `8c5f749466f2a4a23d0148758dd4dbf5` / 1200×800 / 782,102 bytes / etag `dc2823afe1bc61d5e778cf6d13009429`

## NOT PROVEN / BLOCKED

- Engine import and traversal with the real CharacterBody have not been run.
- Local/variable-gravity gameplay and camera behavior are not proven by Blender geometry.
- Final UVs, texture sets, causal micro-surface detail and PBR are not produced.
- LOD/HLOD and target GPU budgets remain unresolved pending production-engine/hardware qualification.
- Final EXOVANT boss/heart core is explicitly excluded from this claim.
- `GATE-ART` human creative-director approval remains pending.
- A preview PNG exists, but the current agent surface did not expose its pixels for direct agent visual inspection; no fabricated visual-art PASS is claimed.

## FILES

- `production/claims/CLM-ORIGIN-WORLD-001.yaml`
- `production/claims/CLM-ORIGIN-MEGA-ATRIO-001.yaml`
- `art_source/worlds/origin/atrio/PLAN.md`
- `art_source/worlds/origin/atrio/origin_atrio.py`
- `production/manifests/origin/megastructures/ORG_ATRIO_STRUCTURAL_KIT_001.yaml`
- `production/receipts/origin/CLM-ORIGIN-MEGA-ATRIO-001-QA.yaml`
- `production/handoffs/AGENT-ORIGIN-WORLD-01.md`

## DEPENDENCIES / INTERFACES FOR OTHER AGENTS

ORIGIN is world-owned by this branch, but other cells may claim explicit non-overlapping assets. Current locked IDs are:

- `ORG_ATR_RING_A70`
- `ORG_ATR_RING_B52`
- `ORG_ATR_RING_C34`
- `ORG_ATR_BRIDGE_RADIAL_A/B/C`
- `ORG_ATR_NODE_SAFE`
- `ORG_ATR_NODE_VALVE`
- `ORG_ATR_ROUTE_APERTURE`
- `ORG_ATR_SUPPORT_PIER`

Do not reuse these IDs in another branch.

Unclaimed candidate domains inside ORIGIN include final Archive of the First Wound architecture, final Heart negotiation center, EXOVANT boss body/rig, fauna, NPCs, Arca-specific integration and material-detail specialization. Each requires a new atomic claim.

## NEXT 3 ACTIONS

1. Import revision-2 GLB into an isolated engine scene and run real CharacterBody traversal/collision over all three rings, radial bridges and route aperture; feed measured defects back into the generator.
2. Create `CLM-ORIGIN-ARCH-ARCHIVE-001` or another explicitly non-overlapping atomic cell for the next ORIGIN production wave only after a fresh ownership resync.
3. After traversal validates dimensions, perform causal material/UV/LOD pass and human GATE-ART review rather than adding indiscriminate microdetail now.

WORLD CLAIM STATUS: **KEEP**  
ATOMIC ATRIO CLAIM STATUS: **KEEP / IN_PROGRESS**
