# KHEPRI — World Macro / Planetary Foundation Contract

**Scope:** `khepri/world-macro/planetary-foundation`  
**Claim:** `CLM-KHEPRI-WMACRO-001`  
**Agent:** `AGENT-KHEPRI-WMACRO-001`  
**Session:** `SESSION-20260912-KHEPRI-001`  
**Branch:** `art/world-khepri-001`  
**Base main:** `4c2fa044080004609ea6df45f34b2a784536507a`  
**3D Jutsu project:** `040f0c45-83a7-483c-9ee7-1e31c640a587`  
**Status:** IN_PROGRESS / WAVE 0→1

## 1. Repo evidence pack

| Evidence | Value | Epistemic status |
|---|---|---|
| Repository | `rotprods/-` | OBSERVED |
| Default branch | `main` | OBSERVED |
| Base HEAD at claim | `4c2fa044080004609ea6df45f34b2a784536507a` | OBSERVED |
| Canon files | `AGENTS.md`, `_project_intelligence/STATE.json`, `_project_intelligence/PLAN.json`, `HANDOFF.md`, `MEMORY.md`, `design/EXOVANT_BIBLIA.md`, `design/EXOVANT_DATA.json` | DOCUMENTED |
| Agent protocol | `AGENTS.md` + `docs/PROTOCOLS.md` | DOCUMENTED |
| Art authority | `docs/ART_PRODUCTION.md` | DOCUMENTED |
| World authority | `design/EXOVANT_BIBLIA.md` + `design/EXOVANT_DATA.json` | DOCUMENTED |
| Progress authority | `_project_intelligence/STATE.json`; global `PROGRESS.md` is a readable projection | DOCUMENTED |
| Claims authority | No dedicated claim system found; fallback shard under `production/claims/` introduced only on this branch | OBSERVED + PROPOSAL |
| Runtime engine | Godot 4.7.2 executable prototype | DOCUMENTED |
| Production-engine decision | Unreal remains principal candidate; not yet qualified as irreversible target | DOCUMENTED |
| Blender workflow | Higgsfield 3D Jutsu / Blender 5.2.0 LTS / `bpy` / editable `.blend` + generator + GLB + validation evidence | DOCUMENTED + OBSERVED |
| “Flu In / Flow In” | No matching repo workflow/addon/script found in `rotprods/-`, `game-dev-mcp-hub`, or `rot.knowledge` searches | `PIPELINE_METHOD_NOT_FOUND` |
| Units | Existing Blender art pipeline works at metre scale; this scope uses `1 BU = 1 m` | DOCUMENTED + LOCAL CONTRACT |
| Authoring coordinates | Blender `bpy`: Z-up local cell coordinates | TOOL CONTRACT |
| Portable export | glTF/GLB; conversion to glTF Y-up handled by exporter/tooling | TOOL CONTRACT |
| Naming | Existing project requires descriptive names; this scope uses deterministic `KHP_WM_*` semantic prefixes without changing global convention | LOCAL CONTRACT |
| Source of truth | GitHub `rotprods/-` `main`; this branch is proposed work until integrated | DOCUMENTED |

## 2. Canon extracted for KHEPRI

The following facts are not invented by this cell:

- **CANON/PROPOSED WORLD ENTRY:** world `khepri`, galaxy Andrómeda, system Sahra, faction **Sínodo de Bronce**.
- **DOCUMENTED:** Sahra is an F8 V fictional star; Khepri is described as a **solar-glass desert with cities under heliostats**, with the reflector station Aguja and two fictional rocky moons.
- **DOCUMENTED:** environmental reference is **0.63 g** and **71 °C** for the authored area.
- **DOCUMENTED:** gameplay rule: **light stores energy and rights of use; orienting mirrors changes temperature, doors and district supply**.
- **DOCUMENTED:** boss is **RA-KHET, sol encadenado**.
- **DOCUMENTED:** core mission chain includes repairing communal shade, crossing the glass sea via reflectors or subterranean routes, freeing indebted technicians in the crucible, confronting RA-KHET by redistributing beams between arena nodes, and deciding ownership/maintenance of the solar infrastructure.
- **DOCUMENTED:** visual kit: **crystal and shadow — fabrics, mirrors, scorched ceramic, prisms and walkways**. Art risk: uncontrolled reflections/emission and overexposure.
- **DOCUMENTED:** sound language: glass bells, resonant cables, solar-tracking motors.

## 3. Unknowns that remain unknown

- Physical planet radius, mass, atmosphere composition/pressure, axial tilt, day length, orbital elements, tectonic model and exact continental map are **not canonically fixed in the recovered files**.
- Final playable-area dimensions and shipping streaming-cell dimensions are **not measured against target hardware**.
- Production engine is **not yet irreversibly selected**.
- GPU budgets, virtual-geometry support and final HLOD implementation are **not qualified**.

No value in these categories may silently become canon through this branch.

## 4. Local North Star

Deliver the **KHEPRI planetary/world-macro foundation** as a reproducible Blender scene and shard documentation that:

1. preserves all recovered KHEPRI canon;
2. separates **L0 physical-planet metadata**, **L1 orbital representation**, **L2 macro terrain** and future **L3/L4 gameplay/hero cells**;
3. works at physical metre scale in Blender local coordinates without attempting a single planet-sized mesh;
4. demonstrates one representative solar-glass macro cell with readable terrain frequency, heliostat-field footprint and three functional route anchors as proxies only;
5. exports from the verified Blender pipeline and produces measurable geometry/scene receipts;
6. can be continued by another agent without chat history;
7. does not claim engine integration, AAA finish or canonization of proposed planetary values without gates.

### Quantified acceptance for this wave

- Exactly one editable 3D Jutsu project linked to this claim.
- One deterministic generator script committed to the branch.
- One L1 orbital proxy representation and one L2 local-tangent macro cell.
- Local macro cell target extent: **6.4 km × 4.8 km** (`PROPOSAL`, chosen for pipeline validation, not final playable acreage).
- At least 3 semantically named functional proxy anchors derived from documented mission needs, with no final architecture authored.
- Human scale reference present only as QA guide.
- Scene audit reports object/mesh/material counts, world extents, transform anomalies and duplicate-name errors.
- `.blend` and GLB are retrievable from the committed 3D Jutsu revision; repo binary persistence is required before claiming asset-source DONE.
- Neutral/in-context preview rendered and visually inspected before `QA_PASS`.
- No edit to canonical global PLAN/STATE from this parallel branch unless single-writer reconciliation occurs.

## 5. Planet-scale engineering hierarchy

| LOD of authorship | Purpose | KHEPRI contract |
|---|---|---|
| L0 Planetary canon | Physics/geodesy metadata | Canon gravity = 0.63 g; radius/mass remain proposal pending ADR approval |
| L1 Orbital representation | Low/medium frequency planet silhouette | Separate lightweight mesh/metadata; never gameplay collision |
| L2 Continent/region | Macro topography and bioclimatic partitions | Tileable/local-tangent representation; kilometres per cell |
| L3 Gameplay cells | Traversable authored areas | OUT OF CURRENT CLAIM except proxy interfaces |
| L4 Hero zones | Dense authored encounter/city areas | EXCLUDED |
| L5 Hero assets | Close inspection assets | EXCLUDED |

**Coordinate rule:** KHEPRI world-space production is represented by `(planet_id, geodetic/planetary tile key, local_cell_origin, local XYZ metres)`. Blender only authors local cells. This avoids floating-point loss and makes later Godot/Unreal adapters possible without asserting an engine feature that has not been qualified.

## 6. Art-direction contract for macro foundation

### Shape
Large optical planes, shallow desert basins, radial/axial solar infrastructure, long shadows, sparse but unmistakable vertical navigation markers. Avoid generic sci-fi skyline noise.

### Proportion
Infrastructure must read as heat-management and solar-routing machinery. Proxy landmarks must include human-scale references and service clearances; no scale ambiguity.

### Material role at macro stage
- solar glass substrate: dark amber/brown transparent-looking *mass*, but blockout uses opaque portable PBR to avoid false translucency cost;
- Sínodo/precursor bronze: structural/ritual load-bearing language;
- scorched ivory ceramic: thermal shielding/habitation proxy;
- black mineral: thermal mass, foundations and deep-shadow separators;
- emissive only where it encodes solar routing / access state.

### Forbidden drift
- cyan-neon cyberpunk city language;
- random greebles;
- uniform edge wear;
- mirror spam without optical purpose;
- unbounded emission/bloom;
- ornamental pyramids/ancient-Egypt imitation as a shortcut for the name Khepri;
- final character/creature/architecture detail inside this claim.

## 7. Technical interface for other agents

Other KHEPRI agents may safely claim domains such as architecture, materials, NPCs, fauna, vehicles or RA-KHET. They should consume, not mutate, these interfaces until coordinated:

- `KHP_WM_PLANET_META` — L0 proposal/canon metadata object.
- `KHP_WM_MACROCELL_A` — representative local cell anchor.
- `KHP_WM_ROUTE_SHADE` — communal-shade route anchor.
- `KHP_WM_ROUTE_GLASS_SEA` — glass-sea crossing route anchor.
- `KHP_WM_ROUTE_CRUCIBLE` — crucible route anchor.
- `KHP_WM_ROUTE_RAKHET` — boss-approach interface anchor.

The anchors define locations/interfaces only. They do **not** reserve final meshes owned by other domains.

## 8. Definition of Done — current claim

This claim is not DONE until all applicable checks are true:

- [x] Repo/authority bootstrap reconstructed
- [x] Semantic collision audit performed against observed parallel branches
- [x] Atomic claim persisted
- [x] Blender pipeline identified; `Flu In / Flow In` marked not found instead of guessed
- [ ] Planet-scale ADR recorded with CANON vs PROPOSAL separation
- [ ] Generator script committed
- [ ] Blender macro scene generated from clean project
- [ ] Geometry/scale audit PASS
- [ ] Neutral/in-context visual inspection PASS or explicit defects logged
- [ ] GLB retrieval verified
- [ ] `.blend` retrieval verified
- [ ] Binary persistence strategy resolved/recorded
- [ ] Manifest and receipts updated
- [ ] Draft PR opened after meaningful source/evidence exists
- [ ] Final resync confirms no ownership collision
- [ ] Recoverable handoff written

Until then claim state remains `IN_PROGRESS` / `KEEP`.
