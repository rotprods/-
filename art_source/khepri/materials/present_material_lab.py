"""Presentation-only stage for the KHEPRI X100 Material Lab.

Requires `compile_material_library.py` identity to already exist in the current Blender scene.
Adds labels, neutral backdrop, camera and motivated lights. It MUST NOT mutate any material or
contract image. Presentation is QA evidence, not material identity.
"""
from __future__ import annotations

import math
import bpy
from mathutils import Vector

CONTRACT = "KHP_MATERIAL_PRODUCTION_X100_V1"
PRESENTATION = "R3_NORMALIZED_PRESENTATION"

FAMILY_ROWS = [
    ("SOLAR GLASS", ["calibrated", "service worn", "thermal cycled", "repair laminated"]),
    ("MIRROR OPTICAL", ["calibrated", "maintenance cleaning", "service microabrasion", "repair recoated"]),
    ("BRONZE SYNOD", ["service clean", "contact polished", "heat affected local", "field repaired"]),
    ("CERAMIC SCORCHED", ["intact", "heat cycled", "stress chipped", "patch replaced"]),
    ("FABRIC SHADE", ["taut service", "handled worn", "solar aged", "stitched repair"]),
    ("MINERAL DARK", ["cut clean", "foot traffic worn", "thermal fissure proxy", "mechanical patch"]),
]
XS = [-7.8, -2.6, 2.6, 7.8]
ZS = [8.6, 5.15, 1.70, -1.75, -5.20, -8.65]


def _simple_material(name: str, color: tuple[float, float, float], roughness: float):
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    return mat


def _remove_previous() -> None:
    prefixes = ("KHP_MATLAB_PRESENT_", "KHP_MATLAB_CAM", "KHP_MATLAB_SUN", "KHP_MATLAB_KEY", "KHP_MATLAB_FILL", "LBL_")
    for obj in list(bpy.data.objects):
        if obj.name.startswith(prefixes):
            bpy.data.objects.remove(obj, do_unlink=True)
    for collection in list(bpy.data.collections):
        if collection.name in {"KHP_MATLAB_PRESENTATION", "KHP_MATLAB_LABELS", "KHP_MATLAB_LIGHTS"}:
            bpy.data.collections.remove(collection)


def _look_at(obj, point=(0.0, 0.0, 0.0)) -> None:
    obj.rotation_euler = (Vector(point) - obj.location).to_track_quat("-Z", "Y").to_euler()


def present() -> dict:
    scene = bpy.context.scene
    contract_images = [img for img in bpy.data.images if img.get("contract") == CONTRACT]
    contract_materials = [mat for mat in bpy.data.materials if mat.get("contract") == CONTRACT]
    samples = [obj for obj in bpy.data.objects if obj.name.startswith("KHP_SAMPLE_")]
    if len(contract_images) != 96 or len(contract_materials) != 24 or len(samples) != 48:
        raise RuntimeError("identity precondition failed; run compile_material_library.py first")

    _remove_previous()
    root = bpy.data.collections.new("KHP_MATLAB_PRESENTATION")
    labels = bpy.data.collections.new("KHP_MATLAB_LABELS")
    lights = bpy.data.collections.new("KHP_MATLAB_LIGHTS")
    scene.collection.children.link(root)
    root.children.link(labels)
    root.children.link(lights)

    backdrop_mat = _simple_material("KHP_MATLAB_PRESENT_BACKDROP", (0.028, 0.026, 0.023), 0.88)
    label_mat = _simple_material("KHP_MATLAB_PRESENT_LABEL", (0.72, 0.70, 0.62), 0.72)

    bpy.ops.mesh.primitive_cube_add(location=(0, 0.8, 0), scale=(11.7, 0.12, 11.1))
    backdrop = bpy.context.object
    backdrop.name = "KHP_MATLAB_PRESENT_BACKDROP"
    backdrop.data.materials.append(backdrop_mat)
    for collection in list(backdrop.users_collection):
        collection.objects.unlink(backdrop)
    root.objects.link(backdrop)

    def label(text: str, location, size=0.24, align="CENTER"):
        curve = bpy.data.curves.new("LBL_CURVE_" + text[:18], "FONT")
        curve.body = text
        curve.align_x = align
        curve.size = size
        curve.extrude = 0.008
        curve.materials.append(label_mat)
        obj = bpy.data.objects.new("LBL_" + text[:28], curve)
        labels.objects.link(obj)
        obj.location = location
        obj.rotation_euler = (math.radians(90), 0, 0)
        return obj

    for row, (family, states) in enumerate(FAMILY_ROWS):
        label(family, (-10.9, -0.35, ZS[row] + 0.35), 0.30, "LEFT")
        for col, state in enumerate(states):
            label(state, (XS[col] - 0.05, -0.38, ZS[row] - 1.12), 0.20, "CENTER")

    camera_data = bpy.data.cameras.new("KHP_MATLAB_CAM")
    camera = bpy.data.objects.new("KHP_MATLAB_CAM", camera_data)
    lights.objects.link(camera)
    camera.location = (0, -44, 0)
    camera_data.lens = 55
    camera_data.sensor_width = 36
    camera_data.clip_end = 200
    _look_at(camera)
    scene.camera = camera

    sun_data = bpy.data.lights.new("KHP_MATLAB_SUN", "SUN")
    sun_data.energy = 3.0
    sun_data.angle = math.radians(6)
    sun = bpy.data.objects.new("KHP_MATLAB_SUN", sun_data)
    lights.objects.link(sun)
    sun.rotation_euler = (math.radians(38), 0, math.radians(-32))

    key_data = bpy.data.lights.new("KHP_MATLAB_KEY", "POINT")
    key_data.energy = 1250
    key_data.color = (1.0, 0.78, 0.58)
    key = bpy.data.objects.new("KHP_MATLAB_KEY", key_data)
    lights.objects.link(key)
    key.location = (-11, -12, 11)

    fill_data = bpy.data.lights.new("KHP_MATLAB_FILL", "POINT")
    fill_data.energy = 780
    fill_data.color = (0.58, 0.70, 1.0)
    fill = bpy.data.objects.new("KHP_MATLAB_FILL", fill_data)
    lights.objects.link(fill)
    fill.location = (11, -10, 4)

    scene.render.engine = "BLENDER_EEVEE"
    scene.render.resolution_x = 960
    scene.render.resolution_y = 720
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.film_transparent = False
    if scene.world:
        scene.world.color = (0.018, 0.018, 0.016)
    scene["material_presentation_revision"] = PRESENTATION

    return {
        "contract": CONTRACT,
        "presentation": PRESENTATION,
        "identity_mutated": False,
        "resolution": [960, 720],
    }


if __name__ == "__main__":
    print(present())
