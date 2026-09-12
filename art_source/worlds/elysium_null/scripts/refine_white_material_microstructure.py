"""EXOVANT 2950 / ELYSIUM NULL — R7 white-material refinement.

Precondition:
- Run after `add_white_material_proof.py` against the ELYSIUM World Master.
- Scene units are metric, 1 BU = 1 metre.

Purpose:
- turn revision-6 flat Principled material candidates into physically restrained
  manufacturing-surface candidates;
- add an explicit 16 mm joint assembly (gasket/backer/anchors/cavity);
- preserve the anti-grunge contract: intrinsic material variation only.

Status: LOOKDEV candidate. This script does NOT constitute target-engine shader,
UV/texture-budget, GATE-ASSET, GATE-ART or production-performance qualification.
"""

import bpy

scene = bpy.context.scene
proof = bpy.data.collections.get("70_W1_MATERIAL_PROOF")
if proof is None:
    proof = bpy.data.collections.new("70_W1_MATERIAL_PROOF")
    scene.collection.children.link(proof)


def move_to(obj, target):
    for old in list(obj.users_collection):
        old.objects.unlink(obj)
    target.objects.link(obj)


def clear_nodes(mat):
    mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.clear()
    return nt


def set_principled(mat, base=(0.8, 0.8, 0.8, 1.0), rough=0.4, metallic=0.0, coat=0.0, coat_rough=0.1):
    nt = clear_nodes(mat)
    output = nt.nodes.new("ShaderNodeOutputMaterial")
    output.location = (720, 0)
    bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled")
    bsdf.location = (450, 0)
    bsdf.name = "PBR_MASTER"
    bsdf.label = "PBR candidate / physically restrained"
    bsdf.inputs["Base Color"].default_value = base
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = rough
    bsdf.inputs["Coat Weight"].default_value = coat
    bsdf.inputs["Coat Roughness"].default_value = coat_rough
    nt.links.new(bsdf.outputs["BSDF"], output.inputs["Surface"])
    return nt, bsdf


def procedural_white(
    mat,
    macro_scale,
    c0,
    c1,
    rough0,
    rough1,
    micro_scale,
    bump_strength,
    bump_distance_m,
    coat=0.0,
    coat_rough=0.1,
):
    nt, bsdf = set_principled(
        mat,
        base=(*c0, 1.0),
        rough=(rough0 + rough1) / 2.0,
        coat=coat,
        coat_rough=coat_rough,
    )

    tex = nt.nodes.new("ShaderNodeTexCoord")
    tex.location = (-920, 80)
    tex.name = "COORD_OBJECT_SCALE"
    tex.label = "Object coordinates / 1 BU = 1 m"

    macro = nt.nodes.new("ShaderNodeTexNoise")
    macro.location = (-690, 170)
    macro.name = "MACRO_VARIATION"
    macro.noise_dimensions = "3D"
    macro.inputs["Scale"].default_value = macro_scale
    macro.inputs["Detail"].default_value = 3.0
    macro.inputs["Roughness"].default_value = 0.55

    color_ramp = nt.nodes.new("ShaderNodeValToRGB")
    color_ramp.location = (-430, 190)
    color_ramp.name = "MACRO_COLOR_RANGE"
    color_ramp.color_ramp.elements[0].color = (*c0, 1.0)
    color_ramp.color_ramp.elements[1].color = (*c1, 1.0)

    micro = nt.nodes.new("ShaderNodeTexNoise")
    micro.location = (-680, -210)
    micro.name = "MICRO_SURFACE"
    micro.noise_dimensions = "3D"
    micro.inputs["Scale"].default_value = micro_scale
    micro.inputs["Detail"].default_value = 2.0
    micro.inputs["Roughness"].default_value = 0.48

    rough_map = nt.nodes.new("ShaderNodeMapRange")
    rough_map.location = (-390, -135)
    rough_map.name = "ROUGHNESS_RANGE"
    rough_map.inputs["From Min"].default_value = 0.0
    rough_map.inputs["From Max"].default_value = 1.0
    rough_map.inputs["To Min"].default_value = rough0
    rough_map.inputs["To Max"].default_value = rough1

    bump = nt.nodes.new("ShaderNodeBump")
    bump.location = (120, -160)
    bump.name = "MICRO_BUMP_METRIC"
    bump.inputs["Strength"].default_value = bump_strength
    bump.inputs["Distance"].default_value = bump_distance_m

    nt.links.new(tex.outputs["Generated"], macro.inputs["Vector"])
    nt.links.new(macro.outputs["Fac"], color_ramp.inputs["Fac"])
    nt.links.new(color_ramp.outputs["Color"], bsdf.inputs["Base Color"])

    nt.links.new(tex.outputs["Generated"], micro.inputs["Vector"])
    nt.links.new(micro.outputs["Fac"], rough_map.inputs["Value"])
    nt.links.new(rough_map.outputs["Result"], bsdf.inputs["Roughness"])
    nt.links.new(micro.outputs["Fac"], bump.inputs["Height"])
    nt.links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])

    mat["material_status"] = "W1_MICROSTRUCTURE_CANDIDATE"
    mat["metric_bump_distance_m"] = bump_distance_m
    mat["macro_noise_scale_per_m"] = macro_scale
    mat["micro_noise_scale_per_m"] = micro_scale
    mat["anti_grunge"] = "NO_RANDOM_WEAR; intrinsic manufacturing microstructure only"
    return mat


ceramic = bpy.data.materials["MAT_Elysium_WHITE_C01_SinteredCeramic"]
mineral = bpy.data.materials["MAT_Elysium_WHITE_C02_MineralComposite"]
glaze = bpy.data.materials["MAT_Elysium_WHITE_C03_ServiceGlaze"]

procedural_white(
    ceramic,
    3.2,
    (0.765, 0.775, 0.772),
    (0.795, 0.802, 0.798),
    0.30,
    0.39,
    650.0,
    0.10,
    0.00028,
    0.055,
    0.12,
)
ceramic["manufacturing_hypothesis"] = "sintered mineral-ceramic facing / controlled firing variation"

procedural_white(
    mineral,
    11.0,
    (0.635, 0.650, 0.655),
    (0.690, 0.700, 0.702),
    0.47,
    0.60,
    145.0,
    0.17,
    0.00110,
)
mineral["manufacturing_hypothesis"] = "cast/mineral composite service core / low-frequency aggregate response"

procedural_white(
    glaze,
    7.0,
    (0.815, 0.820, 0.812),
    (0.845, 0.848, 0.840),
    0.18,
    0.27,
    340.0,
    0.06,
    0.00010,
    0.15,
    0.075,
)
glaze["manufacturing_hypothesis"] = "maintainable glazed service surface / subtle orange-peel microtexture"

# EPDM-like compressed gasket candidate.
gasket = bpy.data.materials.get("MAT_Elysium_JointGasket_EPDM") or bpy.data.materials.new("MAT_Elysium_JointGasket_EPDM")
_, gasket_bsdf = set_principled(
    gasket,
    base=(0.018, 0.021, 0.022, 1.0),
    rough=0.46,
    metallic=0.0,
)
gasket_bsdf.inputs["IOR"].default_value = 1.47
gasket["material_status"] = "W1_CONSTRUCTION_CANDIDATE"
gasket["role"] = "compressed joint gasket / not decorative black trim"

metal = bpy.data.materials["MAT_Elysium_SatinMetal_PROPOSAL"]
recess = bpy.data.materials["MAT_Elysium_Recess_PROPOSAL"]


def box(name, location, dimensions, material, bevel=0.0):
    old = bpy.data.objects.get(name)
    if old:
        bpy.data.objects.remove(old, do_unlink=True)
    bpy.ops.mesh.primitive_cube_add(location=location)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = dimensions
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.data.materials.append(material)
    move_to(obj, proof)
    if bevel:
        mod = obj.modifiers.new("Bevel_physical", "BEVEL")
        mod.width = bevel
        mod.segments = 3
    return obj


# Complete the existing 16 mm panel-joint construction witness.
gasket_obj = box(
    "MAT_JOINT_GASKET_EPDM",
    (85.004, -86.085, 1.5),
    (0.010, 0.022, 2.86),
    gasket,
    0.0015,
)
gasket_obj["compressed_width_m"] = 0.010
gasket_obj["joint_nominal_width_m"] = 0.016

rail = box(
    "MAT_JOINT_BACKER_RAIL",
    (85.004, -85.96, 1.5),
    (0.042, 0.032, 2.88),
    metal,
    0.003,
)
rail["role"] = "replaceable panel backer/anchor rail proposal"

for z in (0.48, 1.50, 2.52):
    anchor = box(
        f"MAT_JOINT_ANCHOR_{int(z * 100):03d}",
        (85.004, -85.925, z),
        (0.12, 0.026, 0.06),
        metal,
        0.004,
    )
    anchor["role"] = "mechanical anchor witness"
    anchor["spacing_proposal_m"] = 1.02

cavity = box(
    "MAT_JOINT_SERVICE_CAVITY",
    (85.004, -85.99, 1.5),
    (0.085, 0.12, 2.82),
    recess,
    0.002,
)
cavity["role"] = "joint service cavity / shadow depth"

root = bpy.data.objects.get("META_W1_WHITE_MATERIAL_R7")
if not root:
    root = bpy.data.objects.new("META_W1_WHITE_MATERIAL_R7", None)
    proof.objects.link(root)
root["status"] = "MICROSTRUCTURE_AND_JOINT_CANDIDATE"
root["ceramic_face_m"] = 0.012
root["composite_core_m"] = 0.180
root["metal_backer_m"] = 0.004
root["nominal_joint_m"] = 0.016
root["gasket_width_m"] = 0.010
root["principle"] = "intrinsic manufacturing variation only; no generic dirt/scratch noise"
root["engine_material_translation"] = "PENDING"
root["uv_texture_cost"] = "PENDING; current proof procedural-only"

# Keep identical cameras and resolution to permit direct R6/R7 comparison.
scene.render.resolution_x = 960
scene.render.resolution_y = 540
scene.render.resolution_percentage = 100
old_camera = scene.camera
for camera_name, label in (
    ("CAM_MAT_CLOSE", "close"),
    ("CAM_MAT_MID", "mid"),
    ("CAM_MAT_FAR", "far"),
):
    camera = bpy.data.objects.get(camera_name)
    if not camera:
        continue
    scene.camera = camera
    scene.render.filepath = str((__import__("pathlib").Path(__file__).resolve().parent.parent / "generated" / f"elysium_r7_material_{label}.png"))
    bpy.ops.render.render(write_still=True)
scene.camera = old_camera

print({
    "status": "R7_WHITE_MATERIAL_MICROSTRUCTURE_CANDIDATE",
    "ceramic_bump_m": 0.00028,
    "mineral_bump_m": 0.00110,
    "glaze_bump_m": 0.00010,
    "ceramic_face_m": 0.012,
    "core_m": 0.180,
    "backer_m": 0.004,
    "joint_m": 0.016,
    "gasket_m": 0.010,
    "anchor_count": 3,
    "non_claims": [
        "not target-engine material",
        "not UV/texture-budget qualification",
        "not GATE-ART",
        "procedural proof does not define final production shader cost",
    ],
})
