# EDEN — ARENA STATE GRAPH v0.2

Cell: `ART-ELYSIUM-001`
Remote Blender qualified revision: `5`
Status: `PROPOSAL / BLENDER MOTION + COLLISION CANDIDATE`

## Canon anchors

The following are already present in project canon and are not invented by this cell:

- EDEN arena is a **48 m diameter geometric garden**.
- Arena modules can change position between attacks.
- Minimum corridors must remain guaranteed.
- `Reubicación` displays module destination for **1.5 seconds** before the player must leave the trajectory.
- `Poda perfecta` aligns for 0.9 s.
- `Abrazo de servicio` exposes open hands for 1.1 s.

This graph addresses the spatial, collision and editable-animation foundation for `Reubicación`. It is still **not** target-engine boss implementation.

---

## Module footprint proposal

Four current garden modules use **8 × 8 m** visible footprints. This is a reversible W1 proposal.

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

Visible amber destination footprints remain diagnostic/readability geometry, not final VFX.

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

Current candidate minimum axis-aligned corridor across states A/B/C: **6 m**.

Static comparison against the current executable prototype now exists:

- player capsule: radius `0.38 m`, height `1.85 m`;
- standard enemy capsule: radius `0.40 m`, height `1.80 m`;
- current boss capsule: radius `1.10 m`, height `5.80 m`.

The 6 m arena corridor therefore has ample **static geometric** clearance for the current player and standard enemy body sizes. This does not qualify dodge arcs, combat camera, moving obstacles, accessibility, collision margins or target-runtime navigation.

---

# Architecture-clearance side result

The W1 architecture candidate uses a `2.4 × 2.7 m` clear door.

Against the current prototype player capsule:

- player diameter: `0.76 m`;
- total horizontal slack: `1.64 m`;
- per-side slack when centered: `0.82 m`;
- vertical headroom: `0.85 m`.

Status: `PASS_STATIC_GEOMETRY_ONLY`.

The current boss body is intentionally too tall to traverse that human-scale door. Native traversal remains required before the door/grid can be promoted to production standard.

---

# Blender Reubicación timeline — revision 5

24 fps timeline:

```text
frames 1–24   STABLE_A
frames 25–60  TELEGRAPH_B       36 frames = canonical 1.5 s
frame 61      MOVEMENT_START
frames 61–84  MOVING_A_TO_B     24 frames = proposed 1.0 s
frames 84–108 STABLE_B
```

Measured roots:

```text
f24 / f42 / f60 / f61 = State A exactly
f72 = x approximately ±11.87 m
f84 / f96 = State B exactly at x ±14 m
```

The movement duration is a **PROPOSAL**, deliberately separate from the canonical warning duration.

---

# Physical actuation candidate

Revision 5 contains a first manufacturing-readable mechanism:

- one kinematic root per garden module;
- 2-axis linear actuator sled under each module;
- orthogonal X/Y subfloor guide rails covering A/B/C envelopes;
- service node per module;
- static rails remain floor infrastructure while the sled/garden follows its root.

This replaces the cheap interpretation of `Reubicación` as geometry teleportation. The final technology can change after art/gameplay review, but any replacement must still explain the physical movement.

---

# Geometry / collision separation

Revision 5 now separates, per garden module:

1. visible base/soil/topiary;
2. `GAMEPLAY_BASE_PROXY` — `7.6 × 7.6 × 1.35 m` simplified box;
3. `GAMEPLAY_TOPIARY_PROXY` — approximately `2.7 × 2.7 × 2.8 m` cylinder envelope;
4. diagnostic destination/telegraph geometry;
5. static rail/service mechanism.

Stable collision asset IDs:

```text
ELYS-COL-EDN-00-BASE
ELYS-COL-EDN-00-TOP
ELYS-COL-EDN-01-BASE
ELYS-COL-EDN-01-TOP
ELYS-COL-EDN-02-BASE
ELYS-COL-EDN-02-TOP
ELYS-COL-EDN-03-BASE
ELYS-COL-EDN-03-TOP
```

The collision objects are hidden from beauty render and remain a Blender/export contract pending engine integration.

---

# Hierarchy defect caught by QA

The first committed motion candidate (revision 4) exposed a real hierarchy defect: existing visible garden children were double-transformed after parenting to moving roots. Example: intended `(-10,101)` appeared at `(-20,202)` while collision stayed correct.

Revision 5 fixes the contract by using explicit local child coordinates under each root:

- visible base local Z = `0.80 m`;
- soil local Z = `1.54 m`;
- topiary local Z = `3.00 m`;
- actuator sled local Z = `0.22 m`;
- collision base local Z = `0.80 m`;
- collision top local Z = `3.00 m`.

Verification at State A and State B shows each visible base and base collision proxy at the same XYZ world position, difference `[0,0,0]` for all four modules.

The earlier failed Blender operation caused by the Blender 5.2 animation API was also preserved in the machine-readable receipt; it produced no committed revision.

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

High-level transition:

```text
STABLE_A
  -> TELEGRAPH_B [1.5 s canonical warning]
  -> MOVING_A_TO_B [1.0 s current proposal]
  -> STABLE_B
  -> TELEGRAPH_C
  -> MOVING_B_TO_C
  -> STABLE_C
```

The engine is free to tune movement duration after gameplay validation; the 1.5 s warning must remain the canon anchor unless the project authority changes it.

---

# Readability contract

A state change must communicate through at least two channels where possible:

- destination footprint / spatial cue;
- visible actuator or module preparation;
- audio/mechanical cue;
- floor/service-path change.

Do not rely only on color.

---

# Acceptance path

This candidate can move from `BLENDER MOTION + COLLISION CANDIDATE` to `GAMEPLAY CANDIDATE` only after:

- [x] 48 m arena dimensional check.
- [x] all candidate module corners remain within arena radius.
- [x] three explicit layouts.
- [x] proposed corridor width measured.
- [x] destination-target objects generated.
- [x] movement mechanism designed at candidate level.
- [x] separate collision proxies generated.
- [x] canonical 1.5 s warning represented distinctly from movement in Blender timeline.
- [x] moving-root hierarchy verified after fixing transform defect.
- [ ] actual state transition implemented in target engine.
- [ ] native player traversal test.
- [ ] combat camera test.
- [ ] `Reubicación` 1.5 s readability test in engine.
- [ ] nav-obstacle update strategy implemented.
- [ ] performance/nav update measurement.
- [ ] GATE-ART review.

Machine-readable receipt: `evidence/eden_collision_motion_validation.json`.
