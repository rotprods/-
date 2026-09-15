# VANTA — Godot glTF light transport contract

Status: **diagnostic contract / adapter proposal, not final renderer calibration**.

This file exists to prevent future agents from compensating for a light-unit portability defect by corrupting the CP5 texture payloads.

## Proven facts

Revision 10 already proves that CP5 base-color, ORM and normal payloads survive source → embedded GLB → Godot texture readback. Revision 11's controlled three-swatch silhouette test also proves camera/geometry alignment: silhouette IoU `0.98481187435` and exact mask agreement `0.9950347222`.

The remaining controlled visual mismatch is therefore classified as lighting/shading/tonemapping portability, not geometry or texture transport.

Observed neutral point lights:

| light | Blender source power | glTF `KHR_lights_punctual.intensity` | Godot default import |
|---|---:|---:|---:|
| `L_CP5_NEUTRAL_FILL` | 600 | 47.74648 | `light_energy ≈ 47.74648` |
| `L_CP5_NEUTRAL_KEY` | 1200 | 95.49297 | `light_energy ≈ 95.49297` |

The observed point-light export mapping is approximately `I_gltf = P_source / (4π)`.

Godot documents `light_energy` as the ordinary energy multiplier, while positional physical-light intensity is represented by `light_intensity_lumens` when `rendering/lights_and_shadows/use_physical_light_units=true`. Simply turning physical units on after import made the controlled VANTA board **more** overexposed because the imported `light_energy` values remained large while physical intensity stayed at its default.

Known upstream reference: `godotengine/godot#73624` — glTF light import values affected by the Blender/glTF light-unit specification change.

## Mandatory rules

1. **Do not rebake or darken CP5 BC/ORM/normal textures to compensate for this mismatch.**
2. Preserve the source Blender lighting values and the exact glTF values as evidence.
3. Treat Godot's imported light parameters as a runtime-portability layer, not canonical art data.
4. Keep physical-unit calibration separate from the existing Godot validation path until a controlled A/B passes.
5. Any adapter remains `PROPOSED` until the neutral-board comparison and target-hardware review pass.
6. Final engine selection remains open; this contract must not be used to claim Godot is the final renderer.

## Standards-aware adapter proposal

For a **point/Omni** light, glTF `KHR_lights_punctual.intensity` is an intensity quantity in candela. For an isotropic point source, luminous flux is related by:

`lumens = candela × 4π`

Therefore the first physically coherent Godot A/B to test is:

- enable physical light units for the isolated validation project;
- set `OmniLight3D.light_energy = 1.0`;
- set `OmniLight3D.light_intensity_lumens = imported_gltf_intensity × 4π`;
- preserve color, range and transform exactly;
- compare against the Blender neutral board under controlled camera/background/exposure.

For a **DirectionalLight3D**, glTF directional intensity is already an illuminance-style quantity; test mapping it to Godot `light_intensity_lux` with `light_energy = 1.0`.

Do **not** generalize the point-light `4π` mapping to spotlights. Spotlights require cone/solid-angle handling and need a separate qualification case.

## Acceptance gate for a runtime adapter

The adapter may advance from `PROPOSED` only when all are true:

- same camera transform/FOV and same test geometry;
- same intended light set and background contract;
- material payload readback still passes;
- swatch silhouette alignment remains ≥ 0.98 IoU;
- controlled shaded luminance/edge metrics materially improve over rev11 baseline;
- no clipping/degenerate black/white result;
- human visual review confirms the physical roles remain credible;
- target-hardware run records frame time and does not silently change the art contract.

## Current truth

`LIGHT_UNIT_PORTABILITY_BLOCKER / ADAPTER_CALIBRATION_PENDING`.

This is not a CP5 texture failure. It is not a final-engine failure. It is a cross-renderer light-transport gate that must be solved at import/runtime calibration.
