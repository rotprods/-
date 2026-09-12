#!/usr/bin/env python3
"""EXOVANT 2950 / WORLD-04 UMBRA / WAVE-0 generator.

Repository source corresponding to the executed remote blockout logic from
3D Jutsu project 7ab99682-8777-4143-8ae0-1fbb178ccafb revision 1.

The committed remote revision is the execution receipt. This repository copy
must be replay-tested before claiming byte/geometry identity with that revision.
No external files, network calls, textures, or absolute asset paths are used.
"""

import bpy
import math
import os
import sys
from mathutils import Vector

WORLD_ID = "WORLD-04"
CLAIM_ID = "CLM-W04-WORLD-UMBRA-001"
AGENT_ID = "AGENT-UMBRA-04"
REGION_X = 1200.0
REGION_Y = 700.0


def args_after_double_dash():
    if "--" not in sys.argv:
        return []
    return sys.argv[sys.argv.index("--") + 1 :]


def arg_value(flag, default=None):
    args = args_after_double_dash()
    if flag in args and args.index(flag) + 1 < len(args):
        return args[args.index(flag) + 1]
    return default


def reset_scene(scene):
    for obj in list(bpy.data.objects):
        bpy.data.objects.remove(obj, do_unlink=True)
    for coll in list(bpy.data.collections):
        if coll.name != scene.collection.name:
            bpy.data.collections.remove(coll)


def move_to(obj, collection):
    for c in list(obj.users_collection):
        c.objects.unlink(obj)
    collection.objects.link(obj)
    return obj


def material(name, base, metallic=0.0, roughness=0.5, emission=None, emission_strength=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*base, 1.0)
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = roughness
    if emission is not None:
        bsdf.inputs["Emission Color"].default_value = (*emission, 1.0)
        bsdf.inputs["Emission Strength"].default_value = emission_strength
    return m


def build():
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 1.0
    scene.render.engine = "BLENDER_EEVEE"
    scene.render.resolution_x = 960
    scene.render.resolution_y = 540
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.film_transparent = False
    scene.render.fps = 24

    if scene.world is None:
        scene.world = bpy.data.worlds.new("WORLD_UMBRA_TWILIGHT")
    scene.world.use_nodes = True
    bg = scene.world.node_tree.nodes.get("Background")
    bg.inputs["Color"].default_value = (0.006, 0.012, 0.028, 1.0)
    bg.inputs["Strength"].default_value = 0.16

    reset_scene(scene)

    root = bpy.data.collections.new("W04_UMBRA")
    scene.collection.children.link(root)
    collections = {}
    for name in [
        "00_GUIDES",
        "10_TERRAIN",
        "20_INFRASTRUCTURE",
        "30_CARAVAN",
        "40_NOCTIL_ARENA",
        "50_LIGHTS",
        "60_CAMERAS",
        "90_VALIDATION",
    ]:
        c = bpy.data.collections.new(name)
        root.children.link(c)
        collections[name] = c

    mats = {
        "ice": material("MAT_UMBRA_DARK_ICE", (0.018, 0.028, 0.05), 0.05, 0.28),
        "ice_edge": material("MAT_UMBRA_ICE_EDGE", (0.055, 0.085, 0.13), 0.0, 0.18),
        "fabric": material("MAT_SINSOL_TENSION_FABRIC", (0.055, 0.05, 0.052), 0.0, 0.72),
        "metal": material("MAT_SINSOL_DARK_METAL", (0.045, 0.052, 0.058), 0.78, 0.34),
        "mirror": material("MAT_REFLECTOR_MIRROR", (0.28, 0.32, 0.36), 0.92, 0.08),
        "ivory": material("MAT_COLONIAL_IVORY_REPAIR", (0.42, 0.40, 0.34), 0.06, 0.45),
        "amber": material("MAT_REFUGE_AMBER", (0.32, 0.115, 0.014), 0.0, 0.30, (1.0, 0.29, 0.03), 5.0),
        "red": material("MAT_HOSTILE_VERMILION", (0.28, 0.01, 0.008), 0.0, 0.35, (0.95, 0.018, 0.008), 4.0),
        "guide": material("MAT_GUIDE", (0.08, 0.32, 0.9), 0.0, 0.40),
    }

    def cube(name, loc, scale, mat=None, coll="20_INFRASTRUCTURE", bevel=0.0, rot=(0, 0, 0)):
        bpy.ops.mesh.primitive_cube_add(location=loc, rotation=rot)
        o = bpy.context.object
        o.name = name
        o.scale = scale
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        if bevel > 0:
            mod = o.modifiers.new("BEVEL_PHYSICAL", "BEVEL")
            mod.width = bevel
            mod.segments = 2
        if mat:
            o.data.materials.append(mat)
        return move_to(o, collections[coll])

    def cyl(name, loc, radius, depth, mat=None, coll="20_INFRASTRUCTURE", rot=(0, 0, 0), verts=20):
        bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=radius, depth=depth, location=loc, rotation=rot)
        o = bpy.context.object
        o.name = name
        if mat:
            o.data.materials.append(mat)
        return move_to(o, collections[coll])

    def look_at(obj, target):
        obj.rotation_euler = (Vector(target) - obj.location).to_track_quat("-Z", "Y").to_euler()

    meta = bpy.data.objects.new("GUIDE_PLANETARY_METADATA__RADIUS_UNKNOWN", None)
    collections["00_GUIDES"].objects.link(meta)
    meta["epistemic"] = "CANON+BLOCKED"
    meta["world_id"] = WORLD_ID
    meta["world_name"] = "UMBRA"
    meta["planet_radius_m"] = "UNKNOWN"
    meta["world_condition"] = "tidally_locked_twilight_band"
    meta["faction"] = "Flotilla de los Sin Sol"
    meta["claim_id"] = CLAIM_ID

    region = bpy.data.objects.new("GUIDE_REGION_TWILIGHT_TESTBED_1200x700m", None)
    collections["00_GUIDES"].objects.link(region)
    region["epistemic"] = "PROPOSAL"
    region["authored_extent_m"] = "1200x700"
    region["purpose"] = "WAVE0 authored testbed; not total planetary surface"

    nx, ny = 49, 33
    verts, faces = [], []
    for j in range(ny):
        y = -REGION_Y / 2 + REGION_Y * j / (ny - 1)
        for i in range(nx):
            x = -REGION_X / 2 + REGION_X * i / (nx - 1)
            z = (
                1.8 * math.sin(x * 0.011)
                + 1.25 * math.cos(y * 0.017)
                + 0.75 * math.sin((x + y) * 0.009)
                + 7.5 * math.exp(-((y - 250.0) / 120.0) ** 2) * (0.25 + 0.75 * math.sin(x * 0.009) ** 2)
                - 4.2 * math.exp(-((x - 210.0) / 160.0) ** 2 - ((y + 120.0) / 130.0) ** 2)
            )
            verts.append((x, y, z))
    for j in range(ny - 1):
        for i in range(nx - 1):
            a = j * nx + i
            faces.append((a, a + 1, a + nx + 1, a + nx))
    mesh = bpy.data.meshes.new("MESH_UMBRA_TWILIGHT_TERRAIN")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    terrain = bpy.data.objects.new("ENV_TERRAIN_TWILIGHT_BAND_BLOCKOUT", mesh)
    collections["10_TERRAIN"].objects.link(terrain)
    terrain.data.materials.append(mats["ice"])
    terrain["epistemic"] = "PROPOSAL"

    for idx, x in enumerate([-520, -390, -250, -80, 120, 300, 475]):
        h = 28 + (idx % 3) * 10
        o = cube(
            f"ENV_ICE_RIDGE_{idx:02d}",
            (x, 255, h * 0.42),
            (55, 24, h * 0.42),
            mats["ice_edge"],
            "10_TERRAIN",
            2.0,
            (0, math.radians((idx % 2) * 4 - 2), math.radians(8 + idx * 3)),
        )
        o["wear_causality"] = "windward_ice_ablation"

    route = [
        (-430, -165, 0.8, 110, 14, 0.5, -7),
        (-230, -130, 0.7, 105, 14, 0.5, 4),
        (-25, -95, 0.4, 105, 14, 0.5, -6),
        (180, -55, 0.3, 105, 14, 0.5, 7),
        (390, -5, 0.4, 120, 14, 0.5, 9),
    ]
    for i, (x, y, z, sx, sy, sz, ang) in enumerate(route):
        o = cube(
            f"INFRA_ROUTE_HARDPACK_{i:02d}",
            (x, y, z),
            (sx, sy, sz),
            mats["ice_edge"],
            "20_INFRASTRUCTURE",
            0.35,
            (0, 0, math.radians(ang)),
        )
        o["function"] = "mobile settlement traversal spine"

    def reflector(idx, x, y, h, yaw, pitch=-22):
        cyl(f"INFRA_REFLECTOR_{idx:02d}_MAST", (x, y, h / 2), 2.2, h, mats["metal"])
        cyl(f"INFRA_REFLECTOR_{idx:02d}_COLLAR", (x, y, h - 4), 3.4, 1.6, mats["ivory"])
        panel = cube(
            f"INFRA_REFLECTOR_{idx:02d}_MIRROR",
            (x, y, h + 1),
            (9.5, 0.55, 6.2),
            mats["mirror"],
            bevel=0.4,
            rot=(math.radians(pitch), 0, math.radians(yaw)),
        )
        panel["function"] = "twilight solar/thermal redirection"
        panel["epistemic"] = "PROPOSAL_FROM_CANON_FUNCTION"
        cyl(f"INFRA_REFLECTOR_{idx:02d}_AMBER_BEACON", (x, y, h + 8), 0.55, 1.4, mats["amber"], verts=16)

    for spec in [(0, -455, 80, 62, 16), (1, -150, 145, 78, -8), (2, 170, 115, 68, 12), (3, 455, 165, 86, -12)]:
        reflector(*spec)

    for i, x in enumerate(range(-500, 501, 125)):
        p = cube(f"INFRA_WINDBREAK_PYLON_{i:02d}", (x, 8, 9), (2.2, 2.2, 9), mats["metal"], bevel=0.4)
        p["function"] = "anchor for tensioned windbreak / constant lateral wind"

    def caravan(idx, x, y, yaw):
        z = 5.5
        rot = (0, 0, math.radians(yaw))
        chassis = cube(f"CARAVAN_{idx:02d}_CHASSIS", (x, y, z), (7.8, 3.2, 1.35), mats["metal"], "30_CARAVAN", 0.55, rot)
        cube(f"CARAVAN_{idx:02d}_CABIN", (x - 1.2, y, z + 2.7), (4.8, 2.8, 1.6), mats["ivory"], "30_CARAVAN", 0.7, rot)
        cube(
            f"CARAVAN_{idx:02d}_TENSION_CANOPY",
            (x + 2.4, y, z + 4.8),
            (3.3, 3.35, 0.22),
            mats["fabric"],
            "30_CARAVAN",
            0.35,
            (math.radians(-5), 0, math.radians(yaw)),
        )
        for side in (-1, 1):
            cube(f"CARAVAN_{idx:02d}_TRACK_{side:+d}", (x, y + side * 3.7, z - 1.4), (7.4, 0.8, 0.7), mats["metal"], "30_CARAVAN", 0.45, rot)
        cyl(f"CARAVAN_{idx:02d}_REFUGE_BEACON", (x - 4.9, y, z + 5.2), 0.35, 1.1, mats["amber"], "30_CARAVAN", verts=14)
        chassis["function"] = "mobile twilight settlement"
        chassis["manufacturing"] = "welded modular chassis / field repaired shell"

    for i, spec in enumerate([(-365, -165, -6), (-210, -132, 4), (-60, -104, -5), (105, -78, 6), (270, -38, 7)]):
        caravan(i, *spec)

    cube("ARCH_REFUGE_HUB_BASE", (72, 35, 6), (22, 15, 6), mats["ivory"], bevel=1.2, rot=(0, 0, math.radians(8)))
    cube("ARCH_REFUGE_HUB_WIND_SHELL", (72, 35, 15.5), (24, 17, 1.2), mats["fabric"], bevel=0.8, rot=(math.radians(-4), 0, math.radians(8)))
    for k, dx in enumerate((-14, 0, 14)):
        cyl(f"ARCH_REFUGE_HUB_AMBER_{k}", (72 + dx, 20, 13), 0.5, 1.8, mats["amber"], verts=14)

    bpy.ops.mesh.primitive_torus_add(
        major_radius=46,
        minor_radius=2.2,
        major_segments=48,
        minor_segments=12,
        location=(385, 245, 34),
        rotation=(math.radians(90), 0, math.radians(-12)),
    )
    ring = bpy.context.object
    ring.name = "BOSS_NOCTIL_ECLIPSE_RING_PROXY"
    ring.data.materials.append(mats["metal"])
    move_to(ring, collections["40_NOCTIL_ARENA"])
    ring["epistemic"] = "PROPOSAL_PROXY_ONLY"
    ring["not_final"] = "NOCTIL anatomy/rig/attack design"

    for i, angle in enumerate(range(0, 360, 45)):
        r = math.radians(angle)
        x = 385 + 62 * math.cos(r)
        y = 245 + 62 * math.sin(r)
        cube(f"BOSS_ARENA_ANCHOR_{i:02d}", (x, y, 4.5), (4, 4, 4.5), mats["metal"], "40_NOCTIL_ARENA", 0.55, (0, 0, r))
    cyl("BOSS_ARENA_HOSTILE_SIGNAL", (385, 245, 8), 1.2, 16, mats["red"], "40_NOCTIL_ARENA", verts=18)

    human = cyl("VALIDATION_HUMAN_1P75M", (-525, -250, 0.875), 0.22, 1.75, mats["guide"], "90_VALIDATION", verts=16)
    human["height_m"] = 1.75
    rover = cube("VALIDATION_ROVER_4P6M", (-500, -238, 1.0), (2.3, 1.05, 1.0), mats["guide"], "90_VALIDATION", 0.25)
    rover["length_m"] = 4.6

    bpy.ops.object.light_add(type="SUN", location=(-300, -500, 350))
    sun = bpy.context.object
    sun.name = "LIGHT_SERE_TWILIGHT_KEY"
    sun.data.energy = 2.2
    sun.data.color = (0.78, 0.19, 0.065)
    sun.rotation_euler = (math.radians(74), math.radians(-8), math.radians(-28))
    move_to(sun, collections["50_LIGHTS"])

    bpy.ops.object.light_add(type="SUN", location=(300, 500, 250))
    fill = bpy.context.object
    fill.name = "LIGHT_COLD_HORIZON_FILL"
    fill.data.energy = 0.55
    fill.data.color = (0.14, 0.23, 0.48)
    fill.rotation_euler = (math.radians(84), math.radians(18), math.radians(145))
    move_to(fill, collections["50_LIGHTS"])

    for i, (x, y, z) in enumerate([(-365, -165, 11), (-60, -104, 11), (105, -78, 11), (72, 20, 16), (385, 245, 22)]):
        bpy.ops.object.light_add(type="POINT", location=(x, y, z))
        light = bpy.context.object
        light.name = f"LIGHT_LOCAL_{i:02d}"
        light.data.energy = 900 if i < 4 else 500
        light.data.color = (1.0, 0.20, 0.045) if i < 4 else (0.9, 0.02, 0.01)
        light.data.shadow_soft_size = 5.0
        move_to(light, collections["50_LIGHTS"])

    bpy.ops.object.camera_add(location=(430, -610, 165))
    cam = bpy.context.object
    cam.name = "CAM_DELIVERY_UMBRA_WAVE0"
    cam.data.lens = 46
    cam.data.sensor_width = 36
    cam.data.clip_start = 0.2
    cam.data.clip_end = 3000
    look_at(cam, (40, 30, 26))
    move_to(cam, collections["60_CAMERAS"])
    scene.camera = cam

    bpy.ops.object.camera_add(location=(-460, -300, 35))
    cam2 = bpy.context.object
    cam2.name = "CAM_SCALE_VALIDATION"
    cam2.data.lens = 50
    look_at(cam2, (-270, -120, 7))
    move_to(cam2, collections["60_CAMERAS"])

    scene["exovant_project"] = "EXOVANT 2950"
    scene["world_id"] = WORLD_ID
    scene["world_name"] = "UMBRA"
    scene["claim_id"] = CLAIM_ID
    scene["agent_id"] = AGENT_ID
    scene["checkpoint"] = "WAVE0_BLOCKOUT_001"
    scene["canon_planet_radius"] = "UNKNOWN"
    scene["authored_region_extent_m"] = "1200x700 PROPOSAL"
    scene["quality_claim"] = "BLOCKOUT / NOT AAA COMPLETE"
    return scene


def export(scene):
    out_blend = arg_value("--blend")
    out_glb = arg_value("--glb")
    out_png = arg_value("--render")
    if out_blend:
        os.makedirs(os.path.dirname(os.path.abspath(out_blend)), exist_ok=True)
        bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(out_blend))
    if out_glb:
        os.makedirs(os.path.dirname(os.path.abspath(out_glb)), exist_ok=True)
        bpy.ops.export_scene.gltf(filepath=os.path.abspath(out_glb), export_format="GLB")
    if out_png:
        os.makedirs(os.path.dirname(os.path.abspath(out_png)), exist_ok=True)
        scene.render.filepath = os.path.abspath(out_png)
        bpy.ops.render.render(write_still=True)


if __name__ == "__main__":
    export(build())
