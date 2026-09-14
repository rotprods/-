"""ELYSIUM NULL — W1 white-envelope material proof.

ART-ELYSIUM-001
Observed Blender target: 5.2.0 LTS, metric 1 BU = 1 m.

Purpose:
- Compare three portable Principled white-surface roles before propagating them.
- Give the dominant envelope a plausible layered construction hypothesis.
- Keep wear/anomaly local and causal rather than adding global procedural grunge.

Everything authored here is PROPOSAL until creative + target-engine material review.
No external textures or network access are required.
"""

import bpy
from mathutils import Vector

scene = bpy.context.scene
scene.render.resolution_x = 960
scene.render.resolution_y = 540
scene.render.resolution_percentage = 100


def ensure_collection(name):
    col = bpy.data.collections.get(name) or bpy.data.collections.new(name)
    if scene.collection.children.get(col.name) is None:
        scene.collection.children.link(col)
    return col


PROOF = ensure_collection("70_W1_MATERIAL_PROOF")
LIGHTS = ensure_collection("71_W1_MATERIAL_LIGHTS")


def move_to(obj, collection):
    for old in list(obj.users_collection):
        old.objects.unlink(obj)
    collection.objects.link(obj)


def make_material(name, base, roughness, coat=0.0, coat_roughness=0.03):
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*base, 1.0)
    bsdf.inputs["Metallic"].default_value = 0.0
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Coat Weight"].default_value = coat
    bsdf.inputs["Coat Roughness"].default_value = coat_roughness
    mat["epistemic"] = "PROPOSAL"
    return mat


def box(name, location, dimensions, material, bevel=0.0):
    bpy.ops.mesh.primitive_cube_add(location=location)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = dimensions
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.data.materials.append(material)
    move_to(obj, PROOF)
    if bevel:
        mod = obj.modifiers.new("Bevel_physical", "BEVEL")
        mod.width = bevel
        mod.segments = 3
    return obj


def look_at(obj, target):
    obj.rotation_euler = (Vector(target) - obj.location).to_track_quat("-Z", "Y").to_euler()


C01 = make_material(
    "MAT_Elysium_WHITE_C01_SinteredCeramic",
    (0.78, 0.79, 0.785),
    roughness=0.34,
    coat=0.06,
    coat_roughness=0.12,
)
C01["manufacturing_hypothesis"] = "sintered aluminosilicate ceramic facing"
C01["role"] = "dominant maintained exterior/interior facing"

C02 = make_material(
    "MAT_Elysium_WHITE_C02_MineralComposite",
    (0.66, 0.675, 0.68),
    roughness=0.52,
    coat=0.0,
)
C02["manufacturing_hypothesis"] = "mineral-filled structural composite"
C02["role"] = "load-bearing/recessed matte body"

C03 = make_material(
    "MAT_Elysium_WHITE_C03_ServiceGlaze",
    (0.83, 0.835, 0.825),
    roughness=0.22,
    coat=0.14,
    coat_roughness=0.08,
)
C03["manufacturing_hypothesis"] = "maintained ceramic glaze / hygienic service surface"
C03["role"] = "rare touched/service surfaces, not universal envelope"

METAL = bpy.data.materials["MAT_Elysium_SatinMetal_PROPOSAL"]
DARK = bpy.data.materials["MAT_Elysium_Recess_PROPOSAL"]
AMBER = bpy.data.materials["MAT_Elysium_ServiceAmber_PROPOSAL"]

# 2.4 m x 3 m material cards inside the proposed 240 mm architecture system.
for x, mat, label in zip(
    (86, 90, 94),
    (C01, C02, C03),
    ("C01_CERAMIC", "C02_MINERAL", "C03_GLAZE"),
):
    panel = box(f"MAT_PROOF_{label}", (x, -90, 1.5), (2.4, 0.24, 3.0), mat, 0.035)
    panel["sample_role"] = "material candidate coupon"
    panel["system_thickness_m"] = 0.24
    box(f"MAT_PROOF_{label}_PLINTH", (x, -90.16, 0.14), (2.6, 0.38, 0.28), DARK, 0.025)

# Sectioned construction hypothesis. These are design values, not certified engineering data.
cut_x = 98.5
face = box("MAT_CUTAWAY_CERAMIC_FACE", (cut_x, -90.11, 1.5), (2.2, 0.012, 3.0), C01, 0.01)
face["layer"] = "12 mm ceramic face proposal"
core = box("MAT_CUTAWAY_MINERAL_CORE", (cut_x, -89.99, 1.5), (2.2, 0.18, 3.0), C02, 0.015)
core["layer"] = "180 mm composite core proposal"
back = box("MAT_CUTAWAY_METAL_BACKER", (cut_x, -89.895, 1.5), (2.2, 0.004, 3.0), METAL, 0.002)
back["layer"] = "4 mm service backer proposal"

# Controlled construction joint: 16 mm reveal candidate.
box("MAT_JOINT_PANEL_L", (84, -86, 1.5), (1.992, 0.24, 3.0), C01, 0.03)
box("MAT_JOINT_PANEL_R", (86.008, -86, 1.5), (1.992, 0.24, 3.0), C01, 0.03)
joint = box("MAT_JOINT_SHADOW_REVEAL", (85.004, -86.135, 1.5), (0.016, 0.05, 2.9), DARK, 0.002)
joint["joint_width_m"] = 0.016

# Human anomaly remains localized instead of turning the whole world dirty.
box("MAT_HUMAN_CONTACT_PLATE", (90, -86.14, 1.1), (0.42, 0.035, 0.9), METAL, 0.025)
box("MAT_HUMAN_REPAIR_TAB", (90.18, -86.17, 0.92), (0.16, 0.025, 0.22), AMBER, 0.015)

# Highlight-reference spheres.
for x, mat, label in zip(
    (86, 90, 94),
    (C01, C02, C03),
    ("C01_CERAMIC", "C02_MINERAL", "C03_GLAZE"),
):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=48, ring_count=24, radius=0.55, location=(x, -87.4, 0.7))
    sphere = bpy.context.object
    sphere.name = f"MAT_SPHERE_{label}"
    sphere.data.materials.append(mat)
    move_to(sphere, PROOF)

# Portable point-light lab; no HDRI dependency.
for name, location, energy, color, radius in (
    ("MATLAB_KEY", (82, -98, 7), 1200, (1.0, 0.78, 0.62), 3.0),
    ("MATLAB_FILL", (101, -96, 5), 900, (0.58, 0.72, 1.0), 4.0),
    ("MATLAB_RAKE", (88, -84, 3), 650, (1.0, 0.95, 0.88), 2.0),
):
    bpy.ops.object.light_add(type="POINT", location=location)
    light = bpy.context.object
    light.name = name
    light.data.energy = energy
    light.data.color = color
    light.data.shadow_soft_size = radius
    move_to(light, LIGHTS)

# Close / mid / far cameras are part of the evaluation contract.
for name, location, target, lens in (
    ("CAM_MAT_CLOSE", (88, -96, 2.4), (90, -90, 1.5), 70),
    ("CAM_MAT_MID", (90, -103, 4.2), (90, -90, 1.5), 55),
    ("CAM_MAT_FAR", (91, -115, 7.2), (90, -89, 1.5), 48),
):
    bpy.ops.object.camera_add(location=location)
    camera = bpy.context.object
    camera.name = name
    camera.data.lens = lens
    look_at(camera, target)
    move_to(camera, LIGHTS)

print(
    {
        "status": "WHITE_MATERIAL_PROOF_BUILT",
        "candidate_materials": [C01.name, C02.name, C03.name],
        "panel_system_thickness_m": 0.24,
        "cutaway_layers_m": {"ceramic_face": 0.012, "mineral_core": 0.18, "metal_backer": 0.004},
        "joint_reveal_m": 0.016,
        "visual_approval": "PENDING",
    }
)
