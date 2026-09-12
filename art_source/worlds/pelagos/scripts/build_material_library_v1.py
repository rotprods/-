"""PELAGOS marine PBR foundation library.

Task: PEL/MAT/011
Blender: 5.2+
Units: 1 BU = 1 metre
Status: deterministic material foundation, not final production texture pass.

Important persistence rule learned empirically in 3D Jutsu:
for generated channel maps, create a fresh image datablock, write pixels, save to PNG
(source -> FILE), pack it while retaining filepath provenance, then bind the packed FILE
image to the material. Cold-reopen pixel recovery is the required gate.
"""
import bpy
import math
import os

SIZE = 128
LIBRARY_ID = "PEL-MATLIB-001"

MATERIALS = {
    "CERAMIC": ("PEL_MAT_IvoryCeramic_Marine", (0.63, 0.66, 0.60), 0.05, 0.38, "ceramic", 0.0),
    "BRONZE": ("PEL_MAT_Bronze_Oxidized_Marine", (0.22, 0.18, 0.10), 0.78, 0.42, "bronze", 0.0),
    "COMPOSITE": ("PEL_MAT_DarkTechnicalComposite", (0.025, 0.035, 0.040), 0.08, 0.54, "composite", 0.0),
    "MINERAL": ("PEL_MAT_BlackMineral_Wet", (0.025, 0.033, 0.034), 0.02, 0.62, "mineral", 0.0),
    "TEXTILE": ("PEL_MAT_WaterproofTextile", (0.055, 0.075, 0.072), 0.0, 0.72, "textile", 0.0),
    "CORAL": ("PEL_MAT_LivingCoral_Tissue", (0.19, 0.37, 0.31), 0.0, 0.59, "coral", 0.0),
    "MEMORY": ("PEL_MAT_MemoryCyan_Biolum", (0.018, 0.22, 0.31), 0.03, 0.30, "memory", 2.5),
}


def smoothband(value, center, width):
    return max(0.0, 1.0 - abs(value - center) / max(width, 1e-6))


def causal_fields(u, v):
    salt = smoothband(v, 0.22, 0.10) * (0.5 + 0.5 * math.sin(u * math.tau * 4 + 0.4))
    vertical = max(0.0, math.sin((u * 2 + v * 0.3) * math.tau * 2))
    weave = (0.5 + 0.5 * math.sin(u * math.tau * 18)) * (0.5 + 0.5 * math.sin(v * math.tau * 14))
    vein = max(0.0, 1.0 - abs(math.sin((u * 0.7 + v * 1.3) * math.tau * 3)) * 5.0)
    growth = 0.5 + 0.5 * math.sin((v + 0.12 * math.sin(u * math.tau * 3)) * math.tau * 8)
    return salt, vertical, weave, vein, growth


def base_rgba(u, v, base, pattern):
    br, bg, bb = base
    salt, vertical, weave, vein, growth = causal_fields(u, v)
    if pattern == "bronze":
        p = min(1.0, salt * 0.7 + vertical * 0.25)
        return (br * (1-p) + 0.08*p, bg * (1-p) + 0.31*p, bb * (1-p) + 0.26*p, 1.0)
    if pattern == "ceramic":
        p = min(1.0, salt * 0.45)
        return (br * (1-p) + 0.88*p, bg * (1-p) + 0.90*p, bb * (1-p) + 0.84*p, 1.0)
    if pattern == "mineral":
        return (br + vein*0.022, bg + vein*0.031, bb + vein*0.029, 1.0)
    if pattern == "coral":
        return (br + growth*0.0105, bg + growth*0.015, bb + growth*0.009, 1.0)
    if pattern == "textile":
        return (br + weave*0.0014, bg + weave*0.0018, bb + weave*0.0014, 1.0)
    if pattern == "composite":
        return (br + weave*0.0006, bg + weave*0.00072, bb + weave*0.0008, 1.0)
    if pattern == "memory":
        return (br + growth*0.003, bg + growth*0.012, bb + growth*0.016, 1.0)
    return (br, bg, bb, 1.0)


def rough_rgba(u, v, base_roughness, pattern):
    salt, vertical, weave, vein, growth = causal_fields(u, v)
    r = base_roughness
    if pattern == "bronze": r = min(0.95, max(0.15, r + 0.22*salt - 0.06*vertical))
    elif pattern == "ceramic": r = min(0.92, max(0.18, r + 0.18*salt))
    elif pattern == "mineral": r = min(0.98, max(0.12, r - 0.18*vein + 0.08*salt))
    elif pattern in ("textile", "composite"): r = min(0.98, max(0.22, r + 0.14*weave))
    elif pattern == "coral": r = min(0.95, max(0.25, r + 0.10*growth))
    elif pattern == "memory": r = min(0.80, max(0.12, r - 0.08*growth))
    return (r, r, r, 1.0)


def normal_rgba(u, v, pattern):
    dx = dy = 0.0
    if pattern in ("textile", "composite"):
        dx = 0.045 * math.sin(u * math.tau * 18); dy = 0.040 * math.sin(v * math.tau * 14)
    elif pattern == "coral":
        dx = 0.035 * math.cos((v + u*0.12) * math.tau * 8); dy = 0.055 * math.sin((v + u*0.12) * math.tau * 8)
    elif pattern == "mineral":
        dx = 0.035 * math.sin((u*0.7 + v*1.3) * math.tau * 3); dy = 0.025 * math.cos((u*0.7 + v*1.3) * math.tau * 3)
    elif pattern in ("ceramic", "bronze"):
        dx = 0.018 * math.sin(u * math.tau * 4); dy = 0.012 * math.cos(v * math.tau * 5)
    nz = max(0.75, math.sqrt(max(0.01, 1.0 - dx*dx - dy*dy)))
    return (0.5 + dx*0.5, 0.5 + dy*0.5, 0.5 + nz*0.5, 1.0)


def new_persistent_image(name, fn, noncolor):
    old = bpy.data.images.get(name)
    if old:
        if old.users:
            raise RuntimeError(f"Refuse to replace in-use image {name}; rebind explicitly")
        bpy.data.images.remove(old)
    image = bpy.data.images.new(name, width=SIZE, height=SIZE, alpha=True, float_buffer=False)
    if noncolor:
        image.colorspace_settings.name = "Non-Color"
    pixels = []
    for y in range(SIZE):
        v = y / (SIZE - 1)
        for x in range(SIZE):
            pixels.extend(fn(x / (SIZE - 1), v))
    image.pixels.foreach_set(pixels)
    image.update()
    center = (64 * SIZE + 64) * 4
    sample = [float(image.pixels[center+i]) for i in range(4)]
    if not any(v > 0.05 for v in sample[:3]):
        raise RuntimeError(f"Pixel write failed: {name} {sample}")
    path = os.path.join(bpy.app.tempdir, name + ".png")
    image.filepath_raw = path
    image.file_format = "PNG"
    image.save()  # source becomes FILE
    image.pack()  # packed bytes are authoritative on reopen
    sample_after = [float(image.pixels[center+i]) for i in range(4)]
    if not any(v > 0.05 for v in sample_after[:3]):
        raise RuntimeError(f"Persistence failed before checkpoint: {name} {sample_after}")
    return image


def build_material(key, spec):
    name, base, metallic, roughness, pattern, emission_strength = spec
    base_img = new_persistent_image(
        f"PEL_TEX_{key}_BaseColor_V2",
        lambda u, v: base_rgba(u, v, base, pattern),
        False,
    )
    rough_img = new_persistent_image(
        f"PEL_TEX_{key}_Roughness_PERSIST_V2",
        lambda u, v: rough_rgba(u, v, roughness, pattern),
        True,
    )
    normal_img = new_persistent_image(
        f"PEL_TEX_{key}_Normal_PERSIST_V2",
        lambda u, v: normal_rgba(u, v, pattern),
        True,
    )
    material = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    material.use_nodes = True
    nt = material.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled")
    t_base = nt.nodes.new("ShaderNodeTexImage"); t_base.image = base_img; t_base.label = "Packed BaseColor"
    t_rough = nt.nodes.new("ShaderNodeTexImage"); t_rough.image = rough_img; t_rough.label = "Packed Roughness"
    t_normal = nt.nodes.new("ShaderNodeTexImage"); t_normal.image = normal_img; t_normal.label = "Packed Tangent Normal"
    normal = nt.nodes.new("ShaderNodeNormalMap"); normal.inputs["Strength"].default_value = 0.35
    bsdf.inputs["Metallic"].default_value = metallic
    nt.links.new(t_base.outputs["Color"], bsdf.inputs["Base Color"])
    nt.links.new(t_rough.outputs["Color"], bsdf.inputs["Roughness"])
    nt.links.new(t_normal.outputs["Color"], normal.inputs["Color"])
    nt.links.new(normal.outputs["Normal"], bsdf.inputs["Normal"])
    if emission_strength > 0 and "Emission Color" in bsdf.inputs:
        nt.links.new(t_base.outputs["Color"], bsdf.inputs["Emission Color"])
        bsdf.inputs["Emission Strength"].default_value = emission_strength
    nt.links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])
    material["world"] = "pelagos"
    material["material_library"] = LIBRARY_ID
    material["production_state"] = "PORTABLE_PBR_FOUNDATION"
    material["texture_resolution"] = SIZE
    material["runtime_status"] = "ENGINE_PARITY_PENDING"
    return material


def build():
    built = []
    for key, spec in MATERIALS.items():
        built.append(build_material(key, spec).name)
    return {
        "library": LIBRARY_ID,
        "materials": built,
        "resolution": [SIZE, SIZE],
        "channels": ["BaseColor", "Roughness", "Normal"],
        "required_post_gate": "save/checkpoint -> reopen fresh worker -> force pixel reads -> verify nonzero + node bindings",
        "pending": ["production-resolution bakes", "texel density", "engine shader parity", "texture memory profile", "human art review"],
    }


if __name__ == "__main__":
    print(build())
