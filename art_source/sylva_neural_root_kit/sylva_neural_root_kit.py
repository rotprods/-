"""EXOVANT 2950 — SYLVA PRIME neural-root structural kit.

Claim: CLM-SYLVA-PROC-NROOT-001
Validated remote runtime: Blender 5.2.0 LTS / metric 1 BU = 1 m.

This script is the recoverable source for the first production blockout. It deliberately
models structural/root-route language only; it does not claim final vegetation, VESPER,
characters, terrain, textures, engine integration or final art approval.

Run inside Blender 5.2+:
  blender --background --factory-startup --python sylva_neural_root_kit.py

Outputs are written to ./generated/ next to this script when __file__ is available.
"""

from __future__ import annotations

import math
from pathlib import Path

import bpy
from mathutils import Vector

CLAIM_ID = "CLM-SYLVA-PROC-NROOT-001"
WORLD_ID = "SYLVA-PRIME"
GENERATOR_ID = "SYLVA_NEURAL_ROOT_KIT_V1"
PLAYER_HEIGHT_M = 1.85
PLAYER_RADIUS_M = 0.38

scene = bpy.context.scene

# Clean scene, deterministic hierarchy.
for obj in list(bpy.data.objects):
    bpy.data.objects.remove(obj, do_unlink=True)
for collection in list(bpy.data.collections):
    if collection != scene.collection:
        bpy.data.collections.remove(collection)

scene.unit_settings.system = "METRIC"
scene.unit_settings.scale_length = 1.0
scene.render.engine = "BLENDER_EEVEE"
scene.render.resolution_x = 1100
scene.render.resolution_y = 760
scene.render.resolution_percentage = 100
scene.render.image_settings.media_type = "IMAGE"
scene.render.image_settings.file_format = "PNG"
scene.render.fps = 24
scene.frame_start = 1
scene.frame_end = 1
scene.view_settings.view_transform = "Khronos PBR Neutral"

if not scene.world:
    scene.world = bpy.data.worlds.new("SYLVA Preview World")
scene.world.use_nodes = True
background = scene.world.node_tree.nodes.get("Background")
background.inputs["Color"].default_value = (0.018, 0.026, 0.022, 1)
background.inputs["Strength"].default_value = 0.30

COLLECTIONS: dict[str, bpy.types.Collection] = {}
for name in (
    "00_GUIDES",
    "01_STRUCTURAL_ROOTS",
    "02_CALLOUS_WALK_SURFACES",
    "03_MEMBRANE_INTERFACES",
    "04_COLLISION_PROXIES",
    "90_PREVIEW_RIG",
):
    collection = bpy.data.collections.new(name)
    scene.collection.children.link(collection)
    COLLECTIONS[name] = collection


def move_to(obj: bpy.types.Object, collection_name: str) -> None:
    for collection in list(obj.users_collection):
        collection.objects.unlink(obj)
    COLLECTIONS[collection_name].objects.link(obj)


def material(name: str, color: tuple[float, float, float], roughness: float) -> bpy.types.Material:
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*color, 1)
    bsdf.inputs["Metallic"].default_value = 0.0
    bsdf.inputs["Roughness"].default_value = roughness
    mat.diffuse_color = (*color, 1)
    return mat


BARK = material("SYL_MAT_Bark_Primary", (0.105, 0.155, 0.095), 0.82)
BARK_DRY = material("SYL_MAT_Bark_CallusEdge", (0.28, 0.26, 0.14), 0.72)
CALLOUS = material("SYL_MAT_Traversable_Callus", (0.34, 0.39, 0.21), 0.66)
MEMBRANE = material("SYL_MAT_Membrane_Preview", (0.10, 0.31, 0.20), 0.46)
FLOOR = material("PREVIEW_MAT_Floor", (0.055, 0.065, 0.060), 0.88)
GUIDE = material("PREVIEW_MAT_Guide", (0.62, 0.72, 0.60), 0.55)
COLLISION = material("PREVIEW_MAT_Collision", (0.38, 0.06, 0.04), 0.85)

Z_AXIS = Vector((0, 0, 1))
X_AXIS = Vector((1, 0, 0))


def catmull_rom(
    controls: list[tuple[float, float, float]],
    radii: list[float],
    steps: int = 10,
) -> tuple[list[Vector], list[float]]:
    points = [Vector(point) for point in controls]
    sampled: list[Vector] = []
    sampled_radii: list[float] = []
    for index in range(len(points) - 1):
        p0 = points[max(0, index - 1)]
        p1 = points[index]
        p2 = points[index + 1]
        p3 = points[min(len(points) - 1, index + 2)]
        for step in range(steps):
            t = step / steps
            t2 = t * t
            t3 = t2 * t
            point = 0.5 * (
                (2 * p1)
                + (-p0 + p2) * t
                + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2
                + (-p0 + 3 * p1 - 3 * p2 + p3) * t3
            )
            sampled.append(point)
            sampled_radii.append(radii[index] * (1 - t) + radii[index + 1] * t)
    sampled.append(points[-1])
    sampled_radii.append(radii[-1])
    return sampled, sampled_radii


def root_mesh(
    name: str,
    controls: list[tuple[float, float, float]],
    radii: list[float],
    width_scale: float = 1.0,
    height_scale: float = 0.68,
    sides: int = 18,
    steps: int = 10,
    collection: str = "01_STRUCTURAL_ROOTS",
    mat: bpy.types.Material = BARK,
    collision: bool = False,
) -> tuple[bpy.types.Object, list[Vector], list[float]]:
    path, path_radii = catmull_rom(controls, radii, steps)
    vertices: list[tuple[float, float, float]] = []
    faces: list[tuple[int, ...]] = []

    for index, point in enumerate(path):
        previous = path[max(index - 1, 0)]
        following = path[min(index + 1, len(path) - 1)]
        tangent = following - previous
        if tangent.length < 1e-6:
            tangent = Vector((1, 0, 0))
        tangent.normalize()
        lateral = tangent.cross(Z_AXIS)
        if lateral.length < 1e-4:
            lateral = tangent.cross(X_AXIS)
        lateral.normalize()
        vertical = lateral.cross(tangent).normalized()
        longitudinal = index / max(1, len(path) - 1)

        for side in range(sides):
            angle = math.tau * side / sides
            # Deterministic longitudinal growth ribs: physical morphology, not random noise.
            flute = 1.0 + 0.050 * math.cos(5 * angle + 0.9 * longitudinal) + 0.020 * math.cos(
                2 * angle - 0.45 * longitudinal
            )
            width = path_radii[index] * width_scale * flute
            height = path_radii[index] * height_scale * flute
            vertex = point + lateral * (math.cos(angle) * width) + vertical * (math.sin(angle) * height)
            vertices.append(tuple(vertex))

    rings = len(path)
    for ring in range(rings - 1):
        for side in range(sides):
            a = ring * sides + side
            b = ring * sides + (side + 1) % sides
            c = (ring + 1) * sides + (side + 1) % sides
            d = (ring + 1) * sides + side
            faces.append((a, b, c, d))
    faces.append(tuple(range(sides - 1, -1, -1)))
    offset = (rings - 1) * sides
    faces.append(tuple(offset + side for side in range(sides)))

    mesh = bpy.data.meshes.new(name + "_MESH")
    mesh.from_pydata(vertices, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    COLLECTIONS[collection].objects.link(obj)
    mesh.materials.append(mat)
    for polygon in mesh.polygons:
        polygon.use_smooth = True

    obj["world_id"] = WORLD_ID
    obj["claim_id"] = CLAIM_ID
    obj["generator"] = GENERATOR_ID
    obj["metre_scale"] = 1.0
    obj["status"] = "BLOCKOUT_V1"

    if collision:
        obj.hide_render = True
        obj.display_type = "WIRE"
        obj.color = (0.8, 0.08, 0.04, 1)
        obj["collision_proxy"] = True
    else:
        bevel = obj.modifiers.new("Biological edge continuity", "BEVEL")
        bevel.width = 0.018
        bevel.segments = 2
    return obj, path, path_radii


def traversable_root(
    asset_id: str,
    controls: list[tuple[float, float, float]],
    radii: list[float],
    route_width: float,
    root_width: float = 1.25,
    root_height: float = 0.62,
) -> None:
    _, path, path_radii = root_mesh(
        asset_id,
        controls,
        radii,
        root_width,
        root_height,
        20,
        12,
    )

    vertices: list[tuple[float, float, float]] = []
    faces: list[tuple[int, int, int, int]] = []
    for index, point in enumerate(path):
        previous = path[max(index - 1, 0)]
        following = path[min(index + 1, len(path) - 1)]
        tangent = following - previous
        if tangent.length < 1e-6:
            tangent = Vector((1, 0, 0))
        tangent.normalize()
        lateral = tangent.cross(Z_AXIS)
        if lateral.length < 1e-4:
            lateral = tangent.cross(X_AXIS)
        lateral.normalize()
        vertical = lateral.cross(tangent).normalized()
        top = point + vertical * (path_radii[index] * root_height * 0.89)
        half_width = min(route_width / 2.0, path_radii[index] * root_width * 0.79)
        vertices.extend((tuple(top - lateral * half_width), tuple(top + lateral * half_width)))

    for index in range(len(path) - 1):
        faces.append((2 * index, 2 * index + 1, 2 * index + 3, 2 * index + 2))

    mesh = bpy.data.meshes.new(asset_id + "_CALLOUS_MESH")
    mesh.from_pydata(vertices, [], faces)
    mesh.update()
    deck = bpy.data.objects.new(asset_id + "_CALLOUS", mesh)
    COLLECTIONS["02_CALLOUS_WALK_SURFACES"].objects.link(deck)
    mesh.materials.append(CALLOUS)
    solidify = deck.modifiers.new("Callus thickness", "SOLIDIFY")
    solidify.thickness = 0.085
    solidify.offset = -0.35
    bevel = deck.modifiers.new("Soft crown edge", "BEVEL")
    bevel.width = 0.055
    bevel.segments = 3
    deck["route_width_m"] = route_width
    deck["route_width_status"] = "PROPOSAL"
    deck["player_capsule_reference_height_m"] = PLAYER_HEIGHT_M
    deck["world_id"] = WORLD_ID
    deck["claim_id"] = CLAIM_ID
    deck["generator"] = GENERATOR_ID
    deck["status"] = "BLOCKOUT_V1"

    collision_obj, _, _ = root_mesh(
        "COL_" + asset_id,
        controls,
        radii,
        root_width * 0.92,
        root_height * 0.82,
        8,
        4,
        "04_COLLISION_PROXIES",
        COLLISION,
        True,
    )
    collision_obj["collision_policy"] = "custom_low_poly_root_shell"


def structural_root(
    asset_id: str,
    controls: list[tuple[float, float, float]],
    radii: list[float],
    width: float = 1.0,
    height: float = 0.72,
) -> None:
    root_mesh(asset_id, controls, radii, width, height, 18, 10)
    collision_obj, _, _ = root_mesh(
        "COL_" + asset_id,
        controls,
        radii,
        width * 0.94,
        height * 0.90,
        8,
        4,
        "04_COLLISION_PROXIES",
        COLLISION,
        True,
    )
    collision_obj["collision_policy"] = "custom_low_poly_root_shell"


def label(text: str, location: tuple[float, float, float], size: float = 0.48) -> None:
    curve = bpy.data.curves.new("TXT_" + text, "FONT")
    curve.body = text
    curve.align_x = "CENTER"
    curve.align_y = "CENTER"
    curve.size = size
    curve.extrude = 0.006
    obj = bpy.data.objects.new("LABEL_" + text, curve)
    COLLECTIONS["90_PREVIEW_RIG"].objects.link(obj)
    obj.location = location
    curve.materials.append(GUIDE)


# Preview floor.
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, -0.34))
floor = bpy.context.object
floor.name = "PREVIEW_Ground"
floor.scale = (34, 24, 1)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
move_to(floor, "90_PREVIEW_RIG")
floor.data.materials.append(FLOOR)

# A family: broad traversable roots.
traversable_root("SYL_ROOT_A1_STRAIGHT_08M", [(-15, 8, 0), (-11, 8, 0.2), (-7, 8, 0.05)], [2.0, 2.15, 1.9], 3.2)
label("A1 / STRAIGHT 08M", (-11, 4.9, -0.30))
traversable_root("SYL_ROOT_A2_CURVE_12M", [(-4, 8, 0), (0, 9, 0.25), (3, 12, 0.45), (3.5, 16, 0.2)], [2.0, 2.15, 2.0, 1.75], 3.4)
label("A2 / CURVE 12M", (0, 5.0, -0.30))
traversable_root("SYL_ROOT_A3_RISE_10M", [(8, 8, 0), (11, 8, 1.0), (14, 8, 2.2), (17, 8, 3.4)], [2.1, 2.1, 2.0, 1.8], 3.2)
label("A3 / RISE 10M", (12.5, 4.9, -0.30))

# B1: Y junction with three independently editable load paths.
traversable_root("SYL_ROOT_B1_FORK_TRUNK", [(-15, -1, 0), (-12, -1, 0.1), (-9, -1, 0.35)], [2.2, 2.35, 2.45], 3.5)
traversable_root("SYL_ROOT_B1_FORK_LEFT", [(-9, -1, 0.35), (-6, 0, 0.6), (-3, 3, 0.75)], [2.45, 1.95, 1.65], 3.0)
traversable_root("SYL_ROOT_B1_FORK_RIGHT", [(-9, -1, 0.35), (-6, -2, 0.55), (-3, -5, 0.70)], [2.45, 1.95, 1.65], 3.0)
bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=1, location=(-8.7, -1, 0.45))
fork_node = bpy.context.object
fork_node.name = "SYL_ROOT_B1_FORK_CALLOUS_NODE"
fork_node.scale = (2.75, 2.35, 1.25)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
move_to(fork_node, "01_STRUCTURAL_ROOTS")
fork_node.data.materials.append(BARK_DRY)
for polygon in fork_node.data.polygons:
    polygon.use_smooth = True
fork_node["world_id"] = WORLD_ID
fork_node["claim_id"] = CLAIM_ID
fork_node["generator"] = GENERATOR_ID
fork_node["status"] = "BLOCKOUT_V1"
label("B1 / Y-FORK", (-9, -6.7, -0.30))

# B2 and C1: non-traversable load-bearing forms.
structural_root(
    "SYL_ROOT_B2_ARCH_14M",
    [(0, -4, 0), (2.7, -4, 3.0), (4.8, -4, 6.8), (7, -4, 8.1), (9.2, -4, 6.8), (11.3, -4, 3.0), (14, -4, 0)],
    [1.15, 1.05, 0.9, 0.72, 0.9, 1.05, 1.15],
    1.0,
    0.78,
)
label("B2 / STRUCTURAL ARCH", (7, -7.1, -0.30))
structural_root(
    "SYL_ROOT_C1_BUTTRESS_07M",
    [(17, -4, 0), (16.4, -4, 2.0), (16.1, -4, 4.5), (16.8, -4, 7.2)],
    [1.65, 1.35, 0.95, 0.55],
    1.08,
    0.82,
)
label("C1 / BUTTRESS", (17, -7.2, -0.30))

# C2: three structural roots carrying a grown terrace interface.
for index, (dx, dy) in enumerate(((-2.2, -1.5), (2.2, -1.2), (0, 2.0)), start=1):
    structural_root(
        f"SYL_ROOT_C2_SUPPORT_{index}",
        [(dx - 7, dy - 13, 0), (dx - 7.3, dy - 13, 1.6), (dx - 7, dy - 13, 3.6)],
        [1.25, 1.05, 0.8],
        0.95,
        0.78,
    )

bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=4.3, depth=0.46, location=(-7, -13, 3.82))
terrace = bpy.context.object
terrace.name = "SYL_ROOT_C2_TERRACE_CALLOUS"
move_to(terrace, "03_MEMBRANE_INTERFACES")
terrace.data.materials.append(CALLOUS)
terrace_bevel = terrace.modifiers.new("Grown terrace rim", "BEVEL")
terrace_bevel.width = 0.18
terrace_bevel.segments = 4
terrace["world_id"] = WORLD_ID
terrace["claim_id"] = CLAIM_ID
terrace["generator"] = GENERATOR_ID
terrace["status"] = "PROPOSAL_BLOCKOUT"
terrace["interface"] = "terrace_support_surface"

bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=4.28, depth=0.50, location=terrace.location)
terrace_collision = bpy.context.object
terrace_collision.name = "COL_SYL_ROOT_C2_TERRACE_CALLOUS"
move_to(terrace_collision, "04_COLLISION_PROXIES")
terrace_collision.data.materials.append(COLLISION)
terrace_collision.hide_render = True
terrace_collision.display_type = "WIRE"
terrace_collision["claim_id"] = CLAIM_ID
terrace_collision["collision_proxy"] = True
terrace_collision["collision_policy"] = "primitive_lowpoly_terrace"
label("C2 / TERRACE SUPPORT", (-7, -18.0, -0.30))

# C3: living membrane anchor ring. The membrane material is preview-only.
center = Vector((7, -13, 3.4))
anchor_points: list[tuple[float, float, float]] = []
anchor_radii: list[float] = []
for index in range(13):
    angle = math.tau * index / 12
    anchor_points.append(tuple(center + Vector((3.1 * math.cos(angle), 0, 3.55 * math.sin(angle)))))
    anchor_radii.append(0.46 + 0.06 * math.cos(3 * angle))
anchor, _, _ = root_mesh(
    "SYL_ROOT_C3_MEMBRANE_ANCHOR",
    anchor_points,
    anchor_radii,
    1.0,
    0.9,
    16,
    5,
    "03_MEMBRANE_INTERFACES",
    BARK_DRY,
)
anchor_collision = anchor.copy()
anchor_collision.data = anchor.data.copy()
anchor_collision.name = "COL_SYL_ROOT_C3_MEMBRANE_ANCHOR"
COLLECTIONS["04_COLLISION_PROXIES"].objects.link(anchor_collision)
anchor_collision.data.materials.clear()
anchor_collision.data.materials.append(COLLISION)
decimate = anchor_collision.modifiers.new("Collision simplification", "DECIMATE")
decimate.ratio = 0.28
anchor_collision.hide_render = True
anchor_collision.display_type = "WIRE"
anchor_collision["claim_id"] = CLAIM_ID
anchor_collision["collision_proxy"] = True
anchor_collision["collision_policy"] = "decimated_ring_proxy"

membrane_vertices = [tuple(center)]
for index in range(48):
    angle = math.tau * index / 48
    membrane_vertices.append(tuple(center + Vector((2.72 * math.cos(angle), 0.08, 3.05 * math.sin(angle)))))
membrane_faces = [(0, index + 1, (index + 1) % 48 + 1) for index in range(48)]
membrane_mesh = bpy.data.meshes.new("SYL_MEMBRANE_C3_MESH")
membrane_mesh.from_pydata(membrane_vertices, [], membrane_faces)
membrane_mesh.update()
membrane = bpy.data.objects.new("SYL_MEMBRANE_C3_SURFACE", membrane_mesh)
COLLECTIONS["03_MEMBRANE_INTERFACES"].objects.link(membrane)
membrane_mesh.materials.append(MEMBRANE)
membrane["claim_id"] = CLAIM_ID
membrane["world_id"] = WORLD_ID
membrane["status"] = "PREVIEW_MATERIAL_ONLY"
label("C3 / MEMBRANE ANCHOR", (7, -18.0, -0.30))

# Current prototype player collision guide: scripts/player.gd = 1.85 m height, 0.38 m radius.
cylinder_height = PLAYER_HEIGHT_M - 2 * PLAYER_RADIUS_M
body_center_z = PLAYER_HEIGHT_M / 2
bpy.ops.mesh.primitive_cylinder_add(
    vertices=20,
    radius=PLAYER_RADIUS_M,
    depth=cylinder_height,
    location=(20, 10, body_center_z),
)
player_body = bpy.context.object
player_body.name = "GUIDE_PlayerCapsule_Body"
move_to(player_body, "00_GUIDES")
player_body.data.materials.append(GUIDE)

player_parts = [player_body]
for z_position, suffix in (
    (PLAYER_RADIUS_M, "Bottom"),
    (PLAYER_HEIGHT_M - PLAYER_RADIUS_M, "Top"),
):
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=20,
        ring_count=10,
        radius=PLAYER_RADIUS_M,
        location=(20, 10, z_position),
    )
    sphere = bpy.context.object
    sphere.name = "GUIDE_PlayerCapsule_" + suffix
    move_to(sphere, "00_GUIDES")
    sphere.data.materials.append(GUIDE)
    player_parts.append(sphere)
for part in player_parts:
    part["source"] = "scripts/player.gd"
    part["height_m"] = PLAYER_HEIGHT_M
    part["radius_m"] = PLAYER_RADIUS_M
label("PLAYER 1.85M", (20, 8.4, -0.30), 0.42)

# Preview light rig.
bpy.ops.object.light_add(type="SUN", location=(0, 0, 18))
sun = bpy.context.object
sun.name = "PREVIEW_Sun"
move_to(sun, "90_PREVIEW_RIG")
sun.data.energy = 2.2
sun.rotation_euler = (math.radians(28), math.radians(-18), math.radians(28))

for name, location, energy, color in (
    ("PREVIEW_Key", (-18, -22, 18), 1250, (1.0, 0.82, 0.58)),
    ("PREVIEW_Fill", (20, 8, 12), 900, (0.45, 0.70, 1.0)),
    ("PREVIEW_Rim", (2, 22, 16), 800, (0.55, 1.0, 0.68)),
):
    bpy.ops.object.light_add(type="POINT", location=location)
    light = bpy.context.object
    light.name = name
    move_to(light, "90_PREVIEW_RIG")
    light.data.energy = energy
    light.data.color = color
    light.data.shadow_soft_size = 7.0

bpy.ops.object.camera_add(location=(31, -39, 27))
camera = bpy.context.object
camera.name = "CAM_Delivery_SylvaRootKit"
move_to(camera, "90_PREVIEW_RIG")
camera.data.lens = 38.5
scene.camera = camera
camera.rotation_euler = (Vector((0, -3, 2.2)) - camera.location).to_track_quat("-Z", "Y").to_euler()

# Local outputs. Remote 3D Jutsu stores its own committed .blend/.glb and revision receipts.
try:
    root_dir = Path(__file__).resolve().parent
except NameError:
    root_dir = Path.cwd()
out_dir = root_dir / "generated"
out_dir.mkdir(parents=True, exist_ok=True)

scene.render.filepath = str(out_dir / "sylva-root-kit-blockout.png")
bpy.ops.render.render(write_still=True)
bpy.ops.wm.save_as_mainfile(filepath=str(out_dir / "EXOVANT_SYLVA_Neural_Root_Kit.blend"))
bpy.ops.export_scene.gltf(
    filepath=str(out_dir / "EXOVANT_SYLVA_Neural_Root_Kit.glb"),
    export_format="GLB",
    export_apply=True,
)

print(
    {
        "claim": CLAIM_ID,
        "world": WORLD_ID,
        "objects": len(scene.objects),
        "collision_objects": len([obj for obj in scene.objects if obj.name.startswith("COL_")]),
        "status": "BLOCKOUT_V1",
    }
)
