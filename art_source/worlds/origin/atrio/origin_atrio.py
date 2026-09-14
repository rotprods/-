import bpy, math
from mathutils import Vector

# EXOVANT 2950 — ORIGIN / Atrio de las Rutas
# Claim: CLM-ORIGIN-MEGA-ATRIO-001
# Blender 5.2 LTS. Metric scene. Final values reproduce remote revision 2 blockout.

CLAIM = "CLM-ORIGIN-MEGA-ATRIO-001"
WORLD_CLAIM = "CLM-ORIGIN-WORLD-001"
WORLD = "ORIGIN"
RING_Z = 4.0
RING_THICKNESS = 0.90
RINGS = [
    ("A70", 35.0, 5.0, "ORG_ATR_RING_A70"),
    ("B48", 24.0, 5.0, "ORG_ATR_RING_B52"),
    ("C26", 13.0, 5.0, "ORG_ATR_RING_C34"),
]
SECTOR_SPAN = math.radians(108.0)
SECTOR_CENTERS = [0.0, math.radians(120), math.radians(240)]
BRIDGE_ANGLES = [0.0, math.radians(120), math.radians(240)]
BRIDGE_IDS = ["ORG_ATR_BRIDGE_RADIAL_A", "ORG_ATR_BRIDGE_RADIAL_B", "ORG_ATR_BRIDGE_RADIAL_C"]

scene = bpy.context.scene
for o in list(bpy.data.objects):
    bpy.data.objects.remove(o, do_unlink=True)
for c in list(bpy.data.collections):
    if c.name != scene.collection.name:
        bpy.data.collections.remove(c)
scene.unit_settings.system = "METRIC"
scene.unit_settings.scale_length = 1.0
scene.render.engine = "BLENDER_EEVEE"
scene.render.resolution_x = 1200
scene.render.resolution_y = 800
scene.render.resolution_percentage = 100
scene.render.image_settings.media_type = "IMAGE"
scene.render.image_settings.file_format = "PNG"
scene.render.fps = 24
scene.frame_start = 1
scene.frame_end = 1
scene.view_settings.view_transform = "Khronos PBR Neutral"
if not scene.world:
    scene.world = bpy.data.worlds.new("ORIGIN Atrio Preview World")
scene.world.use_nodes = True
bg = scene.world.node_tree.nodes.get("Background")
bg.inputs["Color"].default_value = (0.008, 0.011, 0.014, 1)
bg.inputs["Strength"].default_value = 0.20

COL = {}
for name in [
    "00_GUIDES", "01_BLACK_MINERAL_STRUCTURE", "02_RING_DECKS",
    "03_LIVING_BRONZE_JOINTS", "04_ROUTE_NODES", "05_COLLISION_PROXIES",
    "90_PREVIEW_RIG",
]:
    c = bpy.data.collections.new(name)
    scene.collection.children.link(c)
    COL[name] = c


def move(o, col):
    for cc in list(o.users_collection):
        cc.objects.unlink(o)
    COL[col].objects.link(o)


def mat(name, color, metal=0.0, rough=0.6, emission=None):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    p = m.node_tree.nodes.get("Principled BSDF")
    p.inputs["Base Color"].default_value = (*color, 1)
    p.inputs["Metallic"].default_value = metal
    p.inputs["Roughness"].default_value = rough
    if emission:
        p.inputs["Emission Color"].default_value = (*emission[0], 1)
        p.inputs["Emission Strength"].default_value = emission[1]
    m.diffuse_color = (*color, 1)
    return m


BLACK = mat("ORG_MAT_BlackMineral_Load", (0.018, 0.024, 0.029), 0.28, 0.74)
BLACK_EDGE = mat("ORG_MAT_BlackMineral_Cut", (0.044, 0.050, 0.053), 0.20, 0.62)
BRONZE = mat("ORG_MAT_LivingBronze_Joint", (0.29, 0.145, 0.045), 0.78, 0.34)
BRONZE_DARK = mat("ORG_MAT_LivingBronze_Deep", (0.12, 0.055, 0.022), 0.72, 0.46)
ROUTE = mat("ORG_MAT_RouteSurface", (0.105, 0.115, 0.115), 0.18, 0.67)
SAFE = mat("ORG_MAT_SafeNode", (0.17, 0.205, 0.18), 0.15, 0.56)
AMBER = mat("ORG_MAT_SignalAmber", (0.70, 0.25, 0.035), 0.12, 0.30, ((0.90, 0.24, 0.02), 1.0))
COLMAT = mat("PREVIEW_MAT_Collision", (0.34, 0.045, 0.035), 0.0, 0.88)
GUIDE = mat("PREVIEW_MAT_Guide", (0.62, 0.68, 0.68), 0.0, 0.55)
FLOOR = mat("PREVIEW_MAT_Floor", (0.026, 0.031, 0.035), 0.05, 0.88)


def tag(o, asset_id, role, status="BLOCKOUT_V2"):
    o["world_id"] = WORLD
    o["world_owner_claim"] = WORLD_CLAIM
    o["atomic_claim"] = CLAIM
    o["claim_id"] = CLAIM
    o["asset_id"] = asset_id
    o["role"] = role
    o["status"] = status
    o["metre_scale"] = 1.0
    return o


def bevel(o, width=0.06, segments=2):
    b = o.modifiers.new("Physical edge radius", "BEVEL")
    b.width = width
    b.segments = segments


def cube(name, loc, dims, material, col, rot_z=0.0, asset_id=None, role="structure", edge=0.04):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=(0, 0, rot_z))
    o = bpy.context.object
    o.name = name
    o.scale = dims
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    move(o, col)
    o.data.materials.append(material)
    if edge:
        bevel(o, edge, 3)
    return tag(o, asset_id or name, role)


def cylinder(name, loc, radius, depth, material, col, verts=48, asset_id=None, role="structure", render=True):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=radius, depth=depth, location=loc)
    o = bpy.context.object
    o.name = name
    move(o, col)
    o.data.materials.append(material)
    for p in o.data.polygons:
        p.use_smooth = True
    bevel(o, min(0.08, depth * 0.08), 2)
    tag(o, asset_id or name, role)
    if not render:
        o.hide_render = True
        o.display_type = "WIRE"
    return o


def annular_sector(name, radius, width, a0, a1, z, thickness, material, col, segments=72, asset_id=None, role="ring_deck"):
    ro, ri = radius + width / 2, radius - width / 2
    verts, faces = [], []
    for i in range(segments + 1):
        a = a0 + (a1 - a0) * i / segments
        ca, sa = math.cos(a), math.sin(a)
        verts += [
            (ri * ca, ri * sa, z - thickness / 2),
            (ro * ca, ro * sa, z - thickness / 2),
            (ri * ca, ri * sa, z + thickness / 2),
            (ro * ca, ro * sa, z + thickness / 2),
        ]
    for i in range(segments):
        j, k = 4 * i, 4 * (i + 1)
        faces += [
            (j, j + 1, k + 1, k), (j + 2, k + 2, k + 3, j + 3),
            (j, j + 2, j + 3, j + 1), (j + 1, j + 3, k + 3, k + 1),
        ]
    faces += [(0, 4 * segments, 4 * segments + 2, 2), (1, 3, 4 * segments + 3, 4 * segments + 1)]
    me = bpy.data.meshes.new(name + "_MESH")
    me.from_pydata(verts, [], faces)
    me.update()
    o = bpy.data.objects.new(name, me)
    COL[col].objects.link(o)
    me.materials.append(material)
    bevel(o, 0.10 if role == "ring_deck" else 0.05, 3)
    tag(o, asset_id or name, role)
    o["radius_m"] = radius
    o["width_m"] = width
    o["sector_deg"] = round(math.degrees(a1 - a0), 3)
    return o


def polar(r, a, z=0.0):
    return Vector((r * math.cos(a), r * math.sin(a), z))


def tangent_angle(a):
    return a + math.pi / 2


def collision_sector(name, radius, width, a0, a1, z, thickness, asset_id):
    o = annular_sector(name, radius, width * 0.92, a0, a1, z, thickness * 0.72, COLMAT, "05_COLLISION_PROXIES", 18, asset_id, "collision_proxy")
    o.hide_render = True
    o.display_type = "WIRE"
    o["collision_policy"] = "custom_low_poly_sector"
    return o


def collision_box(name, loc, dims, rot_z, asset_id):
    o = cube(name, loc, dims, COLMAT, "05_COLLISION_PROXIES", rot_z, asset_id, "collision_proxy", 0)
    o.hide_render = True
    o.display_type = "WIRE"
    o["collision_policy"] = "box_proxy"
    return o


# Preview datum.
bpy.ops.mesh.primitive_cylinder_add(vertices=96, radius=41.0, depth=0.45, location=(0, 0, 0))
floor = bpy.context.object
floor.name = "PREVIEW_AtrioDatum"
move(floor, "90_PREVIEW_RIG")
floor.data.materials.append(FLOOR)
tag(floor, "PREVIEW_DATUM", "preview", "PREVIEW_ONLY")
bevel(floor, 0.18, 3)

# Three canonical connected rings; 12-degree gaps are intentional route apertures between 108-degree sectors.
for code, r, w, asset in RINGS:
    for si, center in enumerate(SECTOR_CENTERS):
        a0, a1 = center - SECTOR_SPAN / 2, center + SECTOR_SPAN / 2
        nm = f"{asset}_SEG_{si:02d}"
        annular_sector(nm, r, w, a0, a1, RING_Z, RING_THICKNESS, ROUTE, "02_RING_DECKS", 64, asset, "ring_deck")
        collision_sector("COL_" + nm, r, w, a0, a1, RING_Z, RING_THICKNESS, asset)
        annular_sector(nm + "_LOADBAND", r, w * 0.72, a0 + 0.018, a1 - 0.018, RING_Z - 0.62, 0.62, BLACK, "01_BLACK_MINERAL_STRUCTURE", 48, asset, "load_band")
        for end_i, a in enumerate((a0, a1)):
            loc = polar(r, a, RING_Z + 0.52)
            joint = cube(f"{nm}_BRONZE_END_{end_i}", tuple(loc), (w * 0.78, 1.10, 0.34), BRONZE, "03_LIVING_BRONZE_JOINTS", tangent_angle(a), asset, "living_joint", 0.09)
            joint["joint_function"] = "sector_end_load_transfer_and_signal"

# Load-bearing piers contact the datum and overlap the ring underside.
for code, r, w, asset in RINGS:
    for pi, a in enumerate(SECTOR_CENTERS):
        loc = polar(r, a, 2.01)  # 0.015 m penetration into 0.225 m datum top.
        pier = cube(f"ORG_ATR_SUPPORT_PIER_{code}_{pi:02d}", tuple(loc), (2.2, 3.0, 3.6), BLACK, "01_BLACK_MINERAL_STRUCTURE", tangent_angle(a), "ORG_ATR_SUPPORT_PIER", "support_pier", 0.16)
        pier["supported_asset"] = asset
        bearing = cube(f"ORG_ATR_SUPPORT_BEARING_{code}_{pi:02d}", tuple(polar(r, a, 3.46)), (3.2, 3.7, 0.32), BRONZE_DARK, "03_LIVING_BRONZE_JOINTS", tangent_angle(a), "ORG_ATR_SUPPORT_PIER", "bearing_joint", 0.08)
    if code == "A70":
        for pi, a in enumerate([math.radians(40), math.radians(160), math.radians(280)]):
            cube(f"ORG_ATR_SUPPORT_PIER_AUX_{pi:02d}", tuple(polar(r, a, 1.88)), (1.65, 2.3, 3.35), BLACK_EDGE, "01_BLACK_MINERAL_STRUCTURE", tangent_angle(a), "ORG_ATR_SUPPORT_PIER", "secondary_support", 0.12)

# Radial bridges at 0/120/240 degrees.
for a, asset in zip(BRIDGE_ANGLES, BRIDGE_IDS):
    for r0, r1, part in [(15.5, 21.5, "INNER"), (26.5, 32.5, "OUTER")]:
        rm, length = (r0 + r1) / 2, r1 - r0
        o = cube(f"{asset}_{part}", tuple(polar(rm, a, RING_Z)), (length, 4.5, 0.75), ROUTE, "02_RING_DECKS", a, asset, "radial_bridge", 0.09)
        o["bridge_part"] = part
        o["clear_width_m"] = 4.5
        o["proposal_dimension"] = True
        collision_box("COL_" + o.name, tuple(polar(rm, a, RING_Z)), (length, 4.1, 0.55), a, asset)
        cube(o.name + "_LOADSPINE", tuple(polar(rm, a, RING_Z - 0.60)), (length, 2.0, 0.62), BLACK, "01_BLACK_MINERAL_STRUCTURE", a, asset, "bridge_load_spine", 0.08)
    for ji, r in enumerate([15.5, 21.5, 26.5, 32.5]):
        j = cube(f"{asset}_JOINT_{ji:02d}", tuple(polar(r, a, RING_Z + 0.56)), (1.35, 5.25, 0.38), BRONZE, "03_LIVING_BRONZE_JOINTS", a, asset, "bridge_joint", 0.12)
        j["joint_function"] = "bridge_to_ring_adaptive_bearing"

# Safe node.
safe_center = polar(24.0, 0, RING_Z)
safe = cylinder("ORG_ATR_NODE_SAFE", tuple(safe_center), 4.0, 0.96, SAFE, "04_ROUTE_NODES", 64, "ORG_ATR_NODE_SAFE", "safe_node")
safe["clear_zone_radius_m"] = 3.25
safe["proposal_dimension"] = True
cylinder("COL_ORG_ATR_NODE_SAFE", tuple(safe_center), 3.72, 0.58, COLMAT, "05_COLLISION_PROXIES", 12, "ORG_ATR_NODE_SAFE", "collision_proxy", False)["collision_policy"] = "low_poly_cylinder_inside_visual_boundary"
cylinder("ORG_ATR_NODE_SAFE_UNDERBODY", tuple(safe_center + Vector((0, 0, -0.58))), 3.55, 0.48, BLACK, "01_BLACK_MINERAL_STRUCTURE", 48, "ORG_ATR_NODE_SAFE", "safe_node_load")
for i in range(3):
    a = i * math.tau / 3
    loc = safe_center + Vector((2.75 * math.cos(a), 2.75 * math.sin(a), 0.57))
    cube(f"ORG_ATR_NODE_SAFE_SIGNAL_{i}", tuple(loc), (0.65, 0.12, 0.06), AMBER, "04_ROUTE_NODES", a, "ORG_ATR_NODE_SAFE", "signal_cut", 0.02)

# Valve node.
valve_center = polar(24.0, math.radians(120), RING_Z)
cylinder("ORG_ATR_NODE_VALVE", tuple(valve_center), 4.0, 0.96, ROUTE, "04_ROUTE_NODES", 64, "ORG_ATR_NODE_VALVE", "valve_node")
cylinder("COL_ORG_ATR_NODE_VALVE", tuple(valve_center), 3.72, 0.58, COLMAT, "05_COLLISION_PROXIES", 12, "ORG_ATR_NODE_VALVE", "collision_proxy", False)["collision_policy"] = "low_poly_cylinder_inside_visual_boundary"
cylinder("ORG_ATR_NODE_VALVE_BEARING", tuple(valve_center + Vector((0, 0, 0.72))), 2.05, 0.48, BRONZE, "03_LIVING_BRONZE_JOINTS", 48, "ORG_ATR_NODE_VALVE", "valve_bearing")
cylinder("ORG_ATR_NODE_VALVE_CORE", tuple(valve_center + Vector((0, 0, 1.15))), 0.78, 1.20, BRONZE_DARK, "03_LIVING_BRONZE_JOINTS", 32, "ORG_ATR_NODE_VALVE", "valve_core")
for i in range(6):
    a = math.tau * i / 6
    loc = valve_center + Vector((1.42 * math.cos(a), 1.42 * math.sin(a), 1.15))
    cube(f"ORG_ATR_NODE_VALVE_RIB_{i:02d}", tuple(loc), (1.15, 0.28, 0.28), BRONZE, "03_LIVING_BRONZE_JOINTS", a, "ORG_ATR_NODE_VALVE", "valve_rib", 0.06)

# Route aperture: 4 m-class clear passage at outer gap around 60 degrees.
ap_a = math.radians(60)
ap_center = polar(35, ap_a, RING_Z)
tangent = Vector((-math.sin(ap_a), math.cos(ap_a), 0))
for side in [-1, 1]:
    loc = ap_center + tangent * (side * 3.0) + Vector((0, 0, 2.55))
    cube(f"ORG_ATR_ROUTE_APERTURE_PYLON_{side:+d}", tuple(loc), (1.05, 1.55, 5.1), BLACK, "01_BLACK_MINERAL_STRUCTURE", ap_a, "ORG_ATR_ROUTE_APERTURE", "route_aperture_pylon", 0.14)
    cube(f"ORG_ATR_ROUTE_APERTURE_COLLAR_{side:+d}", tuple(loc + Vector((0, 0, 1.7))), (1.28, 1.85, 0.55), BRONZE, "03_LIVING_BRONZE_JOINTS", ap_a, "ORG_ATR_ROUTE_APERTURE", "aperture_joint", 0.10)
    collision_box(f"COL_ORG_ATR_ROUTE_APERTURE_PYLON_{side:+d}", tuple(loc), (0.95, 1.40, 5.0), ap_a, "ORG_ATR_ROUTE_APERTURE")
cube("ORG_ATR_ROUTE_APERTURE_LINTEL", tuple(ap_center + Vector((0, 0, 5.15))), (7.2, 1.45, 0.80), BLACK_EDGE, "01_BLACK_MINERAL_STRUCTURE", tangent_angle(ap_a), "ORG_ATR_ROUTE_APERTURE", "route_aperture_lintel", 0.16)

# Explicit exclusion marker for future boss/negotiation-center claim.
bpy.ops.object.empty_add(type="CIRCLE", radius=7.5, location=(0, 0, RING_Z + 0.1))
ex = bpy.context.object
ex.name = "GUIDE_EXCLUDED_EXOVANT_HEART_CORE"
move(ex, "00_GUIDES")
ex["excluded_from_claim"] = True
ex["reason"] = "final boss / negotiation center owned by future atomic claim"

# Player capsule reference: current Godot prototype 1.85 m / radius .38 m.
player_base = polar(34.2, math.radians(-18), RING_Z + RING_THICKNESS / 2)
body_h = 1.09
bpy.ops.mesh.primitive_cylinder_add(vertices=20, radius=0.38, depth=body_h, location=tuple(player_base + Vector((0, 0, 0.38 + body_h / 2))))
pb = bpy.context.object
pb.name = "GUIDE_PlayerCapsule_Body"
move(pb, "00_GUIDES")
pb.data.materials.append(GUIDE)
tag(pb, "GUIDE_PLAYER_1P85", "scale_reference", "GUIDE")
pb["source"] = "scripts/player.gd"
pb["height_m"] = 1.85
pb["radius_m"] = 0.38
for nm, z in [("Bottom", 0.38), ("Top", 0.38 + body_h)]:
    bpy.ops.mesh.primitive_uv_sphere_add(segments=20, ring_count=12, radius=0.38, location=tuple(player_base + Vector((0, 0, z))))
    s = bpy.context.object
    s.name = "GUIDE_PlayerCapsule_" + nm
    move(s, "00_GUIDES")
    s.data.materials.append(GUIDE)
    tag(s, "GUIDE_PLAYER_1P85", "scale_reference", "GUIDE")

# Bounded prior-world material echoes — no imported source geometry.
for label, color, a in [
    ("TERRA", (0.44, 0.40, 0.31), math.radians(15)),
    ("NACRE", (0.42, 0.46, 0.49), math.radians(135)),
    ("VANTA", (0.24, 0.25, 0.26), math.radians(255)),
]:
    echo_mat = mat("ORG_MAT_Echo_" + label, color, 0.25, 0.58)
    o = cube("ORG_ATR_ECHO_INSERT_" + label, tuple(polar(30.0, a, RING_Z + 0.54)), (2.4, 0.65, 0.16), echo_mat, "04_ROUTE_NODES", tangent_angle(a), "ORG_ATR_ECHO_INSERTS", "prior_world_echo", 0.04)
    o["source_world_reference"] = label
    o["ownership_note"] = "material echo only; not source asset ownership"

# Delivery camera and motivated preview lights.
bpy.ops.object.camera_add(location=(78.75, -91.25, 71.25))
cam = bpy.context.object
cam.name = "CAM_Delivery_ORIGIN_Atrio"
move(cam, "90_PREVIEW_RIG")
cam.data.lens = 45
scene.camera = cam

def look_at(obj, target):
    d = Vector(target) - obj.location
    obj.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
look_at(cam, (0, 0, 3.0))

bpy.ops.object.light_add(type="SUN", location=(0, 0, 45))
sun = bpy.context.object
sun.name = "PREVIEW_Sun"
move(sun, "90_PREVIEW_RIG")
sun.data.energy = 2.1
sun.rotation_euler = (math.radians(34), math.radians(-22), math.radians(26))
for name, loc, energy, color, size in [
    ("PREVIEW_Key", (-38, -48, 34), 1800, (1.0, .72, .45), 10.0),
    ("PREVIEW_Fill", (45, -5, 24), 1200, (.36, .58, 1.0), 12.0),
    ("PREVIEW_Rim", (0, 52, 30), 1450, (.58, .82, 1.0), 9.0),
]:
    bpy.ops.object.light_add(type="POINT", location=loc)
    l = bpy.context.object
    l.name = name
    move(l, "90_PREVIEW_RIG")
    l.data.energy = energy
    l.data.color = color
    l.data.shadow_soft_size = size

print("ORIGIN Atrio blockout generated", len(bpy.data.objects), "objects")
