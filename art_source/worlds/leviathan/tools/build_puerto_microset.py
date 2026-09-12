"""EXOVANT 2950 — LEVIATHAN / Puerto de la Herida representative-detail microset.

Additive deterministic pass over build_master_scene.py.
Owned claim: CLM-W10-WORLD-LEVIATHAN-001.

Purpose:
- move LEV-ARCH-001, LEV-INF-002 and LEV-INF-003 beyond primitive blockout;
- establish plausible human-graft manufacturing against living host anatomy;
- remain portable to GLB with no external textures;
- keep final PBR/UV/runtime budgets unclaimed.
"""

import bpy
import math
from mathutils import Vector

SOURCE_STAGE = "PUERTO_MICROSET_V1"


def build():
    scene = bpy.context.scene
    root = bpy.data.collections.get("LEV_W10_MASTER")
    if root is None:
        raise RuntimeError("Base LEVIATHAN master scene is required before Puerto microset pass")

    # Remove previous microset deterministically.
    old = bpy.data.collections.get("24_R1_HERO_GRAFT_MICROSET")
    if old:
        for obj in list(old.all_objects):
            bpy.data.objects.remove(obj, do_unlink=True)
        bpy.data.collections.remove(old)

    # Replace four primitive blockout representatives with detailed equivalents.
    for name in ["R1_COLONY_MODULE_00", "R1_MODULE_TECH_BELLY_00", "R1_SUTURE_CLAMP_02", "R1_AIRLOCK_VALVE"]:
        obj = bpy.data.objects.get(name)
        if obj:
            bpy.data.objects.remove(obj, do_unlink=True)

    c = bpy.data.collections.new("24_R1_HERO_GRAFT_MICROSET")
    root.children.link(c)
    c_collision = bpy.data.collections.get("40_COLLISION_PROXY")
    c_camera = bpy.data.collections.get("90_CAMERAS_LIGHTS")
    if c_collision is None or c_camera is None:
        raise RuntimeError("Base collision/camera collections missing")

    def mat(name):
        m = bpy.data.materials.get(name)
        if m is None:
            raise RuntimeError(f"Required base material missing: {name}")
        return m

    ivory = mat("HUM_MAT_IVORY_CERAMIC")
    tech = mat("HUM_MAT_DARK_TECH")
    membrane = mat("LEV_MAT_MEMBRANE")
    cartilage = mat("LEV_MAT_CARTILAGE")
    vascular = mat("LEV_MAT_VASCULAR")
    amber = mat("SIGNAL_AMBER_REFUGE")
    cyan = mat("SIGNAL_CYAN_MEMORY")
    collision = mat("DEBUG_COLLISION_STABLE")

    def portable_material(name, color, roughness, metallic):
        existing = bpy.data.materials.get(name)
        if existing:
            return existing
        m = bpy.data.materials.new(name)
        m.use_nodes = True
        bsdf = m.node_tree.nodes.get("Principled BSDF")
        bsdf.inputs["Base Color"].default_value = (*color, 1.0)
        bsdf.inputs["Roughness"].default_value = roughness
        bsdf.inputs["Metallic"].default_value = metallic
        return m

    metal = portable_material("HUM_MAT_BRUSHED_METAL", (0.18, 0.20, 0.22), 0.30, 0.86)
    seal = portable_material("HUM_MAT_SEAL_RUBBER", (0.018, 0.022, 0.026), 0.82, 0.02)

    def link(obj, target=c):
        for oc in list(obj.users_collection):
            oc.objects.unlink(obj)
        target.objects.link(obj)
        return obj

    def assign(obj, material):
        if hasattr(obj.data, "materials"):
            obj.data.materials.append(material)
        return obj

    def box(name, loc, dims, material, bevel=0.08, target=c, rot=(0, 0, 0)):
        bpy.ops.mesh.primitive_cube_add(location=loc, rotation=rot)
        o = bpy.context.object
        o.name = name
        o.dimensions = dims
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        if bevel:
            b = o.modifiers.new("Physical_Bevel", "BEVEL")
            b.width = bevel
            b.segments = 3
        assign(o, material)
        return link(o, target)

    def cylinder(name, loc, radius, depth, material, rot=(0, 0, 0), vertices=32, target=c):
        bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=loc, rotation=rot)
        o = bpy.context.object
        o.name = name
        assign(o, material)
        return link(o, target)

    def torus(name, loc, major, minor, material, rot=(0, 0, 0), target=c, major_segments=64, minor_segments=12):
        bpy.ops.mesh.primitive_torus_add(major_radius=major, minor_radius=minor, major_segments=major_segments, minor_segments=minor_segments, location=loc, rotation=rot)
        o = bpy.context.object
        o.name = name
        assign(o, material)
        return link(o, target)

    def tube(name, points, radius, material, target=c):
        cu = bpy.data.curves.new(name + "_CURVE", "CURVE")
        cu.dimensions = "3D"
        cu.resolution_u = 4
        cu.bevel_depth = radius
        cu.bevel_resolution = 3
        sp = cu.splines.new("BEZIER")
        sp.bezier_points.add(len(points) - 1)
        for bp, co in zip(sp.bezier_points, points):
            bp.co = co
            bp.handle_left_type = "AUTO"
            bp.handle_right_type = "AUTO"
        o = bpy.data.objects.new(name, cu)
        target.objects.link(o)
        assign(o, material)
        return o

    def empty(name, asset_id, tier):
        o = bpy.data.objects.new(name, None)
        c.objects.link(o)
        o["asset_id"] = asset_id
        o["quality_tier"] = tier
        o["production_state"] = "REPRESENTATIVE_DETAIL_NOT_FINAL"
        o["generator_stage"] = SOURCE_STAGE
        return o

    # ------------------------------------------------------------------
    # A. LEV-ARCH-001 — pressurized human graft module A
    # ------------------------------------------------------------------
    module = empty("R1_HERO_GRAFT_MODULE_A_ROOT", "LEV-ARCH-001", "A")
    module["manufacturing_logic"] = "metal pressure frame + replaceable ivory ceramic panels + elastomer seals + exposed service underbelly"
    module["real_dimensions_m"] = "24 x 12 x 10 envelope"

    cx, cy = -250.0, -100.0
    box("R1_HG_A_PRESSURE_CORE", (cx, cy, 9.0), (23.0, 11.0, 9.1), tech, 0.35)
    box("R1_HG_A_UNDERBELLY", (cx, cy, 3.65), (18.0, 8.7, 2.1), tech, 0.22)

    # Five structural pressure hoops, each built from four serviceable members.
    for i, x in enumerate((-260.0, -255.0, -250.0, -245.0, -240.0)):
        box(f"R1_HG_A_FRAME_{i}_TOP", (x, cy, 13.8), (0.34, 12.25, 0.38), metal, 0.07)
        box(f"R1_HG_A_FRAME_{i}_BOTTOM", (x, cy, 4.25), (0.34, 12.25, 0.38), metal, 0.07)
        box(f"R1_HG_A_FRAME_{i}_L", (x, cy - 5.95, 9.0), (0.34, 0.38, 9.3), metal, 0.07)
        box(f"R1_HG_A_FRAME_{i}_R", (x, cy + 5.95, 9.0), (0.34, 0.38, 9.3), metal, 0.07)

    # Replaceable ceramic panel cassettes. Seams remain visible for maintenance realism.
    panel_x = (-257.5, -252.5, -247.5, -242.5)
    for i, x in enumerate(panel_x):
        box(f"R1_HG_A_PANEL_TOP_{i}", (x, cy, 14.0), (4.55, 11.35, 0.32), ivory, 0.10)
        box(f"R1_HG_A_PANEL_SIDE_L_{i}", (x, cy - 6.08, 9.05), (4.55, 0.30, 8.75), ivory, 0.10)
        box(f"R1_HG_A_PANEL_SIDE_R_{i}", (x, cy + 6.08, 9.05), (4.55, 0.30, 8.75), ivory, 0.10)

    # Pressure endcaps and a physically scaled service door.
    box("R1_HG_A_ENDCAP_FRONT", (-238.25, cy, 9.0), (0.34, 11.25, 8.8), ivory, 0.14)
    box("R1_HG_A_ENDCAP_REAR", (-261.75, cy, 9.0), (0.34, 11.25, 8.8), ivory, 0.14)
    box("R1_HG_A_DOOR", (-262.0, cy, 8.2), (0.28, 2.15, 4.35), tech, 0.10)
    box("R1_HG_A_DOOR_FRAME_TOP", (-262.18, cy, 10.55), (0.22, 2.65, 0.25), metal, 0.05)
    box("R1_HG_A_DOOR_FRAME_L", (-262.18, cy - 1.25, 8.2), (0.22, 0.22, 4.6), metal, 0.05)
    box("R1_HG_A_DOOR_FRAME_R", (-262.18, cy + 1.25, 8.2), (0.22, 0.22, 4.6), metal, 0.05)
    cylinder("R1_HG_A_DOOR_HANDLE", (-262.42, cy + 0.72, 8.25), 0.11, 0.42, metal, (0, math.radians(90), 0), 20)

    # Diagnostic window: cyan means memory/diagnostic, not generic decoration.
    box("R1_HG_A_DIAGNOSTIC_WINDOW", (-250.0, cy - 6.26, 10.5), (4.2, 0.16, 1.55), cyan, 0.05)

    # Four load paths down to the stable deck; tissue collar indicates the graft transition.
    for i, (x, y) in enumerate([(-258.5, -104.0), (-241.5, -104.0), (-258.5, -96.0), (-241.5, -96.0)]):
        cylinder(f"R1_HG_A_LEG_{i}", (x, y, 3.0), 0.32, 4.2, metal, vertices=24)
        torus(f"R1_HG_A_FOOT_SEAL_{i}", (x, y, 1.05), 0.72, 0.18, seal, major_segments=36, minor_segments=10)
        tube(f"R1_HG_A_TISSUE_GASKET_{i}", [(x, y, 1.0), (x + (1.5 if i % 2 else -1.5), y, 0.4), (x + (2.5 if i % 2 else -2.5), y + (1.3 if i > 1 else -1.3), 0.2)], 0.32, membrane)

    # Service plumbing exits downward and bends toward the living interface.
    tube("R1_HG_A_SERVICE_RED", [(-246, -95.2, 4.2), (-244, -93.5, 2.6), (-241, -92.0, 1.2)], 0.22, vascular)
    tube("R1_HG_A_SERVICE_CYAN", [(-252, -95.2, 4.2), (-254, -93.2, 2.8), (-257, -91.2, 1.2)], 0.18, cyan)
    cylinder("R1_HG_A_DRAIN", (-250, -94.4, 3.9), 0.24, 1.2, metal, (math.radians(90), 0, 0), 24)

    coll_module = box("COLL_R1_HERO_GRAFT_MODULE_A", (cx, cy, 8.4), (24.0, 12.0, 9.0), collision, 0.5, c_collision)
    coll_module["collision_role"] = "COMPOUND_PROXY_FUTURE; CURRENT_SIMPLE_BOX"
    coll_module["asset_id"] = "LEV-ARCH-001"

    # ------------------------------------------------------------------
    # B. LEV-INF-002 — hero suture clamp
    # ------------------------------------------------------------------
    clamp_root = empty("R1_HERO_SUTURE_CLAMP_ROOT", "LEV-INF-002", "A")
    clamp_root["manufacturing_logic"] = "opposed anchor plates + tension yoke + replaceable bolts + compression pads"
    sx, sy = -210.0, -17.0
    box("R1_HSC_INNER_PLATE", (sx, sy - 8.2, 9.4), (8.0, 5.4, 1.1), ivory, 0.18)
    box("R1_HSC_OUTER_PLATE", (sx, sy + 8.2, 9.4), (8.0, 5.4, 1.1), ivory, 0.18)
    box("R1_HSC_TENSION_YOKE", (sx, sy, 13.0), (6.8, 21.8, 1.65), metal, 0.22)
    box("R1_HSC_PAD_INNER", (sx, sy - 7.8, 8.65), (6.8, 4.4, 0.42), seal, 0.12)
    box("R1_HSC_PAD_OUTER", (sx, sy + 7.8, 8.65), (6.8, 4.4, 0.42), seal, 0.12)
    for j, x in enumerate((sx - 2.55, sx + 2.55)):
        for k, y in enumerate((sy - 8.2, sy + 8.2)):
            cylinder(f"R1_HSC_TENSION_ROD_{j}_{k}", (x, y, 11.15), 0.18, 4.1, metal, vertices=20)
            cylinder(f"R1_HSC_BOLT_HEAD_{j}_{k}", (x, y, 13.35), 0.34, 0.28, metal, vertices=12)
    cylinder("R1_HSC_TURNBUCKLE", (sx, sy, 14.35), 0.38, 8.0, metal, (0, math.radians(90), 0), 24)
    tube("R1_HSC_LOAD_SENSOR", [(sx - 3.0, sy - 1.2, 13.6), (sx - 4.2, sy, 14.5), (sx - 3.0, sy + 1.2, 13.6)], 0.10, cyan)

    # ------------------------------------------------------------------
    # C. LEV-INF-003 — living/mechanical valve at scar boundary
    # ------------------------------------------------------------------
    valve_root = empty("R1_HERO_LIVING_VALVE_ROOT", "LEV-INF-003", "A")
    valve_root["function"] = "pressure isolation + traversable service aperture"
    valve_root["construction_logic"] = "human actuator cage compresses a living cartilage/membrane iris without pretending the tissue is machined metal"
    vx, vy, vz = -143.0, -75.0, 11.0
    # Normal points radially outward (+X); torus plane is YZ.
    rot_y = (0, math.radians(90), 0)
    torus("R1_HLV_OUTER_FRAME", (vx, vy, vz), 6.75, 0.72, metal, rot_y, major_segments=72)
    torus("R1_HLV_CARTILAGE_RING", (vx - 0.25, vy, vz), 5.45, 0.78, cartilage, rot_y, major_segments=72)
    torus("R1_HLV_MEMBRANE_RING", (vx - 0.48, vy, vz), 4.05, 0.88, membrane, rot_y, major_segments=72)
    torus("R1_HLV_PRESSURE_SEAL", (vx + 0.15, vy, vz), 6.05, 0.20, seal, rot_y, major_segments=72, minor_segments=10)

    # Eight actuator pods and six iris leaves in the YZ aperture plane.
    for i in range(8):
        a = math.radians(i * 45)
        y = vy + 6.72 * math.cos(a)
        z = vz + 6.72 * math.sin(a)
        cylinder(f"R1_HLV_ACTUATOR_{i}", (vx + 0.1, y, z), 0.34, 1.7, metal, (0, math.radians(90), 0), 20)
        if i % 2 == 0:
            torus(f"R1_HLV_STATUS_{i}", (vx + 1.0, y, z), 0.38, 0.10, amber, rot_y, major_segments=24, minor_segments=8)
    for i in range(6):
        a = math.radians(i * 60)
        y = vy + 1.55 * math.cos(a)
        z = vz + 1.55 * math.sin(a)
        blade = box(f"R1_HLV_IRIS_BLADE_{i}", (vx - 0.05, y, z), (0.32, 1.45, 4.1), cartilage, 0.16, c, (a, 0, math.radians(18)))
        blade["moving_part"] = True
        blade["rig_dependency"] = "future valve rig"

    tube("R1_HLV_VASCULAR_FEED_A", [(vx - 2.0, vy - 4.0, vz - 4.0), (vx - 7.0, vy - 7.0, vz - 5.0), (vx - 13.0, vy - 8.0, vz - 6.0)], 0.42, vascular)
    tube("R1_HLV_VASCULAR_FEED_B", [(vx - 2.0, vy + 4.0, vz + 3.5), (vx - 8.0, vy + 7.0, vz + 5.0), (vx - 14.0, vy + 9.0, vz + 4.0)], 0.34, vascular)
    tube("R1_HLV_DIAGNOSTIC_LINE", [(vx + 0.8, vy - 5.7, vz + 3.0), (vx + 2.5, vy - 8.0, vz + 5.0), (vx + 4.0, vy - 10.0, vz + 5.5)], 0.10, cyan)

    # Inspection camera and portable key light for the microset.
    cam_data = bpy.data.cameras.new("CAM_R1_MICROSET_CLOSE_DATA")
    cam_data.lens = 42
    cam = bpy.data.objects.new("CAM_R1_MICROSET_CLOSE", cam_data)
    cam.location = (-305.0, -175.0, 27.0)
    c_camera.objects.link(cam)
    target = Vector((-220.0, -79.0, 10.0))
    cam.rotation_euler = (target - cam.location).to_track_quat("-Z", "Y").to_euler()

    light_data = bpy.data.lights.new("LGT_R1_MICROSET_KEY", "SPOT")
    light_data.energy = 2200
    light_data.color = (1.0, 0.72, 0.55)
    light_data.spot_size = math.radians(75)
    light_data.spot_blend = 0.55
    light = bpy.data.objects.new("LGT_R1_MICROSET_KEY", light_data)
    light.location = (-285.0, -145.0, 42.0)
    light.rotation_euler = (target - light.location).to_track_quat("-Z", "Y").to_euler()
    c_camera.objects.link(light)

    scene["puerto_microset_stage"] = SOURCE_STAGE
    return {
        "stage": SOURCE_STAGE,
        "collection_objects": len(c.all_objects),
        "module_asset": "LEV-ARCH-001",
        "suture_asset": "LEV-INF-002",
        "valve_asset": "LEV-INF-003",
        "new_material_roles": ["HUM_MAT_BRUSHED_METAL", "HUM_MAT_SEAL_RUBBER"],
        "camera": "CAM_R1_MICROSET_CLOSE",
        "status": "REPRESENTATIVE_DETAIL_NOT_FINAL"
    }


if __name__ == "__main__":
    print(build())
