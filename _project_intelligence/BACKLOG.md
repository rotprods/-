# Dependency-aware frontier

The global plan remains `design/EXOVANT_BIBLIA.md`. World and mission catalog entries retain PROPOSED status until their actual implementation meets acceptance. Do not label all five Terra missions complete because the prototype contains a condensed chain.

| ID | Increment | Depends on | Acceptance |
|---|---|---|---|
| EXO-004 | Complete playability route, input and guidance | Current prototype | Start a fresh game, walk every route without teleports/debug progression, solve puzzle, win or lose/recover, decide and return. Record friction and fix blockers. Add gamepad/remapping with parity checks. |
| EXO-005 | Player combat and animation pass | 004 | Authored readable anticipation/recovery, attack and dodge cancel policy, second weapon family, hit feedback, audio events, combat drill with recorded inputs. |
| EXO-006 | Portal asset production pass | Current GLB + runtime | Retain original source, reduce draw calls/material duplication, UV/texture/LOD as appropriate, explicit collision asset, compare visuals and target performance. |
| EXO-007 | Terra art direction proof | 004 + 006 | One short route with coherent bronze/basalt/ivory, plausible scale, vegetation, lighting and final character target. Review in engine, not only as concept images. |
| EXO-008 | ATLAS authored encounter | 005 + 007 | Six to eight attacks, three genuinely distinct phase rules, non-destructive isolation route, tested cover/camera/weapon parity. |
| EXO-009 | Archive route alternatives | 004 | Roof, lock and negotiated routes; evidence integrity, debt and nursery flags; save/reload at each transition. |
| EXO-010 | Ecology and consequences | 009 | At least three regional changes visible in routes, NPC behavior and services; no mere palette swap as final consequence. |
| EXO-011 | Rover physics and accessibility | 004 | Mount/dismount collision clearance, controller support, slopes/water behavior and reliable save/reset. |
| EXO-012 | Production engine decision | 006 + 007 + runnable target host | Same representative scenario measured in the chosen native engine; document build, frame-time, memory and workflow. No automatic migration based on tool availability alone. |
| EXO-013 | 30–45 minute Terra slice | 005–012 | Complete region, three enemy archetypes, three NPC arcs, two weapons, one vehicle, one minigame, ATLAS and persistent consequence; human playtest gates from the plan. |
| EXO-014 | Planetary travel framework | 013 | Explicit domain transitions, ship cabin/map, save across travel, bounded scene streaming; no runtime external content dependency. |
| EXO-015 | Ares IX chapter | 014 | Unique world rule, assets, missions, ecology, MOL-9 and outcome with regressions. |
| EXO-016 | Remaining Milky Way chapters | 015 + production review | Pelagos and Umbra meet the same chapter gate and add mechanically distinct systems. |
| EXO-017 | Andromeda chapters | 016 | Sylva Prime, Khepri, Nacre and Vanta, staged one chapter at a time. |
| EXO-018 | Extragalactic final act | 017 | Aurora Veil, Leviathan, Elysium Null and Origin with full campaign consequence resolution. |
| EXO-019 | Release qualification | Full campaign + platform targets | Localisation, options, controller parity, save migration, licensing, target performance, packaging, external playtests and release criteria. |

DLSS work starts only when an actual compatible engine plugin, NVIDIA hardware and target platform are available. It is not a substitute for base frame-time performance. Multiplayer, PvP and MMO remain outside the first campaign scope in the plan.

At every activation, reconstruct state and select the highest-impact unresolved dependency. Correct regressions before adding content. Preserve the original twelve-world vision while keeping each implementation wave small enough to qualify and hand off.
