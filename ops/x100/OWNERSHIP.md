# EXOVANT-X100 V2 protocol ownership

Owner cell: `AGENT-OPS-X100-V2`
Branch: `ops/exovant-x100-v2`
Base at claim: `main@26ae20f5d1b47d1efa0d54b20124ed93cbc0b43e`
Coordination receipt: issue #7 comment `5655133582`

Scope: protocol/tooling only. No world, region, Blender project, asset ID, gameplay system or producer path is owned by this cell.

Owned new paths:
- `docs/EXOVANT_X100_V2.md`
- `ops/x100/`

Bounded shared integration paths:
- `AGENTS.md`
- `docs/DEVELOPMENT_PROTOCOL.md`
- `docs/PROTOCOLS.md`
- generated `MANIFEST.json` refresh required for merge

Explicit exclusions: producer art branches, Fleet transitions on behalf of owners, STATE/PLAN replacement, canonical Graphify schema mutation, Blender scene mutation, asset production.

Control-plane decision: optimizer, spatial projection and tests live under `ops/x100/`, intentionally outside `tools/` and root `tests/`, so protocol-only changes do not invalidate Godot runtime source evidence.

Status: `PROTOCOL_CANDIDATE`; becomes default only after merge/readback from `main`.
