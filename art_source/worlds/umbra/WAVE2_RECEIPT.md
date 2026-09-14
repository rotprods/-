# UMBRA WAVE 2 RECEIPT

Status: `WAVE2_ENVIRONMENT_PRODUCTION_FOUNDATION / REPRODUCIBLE / NOT FINAL AAAA`

Primary project: `7ab99682-8777-4143-8ae0-1fbb178ccafb`  
Replay project: `7f33ae14-540c-4af5-8131-1490465fe6cc`

## Scope

Wave 2 remains inside the reversible 1200×700 m L2 testbed. It does not invent physical planet size/global geology, final NOCTIL anatomy/rig/attacks, runtime quest logic, final PBR/UV, collision or LOD budgets.

Implemented:
- refuge structural/thermal/logistics foundation: portal ribs, rails, replaceable wind baffles, sealed airlock, external thermal modules, heat fins/service trunks, cargo dock and refuge beacons;
- M01 environmental interface: thermal anchors, physical track scars and lee shelters;
- M02 environmental interface: occlusion fins, exposure corridor edges and future reflector-control plinth;
- M03 environmental interface: exclusion archive shell, evidence slabs and caches without inventing narrative record content;
- M04 environmental approach: ascent platforms, markers/spine and crown threshold, stopping before final NOCTIL entity.

Initial QA found five tilted refuge baffles penetrating terrain by ~0.33 m and M01/M02/M04 camera clipping. These were corrected before acceptance: baffles were seated at +0.05 m and all four mission QA cameras contain their required anchors.

## Final Wave-2 checkpoint

Checkpoint: `WAVE2_REFUGE_QUESTCELLS_OPT_001`

- objects: `552`;
- mesh objects: `536`;
- materials: `10`;
- evaluated triangles: `44,616`;
- residual bad scales: `0`;
- zero-dimension meshes: `0`;
- Wave-1 reflector/caravan/refuge contact set preserved;
- five Wave-2 baffles: `+0.05 m` authored contact clearance;
- M01/M02/M03/M04 semantic-anchor framing: PASS.

## Exact mesh-data sharing

Repeated mechanical/environment primitives share mesh datablocks only when topology, local coordinates, material assignment, smoothing, material list, UV names/values and mesh custom properties are equivalent. Shape-key meshes or unfamiliar non-internal custom attributes are refused. Object count, transforms and evaluated triangle count remain unchanged.

## Independent replay

The clean replay reproduced the Wave-2 structural/semantic contract from the independently reconstructed Wave-1 input:
- 552 objects;
- 536 mesh objects;
- 10 materials;
- 44,616 evaluated triangles;
- zero bad scales / zero degenerate meshes;
- same contact contract;
- same M01–M04 camera contract;
- same quest-cell structure and exact-linking policy.

Binary `.blend`/GLB hashes are not used as the semantic equality gate because provider/container metadata can differ. Provider-independent binary custody remains separately blocked under MR-EXO-001.

## Acceptance limits

Wave 2 does not claim final pixel-level art approval, final runtime behavior, final UV/PBR, collision/LOD/HLOD/GPU acceptance, planet-scale coverage or final NOCTIL design.
