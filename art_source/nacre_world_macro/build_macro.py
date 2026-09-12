"""EXOVANT 2950 — NACRE macro-foundation deterministic Blender generator.

Scope: CLM-NACRE-WORLD-MACRO-001 / AGENT-3D-NACRE-01
Target: Blender 5.2, metre scale. Rebuilds the revision-3 blockout contract.

DOCUMENTED canon used by this script:
- Nacre / Mneme / Casas de Nácar.
- Cities grow inside kilometre-scale mineral shells.
- Archivo de MNEMOS uses spherical archive rooms connected by bridges.
- Reference gravity is 0.26 g.

PROPOSAL only (reversible blockout values, NOT planetary canon):
- shell envelope target ~1400 m span;
- archive core diameter 184 m;
- exact archive positions, bridge widths and shell-rib spacing.

The script intentionally does NOT define planetary radius/diameter, final playable area,
final LOD/performance budgets, final collision, characters, MNEMOS anatomy, vehicles or runtime.
"""

import bpy
import math
from mathutils import Vector

BUILD_MACRO_VERSION = 3
CLAIM_ID = "CLM-NACRE-WORLD-MACRO-001"
AGENT_ID = "AGENT-3D-NACRE-01"


def reset_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 1.0
    scene.render.engine = "BLENDER_EEVEE"
    if scene.world is None:
        scene.world = bpy.data.worlds.new("NACRE_WORLD")
    scene.world.color = (0.002, 0.003, 0.008)
    return scene


def collection(name, scene):
    c = bpy.data.collections.get(name) or bpy.data.collections.new(name)
    if c not in scene.collection.children:
        scene.collection.children.link(c)
    return c


def move_to(obj, target):
    for c in list(obj.users_collection):
        c.objects.unlink(obj)
    target.objects.link(obj)


def material(name, base, rough, metal=0.0, alpha=1.0, emission=None, emission_strength=0.0):
    old = bpy.data.materials.get(name)
    if old:
        return old
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bs = m.node_tree.nodes.get("Principled BSDF")
    bs.inputs["Base Color"].default_value = (*base, 1.0)
    bs.inputs["Roughness"].default_value = rough
    bs.inputs["Metallic"].default_value = metal
    if "Alpha" in bs.inputs:
        bs.inputs["Alpha"].default_value = alpha
    if emission is not None:
        key = "Emission Color" if "Emission Color" in bs.inputs else "Emission"
        if key in bs.inputs:
            bs.inputs[key].default_value = (*emission, 1.0)
        if "Emission Strength" in bs.inputs:
            bs.inputs["Emission Strength"].default_value = emission_strength
    m.diffuse_color = (*base, alpha)
    if alpha < 1.0:
        try:
            m.surface_render_method = "DITHERED"
        except Exception:
            pass
    return m


def poly_curve(name, pts, radius, mat, target):
    cu = bpy.data.curves.new(name + "_CURVE", "CURVE")
    cu.dimensions = "3D"
    cu.resolution_u = 2
    cu.bevel_depth = radius
    cu.bevel_resolution = 2
    sp = cu.splines.new("POLY")
    sp.points.add(len(pts) - 1)
    for point, co in zip(sp.points, pts):
        point.co = (*co, 1.0)
    obj = bpy.data.objects.new(name, cu)
    target.objects.link(obj)
    obj.data.materials.append(mat)
    return obj


def shell_patch(name, target, mat, scale, theta0, theta1, phi0, phi1, nt=72, np=36, thickness=10.0):
    verts, faces = [], []
    for j in range(np + 1):
        ph = phi0 + (phi1 - phi0) * j / np
        s, c = math.sin(ph), math.cos(ph)
        for i in range(nt + 1):
            th = theta0 + (theta1 - theta0) * i / nt
            wobble = 1.0 + 0.022 * math.sin(3 * th + 0.7) * math.sin(2 * ph) + 0.012 * math.sin(7 * ph)
            verts.append((
                scale[0] * s * math.cos(th) * wobble,
                scale[1] * s * math.sin(th) * wobble,
                scale[2] * c * wobble,
            ))
    stride = nt + 1
    for j in range(np):
        for i in range(nt):
            a = j * stride + i
            faces.append((a, a + 1, a + stride + 1, a + stride))
    mesh = bpy.data.meshes.new(name + "_MESH")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    target.objects.link(obj)
    solid = obj.modifiers.new("PhysicalThickness", "SOLIDIFY")
    solid.thickness = thickness
    solid.offset = 0.0
    bevel = obj.modifiers.new("MacroEdgeSoftening", "BEVEL")
    bevel.width = 1.2
    bevel.segments = 2
    obj.data.materials.append(mat)
    return obj


def beam_between(name, a, b, width, height, mat, target, z_offset=0.0):
    a, b = Vector(a), Vector(b)
    d = b - a
    mid = (a + b) * 0.5
    mid.z += z_offset
    bpy.ops.mesh.primitive_cube_add(size=1, location=mid)
    obj = bpy.context.object
    obj.name = name
    move_to(obj, target)
    obj.rotation_mode = "QUATERNION"
    obj.rotation_quaternion = d.to_track_quat("X", "Z")
    obj.dimensions = (d.length, width, height)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.data.materials.append(mat)
    bevel = obj.modifiers.new("EdgeRadius", "BEVEL")
    bevel.width = min(0.6, height * 0.28)
    bevel.segments = 2
    return obj


def socket(name, point, axis, radius, depth, mat, target):
    bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=radius, depth=depth, location=point)
    obj = bpy.context.object
    obj.name = name
    move_to(obj, target)
    obj.rotation_mode = "QUATERNION"
    obj.rotation_quaternion = Vector(axis).to_track_quat("Z", "Y")
    obj.data.materials.append(mat)
    bevel = obj.modifiers.new("SocketEdge", "BEVEL")
    bevel.width = 0.35
    bevel.segments = 2
    return obj


def point_camera(cam, target):
    cam.rotation_euler = (Vector(target) - cam.location).to_track_quat("-Z", "Y").to_euler()


def build():
    scene = reset_scene()
    c_shell = collection("10_SHELL_CITY", scene)
    c_arch = collection("20_ARCHIVE_SPHERES", scene)
    c_bridge = collection("30_BRIDGES", scene)
    c_struct = collection("35_STRUCTURAL_SUPPORTS", scene)
    c_scale = collection("40_SCALE_REFERENCE", scene)
    c_light = collection("90_LIGHTING", scene)

    m_outer = material("MAT_Nacre_OuterMineral", (0.24, 0.25, 0.23), 0.72, 0.02)
    m_inner = material("MAT_Nacre_InnerPearl", (0.62, 0.70, 0.68), 0.28, 0.06)
    m_struct = material("MAT_Nacre_StructureDark", (0.035, 0.045, 0.052), 0.32, 0.82)
    m_archive = material("MAT_Nacre_ArchivePearl", (0.68, 0.80, 0.86), 0.22, 0.03)
    m_deck = material("MAT_Nacre_ServiceDeck", (0.12, 0.13, 0.14), 0.48, 0.55)
    m_plate = material("MAT_Nacre_PalimpsestPlate", (0.46, 0.74, 0.78), 0.18, 0.0, 0.30)
    m_signal = material("MAT_Nacre_ArchiveSignal", (0.12, 0.42, 0.58), 0.26, 0.0, 1.0, (0.05, 0.42, 0.66), 2.4)
    m_human = material("MAT_ScaleHuman", (0.72, 0.17, 0.09), 0.58)

    shell_patch(
        "NACRE_SHELL_CITY_ENVELOPE", c_shell, m_outer, (700, 560, 430),
        math.radians(-30), math.radians(210), math.radians(18), math.radians(162), 72, 36, 10.0,
    )
    inner = shell_patch(
        "NACRE_INNER_PEARL_LINING", c_shell, m_inner, (682, 542, 414),
        math.radians(-28), math.radians(208), math.radians(22), math.radians(158), 60, 30, 4.0,
    )

    for idx, th_deg in enumerate(range(-18, 199, 18)):
        th = math.radians(th_deg)
        pts = []
        for k in range(31):
            ph = math.radians(28 + 124 * k / 30)
            s, c = math.sin(ph), math.cos(ph)
            pts.append((665 * s * math.cos(th), 525 * s * math.sin(th), 400 * c))
        poly_curve(f"SHELL_RIB_{idx:02d}", pts, 2.8, m_struct, c_shell)

    for idx, ph_deg in enumerate((42, 64, 88, 112, 136)):
        ph = math.radians(ph_deg)
        pts = []
        for k in range(70):
            th = math.radians(-22 + 224 * k / 69)
            s, c = math.sin(ph), math.cos(ph)
            pts.append((670 * s * math.cos(th), 530 * s * math.sin(th), 404 * c))
        poly_curve(f"SHELL_BELT_{idx:02d}", pts, 1.7, m_struct, c_shell)

    archive_specs = [
        ("ARCHIVE_CORE", (0, 80, 20), 92),
        ("ARCHIVE_NW", (-165, 100, 105), 58),
        ("ARCHIVE_NE", (170, 115, 115), 62),
        ("ARCHIVE_W", (-245, 55, -55), 46),
        ("ARCHIVE_E", (245, 70, -38), 50),
        ("ARCHIVE_UP", (15, 155, 195), 42),
        ("ARCHIVE_LOW", (8, 40, -160), 48),
    ]
    archives = {}
    radii = {}
    for name, pos, radius in archive_specs:
        bpy.ops.mesh.primitive_uv_sphere_add(segments=40, ring_count=24, radius=radius, location=pos)
        obj = bpy.context.object
        obj.name = name
        move_to(obj, c_arch)
        obj.data.materials.append(m_archive)
        for face in obj.data.polygons:
            face.use_smooth = True
        for ridx, rot in enumerate(((0, 0, 0), (math.pi / 2, 0, 0))):
            bpy.ops.mesh.primitive_torus_add(
                major_radius=radius * 1.015,
                minor_radius=max(0.9, radius * 0.018),
                major_segments=48,
                minor_segments=8,
                location=pos,
                rotation=rot,
            )
            tor = bpy.context.object
            tor.name = f"{name}_FRAME_{ridx}"
            move_to(tor, c_arch)
            tor.data.materials.append(m_struct)
        bpy.ops.mesh.primitive_uv_sphere_add(
            segments=24, ring_count=12, radius=max(2.2, radius * 0.06),
            location=(pos[0], pos[1] - radius * 0.91, pos[2]),
        )
        sig = bpy.context.object
        sig.name = f"{name}_SIGNAL"
        move_to(sig, c_arch)
        sig.data.materials.append(m_signal)
        archives[name] = obj
        radii[name] = radius

    links = [
        ("ARCHIVE_CORE", "ARCHIVE_NW"), ("ARCHIVE_CORE", "ARCHIVE_NE"),
        ("ARCHIVE_CORE", "ARCHIVE_W"), ("ARCHIVE_CORE", "ARCHIVE_E"),
        ("ARCHIVE_CORE", "ARCHIVE_UP"), ("ARCHIVE_CORE", "ARCHIVE_LOW"),
        ("ARCHIVE_NW", "ARCHIVE_UP"), ("ARCHIVE_NE", "ARCHIVE_UP"),
        ("ARCHIVE_W", "ARCHIVE_LOW"), ("ARCHIVE_E", "ARCHIVE_LOW"),
    ]
    for idx, (na, nb) in enumerate(links):
        ca, cb = Vector(archives[na].location), Vector(archives[nb].location)
        direction = (cb - ca).normalized()
        a = ca + direction * (radii[na] + 3.0)
        b = cb - direction * (radii[nb] + 3.0)
        beam_between(f"BRIDGE_DECK_{idx:02d}", a, b, 8.0, 1.4, m_deck, c_bridge)
        beam_between(f"BRIDGE_SPINE_{idx:02d}", a, b, 1.3, 3.2, m_struct, c_bridge, -4.0)
        socket(f"DOCK_{idx:02d}_A", a, direction, 5.6, 4.0, m_struct, c_struct)
        socket(f"DOCK_{idx:02d}_B", b, direction, 5.6, 4.0, m_struct, c_struct)

    entry = Vector((-20, -420, -20))
    core = Vector(archives["ARCHIVE_CORE"].location)
    direction = (core - entry).normalized()
    end = core - direction * (radii["ARCHIVE_CORE"] + 4.0)
    beam_between("BRIDGE_ENTRY_MAIN", entry, end, 12.0, 1.8, m_deck, c_bridge)
    beam_between("BRIDGE_ENTRY_SPINE", entry, end, 1.8, 4.2, m_struct, c_bridge, -5.2)
    socket("DOCK_ENTRY_CORE", end, direction, 8.0, 5.0, m_struct, c_struct)

    for name, obj in archives.items():
        radius = radii[name]
        bpy.ops.mesh.primitive_torus_add(
            major_radius=radius * 1.045, minor_radius=max(0.8, radius * 0.012),
            major_segments=48, minor_segments=8, location=obj.location,
        )
        ring = bpy.context.object
        ring.name = "SERVICE_RING_" + name
        move_to(ring, c_struct)
        ring.data.materials.append(m_deck)

    # Reversible macro load paths to the inner blockout shell.
    ea, eb, ec = 650.0, 510.0, 390.0
    for name, obj in archives.items():
        p = Vector(obj.location)
        q = (p.x / ea) ** 2 + (p.y / eb) ** 2 + (p.z / ec) ** 2
        if q < 1e-6:
            anchor = Vector((0, eb * 0.96, 0))
        else:
            anchor = p * (1.0 / math.sqrt(q)) * 0.96
        direction = (anchor - p).normalized()
        start = p + direction * (radii[name] + 3.0)
        poly_curve("SUSPENSION_" + name, [start, anchor], 1.6, m_struct, c_struct)

    # Growth-history strata: causal shell growth signal, not random surface noise.
    for idx, ph_deg in enumerate((52, 76, 100, 124, 148)):
        ph = math.radians(ph_deg)
        pts = []
        for k in range(64):
            th = math.radians(-20 + 220 * k / 63)
            s, c = math.sin(ph), math.cos(ph)
            pts.append((660 * s * math.cos(th), 520 * s * math.sin(th), 396 * c))
        poly_curve(f"GROWTH_STRATUM_{idx:02d}", pts, 0.9, m_inner, c_struct)

    # Bounded translucent accents only.
    for idx, x in enumerate((-360, -250, -140, 140, 250, 360)):
        bpy.ops.mesh.primitive_cube_add(size=1, location=(x, -360, 80 + 35 * math.sin(idx)))
        obj = bpy.context.object
        obj.name = f"TRANSLUCENT_PLATE_{idx:02d}"
        move_to(obj, c_shell)
        obj.dimensions = (70, 3, 115)
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        obj.rotation_euler[2] = math.radians((idx - 2.5) * 4)
        obj.data.materials.append(m_plate)

    bpy.ops.mesh.primitive_cube_add(size=1, location=(-20, -455, -23))
    platform = bpy.context.object
    platform.name = "ENTRY_SERVICE_PLATFORM"
    move_to(platform, c_scale)
    platform.dimensions = (120, 72, 3)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    platform.data.materials.append(m_deck)

    for idx, x in enumerate((-12, -4, 4, 12)):
        bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.28, depth=1.35, location=(x, -448, -21.825))
        body = bpy.context.object
        body.name = f"SCALE_HUMAN_{idx:02d}_BODY"
        move_to(body, c_scale)
        body.data.materials.append(m_human)
        bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=0.22, location=(x, -448, -21.02))
        head = bpy.context.object
        head.name = f"SCALE_HUMAN_{idx:02d}_HEAD"
        move_to(head, c_scale)
        head.data.materials.append(m_human)

    for idx, x in enumerate((-50, 50)):
        bpy.ops.mesh.primitive_cube_add(size=1, location=(x, -440, 27))
        pylon = bpy.context.object
        pylon.name = f"SCALE_PYLON_100M_{idx:02d}"
        move_to(pylon, c_scale)
        pylon.dimensions = (3, 3, 100)
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        pylon.data.materials.append(m_struct)

    cam_data = bpy.data.cameras.new("CAM_NACRE_MACRO")
    cam = bpy.data.objects.new("CAM_NACRE_MACRO", cam_data)
    c_light.objects.link(cam)
    cam.location = (0, -1120, 210)
    cam_data.lens = 38
    cam_data.clip_start = 0.1
    cam_data.clip_end = 5000
    point_camera(cam, (0, 70, 30))
    scene.camera = cam

    def add_sun(name, rotation, color, energy, angle):
        data = bpy.data.lights.new(name, "SUN")
        data.energy = energy
        data.color = color
        data.angle = angle
        obj = bpy.data.objects.new(name, data)
        c_light.objects.link(obj)
        obj.rotation_euler = rotation

    add_sun("SUN_MNEME_A", (math.radians(38), math.radians(-28), math.radians(-22)), (1.0, 0.79, 0.58), 3.2, math.radians(5.0))
    add_sun("SUN_MNEME_B", (math.radians(68), math.radians(34), math.radians(142)), (0.58, 0.76, 1.0), 1.6, math.radians(3.0))

    scene["EXOVANT_WORLD"] = "NACRE"
    scene["CLAIM_ID"] = CLAIM_ID
    scene["AGENT_ID"] = AGENT_ID
    scene["BUILD_MACRO_VERSION"] = BUILD_MACRO_VERSION
    scene["DOCUMENTED_GRAVITY_G"] = 0.26
    scene["PROPOSAL_shell_span_m"] = 1400.0
    scene["PROPOSAL_archive_core_diameter_m"] = 184.0
    scene["STRUCTURAL_PASS_NOTE"] = "Surface-to-surface bridges, docking sockets, service rings, suspension load paths and shell growth strata."

    return {
        "claim": CLAIM_ID,
        "build_version": BUILD_MACRO_VERSION,
        "mesh_objects": len([o for o in bpy.data.objects if o.type == "MESH"]),
        "curve_objects": len([o for o in bpy.data.objects if o.type == "CURVE"]),
        "lights": [o.name for o in bpy.data.objects if o.type == "LIGHT"],
    }


if __name__ == "__main__":
    print(build())
