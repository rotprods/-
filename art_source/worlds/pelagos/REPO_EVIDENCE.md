# PELAGOS · Repo Evidence Pack

Evidence cut: 2026-09-12. This file records observed/documented state for `CLM-PEL-WORLD-001`; it is not a replacement for root project authority.

| Evidence | Value | Epistemic status |
|---|---|---|
| Repository | `rotprods/-` | OBSERVED |
| Default branch | `main` | OBSERVED |
| Base HEAD at claim/resync | `4c2fa044080004609ea6df45f34b2a784536507a` | OBSERVED |
| Project | `EXOVANT 2950 · Humanity game` | DOCUMENTED |
| Root agent protocol | `AGENTS.md` | DOCUMENTED |
| Global state | `_project_intelligence/STATE.json` | DOCUMENTED |
| Global work contract | `_project_intelligence/PLAN.json` | DOCUMENTED |
| Creative world authority | `design/EXOVANT_BIBLIA.md`, `design/EXOVANT_DATA.json` | DOCUMENTED |
| Art authority | `docs/ART_PRODUCTION.md` + world canon | DOCUMENTED |
| Development protocol | `docs/DEVELOPMENT_PROTOCOL.md` | DOCUMENTED |
| Progress authority | STATE/PLAN/PROGRESS/HANDOFF, with STATE/PLAN canonical for mutable task state | DOCUMENTED |
| Claims authority | No pre-existing repository claim schema found by code search; this scope uses a sharded fallback claim file under `production/claims/` | OBSERVED + PROPOSAL |
| Executable prototype engine | Godot `4.7.2.stable` | DOCUMENTED |
| Production engine decision | Unreal remains candidate; not yet qualified | DOCUMENTED |
| Blender route | Higgsfield 3D Jutsu `bpy` | DOCUMENTED/OBSERVED |
| Blender version used for this scope | `5.2.0 LTS` | OBSERVED |
| Blender units used by this scope | metric, scene scale `1.0`; 1 Blender unit treated as 1 metre | OBSERVED WORLD-LOCAL DECISION |
| Blender coordinates | Z-up in `bpy` | DOCUMENTED BY TOOL CONTRACT |
| GLB/editor coordinates | Y-up conversion handled by remote export path | DOCUMENTED BY TOOL CONTRACT |
| Final engine coordinate convention | No project-specific canonical statement located during bootstrap | UNKNOWN |
| Portable export format | GLB/glTF 2.0; editable `.blend` retained | DOCUMENTED/OBSERVED |
| Pelagos naming convention | `PEL_<DOMAIN>_<semantic>` object names and stable `PEL-*` asset IDs | PROPOSAL, world-local |
| Source of truth | GitHub `main` for integrated project; this branch for unmerged Pelagos work; exact 3D scene revision in 3D Jutsu for Blender receipts | DOCUMENTED + OBSERVED |

## Files actually read before build

- `README.md`
- `AGENTS.md`
- `_project_intelligence/STATE.json`
- `_project_intelligence/PLAN.json`
- `GOALS.md`
- `ROADMAP.md`
- `HANDOFF.md`
- `MEMORY.md`
- `learning/README.md`
- `docs/ART_PRODUCTION.md`
- `docs/DEVELOPMENT_PROTOCOL.md`
- `ops/tool-registry.json`
- `design/EXOVANT_BIBLIA.md`
- `design/EXOVANT_DATA.json`
- `learning/.../LRN-EXO-20260912-BLENDER.json`
- `learning/.../LRN-EXO-20260912-ART.json`

## Blender workflow discovery

The approximate user phrase “Flu In / Flow In” was searched in the repository and no exact method/add-on documentation was located. Status: `PIPELINE_METHOD_NOT_FOUND`.

The verified project workflow is instead:

1. Higgsfield 3D Jutsu executes editable Blender `bpy` operations.
2. Inspect revision and scene sequence before mutation.
3. Mutate against exact guards.
4. Retain editable `.blend`, procedural/generator source, GLB and evidence.
5. A successful Blender operation is not sufficient for a game-ready claim.
6. Visual review must use game-relevant camera evidence; engine collision/import/performance remain separate gates.

## Authority chain applied locally

1. latest explicit project instruction / master production contract;
2. `AGENTS.md` and current project state/plan;
3. `design/EXOVANT_BIBLIA.md` + `design/EXOVANT_DATA.json` for Pelagos canon;
4. `docs/ART_PRODUCTION.md` + `docs/DEVELOPMENT_PROTOCOL.md`;
5. project learning events with their stated generalization boundaries;
6. world-local ADRs and manifests in this branch;
7. implementation.

## Collision audit

Before building, the connected surfaces showed active 3D world projects for Terra, Ares IX, Khepri and Vanta. No Pelagos project existed. GitHub search after the claim found only branch `art/world-pelagos-thalassa-001` for `pelagos`, and no Pelagos PR. Terra PR #1 reserves its own art paths and is explicitly excluded here.
