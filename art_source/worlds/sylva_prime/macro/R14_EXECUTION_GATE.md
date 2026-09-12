# R14 EXECUTION GATE — SYLVA PRIME MACRO

Claim: `CLM-SYLVA-MACRO-001`  
Primary remote: `05dce898-753d-4ff6-a4b0-31757dc868d8`  
Accepted remote revision: **13**  
Fence: `SYLVA-MACRO-WRITER-EPOCH-2-20260912`

## Current state

`FROZEN_PENDING_FLEET_ACTIVE`

No mutation of the primary Blender project is allowed while published `main:ops/fleet/registry.json` reports this claim as `reserved` or `ack:null`.

## Ready work

R14 has already been designed and statically validated without Blender mutation:

- `STREAM_HIERARCHY_R14_PROPOSAL.json`
- `build_stream_hierarchy_r14.py`
- `validate_stream_hierarchy_r14.py`
- `qa/R14_STREAM_HIERARCHY_PREFLIGHT.json`

Target contract: `SYLVA_STREAM_HIERARCHY_R14`.

## Required activation sequence

1. Read latest `main` and `ops/fleet/registry.json`.
2. Verify `CLM-SYLVA-MACRO-001.status == active`.
3. Verify ACK owner `AGENT-SYLVA-MACRO-01`, epoch matches current claim.
4. Verify primary project ID `05dce898-753d-4ff6-a4b0-31757dc868d8` is registered.
5. Read `REMOTE_WRITER_FENCE.json` and claim file on the producer branch.
6. Establish exactly one writer session for the wave.
7. Read remote project and require: revision 13, sceneSequence 0, no active operation.
8. Re-run the R14 read-only preflight if branch or remote revision changed.
9. Execute `build_stream_hierarchy_r14.py` as one coherent mutation.
10. QA hierarchy, neighbor symmetry, hero residency overlays and zero geometry delta.
11. Persist receipt/status/handoff before handing writer epoch to another session.

## R14 invariant

R14 is metadata/hierarchy only. It must **not**:

- move Puerto, Bosque or VESPER;
- alter terrain/routing/collision geometry;
- generate HLOD geometry;
- select a Godot/Unreal streaming backend;
- instantiate PR #6 root modules;
- mutate orbital project `c796230b-0463-4e17-9446-2e746c5c4933`.

Bosque's hero core naturally crosses all four L2 supercells. The correct response is an explicit hero-residency overlay, not a geography change.
