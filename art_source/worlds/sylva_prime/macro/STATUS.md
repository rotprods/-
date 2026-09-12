# STATUS — CLM-SYLVA-MACRO-001

**Agent:** `AGENT-SYLVA-MACRO-01`  
**Session:** `20260912-SYLVA-MACRO-001`  
**Branch:** `art/world-sylva-prime-macro-001`  
**Remote Blender:** `05dce898-753d-4ff6-a4b0-31757dc868d8` @ revision `3`  
**State:** `IN_PROGRESS / VERIFIED CHECKPOINT`

## Coverage

| Task | Priority | State | Receipt |
|---|---|---|---|
| SYLVA/MACRO/001 Evidence pack | P0 | DONE | claim + draft PR #3 |
| SYLVA/MACRO/002 Coordinate/scale contract | P0 | DONE | Blender root metadata + World Bible |
| SYLVA/MACRO/003 World-bible delta | P0 | DONE | `WORLD_BIBLE_MACRO.md` |
| SYLVA/MACRO/004 Macro terrain | P0 | DONE (BLOCKOUT) | Blender r3 + generator |
| SYLVA/MACRO/005 Structural root network | P0 | REVIEW | 6 primary + 8 secondary roots; human art review pending |
| SYLVA/MACRO/006 Puerto del Injerto | P1 | REVIEW | regional proxy foundation present |
| SYLVA/MACRO/007 Bosque de las Frases | P1 | REVIEW | 3 geometrically distinct route families present |
| SYLVA/MACRO/008 Cámara de VESPER envelope | P1 | REVIEW | boss-space envelope; no final boss asset |
| SYLVA/MACRO/009 Traversal / scale / collision QA | P0 | IN_PROGRESS | numeric/export QA pass; engine traversal/collision pending |
| SYLVA/MACRO/010 Export + handoff | P0 | IN_PROGRESS | `.blend` + GLB r3 + validation; engine import/human review pending |

## Progress metrics

Percentages below are **stage estimates for this atomic macro claim**, not global game progress.

- Asset-family blockout presence: **100%** of declared macro families have a proxy/foundation.
- Modeling maturity: **40%** — macro/blockout only; no production sculpt/topology/UV pass.
- Materials maturity: **10%** — 8 diagnostic PBR materials; no final texture sets.
- Optimization maturity: **15%** — triangle/object metrics exist; no target-hardware profiling/LOD implementation.
- Integration maturity: **25%** — portable GLB generated; no Godot/Unreal import gate yet.
- QA maturity: **45%** — namespace/transforms/scale/export/scope guards pass; human art, engine, collision and performance gates pending.

## Current scene receipts

- 100 objects.
- 76 mesh objects.
- 8 curve objects.
- 8 diagnostic materials.
- ~15,052 blockout triangles.
- Local terrain bounds: 12,000 × 12,000 m; ~828.9 m vertical span.
- 6 primary structural roots + 8 secondary roots.
- 4 diagnostic route guides at proposed 6 m width.
- Region straight-line spacing: Puerto→Bosque 3,970.25 m; Bosque→VESPER 3,897.10 m; Puerto→VESPER 7,842.99 m.
- No objects outside `SYLVA_` namespace.
- No non-unit-scale objects in final r2 QA query.
- No final Edda/Siete/Nico/VESPER asset accidentally created.
- Unsupported portable light types after r2: none.
- `.blend` r3: 1,897,056 bytes, etag `ffd2e7ad0ac1f97b5e5908ab3c569394`.
- GLB r3: 1,013,560 bytes, etag `d07f51362f8c6c9a29cc3ec03661b0d4`.

## QA notes

- A four-render r3 mutation timed out at 300 s and produced no commit. This failure is preserved in `validation.json`.
- Direct `Render Result` pixel reads returned a false all-zero result. Independent PNG-byte decoding of a 160×90 Puerto render returned mean 20.4967, variance 254.9406, range 0–249: file is nonblank.
- Visual quality is **not approved**: current client cannot visually inspect the published render.
- The interactive GLB scene is exposed for human inspection via the 3D Jutsu project.

## Open priorities

### P0
1. Import GLB into the actual runtime target and test scale/traversal/collision.
2. Human art-direction review from game camera / regional cameras.
3. Decide or explicitly defer planetary radius via ADR before L1 orbital work.
4. Define target hardware before meaningful performance budgets/LOD thresholds.

### P1
1. Approve/revise Puerto silhouette and graft interface.
2. Approve/revise Bosque route readability without color-only dependence.
3. Approve/revise VESPER chamber envelope and camera clearances.

## Claim

`KEEP` — macro foundation still has P0 gates open and must not be released as DONE.
