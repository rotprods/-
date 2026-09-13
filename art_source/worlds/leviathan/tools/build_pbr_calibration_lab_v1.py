"""EXOVANT 2950 — LEVIATHAN portable PBR calibration lab v1.

Isolated deterministic material QA stage for W10/MAT/008.
No external textures. No world-master mutation. No final art/texture-budget claim.
Existing interfaces only: LEV-MAT-001 (living host), LEV-MAT-002 (human graft).
"""

import bpy
import hashlib
import math
import numpy as np
from mathutils import Vector

STAGE = "LEVIATHAN_PBR_CALIBRATION_LAB_V1"
RES = 256

SWATCHES = [
    {
        "name": "LEV_CAL_TISSUE_WARM",
        "family": "LEV-MAT-001",
        "role": "load-bearing living host tissue",
        "base": (0.37, 0.055, 0.050),
        "rough": (0.36, 0.58),
        "metal": 0.0,
        "height_strength": 1.8,
        "pattern": "tissue",
    },
    {
        "name": "LEV_CAL_MUCOSA_WET",
        "family": "LEV-MAT-001",
        "role": "moist pressure/lumen surface",
        "base": (0.24, 0.025, 0.040),
        "rough": (0.10, 0.28),
        "metal": 0.0,
        "height_strength": 1.35,
        "pattern": "mucosa",
    },
    {
        "name": "LEV_CAL_CARTILAGE",
        "family": "LEV-MAT-001",
        "role": "fibrous structural biological frame",
        "base": (0.58, 0.48, 0.36),
        "rough": (0.38, 0.62),
        "metal": 0.0,
        "height_strength": 1.15,
        "pattern": "cartilage",
    },
    {
        "name": "HUM_CAL_IVORY_CERAMIC",
        "family": "LEV-MAT-002",
        "role": "replaceable human graft shell",
        "base": (0.72, 0.69, 0.61),
        "rough": (0.20, 0.34),
        "metal": 0.0,
        "height_strength": 0.55,
        "pattern": "ceramic",
    },
    {
        "name": "HUM_CAL_BRUSHED_METAL",
        "family": "LEV-MAT-002",
        "role": "human technical load frame",
        "base": (0.34, 0.36, 0.38),
        "rough": (0.24, 0.42),
        "metal": 1.0,
        "height_strength": 0.75,
        "pattern": "metal",
    },
    {
        "name": "HUM_CAL_SEAL_RUBBER",
        "family": "LEV-MAT-002",
        "role": "compression gasket / soft technical seal",
        "base": (0.035, 0.040, 0.045),
        "rough": (0.56, 0.78),
        "metal": 0.0,
        "height_strength": 0.70,
        "pattern": "rubber",
    },
]


def _clear_scene():
    for obj in list(bpy.data.objects):
        bpy.data.objects.remove(obj, do_unlink=True)
    for coll in list(bpy.data.collections):
        if coll.name != "Collection":
            bpy.data.collections.remove(coll)
    root = bpy.context.scene.collection
    default = bpy.data.collections.get("Collection")
    if default:
        for obj in list(default.objects):
            default.objects.unlink(obj)
        if default.name in root.children:
            root.children.unlink(default)
        bpy.data.collections.remove(default)
    for m in list(bpy.data.materials):
        bpy.data.materials.remove(m)
    for img in list(bpy.data.images):
        if img.name not in {"Render Result", "Viewer Node"}:
            bpy.data.images.remove(img)


def _collection(name, parent=None):
    c = bpy.data.collections.new(name)
    (parent or bpy.context.scene.collection).children.link(c)
    return c


def _move(obj, coll):
    for c in list(obj.users_collection):
        c.objects.unlink(obj)
    coll.objects.link(obj)
    return obj


def _look_at(obj, target):
    obj.rotation_euler = (Vector(target) - obj.location).to_track_quat("-Z", "Y").to_euler()


def _pattern(spec):
    y, x = np.mgrid[0:RES, 0:RES].astype(np.float32)
    u = x / RES
    v = y / RES
    tau = np.float32(math.tau)
    p = spec["pattern"]

    if p == "tissue":
        macro = 0.55 + 0.23*np.sin(tau*(u*2.0 + 0.14*np.sin(v*tau*2.0))) + 0.12*np.sin(tau*(v*7.0-u*1.5))
        micro = 0.5 + 0.5*np.sin(tau*(u*31.0 + v*23.0)) * np.sin(tau*(v*37.0-u*11.0))
        height = 0.70*macro + 0.30*micro
        color_mod = 0.84 + 0.24*macro
    elif p == "mucosa":
        ridges = 0.5 + 0.5*np.sin(tau*(v*5.0 + 0.18*np.sin(u*tau*3.0)))
        pores = 0.5 + 0.5*np.cos(tau*(u*29.0))*np.cos(tau*(v*31.0))
        height = 0.78*ridges + 0.22*pores
        color_mod = 0.80 + 0.25*ridges
    elif p == "cartilage":
        fibers = 0.5 + 0.5*np.sin(tau*(u*10.0 + 0.09*np.sin(v*tau*4.0)))
        cross = 0.5 + 0.5*np.sin(tau*(v*3.0-u*1.2))
        height = 0.76*fibers + 0.24*cross
        color_mod = 0.88 + 0.18*fibers
    elif p == "ceramic":
        speck = 0.5 + 0.5*np.sin(tau*(u*47.0+v*19.0))*np.sin(tau*(u*13.0-v*43.0))
        broad = 0.5 + 0.5*np.sin(tau*(u*1.0+v*0.7))
        height = 0.30*speck + 0.70*broad
        color_mod = 0.96 + 0.06*speck
    elif p == "metal":
        brush = 0.5 + 0.5*np.sin(tau*(v*96.0 + 0.05*np.sin(u*tau*2.0)))
        broad = 0.5 + 0.5*np.sin(tau*(u*2.0))
        height = 0.86*brush + 0.14*broad
        color_mod = 0.88 + 0.18*brush
    elif p == "rubber":
        stipple = 0.5 + 0.5*np.sin(tau*(u*41.0+v*17.0))*np.cos(tau*(v*37.0-u*7.0))
        wave = 0.5 + 0.5*np.sin(tau*(u*3.0+v*2.0))
        height = 0.70*stipple + 0.30*wave
        color_mod = 0.88 + 0.16*stipple
    else:
        height = np.zeros((RES, RES), dtype=np.float32) + 0.5
        color_mod = np.ones((RES, RES), dtype=np.float32)

    height = np.clip(height, 0.0, 1.0).astype(np.float32)
    color_mod = np.clip(color_mod, 0.0, 1.2).astype(np.float32)
    return u, v, height, color_mod


def _texture_arrays(spec):
    u, v, height, color_mod = _pattern(spec)
    base = np.zeros((RES, RES, 4), dtype=np.float32)
    for i, c in enumerate(spec["base"]):
        base[:, :, i] = np.clip(c * color_mod, 0.0, 1.0)
    base[:, :, 3] = 1.0

    rmin, rmax = spec["rough"]
    rough = rmin + (rmax-rmin) * (0.25 + 0.75*height)
    mr = np.zeros((RES, RES, 4), dtype=np.float32)
    mr[:, :, 0] = 1.0
    mr[:, :, 1] = np.clip(rough, 0.0, 1.0)
    mr[:, :, 2] = spec["metal"]
    mr[:, :, 3] = 1.0

    gy, gx = np.gradient(height)
    strength = np.float32(spec["height_strength"])
    nx = -gx * strength
    ny = -gy * strength
    nz = np.ones_like(height)
    norm = np.sqrt(nx*nx + ny*ny + nz*nz)
    nx /= norm; ny /= norm; nz /= norm
    normal = np.zeros((RES, RES, 4), dtype=np.float32)
    normal[:, :, 0] = nx*0.5 + 0.5
    normal[:, :, 1] = ny*0.5 + 0.5
    normal[:, :, 2] = nz*0.5 + 0.5
    normal[:, :, 3] = 1.0
    return base, mr, normal


def _digest(arr):
    q = np.clip(np.rint(arr*255.0), 0, 255).astype(np.uint8)
    return hashlib.sha256(q.tobytes(order="C")).hexdigest()


def _image(name, arr, non_color=False):
    img = bpy.data.images.new(name, width=RES, height=RES, alpha=True, float_buffer=False)
    img.pixels.foreach_set(arr.reshape(-1))
    img.update()
    try:
        img.colorspace_settings.name = "Non-Color" if non_color else "sRGB"
    except Exception:
        pass
    img.pack()
    img["generator_stage"] = STAGE
    img["resolution"] = RES
    img["sha256_u8_rgba"] = _digest(arr)
    return img


def _material(spec, base_img, mr_img, normal_img):
    m = bpy.data.materials.new(spec["name"])
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    bs = nt.nodes.new("ShaderNodeBsdfPrincipled")
    tex_base = nt.nodes.new("ShaderNodeTexImage")
    tex_base.image = base_img
    tex_base.interpolation = "Linear"
    tex_mr = nt.nodes.new("ShaderNodeTexImage")
    tex_mr.image = mr_img
    tex_mr.interpolation = "Linear"
    sep = nt.nodes.new("ShaderNodeSeparateColor")
    sep.mode = "RGB"
    tex_n = nt.nodes.new("ShaderNodeTexImage")
    tex_n.image = normal_img
    tex_n.interpolation = "Linear"
    nmap = nt.nodes.new("ShaderNodeNormalMap")
    nmap.space = "TANGENT"
    nmap.inputs["Strength"].default_value = 1.0
    nt.links.new(tex_base.outputs["Color"], bs.inputs["Base Color"])
    nt.links.new(tex_mr.outputs["Color"], sep.inputs["Color"])
    nt.links.new(sep.outputs["Green"], bs.inputs["Roughness"])
    nt.links.new(sep.outputs["Blue"], bs.inputs["Metallic"])
    nt.links.new(tex_n.outputs["Color"], nmap.inputs["Color"])
    nt.links.new(nmap.outputs["Normal"], bs.inputs["Normal"])
    nt.links.new(bs.outputs["BSDF"], out.inputs["Surface"])
    bs.inputs["IOR"].default_value = 1.46 if spec["metal"] == 0.0 else 1.50
    m["asset_family"] = spec["family"]
    m["physical_role"] = spec["role"]
    m["roughness_intent_min"] = spec["rough"][0]
    m["roughness_intent_max"] = spec["rough"][1]
    m["metallic_intent"] = spec["metal"]
    m["generator_stage"] = STAGE
    m["production_state"] = "CALIBRATION_PROTOTYPE_NOT_FINAL"
    return m


def _neutral_mat(name, color, rough=0.7):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bs = m.node_tree.nodes.get("Principled BSDF")
    bs.inputs["Base Color"].default_value = (*color, 1.0)
    bs.inputs["Roughness"].default_value = rough
    return m


def build():
    _clear_scene()
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 1.0
    scene.render.engine = "BLENDER_EEVEE"
    scene.render.fps = 24
    scene.render.resolution_x = 960
    scene.render.resolution_y = 540
    scene.render.resolution_percentage = 100

    if scene.world is None:
        scene.world = bpy.data.worlds.new("LEVIATHAN_CAL_WORLD")
    scene.world.use_nodes = True
    bg = scene.world.node_tree.nodes.get("Background")
    bg.inputs["Color"].default_value = (0.015, 0.018, 0.022, 1.0)
    bg.inputs["Strength"].default_value = 0.18

    root = _collection("LEV_PBR_CAL_LAB")
    host = _collection("10_HOST_SWATCHES", root)
    human = _collection("20_HUMAN_GRAFT_SWATCHES", root)
    refs = _collection("80_REFERENCE", root)
    lights = _collection("90_CAMERAS_LIGHTS", root)

    floor_mat = _neutral_mat("CAL_NEUTRAL_FLOOR", (0.055, 0.060, 0.068), 0.82)
    ref_mat = _neutral_mat("CAL_HUMAN_REF", (0.42, 0.46, 0.50), 0.56)

    bpy.ops.mesh.primitive_cube_add(location=(0, 0, -0.12))
    floor = bpy.context.object
    floor.name = "CAL_FLOOR"
    floor.dimensions = (14.0, 8.0, 0.24)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    floor.data.materials.append(floor_mat)
    _move(floor, refs)

    # 1.85 m human scale reference.
    bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=0.24, depth=1.45, location=(-6.1, 2.6, 0.725))
    hbody = bpy.context.object
    hbody.name = "CAL_REF_HUMAN_BODY_1P85M"
    hbody.data.materials.append(ref_mat)
    _move(hbody, refs)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=0.22, location=(-6.1, 2.6, 1.63))
    hhead = bpy.context.object
    hhead.name = "CAL_REF_HUMAN_HEAD"
    hhead.data.materials.append(ref_mat)
    _move(hhead, refs)
    ref_root = bpy.data.objects.new("CAL_REF_HUMAN_1P85M", None)
    refs.objects.link(ref_root)
    ref_root["reference_height_m"] = 1.85

    receipts = []
    xs = [-4.3, 0.0, 4.3]
    ys = [1.8, -1.7]
    for idx, spec in enumerate(SWATCHES):
        base_arr, mr_arr, normal_arr = _texture_arrays(spec)
        base_img = _image(spec["name"] + "_BASECOLOR", base_arr, False)
        mr_img = _image(spec["name"] + "_MR", mr_arr, True)
        normal_img = _image(spec["name"] + "_NORMAL", normal_arr, True)
        mat = _material(spec, base_img, mr_img, normal_img)
        coll = host if spec["family"] == "LEV-MAT-001" else human
        loc = (xs[idx % 3], ys[idx // 3], 0.9)

        bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32, radius=0.82, location=loc)
        sphere = bpy.context.object
        sphere.name = spec["name"] + "_SPHERE"
        sphere.data.materials.append(mat)
        _move(sphere, coll)
        sphere["asset_family"] = spec["family"]
        sphere["calibration_role"] = spec["role"]

        # Grazing-light coupon with enough thickness to avoid single-sided ambiguity.
        bpy.ops.mesh.primitive_cube_add(location=(loc[0], loc[1] + 1.08, 0.72), rotation=(math.radians(62), 0, 0))
        coupon = bpy.context.object
        coupon.name = spec["name"] + "_COUPON"
        coupon.dimensions = (1.45, 0.08, 1.45)
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        coupon.data.materials.append(mat)
        _move(coupon, coll)
        coupon["asset_family"] = spec["family"]
        coupon["calibration_role"] = spec["role"]

        # Text label is reference-only; material identity remains machine-readable on objects.
        bpy.ops.object.text_add(location=(loc[0]-0.95, loc[1]-0.95, 0.10), rotation=(math.radians(90), 0, 0))
        label = bpy.context.object
        label.name = spec["name"] + "_LABEL"
        label.data.body = spec["name"]
        label.data.size = 0.22
        label.data.extrude = 0.004
        label.data.materials.append(ref_mat)
        _move(label, refs)

        receipts.append({
            "name": spec["name"],
            "asset_family": spec["family"],
            "roughness_intent": list(spec["rough"]),
            "metallic_intent": spec["metal"],
            "basecolor_sha256": base_img["sha256_u8_rgba"],
            "mr_sha256": mr_img["sha256_u8_rgba"],
            "normal_sha256": normal_img["sha256_u8_rgba"],
        })

    # Portable lights only.
    sun_data = bpy.data.lights.new("CAL_KEY_SUN_DATA", "SUN")
    sun_data.energy = 2.2
    sun_data.color = (1.0, 0.86, 0.72)
    sun = bpy.data.objects.new("CAL_KEY_SUN", sun_data)
    sun.rotation_euler = (math.radians(38), math.radians(-22), math.radians(-34))
    lights.objects.link(sun)

    point_data = bpy.data.lights.new("CAL_COOL_FILL_DATA", "POINT")
    point_data.energy = 850
    point_data.color = (0.33, 0.52, 1.0)
    point_data.shadow_soft_size = 2.6
    point = bpy.data.objects.new("CAL_COOL_FILL", point_data)
    point.location = (0, -2.0, 5.6)
    lights.objects.link(point)

    spot_data = bpy.data.lights.new("CAL_GRAZE_SPOT_DATA", "SPOT")
    spot_data.energy = 1700
    spot_data.color = (1.0, 0.34, 0.22)
    spot_data.spot_size = math.radians(75)
    spot_data.spot_blend = 0.55
    spot = bpy.data.objects.new("CAL_GRAZE_SPOT", spot_data)
    spot.location = (-5.8, -4.8, 2.3)
    _look_at(spot, (0, 0, 0.75))
    lights.objects.link(spot)

    cam_data = bpy.data.cameras.new("CAM_CAL_OVERVIEW_DATA")
    cam_data.lens = 48
    cam = bpy.data.objects.new("CAM_CAL_OVERVIEW", cam_data)
    cam.location = (0, -12.8, 6.0)
    _look_at(cam, (0, 0.3, 0.75))
    lights.objects.link(cam)

    close_data = bpy.data.cameras.new("CAM_CAL_GRAZE_DATA")
    close_data.lens = 70
    close = bpy.data.objects.new("CAM_CAL_GRAZE", close_data)
    close.location = (0, -6.3, 1.45)
    _look_at(close, (0, -1.1, 0.72))
    lights.objects.link(close)

    scene.camera = cam
    scene["pbr_calibration_stage"] = STAGE
    scene["texture_resolution"] = RES
    scene["final_art_approved"] = False
    scene["world_master_propagation_approved"] = False
    scene["asset_families"] = "LEV-MAT-001,LEV-MAT-002"

    return {
        "stage": STAGE,
        "texture_resolution": RES,
        "swatches": receipts,
        "materials": [s["name"] for s in SWATCHES],
        "images_generated": len(SWATCHES) * 3,
        "packed_images": sum(1 for i in bpy.data.images if getattr(i, "packed_file", None)),
        "objects": len(bpy.context.scene.objects),
        "status": "CALIBRATION_PROTOTYPE_NOT_FINAL",
    }


if __name__ == "__main__":
    print(build())
