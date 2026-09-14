"""EXOVANT 2950 — LEVIATHAN / Cámara de SOMA encounter-environment microset.

Deterministic additive stage. It advances the region/environment interfaces without
claiming final SOMA anatomy. Existing boss proxy remains untouched and explicitly non-final.

Uses existing IDs only:
- LEV-RGN-003 Cámara de SOMA
- LEV-INF-003 living/safe-valve family
- LEV-ENV-002 living tissue visual shell family
- LEV-ENV-003 cartilage/rib macrostructure family
"""

import bpy
import math
from mathutils import Vector

STAGE = "SOMA_ENCOUNTER_MICROSET_V1"


def build():
    scene = bpy.context.scene
    root = bpy.data.collections.get("LEV_W10_MASTER")
    if root is None:
        raise RuntimeError("LEVIATHAN master scene required")

    old = bpy.data.collections.get("26_R3_SOMA_ENCOUNTER_MICROSET")
    if old:
        for obj in list(old.all_objects):
            bpy.data.objects.remove(obj, do_unlink=True)
        bpy.data.collections.remove(old)

    # Replace primitive visual representatives. Stable arena floor and SOMA proxy stay untouched.
    for name in [
        "R3_BIO_BRIDGE_0", "R3_BIO_BRIDGE_1", "R3_BIO_BRIDGE_2",
        "R3_SAFE_VALVE_0", "R3_SAFE_VALVE_1", "R3_SAFE_VALVE_2",
        "R3_CONTRACTION_MEMBRANE_0", "R3_CONTRACTION_MEMBRANE_1", "R3_CONTRACTION_MEMBRANE_2",
    ]:
        obj = bpy.data.objects.get(name)
        if obj:
            bpy.data.objects.remove(obj, do_unlink=True)

    c = bpy.data.collections.new("26_R3_SOMA_ENCOUNTER_MICROSET")
    root.children.link(c)
    c_collision = bpy.data.collections.get("40_COLLISION_PROXY")
    c_camera = bpy.data.collections.get("90_CAMERAS_LIGHTS")
    if c_collision is None or c_camera is None:
        raise RuntimeError("Required master collections missing")

    def mat(name):
        m = bpy.data.materials.get(name)
        if m is None:
            raise RuntimeError(f"Missing base material: {name}")
        return m

    tissue = mat("LEV_MAT_TISSUE_WARM")
    tissue_dark = mat("LEV_MAT_TISSUE_DARK")
    membrane = mat("LEV_MAT_MEMBRANE")
    cartilage = mat("LEV_MAT_CARTILAGE")
    vascular = mat("LEV_MAT_VASCULAR")
    amber = mat("SIGNAL_AMBER_REFUGE")
    cyan = mat("SIGNAL_CYAN_MEMORY")
    verm = mat("SIGNAL_VERMILION_HOSTILE")
    collision = mat("DEBUG_COLLISION_STABLE")

    def portable_material(name, color, roughness, metallic=0.0):
        m = bpy.data.materials.get(name)
        if m:
            return m
        m = bpy.data.materials.new(name)
        m.use_nodes = True
        bsdf = m.node_tree.nodes.get("Principled BSDF")
        bsdf.inputs["Base Color"].default_value = (*color, 1.0)
        bsdf.inputs["Roughness"].default_value = roughness
        bsdf.inputs["Metallic"].default_value = metallic
        return m

    pressure = portable_material("LEV_MAT_PRESSURE_LUMEN", (0.34, 0.045, 0.040), 0.34)
    fibrous = portable_material("LEV_MAT_FIBROUS_TENDON", (0.22, 0.15, 0.11), 0.72)

    def relink(obj, target=c):
        for oc in list(obj.users_collection):
            oc.objects.unlink(obj)
        target.objects.link(obj)
        return obj

    def assign(obj, material):
        if getattr(obj, "data", None) and hasattr(obj.data, "materials"):
            obj.data.materials.append(material)
        return obj

    def box(name, loc, dims, material, bevel=0.08, target=c, rot=(0, 0, 0)):
        bpy.ops.mesh.primitive_cube_add(location=loc, rotation=rot)
        obj = bpy.context.object
        obj.name = name
        obj.dimensions = dims
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        if bevel:
            mod = obj.modifiers.new("Physical_Bevel", "BEVEL")
            mod.width = bevel
            mod.segments = 3
        assign(obj, material)
        return relink(obj, target)

    def sphere(name, loc, scale, material, segments=32, rings=16, target=c):
        bpy.ops.mesh.primitive_uv_sphere_add(segments=segments, ring_count=rings, location=loc)
        obj = bpy.context.object
        obj.name = name
        obj.scale = scale
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        assign(obj, material)
        return relink(obj, target)

    def cylinder(name, loc, radius, depth, material, rot=(0, 0, 0), vertices=28, target=c):
        bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=loc, rotation=rot)
        obj = bpy.context.object
        obj.name = name
        assign(obj, material)
        return relink(obj, target)

    def torus(name, loc, major, minor, material, rot=(0, 0, 0), major_segments=48, minor_segments=12, target=c):
        bpy.ops.mesh.primitive_torus_add(major_radius=major, minor_radius=minor, major_segments=major_segments, minor_segments=minor_segments, location=loc, rotation=rot)
        obj = bpy.context.object
        obj.name = name
        assign(obj, material)
        return relink(obj, target)

    def tube(name, points, radius, material, target=c):
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
        assign(obj, material)
        return obj

    def empty(name, asset_id, tier):
        obj = bpy.data.objects.new(name, None)
        c.objects.link(obj)
        obj["asset_id"] = asset_id
        obj["quality_tier"] = tier
        obj["production_state"] = "REPRESENTATIVE_DETAIL_NOT_FINAL"
        obj["generator_stage"] = STAGE
        return obj

    center = Vector((225.0, -75.0, 8.0))

    chamber_root = empty("R3_HERO_CHAMBER_ENV_ROOT", "LEV-RGN-003", "A")
    chamber_root["canon_outer_envelope_m"] = 58.0
    chamber_root["boss_art_dependency"] = "LEV-BOSS-001 remains BLOCKED; this stage changes environment only"
    chamber_root["safe_space_rule"] = "no contraction removes all escape space"

    bridge_root = empty("R3_HERO_BRIDGE_SYSTEM_ROOT", "LEV-ENV-003", "A")
    bridge_root["construction_logic"] = "cartilage load ribs carry membrane tread over stable gameplay floor; visual bridge may flex later without owning collision"

    valve_root = empty("R3_HERO_SAFE_VALVE_SYSTEM_ROOT", "LEV-INF-003", "A")
    valve_root["function"] = "pressure refuge / bypass interface"
    valve_root["signal_semantics"] = "amber refuge; cyan diagnostic; vermilion contraction hazard"

    contraction_root = empty("R3_HERO_CONTRACTION_SYSTEM_ROOT", "LEV-ENV-002", "A")
    contraction_root["collision_authority"] = "NONE_VISUAL_ONLY"
    contraction_root["telegraph_contract"] = "tendon pre-load + vermilion pressure node before visual contraction"

    # ------------------------------------------------------------------
    # Three radial bridge sectors: visual hierarchy only; stable arena floor remains collision authority.
    # ------------------------------------------------------------------
    for sector, deg in enumerate((0, 120, 240)):
        a = math.radians(deg)
        radial = Vector((math.cos(a), math.sin(a), 0.0))
        tangent = Vector((-math.sin(a), math.cos(a), 0.0))
        mid = center + radial * 13.0 + Vector((0, 0, 1.4))

        # Paired load ribs and segmented membrane tread establish manufacturing/evolution logic.
        for side in (-1, 1):
            p0 = center + radial * 3.2 + tangent * side * 2.25 + Vector((0, 0, 1.1))
            p1 = center + radial * 12.5 + tangent * side * 2.0 + Vector((0, 0, 2.0))
            p2 = center + radial * 23.2 + tangent * side * 1.55 + Vector((0, 0, 1.25))
            tube(f"R3_HEB_RIB_{sector}_{'L' if side < 0 else 'R'}", [tuple(p0), tuple(p1), tuple(p2)], 0.42, cartilage)

        for seg in range(7):
            r = 5.0 + seg * 2.8
            loc = center + radial * r + Vector((0, 0, 1.15 + 0.35 * math.sin(seg * math.pi / 6)))
            tile = box(f"R3_HEB_TREAD_{sector}_{seg}", tuple(loc), (2.65, 4.15, 0.32), membrane, 0.18, c, (0, 0, a))
            tile["visual_flex_future"] = True

        # Tendon ties communicate load transfer into the chamber wall.
        for tie in (-1, 1):
            p0 = center + radial * 21.5 + tangent * tie * 1.5 + Vector((0, 0, 1.4))
            p1 = center + radial * 26.0 + tangent * tie * 3.0 + Vector((0, 0, 6.0))
            tube(f"R3_HEB_TENDON_{sector}_{tie:+d}", [tuple(p0), tuple(p1)], 0.22, fibrous)

    # ------------------------------------------------------------------
    # Three safe-valve refuges. Same LEV-INF-003 family as Puerto, local living variant.
    # ------------------------------------------------------------------
    for sector, deg in enumerate((0, 120, 240)):
        a = math.radians(deg)
        radial = Vector((math.cos(a), math.sin(a), 0.0))
        tangent = Vector((-math.sin(a), math.cos(a), 0.0))
        pos = center + radial * 22.0 + Vector((0, 0, 4.0))

        torus(f"R3_HSV_FRAME_{sector}", tuple(pos), 4.3, 0.42, cartilage, (math.radians(90), 0, a), 56, 12)
        torus(f"R3_HSV_MEMBRANE_SEAL_{sector}", tuple(pos - radial * 0.25), 3.45, 0.48, membrane, (math.radians(90), 0, a), 56, 12)
        torus(f"R3_HSV_AMBER_REFUGE_{sector}", tuple(pos + radial * 0.35), 3.85, 0.12, amber, (math.radians(90), 0, a), 48, 8)

        # Four pressure actuator nodules, with diagnostic line leading outward.
        for n in range(4):
            aa = math.radians(n * 90)
            local = tangent * (4.25 * math.cos(aa)) + Vector((0, 0, 4.25 * math.sin(aa)))
            npos = pos + local
            sphere(f"R3_HSV_ACTUATOR_{sector}_{n}", tuple(npos), (0.55, 0.55, 0.55), pressure, 24, 12)
        diag_start = pos + tangent * -4.5 + Vector((0, 0, 0.8))
        diag_end = pos + tangent * -7.5 + Vector((0, 0, 1.8))
        tube(f"R3_HSV_DIAGNOSTIC_{sector}", [tuple(diag_start), tuple(diag_end)], 0.10, cyan)

        # Pressure bypass tube implies actual function.
        b0 = pos - radial * 2.0 + Vector((0, 0, -2.4))
        b1 = pos - radial * 5.0 + Vector((0, 0, -3.1))
        b2 = center + radial * 18.5 + Vector((0, 0, -0.5))
        tube(f"R3_HSV_BYPASS_{sector}", [tuple(b0), tuple(b1), tuple(b2)], 0.34, vascular)

    # ------------------------------------------------------------------
    # Three contraction walls: tendon pre-load, membrane wall, hazard pressure node.
    # No collision objects are created here.
    # ------------------------------------------------------------------
    for sector, deg in enumerate((60, 180, 300)):
        a = math.radians(deg)
        radial = Vector((math.cos(a), math.sin(a), 0.0))
        tangent = Vector((-math.sin(a), math.cos(a), 0.0))
        wall_center = center + radial * 28.0 + Vector((0, 0, 10.0))
        membrane_obj = sphere(f"R3_HCM_MEMBRANE_{sector}", tuple(wall_center), (3.8, 8.5, 10.5), tissue, 32, 16)
        membrane_obj.rotation_euler.z = a
        membrane_obj["collision_authority"] = "NONE_VISUAL_ONLY"
        membrane_obj["future_deformation"] = "controlled contraction only after gameplay validation"

        for rib in (-2, -1, 0, 1, 2):
            start = wall_center + tangent * rib * 2.6 + Vector((0, 0, -8.2))
            end = wall_center + tangent * rib * 2.2 + Vector((0, 0, 8.2))
            tube(f"R3_HCM_TENDON_{sector}_{rib:+d}", [tuple(start), tuple(end)], 0.26, fibrous)

        node_pos = wall_center - radial * 4.5 + Vector((0, 0, 4.0))
        sphere(f"R3_HCM_PRESSURE_NODE_{sector}", tuple(node_pos), (1.1, 1.1, 1.1), verm, 28, 14)
        tube(f"R3_HCM_SIGNAL_LINE_{sector}", [tuple(node_pos), tuple(node_pos + tangent * 4.2)], 0.10, cyan)

    # ------------------------------------------------------------------
    # Central regulator cradle around SOMA proxy. It is environmental support, not SOMA anatomy.
    # ------------------------------------------------------------------
    for i, deg in enumerate((45, 135, 225, 315)):
        a = math.radians(deg)
        radial = Vector((math.cos(a), math.sin(a), 0.0))
        base = center + radial * 11.0 + Vector((0, 0, 1.2))
        top = center + radial * 7.2 + Vector((0, 0, 13.5))
        tube(f"R3_HRC_SUPPORT_{i}", [tuple(base), tuple(top)], 0.52, cartilage)
        sphere(f"R3_HRC_PRESSURE_BULB_{i}", tuple(base + Vector((0, 0, 1.2))), (0.9, 0.9, 0.75), pressure, 24, 12)

    torus("R3_HRC_REGULATOR_RING", (225.0, -75.0, 17.5), 10.5, 0.38, cartilage, major_segments=64, minor_segments=12)
    torus("R3_HRC_DIAGNOSTIC_RING", (225.0, -75.0, 18.0), 11.2, 0.10, cyan, major_segments=64, minor_segments=8)

    # Inspection camera/light. Existing gameplay SOMA camera remains untouched.
    cam_data = bpy.data.cameras.new("CAM_R3_MICROSET_CLOSE_DATA")
    cam_data.lens = 39
    cam = bpy.data.objects.new("CAM_R3_MICROSET_CLOSE", cam_data)
    cam.location = (225.0, -145.0, 25.0)
    target = Vector((225.0, -75.0, 10.0))
    cam.rotation_euler = (target - cam.location).to_track_quat("-Z", "Y").to_euler()
    c_camera.objects.link(cam)

    light_data = bpy.data.lights.new("LGT_R3_MICROSET_KEY", "SPOT")
    light_data.energy = 2300
    light_data.color = (1.0, 0.28, 0.20)
    light_data.spot_size = math.radians(82)
    light_data.spot_blend = 0.64
    light = bpy.data.objects.new("LGT_R3_MICROSET_KEY", light_data)
    light.location = (225.0, -115.0, 42.0)
    light.rotation_euler = (target - light.location).to_track_quat("-Z", "Y").to_euler()
    c_camera.objects.link(light)

    scene["soma_encounter_microset_stage"] = STAGE

    return {
        "stage": STAGE,
        "collection_objects": len(c.all_objects),
        "assets": ["LEV-RGN-003", "LEV-INF-003", "LEV-ENV-002", "LEV-ENV-003"],
        "boss_proxy_changed": False,
        "canon_chamber_outer_envelope_m": 58.0,
        "new_material_roles": ["LEV_MAT_PRESSURE_LUMEN", "LEV_MAT_FIBROUS_TENDON"],
        "status": "REPRESENTATIVE_ENCOUNTER_ENVIRONMENT_NOT_FINAL"
    }


if __name__ == "__main__":
    print(build())
