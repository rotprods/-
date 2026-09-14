"""SYLVA PRIME macro foundation generator.

Scope: CLM-SYLVA-MACRO-001
Target: Blender 5.2 LTS / metric scene
Status: blockout/proxy generator, not final art.

Planet radius/diameter are deliberately NOT authored here because current canon does not define them.
The 12 km local authored patch is a reversible production proposal, not planetary canon.
"""
from __future__ import annotations

import bpy
import math
from mathutils import Vector

PREFIX = "SYLVA_"
LOCAL_ENVELOPE_M = 12_000.0  # PROPOSAL
PLANET_RADIUS = None          # BLOCKED / UNKNOWN

PUERTO = Vector((-3200.0, -2200.0, 330.0))
BOSQUE = Vector((0.0, 150.0, 350.0))
VESPER = Vector((3200.0, 2300.0, -220.0))


def _move(obj, col):
    for c in list(obj.users_collection):
        c.objects.unlink(obj)
    col.objects.link(obj)


def _mat(name, base, metallic=0.0, rough=0.7, emission=None, strength=0.0):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*base, 1.0)
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = rough
    if emission:
        key = "Emission Color" if "Emission Color" in bsdf.inputs else "Emission"
        bsdf.inputs[key].default_value = (*emission, 1.0)
        if "Emission Strength" in bsdf.inputs:
            bsdf.inputs["Emission Strength"].default_value = strength
    return m


def _assign(obj, material):
    if hasattr(obj.data, "materials") and len(obj.data.materials) == 0:
        obj.data.materials.append(material)


def _cube(name, loc, scale, material, col, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(location=loc, rotation=rot)
    obj = bpy.context.object
    obj.name = name
    obj.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    _assign(obj, material)
    _move(obj, col)
    return obj


def _cyl(name, loc, radius, depth, material, col, vertices=16, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=vertices, radius=radius, depth=depth, location=loc, rotation=rot
    )
    obj = bpy.context.object
    obj.name = name
    _assign(obj, material)
    _move(obj, col)
    return obj


def _sphere(name, loc, scale, material, col):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, location=loc)
    obj = bpy.context.object
    obj.name = name
    obj.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    _assign(obj, material)
    _move(obj, col)
    return obj


def _torus(name, loc, major, minor, material, col, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_torus_add(
        major_radius=major,
        minor_radius=minor,
        major_segments=32,
        minor_segments=8,
        location=loc,
        rotation=rot,
    )
    obj = bpy.context.object
    obj.name = name
    _assign(obj, material)
    _move(obj, col)
    return obj


def _pipe(name, a, b, radius, material, col, vertices=12):
    a, b = Vector(a), Vector(b)
    delta = b - a
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=vertices,
        radius=radius,
        depth=delta.length,
        location=(a + b) * 0.5,
    )
    obj = bpy.context.object
    obj.name = name
    obj.rotation_mode = "QUATERNION"
    obj.rotation_quaternion = delta.to_track_quat("Z", "Y")
    _assign(obj, material)
    _move(obj, col)
    return obj


def _curve_root(name, points, radius, material, col):
    curve = bpy.data.curves.new(name + "_Curve", "CURVE")
    curve.dimensions = "3D"
    curve.resolution_u = 2
    curve.bevel_depth = radius
    curve.bevel_resolution = 2
    spline = curve.splines.new("BEZIER")
    spline.bezier_points.add(len(points) - 1)
    for bp, point in zip(spline.bezier_points, points):
        bp.co = point
        bp.handle_left_type = "AUTO"
        bp.handle_right_type = "AUTO"
    obj = bpy.data.objects.new(name, curve)
    col.objects.link(obj)
    _assign(obj, material)
    return obj


def _empty(name, loc, props, col, size=30):
    obj = bpy.data.objects.new(name, None)
    obj.location = loc
    obj.empty_display_type = "SPHERE"
    obj.empty_display_size = size
    col.objects.link(obj)
    for key, value in props.items():
        obj[key] = value
    return obj


def _human(name, loc, col, material):
    _cyl(name + "_Torso", (loc[0], loc[1], loc[2] + 1.05), 0.23, 0.82, material, col, 12)
    _sphere(name + "_Head", (loc[0], loc[1], loc[2] + 1.68), (0.16, 0.16, 0.19), material, col)


def _look_at(obj, target):
    obj.rotation_euler = (Vector(target) - obj.location).to_track_quat("-Z", "Y").to_euler()


def build():
    scene = bpy.context.scene
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 1.0
    if scene.world is None:
        scene.world = bpy.data.worlds.new("SYLVA_World")
    scene.world.color = (0.006, 0.012, 0.009)
    scene.render.engine = "BLENDER_EEVEE"
    scene.render.resolution_x = 1280
    scene.render.resolution_y = 720
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.film_transparent = False
    scene.view_settings.look = "Medium High Contrast"
    scene.view_settings.exposure = -0.6

    names = [
        "00_META", "10_TERRAIN", "20_ROOT_NETWORK", "30_PUERTO_INJERTO",
        "40_BOSQUE_FRASES", "50_CAMARA_VESPER", "60_SCALE_TRAVERSAL",
        "70_LOOKDEV", "80_LIGHTS_CAM"
    ]
    cols = {}
    for name in names:
        c = bpy.data.collections.get(PREFIX + name) or bpy.data.collections.new(PREFIX + name)
        if c.name not in scene.collection.children:
            scene.collection.children.link(c)
        cols[name] = c

    soil = _mat("SYLVA_DIAG_Soil", (0.018, 0.035, 0.022), rough=0.96)
    root = _mat("SYLVA_DIAG_RootFiber", (0.055, 0.095, 0.045), rough=0.86)
    root2 = _mat("SYLVA_DIAG_YoungRoot", (0.11, 0.17, 0.075), rough=0.74)
    membrane = _mat("SYLVA_DIAG_Membrane", (0.34, 0.42, 0.30), rough=0.58)
    graft = _mat("SYLVA_DIAG_GraftHardware", (0.055, 0.062, 0.060), metallic=0.72, rough=0.34)
    cyan = _mat("SYLVA_DIAG_MemorySignal", (0.02, 0.09, 0.10), metallic=0.18, rough=0.38, emission=(0.03, 0.70, 0.82), strength=3.2)
    amber = _mat("SYLVA_DIAG_RefugeSignal", (0.12, 0.06, 0.012), metallic=0.15, rough=0.42, emission=(1.0, 0.30, 0.025), strength=3.4)
    human_mat = _mat("SYLVA_DIAG_HumanScale", (0.52, 0.52, 0.50), metallic=0.15, rough=0.55)

    meta = _empty(
        "SYLVA_WORLD_ROOT", (0, 0, 0),
        {
            "claim_id": "CLM-SYLVA-MACRO-001",
            "world_id": "sylva",
            "world_name": "SYLVA PRIME",
            "classification_planet_radius": "BLOCKED_UNKNOWN",
            "planet_radius_m": "UNKNOWN",
            "classification_local_envelope": "PROPOSAL",
            "local_envelope_m": LOCAL_ENVELOPE_M,
            "units": "metres",
            "gravity_g_documented": 1.12,
            "temperature_c_documented": 34.0,
            "regions_canon": "Puerto del Injerto | Bosque de las Frases | Camara de VESPER",
            "build_status": "WAVE1_MACRO_BLOCKOUT_R3",
        }, cols["00_META"], 50,
    )

    # Low-frequency 12 km working terrain.
    n = 49
    size = LOCAL_ENVELOPE_M
    verts, faces = [], []
    for iy in range(n):
        y = -size / 2 + size * iy / (n - 1)
        for ix in range(n):
            x = -size / 2 + size * ix / (n - 1)
            broad = 180 * math.sin(x / 1500) + 120 * math.cos(y / 1250) + 55 * math.sin((x - y) / 700)
            puerto_mound = 160 * math.exp(-(((x + 3200) / 1300) ** 2 + ((y + 2200) / 1200) ** 2))
            bosque_rise = 240 * math.exp(-(((x - 150) / 2000) ** 2 + ((y - 150) / 1700) ** 2))
            vesper_sink = -460 * math.exp(-(((x - 3200) / 1050) ** 2 + ((y - 2300) / 1000) ** 2))
            verts.append((x, y, broad + puerto_mound + bosque_rise + vesper_sink))
    for iy in range(n - 1):
        for ix in range(n - 1):
            a = iy * n + ix
            faces.append((a, a + 1, a + 1 + n, a + n))
    mesh = bpy.data.meshes.new("SYLVA_Terrain12km_Mesh")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    terrain = bpy.data.objects.new("SYLVA_TERRAIN_Macro12km_PROPOSAL", mesh)
    cols["10_TERRAIN"].objects.link(terrain)
    _assign(terrain, soil)
    terrain["classification"] = "PROPOSAL"
    terrain["extent_m"] = size

    _empty("SYLVA_REGION_PuertoDelInjerto", PUERTO, {"canon": True}, cols["00_META"], 80)
    _empty("SYLVA_REGION_BosqueDeLasFrases", BOSQUE, {"canon": True}, cols["00_META"], 80)
    _empty("SYLVA_REGION_CamaraVESPER", VESPER, {"canon": True}, cols["00_META"], 80)

    primary = [
        ("R01", [(-5000,-3500,180),(-4100,-2800,440),PUERTO,(-2200,-1200,520),(-1100,-300,420)], 48),
        ("R02", [(-1200,-500,400),(-700,150,560),BOSQUE,(900,700,560),(1800,1350,400)], 62),
        ("R03", [(1700,1200,390),(2350,1700,280),VESPER,(3900,2800,-20),(4800,3300,170)], 72),
        ("R04", [(-3900,-500,150),(-2500,200,310),(-900,800,450),(700,1200,380),(2300,1800,150)], 36),
        ("R05", [(-1700,-3600,80),(-800,-2200,230),(200,-900,300),(900,200,360),(1450,1300,260)], 30),
        ("R06", [(3600,-800,120),(2800,200,250),(2100,900,330),(1800,1600,250),(2500,2200,-60)], 40),
    ]
    for name, pts, radius in primary:
        obj = _curve_root("SYLVA_ROOT_PRIMARY_" + name, pts, radius, root, cols["20_ROOT_NETWORK"])
        obj["hierarchy"] = "PRIMARY"
        obj["radius_m"] = radius

    secondary = [
        ((-3150,-2150,390),(-3550,-1550,560)),((-3000,-2050,380),(-2550,-2650,500)),
        ((-350,100,480),(-850,1050,620)),((200,200,470),(750,1050,650)),
        ((650,750,520),(1150,1450,430)),((2850,2100,30),(2450,2850,260)),
        ((3350,2250,-80),(3800,1700,190)),((3600,2450,-40),(4200,3100,240)),
    ]
    for i, (a, b) in enumerate(secondary):
        _pipe(f"SYLVA_ROOT_SECONDARY_{i:02d}", a, b, 18 if i < 5 else 22, root2, cols["20_ROOT_NETWORK"])

    # Puerto del Injerto macro language.
    _empty("SYLVA_POI_PuertoDelInjerto", PUERTO, {"status": "BLOCKOUT"}, cols["30_PUERTO_INJERTO"], 40)
    _curve_root("SYLVA_PUERTO_LivingArch_A", [(-3500,-2350,330),(-3400,-2250,520),(-3200,-2200,690),(-3000,-2150,520),(-2900,-2050,330)], 26, root, cols["30_PUERTO_INJERTO"])
    _curve_root("SYLVA_PUERTO_LivingArch_B", [(-3450,-2000,340),(-3350,-1900,500),(-3150,-1850,620),(-2950,-1950,500),(-2900,-2100,340)], 20, root2, cols["30_PUERTO_INJERTO"])
    _cube("SYLVA_PUERTO_ProxyDeck", (-3200,-2200,360), (150,95,8), graft, cols["30_PUERTO_INJERTO"])
    for ix in range(-2, 3):
        x = -3200 + ix * 50
        for side in (-1, 1):
            y = -2200 + side * 82
            _pipe(f"SYLVA_PUERTO_ScaffoldPost_{ix}_{side}", (x,y,368), (x,y,448), 2.2, graft, cols["30_PUERTO_INJERTO"])
        _pipe(f"SYLVA_PUERTO_ScaffoldBeam_{ix}", (x,-2282,448), (x,-2118,448), 2.0, graft, cols["30_PUERTO_INJERTO"])
    for i in range(3):
        _torus(f"SYLVA_PUERTO_GraftClamp_{i}", (-3300+i*100,-2290,390), 12, 2.4, amber, cols["30_PUERTO_INJERTO"], (math.radians(90),0,0))
    _human("SYLVA_SCALE_Human_Puerto", (-3180,-2180,369), cols["60_SCALE_TRAVERSAL"], human_mat)

    # Bosque de las Frases: three geometrically distinct routes.
    _empty("SYLVA_POI_BosqueDeLasFrases", BOSQUE, {"status":"BLOCKOUT","route_count":3}, cols["40_BOSQUE_FRASES"], 40)
    for ridx, angle in enumerate((-0.75, 0.05, 0.8)):
        sx, sy = BOSQUE.x, BOSQUE.y
        ex, ey = sx + math.cos(angle)*1650, sy + math.sin(angle)*1650
        z0, ze = BOSQUE.z, 300 + 80*ridx
        dx, dy = -math.sin(angle)*42, math.cos(angle)*42
        _pipe(f"SYLVA_BOSQUE_Route{ridx}_RootL", (sx+dx,sy+dy,z0), (ex+dx,ey+dy,ze), 13, root, cols["40_BOSQUE_FRASES"])
        _pipe(f"SYLVA_BOSQUE_Route{ridx}_RootR", (sx-dx,sy-dy,z0), (ex-dx,ey-dy,ze), 13, root, cols["40_BOSQUE_FRASES"])
        for k in range(ridx + 1):
            t = 0.32 + 0.08*k
            px, py, pz = sx+(ex-sx)*t, sy+(ey-sy)*t, z0+(ze-z0)*t
            _torus(f"SYLVA_BOSQUE_Route{ridx}_SignalArch{k}", (px,py,pz+18), 22+5*ridx, 3.5, cyan, cols["40_BOSQUE_FRASES"], (math.radians(90),0,angle))
    _cyl("SYLVA_BOSQUE_PhraseNode", (0,150,390), 46, 90, root, cols["40_BOSQUE_FRASES"], 20)
    _torus("SYLVA_BOSQUE_PhraseHalo", (0,150,465), 85, 8, membrane, cols["40_BOSQUE_FRASES"])
    _human("SYLVA_SCALE_Human_Bosque", (0,100,390), cols["60_SCALE_TRAVERSAL"], human_mat)

    # Camara de VESPER envelope only. No VESPER final model.
    _empty("SYLVA_POI_CamaraVESPER", VESPER, {"status":"BLOCKOUT_ENVELOPE","final_boss_mesh":"EXCLUDED"}, cols["50_CAMARA_VESPER"], 50)
    _cyl("SYLVA_VESPER_ProxyArenaFloor", (3200,2300,-260), 90, 8, soil, cols["50_CAMARA_VESPER"], 48)
    _torus("SYLVA_VESPER_EnvelopeRing", (3200,2300,-252), 88, 3.2, cyan, cols["50_CAMARA_VESPER"])
    for k in range(6):
        a = 2*math.pi*k/6
        outer = (3200+math.cos(a)*260, 2300+math.sin(a)*260, -80)
        inner = (3200+math.cos(a)*82, 2300+math.sin(a)*82, -245)
        _pipe(f"SYLVA_VESPER_Buttress_{k:02d}", outer, inner, 24, root, cols["50_CAMARA_VESPER"])
    for k in range(8):
        a = 2*math.pi*k/8
        radius = 260 + 45*(k%2)
        x, y = 3200+math.cos(a)*radius, 2300+math.sin(a)*radius
        h = 120 + 35*(k%3)
        _cyl(f"SYLVA_VESPER_CityRootTower_{k:02d}", (x,y,-80+h*0.5), 22+4*(k%2), h, root2, cols["50_CAMARA_VESPER"], 12)
        _sphere(f"SYLVA_VESPER_MembranePod_{k:02d}", (x,y,-80+h+22), (32,24,18), membrane, cols["50_CAMARA_VESPER"])
    _human("SYLVA_SCALE_Human_Vesper", (3200,2210,-252), cols["60_SCALE_TRAVERSAL"], human_mat)

    # Diagnostic 6 m route ribbon; not final road geometry.
    path_nodes = [PUERTO, Vector((-1800,-900,430)), BOSQUE, Vector((1650,1150,300)), VESPER]
    for i in range(len(path_nodes)-1):
        a, b = path_nodes[i], path_nodes[i+1]
        delta = b-a
        obj = _cube(f"SYLVA_TRAV_PathGuide_{i:02d}", (a+b)*0.5, (delta.length*0.5,3.0,0.35), amber, cols["60_SCALE_TRAVERSAL"])
        obj.rotation_mode = "QUATERNION"
        obj.rotation_quaternion = delta.to_track_quat("X", "Z")
        obj["diagnostic_width_m"] = 6.0
        obj["final_geometry"] = False

    # Portable lighting only (SUN / POINT / SPOT are glTF-supported).
    bpy.ops.object.light_add(type="SUN", location=(0,0,6000))
    sun = bpy.context.object; sun.name = "SYLVA_LIGHT_DendraSun"; sun.data.energy = 2.2; sun.data.angle = math.radians(4)
    sun.rotation_euler = (math.radians(42), math.radians(-18), math.radians(22)); _move(sun, cols["80_LIGHTS_CAM"])
    bpy.ops.object.light_add(type="SUN", location=(0,0,5000))
    fill = bpy.context.object; fill.name = "SYLVA_LIGHT_CanopyFillPortable"; fill.data.energy = 0.42; fill.data.angle = math.radians(8)
    fill.rotation_euler = (math.radians(120), math.radians(12), math.radians(-145)); _move(fill, cols["80_LIGHTS_CAM"])
    for i, pos in enumerate([(-3200,-2200,620),(0,150,650),(3200,2300,80)]):
        bpy.ops.object.light_add(type="POINT", location=pos)
        light = bpy.context.object; light.name = f"SYLVA_LIGHT_Bio_{i:02d}"; light.data.energy = 45000
        light.data.color = (0.03,0.55,0.70) if i else (1.0,0.28,0.02); light.data.shadow_soft_size = 40
        _move(light, cols["80_LIGHTS_CAM"])

    camera_specs = [
        ("SYLVA_CAM_MasterOverview", (9800,-11500,7600), (0,0,180), 58),
        ("SYLVA_CAM_Puerto", (-4300,-3600,1250), PUERTO+(0,0,90), 52),
        ("SYLVA_CAM_Bosque", (-1100,-1650,1250), BOSQUE+(0,0,80), 50),
        ("SYLVA_CAM_Vesper", (4400,900,850), VESPER+(0,0,100), 52),
    ]
    for name, loc, target, lens in camera_specs:
        bpy.ops.object.camera_add(location=loc)
        cam = bpy.context.object; cam.name = name; cam.data.lens = lens; cam.data.sensor_width = 36
        cam.data.clip_start = 0.5; cam.data.clip_end = 30000.0; _look_at(cam, target); _move(cam, cols["80_LIGHTS_CAM"])
    scene.camera = bpy.data.objects["SYLVA_CAM_MasterOverview"]

    bpy.ops.object.select_all(action="DESELECT")
    return meta


if __name__ == "__main__":
    build()
