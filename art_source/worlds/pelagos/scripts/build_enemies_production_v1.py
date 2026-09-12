"""PELAGOS enemy production foundations v1.

Rebuilds the three canonical Pelagos enemy families on top of the Pelagos World Master.
Blender 5.2+, metres. All dimensions/anatomy not explicitly in canon are reversible PROPOSALS.
This script creates production foundations, not final game-ready enemies.
"""
import bpy
import math
from mathutils import Vector

ROOT = "PELAGOS_WORLD"
COLLECTION = "71_ENEMIES_PRODUCTION_V1"
STATE = "ENEMY_PRODUCTION_FOUNDATION_V1"


def material(*names):
    for name in names:
        m = bpy.data.materials.get(name)
        if m:
            return m
    raise RuntimeError(f"Missing Pelagos material candidates: {names}")


def ensure_collection():
    root = bpy.data.collections.get(ROOT)
    if root is None:
        raise RuntimeError("Build Pelagos World Foundation first")
    old = bpy.data.collections.get(COLLECTION)
    if old:
        for obj in list(old.objects):
            bpy.data.objects.remove(obj, do_unlink=True)
        bpy.data.collections.remove(old)
    col = bpy.data.collections.new(COLLECTION)
    root.children.link(col)
    return col


def set_material(obj, mat):
    if hasattr(obj.data, "materials") and not obj.data.materials:
        obj.data.materials.append(mat)


def tag(obj, aid, role, collision="none", tier="A"):
    obj["asset_id"] = aid
    obj["world"] = "pelagos"
    obj["role"] = role
    obj["production_state"] = STATE
    obj["collision_intent"] = collision
    obj["quality_tier"] = tier
    return obj


def relink(obj, col):
    for old in list(obj.users_collection):
        old.objects.unlink(obj)
    col.objects.link(obj)
    return obj


def box(col, name, loc, dims, mat, aid, role, rot=(0, 0, 0), bevel=0.04, collision="simple"):
    bpy.ops.mesh.primitive_cube_add(location=loc, rotation=rot)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = dims
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if bevel:
        mod = obj.modifiers.new("ManufacturedEdge", "BEVEL")
        mod.width = bevel
        mod.segments = 2
    set_material(obj, mat)
    relink(obj, col)
    return tag(obj, aid, role, collision)


def cylinder(col, name, loc, radius, depth, mat, aid, role, vertices=20, rot=(0, 0, 0), collision="simple"):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=loc, rotation=rot)
    obj = bpy.context.object
    obj.name = name
    set_material(obj, mat)
    relink(obj, col)
    return tag(obj, aid, role, collision)


def sphere(col, name, loc, scale, mat, aid, role, collision="none"):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=20, ring_count=10, location=loc)
    obj = bpy.context.object
    obj.name = name
    obj.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    set_material(obj, mat)
    relink(obj, col)
    return tag(obj, aid, role, collision)


def torus(col, name, loc, major, minor, mat, aid, role, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_torus_add(major_radius=major, minor_radius=minor, major_segments=32, minor_segments=8, location=loc, rotation=rot)
    obj = bpy.context.object
    obj.name = name
    set_material(obj, mat)
    relink(obj, col)
    return tag(obj, aid, role)


def curve(col, name, points, radius, mat, aid, role):
    data = bpy.data.curves.new(name + "_CURVE", "CURVE")
    data.dimensions = "3D"
    data.bevel_depth = radius
    data.bevel_resolution = 2
    spline = data.splines.new("POLY")
    spline.points.add(len(points) - 1)
    for point, xyz in zip(spline.points, points):
        point.co = (*xyz, 1)
    obj = bpy.data.objects.new(name, data)
    col.objects.link(obj)
    set_material(obj, mat)
    return tag(obj, aid, role)


def empty(col, name, loc, aid, role):
    obj = bpy.data.objects.new(name, None)
    obj.location = loc
    col.objects.link(obj)
    return tag(obj, aid, role)


def armature(col, name, bones, aid):
    data = bpy.data.armatures.new(name + "_DATA")
    obj = bpy.data.objects.new(name, data)
    col.objects.link(obj)
    tag(obj, aid, "enemy_armature", collision="none")
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.mode_set(mode="EDIT")
    made = {}
    for bname, head, tail, parent in bones:
        b = data.edit_bones.new(bname)
        b.head = head
        b.tail = tail
        if parent and parent in made:
            b.parent = made[parent]
        made[bname] = b
    bpy.ops.object.mode_set(mode="OBJECT")
    obj.select_set(False)
    return obj


def supersede_old_proxies():
    legacy_ids = {"PEL-EN-DIVER", "PEL-EN-POLYP", "PEL-EN-EEL"}
    hidden = []
    for obj in bpy.data.objects:
        if str(obj.get("asset_id", "")) in legacy_ids:
            obj.hide_render = True
            obj.hide_viewport = True
            obj["production_state"] = "SUPERSEDED_ENEMY_PROXY"
            obj["exclude_from_delivery"] = True
            hidden.append(obj.name)
    return hidden


def build_diver(col, mats):
    aid = "PEL-EN-DIVER-PROD-001"
    ivory, bronze, dark, _coral, _mem, mineral, textile, red = mats
    x, y, z = 320.0, 70.0, 7.0
    bones = [
        ("root", (x, y, z), (x, y, z + 0.2), None),
        ("pelvis", (x, y, z + 0.85), (x, y, z + 1.0), "root"),
        ("spine", (x, y, z + 1.0), (x, y, z + 1.45), "pelvis"),
        ("head", (x, y, z + 1.45), (x, y, z + 1.9), "spine"),
    ]
    for side, s in (("L", 1), ("R", -1)):
        bones += [
            (f"upper_arm_{side}", (x, y + s * 0.18, z + 1.4), (x, y + s * 0.48, z + 1.15), "spine"),
            (f"forearm_{side}", (x, y + s * 0.48, z + 1.15), (x, y + s * 0.62, z + 0.92), f"upper_arm_{side}"),
            (f"thigh_{side}", (x, y + s * 0.13, z + 0.84), (x, y + s * 0.16, z + 0.45), "pelvis"),
            (f"shin_{side}", (x, y + s * 0.16, z + 0.45), (x, y + s * 0.16, z + 0.10), f"thigh_{side}"),
        ]
    armature(col, "PEL_DIV_RIG", bones, aid)
    cylinder(col, "PEL_DIV_Torso", (x, y, z + 1.24), 0.36, 0.65, textile, aid, "pressure_suit_torso", 16)
    sphere(col, "PEL_DIV_Helmet", (x, y, z + 1.75), (0.34, 0.31, 0.30), ivory, aid, "pressure_helmet")
    torus(col, "PEL_DIV_HelmetSeal", (x, y, z + 1.55), 0.28, 0.045, bronze, aid, "helmet_pressure_seal")
    box(col, "PEL_DIV_ChestPlate", (x, y - 0.33, z + 1.30), (0.5, 0.12, 0.4), ivory, aid, "ceramic_chest_plate", bevel=0.05)
    for s in (-1, 1):
        cylinder(col, f"PEL_DIV_UpperArm_{s}", (x, y + s * 0.40, z + 1.25), 0.12, 0.50, textile, aid, "pressure_suit_upper_arm", 14, (math.radians(25), 0, 0))
        cylinder(col, f"PEL_DIV_Forearm_{s}", (x, y + s * 0.58, z + 1.00), 0.105, 0.42, dark, aid, "pressure_suit_forearm", 14, (math.radians(18), 0, 0))
        cylinder(col, f"PEL_DIV_Thigh_{s}", (x, y + s * 0.15, z + 0.62), 0.15, 0.55, textile, aid, "pressure_suit_thigh", 14)
        cylinder(col, f"PEL_DIV_Shin_{s}", (x, y + s * 0.15, z + 0.24), 0.13, 0.45, dark, aid, "pressure_suit_shin", 14)
        box(col, f"PEL_DIV_Foot_{s}", (x + 0.12, y + s * 0.15, z + 0.02), (0.42, 0.24, 0.12), mineral, aid, "reef_grip_boot", bevel=0.04)
    box(col, "PEL_DIV_Backpack", (x + 0.30, y, z + 1.28), (0.38, 0.60, 0.72), dark, aid, "life_support_ballast_pack", bevel=0.07)
    for s in (-1, 1):
        cylinder(col, f"PEL_DIV_Tank_{s}", (x + 0.52, y + s * 0.19, z + 1.28), 0.10, 0.62, bronze, aid, "compressed_gas_tank", 12)
    box(col, "PEL_DIV_HarpoonBody", (x - 0.02, y - 0.72, z + 1.02), (0.22, 0.72, 0.22), ivory, aid, "harpoon_launcher", bevel=0.035)
    cylinder(col, "PEL_DIV_HarpoonBarrel", (x - 0.02, y - 1.12, z + 1.02), 0.065, 0.62, bronze, aid, "harpoon_barrel", 14, (math.pi / 2, 0, 0))
    torus(col, "PEL_DIV_CableSpool", (x + 0.04, y - 0.55, z + 0.86), 0.16, 0.045, bronze, aid, "harpoon_cable_spool", (math.pi / 2, 0, 0))
    curve(col, "PEL_DIV_Tether_A", [(x - 0.02, y - 1.43, z + 1.02), (x - 0.1, y - 1.8, z + 0.95), (x - 0.2, y - 2.18, z + 0.88)], 0.025, dark, aid, "harpoon_tether_segment")
    sphere(col, "PEL_DIV_TetherCutCoupler", (x - 0.2, y - 2.18, z + 0.88), (0.075, 0.075, 0.075), red, aid, "cuttable_tether_coupler")
    curve(col, "PEL_DIV_Tether_B", [(x - 0.2, y - 2.18, z + 0.88), (x - 0.28, y - 2.65, z + 0.80), (x - 0.4, y - 3.05, z + 0.76)], 0.025, dark, aid, "harpoon_tether_segment")
    cylinder(col, "PEL_DIV_HarpoonHead", (x - 0.4, y - 3.18, z + 0.76), 0.07, 0.34, bronze, aid, "harpoon_head", 12, (math.pi / 2, 0, 0))
    proxy = cylinder(col, "PEL_DIV_COLLISION", (x, y, z + 0.95), 0.42, 1.9, red, aid, "collision_proxy_body", 12, collision="primitive_proxy")
    proxy.hide_render = True
    proxy.display_type = "WIRE"
    meta = empty(col, "PEL_DIV_METADATA", (x, y, z), aid, "enemy_metadata")
    meta["canon_enemy"] = "Buzo de extracción: arpón con cable que se puede cortar"
    meta["height_m_proposal"] = 1.90
    meta["rig_status"] = "ARMATURE_FOUNDATION_NO_SKIN_WEIGHTS"
    meta["cable_cut_interface"] = "breakaway coupler between two separate tether segments"
    meta["locomotion"] = "HUMANOID_DIVER_PROPOSAL"
    meta["engine_status"] = "NOT_IMPORTED"


def build_polyp(col, mats):
    aid = "PEL-EN-POLYP-PROD-001"
    _ivory, _bronze, _dark, coral, memory, mineral, _textile, red = mats
    x, y, z = 260.0, -80.0, 8.0
    sphere(col, "PEL_POL_Core", (x, y, z + 1.2), (1.15, 1.15, 1.55), coral, aid, "contractile_core")
    cylinder(col, "PEL_POL_BasalDisk", (x, y, z + 0.05), 1.35, 0.25, mineral, aid, "mineralized_basal_disk", 24)
    bones = [("root", (x, y, z), (x, y, z + 0.25), None), ("core", (x, y, z + 0.25), (x, y, z + 1.4), "root")]
    for i in range(6):
        a = 2 * math.pi * i / 6
        bones.append((f"arm_{i}", (x + math.cos(a) * 0.8, y + math.sin(a) * 0.8, z + 1.15), (x + math.cos(a) * 2.7, y + math.sin(a) * 2.7, z + 0.8), "core"))
    armature(col, "PEL_POL_RIG", bones, aid)
    for i in range(6):
        a = 2 * math.pi * i / 6
        pts = [(x + math.cos(a) * 0.7, y + math.sin(a) * 0.7, z + 1.15), (x + math.cos(a) * 1.5, y + math.sin(a) * 1.5, z + 1.35), (x + math.cos(a) * 2.4, y + math.sin(a) * 2.4, z + 0.78)]
        curve(col, f"PEL_POL_Arm_{i}", pts, 0.18, coral, aid, "polyp_guard_arm")
        sphere(col, f"PEL_POL_ContactPad_{i}", pts[-1], (0.34, 0.34, 0.14), mineral, aid, "reef_contact_pad")
        box(col, f"PEL_POL_AcousticPlate_{i}", (x + math.cos(a) * 1.25, y + math.sin(a) * 1.25, z + 1.55), (0.38, 0.12, 0.48), memory, aid, "dissonance_receptor_plate", (0, 0, a), 0.04, "none")
    for i in range(8):
        a = 2 * math.pi * i / 8
        sphere(col, f"PEL_POL_SensoryBud_{i}", (x + math.cos(a) * 0.82, y + math.sin(a) * 0.82, z + 2.25), (0.18, 0.18, 0.28), memory, aid, "acoustic_sensory_bud")
    proxy = cylinder(col, "PEL_POL_COLLISION", (x, y, z + 1.1), 1.2, 2.3, red, aid, "collision_proxy_core", 16, collision="primitive_proxy")
    proxy.hide_render = True
    proxy.display_type = "WIRE"
    meta = empty(col, "PEL_POL_METADATA", (x, y, z), aid, "enemy_metadata")
    meta["canon_enemy"] = "Guardia de pólipos: protege zonas acústicas, retrocede ante disonancia aprendida"
    meta["movement_model"] = "SEMI_SESSILE_SIX_CONTACT_CONTRACTILE_PROPOSAL"
    meta["dissonance_readability"] = "six outward receptor plates + sensory crown"
    meta["rig_status"] = "ARMATURE_FOUNDATION_NO_SKIN_WEIGHTS"
    meta["engine_status"] = "NOT_IMPORTED"


def build_sentinel(col, mats):
    aid = "PEL-EN-EEL-PROD-001"
    _ivory, _bronze, _dark, coral, memory, mineral, _textile, red = mats
    origin = Vector((400.0, -150.0, 12.0))
    length = 8.2
    segments = 12
    bones = []
    for i in range(segments):
        hx = origin.x - length / 2 + i * (length / segments)
        tx = origin.x - length / 2 + (i + 1) * (length / segments)
        bones.append((f"spine_{i:02d}", (hx, origin.y, origin.z), (tx, origin.y, origin.z), f"spine_{i-1:02d}" if i > 0 else None))
    armature(col, "PEL_SENT_RIG", bones, aid)
    for i in range(segments):
        t = i / (segments - 1)
        xx = origin.x - length / 2 + (i + 0.5) * (length / segments)
        rr = max(0.16, 0.48 * (1 - 0.58 * abs(t - 0.45) / 0.55))
        cylinder(col, f"PEL_SENT_BodySeg_{i:02d}", (xx, origin.y, origin.z), rr, length / segments * 0.94, coral, aid, "sentinel_body_segment", 16, (0, math.pi / 2, 0), "none")
        if i in (2, 4, 6, 8, 10):
            sphere(col, f"PEL_SENT_LateralNode_{i:02d}", (xx, origin.y - 0.48, origin.z), (0.10, 0.07, 0.10), memory, aid, "charge_path_lateral_node")
    sphere(col, "PEL_SENT_Head", (origin.x + length / 2 + 0.25, origin.y, origin.z), (0.72, 0.55, 0.50), coral, aid, "sentinel_head")
    for s in (-1, 1):
        box(col, f"PEL_SENT_Jaw_{s}", (origin.x + length / 2 + 0.52, origin.y + s * 0.22, origin.z - 0.06), (0.58, 0.16, 0.18), mineral, aid, "jaw_plate", (0, 0, s * 0.12), 0.04)
    for i in (3, 6, 9):
        xx = origin.x - length / 2 + (i + 0.5) * (length / segments)
        box(col, f"PEL_SENT_Fin_{i}", (xx, origin.y, origin.z + 0.48), (0.75, 0.08, 0.52), memory, aid, "acoustic_stabilizer_fin", bevel=0.04, collision="none")
    sphere(col, "PEL_SENT_AnchorSensor", (origin.x + length / 2 + 0.72, origin.y, origin.z + 0.14), (0.18, 0.18, 0.18), memory, aid, "anchor_field_sensor")
    torus(col, "PEL_SENT_TelegraphRing", (origin.x + length / 2 - 0.05, origin.y, origin.z), 0.54, 0.055, memory, aid, "charge_telegraph_ring", (0, math.pi / 2, 0))
    for i in range(4):
        xx = origin.x - length / 2 + (i + 0.5) * (length / 4)
        proxy = cylinder(col, f"PEL_SENT_COLLISION_{i}", (xx, origin.y, origin.z), 0.45, length / 4 * 0.9, red, aid, "collision_proxy_segment", 12, (0, math.pi / 2, 0), "compound_proxy")
        proxy.hide_render = True
        proxy.display_type = "WIRE"
    meta = empty(col, "PEL_SENT_METADATA", origin, aid, "enemy_metadata")
    meta["canon_enemy"] = "Anguila centinela: carga entre anclajes, con recorrido visible"
    meta["length_m_proposal"] = 8.2
    meta["movement_model"] = "ANGUILLIFORM_SPINE_CHAIN_PROPOSAL"
    meta["charge_readability"] = "lateral mnemonic nodes + head telegraph ring; gameplay path requires engine implementation"
    meta["rig_status"] = "12_BONE_SPINE_FOUNDATION_NO_SKIN_WEIGHTS"
    meta["engine_status"] = "NOT_IMPORTED"


def build():
    col = ensure_collection()
    mats = (
        material("PEL_MAT_IvoryCeramic_Marine", "PEL_Human_IvoryCeramic"),
        material("PEL_MAT_Bronze_Oxidized_Marine", "PEL_Precursor_Bronze"),
        material("PEL_MAT_DarkTechnicalComposite", "PEL_TechnicalFabric"),
        material("PEL_MAT_LivingCoral_Tissue", "PEL_LivingCoral"),
        material("PEL_MAT_MemoryCyan_Biolum", "PEL_Memory_Cyan"),
        material("PEL_MAT_BlackMineral_Wet", "PEL_Seabed_BlackMineral"),
        material("PEL_MAT_WaterproofTextile", "PEL_TechnicalFabric"),
        material("PEL_Hostile_Vermilion", "PEL_MAT_Bronze_Oxidized_Marine"),
    )
    hidden = supersede_old_proxies()
    build_diver(col, mats)
    build_polyp(col, mats)
    build_sentinel(col, mats)
    bpy.context.view_layer.update()
    return {
        "checkpoint": "PELAGOS-ENEMIES-001",
        "collection": COLLECTION,
        "legacy_proxies_hidden": hidden,
        "object_count": len(col.objects),
        "mesh_count": len([o for o in col.objects if o.type == "MESH"]),
        "armature_count": len([o for o in col.objects if o.type == "ARMATURE"]),
        "pending": [
            "structural and silhouette QA",
            "final sculpt/retopology",
            "UV/bake/final PBR",
            "skin weights/deformation",
            "combat animation/behavior",
            "engine hitboxes/collision",
            "LOD/performance",
            "human art review",
        ],
    }


if __name__ == "__main__":
    result = build()
    print(result)
