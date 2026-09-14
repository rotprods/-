# UMBRA COLD HANDOFF — ART-UMBRA-001

## Identity

- Project: EXOVANT 2950
- World: `W04 UMBRA`
- Owner: `AGENT-UMBRA-04`
- Claim: `CLM-W04-WORLD-UMBRA-001`
- Role: `WORLD_OWNER`
- Branch: `art/world-umbra-001`
- PR: `#16` — DRAFT / KEEP
- Linear: `ROT-119` — In Progress
- Primary Blender: `7ab99682-8777-4143-8ae0-1fbb178ccafb`
- Independent replay Blender: `7f33ae14-540c-4af5-8131-1490465fe6cc`

## Resume truth

Current state is **X100 Production World foundation at 40.86% multiplicative completeness, not final AAAA**.

Do not restart UMBRA. Do not treat object count as completeness. Do not invent planet scale, detailed ecology species, religion/lore text or final NOCTIL morphology to inflate X100.

Current primary scene is revision **15**, checkpoint `X100_HABITATION_ANNEX_QA_FIXED_001`:

- `4,871` objects;
- `4,329` mesh objects;
- `13` materials;
- `0` residual non-unit scales;
- `0` zero-dimension meshes;
- editable `.blend` `15,793,297 B`;
- GLB `4,566,312 B`.

Independent clean replay is verified through **Wave 2**, not through the full X100 batch. X100 replay is still pending and must not be claimed as PASS.

## Current repository/fleet state

Latest resync incorporated `main@26ae20f5d1b47d1efa0d54b20124ed93cbc0b43e` through normal two-parent commit `8ee7d335754400f2b4847dfc966ced7dfdbf7815`; no force update was used.

That main commit placed the EXOVANT Gauntlet under **manual cost quarantine**: `.github/workflows/gauntlet.yml` now uses `workflow_dispatch` only. Therefore batch meaningful producer work, refresh exact `MANIFEST.json` last, then execute one bounded manual Gauntlet instead of spending Actions on every commit.

Fleet registry truth at last readback:

- claim `CLM-W04-WORLD-UMBRA-001`;
- owner `AGENT-UMBRA-04`;
- epoch `1`;
- status `active`;
- ACK evidence issue #7 comment `5648349781`.

Always re-read main/registry/PR before a new destructive mutation because the multi-agent fleet can advance independently.

## Canon safe to rely on

- UMBRA / World 04 / Sere / Flotilla de los Sin Sol / NOCTIL.
- Sere is a fictional M4 V red dwarf.
- synchronous rotation; habitation concentrated in the twilight band.
- small reflector-station swarm.
- reference gravity `0.81 g`.
- reference-area temperature `−87 °C`.
- light/shadow are navigation permissions as well as thermal states.
- reflector activation can reveal routes while exposing caravans.
- visual seed: mobile twilight, caravans, reflectors, dark ice, tensioned fabric, constant lateral wind.
- darkness must preserve combat anticipation.

Quest chain:

- `Q_UMBRA_M01` — La frontera del día.
- `Q_UMBRA_M02` — Sombras que respiran.
- `Q_UMBRA_M03` — Geometría del eclipse.
- `Q_UMBRA_M04` — El refugio de NOCTIL.

Still blocked by canon/spec:

- physical planet radius/diameter/global geography/atmosphere contract;
- detailed native ecology/flora/fauna;
- final NOCTIL morphology/function/rig/attacks.

The authored `1200 × 700 m` L2 region remains a reversible proposal, never planet size.

## Verified historical foundations

### Wave 1

- 407 objects / 395 meshes / 9 materials / 35,028 evaluated tris.
- terrain-aware reflector/caravan/refuge contact corrections.
- reflector mechanism and caravan production foundations.
- independent Wave-1 replay PASS.

### Wave 2

Checkpoint `WAVE2_REFUGE_QUESTCELLS_OPT_001`:

- 552 objects / 536 mesh objects / 10 materials / 44,616 tris.
- refuge production foundation.
- authored M01–M04 environment cells.
- exact mesh-data sharing optimization.
- contact and camera/framing gates PASS.
- independent Wave-2 replay PASS on structural/semantic contract.

Do not regress Wave-0 defects previously found: caravan tracks once floated ~2.43–5.80 m and several foundations had errors up to ~3.62 m.

## X100 control plane

`/EXOVANT-X100` is active permanently for UMBRA.

Persisted control surfaces:

- `WORLD_DENSITY_X100.md`
- `WORLD_DENSITY_X100_PROGRESS.json`
- `TASKS.md`
- `ASSET_MANIFEST.json`

Current conservative multiplicative completeness: **40.86% — PRODUCTION WORLD**.

The low ecology (`0.02`) and macro-world (`0.18`) factors are intentional blockers; they are not to be compensated by adding random props.

## X100 production delivered

### 1. Service / cultural utility ecosystem

10 families:

`CABLE_REEL`, `HEATEX`, `LAMP`, `POWERBOX`, `SERVICE_STAND`, `STORAGE`, `TEXTILE`, `TOOLCASE`, `WAYFIND`, `WINCH`.

Each has S/M/L and causal service states. Total library roots: 90.

Three systemic service yards exist:

- caravan repair;
- reflector maintenance;
- refuge logistics.

### 2. Damage / abandonment

60 family-specific `DAMAGED` / `ABANDONED` roots exist. Damage is causal, not random destruction or blanket grunge.

### 3. Architectural interface library

10 families:

`ACCESS_CANOPY`, `ACCESS_DOOR`, `BRIDGE_DECK`, `CABLE_GLAND`, `CONDUIT_JUNCTION`, `GANTRY_FRAME`, `HANDRAIL`, `LADDER`, `PLATFORM`, `SERVICE_HATCH`.

Each has S/M/L and `STANDARD / WIND_SHIELDED / FIELD_MODIFIED` fabrication variants under a 0.2 m modular interface contract.

### 4. L5 microdetail library

10 causal families exist in Blender:

`ABRASION_GUARD`, `CABLE_CLAMP`, `EXPANSION_JOINT`, `FASTENER_PLATE`, `GASKET_FLANGE`, `HINGE`, `ISOLATOR_FOOT`, `LATCH`, `REPAIR_PATCH`, `WELD_SEAM`.

Placement mode is explicitly rule-driven, never random scatter.

**Important:** exact generator/receipt persistence for this library remains open. Scene existence is authoritative evidence, but do not call it reproducible until `W04/X100/037` is closed.

### 5. Site-history integration

Checkpoint `X100_SITE_HISTORY_INTEGRATION_001` integrated 31 linked prefab roots into five real locations:

- refuge service;
- reflector 02;
- reflector 03;
- M03 archive;
- caravan repair.

Physical history is encoded as:

`ERA_0 ORIGINAL → ERA_1 MODIFICATION → ERA_2 CURRENT DAMAGE/REPAIR`.

All 31 roots are terrain-seated at `+0.04 m`.

Persisted source/receipt:

- `integrate_x100_site_history.py`
- `X100_SITE_HISTORY_RECEIPT.md`

### 6. Habitation / culture systemic library

10 daily-survival families:

`SLEEP_POD`, `RATION_LOCKER`, `MESS_TRAY`, `HEATED_BENCH`, `DRYING_RACK`, `PERSONAL_LOCKER`, `MED_CABINET`, `PRIVACY_SCREEN`, `CREW_ID_PLATE`, `THERMAL_VESSEL_RACK`.

Each has:

- S/M/L;
- `SERVICED / LIVED_IN / FIELD_REPAIRED`;
- stable ID;
- semantic purpose;
- placement rules;
- provisional LOD/collision contract;
- at least 108 credible configuration combinations.

Total library roots: 90. All 90 pass terrain contact at `+0.03 m`.

Cultural identity is deliberately utilitarian/survival-derived: low profile, glove ergonomics, strapped/sealed storage, replaceable repairs, functional heat transfer and non-text identity marks. No unlicensed/invented lore text or religion was introduced.

### 7. Habitation QA correction

The first habitation site composition exposed a real defect in the underlying refuge: `ARCH_REFUGE_HUB_BASE` is still a closed blockout solid (8 vertices / 6 faces / 44×30×12 m). Therefore placing furniture inside its bbox would hide it inside solid geometry.

The invalid interpretation was rejected. At revision 15, the 12 domestic roots were moved to a **visible leeward habitation annex** outside the solid base, and 20 structural roots were reused from the X100 architectural kit:

- 6 field-modified gantry frames;
- 6 wind-shielded canopies;
- 6 wind-shielded handrails;
- 2 entry decks.

All 32 integrated roots pass contact at `+0.03 m` and the annex reserves a central entry corridor.

Persisted source/receipt:

- `generate_x100_habitation_culture.py`
- `fix_x100_habitation_annex.py`
- `X100_HABITATION_RECEIPT.md`

## Visual epistemic state

A 960×540 Eevee review artifact exists for r15 (`21c57b605bb5715b889c8394f4214cc9`). The temporary review camera was too tight to contain both extreme canopy bays. That is a review-camera framing defect, not evidence of a geometry/contact failure.

The current session cannot independently inspect the image pixels through the available binary transport, so:

`DIRECT_PIXEL_ART_REVIEW = REVIEW_NOT_CLAIMED`

Do not turn this into PASS without actual image/human inspection.

## Current blockers / open acceptance gates

1. Physical planet/global representation contract.
2. Native ecology/flora/fauna canon.
3. Final NOCTIL entity contract.
4. Final UV0/PBR/texel-density/material budgets.
5. UMBRA-specific runtime import/collision/traversal/profile.
6. LOD/HLOD + target GPU budget.
7. Direct pixel/human art review and low-light accessibility acceptance.
8. Exact X100 independent replay.
9. Exact microdetail generator/receipt persistence.
10. MR-EXO-001 provider-independent `.blend` + GLB + dependency custody.
11. Post-X100 exact root `MANIFEST.json` and one manual cost-bounded Gauntlet.

## Next critical path

1. `W04/X100/040`: build traversal/settlement systemic grammar linking hardpack routes, service yards, refuge annex and quest cells using bridges, sheltered checkpoints, loading interfaces and thermal refuge markers. Keep runtime behavior external.
2. `W04/X100/037`: recover/persist exact microdetail generator/receipt from authoritative scene metadata.
3. Batch those changes, RESYNC main, regenerate exact `MANIFEST.json` as final byte-level content change, then run one manual Gauntlet under CI cost quarantine.
4. Coordinate runtime import/collision/profile; only after that lock LOD/material budgets.

Claim status: **ACTIVE / KEEP**.
