# Consumer Interface — `KHP_WM_HELIOSTAT_FOOTPRINTS`

Status: **INTERFACE_READY / PILOT_BLOCKED_ON_UV0 + REGISTRY**  
Material claim: `CLM-KHEPRI-MATERIALS-001`  
Geometry owner: `CLM-KHEPRI-WMACRO-001`  
Observed source: KHEPRI world-macro project `040f0c45-83a7-483c-9ee7-1e31c640a587` rev `8`.

## Read-only evidence

Representative field:
- 107 mast instances;
- 107 panel instances;
- shared LOD0 mesh families: compact / standard / wide.

Exact LOD0 slot contract observed:

| Mesh family | Current blockout slots | Users |
|---|---|---:|
| `KHP_WM_X100_MAST_COMPACT` | Bronze | 22 |
| `KHP_WM_X100_MAST_STANDARD` | Bronze | 64 |
| `KHP_WM_X100_MAST_WIDE` | Bronze | 21 |
| `KHP_WM_X100_PANEL_COMPACT` | Mirror, Bronze | 22 |
| `KHP_WM_X100_PANEL_STANDARD` | Mirror, Bronze | 64 |
| `KHP_WM_X100_PANEL_WIDE` | Mirror, Bronze | 21 |

Current blockout materials:
- `KHP_WM_MAT_BRONZE_BLOCKOUT`;
- `KHP_WM_MAT_MIRROR_BLOCKOUT`.

## Proposed material binding — pilot only

The first pilot should replace only material roles on a duplicate/integration candidate, not change geometry:

- Bronze structural slot → `KHP_MAT_BRONZE_SYNOD_001::service_clean::cast_structural::architectural`
- Mirror reflector slot → `KHP_MAT_MIRROR_OPTICAL_001::calibrated::broad_reflector::architectural`

Do **not** assign whole-object wear states merely because an assembly is tagged `maintenance`. For example, `contact_polished` should eventually be spatially masked to service/contact regions, not applied across an entire mast.

## Blocking interface defect — UV0

Read-only rev8 audit shows all six LOD0 family meshes have:

- `uv_layers = []`;
- active UV = `null`;
- UV loop count = `0`;
- mesh loop count = `72`.

The current portable material compiler uses a named `UVMap` and exports standard glTF PBR textures. Therefore a deterministic UV0 interface is required before real textured application.

### Required geometry-owner handoff

For each of the six LOD0 meshes, geometry owner must supply:

- one deterministic UV0 layer named `UVMap` unless project convention specifies another canonical name;
- UV loop coverage for all render loops;
- deliberate seams;
- no accidental overlap where unique state masks are expected;
- documented intentional overlap/stacking where tiling is intended;
- metre-scale tiling rule compatible across compact/standard/wide;
- no geometry/silhouette/material-slot regression;
- matching strategy for LOD1/LOD2 source meshes or explicit waiver if far LODs use a simpler material path.

The material agent will **not** create/modify those UVs without explicit geometry-owner handoff.

## Pilot acceptance gates

After UV0 + registry promotion:

1. clone/duplicate an approved macro candidate or receive integration branch handoff;
2. bind two material applications above without geometry mutation;
3. validate UV scale and visible seams;
4. export self-contained GLB;
5. Godot native readback of material roles;
6. compare before/after macro render for material identity and route readability;
7. compare GLB bytes/material count/draw-call/resource sharing;
8. record receipt;
9. do not merge geometry-owner changes from the material branch.

## Nonclaims

This interface does not authorize:
- geometry edits;
- UV edits;
- final Glass Sea architecture;
- per-instance damage/history assignment;
- optical simulation;
- runtime performance approval;
- final-resolution texture art.
