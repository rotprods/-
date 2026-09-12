"""Aurora Veil L1 orbital display representation.

Runs against the existing Aurora world scene. The 5,900 km radius is a PROPOSAL
from ADR-AUR-001, never canon. Geometry is a 1e-4 display proxy, deliberately
separate from local 1:1 metre gameplay frames. No continental geography is
authored because the canon does not define it.

Blender worker validated: 5.2.
"""
import bpy
import math
from mathutils import Vector

PHYSICAL_RADIUS_M_PROPOSAL = 5_900_000.0
DISPLAY_SCALE = 1e-4
DISPLAY_RADIUS_M = PHYSICAL_RADIUS_M_PROPOSAL * DISPLAY_SCALE
CENTER = Vector((8000.0, 0.0, 0.0))
COLLECTION = "14_ORBITAL_PROXY"


def ensure_collection(name, parent):
    c = bpy.data.collections.get(name)
    if not c:
        c = bpy.data.collections.new(name)
        parent.children.link(c)
    return c


def move_to(obj, col):
    for current in list(obj.users_collection):
        current.objects.unlink(obj)
    col.objects.link(obj)
    return obj


def material(name, base, metallic=0.0, roughness=0.5, emission=None, alpha=1.0):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    p = m.node_tree.nodes.get("Principled BSDF")
    p.inputs["Base Color"].default_value = (*base, 1.0)
    p.inputs["Metallic"].default_value = metallic
    p.inputs["Roughness"].default_value = roughness
    p.inputs["Alpha"].default_value = alpha
    if emission:
        color, strength = emission
        p.inputs["Emission Color"].default_value = (*color, 1.0)
        p.inputs["Emission Strength"].default_value = strength
    if alpha < 1.0:
        m.surface_render_method = "DITHERED"
    return m


def ribbon(name, latitude_degrees, phase, mat, col, amplitude=8.0):
    latitude = math.radians(latitude_degrees)
    points = []
    count = 96
    for i in range(count + 1):
        a = 2.0 * math.pi * i / count
        r = DISPLAY_RADIUS_M * 1.028 + amplitude * (
            0.55 * math.sin(a * 3.0 + phase) + 0.25 * math.sin(a * 7.0 - phase)
        )
        xy = r * math.cos(latitude)
        z = r * math.sin(latitude) + 6.0 * math.sin(a * 2.0 + phase)
        points.append((CENTER.x + xy * math.cos(a), CENTER.y + xy * math.sin(a), CENTER.z + z))
    curve = bpy.data.curves.new(name, "CURVE")
    curve.dimensions = "3D"
    curve.resolution_u = 2
    curve.bevel_depth = 3.4
    curve.bevel_resolution = 3
    spline = curve.splines.new("POLY")
    spline.points.add(len(points) - 1)
    for i, p in enumerate(points):
        spline.points[i].co = (*p, 1.0)
    obj = bpy.data.objects.new(name, curve)
    col.objects.link(obj)
    curve.materials.append(mat)
    obj["asset_id"] = "AUR-ATM-001"
    obj["layer"] = "aurora_ribbon"
    obj["physical_interpretation"] = "display proxy; not canonical field map"
    return obj


def build():
    scene = bpy.context.scene
    root = bpy.data.collections.get("AURORA_VEIL_ROOT") or scene.collection
    orbital = ensure_collection(COLLECTION, root)
    cameras = ensure_collection("13_CAMERAS", root)

    # Idempotent replacement of this package only.
    for obj in list(orbital.objects):
        bpy.data.objects.remove(obj, do_unlink=True)
    old_camera = bpy.data.objects.get("CAM_AURORA_ORBITAL_L1")
    if old_camera:
        bpy.data.objects.remove(old_camera, do_unlink=True)

    body_mat = material("AUR_MAT_ORBITAL_BODY_PROXY", (0.026, 0.055, 0.067), roughness=0.88)
    atm_mat = material(
        "AUR_MAT_ATMOSPHERE_PROXY", (0.04, 0.22, 0.30), roughness=0.32,
        emission=((0.02, 0.18, 0.30), 0.4), alpha=0.18
    )
    teal = material(
        "AUR_MAT_ORBITAL_AURORA_PROXY", (0.02, 0.16, 0.14), roughness=0.25,
        emission=((0.03, 0.95, 0.73), 5.0), alpha=0.72
    )
    violet = material(
        "AUR_MAT_ORBITAL_AURORA_VIOLET", (0.10, 0.02, 0.17), roughness=0.25,
        emission=((0.48, 0.06, 1.0), 4.2), alpha=0.66
    )
    steel = bpy.data.materials.get("AUR_MAT_OBSERVATORY_STEEL") or material(
        "AUR_MAT_OBSERVATORY_STEEL", (0.07, 0.09, 0.11), 0.78, 0.30
    )
    bronze = bpy.data.materials.get("AUR_MAT_CLOCK_BRONZE") or material(
        "AUR_MAT_CLOCK_BRONZE", (0.27, 0.15, 0.055), 0.62, 0.42
    )

    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=5, radius=DISPLAY_RADIUS_M, location=CENTER)
    body = bpy.context.object
    body.name = "AUR_PLN_001_ORBITAL_SHELL"
    body.data.materials.append(body_mat)
    move_to(body, orbital)
    body["asset_id"] = "AUR-PLN-001"
    body["epistemic"] = "PROPOSAL_DISPLAY_REPRESENTATION"
    body["physical_radius_m_proposal"] = PHYSICAL_RADIUS_M_PROPOSAL
    body["display_radius_m"] = DISPLAY_RADIUS_M
    body["display_scale"] = DISPLAY_SCALE
    body["global_geography"] = "UNKNOWN_NOT_AUTHORED"
    body["quality_tier"] = "D_ORBITAL_PROXY"

    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=96, ring_count=48, radius=DISPLAY_RADIUS_M * 1.022, location=CENTER
    )
    atmosphere = bpy.context.object
    atmosphere.name = "AUR_ATM_001_ATMOSPHERE_SHELL"
    atmosphere.data.materials.append(atm_mat)
    move_to(atmosphere, orbital)
    atmosphere["asset_id"] = "AUR-ATM-001"
    atmosphere["epistemic"] = "PROPOSAL_VISUAL_LAYER"
    atmosphere["separate_from_surface"] = True

    for i, (lat, phase, mat) in enumerate(
        ((67, 0.2, teal), (73, 1.1, violet), (-65, 2.0, teal), (-71, 2.9, violet))
    ):
        ribbon(f"AUR_ATM_001_AURORA_RIBBON_{i}", lat, phase, mat, orbital)

    # Two stations are canon; exact orbital altitude/layout remains proposal.
    for idx, angle in enumerate((math.radians(22), math.radians(204))):
        rr = DISPLAY_RADIUS_M * 1.34
        location = CENTER + Vector((rr * math.cos(angle), rr * math.sin(angle), 180 if idx == 0 else -145))
        bpy.ops.mesh.primitive_torus_add(
            major_radius=19, minor_radius=2.1, major_segments=40, minor_segments=8,
            location=location, rotation=(math.radians(72), 0, angle)
        )
        station = bpy.context.object
        station.name = f"AUR_ORBITAL_OBSERVATION_STATION_{idx + 1}"
        station.data.materials.append(steel)
        move_to(station, orbital)
        station["canon"] = "two observation stations with divergent clocks"
        station["orbit_altitude"] = "PROPOSAL_DISPLAY_ONLY"
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=24, radius=6, depth=8, location=location,
            rotation=(math.radians(72), 0, angle)
        )
        core = bpy.context.object
        core.name = f"AUR_ORBITAL_CLOCK_CORE_{idx + 1}"
        core.data.materials.append(bronze)
        move_to(core, orbital)

    anchor = bpy.data.objects.new("AUR_ORBITAL_METADATA_ANCHOR", None)
    anchor.location = CENTER
    orbital.objects.link(anchor)
    anchor["physical_radius_m_proposal"] = PHYSICAL_RADIUS_M_PROPOSAL
    anchor["display_radius_m"] = DISPLAY_RADIUS_M
    anchor["display_scale"] = DISPLAY_SCALE
    anchor["global_planetary_geography"] = "UNKNOWN"
    anchor["layer_contract"] = "surface / atmosphere / aurora / stations separate"

    bpy.ops.object.camera_add(location=(CENTER.x + 1540, CENTER.y - 1920, CENTER.z + 780))
    camera = bpy.context.object
    camera.name = "CAM_AURORA_ORBITAL_L1"
    camera.data.lens = 58
    camera.data.clip_end = 6000
    camera.rotation_euler = (CENTER - camera.location).to_track_quat("-Z", "Y").to_euler()
    move_to(camera, cameras)

    # Reuse the single stellar SUN_VELAR_LOW. Do not create another SUN; a directional light is global.
    scene["orbital_representation"] = "L1_DISPLAY_PROXY"
    scene["orbital_physical_radius_m_proposal"] = PHYSICAL_RADIUS_M_PROPOSAL
    scene["orbital_display_scale"] = DISPLAY_SCALE
    scene["orbital_global_geography"] = "UNKNOWN_NOT_INVENTED"
    scene["orbital_lighting_contract"] = "reuse SUN_VELAR_LOW; no second global directional light"
    scene["status"] = "WAVE1_ORBITAL_L1_REPRODUCIBLE"


if __name__ == "__main__":
    build()
