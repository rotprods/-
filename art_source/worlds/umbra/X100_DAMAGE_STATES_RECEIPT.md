# UMBRA X100 DAMAGE / ABANDONMENT STATE RECEIPT

Scope: `W04-X100-DAMAGE-REPAIR-STATES`  
Status: `STATE_FOUNDATION / QA-PASS / NOT FAMILY_COMPLETE`

The service ecosystem previously exposed three active-life states: `SERVICED`, `USED`, `FIELD_REPAIRED`.

This pass adds two causal late-life states across all ten systemic families:

- `DAMAGED`
- `ABANDONED`

No random grunge, arbitrary destruction, noise decals or generic debris field is used. Each family has a distinct physical failure mechanism.

## Authored expansion

- 10 families;
- 3 size classes (`S/M/L`);
- 2 new late-life states;
- 60 new prefab roots total;
- 30 `DAMAGED` + 30 `ABANDONED`;
- six new roots per family.

The total service-state vocabulary is now:

`SERVICED | USED | FIELD_REPAIRED | DAMAGED | ABANDONED`.

## Failure modes

| Family | DAMAGED | ABANDONED |
|---|---|---|
| Tool case | impact distorts lid alignment and latch | open case, failed latch, collapsed handle |
| Cable reel | side-frame impact misaligns cheek/hub | missing hub + collapsed side frame |
| Storage | corner impact removes protector/racks lid | open container after corner failures |
| Power box | service-door strike + fin/port damage | disconnected cabinet, open/fallen door, missing cooling parts |
| Heat exchanger | windborne impact bends/removes fins | isolated core with major fin loss |
| Winch | overload deforms guide/drum cheek | lost guide, displaced motor, collapsed cheek |
| Lamp | shield/cage impact | emitter missing, mast/shield bent and unpowered |
| Textile bundle | strap failure shifts roll under wind load | unstrapped roll displaced by persistent lateral wind |
| Service stand | overload bends one leg/foot | partial collapse after load-path failure |
| Wayfinding marker | upper marker racked while anchor remains intact | upper marker fails at anchor interface while base stump remains seated |

This yields 20 distinct documented failure modes, two per family.

## Blender checkpoint

Primary project: `7ab99682-8777-4143-8ae0-1fbb178ccafb`  
Revision: `9`  
Checkpoint: `X100_DAMAGE_STATES_FOUNDATION_001`

Post-pass scene:
- objects: `2,009`;
- mesh objects: `1,800`;
- evaluated triangles: `71,940`;
- active mesh datablocks: `340`;
- multi-user mesh datablocks: `226`;
- maximum users on one mesh: `36`;
- bad residual scales: `0`;
- zero-dimension meshes: `0`.

## Terrain-contact QA

Every bbox corner of every child mesh in the 60 new prefab roots was compared against local terrain.

- global minimum clearance: `+0.005 m`;
- no prefab root had child geometry below `-0.12 m` terrain tolerance;
- no prefab root had its minimum clearance above `+0.20 m`;
- therefore no late-life state is accepted as floating or materially embedded at this checkpoint.

## Completeness impact

Planning-only multiplicative factors are updated after this pass because it directly raises temporal depth, causal material history, variation and physical storytelling. It does not alter blocked ecology or planet-scale factors.

Estimated normalized multiplicative completeness after this pass: approximately `30.46%` → still `PLAYABLE_FOUNDATION`.

## Remaining family-complete gates

The service families are not `FAMILY_COMPLETE` until UV0/texel-density, final PBR state masks, collision, runtime import, validated LODs, direct art review and durable binary custody pass their independent gates.
