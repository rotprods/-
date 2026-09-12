"""Generate the isolated SYLVA PRIME L0/L1 orbital scale proof for ADR-SYLVA-001 Option C.

IMPORTANT
---------
This is a PROPOSAL generator, not canonical world data.
Do not execute against remote project c796230b-0463-4e17-9446-2e746c5c4933 until
that projectId is present in the active fleet reservation for CLM-SYLVA-MACRO-001.

The visible L1 proxy is intentionally scaled 1:10,000 for stable Blender/orbital review.
Exact proposed physical values live as metadata on SYLVA_L0_PHYSICAL_ROOT.
No continents, biome borders, moon orbit, axial tilt, atmosphere thickness or settlement
coordinates are invented here.
"""
from __future__ import annotations

import bpy
import math
from mathutils import Vector

CLAIM = "CLM-SYLVA-MACRO-001"
ADR = "ADR-SYLVA-001"
OPTION = "SYL_SCALE_C_BROAD_BIOGENIC"
CLASSIFICATION = "PROPOSAL_PENDING_CREATIVE_DIRECTOR"

# Option C exact proposal values. Do not promote to global canon from this script.
PHYSICAL_RADIUS_M = 7_645_210.08
PHYSICAL_DIAMETER_M = 15_290_420.16
CIRCUMFERENCE_M = 48_036_271.64495726
SURFACE_AREA_KM2 = 734_494_776.3712908
MASS_EARTH = 1.6128
MEAN_DENSITY_G_CM3 = 5.14584
SURFACE_GRAVITY_EARTH = 1.12
ESCAPE_VELOCITY_KM_S = 12.972680463188784

REPRESENTATION_SCALE = 1.0 / 10_000.0
DISPLAY_RADIUS_M = PHYSICAL_RADIUS_M * REPRESENTATION_SCALE


def ensure_world(scene):
    if scene.world is None:
        scene.world = bpy.data.worlds.new("SYLVA_ORBITAL_WORLD")
    scene.world.color = (0.004, 0.007, 0.006)


def ensure_collection(scene, name):
    col = bpy.data.collections.get(name)
    if col is None:
        col = bpy.data.collections.new(name)
        scene.collection.children.link(col)
    return col


def move_to(obj, col):
    for old in list(obj.users_collection):
        old.objects.unlink(obj)
    col.objects.link(obj)


def material(name, base, metallic=0.0, roughness=0.6, emission=None, emission_strength=0.0):
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*base, 1.0)
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = roughness
    if emission is not None:
        if "Emission Color" in bsdf.inputs:
            bsdf.inputs["Emission Color"].default_value = (*emission, 1.0)
        elif "Emission" in bsdf.inputs:
            bsdf.inputs["Emission"].default_value = (*emission, 1.0)
        if "Emission Strength" in bsdf.inputs:
            bsdf.inputs["Emission Strength"].default_value = emission_strength
    return mat


def add_empty(name, loc, props, col, display="SPHERE", size=10.0):
    obj = bpy.data.objects.new(name, None)
    obj.location = loc
    obj.empty_display_type = display
    obj.empty_display_size = size
    col.objects.link(obj)
    for key, value in props.items():
        obj[key] = value
    return obj


def look_at(obj, target=(0.0, 0.0, 0.0)):
    direction = Vector(target) - obj.location
    obj.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()


def build():
    # Dedicated project only: destructive reset is intentional here.
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)

    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 1.0
    scene.render.engine = "BLENDER_EEVEE"
    scene.render.resolution_x = 1280
    scene.render.resolution_y = 720
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.film_transparent = False
    ensure_world(scene)

    meta_col = ensure_collection(scene, "SYLVA_L0_META")
    planet_col = ensure_collection(scene, "SYLVA_L1_ORBITAL_PROXY")
    review_col = ensure_collection(scene, "SYLVA_L1_REVIEW")

    physical = add_empty(
        "SYLVA_L0_PHYSICAL_ROOT",
        (0, 0, 0),
        {
            "world_id": "sylva",
            "world_name": "SYLVA PRIME",
            "claim_id": CLAIM,
            "adr": ADR,
            "option_id": OPTION,
            "classification": CLASSIFICATION,
            "canonicalized": False,
            "planet_radius_m_proposal": PHYSICAL_RADIUS_M,
            "planet_diameter_m_proposal": PHYSICAL_DIAMETER_M,
            "circumference_m_proposal": CIRCUMFERENCE_M,
            "surface_area_km2_proposal": SURFACE_AREA_KM2,
            "mass_earth_proposal": MASS_EARTH,
            "mean_density_g_cm3_proposal": MEAN_DENSITY_G_CM3,
            "surface_gravity_earth_documented": SURFACE_GRAVITY_EARTH,
            "escape_velocity_km_s_proposal": ESCAPE_VELOCITY_KM_S,
            "visible_proxy_scale": REPRESENTATION_SCALE,
            "visible_proxy_is_physical_scale": False,
            "continents": "UNKNOWN_NOT_MODELED",
            "atmosphere_thickness": "UNKNOWN_NOT_MODELED",
            "axial_tilt": "UNKNOWN_NOT_MODELED",
            "semilla_orbit": "UNKNOWN_NOT_MODELED",
        },
        meta_col,
        display="SPHERE",
        size=25.0,
    )

    # One visible, low-frequency L1 sphere. No continent layout is encoded.
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=5, radius=DISPLAY_RADIUS_M, location=(0, 0, 0))
    planet = bpy.context.object
    planet.name = "SYLVA_L1_ORBITAL_PROXY_OPTION_C"
    move_to(planet, planet_col)
    planet["classification"] = CLASSIFICATION
    planet["representation_scale"] = REPRESENTATION_SCALE
    planet["physical_radius_m_proposal"] = PHYSICAL_RADIUS_M
    planet["geography_status"] = "LOW_FREQUENCY_ABSTRACT_NO_CONTINENTS"

    # Deterministic small-amplitude abstract relief: orbital readability only, not geography.
    mesh = planet.data
    max_relief_fraction = 0.004
    for vertex in mesh.vertices:
        p = vertex.co.normalized()
        signal = (
            0.42 * math.sin(p.x * 7.0 + p.y * 3.0)
            + 0.31 * math.cos(p.y * 9.0 - p.z * 4.0)
            + 0.18 * math.sin((p.x + p.z) * 13.0)
        )
        radius = DISPLAY_RADIUS_M * (1.0 + max_relief_fraction * signal)
        vertex.co = p * radius

    surface_mat = material("SYLVA_L1_MAT_BiogenicDiagnostic", (0.035, 0.115, 0.072), 0.0, 0.74)
    planet.data.materials.append(surface_mat)

    # Equatorial scale guide only. This is a review aid, not an in-world structure.
    bpy.ops.mesh.primitive_torus_add(
        major_radius=DISPLAY_RADIUS_M * 1.012,
        minor_radius=DISPLAY_RADIUS_M * 0.0016,
        major_segments=128,
        minor_segments=8,
        location=(0, 0, 0),
    )
    guide = bpy.context.object
    guide.name = "SYLVA_L1_REVIEW_EquatorialScaleGuide"
    move_to(guide, review_col)
    guide["classification"] = "REVIEW_GUIDE_NOT_WORLD_GEOMETRY"
    guide.data.materials.append(material("SYLVA_L1_MAT_ScaleGuide", (0.16, 0.26, 0.21), 0.2, 0.4, (0.08, 0.35, 0.18), 1.5))

    # Unknown celestial features remain metadata empties, intentionally not dimensioned/rendered.
    add_empty(
        "SYLVA_L0_UNKNOWN_SEMILLA",
        (0, 0, 0),
        {
            "classification": "CANON_NAME_UNKNOWN_DIMENSIONS",
            "canonical_name": "Semilla",
            "radius": "UNKNOWN",
            "orbit": "UNKNOWN",
            "visible_geometry_created": False,
        },
        meta_col,
        display="CIRCLE",
        size=18,
    )
    add_empty(
        "SYLVA_L0_UNKNOWN_POLLINATOR_SWARM",
        (0, 0, 0),
        {
            "classification": "CANON_EXISTENCE_UNKNOWN_CONFIGURATION",
            "canonical_description": "enjambre polinizador orbital",
            "orbit": "UNKNOWN",
            "visible_geometry_created": False,
        },
        meta_col,
        display="CIRCLE",
        size=22,
    )

    # Portable lighting only.
    bpy.ops.object.light_add(type="SUN", location=(DISPLAY_RADIUS_M * 2.0, -DISPLAY_RADIUS_M, DISPLAY_RADIUS_M * 1.5))
    sun = bpy.context.object
    sun.name = "SYLVA_L1_LIGHT_DendraDiagnostic"
    sun.data.energy = 3.0
    sun.data.angle = math.radians(1.2)
    sun.rotation_euler = (math.radians(48), math.radians(-18), math.radians(32))
    move_to(sun, review_col)
    sun["classification"] = "DIAGNOSTIC_LIGHT_NOT_STELLAR_ORBIT_MODEL"

    bpy.ops.object.light_add(type="POINT", location=(-DISPLAY_RADIUS_M * 1.8, DISPLAY_RADIUS_M * 0.7, DISPLAY_RADIUS_M * 0.4))
    fill = bpy.context.object
    fill.name = "SYLVA_L1_LIGHT_LimbFill"
    fill.data.energy = 85000
    fill.data.color = (0.08, 0.20, 0.13)
    fill.data.shadow_soft_size = DISPLAY_RADIUS_M * 0.15
    move_to(fill, review_col)
    fill["classification"] = "DIAGNOSTIC_LIGHT"

    bpy.ops.object.camera_add(location=(DISPLAY_RADIUS_M * 2.65, -DISPLAY_RADIUS_M * 2.45, DISPLAY_RADIUS_M * 1.75))
    camera = bpy.context.object
    camera.name = "SYLVA_L1_CAM_OrbitalReview"
    camera.data.lens = 62
    camera.data.clip_start = 0.5
    camera.data.clip_end = DISPLAY_RADIUS_M * 15
    move_to(camera, review_col)
    look_at(camera)
    scene.camera = camera

    scene.view_settings.look = "Medium High Contrast"
    scene.view_settings.exposure = -0.4

    physical["visible_proxy_object"] = planet.name
    physical["visible_proxy_radius_m"] = DISPLAY_RADIUS_M

    bpy.ops.object.select_all(action="DESELECT")
    return {
        "classification": CLASSIFICATION,
        "canonicalized": False,
        "physical_radius_m_proposal": PHYSICAL_RADIUS_M,
        "display_radius_m": DISPLAY_RADIUS_M,
        "representation_scale": REPRESENTATION_SCALE,
        "visible_meshes": len([o for o in bpy.data.objects if o.type == "MESH"]),
        "objects": len(bpy.data.objects),
        "unknown_features_preserved": ["continents", "atmosphere thickness", "axial tilt", "Semilla orbit"],
    }


if __name__ == "__main__":
    print(build())
