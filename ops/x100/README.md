# ops/x100

Generated/operational surfaces for `EXOVANT-X100-V2`.

- `GOAL.json`: canonical North Star/subgoals/checkpoints for the protocol migration.
- `config.json`: exact optimizer weights, gates and fidelity rules.
- `bootstrap-branch-index.json`: one-time live GitHub branch snapshot used to prove full non-main branch coverage at protocol creation; branch semantics are inferred and tagged, not authoritative.
- `spatial-index.json`: generated later by `python3 tools/x100_spatial.py build` from the checkout's fetched refs + `ops/fleet/registry.json`; this is a projection and should be regenerated after meaningful branch/claim changes.

Do not edit Fleet ownership through this folder. Do not treat vectors as canon. Unknown physical coordinates remain unknown.
