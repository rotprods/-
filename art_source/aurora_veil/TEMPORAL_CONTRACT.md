# AURORA VEIL — BOUNDED TEMPORAL CONTRACT v1

**Owner:** `AGENT-02-AURORA`  
**Claim:** `CLM-AURORA-WORLD-001`  
**Task:** `AUR/TEMPORAL/007`  
**Remote proof:** Blender rev 12  
**Truth:** production interface candidate; runtime implementation remains blocked by engine interface.

## Canon boundary

CANON from the Aurora world design:

- temporal echoes repeat actions only in small areas and bounded intervals;
- the whole world is never rewound;
- state rules must remain stable/readable;
- AEON arena has exactly three primary echo sectors and one visible delay rule per sector;
- combat timing outside these local mechanics is not silently altered.

PROPOSAL / prototype values:

- field delays: 1.0 s / 1.4 s / 1.8 s;
- cue lead: 0.80 s / 1.05 s / 1.25 s;
- active windows: 0.55 s / 0.65 s / 0.75 s;
- AEON sector delays: 0.9 s / 1.2 s / 1.5 s.

These numbers require gameplay/human qualification before becoming final.

## State machine

Deterministic order:

`IDLE → PRE_CUE → REPEAT_ARMED → REPEAT_ACTIVE → COOLDOWN → IDLE`

### IDLE

- boundary visible but low salience;
- collision: NONE;
- no pending repeat action;
- leaving the encounter can safely reset here.

### PRE_CUE

- announces that a repeat will be armed;
- collision: NONE;
- cue MUST be shape/motion/audio readable, not color-only;
- Blender proof uses eight inward radial ticks.

### REPEAT_ARMED

- source action has been captured/selected;
- collision: NONE;
- Blender proof uses four raised gates to distinguish silhouette from PRE_CUE.

### REPEAT_ACTIVE

- exactly one bounded repeat is materialized;
- only this state may enable the local repeat collision proxy when gameplay requires physical occupancy;
- source and repeat are separate semantic objects;
- the field/world is never duplicated;
- repeated action must retain a visible trajectory/telegraph.

### COOLDOWN

- repeat finished;
- collision: NONE;
- cannot immediately arm again until local cooldown expires;
- Blender proof uses low segmented posts distinct from armed gates.

## Persistence contract

Field persistence:

`ENCOUNTER_LOCAL_RESET_ON_EXIT_OR_RELOAD`

Arena persistence:

`ARENA_LOCAL_ONLY`

Forbidden:

- global world rewind;
- writing temporal repeats into global save-state history;
- silently changing universal dodge/combat timing;
- duplicating actors/world geometry as a general rewind mechanism;
- enabling repeat collision outside `REPEAT_ACTIVE`.

## Stable field IDs

- `AUR-TMP-FIELD-A` — prototype delay 1.0 s;
- `AUR-TMP-FIELD-B` — prototype delay 1.4 s;
- `AUR-TMP-FIELD-C` — prototype delay 1.8 s.

Each field root owns:

- `delay_s`;
- `cue_lead_s`;
- `active_window_s`;
- `rule`;
- `state_order`;
- `persistence`;
- `save_state_mutation=FORBIDDEN`;
- `global_rewind=FORBIDDEN`;
- collision-owner collection.

## AEON arena sectors

Stable proof roots:

- `AUR-AEON-TMP-SECTOR-1_ROOT`;
- `AUR-AEON-TMP-SECTOR-2_ROOT`;
- `AUR-AEON-TMP-SECTOR-3_ROOT`.

Rules:

- exactly three primary sectors;
- `ONE_VISIBLE_DELAY_PER_SECTOR`;
- each sector has a distinct non-color geometric cue: 1 / 2 / 3 fins;
- collision proxies are separate, hidden, disabled by default and active only in `REPEAT_ACTIVE`;
- arena timeline never mutates global save state.

## Collision interface

Collection: `19_TEMPORAL_COLLISION_PROXIES`.

Prototype collision form: simple box.

Required runtime behavior:

```text
on state != REPEAT_ACTIVE:
    collision_proxy.enabled = false

on enter REPEAT_ACTIVE:
    collision_proxy.transform = authored_repeat_transform
    collision_proxy.enabled = authored_repeat_requires_collision

on exit REPEAT_ACTIVE:
    collision_proxy.enabled = false
```

The Blender proxy proves ownership/scale only. It does not claim a production engine collision implementation.

## Accessibility / anticipation

Every temporal interaction must expose at least two of:

- shape/silhouette change;
- motion/trajectory cue;
- audio cue;
- optional color/emissive cue.

Color alone is forbidden as the only state channel.

Runtime UX should expose an optional timeline/sector indicator for players who need explicit timing information.

## Runtime-neutral event interface

Candidate events:

```text
TemporalFieldEntered(field_id)
TemporalPreCueStarted(field_id, cue_lead_s)
TemporalRepeatArmed(field_id, source_action_id, delay_s)
TemporalRepeatActivated(field_id, source_action_id, repeat_instance_id)
TemporalRepeatEnded(field_id, repeat_instance_id)
TemporalCooldownStarted(field_id)
TemporalFieldReset(field_id, reason)
```

Candidate state payload:

```json
{
  "field_id": "AUR-TMP-FIELD-B",
  "state": "REPEAT_ACTIVE",
  "source_action_id": "runtime-owned-id",
  "delay_s": 1.4,
  "active_window_s": 0.65,
  "collision_required": true,
  "persistence": "ENCOUNTER_LOCAL"
}
```

No engine class, node type, physics layer or save-system API is prescribed until EXO-012/runtime authority resolves it.

## QA gates

PASS at Blender rev 12:

- 3 field roots;
- 5 state families present per field;
- legacy temporal blockout hidden from render, not destructively deleted;
- 3 field collision proxies + 3 AEON sector collision proxies;
- all proxies hidden from render and runtime-default disabled;
- field collision bound only to `REPEAT_ACTIVE`;
- global rewind FORBIDDEN;
- save mutation FORBIDDEN;
- three AEON sectors retained;
- GLB export succeeds.

OPEN:

- human comprehension test;
- sound cue implementation;
- runtime state-machine implementation;
- actual collision toggle integration;
- gameplay timing qualification;
- human art-direction approval.
