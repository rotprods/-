"""EXOVANT 2950 — ELYSIUM NULL foundation generator.

ART-ELYSIUM-001 / FOUNDATION_WAVE_0
Blender target observed during qualification: 5.2.0 LTS.
Units: metric, 1 BU = 1 metre.

Canon anchor used by geometry:
- EDEN arena diameter = 48 m.

All other scene dimensions are reversible production proposals and MUST NOT be
promoted to project canon merely because this generator creates them.

Run example:
  blender --background --factory-startup --python generate_foundation.py

The script intentionally has no network dependency and uses portable Principled
materials. 3D Jutsu automatically persists .blend and GLB; standalone Blender
also writes a .blend and GLB beside this script under ../generated/.
"""

from pathlib import Path
import math
import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "generated"
OUT.mkdir(parents=True, exist_ok=True)

scene = bpy.context.scene
scene.unit_settings.system = "METRIC"
scene.unit_settings.scale_length = 1.0
scene.render.engine = "BLENDER_EEVEE"
scene.render.resolution_x = 1280
scene.render.resolution_y = 720
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "PNG"

if scene.world is None:
    scene.world = bpy.data.worlds.new("WORLD_Elysium_Null")
scene.world.use_nodes = True
bg = scene.world.node_tree.nodes.get("Background")
bg.inputs["Color"].default_value = (0.035, 0.045, 0.055, 1.0)
bg.inputs["Strength"].default_value = 0.32

for obj in list(bpy.data.objects):
    bpy.data.objects.remove(obj, do_unlink=True)


def collection(name):
    c = bpy.data.collections.get(name) or bpy.data.collections.new(name)
    if scene.collection.children.get(c.name) is None:
        scene.collection.children.link(c)
    return c


COL = {
    name: collection(name)
    for name in (
        "00_REFERENCE",
        "10_AVENIDA",
        "20_ARCOLOGY",
        "30_GARDENS",
        "40_EDEN",
        "50_HUMAN_TRACE",
        "90_LIGHTS_CAM",
    )
}


def move_to(obj, target):
    for old in list(obj.users_collection):
        old.objects.unlink(obj)
    target.objects.link(obj)


def material(name, base, metallic=0.0, roughness=0.45, emission=None, strength=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*base, 1.0)
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = roughness
    if emission:
        bsdf.inputs["Emission Color"].default_value = (*emission, 1.0)
        bsdf.inputs["Emission Strength"].default_value = strength
    return m


WHITE = material("MAT_Elysium_WhiteCeramic_PROPOSAL", (0.78, 0.80, 0.80), roughness=0.28)
WHITE_MATTE = material("MAT_Elysium_WhiteMineral_PROPOSAL", (0.62, 0.65, 0.65), roughness=0.62)
DARK = material("MAT_Elysium_Recess_PROPOSAL", (0.012, 0.016, 0.020), metallic=0.15, roughness=0.28)
METAL = material("MAT_Elysium_SatinMetal_PROPOSAL", (0.25, 0.28, 0.30), metallic=0.75, roughness=0.24)
GREEN = material("MAT_Elysium_Garden_PROPOSAL", (0.095, 0.22, 0.13), roughness=0.66)
SOIL = material("MAT_Elysium_Substrate_PROPOSAL", (0.07, 0.055, 0.045), roughness=0.88)
AMBER = material(
    "MAT_Elysium_ServiceAmber_PROPOSAL",
    (0.38, 0.12, 0.02),
    metallic=0.15,
    roughness=0.34,
    emission=(1.0, 0.22, 0.035),
    strength=3.5,
)
HUMAN = material("MAT_HumanTrace_Repaired_PROPOSAL", (0.22, 0.07, 0.035), metallic=0.55, roughness=0.48)
PROXY = material("MAT_ScaleProxy", (0.18, 0.32, 0.65), roughness=0.55)


def box(name, location, dimensions, mat, target, bevel=0.0):
    bpy.ops.mesh.primitive_cube_add(location=location)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = dimensions
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.data.materials.append(mat)
    move_to(obj, target)
    if bevel:
        mod = obj.modifiers.new("Bevel_physical", "BEVEL")
        mod.width = bevel
        mod.segments = 3
    return obj


def cylinder(name, location, radius, depth, mat, target, vertices=48):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=location)
    obj = bpy.context.object
    obj.name = name
    obj.data.materials.append(mat)
    move_to(obj, target)
    return obj


def sphere(name, location, radius, mat, target):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=radius, location=location)
    obj = bpy.context.object
    obj.name = name
    obj.data.materials.append(mat)
    move_to(obj, target)
    return obj


def torus(name, location, major_radius, minor_radius, mat, target, rotation=(0, 0, 0)):
    bpy.ops.mesh.primitive_torus_add(
        major_radius=major_radius,
        minor_radius=minor_radius,
        major_segments=64,
        minor_segments=16,
        location=location,
        rotation=rotation,
    )
    obj = bpy.context.object
    obj.name = name
    obj.data.materials.append(mat)
    move_to(obj, target)
    return obj


def look_at(obj, target):
    obj.rotation_euler = (Vector(target) - obj.location).to_track_quat("-Z", "Y").to_euler()


# Scale witness: 1.85 m human reference.
cylinder("REF_HUMAN_1p85m", (0, -112, 0.925), 0.26, 1.85, PROXY, COL["00_REFERENCE"], 24)
box("REF_HUMAN_SHOULDERS", (0, -112, 1.48), (0.68, 0.28, 0.28), PROXY, COL["00_REFERENCE"], 0.05)

# Avenida del Recibimiento representative authored cell — PROPOSAL.
box("AVN_BASE_260x72m", (0, 0, -0.45), (72, 260, 0.9), WHITE_MATTE, COL["10_AVENIDA"], 0.12)
box("AVN_WALKWAY_CENTER", (0, -8, 0.04), (22, 232, 0.16), WHITE, COL["10_AVENIDA"], 0.04)
box("AVN_TRAM_RECESS", (0, -8, 0), (5.8, 232, 0.10), DARK, COL["10_AVENIDA"])
for x in (-1.85, 1.85):
    box(f"TRAM_RAIL_{x:+.2f}", (x, -8, 0.12), (0.16, 232, 0.22), METAL, COL["10_AVENIDA"], 0.04)
for x in (-10.9, 10.9):
    box(f"SERVICE_LINE_{x:+.1f}", (x, -8, 0.15), (0.08, 232, 0.12), AMBER, COL["10_AVENIDA"], 0.02)

# Arcology repetition: mass / reveal / service spine / canopy.
ys = [-90, -58, -26, 6, 38, 70]
heights = [28, 34, 40, 34, 40, 46]
for side in (-1, 1):
    sx = side * 25
    side_name = "W" if side < 0 else "E"
    for i, (y, h) in enumerate(zip(ys, heights)):
        pre = f"ARC_{side_name}_{i:02d}"
        box(pre + "_CORE", (sx, y, h / 2), (14, 19, h), WHITE, COL["20_ARCOLOGY"], 0.42)
        box(pre + "_REVEAL", (sx - side * 7.15, y, 5.2), (0.32, 13.5, 7.2), DARK, COL["20_ARCOLOGY"], 0.06)
        box(pre + "_SPINE", (sx + side * 6.65, y, 0.8 + h * 0.48), (0.38, 3, h * 0.82), METAL, COL["20_ARCOLOGY"], 0.08)
        box(pre + "_CANOPY", (sx - side * 5.8, y - 5.5, 5.6), (8.2, 4, 0.42), WHITE, COL["20_ARCOLOGY"], 0.14)

for i, y in enumerate((-42, 22, 62)):
    z = (15, 20, 24)[i]
    box(f"ARC_BRIDGE_{i:02d}", (0, y, z), (35, 3.2, 2.4), WHITE, COL["20_ARCOLOGY"], 0.34)
    box(f"ARC_BRIDGE_GAP_{i:02d}", (0, y, z - 0.1), (26.5, 3.3, 0.28), DARK, COL["20_ARCOLOGY"])

# Repeated garden grammar. Slight deterministic plant-height changes remain explicit proposals.
for garden_i, y in enumerate((-76, -44, -12, 20, 52)):
    for side in (-1, 1):
        x = side * 12.8
        box(f"GARDEN_{garden_i:02d}_{side:+d}_BED", (x, y, 0.55), (6.8, 10, 1), WHITE, COL["30_GARDENS"], 0.25)
        box(f"GARDEN_{garden_i:02d}_{side:+d}_SOIL", (x, y, 1.08), (5.9, 9.1, 0.16), SOIL, COL["30_GARDENS"], 0.05)
        for plant_i, dy in enumerate((-2.8, 0, 2.8)):
            radius = 1.1 + 0.15 * ((garden_i + plant_i) % 3)
            sphere(
                f"GARDEN_{garden_i:02d}_{side:+d}_PLANT_{plant_i}",
                (x, y + dy, 1.35 + radius * 0.62),
                radius,
                GREEN,
                COL["30_GARDENS"],
            )

# Canonical custodian-tram concept; dimensions are proposal.
box("VEH_TRAM_CUSTODIAN_PROXY", (0, -61, 1.35), (4.3, 12, 2.6), WHITE, COL["10_AVENIDA"], 0.45)
box("VEH_TRAM_WINDOW_BAND", (0, -61, 1.8), (4.34, 7.2, 0.62), DARK, COL["10_AVENIDA"], 0.08)

# EDEN arena — CANONICAL 48 m diameter.
cylinder("EDEN_ARENA_48M_CANON", (0, 108, -0.05), 24, 0.55, WHITE, COL["40_EDEN"], 96)
torus("EDEN_ARENA_BOUNDARY", (0, 108, 0.35), 23.2, 0.32, METAL, COL["40_EDEN"])

for i, (x, y) in enumerate(((-10, 101), (10, 101), (-10, 115), (10, 115))):
    box(f"EDEN_MOVABLE_GARDEN_{i:02d}", (x, y, 0.8), (8, 8, 1.4), WHITE, COL["40_EDEN"], 0.28)
    box(f"EDEN_MOVABLE_GARDEN_{i:02d}_SOIL", (x, y, 1.54), (7.1, 7.1, 0.14), SOIL, COL["40_EDEN"])
    sphere(f"EDEN_MOVABLE_GARDEN_{i:02d}_TOPIARY", (x, y, 3), 1.55, GREEN, COL["40_EDEN"])

# EDEN is only a silhouette/control-axis proxy in W0, not a boss production model.
cylinder("EDEN_CORE_PROXY", (0, 108, 8), 2.8, 16, WHITE, COL["40_EDEN"], 64)
torus("EDEN_HALO_PROXY", (0, 108, 16.2), 5.8, 0.42, AMBER, COL["40_EDEN"], (math.radians(90), 0, 0))
for i, (x, y, dimensions) in enumerate(
    (
        (8.8, 108, (0.55, 7, 4.4)),
        (-8.8, 108, (0.55, 7, 4.4)),
        (0, 116.8, (7, 0.55, 4.4)),
        (0, 99.2, (7, 0.55, 4.4)),
    )
):
    box(f"EDEN_BARRIER_PROXY_{i:02d}", (x, y, 2.2), dimensions, WHITE, COL["40_EDEN"], 0.16)

# Carefully localized human anomaly: one repaired public object, not global grime.
box("TRACE_REPAIRED_BENCH_SEAT", (-8.6, -25.5, 0.82), (3.8, 0.62, 0.18), HUMAN, COL["50_HUMAN_TRACE"], 0.06)
box("TRACE_REPAIRED_BENCH_LEG_A", (-10, -25.5, 0.42), (0.18, 0.48, 0.82), HUMAN, COL["50_HUMAN_TRACE"], 0.04)
box("TRACE_REPAIRED_BENCH_LEG_B", (-7.1, -25.38, 0.36), (0.18, 0.48, 0.68), HUMAN, COL["50_HUMAN_TRACE"], 0.04)
box("TRACE_REPAIR_PATCH", (-8.15, -25.16, 0.94), (0.72, 0.07, 0.30), AMBER, COL["50_HUMAN_TRACE"], 0.03)
fragment = box("TRACE_DISPLACED_FRAGMENT", (-6.35, -24.8, 0.18), (0.42, 0.24, 0.16), HUMAN, COL["50_HUMAN_TRACE"], 0.02)
fragment.rotation_euler[2] = math.radians(17)

# Arrival thresholds.
for y in (-104, -6, 82):
    for x in (-9.5, 9.5):
        box(f"GATE_{y}_{x:+.1f}_PIER", (x, y, 5), (1, 1.5, 10), WHITE, COL["10_AVENIDA"], 0.22)
    box(f"GATE_{y}_BEAM", (0, y, 9.6), (20, 1.5, 0.9), WHITE, COL["10_AVENIDA"], 0.22)

# Delivery camera + motivated artificial-source lighting.
bpy.ops.object.camera_add(location=(72, -145, 52))
camera = bpy.context.object
camera.name = "CAM_DELIVERY_FOUNDATION"
camera.data.lens = 43
camera.data.sensor_width = 36
look_at(camera, (0, 26, 7))
scene.camera = camera
move_to(camera, COL["90_LIGHTS_CAM"])

bpy.ops.object.light_add(type="SUN", location=(20, -30, 70))
sun = bpy.context.object
sun.name = "LGT_ARTIFICIAL_SOURCE_KEY"
sun.data.energy = 2.2
sun.rotation_euler = (math.radians(28), math.radians(-20), math.radians(-35))
move_to(sun, COL["90_LIGHTS_CAM"])

for name, location, energy, color in (
    ("LGT_EDEN_WARM", (0, 102, 22), 950, (1.0, 0.34, 0.10)),
    ("LGT_ENTRY_FILL", (0, -92, 16), 700, (0.56, 0.72, 1.0)),
):
    bpy.ops.object.light_add(type="POINT", location=location)
    light = bpy.context.object
    light.name = name
    light.data.energy = energy
    light.data.color = color
    light.data.shadow_soft_size = 7
    move_to(light, COL["90_LIGHTS_CAM"])

# Deterministic outputs for standalone execution.
preview = OUT / "elysium_foundation_v1.png"
blend = OUT / "elysium_foundation_v1.blend"
glb = OUT / "elysium_foundation_v1.glb"
scene.render.filepath = str(preview)
bpy.ops.render.render(write_still=True)
bpy.ops.wm.save_as_mainfile(filepath=str(blend))
bpy.ops.export_scene.gltf(filepath=str(glb), export_format="GLB")

meshes = [obj for obj in bpy.data.objects if obj.type == "MESH"]
print(
    {
        "world": "ELYSIUM NULL",
        "status": "FOUNDATION_BLOCKOUT_V1",
        "objects": len(bpy.data.objects),
        "meshes": len(meshes),
        "vertices": sum(len(obj.data.vertices) for obj in meshes),
        "polygons": sum(len(obj.data.polygons) for obj in meshes),
        "canonical_eden_diameter_m": 48.0,
        "proposal_route_m": 260.0,
        "proposal_district_width_m": 72.0,
        "human_reference_m": 1.85,
        "blend": str(blend),
        "glb": str(glb),
        "preview": str(preview),
    }
)
