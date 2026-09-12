# EDEN — ARENA STATE GRAPH v0.1

Cell: `ART-ELYSIUM-001`
Remote Blender revision: `3`
Status: `PROPOSAL / STRUCTURAL CANDIDATE`

## Canon anchors

The following are already present in project canon and are not invented by this cell:

- EDEN arena is a **48 m diameter geometric garden**.
- Arena modules can change position between attacks.
- Minimum corridors must remain guaranteed.
- `Reubicación` displays module destination for **1.5 seconds** before the player must leave the trajectory.
- `Poda perfecta` aligns for 0.9 s.
- `Abrazo de servicio` exposes open hands for 1.1 s.

This state graph only addresses the spatial foundation for `Reubicación`. It is not the final boss encounter implementation.

---

## Module footprint proposal

Four current garden modules are represented as **8 × 8 m** footprints. This dimension is a W0/W1 proposal and can change if combat/camera tests demand it.

Canonical arena radius: `24 m`.

---

## State A — initial cross

Module centers in world XY:

```text
(-10, 101)   (10, 101)
(-10, 115)   (10, 115)
```

Relative to arena centre `(0,108)`:

```text
(-10,-7)   (10,-7)
(-10,+7)   (10,+7)
```

Structural checks:

- maximum module-corner radius: `17.804 m`;
- inside 24 m arena radius: PASS;
- central vertical corridor: `12 m`;
- central horizontal corridor: `6 m`;
- minimum axis corridor: `6 m`.

---

## State B — lateral correction

Module centers:

```text
(-14, 101)   (14, 101)
(-14, 115)   (14, 115)
```

Structural checks:

- maximum module-corner radius: `21.095 m`;
- inside 24 m arena radius: PASS;
- central vertical corridor: `20 m`;
- central horizontal corridor: `6 m`;
- minimum axis corridor: `6 m`.

State B currently has visible amber destination footprints in Blender revision 3. These are **debug/readability geometry**, not final VFX.

This is the first physical representation of the canonical `Reubicación` rule: the player can see where a module intends to arrive before displacement occurs.

---

## State C — longitudinal correction

Module centers:

```text
(-10, 97)   (10, 97)
(-10,119)   (10,119)
```

Structural checks:

- maximum module-corner radius: `20.518 m`;
- inside 24 m arena radius: PASS;
- central vertical corridor: `12 m`;
- central horizontal corridor: `14 m`;
- minimum axis corridor: `12 m`.

---

# Proposed corridor contract

Current candidate minimum axis-aligned corridor across states A/B/C:

**6 m**.

This is not canon and is not yet qualified. Promotion requires testing with:

- real player capsule;
- dodge/sprint motion;
- camera boom;
- representative EDEN attack collision;
- enemy/boss body clearances;
- accessibility route requirements;
- target-engine collision margins.

If any fail, the state graph changes before the corridor value is promoted.

---

# Runtime state contract — proposal

Each moving module should expose at minimum:

```text
module_id
current_state
source_transform
target_transform
preview_transform / footprint
telegraph_started_at
telegraph_duration
movement_started_at
movement_duration
collision_mode
nav_update_policy
```

Suggested high-level transition:

```text
STABLE_A
  -> TELEGRAPH_B [1.5 s canonical warning]
  -> MOVING_A_TO_B
  -> STABLE_B
  -> TELEGRAPH_C
  -> MOVING_B_TO_C
  -> STABLE_C
```

The canonical 1.5 s value belongs to the visible destination warning for `Reubicación`; movement duration remains unresolved and must be tuned through combat tests rather than assumed equal to telegraph duration.

---

# Geometry / collision separation

Final production should separate:

1. visible garden body;
2. simplified collision body;
3. target/telegraph representation;
4. nav-obstacle representation;
5. service/VFX sockets.

Do not move detailed plant geometry as the only source of gameplay collision.

---

# Readability contract

A state change must be readable through at least two channels where possible:

- destination geometry/light cue;
- module motion preparation;
- audio/mechanical cue;
- floor/service-path change.

Do not rely only on color because encounter comprehension must survive color-vision variance and visual noise.

---

# Anti-cheapness rule

`Reubicación` must not look like geometry teleporting to create difficulty. The architecture should imply a real actuation system—subfloor rails, magnetic/linear actuators, telescoping service roots or another coherent mechanism selected later.

That mechanism becomes part of manufacturing realism and must be visible enough that a player can believe the arena was built to reconfigure.

---

# Acceptance path

This candidate can move from `STRUCTURAL CANDIDATE` to `GAMEPLAY CANDIDATE` only after:

- [x] 48 m arena dimensional check.
- [x] all candidate module corners remain within arena radius.
- [x] three explicit layouts.
- [x] proposed corridor width measured.
- [x] destination-target objects generated.
- [ ] movement mechanism designed.
- [ ] collision proxies generated.
- [ ] actual state transition implemented in target engine.
- [ ] player controller traversal test.
- [ ] combat camera test.
- [ ] `Reubicación` 1.5 s readability test.
- [ ] performance/nav update measurement.
- [ ] GATE-ART review.
