# KHEPRI Optical Geometry → Materials UV0 Handoff

Status: **AUTHORIZED BY GEOMETRY OWNER**  
Geometry claim: `CLM-KHEPRI-WMACRO-001`  
Material consumer: `CLM-KHEPRI-MATERIALS-001`  
Project: `040f0c45-83a7-483c-9ee7-1e31c640a587`  
Contract: `KHP_OPTICAL_UV0_HANDOFF_V1`

## Purpose
Close the UV0 interface blocker for the first real KHEPRI material consumer without transferring geometry ownership.

## Authorized geometry change
The geometry owner authorizes exactly one interface mutation on the shared heliostat mesh families:

- add/replace a deterministic UV layer named `UVMap`;
- apply the same metre-based mapping contract to LOD0, LOD1 and LOD2 source meshes;
- write UV metadata only.

No vertices, polygons, object transforms, silhouette, material-slot count/order, instancing topology or asset IDs may change.

## Mapping contract

- Projection: dominant polygon-axis object-space projection.
- Scale: **4 metres per texture repeat** (`0.25 UV units/metre`).
- Coordinate space: local mesh coordinates, so compact/standard/wide remain metrically compatible.
- Wrapping: repeating/tileable.
- Overlap: intentional across repeated/tileable surfaces.
- UV values may extend outside `[0,1]`; repeat sampling is the contract.

This UV0 is specifically for tileable family-base / manufacturing-finish material applications such as:

- `KHP_MAT_BRONZE_SYNOD_001::service_clean::cast_structural::architectural`
- `KHP_MAT_MIRROR_OPTICAL_001::calibrated::broad_reflector::architectural`

It is **not** an authorization to bake unique per-instance story masks into the same overlapping UV set.

## LOD policy
The exact same UV projection/scale rule applies to:

- six LOD0 mast/panel meshes;
- six LOD1 mast/panel meshes;
- six LOD2 mast/panel meshes.

This keeps material scale stable through LOD changes. Runtime LOD thresholds/HLOD remain outside this handoff.

## Acceptance gates

1. exact expected 18 mesh datablocks present;
2. every mesh has active `UVMap`;
3. UV loop count equals mesh loop count;
4. all UV values finite;
5. geometry semantic SHA before/after identical;
6. material slots before/after identical;
7. object instance count and transforms unchanged;
8. GLB export/import does not lose material resource sharing;
9. material pilot may bind materials only after this receipt passes.

## Nonclaims
This handoff does not authorize:

- geometry edits beyond UV data;
- unique hero UVs;
- per-instance damage masks;
- final texel density;
- target-hardware memory/performance claims;
- final Glass Sea architecture;
- human art approval.

Source tool: `art_source/khepri/world_macro/add_optical_uv0_handoff.py`.
