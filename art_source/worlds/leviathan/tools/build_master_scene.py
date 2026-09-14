"""EXOVANT 2950 — LEVIATHAN WAVE-1 deterministic Blender blockout generator.

Authority: design/EXOVANT_BIBLIA.md + design/EXOVANT_DATA.json.
Claim: CLM-W10-WORLD-LEVIATHAN-001.
Blender route qualified during this run: Blender 5.2.0 LTS, metric scale 1 BU = 1 m.

This script intentionally builds a PROPOSAL blockout. It does not invent a physical
planet radius, final SOMA anatomy, final engine budgets, or final playable-world area.
"""

import bpy
import math
from mathutils import Vector


def build():
    scene = bpy.context.scene
    for obj in list(scene.objects):
        bpy.data.objects.remove(obj, do_unlink=True)
    for c in list(bpy.data.collections):
        bpy.data.collections.remove(c)
    for m in list(bpy.data.materials):
        bpy.data.materials.remove(m)

    if scene.world is None:
        scene.world = bpy.data.worlds.new("LEV_WORLD")
    scene.world.color = (0.008, 0.012, 0.018)
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 1.0
    scene.render.engine = "BLENDER_EEVEE"
    scene.render.fps = 24
    scene.render.resolution_x = 1280
    scene.render.resolution_y = 720
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"

    scene["project"] = "EXOVANT 2950"
    scene["world_id"] = "leviathan"
    scene["world_name"] = "LEVIATHAN"
    scene["claim_id"] = "CLM-W10-WORLD-LEVIATHAN-001"
    scene["agent_id"] = "AGENT-LEVIATHAN-10"
    scene["epistemic_position"] = "PROPOSAL_BLOCKOUT"
    scene["canon_gravity_g"] = 1.15
    scene["canon_temperature_c"] = 38.0
    scene["canon_regions"] = "Puerto de la Herida | Jardines Inmunes | Camara de SOMA"
    scene["planet_radius_status"] = "BLOCKED_CANON_UNKNOWN"
    scene["production_engine_status"] = "UNREAL_CANDIDATE_NOT_QUALIFIED; GODOT_PROTOTYPE_EXECUTABLE"

    def coll(name, parent=None):
        c = bpy.data.collections.new(name)
        (parent.children if parent else scene.collection.children).link(c)
        return c

    root = coll("LEV_W10_MASTER")
    c_ref = coll("00_REFERENCE", root)
    c_l2 = coll("10_L2_WORLD_CELL", root)
    c_r1 = coll("20_R1_PUERTO_DE_LA_HERIDA", root)
    c_r2 = coll("21_R2_JARDINES_INMUNES", root)
    c_r3 = coll("22_R3_CAMARA_DE_SOMA", root)
    c_collision = coll("40_COLLISION_PROXY", root)
    c_ecology = coll("50_ECOLOGY_PROXY", root)
    c_combat = coll("60_COMBAT_PROXY", root)
    c_camera = coll("90_CAMERAS_LIGHTS", root)

    def relink(obj, target):
        if target not in obj.users_collection:
            target.objects.link(obj)
        for current in list(obj.users_collection):
            if current != target:
                current.objects.unlink(obj)
        return obj

    def material(name, color, roughness=0.6, metallic=0.0, emission=None, emission_strength=0.0):
        mat = bpy.data.materials.new(name)
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            if bsdf.inputs.get("Base Color"):
                bsdf.inputs["Base Color"].default_value = (*color, 1.0)
            if bsdf.inputs.get("Roughness"):
                bsdf.inputs["Roughness"].default_value = roughness
            if bsdf.inputs.get("Metallic"):
                bsdf.inputs["Metallic"].default_value = metallic
            if emission is not None:
                if bsdf.inputs.get("Emission Color"):
                    bsdf.inputs["Emission Color"].default_value = (*emission, 1.0)
                elif bsdf.inputs.get("Emission"):
                    bsdf.inputs["Emission"].default_value = (*emission, 1.0)
                if bsdf.inputs.get("Emission Strength"):
                    bsdf.inputs["Emission Strength"].default_value = emission_strength
        return mat

    mats = {
        "tissue": material("LEV_MAT_TISSUE_WARM", (0.18, 0.055, 0.052), 0.78),
        "tissue_dark": material("LEV_MAT_TISSUE_DARK", (0.045, 0.020, 0.026), 0.88),
        "vascular": material("LEV_MAT_VASCULAR", (0.30, 0.018, 0.026), 0.52),
        "membrane": material("LEV_MAT_MEMBRANE", (0.32, 0.16, 0.15), 0.42),
        "cartilage": material("LEV_MAT_CARTILAGE", (0.34, 0.28, 0.22), 0.68),
        "ivory": material("HUM_MAT_IVORY_CERAMIC", (0.72, 0.70, 0.62), 0.46),
        "tech": material("HUM_MAT_DARK_TECH", (0.035, 0.045, 0.052), 0.62, 0.15),
        "amber": material("SIGNAL_AMBER_REFUGE", (0.62, 0.22, 0.025), 0.38, 0.0, (1.0, 0.26, 0.03), 2.4),
        "cyan": material("SIGNAL_CYAN_MEMORY", (0.035, 0.22, 0.26), 0.32, 0.0, (0.04, 0.8, 1.0), 1.8),
        "verm": material("SIGNAL_VERMILION_HOSTILE", (0.50, 0.02, 0.015), 0.38, 0.0, (1.0, 0.03, 0.01), 2.0),
        "collision": material("DEBUG_COLLISION_STABLE", (0.035, 0.045, 0.060), 0.95),
    }

    def assign(obj, mat):
        if getattr(obj, "data", None) and hasattr(obj.data, "materials"):
            obj.data.materials.append(mat)
        return obj

    def box(name, loc, dims, mat, target, bevel=0.5):
        bpy.ops.mesh.primitive_cube_add(location=loc)
        obj = bpy.context.object
        obj.name = name
        obj.dimensions = dims
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        if bevel > 0:
            mod = obj.modifiers.new("Physical_Bevel", "BEVEL")
            mod.width = bevel
            mod.segments = 3
        assign(obj, mat)
        return relink(obj, target)

    def sphere(name, loc, scale, mat, target, segments=40, rings=20):
        bpy.ops.mesh.primitive_uv_sphere_add(segments=segments, ring_count=rings, location=loc)
        obj = bpy.context.object
        obj.name = name
        obj.scale = scale
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        assign(obj, mat)
        return relink(obj, target)

    def cylinder(name, loc, radius, depth, mat, target, rotation=(0, 0, 0), vertices=40):
        bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=loc, rotation=rotation)
        obj = bpy.context.object
        obj.name = name
        assign(obj, mat)
        return relink(obj, target)

    def torus(name, loc, major, minor, mat, target, rotation=(0, 0, 0)):
        bpy.ops.mesh.primitive_torus_add(
            major_radius=major,
            minor_radius=minor,
            major_segments=72,
            minor_segments=16,
            location=loc,
            rotation=rotation,
        )
        obj = bpy.context.object
        obj.name = name
        assign(obj, mat)
        return relink(obj, target)

    def tube(name, points, radius, mat, target):
        curve = bpy.data.curves.new(name + "_CURVE", "CURVE")
        curve.dimensions = "3D"
        curve.resolution_u = 4
        curve.bevel_depth = radius
        curve.bevel_resolution = 3
        spline = curve.splines.new("BEZIER")
        spline.bezier_points.add(len(points) - 1)
        for bp, co in zip(spline.bezier_points, points):
            bp.co = co
            bp.handle_left_type = "AUTO"
            bp.handle_right_type = "AUTO"
        obj = bpy.data.objects.new(name, curve)
        target.objects.link(obj)
        return assign(obj, mat)

    def label(name, text, loc, size):
        curve = bpy.data.curves.new(name + "_TXT", "FONT")
        curve.body = text
        curve.align_x = "CENTER"
        curve.size = size
        curve.extrude = 0.04
        obj = bpy.data.objects.new(name, curve)
        obj.location = loc
        c_ref.objects.link(obj)
        return assign(obj, mats["cyan"])

    def look_at(obj, target):
        obj.rotation_euler = (Vector(target) - obj.location).to_track_quat("-Z", "Y").to_euler()

    def camera(name, loc, target, lens=45):
        data = bpy.data.cameras.new(name + "_DATA")
        data.lens = lens
        data.sensor_width = 36
        obj = bpy.data.objects.new(name, data)
        obj.location = loc
        c_camera.objects.link(obj)
        look_at(obj, target)
        return obj

    # Scale reference and explicit unknown L0 decision.
    human = box("REF_HUMAN_1P85M", (0, 0, 0.925), (0.55, 0.40, 1.85), mats["ivory"], c_ref, 0.12)
    human["real_height_m"] = 1.85
    blocker = bpy.data.objects.new("L0_PLANET_RADIUS_BLOCKED_CANON_UNKNOWN", None)
    blocker.empty_display_type = "SPHERE"
    blocker.empty_display_size = 10
    c_ref.objects.link(blocker)
    blocker["status"] = "BLOCKED"
    blocker["decision_needed"] = "LEVIATHAN physical radius/diameter canon"
    blocker["work_that_can_continue"] = "L2/L3 authored-region blockout at metre scale"

    # L2 representative authored cell; not physical planet dimensions.
    substrate = box("L2_STABLE_SUBSTRATE", (0, 0, -8), (720, 480, 12), mats["collision"], c_collision, 3.0)
    substrate["collision_role"] = "STABLE_GAMEPLAY_SUBSTRATE_PROPOSAL"
    masses = [
        (-240, -120, 150, 75, 26, -0.20),
        (-80, -170, 120, 70, 20, 0.14),
        (90, 170, 150, 85, 30, -0.08),
        (250, 75, 130, 72, 24, 0.16),
        (-250, 150, 95, 55, 18, 0.22),
        (180, -155, 110, 62, 22, -0.18),
    ]
    for i, (x, y, sx, sy, sz, rz) in enumerate(masses):
        obj = sphere(f"L2_TISSUE_MASS_{i:02d}", (x, y, sz * 0.35), (sx, sy, sz), mats["tissue_dark"], c_l2, 32, 16)
        obj.rotation_euler.z = rz
    tube("L2_VASCULAR_TRUNK_A", [(-330, -80, 4), (-180, -40, 12), (-30, 20, 8), (150, 25, 15), (330, -30, 6)], 5.5, mats["vascular"], c_l2)
    tube("L2_VASCULAR_TRUNK_B", [(-260, 170, 7), (-110, 115, 13), (40, 105, 9), (180, 140, 12), (300, 175, 8)], 3.8, mats["vascular"], c_l2)
    tube("L2_NERVE_CYAN", [(-300, 40, 10), (-160, 90, 13), (-20, 55, 11), (110, -10, 12), (250, -110, 15)], 1.25, mats["cyan"], c_l2)
    for x in (-260, -130, 0, 130, 260):
        torus(f"L2_RIB_{x:+04d}", (x, 0, 18), 34, 3.2, mats["cartilage"], c_l2, (math.radians(90), 0, 0))

    # R1 — Puerto de la Herida.
    box("R1_PORT_DECK", (-210, -75, 2), (150, 105, 4), mats["collision"], c_collision, 1.2)
    torus("R1_SCAR_RING", (-210, -75, 7), 58, 5.5, mats["membrane"], c_r1)
    for i, deg in enumerate(range(0, 360, 45)):
        angle = math.radians(deg)
        x, y = -210 + 57 * math.cos(angle), -75 + 57 * math.sin(angle)
        clamp = box(f"R1_SUTURE_CLAMP_{i:02d}", (x, y, 10), (11, 4, 5), mats["ivory"], c_r1, 0.6)
        clamp.rotation_euler.z = angle
    modules = [(-250, -100, -0.08), (-215, -118, 0.06), (-180, -102, -0.03), (-245, -60, 0.1), (-200, -52, -0.07), (-165, -70, 0.04)]
    for i, (x, y, rot) in enumerate(modules):
        shell = box(f"R1_COLONY_MODULE_{i:02d}", (x, y, 9), (24, 12, 10), mats["ivory"], c_r1, 2.8)
        shell.rotation_euler.z = rot
        belly = box(f"R1_MODULE_TECH_BELLY_{i:02d}", (x, y, 4.5), (19, 9, 2.5), mats["tech"], c_r1, 0.8)
        belly.rotation_euler.z = rot
    cylinder("R1_REFUGE_BEACON", (-210, -22, 12), 1.4, 20, mats["amber"], c_r1)
    torus("R1_AIRLOCK_VALVE", (-143, -75, 11), 8.5, 1.6, mats["tech"], c_r1, (math.radians(90), 0, 0))

    # R2 — Jardines Inmunes.
    box("R2_STABLE_GARDEN_PATH", (15, 120, 2), (180, 90, 4), mats["collision"], c_collision, 1.2)
    for idx, off in enumerate((-26, 0, 26)):
        tube(f"R2_LYMPH_CHANNEL_{idx}", [(-80, 120 + off, 8), (-30, 135 + off, 11), (25, 118 + off, 10), (85, 132 + off, 9)], 3.2, mats["vascular"], c_r2)
    for i in range(12):
        x, y = -60 + (i % 6) * 28, 92 + (i // 6) * 58
        cylinder(f"R2_ALGA_PULSO_{i:02d}", (x, y, 8), 0.8, 11, mats["cyan"], c_ecology, (0.12 * ((i % 3) - 1), 0, 0))
        sphere(f"R2_ALGA_NODE_{i:02d}", (x, y, 14), (2.8, 2.8, 2.1), mats["cyan"], c_ecology, 24, 12)
    for i, (x, y) in enumerate([(-35, 90), (12, 155), (55, 100)]):
        proxy = sphere(f"R2_PARASITE_GARDENER_PROXY_{i}", (x, y, 14), (4.5, 2.5, 2.2), mats["membrane"], c_ecology, 24, 12)
        proxy["proxy_only"] = True
    whale = sphere("R2_BALLENA_LINFA_PROXY", (55, 168, 24), (18, 5.5, 6.5), mats["tissue"], c_ecology, 40, 20)
    whale.rotation_euler.z = -0.22
    whale["proxy_only"] = True

    # Stable route interface.
    path = [(-210, -22, 6), (-150, 15, 8), (-95, 65, 8), (-40, 105, 7), (30, 120, 7), (95, 90, 8), (150, 35, 8), (205, -20, 8)]
    tube("TRAVERSAL_MAIN_ORGANIC_PATH", path, 6.0, mats["cartilage"], c_l2)
    for i, point in enumerate(path):
        box(f"COLL_PATH_PAD_{i:02d}", (point[0], point[1], 3.5), (28, 22, 3), mats["collision"], c_collision, 1.0)

    # R3 — 58 m outer chamber envelope, exact after QA correction.
    box("R3_ARENA_STABLE_FLOOR", (225, -75, 4), (58, 58, 6), mats["collision"], c_collision, 2.0)
    torus("R3_SOMA_ARENA_RING", (225, -75, 8), 25.8, 3.2, mats["membrane"], c_r3)
    for i, deg in enumerate((0, 120, 240)):
        angle = math.radians(deg)
        x, y = 225 + 22 * math.cos(angle), -75 + 22 * math.sin(angle)
        bridge = box(f"R3_BIO_BRIDGE_{i}", (225 + 13 * math.cos(angle), -75 + 13 * math.sin(angle), 9), (26, 7, 3.5), mats["cartilage"], c_r3, 1.2)
        bridge.rotation_euler.z = angle
        torus(f"R3_SAFE_VALVE_{i}", (x, y, 12), 5.0, 1.2, mats["amber"], c_r3, (math.radians(90), 0, angle))
    for i, deg in enumerate((60, 180, 300)):
        angle = math.radians(deg)
        x, y = 225 + 30 * math.cos(angle), -75 + 30 * math.sin(angle)
        membrane = sphere(f"R3_CONTRACTION_MEMBRANE_{i}", (x, y, 18), (10, 4, 18), mats["tissue"], c_r3, 32, 16)
        membrane.rotation_euler.z = angle
        membrane["collision_authority"] = "NONE_VISUAL_ONLY"
    soma = sphere("SOMA_PROXY_NOT_FINAL", (225, -75, 18), (8.5, 8.5, 11.0), mats["tissue"], c_combat, 48, 24)
    soma["final_anatomy"] = False
    soma["role"] = "COMBAT_SCALE_AND_SILHOUETTE_INTERFACE_ONLY"
    torus("SOMA_IMMUNE_HALO_PROXY", (225, -75, 20), 12.5, 2.0, mats["verm"], c_combat)
    for i, angle in enumerate((0, math.pi * 2 / 3, math.pi * 4 / 3)):
        tube(
            f"SOMA_CILIA_ARM_{i}",
            [(225, -75, 19), (225 + 14 * math.cos(angle), -75 + 14 * math.sin(angle), 23), (225 + 22 * math.cos(angle), -75 + 22 * math.sin(angle), 16)],
            1.4,
            mats["verm"],
            c_combat,
        )

    for name, loc, scale in [
        ("FAGOCITO_GUARDIAN_PROXY", (145, 10, 7), (2.1, 2.1, 3.8)),
        ("EXTRACTOR_PULSO_PROXY", (80, 70, 7), (1.4, 1.4, 3.0)),
        ("COLONIA_PARASITARIA_PROXY", (10, 150, 6), (4.2, 4.2, 2.5)),
    ]:
        proxy = sphere(name, loc, scale, mats["verm"], c_combat, 28, 14)
        proxy["proxy_only"] = True

    label("LBL_R1", "PUERTO DE LA HERIDA", (-210, -150, 30), 6)
    label("LBL_R2", "JARDINES INMUNES", (15, 185, 34), 6)
    label("LBL_R3", "CAMARA DE SOMA", (225, -140, 42), 6)

    scene.camera = camera("CAM_DELIVERY_OVERVIEW", (470, -470, 310), (0, 0, 20), 48)
    camera("CAM_GAMEPLAY_R1", (-250, -155, 8), (-190, -75, 10), 32)
    camera("CAM_GAMEPLAY_R2", (-55, 60, 7), (25, 125, 12), 32)
    camera("CAM_GAMEPLAY_SOMA", (225, -130, 8), (225, -75, 18), 36)

    sun_data = bpy.data.lights.new("LGT_SOMA_SOURCE", "SUN")
    sun_data.energy = 2.0
    sun_data.angle = math.radians(18)
    sun = bpy.data.objects.new("LGT_SOMA_SOURCE", sun_data)
    sun.rotation_euler = (math.radians(42), 0, math.radians(-28))
    c_camera.objects.link(sun)

    # POINT instead of AREA: portable through glTF exporter used by the remote worker.
    bounce_data = bpy.data.lights.new("LGT_TISSUE_BOUNCE", "POINT")
    bounce_data.energy = 1800
    bounce_data.shadow_soft_size = 55
    bounce = bpy.data.objects.new("LGT_TISSUE_BOUNCE", bounce_data)
    bounce.location = (-120, -180, 150)
    c_camera.objects.link(bounce)

    cyan_data = bpy.data.lights.new("LGT_CYAN_MEMORY", "POINT")
    cyan_data.energy = 1900
    cyan_data.color = (0.12, 0.7, 1.0)
    cyan_data.shadow_soft_size = 35
    cyan = bpy.data.objects.new("LGT_CYAN_MEMORY", cyan_data)
    cyan.location = (80, 130, 60)
    c_camera.objects.link(cyan)

    amber_data = bpy.data.lights.new("LGT_AMBER_REFUGE", "POINT")
    amber_data.energy = 1300
    amber_data.color = (1.0, 0.22, 0.04)
    amber_data.shadow_soft_size = 22
    amber = bpy.data.objects.new("LGT_AMBER_REFUGE", amber_data)
    amber.location = (-210, -75, 45)
    c_camera.objects.link(amber)

    for x in range(-300, 301, 100):
        tube(f"REF_GRID_X_{x:+04d}", [(x, -220, -1.5), (x, 220, -1.5)], 0.18, mats["cyan"], c_ref)
    for y in range(-200, 201, 100):
        tube(f"REF_GRID_Y_{y:+04d}", [(-340, y, -1.5), (340, y, -1.5)], 0.18, mats["cyan"], c_ref)

    meta = bpy.data.objects.new("META_LEVIATHAN_WORLD_CONTRACT", None)
    c_ref.objects.link(meta)
    meta["canon_status"] = "PROPOSED_WORLD_DESIGN; BLOCKOUT_IMPLEMENTED"
    meta["planet_radius_m"] = "UNKNOWN"
    meta["authored_cell_extent_m"] = "720x480 PROPOSAL"
    meta["soma_arena_diameter_m"] = 58.0
    meta["soma_arena_measurement"] = "outer chamber envelope"
    meta["stable_collision_rule"] = "separate from deforming visual tissue"
    meta["region_1"] = "Puerto de la Herida"
    meta["region_2"] = "Jardines Inmunes"
    meta["region_3"] = "Camara de SOMA"

    return {
        "object_count": len(scene.objects),
        "mesh_count": sum(1 for obj in scene.objects if obj.type == "MESH"),
        "material_count": len(bpy.data.materials),
        "human_reference_m": 1.85,
        "soma_arena_diameter_m": 58.0,
        "planet_radius": "BLOCKED_CANON_UNKNOWN",
    }


if __name__ == "__main__":
    print(build())
