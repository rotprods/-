# EXOVANT 2950 — WORLD DENSITY ×100 V2

Status: **PROTOCOL_CANDIDATE until merged to `main`**  
Command: `/EXOVANT-X100`  
Authority after merge: default production-selection layer used **with**, never instead of, Fleet Coordination, Graphify/COS and Gauntlet.

## 0. Mission

EXOVANT worlds must not converge toward “many generated objects.” They must converge toward **credible world depth**: history, function, ecology, culture, gameplay, matter, temporal state, audiovisual identity and runtime viability at every relevant scale.

V2 upgrades WORLD DENSITY ×100 from a qualitative mandate into a deterministic production-control loop:

`Fleet ownership → Spatial/vector awareness → Multiplicative completeness → Bottleneck gradient → highest-value unclaimed gap → fidelity-appropriate build path → Gauntlet → evidence → recompute → next gap`.

It does not certify art by itself. It decides where effort has the highest expected marginal impact and prevents local “DONE” from being mistaken for world completeness.

## 1. North Star / `/define-goal`

> Maximize credible playable world depth per production-hour across all twelve EXOVANT worlds without AI slop, ownership collisions, hidden runtime debt or loss of recoverability.

Release target is not “100% assets.” Target is evidence-backed world completeness with all critical dimensions alive, L0–L5 represented where relevant, applicable engine/human gates passed and no unresolved P0/P1 inside the claimed scope.

## 2. Objective function: multiplicative, not additive

For each world let `c_i ∈ [0,1]` be evidence-backed coverage for the 14 dimensions defined in `ops/x100/config.json`.

`WORLD_COMPLETENESS = Π(c_i ^ w_i)`

Weights sum exactly to 1. Critical dimensions are macro world, meso architecture, micro assets, gameplay, material causality, optimization and QA.

Rules:

1. any critical `c_i = 0` ⇒ completion score is exactly `0`;
2. `null`/unmeasured is **not** converted to zero silently: state is `MEASUREMENT_REQUIRED`;
3. evidence controls `c_i`; branch existence, render existence or asset count alone do not;
4. thresholds:
   - `<15%` BLOCKOUT
   - `15–35%` PLAYABLE FOUNDATION
   - `35–65%` PRODUCTION WORLD
   - `65–85%` DENSE AAA WORLD
   - `85–95%` AAAA CANDIDATE
   - `95%+` RELEASE CANDIDATE.

A world cannot compensate for zero ecology, gameplay or QA by overproducing architecture.

## 3. Gradient / adaptive weight algorithm

V2 does not use fixed priority forever. After every evidence-producing wave it recalculates bottleneck pressure.

For base weight `w_i`, coverage `c_i`, λ=1.5 and p=2:

`w'_i = normalize(w_i × [1 + λ(1-c_i)^p])`

Log-gradient pressure:

`P_i = normalize(w'_i / max(ε,c_i))`, with `ε=0.025`.

Thus weak dimensions gain pressure automatically without deleting creative importance.

Each candidate atomic gap receives:

`VALUE = marginal_gain + critical_path + dependency_unlock + player_visibility + reuse + art_importance + systemic_yield + gameplay_value + evidence_confidence + image_grounding_bonus - collision_risk - unresolved_dependency - slop_risk - technical_cost`

The exact coefficients live in `ops/x100/config.json`.

Hard fences override score:
- already claimed by another owner ⇒ ineligible;
- irreversible blocked decision ⇒ ineligible;
- missing Definition of Ready ⇒ ineligible;
- unsafe destructive operation ⇒ stop.

The optimizer is advisory **inside authorized ownership**. It never steals a claim.

## 4. Scale pyramid / WORLD_DENSITY_GATE

Every major world audit tracks:

- `L0 PLANETARY`
- `L1 REGIONAL`
- `L2 DISTRICT / SETTLEMENT`
- `L3 ARCHITECTURAL`
- `L4 PROP / ECOLOGY`
- `L5 MICRODETAIL`

A world cannot pass DENSE_AAA_GATE if applicable L0–L5 coverage is absent. “Microdetail” does not mean noise: it means physically caused bolts, seams, fibers, erosion, residues, repair and manufacturing evidence.

## 5. Master Asset Graph V2

Flat asset lists are deprecated for X100 decisions.

Every family is modeled as relationships among:

`WORLD → REGION/BIOME/CIVILIZATION → DOMAIN → FAMILY → BASE ASSET → VARIANT → STATE → LOD/COLLISION → PLACEMENT → GAMEPLAY/STORY`.

Required family outputs:

- stable ID;
- semantic purpose;
- scale/dimensions;
- base/hero/support/systemic role;
- variant set;
- temporal/material/damage states;
- LOD policy;
- collision policy;
- snapping/modular interfaces;
- procedural placement constraints;
- gameplay/story tags;
- source/export/receipt;
- owner/claim/provenance.

Graphify remains the project-wide typed graph. X100 adds density, family and vector metadata; it does not create a competing source of truth.

## 6. Combinatorial multiplier

`PERCEIVED_COMPLEXITY` should grow by causal recombination, not cloned meshes.

For a family:

`COMBINATIONS = size_variants × regional_variants × material_states × temporal_states × gameplay_states × configurations`

Heuristic grades:
- `<10` poor;
- `10–29` acceptable;
- `30–99` strong;
- `100+` production-grade systemic kit.

100 configurations are valuable only if they remain plausible. A high combinatorial count with random grunge or meaningless topology receives high `slop_risk`.

## 7. Hero / Support / Systemic target

Planning target, not a quota:

- 5% HERO;
- 20% SUPPORT;
- 75% SYSTEMIC / PROCEDURAL.

Hero assets establish identity. Support assets explain the specific place. Systemic kits generate breadth. The ratio is audited at family level, never achieved by duplicating filler.

## 8. AAA fidelity path: Lookdev → image → polygon → clean asset

V2 makes the earlier image-to-polygon strategy explicit.

For Tier S/A hero families or forms whose identity is not already locked, default sequence:

1. `LOOK_LOCK`
   - approved visual target pack;
   - silhouette, proportion, material, construction, wear, climate and narrative intent;
   - multiple useful views where reconstruction needs them.
2. `REFERENCE_PACK`
   - provenance/license;
   - physical observations, not copied copyrighted design.
3. `IMAGE_TARGET_APPROVAL`
   - target images can use Nano Banana/Higgsfield/other approved visual systems;
   - an attractive image is a target, not game geometry.
4. `IMAGE_TO_3D_BASE`
   - Higgsfield 3D Jutsu/reconstruction when it offers real leverage;
   - photogrammetry/manual/procedural route when superior;
   - output status: **BASE_CANDIDATE** only.
5. `GEOMETRY_CAUSALITY`
   - correct scale, mass, thickness, load paths, access and manufacturing.
6. `CLEANUP_RETOPO`
   - topology/shading/UV/pivots/modularity.
7. `UV_MATERIAL`
   - runtime-supported channels; material response caused by construction/environment.
8. `LOD_COLLISION`
9. `ENGINE_IMPORT`
10. `VISUAL_REGRESSION`
    - engine shot vs approved look target;
    - residual error vector: silhouette, proportion, material, density, lighting/readability, scale.
11. `RECEIPT`.

**Raw AI/reconstruction mesh is never final.**

For systemic kits, procedural/manual modeling may skip image-to-3D when it produces cleaner, more reusable geometry. A waiver records why.

### Lookdev residual gradient

For target-vs-runtime comparison, track normalized errors:

`E = [silhouette, proportion, material, construction, density, scale, readability]`.

Fix the highest weighted residual first. Do not compensate a bad silhouette with microdetail.

## 9. Variation without slop

Allowed causal axes:

`environment + manufacturing + age + usage + damage + repair + culture + biology`.

Forbidden shortcuts include random grunge, uniform scratches, meaningless greeble, unmotivated emissive, uncontrolled decal spam, plastic material convergence, unjustified symmetry and random microgeometry.

Every variation must answer “why did this physical difference occur?”

## 10. Culture / ecology / history requirements

### Culture DNA

Every civilization should become identifiable without logos through manufacturing language, construction logic, ergonomics, ornament, repair, resource constraints, palette/material logic, iconography, hierarchy and technology.

### Ecology graph

Where ecology applies:

`RESOURCE → PRIMARY CONSUMER → PREDATOR → SCAVENGER → DECOMPOSER`

Effects must reach terrain, vegetation, structures, routes, remains, sound, light or gameplay.

### History as geometry

Important zones should expose at least three interpretable temporal strata when canon supports them:

`ERA_0 original → ERA_1 occupation/modification → ERA_2 current degradation/adaptation`.

## 11. Fifteen density passes

No blockout → random-detail jump.

1. MACRO
2. STRUCTURE
3. GAMEPLAY
4. SUPPORT ASSETS
5. PROPS
6. ECOLOGY
7. MATERIAL HISTORY
8. MICRODETAIL
9. STORYTELLING
10. LIGHTING
11. AUDIO HOOKS
12. OPTIMIZATION
13. PLAYER SCALE
14. DISTANT VISTA
15. FINAL ART REVIEW

Receipts record which passes apply, pass, fail, or are explicitly waived.

## 12. Spatial-semantic branch awareness

`tools/x100_spatial.py` builds a deterministic 64-dimensional vector per Fleet claim and fetched non-main branch.

Vector includes:
- world identity;
- L0–L5 scale;
- production domain;
- claim status;
- **only explicit** physical bounds when known;
- hashed semantic tail from branch/claim/paths/assets/projects.

Rules:
- unknown coordinates are encoded as `spatial_known=0`, never `(0,0,0)`;
- branch-name world inference is tagged `OBSERVED_BRANCH__SEMANTICS_INFERRED_FROM_NAME`;
- Fleet registry retains ownership authority;
- cosine similarity is a retrieval/awareness aid, not proof of collision;
- physical overlap is evaluated only when both entries carry explicit bounds;
- every vector keeps provenance.

This provides every agent with a compact local map of branch/claim/world/domain proximity after refs are fetched, without inventing physical geography.

## 13. Integration with anti-collision protocol

Mandatory order:

`RESYNC → X100 SPATIAL BUILD → FLEET CHECK → COVERAGE AUDIT → GRADIENT → CANDIDATES → COLLISION CHECK → CLAIM → BUILD`.

Never:

`rank → build → discover owner later`.

Fleet owns:
- owner;
- claim;
- epoch;
- paths;
- project IDs;
- asset IDs;
- scope collision.

X100 owns:
- density measurement;
- gap pressure;
- value ordering;
- family expansion;
- fidelity route;
- systemic yield.

## 14. Default execution loop

`/EXOVANT-X100` means:

1. RESYNC repository / current main.
2. BOOTSTRAP existing project protocols and relevant learning.
3. Build/update spatial-semantic index.
4. Read Fleet and current producer evidence.
5. Audit world/family coverage.
6. Compute multiplicative completeness.
7. Compute bottleneck-adaptive gradient.
8. Enumerate atomic gaps.
9. Remove claimed/conflicting/not-ready candidates.
10. Select highest-value eligible gap.
11. Claim through existing Fleet procedure.
12. Decide fidelity route:
    - hero/high-identity → LOOKDEV-TO-MESH;
    - systemic → modular/procedural-first;
    - ecology/terrain/etc. → domain-specific verified route.
13. Build base family.
14. Expand causal variants/states.
15. Add systemic generation/placement rules.
16. Validate scale/gameplay/material causality.
17. Engine import / collision / LOD as applicable.
18. Gauntlet.
19. Persist source/export/tests/receipts.
20. Update coverage and graph.
21. Recompute gradient.
22. Handoff.
23. Select next eligible gap.

Stop only for existing constitutional stop conditions.

## 15. Per-family DoD

A family is not complete until applicable items have evidence:

semantic purpose, stable ID, dimensions, player scale, silhouette, manufacturing logic, UV0, material slots, pivot, clean transforms, collision, gameplay clearance, LOD strategy, variants, state variants, optimization, engine import, visual QA, technical QA, receipt, persisted source, persisted export and updated claim/handoff.

`tools/x100_control.py family` rejects `raw_ai_mesh_final`.

## 16. World audit data contract

World owners should persist an X100 audit inside an owned path. Minimal example:

```json
{
  "world_id": "nacre",
  "coverage": {
    "macro_world": 0.70,
    "meso_architecture": 0.40,
    "micro_assets": 0.10,
    "ecology": 0.05,
    "civilization": 0.25,
    "gameplay": 0.20,
    "material_causality": 0.35,
    "variation": 0.15,
    "temporal_states": 0.10,
    "storytelling": 0.20,
    "audiovisual_language": 0.15,
    "optimization": 0.20,
    "reusability": 0.40,
    "qa": 0.30
  },
  "scale_coverage": {"L0": true, "L1": false, "L2": false, "L3": true, "L4": false, "L5": false},
  "evidence": []
}
```

Numbers without evidence are estimates, not certification. Use `null` if not measured.

## 17. Commands

```bash
python3 tools/x100_control.py validate-config
python3 tools/x100_control.py audit path/to/world-x100.json
python3 tools/x100_control.py rank path/to/world-x100.json path/to/candidates.json
python3 tools/x100_control.py family path/to/family.json

python3 tools/x100_spatial.py build
python3 tools/x100_spatial.py validate
python3 tools/x100_spatial.py query claim:CLM-NACRE-WORLD-MACRO-001
```

Then run the existing Fleet and Gauntlet commands.

## 18. Adoption rule

After merge to `main`, this V2 is the default production-selection protocol for EXOVANT world/asset development.

It does **not** retroactively invalidate work. Existing owners adopt it at their next normal resync/handoff. No forced heartbeat or background job is created. A producer that cannot yet measure coverage records `MEASUREMENT_REQUIRED`, then continues safe work already inside its claim while creating the missing audit evidence.

## 19. Final principle

Do not optimize for asset completion.

Optimize for:

`credible depth gained × systemic reuse × gameplay value × fidelity / (technical cost + collision risk + slop risk + unresolved dependency)`

while preserving the multiplicative world bottleneck.

A dense world should look like it had causes before the player arrived, not like an asset generator ran longer.
