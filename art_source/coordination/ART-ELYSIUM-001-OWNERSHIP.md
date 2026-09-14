# ART-ELYSIUM-001 · ELYSIUM NULL world production ownership

Date: 2026-09-12. User directive: execute a bounded, multi-week AAAA+ 3D world-production stream for one EXOVANT 2950 world, coordinated with parallel world/art agents and without duplicating active scopes.

Base at original reservation: `4c2fa044080004609ea6df45f34b2a784536507a`.
Branch: `art/world-elysium-null-001`.
World: `elysium` / **ELYSIUM NULL**.
Cell: `ART-ELYSIUM-001`.
Ownership classification: `WORLD_OWNER`.
Linear projection: `ROT-116` — `EXO-018-ELYSIUM-ART · ELYSIUM NULL full 3D world production cell`, child of `ROT-110`.
Coordination surface: GitHub issue `#7`.
Canonical source refs: `AGENTS.md`, `_project_intelligence/STATE.json`, `_project_intelligence/PLAN.json`, `HANDOFF.md`, `MEMORY.md`, `GOALS.md`, `ROADMAP.md`, `design/EXOVANT_BIBLIA.md`, `design/EXOVANT_DATA.json`, `docs/ART_PRODUCTION.md`, `ARCHITECTURE.md`, `learning/README.md`, `learning/.../LRN-EXO-20260912-BLENDER.json`.

## Ownership-preflight timing receipt

The reservation branch was created from `main@4c2fa044080004609ea6df45f34b2a784536507a` after a live branch audit showed no ELYSIUM owner and the authenticated 3D Jutsu project list showed no ELYSIUM World Master.

While this cell was already producing W0, `main` advanced to `196ef814fdc845ec797979906d01dc25009217c7` through PR #12, adding the mandatory branch + PR + Linear ownership preflight to `AGENTS.md`. This branch therefore does **not** claim that Linear reservation preceded geometry. The new rule was reconciled immediately after discovery:

- current `AGENTS.md` re-read;
- coordination issue #7 re-read;
- all current repository branches re-fetched;
- relevant art/world PR state re-fetched;
- ELYSIUM classified as `WORLD_OWNER`;
- Linear issue `ROT-116` created under EXO-018;
- issue #7 updated with the timing receipt and Linear projection;
- fresh branch state still shows exactly one ELYSIUM owner branch.

Current `main` is one commit ahead of the original merge base only because of the ownership-policy update; this branch must be reconciled normally before merge. No force update is permitted.

## Collision audit

Observed active art branches before original claim included ARES IX, Terra, Khepri, Leviathan, Nacre, Pelagos/Thalassa, Sylva Prime, Umbra and Vanta. No branch containing `elysium` existed at claim time.

Fresh preflight after the policy landed additionally shows Aurora Veil and Origin owners, while ELYSIUM remains represented only by `art/world-elysium-null-001`. GitHub coordination issue #7 now records ELYSIUM NULL as `OCCUPIED` by this branch.

## Owned paths

- `art_source/worlds/elysium_null/**`
- `art_source/coordination/ART-ELYSIUM-001-OWNERSHIP.md`

All runtime Godot scenes/scripts, existing portal sources, shared project `STATE/PLAN/HANDOFF`, other worlds and other agents' branches are outside this branch's direct edit scope. Shared-state changes are proposals for the integrator and MUST be reconciled against the newest `main`.

## Canonical world seed

Verified project canon describes ELYSIUM NULL as an Act III world in **EL UMBRAL**, system/locality `Alba Nula`, faction `Los Custodios Vacíos`, 1.00 g, 21 °C, and explicitly a world-scale artificial habitat rather than a natural planet. Boss: `EDEN, la perfección hostil`. Art-kit seed: white/clean arcology modules, repeated gardens and carefully localized human traces. The documented risk is that minimalism can read as missing content; narrative density must therefore come from objects, state changes, interactions and causal wear rather than visual clutter.

## Qualified remote Blender world master

- Provider/path: Higgsfield 3D Jutsu / `bpy`.
- Project ID: `00152eea-2da0-40ec-8666-78d6764c718f`.
- Project name: `EXOVANT 2950 — ELYSIUM NULL World Master — ART-ELYSIUM-001`.
- Blender observed: `5.2.0 LTS`.
- Units observed/configured: metric, `1 BU = 1 m`.
- Current qualified revision: `3`.

### Revision 1 — foundation

- 153 objects / 149 meshes / 9 material roles;
- 1.85 m scale witness;
- representative Avenida cell;
- canonical EDEN arena measured 48 m diameter;
- editable `.blend`, GLB and preview available;
- exact deterministic source persisted in Git.

### Revision 2 — architecture grammar candidate

- W1 modular kit added;
- 1 m planning grid / 4 m bay / 8-12-16 m spans are explicit proposals;
- 32 arrival façade objects verified to share one prototype mesh datablock;
- 2.4 × 2.7 m door clearance remains pending runtime-controller qualification.

### Revision 3 — EDEN state-graph candidate

- three explicit arena layouts A/B/C;
- 12 target transforms and visible State-B relocation footprints;
- canonical 48 m arena preserved;
- canonical 1.5 s `Reubicación` destination-warning anchor preserved;
- proposed 8 × 8 m modules all remain inside the 24 m arena radius;
- proposed minimum axis corridor: 6 m, pending real gameplay/camera/collision validation.

Latest remote revision 3 artifacts:
- editable `.blend`: 2,615,075 bytes, etag `607b88229b4e4dd16a918925aa74ef98`;
- GLB: 2,507,192 bytes, etag `9f3fc126755c2ff89009cc75cb4978e5`;
- EDEN stategraph preview: `elysium_eden_stategraph_v1.png`, artifact `88b6a9523f38fa5dcaeee39b6d3cb7ee`.

Persisted project learning `LRN-EXO-20260912-BLENDER` requires editable source, generator, portable exchange and evidence. This checkpoint satisfies those surfaces through remote revisions plus repository source/receipts; it does **not** imply target-engine, Unreal or GPU qualification.

## Concurrency contract

Parallel world agents MUST use branch-per-world and disjoint owned paths. Cross-world reusable assets are proposed by stable manifest IDs; integration occurs only after collision, naming, licensing and art-direction review. No force updates. Branch existence and a remote render are not proof of world completion.

If another agent needs ELYSIUM work while this `WORLD_OWNER` is active, it must use an `ATOMIC_SUBCLAIM` with explicit asset IDs/collections/exclusions and coordinate with this owner rather than creating a second full-world branch.

## North Star local

Build ELYSIUM NULL so another artist/agent can continue without chat context: physically coherent world representation, formal art language, complete world/asset coverage registry, modular architecture and ecological systems, deterministic Blender scene generation, hero-location blockouts and measurable QA contracts.

## Scope status

`ACTIVE / W1 ARCHITECTURE + EDEN SPATIAL FOUNDATION`.

Implemented / structurally validated in Blender:
- exclusive world claim and current ownership preflight reconciliation;
- canon recovery and World Bible;
- asset coverage manifest;
- multi-week wave/task plan;
- dedicated Blender World Master;
- deterministic source generators;
- representative Avenida/EDEN foundation blockout;
- modular architecture candidate;
- EDEN A/B/C relocation state graph;
- machine-readable structural QA receipts;
- cold-resume handoff.

Not claimed:
- final visual quality;
- final PBR materials/UVs;
- gameplay-qualified collision;
- target-engine import;
- runtime player/camera clearances;
- LOD/HLOD and target-hardware performance;
- GATE-ASSET;
- GATE-ART;
- human playtest;
- complete ELYSIUM world.
