"""EXOVANT 2950 — LEVIATHAN / Jardines Inmunes representative-detail microset.

Additive deterministic stage over the LEVIATHAN master scene.
Claim: CLM-W10-WORLD-LEVIATHAN-001.

Advances existing registry IDs only:
- LEV-INF-005 lymph channel family
- LEV-ECO-004 pulse algae family
- LEV-ECO-001 gardener parasite

All new anatomy dimensions are production PROPOSAL, not canon. Stable gameplay
collision remains separate from visually living/deformable tissue.
"""

import bpy
import math
from mathutils import Vector

STAGE = "JARDINES_MICROSET_V1"


def build():
    scene = bpy.context.scene
    root = bpy.data.collections.get("LEV_W10_MASTER")
    if root is None:
        raise RuntimeError("LEVIATHAN master scene required")

    old = bpy.data.collections.get("25_R2_HERO_LYMPH_MICROSET")
    if old:
        for obj in list(old.all_objects):
            bpy.data.objects.remove(obj, do_unlink=True)
        bpy.data.collections.remove(old)

    # Replace one primitive gardener and four primitive pulse-algae samples so the
    # representative detail does not visually duplicate the old proxy at the same spot.
    for name in [
        "R2_PARASITE_GARDENER_PROXY_1",
        "R2_ALGA_PULSO_02", "R2_ALGA_NODE_02",
        "R2_ALGA_PULSO_03", "R2_ALGA_NODE_03",
        "R2_ALGA_PULSO_08", "R2_ALGA_NODE_08",
        "R2_ALGA_PULSO_09", "R2_ALGA_NODE_09",
    ]:
        obj = bpy.data.objects.get(name)
        if obj:
            bpy.data.objects.remove(obj, do_unlink=True)

    c = bpy.data.collections.new("25_R2_HERO_LYMPH_MICROSET")
    root.children.link(c)
    c_collision = bpy.data.collections.get("40_COLLISION_PROXY")
    c_camera = bpy.data.collections.get("90_CAMERAS_LIGHTS")
    if c_collision is None or c_camera is None:
        raise RuntimeError("Required master collections missing")

    def base_mat(name):
        m = bpy.data.materials.get(name)
        if m is None:
            raise RuntimeError(f"Missing base material: {name}")
        return m

    tissue = base_mat("LEV_MAT_TISSUE_WARM")
    tissue_dark = base_mat("LEV_MAT_TISSUE_DARK")
    vascular = base_mat("LEV_MAT_VASCULAR")
    membrane = base_mat("LEV_MAT_MEMBRANE")
    cartilage = base_mat("LEV_MAT_CARTILAGE")
    cyan = base_mat("SIGNAL_CYAN_MEMORY")
    amber = base_mat("SIGNAL_AMBER_REFUGE")
    collision = base_mat("DEBUG_COLLISION_STABLE")

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

    mucosa = portable_material("LEV_MAT_MUCOSA_WET", (0.23, 0.075, 0.068), 0.28)
    necrotic = portable_material("LEV_MAT_NECROTIC", (0.055, 0.028, 0.024), 0.88)
    algae = portable_material("LEV_MAT_ALGA_PRESSURE", (0.035, 0.24, 0.20), 0.44)

    def relink(obj, target=c):
        for oc in list(obj.users_collection):
            oc.objects.unlink(obj)
        target.objects.link(obj)
        return obj

    def assign(obj, mat):
        if getattr(obj, "data", None) and hasattr(obj.data, "materials"):
            obj.data.materials.append(mat)
        return obj

    def box(name, loc, dims, mat, bevel=0.08, target=c, rot=(0, 0, 0)):
        bpy.ops.mesh.primitive_cube_add(location=loc, rotation=rot)
        obj = bpy.context.object
        obj.name = name
        obj.dimensions = dims
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        if bevel:
            mod = obj.modifiers.new("Physical_Bevel", "BEVEL")
            mod.width = bevel
            mod.segments = 3
        assign(obj, mat)
        return relink(obj, target)

    def sphere(name, loc, scale, mat, segments=32, rings=16, target=c):
        bpy.ops.mesh.primitive_uv_sphere_add(segments=segments, ring_count=rings, location=loc)
        obj = bpy.context.object
        obj.name = name
        obj.scale = scale
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        assign(obj, mat)
        return relink(obj, target)

    def cylinder(name, loc, radius, depth, mat, rot=(0, 0, 0), vertices=28, target=c):
        bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=loc, rotation=rot)
        obj = bpy.context.object
        obj.name = name
        assign(obj, mat)
        return relink(obj, target)

    def torus(name, loc, major, minor, mat, rot=(0, 0, 0), major_segments=48, minor_segments=12, target=c):
        bpy.ops.mesh.primitive_torus_add(major_radius=major, minor_radius=minor, major_segments=major_segments, minor_segments=minor_segments, location=loc, rotation=rot)
        obj = bpy.context.object
        obj.name = name
        assign(obj, mat)
        return relink(obj, target)

    def tube(name, points, radius, mat, target=c):
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
        assign(obj, mat)
        return obj

    def empty(name, asset_id, tier):
        obj = bpy.data.objects.new(name, None)
        c.objects.link(obj)
        obj["asset_id"] = asset_id
        obj["quality_tier"] = tier
        obj["production_state"] = "REPRESENTATIVE_DETAIL_NOT_FINAL"
        obj["generator_stage"] = STAGE
        return obj

    # ------------------------------------------------------------------
    # A. LEV-INF-005 — lymph channel / service crossing microset
    # ------------------------------------------------------------------
    channel_root = empty("R2_HERO_LYMPH_CHANNEL_ROOT", "LEV-INF-005", "A")
    channel_root["construction_logic"] = "living pressure conduit supported by cartilage ribs; human-safe service path uses independent stable substrate"
    channel_root["real_dimensions_status"] = "PROPOSAL"
    channel_root["representative_length_m"] = 34.0

    cx, cy = 18.0, 124.0
    # Stable path is gameplay authority and does not deform with the visual channel.
    stable = box("COLL_R2_LYMPH_SERVICE_WALK_A", (cx, cy - 5.2, 4.4), (34.0, 3.6, 0.55), collision, 0.20, c_collision)
    stable["asset_id"] = "LEV-INF-005"
    stable["collision_role"] = "STABLE_SERVICE_WALK"

    # Visual lumen and outer support anatomy run parallel to the stable walk.
    tube("R2_HLC_LUMEN", [(-1, cy, 7.8), (7, cy + 0.8, 8.3), (18, cy - 0.5, 8.0), (29, cy + 0.7, 8.4), (37, cy, 7.9)], 2.35, mucosa)
    tube("R2_HLC_FLOW_CORE", [(-1, cy, 8.0), (9, cy + 0.4, 8.25), (18, cy - 0.2, 8.15), (28, cy + 0.35, 8.3), (37, cy, 8.0)], 0.62, vascular)
    tube("R2_HLC_DIAGNOSTIC_STRIP", [(-1, cy - 2.55, 8.2), (10, cy - 2.4, 8.55), (22, cy - 2.6, 8.35), (37, cy - 2.5, 8.2)], 0.11, cyan)

    for i, x in enumerate((-0.5, 5.5, 11.5, 17.5, 23.5, 29.5, 35.5)):
        torus(f"R2_HLC_CARTILAGE_RIB_{i}", (x, cy, 8.0), 3.15, 0.34, cartilage, (0, math.radians(90), 0), 40, 10)
        if i in (0, 3, 6):
            box(f"R2_HLC_SERVICE_SADDLE_{i}", (x, cy - 3.05, 6.6), (1.25, 1.9, 1.0), cartilage, 0.20)
            cylinder(f"R2_HLC_PRESSURE_SENSOR_{i}", (x, cy - 4.0, 7.2), 0.18, 0.75, cyan, (math.radians(90), 0, 0), 18)

    # One check valve shows flow direction and maintenance mechanics without becoming a second LEV-INF-003 family.
    torus("R2_HLC_CHECK_VALVE_FRAME", (18.0, cy, 8.0), 3.45, 0.42, cartilage, (0, math.radians(90), 0), 48, 12)
    for i in range(4):
        a = math.radians(45 + i * 90)
        y = cy + 1.35 * math.cos(a)
        z = 8.0 + 1.35 * math.sin(a)
        blade = box(f"R2_HLC_CHECK_LEAF_{i}", (18.15, y, z), (0.22, 1.15, 2.65), membrane, 0.16, c, (a, 0, math.radians(12)))
        blade["moving_part"] = True
        blade["rig_dependency"] = "future channel-valve rig"

    # Pressure refuge marker on the stable path, semantically amber.
    cylinder("R2_HLC_SAFE_PRESSURE_BEACON", (18.0, cy - 7.0, 6.2), 0.22, 3.2, amber, vertices=20)

    # ------------------------------------------------------------------
    # B. LEV-ECO-004 — pulse algae pressure-indicator family
    # ------------------------------------------------------------------
    algae_root = empty("R2_HERO_PULSE_ALGA_ROOT", "LEV-ECO-004", "B")
    algae_root["ecological_function"] = "pressure/flow indicator rooted in channel margins; state communicates local rhythm"
    algae_root["scale_status"] = "PROPOSAL"

    algae_specs = [
        (3.0, cy - 1.9, 5.1, 0.55, 2.2, "young"),
        (8.0, cy + 2.4, 5.3, 0.72, 3.0, "mature"),
        (13.5, cy - 2.0, 5.0, 0.62, 2.6, "mature"),
        (23.0, cy + 2.0, 5.2, 0.80, 3.4, "high_pressure"),
        (28.5, cy - 2.1, 5.0, 0.48, 1.9, "young"),
        (33.0, cy + 2.2, 5.1, 0.68, 2.8, "mature"),
    ]
    for i, (x, y, z0, rad, height, state) in enumerate(algae_specs):
        cylinder(f"R2_HPA_STEM_{i}", (x, y, z0 + height * 0.5), rad * 0.28, height, algae, vertices=18)
        bulb = sphere(f"R2_HPA_BULB_{i}", (x, y, z0 + height + rad * 0.7), (rad, rad, rad * 0.72), cyan if state == "high_pressure" else algae, 24, 12)
        bulb["state"] = state
        torus(f"R2_HPA_ROOT_COLLAR_{i}", (x, y, z0 + 0.05), rad * 0.72, rad * 0.18, membrane, major_segments=24, minor_segments=8)

    # ------------------------------------------------------------------
    # C. LEV-ECO-001 — representative gardener parasite anatomy
    # ------------------------------------------------------------------
    gardener_root = empty("R2_HERO_GARDENER_PARASITE_ROOT", "LEV-ECO-001", "A")
    gardener_root["ecological_role"] = "removes necrotic tissue and returns nutrients; threat emerges through density, not malice"
    gardener_root["anatomy_status"] = "PROPOSAL_REPRESENTATIVE_NOT_FINAL"
    gardener_root["locomotion_logic"] = "six low articulated limbs grip moist channel margins; two anterior cleaning appendages scrape dead tissue"
    gardener_root["feeding_logic"] = "anterior rasp transfers necrotic material to ventral digestive sac"
    gardener_root["proposed_body_length_m"] = 2.6

    gx, gy, gz = 31.0, 132.0, 7.1
    body = sphere("R2_HGP_DIGESTIVE_SAC", (gx, gy, gz + 0.55), (1.30, 0.72, 0.58), tissue, 36, 18)
    body["asset_id"] = "LEV-ECO-001"
    sphere("R2_HGP_CEPHALIC_PLATE", (gx - 1.25, gy, gz + 0.68), (0.62, 0.70, 0.45), cartilage, 28, 14)
    sphere("R2_HGP_NECROTIC_CARGO", (gx + 0.85, gy, gz + 0.72), (0.48, 0.34, 0.28), necrotic, 24, 12)

    # Six limbs: proximal cartilage strut + distal compliant membrane segment + contact pad.
    limb_y = (-0.82, -0.94, -0.72, 0.82, 0.94, 0.72)
    limb_x = (-0.65, 0.05, 0.72, -0.65, 0.05, 0.72)
    for i, (ox, oy) in enumerate(zip(limb_x, limb_y)):
        side = -1 if oy < 0 else 1
        hip = (gx + ox, gy + oy * 0.55, gz + 0.48)
        knee = (gx + ox + 0.22, gy + side * 1.25, gz + 0.05)
        foot = (gx + ox + 0.48, gy + side * 1.75, gz - 0.12)
        tube(f"R2_HGP_LIMB_PROX_{i}", [hip, knee], 0.16, cartilage)
        tube(f"R2_HGP_LIMB_DIST_{i}", [knee, foot], 0.13, membrane)
        pad = sphere(f"R2_HGP_CONTACT_PAD_{i}", foot, (0.28, 0.38, 0.10), membrane, 20, 10)
        pad["contact_role"] = "wet-grip"

    # Two cleaning arms and rasp geometry are function-driven tertiary forms.
    for i, side in enumerate((-1, 1)):
        tube(f"R2_HGP_CLEAN_ARM_{i}", [(gx - 1.35, gy + side * 0.28, gz + 0.65), (gx - 1.90, gy + side * 0.58, gz + 0.30), (gx - 2.15, gy + side * 0.72, gz + 0.05)], 0.12, cartilage)
        rasp = box(f"R2_HGP_RASP_{i}", (gx - 2.20, gy + side * 0.78, gz + 0.02), (0.45, 0.28, 0.12), necrotic, 0.05)
        rasp["functional_role"] = "necrotic-tissue scraper"

    # Pressure-sensitive cilia use cyan tips to communicate perception, not decoration.
    for i, angle in enumerate((-35, 0, 35)):
        a = math.radians(angle)
        tube(f"R2_HGP_SENSOR_CILIUM_{i}", [(gx - 1.55, gy, gz + 0.92), (gx - 2.05, gy + math.sin(a) * 0.7, gz + 1.25)], 0.045, cyan)

    # Conservative low-profile collision proxy; final creature collision waits for rig/gameplay.
    coll_g = box("COLL_R2_GARDENER_REPRESENTATIVE", (gx, gy, gz + 0.48), (2.65, 1.55, 1.05), collision, 0.24, c_collision)
    coll_g["asset_id"] = "LEV-ECO-001"
    coll_g["collision_role"] = "REPRESENTATIVE_STATIC_PROXY_NOT_RIGGED"

    # Inspection camera + portable lighting.
    cam_data = bpy.data.cameras.new("CAM_R2_MICROSET_CLOSE_DATA")
    cam_data.lens = 45
    cam = bpy.data.objects.new("CAM_R2_MICROSET_CLOSE", cam_data)
    cam.location = (-12.0, 72.0, 25.0)
    target = Vector((18.0, 124.0, 8.0))
    cam.rotation_euler = (target - cam.location).to_track_quat("-Z", "Y").to_euler()
    c_camera.objects.link(cam)

    light_data = bpy.data.lights.new("LGT_R2_MICROSET_KEY", "SPOT")
    light_data.energy = 1900
    light_data.color = (0.62, 0.86, 1.0)
    light_data.spot_size = math.radians(80)
    light_data.spot_blend = 0.62
    light = bpy.data.objects.new("LGT_R2_MICROSET_KEY", light_data)
    light.location = (5.0, 92.0, 34.0)
    light.rotation_euler = (target - light.location).to_track_quat("-Z", "Y").to_euler()
    c_camera.objects.link(light)

    scene["jardines_microset_stage"] = STAGE

    return {
        "stage": STAGE,
        "collection_objects": len(c.all_objects),
        "assets": ["LEV-INF-005", "LEV-ECO-004", "LEV-ECO-001"],
        "new_material_roles": ["LEV_MAT_MUCOSA_WET", "LEV_MAT_NECROTIC", "LEV_MAT_ALGA_PRESSURE"],
        "stable_collision_separate": True,
        "gardener_scale_status": "PROPOSAL",
        "status": "REPRESENTATIVE_DETAIL_NOT_FINAL"
    }


if __name__ == "__main__":
    print(build())
