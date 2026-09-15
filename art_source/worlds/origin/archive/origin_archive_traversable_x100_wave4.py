"""EXOVANT 2950 — ORIGIN / Archivo Wave 04 traversable grammar.

Run after `origin_archive_x100_wave1.py` + `origin_lod_x100_wave2.py`.
Rebuilds the four stable Archive assemblies with corrected child-local transforms,
continuous player decks, and collision semantics suitable for native CharacterBody
qualification. Visual source/LOD mesh geometry is not modified.

Claim: CLM-ORIGIN-ARCH-ARCHIVE-NATIVE-001
Dimensions/layout remain PROPOSAL_UNTIL_GODOT.
"""

import bpy
import json
import math
from mathutils import Matrix, Vector

GRAMMAR_CLAIM = "CLM-ORIGIN-ARCH-ARCHIVE-GRAMMAR-001"
NATIVE_CLAIM = "CLM-ORIGIN-ARCH-ARCHIVE-NATIVE-001"
COLLECTION = "80_ORIGIN_ARCHIVE_ASSEMBLIES"

ROOTS = {
    "ORG_ARC_ASM_WITNESS_GALLERY_A": ((-48.0, 62.0, 0.0), 5101, "witness_gallery_v2"),
    "ORG_ARC_ASM_VAULT_JUNCTION_A": ((0.0, 62.0, 0.0), 5102, "vault_junction_v2"),
    "ORG_ARC_ASM_MEMORY_NAVE_A": ((48.0, 62.0, 0.0), 5103, "memory_nave_v2"),
    "ORG_ARC_ASM_SCAR_THRESHOLD_A": ((0.0, 100.0, 0.0), 5104, "scar_threshold_v2"),
}


def _box_faces(x0, x1, y0, y1, z0, z1):
    verts = [
        (x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0),
        (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1),
    ]
    faces = [(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]
    return verts, faces


def _replace_mesh(obj, verts, faces, suffix):
    old = obj.data
    mesh = bpy.data.meshes.new(obj.name + "_" + suffix)
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    for material in old.materials:
        mesh.materials.append(material)
    obj.data = mesh
    if old.users == 0:
        bpy.data.meshes.remove(old)


def _top_only(collider):
    bb = [Vector(c) for c in collider.bound_box]
    x0, x1 = min(p.x for p in bb), max(p.x for p in bb)
    y0, y1 = min(p.y for p in bb), max(p.y for p in bb)
    z = max(p.z for p in bb)
    _replace_mesh(collider, [(x0,y0,z),(x1,y0,z),(x1,y1,z),(x0,y1,z)], [(0,1,2,3)], "TOP_ONLY")
    collider["collision_semantics"] = "walkable_top_surface_only_upward_v2"


def _open_frame(asset_parent, collider, tokens):
    verts, faces = [], []
    parent_inv = asset_parent.matrix_world.inverted_safe()
    for token in tokens:
        matches = [
            o for o in asset_parent.children_recursive
            if o.type == "MESH" and token in o.name and not o.name.startswith("COL_")
        ]
        if not matches:
            continue
        obj = matches[0]
        pts = [parent_inv @ (obj.matrix_world @ Vector(c)) for c in obj.bound_box]
        x0, x1 = min(p.x for p in pts), max(p.x for p in pts)
        y0, y1 = min(p.y for p in pts), max(p.y for p in pts)
        z0, z1 = min(p.z for p in pts), max(p.z for p in pts)
        bv, bf = _box_faces(x0, x1, y0, y1, z0, z1)
        offset = len(verts)
        verts.extend(bv)
        faces.extend([tuple(offset + i for i in face) for face in bf])
    if not faces:
        raise RuntimeError(f"No visual parts found for open-frame collider {asset_parent.name}")
    _replace_mesh(collider, verts, faces, "OPEN_FRAME")
    collider["collision_semantics"] = "open_frame_visual_proxy_v2"


def fix_source_collision_semantics():
    for aid in ["ORG_ARC_FLOOR_SPINE_A", "ORG_ARC_FLOOR_SPINE_B", "ORG_ARC_THRESHOLD_A", "ORG_ARC_THRESHOLD_B"]:
        parent = bpy.data.objects.get(aid)
        collider = bpy.data.objects.get("COL_" + aid)
        if not parent or not collider:
            raise RuntimeError("Missing walkable source collider: " + aid)
        _top_only(collider)
    for aid in ["ORG_ARC_RIB_WALL_A", "ORG_ARC_RIB_WALL_B", "ORG_ARC_RIB_WALL_C"]:
        parent = bpy.data.objects.get(aid)
        collider = bpy.data.objects.get("COL_" + aid)
        if not parent or not collider:
            raise RuntimeError("Missing rib source collider: " + aid)
        _open_frame(parent, collider, ["PIER_-1", "PIER_1", "LINTEL"])
    for aid in ["ORG_ARC_VAULT_FRAME_A", "ORG_ARC_VAULT_FRAME_B", "ORG_ARC_VAULT_FRAME_C"]:
        parent = bpy.data.objects.get(aid)
        collider = bpy.data.objects.get("COL_" + aid)
        if not parent or not collider:
            raise RuntimeError("Missing vault source collider: " + aid)
        _open_frame(parent, collider, ["JAMB_-1", "JAMB_1", "HEADER"])


def _collection():
    coll = bpy.data.collections.get(COLLECTION)
    if coll is None:
        coll = bpy.data.collections.new(COLLECTION)
        bpy.context.scene.collection.children.link(coll)
    return coll


def _purge_assemblies():
    for assembly_id in ROOTS:
        root = bpy.data.objects.get(assembly_id)
        if root is None:
            continue
        descendants = list(root.children_recursive)
        for obj in reversed(descendants):
            bpy.data.objects.remove(obj, do_unlink=True)
        bpy.data.objects.remove(root, do_unlink=True)


def _source_parent(asset_id):
    parent = bpy.data.objects.get(asset_id)
    if parent is None:
        raise RuntimeError("Missing source asset: " + asset_id)
    return parent


def _source_meshes(parent):
    return sorted(
        [o for o in parent.children_recursive if o.type == "MESH" and not o.name.startswith(("LOD1__", "LOD2__"))],
        key=lambda o: o.name,
    )


def _copy_props(src, dst):
    for key in src.keys():
        try:
            dst[key] = src[key]
        except Exception:
            pass


def _add_module(root, collection, index, asset_id, location, rotation_deg):
    parent = _source_parent(asset_id)
    module = bpy.data.objects.new(f"{root.name}__MOD_{index:03d}__{asset_id}", None)
    collection.objects.link(module)
    module.parent = root
    module.matrix_parent_inverse = Matrix.Identity(4)
    module.location = Vector(location)
    module.rotation_euler[2] = math.radians(rotation_deg)
    module["origin_archive_assembly_generated"] = True
    module["origin_source_asset_id"] = asset_id
    module["origin_claim_id"] = GRAMMAR_CLAIM

    source_parent_inverse = parent.matrix_world.inverted_safe()
    for child_index, src in enumerate(_source_meshes(parent)):
        inst = bpy.data.objects.new(f"{root.name}__M{index:03d}__{child_index:02d}__{src.name}", src.data)
        collection.objects.link(inst)
        inst.parent = module
        inst.matrix_parent_inverse = Matrix.Identity(4)
        # Critical Wave04 fix: source child relative to source asset parent.
        # Do NOT repeat module placement in the child local transform.
        inst.matrix_local = source_parent_inverse @ src.matrix_world
        _copy_props(src, inst)
        inst["origin_archive_assembly_generated"] = True
        inst["origin_source_asset_id"] = asset_id
        inst["origin_claim_id"] = GRAMMAR_CLAIM


def _long_grid(asset_id, centers, x_offsets):
    return [(asset_id, (x, y, 0.0), 90.0) for y in centers for x in x_offsets]


def _vault_cross():
    rows = []
    axis = [-6.75, -4.5, -2.25, 0.0, 2.25, 4.5, 6.75]
    lanes = [-1.4, 0.0, 1.4]
    rows += [("ORG_ARC_FLOOR_SPINE_A", (x, y, 0.0), 90.0) for y in axis for x in lanes]
    rows += [("ORG_ARC_FLOOR_SPINE_A", (x, y, 0.0), 0.0) for x in axis if abs(x) > 0.01 for y in lanes]
    return rows


def recipes():
    r = {}
    witness = _long_grid("ORG_ARC_FLOOR_SPINE_B", [-14,-10.5,-7,-3.5,0,3.5,7,10.5,14], [-1.4,0,1.4])
    for y in [-10.5,-3.5,3.5,10.5]:
        witness += [("ORG_ARC_RIB_WALL_B", (0,y,0), 0), ("ORG_ARC_CEILING_RIB_B", (0,y,0), 0)]
    for y in [-8,-4,4,8]:
        witness += [("ORG_ARC_MEMORY_CELL_A", (-3.7,y,0), 0), ("ORG_ARC_MEMORY_CELL_A", (3.7,y,0), 0)]
    witness += [("ORG_ARC_THRESHOLD_A", (0,-16,0), 0), ("ORG_ARC_THRESHOLD_A", (0,16,0), 180)]
    r["ORG_ARC_ASM_WITNESS_GALLERY_A"] = witness

    vault = _vault_cross()
    for pos, deg in [((0,-7.2,0),0),((0,7.2,0),180),((-7.2,0,0),-90),((7.2,0,0),90)]:
        vault.append(("ORG_ARC_VAULT_FRAME_B", pos, deg))
    for pos, deg in [((0,-8.5,0),0),((0,8.5,0),180),((-8.5,0,0),-90),((8.5,0,0),90)]:
        vault.append(("ORG_ARC_BRIDGE_SOCKET_B", pos, deg))
    vault += [
        ("ORG_ARC_ARCHIVE_CORE_SHELL_A", (4.8,4.8,0), 0),
        ("ORG_ARC_MEMORY_CELL_B", (-4.8,4.8,0), 0),
        ("ORG_ARC_MEMORY_CELL_B", (4.8,-4.8,0), 180),
        ("ORG_ARC_CEILING_RIB_C", (0,0,0), 0),
    ]
    r["ORG_ARC_ASM_VAULT_JUNCTION_A"] = vault

    nave = _long_grid("ORG_ARC_FLOOR_SPINE_B", [-15.75,-12.25,-8.75,-5.25,-1.75,1.75,5.25,8.75,12.25,15.75], [-1.4,0,1.4])
    for y in [-12,-4,4,12]:
        nave += [("ORG_ARC_RIB_WALL_C", (0,y,0), 0), ("ORG_ARC_CEILING_RIB_C", (0,y,0), 0)]
    for y in [-10,-6,-2,2,6,10]:
        nave += [("ORG_ARC_MEMORY_CELL_C", (-3.9,y,0), 0), ("ORG_ARC_MEMORY_CELL_C", (3.9,y,0), 0)]
    nave += [
        ("ORG_ARC_VAULT_FRAME_C", (0,-17,0), 0), ("ORG_ARC_VAULT_FRAME_C", (0,17,0), 180),
        ("ORG_ARC_THRESHOLD_B", (0,-17.75,0), 0), ("ORG_ARC_THRESHOLD_B", (0,17.75,0), 180),
        ("ORG_ARC_ARCHIVE_CORE_SHELL_B", (4.8,0,0), 0),
    ]
    r["ORG_ARC_ASM_MEMORY_NAVE_A"] = nave

    scar = _long_grid("ORG_ARC_FLOOR_SPINE_A", [-6.75,-4.5,-2.25,0,2.25,4.5,6.75], [-1.4,0,1.4])
    scar += [
        ("ORG_ARC_THRESHOLD_B", (0,-8.3,0), 0),
        ("ORG_ARC_VAULT_FRAME_B", (0,-7,0), 0),
        ("ORG_ARC_RIB_WALL_A", (0,0,0), 0),
        ("ORG_ARC_CEILING_RIB_A", (0,0,0), 0),
        ("ORG_ARC_BRIDGE_SOCKET_C", (0,8.5,0), 180),
        ("ORG_ARC_MEMORY_CELL_A", (-3.7,3,0), 0),
        ("ORG_ARC_MEMORY_CELL_A", (3.7,3,0), 0),
    ]
    r["ORG_ARC_ASM_SCAR_THRESHOLD_A"] = scar
    return r


def build():
    fix_source_collision_semantics()
    _purge_assemblies()
    coll = _collection()
    recipe_map = recipes()
    report = {}

    for assembly_id, (root_location, seed, archetype) in ROOTS.items():
        root = bpy.data.objects.new(assembly_id, None)
        coll.objects.link(root)
        root.location = root_location
        root["asset_id"] = assembly_id
        root["claim_id"] = GRAMMAR_CLAIM
        root["native_qualification_claim"] = NATIVE_CLAIM
        root["archetype"] = archetype
        root["seed"] = seed
        root["truth_state"] = "authored_traversable_candidate"
        root["dimension_status"] = "PROPOSAL_UNTIL_GODOT"
        root["player_capsule_diameter_m"] = 0.76
        root["minimum_main_deck_clear_width_m"] = 4.3
        root["minimum_narrow_passage_width_m"] = 2.0 if "WITNESS" in assembly_id else 2.75
        recipe = recipe_map[assembly_id]
        root["recipe"] = json.dumps([(a, list(loc), deg) for a, loc, deg in recipe])
        for index, (asset_id, location, rotation_deg) in enumerate(recipe):
            _add_module(root, coll, index, asset_id, location, rotation_deg)

        descendants = list(root.children_recursive)
        meshes = [o for o in descendants if o.type == "MESH"]
        colliders = [o for o in meshes if "__COL_" in o.name]
        walkable = [o for o in colliders if o.get("family") in {"archive_floor_spine", "archive_threshold"}]
        report[assembly_id] = {
            "modules": len([o for o in root.children if o.type == "EMPTY"]),
            "meshes": len(meshes),
            "colliders": len(colliders),
            "walkable_colliders": len(walkable),
            "seed": seed,
        }

    scene = bpy.context.scene
    scene["origin_archive_wave4_claim"] = NATIVE_CLAIM
    scene["origin_archive_collision_semantics"] = "floor_threshold_top_only; rib_vault_open_frame"
    scene["origin_archive_dimension_status"] = "PROPOSAL_UNTIL_GODOT"
    return report


if __name__ == "__main__":
    print(json.dumps(build(), indent=2))
