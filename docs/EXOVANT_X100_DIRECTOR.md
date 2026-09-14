# EXOVANT-X100 V2 — Global Density Director

Status: protocol component. It becomes default only when the containing X100 V2 PR is merged to `main`.

## Purpose

`x100_control.py` answers **how incomplete is one world and which candidate is valuable?**  
`x100_spatial.py` answers **what branches/claims are nearby semantically/spatially?**  
`x100_director.py` answers **what does the whole 12-world portfolio need next, based only on evidence?**

The Director never claims work. Fleet remains the exclusive ownership/collision authority.

## 84-cell evidence contract

Every world is represented by 14 multiplicative dimensions × 6 canonical coverage cells = **84 evidence cells**.

A cell can only advance through an evidence receipt. Supported maturity levels are conservative lower bounds:

`unknown=0.00 → planned=0.05 → implemented=0.20 → locally_validated=0.40 → systemic_complete=0.55 → empirically_qualified=0.65 → human_approved=0.82 → production_complete=0.95 → released=1.00`

Non-unknown maturity requires one or more durable `evidence_refs`.

If two receipts touch the same cell, the strongest evidenced maturity is used and both receipts remain attached for provenance. Duplicate cells inside one receipt are rejected.

## Three numbers, never confuse them

- `strict_score_pct`: weighted multiplicative world completeness. If a multiplicative dimension is zero, strict score stays zero.
- `known_evidence_geomean_pct`: diagnostic maturity of what has actually been evidenced. **Not world completion.**
- `evidence_cell_coverage_pct`: how much of the 84-cell matrix has any non-zero evidence. **Not quality.**

This separation prevents a technically strong blockout from being mislabeled “80% AAA”.

## Portfolio gradient

Raw bottleneck pressure is computed from the same adaptive gradient as X100 V2. It is then combined with opportunity factors:

positive: `critical_path, dependency_unlock, player_visibility, reuse_value, art_importance, systemic_yield, gameplay_value, evidence_confidence, image_grounding_bonus`

negative: `collision_risk, unresolved_dependency, slop_risk, technical_cost`

`claimed_by_other` and irreversible blockers remain hard fences. The scorer can recommend a cell; it cannot bypass Fleet.

## Bootstrap Wave 001

Bootstrap receipts are a conservative snapshot derived from current open PR evidence. They are intentionally incomplete. Branch owners replace or extend them with versioned X100 receipts on their normal handoff; no heartbeat spam or background watcher is required.

`portfolio-wave-001.json` stores the resulting first 12-world baseline and weighted opportunity ranking.

The bootstrap is expected to report `strict_score_pct=0` for every world until every multiplicative dimension has non-zero evidence. That is a feature, not a failure.

## Default loop after merge

```text
RESYNC
→ X100_SPATIAL_BUILD
→ FLEET_PREFLIGHT
→ INGEST_X100_RECEIPTS
→ DIRECTOR_BASELINE
→ WORLD_GRADIENT
→ PORTFOLIO_OPPORTUNITY_SCORE
→ ELIGIBLE_GAPS
→ CLAIM
→ LOOK_LOCK_IF_REQUIRED
→ BUILD_FAMILY
→ GAUNTLET
→ RECEIPT
→ DIRECTOR_RECOMPUTE
→ NEXT
```

## CLI

```bash
python3 ops/x100/x100_director.py \
  --catalog design/EXOVANT_DATA.json \
  --config ops/x100/config.json \
  --fleet ops/fleet/registry.json \
  --receipts-dir ops/x100/receipts/bootstrap \
  --opportunities ops/x100/portfolio-opportunities.json \
  --out ops/x100/world-density-baseline.json
```

For production, prefer sharded receipts in owned paths and aggregate them into a checkout before Director execution. Bootstrap receipts exist only to seed V2 adoption.

## Image → polygon relation

Image grounding is a **bonus, not a shortcut**. Tier S/A or identity-critical opportunities can receive `image_grounding_bonus`, but final acceptance still requires the V2 fidelity route:

`LOOK_LOCK → IMAGE_TARGET_APPROVAL → IMAGE_TO_3D_BASE → GEOMETRY_CAUSALITY → CLEANUP/RETOPO → UV/PBR → LOD/COLLISION → ENGINE_IMPORT → VISUAL_REGRESSION → RECEIPT`

A raw AI/reconstruction mesh cannot advance a final asset cell beyond the evidence its cleanup/runtime receipts actually prove.
