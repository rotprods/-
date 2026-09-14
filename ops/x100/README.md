# ops/x100

Generated/operational surfaces for `EXOVANT-X100-V2`.

- `GOAL.json`: canonical North Star/subgoals/checkpoints for the protocol migration.
- `config.json`: exact optimizer weights, gates and fidelity rules.
- `x100_control.py`: multiplicative world completeness, adaptive bottleneck gradient, candidate ranking and family DoD.
- `x100_spatial.py`: 64D spatial-semantic branch/claim projection with provenance and explicit unknown coordinates.
- `x100_director.py`: 84-cell evidence aggregation + 12-world portfolio gradient. It never mutates Fleet.
- `receipts/bootstrap/`: conservative PR-backed adoption seed; replace/extend through versioned owner receipts.
- `portfolio-opportunities.json`: evidence-linked candidate waves scored by gradient + value/cost/slop factors.
- `portfolio-wave-001.json`: first global 12-world lower-bound baseline and ranked production wave.
- `tests/test_x100.py` / `tests/test_x100_director.py`: deterministic control-plane gauntlet tests.
- `bootstrap-branch-index.json`: one-time live GitHub branch snapshot used to prove full non-main branch coverage at protocol creation; branch semantics are inferred and tagged, not authoritative.
- `spatial-index.json`: generated later by `python3 ops/x100/x100_spatial.py build` from fetched refs + `ops/fleet/registry.json`; projection only.
- `world-density-baseline.json`: generated lower-bound portfolio projection; do not hand-edit or confuse it with canon.

Do not edit Fleet ownership through this folder. Do not treat vectors, bootstrap receipts or diagnostic geomeans as canon/world-completion. Unknown physical coordinates remain unknown.
