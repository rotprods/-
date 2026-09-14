"""Deterministic KHEPRI X100 Material Lab builder (R2 causal-legibility baseline).

Run inside Blender 5.2+ with bpy available. This is calibration source, not final-resolution texture art.
It generates 6 canonical KHEPRI material families × 4 causal states, deterministic FILE-backed PNGs
that are packed into the .blend, test geometry, labels, neutral lighting and stable metadata.
"""
from __future__ import annotations

import binascii
import math
import os
import struct
import tempfile
import zlib

import bpy
from mathutils import Vector

CONTRACT = "KHP_MATERIAL_PRODUCTION_X100_V1"
TEXTURE_RESOLUTION = 128
VALID_COMBINATIONS = 139
LEGIBILITY_REVISION = "R2_CAUSAL_ENHANCEMENT"

FAMILIES = {
    "solar_glass": {
        "asset_id": "KHP_MAT_GLASS_SOLAR_001",
        "base": (0.34, 0.52, 0.56), "metal": 0.0, "rough": 0.16, "trans": 0.35,
        "finish": "cast_vitrified",
        "states": ["calibrated", "service_worn", "thermal_cycled", "repair_laminated"],
    },
    "mirror_optical": {
        "asset_id": "KHP_MAT_MIRROR_OPTICAL_001",
        "base": (0.62, 0.68, 0.70), "metal": 0.94, "rough": 0.075, "trans": 0.0,
        "finish": "broad_reflector",
        "states": ["calibrated", "maintenance_cleaning", "service_microabrasion", "repair_recoated"],
    },
    "bronze_synod": {
        "asset_id": "KHP_MAT_BRONZE_SYNOD_001",
        "base": (0.36, 0.17, 0.065), "metal": 0.82, "rough": 0.34, "trans": 0.0,
        "finish": "cast_structural",
        "states": ["service_clean", "contact_polished", "heat_affected_local", "field_repaired"],
    },
    "ceramic_scorched": {
        "asset_id": "KHP_MAT_CERAMIC_SCORCHED_001",
        "base": (0.31, 0.19, 0.13), "metal": 0.0, "rough": 0.60, "trans": 0.0,
        "finish": "pressed_tile",
        "states": ["intact", "heat_cycled", "stress_chipped", "patch_replaced"],
    },
    "fabric_shade": {
        "asset_id": "KHP_MAT_FABRIC_SHADE_001",
        "base": (0.27, 0.21, 0.145), "metal": 0.0, "rough": 0.84, "trans": 0.0,
        "finish": "woven_dense",
        "states": ["taut_service", "handled_worn", "solar_aged", "stitched_repair"],
    },
    "mineral_dark": {
        "asset_id": "KHP_MAT_MINERAL_DESERT_001",
        "base": (0.075, 0.068, 0.062), "metal": 0.04, "rough": 0.72, "trans": 0.0,
        "finish": "cut_plate",
        "states": ["cut_clean", "foot_traffic_worn", "thermal_fissure_proxy", "mechanical_patch"],
    },
}

CAUSE = {
    "calibrated": "base", "intact": "base", "taut_service": "base", "cut_clean": "base",
    "service_worn": "contact_use", "service_microabrasion": "contact_use",
    "contact_polished": "contact_use", "handled_worn": "contact_use", "foot_traffic_worn": "contact_use",
    "maintenance_cleaning": "maintenance", "service_clean": "maintenance",
    "thermal_cycled": "thermal", "heat_affected_local": "thermal", "heat_cycled": "thermal",
    "solar_aged": "thermal", "thermal_fissure_proxy": "thermal",
    "repair_laminated": "repair", "repair_recoated": "repair", "field_repaired": "repair",
    "patch_replaced": "repair", "stitched_repair": "repair", "mechanical_patch": "repair",
    "stress_chipped": "mechanical_stress",
}

R2_TARGETS = {
    ("solar_glass", "service_worn"), ("solar_glass", "thermal_cycled"),
    ("solar_glass", "repair_laminated"), ("mirror_optical", "maintenance_cleaning"),
    ("mirror_optical", "service_microabrasion"), ("mirror_optical", "repair_recoated"),
    ("ceramic_scorched", "heat_cycled"), ("mineral_dark", "thermal_fissure_proxy"),
}


def clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return lo if x < lo else hi if x > hi else x


def _chunk(kind: bytes, data: bytes) -> bytes:
    return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", binascii.crc32(kind + data) & 0xFFFFFFFF)


def write_png(path: str, rgba: bytes, n: int = TEXTURE_RESOLUTION) -> None:
    raw = b"".join(b"\x00" + rgba[y * n * 4:(y + 1) * n * 4] for y in range(n))
    payload = (
        b"\x89PNG\r\n\x1a\n"
        + _chunk(b"IHDR", struct.pack(">IIBBBBB", n, n, 8, 6, 0, 0, 0))
        + _chunk(b"IDAT", zlib.compress(raw, 9))
        + _chunk(b"IEND", b"")
    )
    with open(path, "wb") as handle:
        handle.write(payload)


def micro(family: str, u: float, v: float) -> tuple[float, float]:
    t = 2.0 * math.pi
    if family == "solar_glass": return 0.028 * math.sin(t * (3 * u + 0.35 * v)), 0.020 * math.cos(t * 2 * v)
    if family == "mirror_optical": return 0.008 * math.sin(t * 12 * u), 0.005 * math.cos(t * 3 * v)
    if family == "bronze_synod": return 0.040 * math.sin(t * 18 * u), 0.012 * math.sin(t * 2 * v)
    if family == "ceramic_scorched": return 0.030 * math.sin(t * (4 * u + 2 * v)), 0.028 * math.cos(t * (3 * v - u))
    if family == "fabric_shade": return 0.060 * math.sin(t * 24 * u), 0.060 * math.sin(t * 24 * v)
    return 0.035 * math.sin(t * (5 * u + 1.7 * v)), 0.035 * math.cos(t * (4 * v - 1.2 * u))


def cause_mask(state: str, u: float, v: float) -> float:
    cause = CAUSE[state]
    if cause == "contact_use": return clamp(1 - abs(v - 0.31) / 0.25) * clamp(1 - abs(u - 0.52) / 0.54)
    if cause == "maintenance": return clamp(1 - abs((u - v) - 0.04) / 0.16)
    if cause == "thermal": return clamp((u - 0.05) / 0.95) ** 1.25
    if cause == "repair": return 1.0 if 0.54 < u < 0.86 and 0.16 < v < 0.84 else 0.0
    if cause == "mechanical_stress":
        line = 0.82 - 0.66 * u + 0.035 * math.sin(u * 18.0)
        return clamp(1 - abs(v - line) / 0.025)
    return 0.0


def thermal_fissure(u: float, v: float) -> float:
    main = 0.80 - 0.62 * u + 0.030 * math.sin(u * 20)
    value = clamp(1 - abs(v - main) / 0.018)
    if u > 0.56:
        branch = 0.47 + 0.34 * (u - 0.56) + 0.020 * math.sin(u * 17)
        value = max(value, clamp(1 - abs(v - branch) / 0.014))
    if u > 0.72:
        branch = 0.58 - 0.42 * (u - 0.72)
        value = max(value, clamp(1 - abs(v - branch) / 0.012))
    return value


def make_maps(family: str, state: str, spec: dict) -> dict[str, bytes]:
    base_color = spec["base"]
    bc, mr, nm, sm = bytearray(), bytearray(), bytearray(), bytearray()
    for y in range(TEXTURE_RESOLUTION):
        v = y / (TEXTURE_RESOLUTION - 1)
        for x in range(TEXTURE_RESOLUTION):
            u = x / (TEXTURE_RESOLUTION - 1)
            cause = CAUSE[state]
            mask = cause_mask(state, u, v)
            r, g, b = base_color
            rough, metallic = spec["rough"], spec["metal"]
            nx, ny = micro(family, u, v)
            stress = 0.0

            if (family, state) in R2_TARGETS:
                if state == "service_worn":
                    rough += 0.23 * mask; r = r * (1 - 0.10 * mask) + 0.16 * mask; g = g * (1 - 0.08 * mask) + 0.18 * mask; b = b * (1 - 0.06 * mask) + 0.20 * mask
                    ny += 0.11 * mask * math.sin(u * math.pi * 48)
                elif state == "thermal_cycled":
                    rough += 0.20 * mask; r *= 1 + 0.28 * mask; g *= 1 - 0.24 * mask; b *= 1 - 0.38 * mask; nx += 0.06 * mask * math.sin(v * math.pi * 10)
                elif state == "repair_laminated":
                    rough -= 0.08 * mask; r = r * (1 - 0.26 * mask) + 0.10 * mask; g = g * (1 - 0.22 * mask) + 0.20 * mask; b = b * (1 - 0.18 * mask) + 0.24 * mask
                    if mask and (abs(u - .54) < .018 or abs(u - .86) < .018 or abs(v - .16) < .018 or abs(v - .84) < .018): nx += .22
                elif state == "maintenance_cleaning":
                    rough = .18 * (1 - mask) + .035 * mask; r *= .88 + .18 * mask; g *= .88 + .18 * mask; b *= .88 + .18 * mask
                elif state == "service_microabrasion":
                    rough += .28 * mask; r *= 1 - .10 * mask; g *= 1 - .09 * mask; b *= 1 - .08 * mask; ny += .16 * mask * math.sin(u * math.pi * 68)
                elif state == "repair_recoated":
                    rough = .13 * (1 - mask) + .025 * mask; r = r * (1 - .18 * mask) + .72 * mask * .18; g = g * (1 - .18 * mask) + .76 * mask * .18; b = b * (1 - .18 * mask) + .78 * mask * .18
                    if mask and (abs(u - .54) < .018 or abs(u - .86) < .018): nx += .18
                elif state == "heat_cycled":
                    rough += .18 * mask; r *= 1 + .20 * mask; g *= 1 - .25 * mask; b *= 1 - .40 * mask; ny += .08 * mask * math.sin(v * math.pi * 8)
                elif state == "thermal_fissure_proxy":
                    stress = thermal_fissure(u, v); rough += .10 * mask + .12 * stress; r *= 1 - .58 * stress; g *= 1 - .58 * stress; b *= 1 - .58 * stress; nx += .20 * stress; ny -= .16 * stress
            else:
                manufacture = 0.025 * (nx + ny)
                if cause == "contact_use":
                    rough += (-0.16 if family in ("bronze_synod", "mirror_optical") else 0.12) * mask; r *= 1 + .08 * mask; g *= 1 + .065 * mask; b *= 1 + .045 * mask
                elif cause == "maintenance":
                    rough -= .09 * mask; r *= 1 + .08 * mask; g *= 1 + .08 * mask; b *= 1 + .08 * mask
                elif cause == "thermal":
                    rough += .10 * mask; r *= 1 + .11 * mask; g *= 1 - .13 * mask; b *= 1 - .22 * mask
                elif cause == "repair":
                    rough += (0.08 if family not in ("mirror_optical", "bronze_synod") else -0.04) * mask; r = r * (1 - .15 * mask) + .16 * mask; g = g * (1 - .15 * mask) + .12 * mask; b = b * (1 - .15 * mask) + .08 * mask
                    if mask and (abs(u - .54) < .018 or abs(u - .86) < .018): nx += .20
                elif cause == "mechanical_stress":
                    rough += .18 * mask; r *= 1 - .55 * mask; g *= 1 - .55 * mask; b *= 1 - .55 * mask; ny += .25 * mask; stress = mask
                r *= 1 + manufacture; g *= 1 + manufacture; b *= 1 + manufacture

            r, g, b = clamp(r), clamp(g), clamp(b)
            rough = clamp(rough, .02, .97)
            bc += bytes((round(r * 255), round(g * 255), round(b * 255), 255))
            mr += bytes((255, round(rough * 255), round(clamp(metallic) * 255), 255))
            nm += bytes((round(clamp(.5 + nx) * 255), round(clamp(.5 + ny) * 255), 255, 255))
            use = mask if cause in ("contact_use", "maintenance") else 0.0
            thermal = mask if cause == "thermal" else 0.0
            repair = mask if cause == "repair" else 0.0
            sm += bytes((round(use * 255), round(thermal * 255), round(repair * 255), round(stress * 255)))
    return {"BC": bytes(bc), "MR": bytes(mr), "N": bytes(nm), "SM": bytes(sm)}


def packed_image(name: str, data: bytes, colorspace: str, revision: str) -> bpy.types.Image:
    path = os.path.join(tempfile.gettempdir(), name + ".png")
    write_png(path, data)
    image = bpy.data.images.load(path, check_existing=False)
    image.name = name
    image.colorspace_settings.name = colorspace
    image.pack()
    image["contract"] = CONTRACT
    image["packed_source"] = "deterministic_png_r2" if revision == LEGIBILITY_REVISION else "deterministic_png"
    image["width"] = TEXTURE_RESOLUTION; image["height"] = TEXTURE_RESOLUTION
    try: os.remove(path)
    except OSError: pass
    image.filepath = ""
    return image


def make_material(family: str, state: str, spec: dict) -> bpy.types.Material:
    asset_id = spec["asset_id"]
    revision = LEGIBILITY_REVISION if (family, state) in R2_TARGETS else "R1_BASELINE"
    maps = make_maps(family, state, spec)
    stem = f"{asset_id}__{state.upper()}"
    images = {key: packed_image(f"{stem}__{key}", value, "sRGB" if key == "BC" else "Non-Color", revision) for key, value in maps.items()}
    material = bpy.data.materials.new(stem); material.use_nodes = True
    for key, value in {"family": family, "asset_id": asset_id, "state": state, "cause": CAUSE[state], "finish": spec["finish"], "contract": CONTRACT, "application_scale": "calibration"}.items(): material[key] = value
    if revision == LEGIBILITY_REVISION: material["legibility_revision"] = revision
    tree = material.node_tree; tree.nodes.clear()
    output = tree.nodes.new("ShaderNodeOutputMaterial")
    bsdf = tree.nodes.new("ShaderNodeBsdfPrincipled"); bsdf.name = "KHP_PRINCIPLED"; bsdf.inputs["IOR"].default_value = 1.5; bsdf.inputs["Transmission Weight"].default_value = spec["trans"]
    uv = tree.nodes.new("ShaderNodeUVMap"); uv.name = "KHP_UV0"; uv.uv_map = "UVMap"
    texture_nodes = {}
    for key in ("BC", "MR", "N", "SM"):
        node = tree.nodes.new("ShaderNodeTexImage"); node.name = "KHP_TEX_" + key; node.image = images[key]; node.interpolation = "Linear"; node.extension = "REPEAT"; texture_nodes[key] = node; tree.links.new(uv.outputs["UV"], node.inputs["Vector"])
    separate = tree.nodes.new("ShaderNodeSeparateColor"); separate.name = "KHP_MR_SEPARATE"
    normal = tree.nodes.new("ShaderNodeNormalMap"); normal.name = "KHP_NORMALMAP"; normal.space = "TANGENT"; normal.inputs["Strength"].default_value = 0.75
    tree.links.new(texture_nodes["BC"].outputs["Color"], bsdf.inputs["Base Color"])
    tree.links.new(texture_nodes["MR"].outputs["Color"], separate.inputs["Color"])
    tree.links.new(separate.outputs["Green"], bsdf.inputs["Roughness"]); tree.links.new(separate.outputs["Blue"], bsdf.inputs["Metallic"])
    tree.links.new(texture_nodes["N"].outputs["Color"], normal.inputs["Color"]); tree.links.new(normal.outputs["Normal"], bsdf.inputs["Normal"]); tree.links.new(bsdf.outputs["BSDF"], output.inputs["Surface"])
    texture_nodes["SM"].label = "Source-only causal state mask: R use/maintenance, G thermal, B repair, A stress"
    return material


def move_to(obj: bpy.types.Object, collection: bpy.types.Collection) -> None:
    for current in list(obj.users_collection): current.objects.unlink(obj)
    collection.objects.link(obj)


def look_at(obj: bpy.types.Object, point: tuple[float, float, float]) -> None:
    obj.rotation_euler = (Vector(point) - obj.location).to_track_quat("-Z", "Y").to_euler()


def build() -> dict:
    for obj in list(bpy.data.objects): bpy.data.objects.remove(obj, do_unlink=True)
    for datablocks in (bpy.data.materials, bpy.data.images, bpy.data.meshes, bpy.data.curves):
        for item in list(datablocks): datablocks.remove(item)
    scene = bpy.context.scene; scene.name = "KHEPRI_X100_MATERIAL_LAB"; scene.render.engine = "BLENDER_EEVEE"; scene.render.resolution_x = 960; scene.render.resolution_y = 720; scene.render.resolution_percentage = 100; scene.render.image_settings.file_format = "PNG"
    scene.world = bpy.data.worlds.get("World") or bpy.data.worlds.new("World"); scene.world.color = (0.018, 0.018, 0.016)
    scene["material_contract"] = CONTRACT; scene["valid_combinations"] = VALID_COMBINATIONS; scene["calibration_texture_resolution"] = TEXTURE_RESOLUTION; scene["material_legibility_revision"] = LEGIBILITY_REVISION
    root = bpy.data.collections.new("KHP_MATLAB_ROOT"); scene.collection.children.link(root)
    samples = bpy.data.collections.new("KHP_MATLAB_SAMPLES"); labels = bpy.data.collections.new("KHP_MATLAB_LABELS"); lights = bpy.data.collections.new("KHP_MATLAB_LIGHTS"); root.children.link(samples); root.children.link(labels); root.children.link(lights)
    meta = bpy.data.objects.new("KHP_MATLAB_META", None); root.objects.link(meta); meta["contract"] = CONTRACT; meta["claim_id"] = "CLM-KHEPRI-MATERIALS-001"; meta["valid_combinations"] = VALID_COMBINATIONS; meta["calibration_cells"] = 24; meta["texture_resolution"] = TEXTURE_RESOLUTION
    label_mat = bpy.data.materials.new("KHP_MATLAB_LABEL"); label_mat.use_nodes = True; lbs = label_mat.node_tree.nodes.get("Principled BSDF"); lbs.inputs["Base Color"].default_value = (0.72, 0.70, 0.62, 1); lbs.inputs["Roughness"].default_value = .72
    def label(body, location, size=.26, align="CENTER"):
        curve = bpy.data.curves.new("TXT_" + body[:20], "FONT"); curve.body = body; curve.align_x = align; curve.size = size; curve.extrude = .008
        obj = bpy.data.objects.new("LBL_" + body[:32], curve); labels.objects.link(obj); obj.location = location; obj.rotation_euler = (math.radians(90), 0, 0); curve.materials.append(label_mat); return obj
    bpy.ops.mesh.primitive_cube_add(location=(0, .8, 0), scale=(11.7, .12, 11.1)); wall = bpy.context.object; wall.name = "KHP_MATLAB_BACKDROP"; move_to(wall, root)
    wall_mat = bpy.data.materials.new("KHP_MATLAB_BACKDROP_MAT"); wall_mat.use_nodes = True; wbs = wall_mat.node_tree.nodes.get("Principled BSDF"); wbs.inputs["Base Color"].default_value = (.035, .032, .028, 1); wbs.inputs["Roughness"].default_value = .82; wall.data.materials.append(wall_mat)
    xs = [-7.8, -2.6, 2.6, 7.8]; zs = [8.6, 5.15, 1.70, -1.75, -5.20, -8.65]
    material_count = 0
    for row, (family, spec) in enumerate(FAMILIES.items()):
        label(family.replace("_", " ").upper(), (-10.9, -.35, zs[row] + .35), .30, "LEFT")
        for col, state in enumerate(spec["states"]):
            material = make_material(family, state, spec); material_count += 1; x, z = xs[col], zs[row]
            bpy.ops.mesh.primitive_cube_add(location=(x - .45, 0, z + .25), scale=(1.45, .15, .95)); panel = bpy.context.object; panel.name = f"KHP_SAMPLE_PANEL__{family.upper()}__{state.upper()}"; move_to(panel, samples); panel.data.materials.append(material); panel["asset_id"] = spec["asset_id"]; panel["state"] = state; panel["cause"] = CAUSE[state]
            bevel = panel.modifiers.new("KHP_BEVEL", "BEVEL"); bevel.width = .08; bevel.segments = 2; bpy.context.view_layer.objects.active = panel; panel.select_set(True); bpy.ops.object.modifier_apply(modifier=bevel.name); panel.select_set(False)
            bpy.ops.mesh.primitive_uv_sphere_add(segments=20, ring_count=12, radius=.62, location=(x + 1.25, -.28, z + .12)); sphere = bpy.context.object; sphere.name = f"KHP_SAMPLE_CURVED__{family.upper()}__{state.upper()}"; move_to(sphere, samples); sphere.data.materials.append(material); sphere["asset_id"] = spec["asset_id"]; sphere["state"] = state; sphere["cause"] = CAUSE[state]
            for polygon in sphere.data.polygons: polygon.use_smooth = True
            label(state.replace("_", " "), (x - .05, -.38, z - 1.12), .20, "CENTER")
    camera_data = bpy.data.cameras.new("KHP_MATLAB_CAM"); camera = bpy.data.objects.new("KHP_MATLAB_CAM", camera_data); lights.objects.link(camera); camera.location = (0, -44, 0); camera_data.lens = 55; camera_data.sensor_width = 36; camera_data.clip_end = 200; look_at(camera, (0, 0, 0)); scene.camera = camera
    sun_data = bpy.data.lights.new("KHP_MATLAB_SUN", "SUN"); sun_data.energy = 3.0; sun_data.angle = math.radians(6); sun = bpy.data.objects.new("KHP_MATLAB_SUN", sun_data); lights.objects.link(sun); sun.rotation_euler = (math.radians(38), 0, math.radians(-32))
    key_data = bpy.data.lights.new("KHP_MATLAB_KEY", "POINT"); key_data.energy = 1250; key_data.color = (1.0, .78, .58); key = bpy.data.objects.new("KHP_MATLAB_KEY", key_data); lights.objects.link(key); key.location = (-11, -12, 11)
    fill_data = bpy.data.lights.new("KHP_MATLAB_FILL", "POINT"); fill_data.energy = 780; fill_data.color = (.58, .70, 1.0); fill = bpy.data.objects.new("KHP_MATLAB_FILL", fill_data); lights.objects.link(fill); fill.location = (11, -10, 4)
    return {"contract": CONTRACT, "materials": material_count, "images": len([i for i in bpy.data.images if i.get("contract") == CONTRACT]), "objects": len(bpy.data.objects), "legibility_revision": LEGIBILITY_REVISION}


if __name__ == "__main__":
    print(build())
