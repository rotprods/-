"""Build Damián Vo character rig foundation for Pelagos.

Blender 5.2+, metres. Canon only defines Damián as buoy captain who needs a trade channel.
Age, ethnicity, face, hair, exact body dimensions and equipment details remain proposals/TBD.
"""
import bpy
import math

ROOT = "PELAGOS_WORLD"
COLLECTION = "62_DAMIAN_HERO_V1"
ASSET_ID = "PEL-NPC-DAMIAN"
STATE = "CHARACTER_RIG_FOUNDATION_V1"
ORIGIN = (-455.0, -105.0, 16.0)


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


def tag(obj, role, collision="none"):
    obj["asset_id"] = ASSET_ID
    obj["world"] = "pelagos"
    obj["role"] = role
    obj["production_state"] = STATE
    obj["quality_tier"] = "A"
    obj["collision_intent"] = collision
    return obj


def relink(obj, col):
    for old in list(obj.users_collection):
        old.objects.unlink(obj)
    col.objects.link(obj)
    return obj


def set_material(obj, mat):
    if hasattr(obj.data, "materials") and not obj.data.materials:
        obj.data.materials.append(mat)


def box(col, name, loc, dims, mat, role, rot=(0, 0, 0), bevel=0.04):
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
    return tag(obj, role)


def cylinder(col, name, loc, radius, depth, mat, role, vertices=16, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=loc, rotation=rot)
    obj = bpy.context.object
    obj.name = name
    set_material(obj, mat)
    relink(obj, col)
    return tag(obj, role)


def sphere(col, name, loc, scale, mat, role):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=20, ring_count=10, location=loc)
    obj = bpy.context.object
    obj.name = name
    obj.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    set_material(obj, mat)
    relink(obj, col)
    return tag(obj, role)


def torus(col, name, loc, major, minor, mat, role):
    bpy.ops.mesh.primitive_torus_add(major_radius=major, minor_radius=minor, major_segments=32, minor_segments=8, location=loc)
    obj = bpy.context.object
    obj.name = name
    set_material(obj, mat)
    relink(obj, col)
    return tag(obj, role)


def curve(col, name, points, radius, mat, role):
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
    return tag(obj, role)


def metadata(col, name, loc):
    obj = bpy.data.objects.new(name, None)
    obj.location = loc
    col.objects.link(obj)
    return tag(obj, "character_metadata")


def armature(col, origin):
    x, y, z = origin
    data = bpy.data.armatures.new("PEL_DAMIAN_RIG_DATA")
    obj = bpy.data.objects.new("PEL_DAMIAN_RIG", data)
    col.objects.link(obj)
    tag(obj, "character_armature")
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.mode_set(mode="EDIT")
    bones = [
        ("root", (x, y, z), (x, y, z + 0.18), None),
        ("pelvis", (x, y, z + 0.82), (x, y, z + 0.98), "root"),
        ("spine_01", (x, y, z + 0.98), (x, y, z + 1.28), "pelvis"),
        ("spine_02", (x, y, z + 1.28), (x, y, z + 1.48), "spine_01"),
        ("neck", (x, y, z + 1.48), (x, y, z + 1.58), "spine_02"),
        ("head", (x, y, z + 1.58), (x, y, z + 1.82), "neck"),
    ]
    for side, s in (("L", 1), ("R", -1)):
        bones += [
            (f"clavicle_{side}", (x, y, z + 1.43), (x, y + s * 0.16, z + 1.43), "spine_02"),
            (f"upper_arm_{side}", (x, y + s * 0.16, z + 1.43), (x, y + s * 0.45, z + 1.2), f"clavicle_{side}"),
            (f"forearm_{side}", (x, y + s * 0.45, z + 1.2), (x, y + s * 0.60, z + 0.97), f"upper_arm_{side}"),
            (f"hand_{side}", (x, y + s * 0.60, z + 0.97), (x, y + s * 0.66, z + 0.88), f"forearm_{side}"),
            (f"thigh_{side}", (x, y + s * 0.12, z + 0.82), (x, y + s * 0.15, z + 0.45), "pelvis"),
            (f"shin_{side}", (x, y + s * 0.15, z + 0.45), (x, y + s * 0.15, z + 0.12), f"thigh_{side}"),
            (f"foot_{side}", (x, y + s * 0.15, z + 0.12), (x + 0.18, y + s * 0.15, z + 0.05), f"shin_{side}"),
        ]
    made = {}
    for bname, head, tail, parent in bones:
        b = data.edit_bones.new(bname)
        b.head = head
        b.tail = tail
        if parent:
            b.parent = made[parent]
        made[bname] = b
    bpy.ops.object.mode_set(mode="OBJECT")
    obj.select_set(False)
    return obj


def supersede_proxy():
    hidden = []
    for obj in bpy.data.objects:
        if str(obj.get("asset_id", "")) == ASSET_ID and obj.name.startswith("PEL_NPC_Damian"):
            obj.hide_render = True
            obj.hide_viewport = True
            obj["production_state"] = "SUPERSEDED_NPC_PROXY"
            obj["exclude_from_delivery"] = True
            hidden.append(obj.name)
    return hidden


def build():
    col = ensure_collection()
    old_proxy = supersede_proxy()
    ivory = material("PEL_MAT_IvoryCeramic_Marine", "PEL_Human_IvoryCeramic")
    bronze = material("PEL_MAT_Bronze_Oxidized_Marine", "PEL_Precursor_Bronze")
    dark = material("PEL_MAT_DarkTechnicalComposite", "PEL_TechnicalFabric")
    textile = material("PEL_MAT_WaterproofTextile", "PEL_TechnicalFabric")
    memory = material("PEL_MAT_MemoryCyan_Biolum", "PEL_Memory_Cyan")
    mineral = material("PEL_MAT_BlackMineral_Wet", "PEL_Seabed_BlackMineral")
    amber = material("PEL_Refuge_Amber")
    x, y, z = ORIGIN
    armature(col, ORIGIN)
    cylinder(col, "PEL_DAMIAN_Torso", (x, y, z + 1.2), 0.30, 0.58, textile, "waterproof_suit_torso")
    sphere(col, "PEL_DAMIAN_Head", (x, y, z + 1.68), (0.23, 0.22, 0.27), ivory, "head_proxy")
    sphere(col, "PEL_DAMIAN_Pelvis", (x, y, z + 0.82), (0.28, 0.22, 0.20), dark, "body_pelvis")
    for s in (-1, 1):
        cylinder(col, f"PEL_DAMIAN_UpperArm_{s}", (x, y + s * 0.32, z + 1.27), 0.105, 0.46, textile, "waterproof_suit_upper_arm", 14, (math.radians(24), 0, 0))
        cylinder(col, f"PEL_DAMIAN_Forearm_{s}", (x, y + s * 0.52, z + 1.04), 0.09, 0.40, dark, "waterproof_suit_forearm", 14, (math.radians(18), 0, 0))
        sphere(col, f"PEL_DAMIAN_Hand_{s}", (x, y + s * 0.64, z + 0.88), (0.10, 0.08, 0.11), ivory, "hand_proxy")
        cylinder(col, f"PEL_DAMIAN_Thigh_{s}", (x, y + s * 0.14, z + 0.61), 0.13, 0.50, textile, "waterproof_suit_thigh", 14)
        cylinder(col, f"PEL_DAMIAN_Shin_{s}", (x, y + s * 0.14, z + 0.26), 0.115, 0.42, dark, "waterproof_suit_shin", 14)
        box(col, f"PEL_DAMIAN_Boot_{s}", (x + 0.10, y + s * 0.14, z + 0.04), (0.38, 0.22, 0.13), mineral, "reef_grip_boot")
        box(col, f"PEL_DAMIAN_BootSole_{s}", (x + 0.13, y + s * 0.14, z - 0.01), (0.42, 0.24, 0.05), bronze, "mooring_deck_grip_sole", bevel=0.02)
        box(col, f"PEL_DAMIAN_FloatHarness_{s}", (x + 0.22, y + s * 0.25, z + 1.27), (0.18, 0.18, 0.44), amber, "emergency_flotation_harness")
    box(col, "PEL_DAMIAN_CaptainChestPlate", (x, y - 0.30, z + 1.25), (0.50, 0.10, 0.34), ivory, "repaired_ceramic_chest_plate", bevel=0.05)
    torus(col, "PEL_DAMIAN_PressureCollar", (x, y, z + 1.51), 0.23, 0.045, bronze, "pressure_seal_collar")
    box(col, "PEL_DAMIAN_RouteRadio", (x + 0.05, y + 0.39, z + 1.42), (0.28, 0.16, 0.32), dark, "buoy_route_radio")
    curve(col, "PEL_DAMIAN_RadioLead", [(x + 0.05, y + 0.39, z + 1.42), (x + 0.12, y + 0.25, z + 1.20), (x + 0.08, y + 0.16, z + 0.96)], 0.025, memory, "route_radio_lead")
    box(col, "PEL_DAMIAN_RouteLedger", (x - 0.02, y - 0.62, z + 1.02), (0.28, 0.08, 0.20), ivory, "trade_route_ledger")
    box(col, "PEL_DAMIAN_MooringKey", (x + 0.02, y - 0.30, z + 0.80), (0.12, 0.06, 0.30), bronze, "mooring_service_key", bevel=0.02)
    meta = metadata(col, "PEL_DAMIAN_METADATA", ORIGIN)
    meta["canon_identity"] = "Damián Vo / capitán de boyas / necesita un canal de comercio"
    meta["body_height_m_proposal"] = 1.76
    meta["body_anatomy_status"] = "HUMAN/HUMANOID PROXY; no non-human physiology claimed"
    meta["face_age_ethnicity"] = "UNDEFINED_BY_CANON"
    meta["wardrobe_status"] = "PELAGOS_CAPTAIN_ROLE_PROPOSAL_FROM_CANON_MATERIAL_LANGUAGE"
    meta["role_equipment_logic"] = "buoy route radio + route ledger + mooring service key + flotation harness support captain/commerce function"
    meta["rig_status"] = "20_BONE_ARMATURE_FOUNDATION_NO_SKIN_WEIGHTS"
    meta["engine_status"] = "NOT_IMPORTED"
    bpy.context.view_layer.update()
    return {
        "checkpoint": "PELAGOS-DAMIAN-001",
        "collection": COLLECTION,
        "object_count": len(col.objects),
        "mesh_count": len([o for o in col.objects if o.type == "MESH"]),
        "curve_count": len([o for o in col.objects if o.type == "CURVE"]),
        "armature_count": len([o for o in col.objects if o.type == "ARMATURE"]),
        "legacy_proxy_hidden": old_proxy,
        "pending": ["final character direction", "sculpt/retopo", "skin/deformation", "UV/PBR", "animation", "engine integration", "LOD/performance", "human art review"],
    }


if __name__ == "__main__":
    result = build()
    print(result)
